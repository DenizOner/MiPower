"""
Bluetooth scanner for MiPower integration.

This module handles Bluetooth device scanning operations,
following the Single Responsibility Principle.
"""

import logging
import time
from typing import Callable

from ...const import CMD_SCAN_OFF, CMD_SCAN_ON
from ...models import TimingOptions
from .exceptions import TurnOnFailedReason
from .process_manager import BluetoothProcessManager

_LOGGER = logging.getLogger(__name__)


class BluetoothScanner:
    """
    Handles Bluetooth device scanning operations.

    Responsible for discovering Bluetooth devices and finding target MAC addresses.
    """

    def __init__(self, process_manager: BluetoothProcessManager) -> None:
        """
        Initialize the scanner.

        Args:
            process_manager: Bluetooth process manager instance
        """
        self._process_manager = process_manager

    def scan_for_device(
        self,
        name: str,
        media_player_entity_id: str,
        mac_address: str,
        timing_options: TimingOptions,
        media_player_checker: Callable[[], bool],
    ) -> TurnOnFailedReason | None:
        """
        Scan for the target Bluetooth device.

        Args:
            name: Device name
            media_player_entity_id: Media player entity ID
            mac_address: Target MAC address
            timing_options: Timing configuration
            media_player_checker: Function to check if media player is on

        Returns:
            TurnOnFailedReason if failed, None if successful
        """
        try:
            _LOGGER.debug(
                "[%s (%s)] Sending '%s' command.",
                name,
                media_player_entity_id,
                CMD_SCAN_ON,
            )

            # Start scanning
            self._process_manager.send_command(CMD_SCAN_ON)

            # Calculate scan end time
            scan_end_time = time.monotonic() + timing_options.scan_duration
            mac_found_during_scan = False

            # Scan loop
            while time.monotonic() < scan_end_time:
                # Check if target MAC is found
                output = self._process_manager.get_output()
                if mac_address.upper() in output.upper():
                    _LOGGER.info(
                        "[%s (%s)] Target MAC address %s found during scan. "
                        "Stopping scan early.",
                        name,
                        media_player_entity_id,
                        mac_address,
                    )
                    mac_found_during_scan = True
                    break

                # Check if media player is already on (early exit)
                if media_player_checker():
                    _LOGGER.info(
                        "[%s (%s)] Media player turned on, stopping scan.",
                        name,
                        media_player_entity_id,
                    )
                    return None  # Success

                # Check for "Discovery started" message
                try:
                    if self._process_manager.expect_response(
                        "Discovery started", timeout=1
                    ):
                        _LOGGER.info(
                            "[%s (%s)] Bluetooth scan started. Scanning for %d "
                            "seconds.",
                            name,
                            media_player_entity_id,
                            timing_options.scan_duration,
                        )
                except Exception:
                    pass  # Continue scanning

            # Check scan result
            if not mac_found_during_scan:
                _LOGGER.warning(
                    "[%s (%s)] Bluetooth scan failed to find target MAC address %s "
                    "within %s seconds.",
                    name,
                    media_player_entity_id,
                    mac_address,
                    timing_options.scan_duration,
                )
                return TurnOnFailedReason.SCAN_FAILED

            return None  # Success

        except Exception as e:
            _LOGGER.error(
                "[%s (%s)] Unexpected error during Bluetooth scan: %s",
                name,
                media_player_entity_id,
                e,
                exc_info=True,
            )
            return TurnOnFailedReason.SCAN_FAILED

    def stop_scan(
        self,
        name: str,
        media_player_entity_id: str,
        timing_options: TimingOptions,
    ) -> TurnOnFailedReason | None:
        """
        Stop the Bluetooth scanning.

        Args:
            name: Device name
            media_player_entity_id: Media player entity ID
            timing_options: Timing configuration

        Returns:
            TurnOnFailedReason if failed, None if successful
        """
        try:
            _LOGGER.debug("[%s (%s)] Stopping scan.", name, media_player_entity_id)

            # Stop scanning
            self._process_manager.send_command(CMD_SCAN_OFF)

            # Wait for confirmation (non-critical)
            try:
                self._process_manager.expect_response(
                    "Discovery stopped", timeout=timing_options.scan_stop_timeout
                )
                _LOGGER.info(
                    "[%s (%s)] Bluetooth scan stopped.", name, media_player_entity_id
                )
            except Exception:
                _LOGGER.warning(
                    "[%s (%s)] No 'Discovery stopped' confirmation received "
                    "within %s seconds.",
                    name,
                    media_player_entity_id,
                    timing_options.scan_stop_timeout,
                )

            return None  # Success

        except Exception as e:
            _LOGGER.error(
                "[%s (%s)] Unexpected error during stopping Bluetooth scan: %s",
                name,
                media_player_entity_id,
                e,
                exc_info=True,
            )
            return TurnOnFailedReason.SCAN_FAILED
