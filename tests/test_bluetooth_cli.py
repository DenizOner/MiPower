"""Regression tests for bluetoothctl interaction without starting Home Assistant."""

import importlib
from pathlib import Path
import re
import sys
import types
import unittest

import pexpect


ROOT = Path(__file__).resolve().parents[1]
# Load only the Bluetooth modules under test, avoiding HA integration startup.
for name in (
    "custom_components",
    "custom_components.mipower",
    "custom_components.mipower.services",
    "custom_components.mipower.services.bluetooth",
):
    package = types.ModuleType(name)
    package.__path__ = [str(ROOT.joinpath(*name.split(".")))]
    sys.modules.setdefault(name, package)

const = importlib.import_module("custom_components.mipower.const")
models = importlib.import_module("custom_components.mipower.models")
process_module = importlib.import_module(
    "custom_components.mipower.services.bluetooth.process_manager"
)
pair_module = importlib.import_module(
    "custom_components.mipower.services.bluetooth.pair_sender"
)
exceptions = importlib.import_module(
    "custom_components.mipower.services.bluetooth.exceptions"
)

MAC = "AA:BB:CC:DD:EE:FF"
OPTIONS = models.TimingOptions(25, 1.0, 0.05, 2.0, 0.15, 10, 1.0)


class PromptTests(unittest.TestCase):
    def test_supported_prompts(self):
        for prompt in (
            "[bluetooth]# ",
            "\x1b[0;94m[bluetooth]\x1b[0m# ",
            "[Living room projector]# ",
            "[bluetoothctl]> ",
        ):
            with self.subTest(prompt=prompt):
                self.assertIsNotNone(re.search(const.BLUETOOTHCTL_PROMPT, prompt))

    def test_device_change_notification_is_not_a_prompt(self):
        self.assertIsNone(
            re.search(const.BLUETOOTHCTL_PROMPT, f"[CHG] Device {MAC} Paired: yes\r\n")
        )


class PairingStateTests(unittest.TestCase):
    def run_info(self, response):
        # A real PTY exercises output consumption and prompt boundaries.
        script = (
            "import sys\n"
            "for line in sys.stdin:\n"
            " if line.strip() == 'quit': break\n"
            f" sys.stdout.write({response!r} + '[bluetooth]# ')\n"
            " sys.stdout.flush()\n"
        )
        manager = process_module.BluetoothProcessManager()
        manager._child = pexpect.spawn(
            sys.executable, ["-u", "-c", script], encoding="utf-8", echo=False
        )
        try:
            return manager.get_pairing_state(MAC, timeout=2)
        finally:
            manager.cleanup()

    def test_existing_pair_is_detected(self):
        self.assertIs(self.run_info(f"Device {MAC} (public)\n\tPaired: yes\n"), True)

    def test_unpaired_device_is_detected(self):
        self.assertIs(self.run_info(f"Device {MAC} (public)\n\tPaired: no\n"), False)

    def test_unknown_pairing_state_fails_closed(self):
        self.assertIsNone(self.run_info(f"Device {MAC} (public)\n\tConnected: no\n"))

    def test_unrelated_device_output_is_not_used(self):
        self.assertIsNone(
            self.run_info("Device 11:22:33:44:55:66 (public)\n\tPaired: no\n")
        )

    def test_stale_prompt_does_not_hide_target_info(self):
        self.assertIs(
            self.run_info(
                "[bluetooth]# Device 11:22:33:44:55:66 (public)\n\tPaired: no\n"
                f"Device {MAC} (public)\n\tPaired: yes\n"
            ),
            True,
        )

    def test_colored_pairing_state_is_detected(self):
        self.assertIs(
            self.run_info(f"Device {MAC} (public)\n\t\x1b[0;94mPaired: yes\x1b[0m\n"),
            True,
        )


class PairCommandTests(unittest.TestCase):
    def sender(self, state):
        class Manager:
            def __init__(self):
                self.commands = []

            def get_pairing_state(self, address, timeout):
                return state

            def send_command(self, command):
                self.commands.append(command)

        manager = Manager()
        return manager, pair_module.BluetoothPairSender(manager)

    def test_existing_pair_is_not_replaced(self):
        manager, sender = self.sender(True)
        result = sender.send_pair_command("Projector", "media_player.projector", MAC, OPTIONS)
        self.assertEqual(result, exceptions.TurnOnFailedReason.ALREADY_PAIRED)
        self.assertEqual(manager.commands, [])

    def test_unknown_state_does_not_send_pair(self):
        manager, sender = self.sender(None)
        result = sender.send_pair_command("Projector", "media_player.projector", MAC, OPTIONS)
        self.assertEqual(result, exceptions.TurnOnFailedReason.SIGNAL_FAILED)
        self.assertEqual(manager.commands, [])

    def test_unpaired_device_keeps_existing_wake_method(self):
        manager, sender = self.sender(False)
        self.assertIsNone(
            sender.send_pair_command("Projector", "media_player.projector", MAC, OPTIONS)
        )
        self.assertEqual(manager.commands, [f"pair {MAC}"])


if __name__ == "__main__":
    unittest.main()
