"""
Sensor Properties Manager - Composition Pattern

This module implements the sensor properties manager following SOLID principles,
coordinating all sensor properties operations using composition pattern.
"""

import logging
from typing import Any

from .properties_interfaces import SensorPropertiesManagerInterface
from .sensor_device_info_provider import SensorDeviceInfoProvider
from .sensor_state_provider import SensorStateProvider

_LOGGER = logging.getLogger(__name__)


class SensorPropertiesManager(SensorPropertiesManagerInterface):
    """Manages all sensor properties operations using composition pattern.

    This class coordinates all sensor properties by composing specialized providers
    for device information, value retrieval. Implements the Facade pattern to
    provide a unified interface for sensor properties.
    """

    def __init__(self):
        """Initialize the sensor properties manager with all providers."""
        _LOGGER.debug("SensorPropertiesManager initialized with SOLID providers")

        # Composition: Initialize all specialized providers
        self._device_info_provider = SensorDeviceInfoProvider()
        self._state_provider = SensorStateProvider()

    def get_device_info(self, entity) -> dict[str, Any]:
        """Get device information for the sensor entity.

        Args:
            entity: The SmartifySensor instance.

        Returns:
            Dictionary containing device information.
        """
        return self._device_info_provider.get_device_info(entity)

    def get_available(self, entity) -> bool:
        """Get the availability status of the sensor.

        Args:
            entity: The SmartifySensor instance.

        Returns:
            True if the sensor is available, False otherwise.
        """
        # For sensors, always return True as they don't have complex availability logic
        # This could be extended with more sophisticated availability checking if needed
        return True

    def get_native_value(self, entity) -> Any:
        """Get the native value of the sensor.

        Args:
            entity: The SmartifySensor instance.

        Returns:
            Native sensor value or None.
        """
        return self._state_provider.get_native_value(entity)
