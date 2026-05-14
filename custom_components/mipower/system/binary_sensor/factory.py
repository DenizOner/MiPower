"""
Binary Sensor Factory - Factory Pattern Implementation

This module implements binary sensor factory functionality following SOLID principles,
providing centralized binary sensor creation and management.
"""

import logging
from typing import Any, List

from homeassistant.components.binary_sensor import (  # type: ignore[import]
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry  # type: ignore[import]
from homeassistant.helpers.update_coordinator import CoordinatorEntity  # type: ignore[import]

from ...const import (
    CONF_NAME,
    ENTITY_NAME_POSTFIX,
)
from .interface import (
    BinarySensorFactoryInterface,
    BinarySensorPropertiesManagerInterface,
)

_LOGGER = logging.getLogger(__name__)


class BinarySensorFactory(BinarySensorFactoryInterface):
    """Factory for creating Smartify binary sensor instances.

    This class implements the Factory pattern to create binary sensor instances,
    following Single Responsibility Principle by focusing only on binary sensor creation.
    """

    def __init__(self, hass: Any):
        """Initialize the binary sensor factory.

        Args:
            hass: Home Assistant instance for dependency injection
        """
        self.hass = hass
        _LOGGER.debug("BinarySensorFactory initialized")

    def create_connectivity_sensor(self, entry: ConfigEntry, coordinator) -> Any:
        """Create a connectivity sensor instance.

        Args:
            entry: Configuration entry.
            coordinator: Data coordinator.

        Returns:
            Connectivity sensor instance.
        """
        from .binary_sensor_properties_manager import (
            BinarySensorPropertiesManager,
        )

        properties_manager = BinarySensorPropertiesManager()
        return SmartifyVerifiedSensor(
            entry, coordinator, "Verification", properties_manager
        )

    def create_all_binary_sensors(self, entry: ConfigEntry, coordinator) -> List[Any]:
        """Create all binary sensors for the integration.

        Args:
            entry: Configuration entry.
            coordinator: Data coordinator.

        Returns:
            List of all binary sensor instances.
        """
        sensors = [
            self.create_connectivity_sensor(entry, coordinator),
        ]
        _LOGGER.debug(
            f"Created {len(sensors)} binary sensors for entry {entry.entry_id}"
        )
        return sensors


class SmartifyVerifiedSensor(CoordinatorEntity, BinarySensorEntity):
    """Binary sensor for Smartify connectivity/verification status.

    This sensor indicates whether the coordinator's last update was successful,
    serving as a connectivity indicator for the Smartify integration.
    """

    _attr_should_poll = False
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY

    def __init__(
        self,
        entry: ConfigEntry,
        coordinator,
        sensor_type: str,
        properties_manager: BinarySensorPropertiesManagerInterface,
    ):
        """Initialize the connectivity sensor.

        Args:
            entry: Configuration entry.
            coordinator: Data coordinator.
            sensor_type: Type of the binary sensor.
            properties_manager: Properties manager instance for SOLID architecture.
        """
        super().__init__(coordinator)
        self._entry = entry
        self.sensor_type = sensor_type
        self._properties_manager = properties_manager
        self._attr_name = f"{entry.data[CONF_NAME]} {sensor_type}{ENTITY_NAME_POSTFIX}"
        self._attr_friendly_name = (
            f"{entry.data[CONF_NAME]} {sensor_type}{ENTITY_NAME_POSTFIX}"
        )
        self._attr_unique_id = (
            f"{entry.entry_id}_{sensor_type.replace(' ', '_').lower()}"
        )

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information for Home Assistant."""
        return self._properties_manager.get_device_info(self)

    @property
    def is_on(self) -> bool:
        """Return the state of the binary sensor.

        The sensor is on when the coordinator's last update was successful.

        Returns:
            True if the sensor is on (verified), False otherwise.
        """
        try:
            is_verified = self.coordinator.last_update_success
            _LOGGER.debug(
                "Connectivity sensor state for '%s': %s",
                self.name,
                "ON" if is_verified else "OFF",
            )
            return is_verified
        except Exception as e:
            _LOGGER.error(
                "Error getting connectivity sensor state for %s: %s",
                self.name,
                e,
                exc_info=True,
            )
            return False

    @property
    def available(self) -> bool:
        """Return the availability of the binary sensor.

        Returns:
            True as this sensor is always available.
        """
        return True
