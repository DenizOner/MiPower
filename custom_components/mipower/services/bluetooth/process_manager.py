"""
Bluetooth process manager for MiPower integration.

This module handles the lifecycle of the bluetoothctl process,
following the Single Responsibility Principle.
"""

import logging
import re
from typing import Any

import pexpect  # type: ignore[import]

from ...const import BLUETOOTHCTL_COMMAND, BLUETOOTHCTL_PROMPT
from ...models import TimingOptions
from .exceptions import TurnOnFailedReason

_LOGGER = logging.getLogger(__name__)


class BluetoothProcessManager:
    """
    Manages the bluetoothctl process lifecycle.

    Handles spawning, monitoring, and cleanup of the bluetoothctl process.
    """

    def __init__(self) -> None:
        """Initialize the process manager."""
        self._child: pexpect.spawn[Any] | None = None

    def spawn_process(self, timing_options: TimingOptions) -> TurnOnFailedReason | None:
        """
        Spawn the bluetoothctl process.

        Args:
            timing_options: Timing configuration

        Returns:
            TurnOnFailedReason if failed, None if successful
        """
        try:
            _LOGGER.debug("Spawning '%s' process.", BLUETOOTHCTL_COMMAND)

            self._child = pexpect.spawn(
                BLUETOOTHCTL_COMMAND,
                encoding="utf-8",
                timeout=float(timing_options.spawn_timeout),
            )

            # Wait for the prompt
            self._child.expect(BLUETOOTHCTL_PROMPT)

            _LOGGER.info("bluetoothctl process started successfully.")
            return None

        except pexpect.exceptions.TIMEOUT as e:
            _LOGGER.warning(
                "Bluetooth spawn operation timed out after %s seconds. Error: %s",
                timing_options.spawn_timeout,
                e,
            )
            return TurnOnFailedReason.PROCESS_SPAWN_FAILED
        except Exception as e:
            _LOGGER.error(
                "Unexpected error during Bluetooth spawn: %s",
                e,
                exc_info=True,
            )
            return TurnOnFailedReason.PROCESS_SPAWN_FAILED

    def send_command(self, command: str) -> None:
        """
        Send a command to the bluetoothctl process.

        Args:
            command: Command to send
        """
        if self._child:
            self._child.sendline(command)

    def expect_response(self, pattern: str, timeout: float) -> bool:
        """
        Wait for a specific response pattern.

        Args:
            pattern: Pattern to expect
            timeout: Timeout in seconds

        Returns:
            True if pattern found, False if timeout
        """
        if not self._child:
            return False

        try:
            self._child.expect(pattern, timeout=timeout)
            return True
        except pexpect.exceptions.TIMEOUT:
            return False

    def get_pairing_state(self, mac_address: str, timeout: float) -> bool | None:
        """Read a fresh target-specific pairing state before sending pair.

        Unknown output fails closed: some bluetoothctl versions replace an
        existing bond when asked to pair again.
        """
        if not self._child or not self._child.isalive():
            return None
        if not re.fullmatch(r"(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}", mac_address):
            return None
        try:
            self._child.sendline(f"info {mac_address}")
            # Earlier scan commands may leave prompts in the input buffer. Wait
            # for this device's info header before consuming its final prompt.
            header = rf"(?i)Device {re.escape(mac_address)}(?: \([^\r\n]*\))?\r?\n"
            self._child.expect(header, timeout=timeout)
            self._child.expect(BLUETOOTHCTL_PROMPT, timeout=timeout)
            output = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", self._child.before)
            match = re.search(r"(?im)^\s*Paired:\s*(yes|no)\s*$", output)
            if match:
                return match.group(1).lower() == "yes"
        except (pexpect.exceptions.TIMEOUT, pexpect.exceptions.EOF):
            _LOGGER.warning("Could not read pairing state for %s", mac_address)
        return None

    def get_output(self) -> str:
        """
        Get the current output from the process.

        Returns:
            Current output buffer
        """
        if not self._child:
            return ""

        return self._child.before + self._child.buffer

    def cleanup(self) -> None:
        """Clean up the bluetoothctl process."""
        if self._child and self._child.isalive():
            _LOGGER.debug("Sending 'quit' command.")
            self._child.sendline("quit")
            self._child.close()

    @property
    def is_alive(self) -> bool:
        """Check if the process is still alive."""
        return self._child is not None and self._child.isalive()
