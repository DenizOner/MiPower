"""
Binary Sensor Device Info Provider - Single Responsibility Principle

This module implements device information operations following SOLID principles,
providing device information for binary sensor entities.
"""

import logging
from typing import Any

from ...const import DOMAIN, MANUFACTURER
from .interface import BinarySensorDeviceInfoProviderInterface

_LOGGER = logging.getLogger(__name__)


class BinarySensorDeviceInfoProvider(BinarySensorDeviceInfoProviderInterface):
    """Provides device information for binary sensor entities with error handling and logging.

    This class is responsible for generating device information dictionaries
    for Home Assistant binary sensor entities. Follows Single Responsibility Principle
    by focusing only on device information provision.
    """

    def __init__(self):
        """Initialize the device info provider."""
        _LOGGER.debug("BinarySensorDeviceInfoProvider initialized")

    def get_device_info(self, binary_sensor) -> dict[str, Any]:
        """Get device information for the binary sensor entity.

        Args:
            binary_sensor: The Smartify binary sensor instance.

        Returns:
            Dictionary containing device identifiers, name, manufacturer, and model.
        """
        try:
            device_info = {
                "identifiers": {(DOMAIN, binary_sensor.unique_id)},
                "name": binary_sensor.name,
                "manufacturer": MANUFACTURER,
                "model": "Smart Binary Sensor",
            }

            _LOGGER.debug(
                "Generated device info for binary sensor '%s': %s",
                binary_sensor.name,
                device_info,
            )
            return device_info

        except Exception as e:
            _LOGGER.error(
                "Error getting device info for binary sensor %s: %s",
                getattr(binary_sensor, "name", "Unknown"),
                e,
                exc_info=True,
            )
            # Return basic device info on error
            return {
                "identifiers": {
                    (DOMAIN, getattr(binary_sensor, "unique_id", "unknown"))
                },
                "name": getattr(binary_sensor, "name", "Unknown Binary Sensor"),
                "manufacturer": MANUFACTURER,
                "model": "Smart Binary Sensor",
            }
