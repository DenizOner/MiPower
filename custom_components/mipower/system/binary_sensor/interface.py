"""
Binary Sensor Interface - Dependency Inversion for Binary Sensor Management

This module defines the abstraction layer for binary sensor functionality in Smartify,
implementing Dependency Inversion Principle (DIP) by decoupling binary sensor operations
from the core components.
"""

from abc import ABC, abstractmethod
from typing import Any, List

from homeassistant.config_entries import ConfigEntry  # type: ignore[import]
from homeassistant.core import HomeAssistant  # type: ignore[import]
from homeassistant.helpers.entity_platform import AddEntitiesCallback  # type: ignore[import]


class BinarySensorFactoryInterface(ABC):
    """Abstract interface for binary sensor factory functionality."""

    @abstractmethod
    def create_connectivity_sensor(self, entry: ConfigEntry, coordinator) -> Any:
        """Create a connectivity sensor instance.

        Args:
            entry: Configuration entry.
            coordinator: Data coordinator.

        Returns:
            Connectivity sensor instance.
        """

    @abstractmethod
    def create_all_binary_sensors(self, entry: ConfigEntry, coordinator) -> List[Any]:
        """Create all binary sensors for the integration.

        Args:
            entry: Configuration entry.
            coordinator: Data coordinator.

        Returns:
            List of all binary sensor instances.
        """


class BinarySensorSetupInterface(ABC):
    """Abstract interface for binary sensor setup functionality."""

    @abstractmethod
    async def setup_binary_sensors(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
    ) -> None:
        """Set up all binary sensors for the integration.

        Args:
            hass: Home Assistant instance.
            entry: Configuration entry.
            async_add_entities: Callback to add entities.
        """


# Binary Sensor Properties Interfaces for SOLID Architecture


class BinarySensorDeviceInfoProviderInterface(ABC):
    """Abstract interface for device information operations."""

    @abstractmethod
    def get_device_info(self, binary_sensor) -> dict[str, Any]:
        """Get device information for the binary sensor entity."""


class BinarySensorStateProviderInterface(ABC):
    """Abstract interface for binary sensor state operations."""

    @abstractmethod
    def get_is_on(self, binary_sensor) -> bool:
        """Get the current on/off state of the binary sensor."""


class BinarySensorPropertiesManagerInterface(ABC):
    """Abstract interface for properties management operations."""

    @abstractmethod
    def get_device_info(self, entity) -> dict[str, Any]:
        """Get device information."""

    @abstractmethod
    def get_is_on(self, entity) -> bool:
        """Get current state."""

    @abstractmethod
    def get_available(self, entity) -> bool:
        """Get availability status."""


class BinarySensorDataProviderInterface(ABC):
    """Abstract interface for binary sensor data provision."""

    @abstractmethod
    def get_sensor_state(self) -> bool:
        """Get the binary sensor state.

        Returns:
            True if sensor is on, False otherwise.
        """

    @abstractmethod
    def get_sensor_attributes(self) -> dict[str, Any]:
        """Get additional sensor attributes.

        Returns:
            Dictionary of sensor attributes.
        """
