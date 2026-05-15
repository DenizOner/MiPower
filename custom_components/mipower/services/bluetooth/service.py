"""
Bluetooth service implementation for MiPower integration.

This module provides the main Bluetooth service interface,
now using a modular architecture with separate components.
"""

from typing import Union

from homeassistant.core import HomeAssistant  # type: ignore[import]

from ...models import TimingOptions
from .exceptions import TurnOnFailedReason
from .interfaces import IBluetoothService
from .wake_coordinator import BluetoothWakeCoordinator


class BluetoothService(IBluetoothService):
    """
    Main Bluetooth service for MiPower integration.

    This service coordinates all Bluetooth wake-up operations using
    a modular architecture with separate, focused components.
    """

    def __init__(self) -> None:
        """Initialize the Bluetooth service."""
        self._coordinator = BluetoothWakeCoordinator()

    async def wake_up(
        self,
        hass: HomeAssistant,
        name: str,
        mac_address: str,
        media_player_entity_id: str,
        timing_options: TimingOptions,
    ) -> Union[bool, TurnOnFailedReason]:
        """
        Perform Bluetooth wake-up operation for a device.

        Args:
            hass: Home Assistant instance
            name: Device name
            mac_address: Target MAC address
            media_player_entity_id: Media player entity ID
            timing_options: Timing configuration

        Returns:
            True if successful, TurnOnFailedReason if failed
        """
        return await self._coordinator.wake_up(
            hass, name, mac_address, media_player_entity_id, timing_options
        )
