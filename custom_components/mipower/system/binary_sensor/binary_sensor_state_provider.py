"""
Binary Sensor State Provider - Single Responsibility Principle

This module implements binary sensor state operations following SOLID principles,
providing current state information for binary sensor entities.
"""

import logging

from .interface import BinarySensorStateProviderInterface

_LOGGER = logging.getLogger(__name__)


class BinarySensorStateProvider(BinarySensorStateProviderInterface):
    """Provides current state information for binary sensor entities with error handling and logging.

    This class is responsible for retrieving the current on/off state of binary sensor entities
    from coordinator data. Follows Single Responsibility Principle by focusing only
    on binary sensor state provision.
    """

    def __init__(self):
        """Initialize the binary sensor state provider."""
        _LOGGER.debug("BinarySensorStateProvider initialized")

    def get_is_on(self, binary_sensor) -> bool:
        """Get the current on/off state of the binary sensor.

        Args:
            binary_sensor: The Smartify binary sensor instance.

        Returns:
            True if the binary sensor is on, False otherwise.
        """
        try:
            # For connectivity sensor, check coordinator last update success
            if hasattr(binary_sensor, "coordinator") and binary_sensor.coordinator:
                is_on = binary_sensor.coordinator.last_update_success
                _LOGGER.debug(
                    "Binary sensor state for '%s': %s",
                    getattr(binary_sensor, "name", "Unknown"),
                    is_on,
                )
                return is_on
            else:
                _LOGGER.debug(
                    "No coordinator available for binary sensor '%s'",
                    getattr(binary_sensor, "name", "Unknown"),
                )
                return False

        except Exception as e:
            _LOGGER.error(
                "Error getting is_on state for %s: %s",
                getattr(binary_sensor, "name", "Unknown"),
                e,
                exc_info=True,
            )
            return False
