"""Device Registry Interface - Dependency Inversion for Device Management

This module defines the abstraction layer for device registry operations,
allowing DIP by decoupling device registry logic from the coordinator.
It provides a standardized interface for device lookup and registry access
with error handling and logging capabilities.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional

from homeassistant.core import HomeAssistant  # type: ignore[import]


class DeviceRegistryInterface(ABC):
    """Interface for device registry operations.

    This abstract base class defines the contract for device registry components
    in Smartify, providing a consistent API for device registry access and
    device lookup with error handling.
    """

    @abstractmethod
    def get_device_registry(self, hass: HomeAssistant) -> Any:
        """Get the Home Assistant device registry.

        Args:
            hass: Home Assistant instance.

        Returns:
            Device registry instance.

        Raises:
            RuntimeError: If accessing the registry fails.
        """

    @abstractmethod
    def get_device_by_id(self, hass: HomeAssistant, device_id: str) -> Optional[Any]:
        """Retrieve a device from the registry by its ID.

        Args:
            hass: Home Assistant instance.
            device_id: The device ID to look up.

        Returns:
            Device entry if found, None otherwise.
        """
