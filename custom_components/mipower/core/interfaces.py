"""Interfaces for SOLID principles in MiPower integration."""

from abc import ABC, abstractmethod
from typing import Any, Dict

from homeassistant.core import HomeAssistant

from ..models import TimingOptions
from ..services.bluetooth import TurnOnFailedReason


class ICoordinator(ABC):
    """Interface for data coordinators."""

    @abstractmethod
    async def async_setup(self) -> None:
        """Set up the coordinator."""
        pass

    @abstractmethod
    async def async_unload(self) -> None:
        """Unload the coordinator."""
        pass

    @property
    @abstractmethod
    def coordinator_data(self) -> Any:
        """Get current coordinator data."""
        pass


class ITurnOnHandler(ABC):
    """Interface for turn-on operations."""

    @abstractmethod
    async def turn_on(
        self, name: str, mac_address: str, timing_options: TimingOptions
    ) -> bool | TurnOnFailedReason:
        """Turn on the device."""
        pass


class ITurnOffHandler(ABC):
    """Interface for turn-off operations."""

    @abstractmethod
    async def turn_off(
        self,
        hass: HomeAssistant,
        media_player_entity_id: str,
        timing_options: TimingOptions,
    ) -> None:
        """Turn off the device."""
        pass


class IDeviceDiscovery(ABC):
    """Interface for device discovery."""

    @abstractmethod
    async def discover_devices(self, hass: HomeAssistant) -> Dict[str, Any]:
        """Discover available devices."""
        pass


class IConfigFlowStep(ABC):
    """Interface for config flow steps."""

    @abstractmethod
    async def async_step(self, user_input: Dict[str, Any] | None = None) -> Any:
        """Execute the step."""
        pass


class IBluetoothService(ABC):
    """Interface for Bluetooth operations."""

    @abstractmethod
    async def wake_up(
        self,
        hass: HomeAssistant,
        name: str,
        mac_address: str,
        media_player_entity_id: str,
        timing_options: TimingOptions,
    ) -> bool | TurnOnFailedReason:
        """Wake up a device using Bluetooth."""
        pass
