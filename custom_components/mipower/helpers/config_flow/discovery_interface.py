"""Device discovery interface for Smartify config flow."""

from abc import ABC, abstractmethod
from typing import List


class DiscoveryInterface(ABC):
    """Interface for device discovery services."""

    @abstractmethod
    async def discover_power_devices(self) -> List[dict]:
        """Discover available power sensor devices.

        Returns:
            List[dict]: List of available power devices with id and name.
        """
        pass

    @abstractmethod
    async def discover_remote_devices(self) -> List[dict]:
        """Discover available remote devices.

        Returns:
            List[dict]: List of available remote devices with id and name.
        """
        pass

    @abstractmethod
    async def discover_scripts_for_device(self, device_id: str) -> List[dict]:
        """Discover scripts available for a specific device.

        Args:
            device_id: The device ID to find scripts for.

        Returns:
            List[dict]: List of available scripts for the device.
        """
        pass
