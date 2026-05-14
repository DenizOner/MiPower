"""Remote device management interface for Smartify integration.

This module defines the interfaces for remote device validation and discovery,
following SOLID principles and dependency inversion.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from homeassistant.helpers import device_registry as dr  # type: ignore[import]
from homeassistant.helpers import entity_registry as er  # type: ignore[import]


class RemoteDeviceValidatorInterface(ABC):
    """Interface for remote device validation."""

    @abstractmethod
    async def is_valid_remote_device(
        self,
        device_entry: dr.DeviceEntry,
        entity_registry: er.EntityRegistry,
    ) -> bool:
        """Validate if a device is a valid remote control device.

        Args:
            device_entry: The device entry to validate.
            entity_registry: The entity registry for entity lookup.

        Returns:
            bool: True if the device is a valid remote control device.
        """
        pass


class RemoteDeviceFinderInterface(ABC):
    """Interface for remote device discovery."""

    @abstractmethod
    async def find_remote_devices(self) -> List[Dict[str, Any]]:
        """Discover all valid remote control devices.

        Returns:
            List[Dict[str, Any]]: List of remote device information.
        """
        pass
