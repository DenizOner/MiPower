"""
Sensor State Provider - Single Responsibility Principle

This module implements sensor state operations following SOLID principles,
providing current state information for sensor entities.
"""

import logging
from typing import Any

from .properties_interfaces import SensorStateProviderInterface

_LOGGER = logging.getLogger(__name__)


class SensorStateProvider(SensorStateProviderInterface):
    """Provides current value information for sensor entities with error handling and logging.

    This class is responsible for retrieving the current value of sensor entities
    from coordinator data. Follows Single Responsibility Principle by focusing only
    on sensor state provision.
    """

    def __init__(self):
        """Initialize the sensor state provider."""
        _LOGGER.debug("SensorStateProvider initialized")

    def get_native_value(self, sensor) -> Any:
        """Get the current native value of the sensor.

        Args:
            sensor: The Smartify sensor instance.

        Returns:
            Native sensor value or None if no data.
        """
        try:
            if sensor.coordinator.data:
                # Sensor-specific value extraction
                sensor_type = getattr(sensor, "sensor_type", "unknown")
                value_key_map = {
                    "Last Power": "last_power",
                    "Last Command": "last_command",
                }

                value_key = value_key_map.get(
                    sensor_type, sensor_type.lower().replace(" ", "_")
                )
                value = sensor.coordinator.data.get(value_key)

                _LOGGER.debug(
                    "Sensor native value for '%s' (%s): %s",
                    getattr(sensor, "name", "Unknown"),
                    sensor_type,
                    value,
                )
                return value

            _LOGGER.debug(
                "No coordinator data available for '%s'",
                getattr(sensor, "name", "Unknown"),
            )
            return None

        except Exception as e:
            _LOGGER.error(
                "Error getting native value for %s: %s",
                getattr(sensor, "name", "Unknown"),
                e,
                exc_info=True,
            )
            return None
