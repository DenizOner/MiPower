"""
Binary Sensor Properties Manager - Composition Pattern

This module implements the binary sensor properties manager following SOLID principles,
coordinating all binary sensor properties operations using composition pattern.
"""

import logging
from typing import Any

from .binary_sensor_device_info_provider import BinarySensorDeviceInfoProvider
from .binary_sensor_state_provider import BinarySensorStateProvider
from .interface import BinarySensorPropertiesManagerInterface

_LOGGER = logging.getLogger(__name__)


class BinarySensorPropertiesManager(BinarySensorPropertiesManagerInterface):
    """Manages all binary sensor properties operations using composition pattern.

    This class coordinates all binary sensor properties by composing specialized providers
    for device information, state retrieval. Implements the Facade pattern to
    provide a unified interface for binary sensor properties.
    """

    def __init__(self):
        """Initialize the binary sensor properties manager with all providers."""
        _LOGGER.debug("BinarySensorPropertiesManager initialized with SOLID providers")

        # Composition: Initialize all specialized providers
        self._device_info_provider = BinarySensorDeviceInfoProvider()
        self._state_provider = BinarySensorStateProvider()

    def get_device_info(self, entity) -> dict[str, Any]:
        """Get device information for the binary sensor entity.

        Args:
            entity: The SmartifyBinarySensor instance.

        Returns:
            Dictionary containing device information.
        """
        return self._device_info_provider.get_device_info(entity)

    def get_available(self, entity) -> bool:
        """Get the availability status of the binary sensor.

        Args:
            entity: The SmartifyBinarySensor instance.

        Returns:
            True if the binary sensor is available, False otherwise.
        """
        # For binary sensors, always return True as they don't have complex availability logic
        # This could be extended with more sophisticated availability checking if needed
        return True

    def get_is_on(self, entity) -> bool:
        """Get the current on/off state of the binary sensor.

        Args:
            entity: The SmartifyBinarySensor instance.

        Returns:
            Native binary sensor state (on/off).
        """
        return self._state_provider.get_is_on(entity)
