"""
Bluetooth-specific interfaces for MiPower integration.

This module defines interfaces specific to Bluetooth operations,
following the Interface Segregation Principle.
"""

from abc import ABC, abstractmethod
from typing import Union

from homeassistant.core import HomeAssistant

from ...models import TimingOptions
from .exceptions import TurnOnFailedReason


class IBluetoothService(ABC):
    """
    Interface for Bluetooth service operations.

    Defines the contract for Bluetooth wake-up operations.
    """

    @abstractmethod
    async def wake_up(
        self,
        hass: HomeAssistant,
        name: str,
        mac_address: str,
        media_player_entity_id: str,
        timing_options: TimingOptions,
    ) -> Union[bool, "TurnOnFailedReason"]:
        """
        Perform Bluetooth wake-up operation.

        Args:
            hass: Home Assistant instance
            name: Device name
            mac_address: Target MAC address
            media_player_entity_id: Media player entity ID
            timing_options: Timing configuration

        Returns:
            True if successful, TurnOnFailedReason if failed
        """
        pass
