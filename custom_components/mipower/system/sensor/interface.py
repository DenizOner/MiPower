"""
Sensor Interface - Dependency Inversion for Sensor Management

This module defines the abstraction layer for sensor functionality in Smartify,
implementing Dependency Inversion Principle (DIP) by decoupling sensor operations
from the core components.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from homeassistant.config_entries import ConfigEntry  # type: ignore[import]
from homeassistant.core import HomeAssistant  # type: ignore[import]
from homeassistant.helpers.entity_platform import AddEntitiesCallback  # type: ignore[import]


class SensorFactoryInterface(ABC):
    """Abstract interface for sensor factory functionality."""

    @abstractmethod
    def create_power_sensor(self, entry: ConfigEntry, hass: HomeAssistant) -> Any:
        """Create a power sensor instance with real-time tracking.

        Args:
            entry: Configuration entry.
            hass: Home Assistant instance for real-time state access.

        Returns:
            Power sensor instance.
        """

    @abstractmethod
    def create_command_sensor(self, entry: ConfigEntry, coordinator) -> Any:
        """Create a command sensor instance.

        Args:
            entry: Configuration entry.
            coordinator: Data coordinator.

        Returns:
            Command sensor instance.
        """

    @abstractmethod
    def create_all_sensors(
        self, entry: ConfigEntry, coordinator, hass: HomeAssistant
    ) -> List[Any]:
        """Create all sensors for the integration.

        Args:
            entry: Configuration entry.
            coordinator: Data coordinator.
            hass: Home Assistant instance.

        Returns:
            List of all sensor instances.
        """


class SensorSetupInterface(ABC):
    """Abstract interface for sensor setup functionality."""

    @abstractmethod
    async def setup_sensors(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
    ) -> None:
        """Set up all sensors for the integration.

        Args:
            hass: Home Assistant instance.
            entry: Configuration entry.
            async_add_entities: Callback to add entities.
        """


class SensorDataProviderInterface(ABC):
    """Abstract interface for sensor data provision."""

    @abstractmethod
    def get_native_value(self) -> Any:
        """Get the native value for the sensor.

        Returns:
            Native sensor value.
        """

    @abstractmethod
    def get_sensor_attributes(self) -> Optional[Dict[str, Any]]:
        """Get additional sensor attributes.

        Returns:
            Dictionary of sensor attributes or None.
        """
