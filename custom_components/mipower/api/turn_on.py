"""
Turn-on logic for the MiPower integration.

This file contains the core logic for turning on the target device. It uses the
`bluetoothctl` command-line utility, which is a standard tool on many Linux systems
for managing Bluetooth devices. The process involves spawning `bluetoothctl`,
scanning for the device, and then sending a `pair` command. The `pair` command
often serves as a "wake-up" signal for sleeping devices.

This entire process is synchronous and involves waiting for subprocess I/O, so it
MUST be run in an executor thread to avoid blocking the main Home Assistant event loop.
"""

import logging
import time
from typing import Any

import pexpect

# Import constants from the main const.py file.
from ..const import (
    BLUETOOTHCTL_COMMAND,
    BLUETOOTHCTL_PROMPT,
    CMD_PAIR,
    CMD_QUIT,
    CMD_TRUST,
    PEXPECT_PAIR_RESPONSES,
    PEXPECT_TRUST_SUCCESS,
)

# Set up a specific logger for this file.
_LOGGER = logging.getLogger(__name__)

# A global variable to store the timestamp of the last successful 'turn_on' call.
# This is used to implement a simple debouncing mechanism.
_last_call_time = 0


def perform_turn_on_sync(
    mac_address: str,
    debounce_seconds: int,
    spawn_timeout: int,
    pair_timeout: int,
    trust_timeout: int,
    inter_step_delay: float,
    scan_duration: int,
) -> bool:
    """
    Wake up the device via `bluetoothctl pair` command using a simple, robust method.
    This function is synchronous and should be run in a thread.
    """
    global _last_call_time
    now = time.time()

    if now - _last_call_time < debounce_seconds:
        _LOGGER.warning(
            "Turn on called too frequently for %s. Debounced for %s seconds. Ignoring.",
            mac_address,
            debounce_seconds,
        )
        return False

    _LOGGER.info("Attempting to send wake-up signal to %s using simplified prototype logic.", mac_address)
    child: pexpect.spawn | None = None
    try:
        _LOGGER.debug("Spawning '%s' process.", BLUETOOTHCTL_COMMAND)
        child = pexpect.spawn(
            BLUETOOTHCTL_COMMAND, encoding="utf-8", timeout=spawn_timeout
        )
        # Wait for a generic prompt (either '>' or '#') to ensure the tool is ready.
        # This is more robust against changes in bluetoothctl versions.
        child.expect(r"[>#] ")
        _LOGGER.info("bluetoothctl process started successfully.")

        _LOGGER.debug("Sending 'scan on' command.")
        child.sendline("scan on")
        child.expect("Discovery started", timeout=10)
        _LOGGER.info("Bluetooth discovery started. Scanning for %d seconds.", scan_duration)

        # Simply wait for the scan duration. Trying to catch the device in the output
        # is less reliable than just giving it enough time to be found.
        time.sleep(scan_duration)

        _LOGGER.debug("Scan duration finished. Stopping scan.")
        child.sendline("scan off")
        try:
            child.expect("Discovery stopped", timeout=5)
            _LOGGER.info("Bluetooth discovery stopped.")
        except pexpect.exceptions.TIMEOUT:
            _LOGGER.warning("Did not receive 'Discovery stopped' confirmation. Proceeding anyway.")

        time.sleep(inter_step_delay)

        _LOGGER.info("Attempting to pair with %s to wake it up.", mac_address)
        child.sendline(f"pair {mac_address}")

        # We don't need to wait for a specific response. Sending the pair command
        # is usually enough to wake the device. We'll wait briefly to allow the command
        # to be processed and then assume success.
        time.sleep(pair_timeout)
        _LOGGER.info("Pair command sent to %s. Assuming wake-up was successful.", mac_address)
        
        _last_call_time = now
        return True

    except pexpect.exceptions.TIMEOUT as e:
        _LOGGER.error(
            "A timeout occurred during bluetoothctl operation for %s. This can happen if the device is unresponsive or the prompt has changed. Error: %s",
            mac_address,
            e,
        )
    except pexpect.exceptions.EOF as e:
        _LOGGER.critical(
            "bluetoothctl process ended unexpectedly (EOF). Is '%s' installed, and does Home Assistant have the necessary permissions (e.g., bluetooth group, D-Bus access)? Error: %s",
            BLUETOOTHCTL_COMMAND,
            e,
        )
    except Exception as e:
        _LOGGER.error("An unexpected error occurred: %s", e, exc_info=True)
    finally:
        if child and child.isalive():
            _LOGGER.debug("Sending 'quit' command to bluetoothctl.")
            child.sendline(CMD_QUIT)
            child.close()
            _LOGGER.debug("bluetoothctl process closed.")
    
    return False
