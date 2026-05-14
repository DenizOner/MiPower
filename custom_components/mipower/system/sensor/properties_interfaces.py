"""
Sensor Properties Interfaces - Dependency Inversion for Sensor Properties

This module defines the abstraction layer for sensor properties functionality in Smartify,
implementing Dependency Inversion Principle (DIP) by decoupling properties operations
from the core properties logic.
"""

from abc import ABC, abstractmethod
from typing import Any


class SensorDeviceInfoProviderInterface(ABC):
    """Abstract interface for device information operations."""

    @abstractmethod
    def get_device_info(self, sensor) -> dict[str, Any]:
        """Get device information for the sensor entity."""


class SensorStateProviderInterface(ABC):
    """Abstract interface for sensor operations."""

    @abstractmethod
    def get_native_value(self, sensor) -> Any:
        """Get the native value of the sensor."""


class SensorAvailabilityCheckerInterface(ABC):
    """Abstract interface for availability checking operations."""

    @abstractmethod
    def get_available(self, sensor) -> bool:
        """Get the availability status of the sensor."""


class SensorPropertiesManagerInterface(ABC):
    """Abstract interface for properties management operations."""

    @abstractmethod
    def get_device_info(self, entity) -> dict[str, Any]:
        """Get device information."""

    @abstractmethod
    def get_available(self, entity) -> bool:
        """Get availability status."""

    @abstractmethod
    def get_native_value(self, entity) -> Any:
        """Get sensor native value."""
