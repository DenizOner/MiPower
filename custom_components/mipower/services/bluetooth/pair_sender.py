"""
Bluetooth pair sender for MiPower integration.

This module handles sending Bluetooth pair commands,
following the Single Responsibility Principle.
"""

import logging

from ...const import CMD_PAIR
from ...models import TimingOptions
from .exceptions import TurnOnFailedReason
from .process_manager import BluetoothProcessManager

_LOGGER = logging.getLogger(__name__)


class BluetoothPairSender:
    """
    Handles sending Bluetooth pair commands.

    Responsible for sending wake-up signals to target devices.
    """

    def __init__(self, process_manager: BluetoothProcessManager) -> None:
        """
        Initialize the pair sender.

        Args:
            process_manager: Bluetooth process manager instance
        """
        self._process_manager = process_manager

    def send_pair_command(
        self,
        name: str,
        media_player_entity_id: str,
        mac_address: str,
        timing_options: TimingOptions,
    ) -> TurnOnFailedReason | None:
        """
        Send the Bluetooth pair command to wake up the device.

        Args:
            name: Device name
            media_player_entity_id: Media player entity ID
            mac_address: Target MAC address
            timing_options: Timing configuration

        Returns:
            TurnOnFailedReason if failed, None if successful
        """
        try:
            paired = self._process_manager.get_pairing_state(
                mac_address, timeout=timing_options.spawn_timeout
            )
            if paired is True:
                _LOGGER.warning(
                    "[%s (%s)] Preserving existing Bluetooth pairing with %s; "
                    "a pairing wake request cannot be sent safely.",
                    name, media_player_entity_id, mac_address,
                )
                return TurnOnFailedReason.ALREADY_PAIRED
            if paired is None:
                _LOGGER.warning(
                    "[%s (%s)] Pairing state of %s is unknown; wake request skipped.",
                    name, media_player_entity_id, mac_address,
                )
                return TurnOnFailedReason.SIGNAL_FAILED
            _LOGGER.info(
                "[%s (%s)] Sending Bluetooth pair command to %s.",
                name,
                media_player_entity_id,
                mac_address,
            )

            # Send pair command
            self._process_manager.send_command(f"{CMD_PAIR} {mac_address}")

            _LOGGER.debug(
                "[%s (%s)] Bluetooth pair command sent.",
                name,
                media_player_entity_id,
            )

            return None  # Success

        except Exception as e:
            _LOGGER.error(
                "[%s (%s)] Unexpected error during Bluetooth pair command: %s",
                name,
                media_player_entity_id,
                e,
                exc_info=True,
            )
            return TurnOnFailedReason.SIGNAL_FAILED
