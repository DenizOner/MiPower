"""
Device Registry Service - Single Responsibility Principle

This module implements device registry operations following SOLID principles,
handling device registry access and device lookup functionality.
"""

import logging
from typing import Any, Optional

from homeassistant.core import HomeAssistant  # type: ignore[import]
from homeassistant.helpers import device_registry as dr  # type: ignore[import]

from .registry_interface import DeviceRegistryInterface

_LOGGER = logging.getLogger(__name__)


class DeviceRegistryService(DeviceRegistryInterface):
    """Handles device registry operations with error handling and logging.

    This class is responsible for accessing the Home Assistant device registry
    and performing device-related operations. Follows Single Responsibility
    Principle by focusing only on device registry operations.
    """

    def __init__(self):
        """Initialize the device registry service."""
        _LOGGER.debug("DeviceRegistryService initialized")

    def get_device_registry(self, hass: HomeAssistant) -> Any:
        """Get the Home Assistant device registry.

        Args:
            hass: Home Assistant instance.

        Returns:
            Device registry instance.

        Raises:
            RuntimeError: If accessing the registry fails.
        """
        if hass is None:
            _LOGGER.error("Home Assistant instance is None")
            raise RuntimeError("Home Assistant instance is None")

        try:
            registry = dr.async_get(hass)
            _LOGGER.debug("Device registry accessed successfully")
            return registry
        except Exception as e:
            _LOGGER.error(
                "Failed to access device registry: %s",
                e,
                exc_info=True,
            )
            raise RuntimeError(f"Failed to access device registry: {e}")

    def get_device_by_id(self, hass: HomeAssistant, device_id: str) -> Optional[Any]:
        """Retrieve a device from the registry by its ID.

        Args:
            hass: Home Assistant instance.
            device_id: The device ID to look up.

        Returns:
            Device entry if found, None otherwise.
        """
        try:
            registry = self.get_device_registry(hass)
            device = registry.async_get(device_id)

            if device:
                _LOGGER.debug("Device found: %s", device_id)
            else:
                _LOGGER.debug("Device not found: %s", device_id)

            return device

        except Exception as e:
            _LOGGER.error(
                "Error retrieving device %s: %s",
                device_id,
                e,
                exc_info=True,
            )
            return None
