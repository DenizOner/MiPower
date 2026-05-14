"""
Sensor Factory - Factory Pattern Implementation

This module implements sensor factory functionality following SOLID principles,
providing centralized sensor creation and management.
"""

import logging
from typing import Any, List

from homeassistant.components.sensor import (  # type: ignore[import]
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry  # type: ignore[import]
from homeassistant.const import UnitOfPower  # type: ignore[import]
from homeassistant.helpers.update_coordinator import CoordinatorEntity  # type: ignore[import]

from ...const import CONF_NAME, CONF_POWER_ENTITY, ENTITY_NAME_POSTFIX
from .interface import SensorFactoryInterface
from .properties_interfaces import SensorPropertiesManagerInterface

_LOGGER = logging.getLogger(__name__)


class SensorFactory(SensorFactoryInterface):
    """Factory for creating Smartify sensor instances.

    This class implements the Factory pattern to create sensor instances,
    following Single Responsibility Principle by focusing only on sensor creation.
    """

    def __init__(self):
        """Initialize the sensor factory."""
        _LOGGER.debug("SensorFactory initialized")

    def create_power_sensor(self, entry: ConfigEntry, hass) -> Any:
        """Create a power sensor instance with real-time tracking.

        Args:
            entry: Configuration entry.
            hass: Home Assistant instance.

        Returns:
            Power sensor instance.
        """
        from .sensor_properties_manager import SensorPropertiesManager

        properties_manager = SensorPropertiesManager()
        return SmartifyLastPowerSensor(entry, hass, properties_manager)

    def create_command_sensor(self, entry: ConfigEntry, coordinator) -> Any:
        """Create a command sensor instance.

        Args:
            entry: Configuration entry.
            coordinator: Data coordinator.

        Returns:
            Command sensor instance.
        """
        from .sensor_properties_manager import SensorPropertiesManager

        properties_manager = SensorPropertiesManager()
        return SmartifyLastCommandSensor(entry, coordinator, properties_manager)

    def create_all_sensors(self, entry: ConfigEntry, coordinator, hass) -> List[Any]:
        """Create all sensors for the integration.

        Args:
            entry: Configuration entry.
            coordinator: Data coordinator.
            hass: Home Assistant instance.

        Returns:
            List of all sensor instances.
        """
        sensors = [
            self.create_power_sensor(entry, hass),
            self.create_command_sensor(entry, coordinator),
        ]
        _LOGGER.debug(f"Created {len(sensors)} sensors for entry {entry.entry_id}")
        return sensors


class SmartifySensor(SensorEntity):
    """Base class for Smartify sensors.

    This class provides a common base for all Smartify sensor entities,
    handling entity initialization and device info.
    """

    _attr_should_poll = False

    def __init__(
        self,
        entry: ConfigEntry,
        sensor_type: str,
        properties_manager: SensorPropertiesManagerInterface,
    ):
        """Initialize the sensor base class.

        Args:
            entry: The config entry for this integration.
            sensor_type: The type of sensor (e.g., "Last Power").
            properties_manager: Properties manager instance for SOLID architecture.
        """
        super().__init__()
        self._entry = entry
        self.sensor_type = sensor_type  # Set as attribute for provider access
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
        """Return device information."""
        return self._properties_manager.get_device_info(self)


class SmartifyCoordinatorSensor(CoordinatorEntity, SmartifySensor):
    """Base class for coordinator-based Smartify sensors.

    This class extends both CoordinatorEntity and SmartifySensor for sensors
    that need coordinator functionality.
    """

    def __init__(
        self,
        entry: ConfigEntry,
        coordinator,
        sensor_type: str,
        properties_manager: SensorPropertiesManagerInterface,
    ):
        """Initialize the coordinator sensor base class.

        Args:
            entry: The config entry for this integration.
            coordinator: The data coordinator.
            sensor_type: The type of sensor (e.g., "Last Command").
            properties_manager: Properties manager instance for SOLID architecture.
        """
        CoordinatorEntity.__init__(self, coordinator)
        SmartifySensor.__init__(self, entry, sensor_type, properties_manager)


class SmartifyLastPowerSensor(SmartifySensor):
    """Sensor for real-time power tracking.

    This sensor provides real-time power consumption value directly from the
    configured power entity, without coordinator dependency.
    """

    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_should_poll = False

    def __init__(
        self,
        entry: ConfigEntry,
        hass,
        properties_manager: SensorPropertiesManagerInterface,
    ):
        """Initialize the real-time power sensor.

        Args:
            entry: The config entry for this integration.
            hass: Home Assistant instance.
            properties_manager: Properties manager instance for SOLID architecture.
        """
        super().__init__(entry, "Last Power", properties_manager)
        self.hass = hass
        self._power_entity_id = entry.data[CONF_POWER_ENTITY]
        self._current_power = None
        self._listener = None

    async def async_added_to_hass(self) -> None:
        """Set up event listener when entity is added to Home Assistant."""
        from homeassistant.helpers.event import async_track_state_change_event  # type: ignore[import]

        self._listener = async_track_state_change_event(
            hass=self.hass,
            entity_ids=[self._power_entity_id],
            action=self._handle_power_state_change,
        )

        # Get initial state
        if state := self.hass.states.get(self._power_entity_id):
            self._update_power_value(state)

    async def async_will_remove_from_hass(self) -> None:
        """Clean up event listener when entity is removed."""
        if self._listener:
            self._listener()
            self._listener = None

    async def _handle_power_state_change(self, event):
        """Handle power entity state changes."""
        new_state = event.data.get("new_state")
        if new_state:
            self._update_power_value(new_state)
            self.async_write_ha_state()

    def _update_power_value(self, state):
        """Update the internal power value from state."""
        try:
            if state.state in ("unknown", "unavailable"):
                self._current_power = None
            else:
                self._current_power = float(state.state)
        except (ValueError, TypeError):
            self._current_power = None

    @property
    def native_value(self) -> float | None:
        """Return the native value of the sensor.

        Returns:
            The current power value in watts, or None if no data.
        """
        return self._current_power


class SmartifyLastCommandSensor(SmartifyCoordinatorSensor):
    """Sensor for last executed command.

    This sensor provides the last executed command from the Smartify device.
    """

    _attr_icon = "mdi:history"

    def __init__(
        self,
        entry: ConfigEntry,
        coordinator,
        properties_manager: SensorPropertiesManagerInterface,
    ):
        """Initialize the last command sensor.

        Args:
            entry: The config entry for this integration.
            coordinator: The data coordinator.
            properties_manager: Properties manager instance for SOLID architecture.
        """
        super().__init__(entry, coordinator, "Last Command", properties_manager)

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor.

        Returns:
            The last executed command as a string, or None if no data.
        """
        if self.coordinator.data:
            return self.coordinator.data.get("last_command")
        return None
