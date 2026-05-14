"""
Sensor Device Info Provider - Single Responsibility Principle

This module implements device information operations following SOLID principles,
providing device information for sensor entities.
"""

import logging
from typing import Any

from ...const import DOMAIN, MANUFACTURER
from .properties_interfaces import SensorDeviceInfoProviderInterface

_LOGGER = logging.getLogger(__name__)


class SensorDeviceInfoProvider(SensorDeviceInfoProviderInterface):
    """Provides device information for sensor entities with error handling and logging.

    This class is responsible for generating device information dictionaries
    for Home Assistant sensor entities. Follows Single Responsibility Principle
    by focusing only on device information provision.
    """

    def __init__(self):
        """Initialize the device info provider."""
        _LOGGER.debug("SensorDeviceInfoProvider initialized")

    def get_device_info(self, sensor) -> dict[str, Any]:
        """Get device information for the sensor entity.

        Args:
            sensor: The Smartify sensor instance.

        Returns:
            Dictionary containing device identifiers, name, manufacturer, and model.
        """
        try:
            device_info = {
                "identifiers": {(DOMAIN, sensor.unique_id)},
                "name": sensor.name,
                "manufacturer": MANUFACTURER,
                "model": "Smart Sensor",
            }

            _LOGGER.debug(
                "Generated device info for sensor '%s': %s",
                sensor.name,
                device_info,
            )
            return device_info

        except Exception as e:
            _LOGGER.error(
                "Error getting device info for sensor %s: %s",
                getattr(sensor, "name", "Unknown"),
                e,
                exc_info=True,
            )
            # Return basic device info on error
            return {
                "identifiers": {(DOMAIN, getattr(sensor, "unique_id", "unknown"))},
                "name": getattr(sensor, "name", "Unknown Sensor"),
                "manufacturer": MANUFACTURER,
                "model": "Smart Sensor",
            }
