"""
Services Interface - Dependency Inversion for Service Management

This module defines the abstraction layer for service management functionality in Smartify,
implementing Dependency Inversion Principle (DIP) by decoupling service operations
from the core components.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from homeassistant.core import HomeAssistant  # type: ignore[import]


class ServiceRegistryInterface(ABC):
    """Abstract interface for service registry functionality."""

    @abstractmethod
    async def register_services(self, hass: HomeAssistant) -> bool:
        """Register all Smartify services.

        Args:
            hass: Home Assistant instance.

        Returns:
            True if registration successful, False otherwise.
        """

    @abstractmethod
    def unregister_services(self, hass: HomeAssistant) -> bool:
        """Unregister all Smartify services.

        Args:
            hass: Home Assistant instance.

        Returns:
            True if unregistration successful, False otherwise.
        """


class ServiceValidatorInterface(ABC):
    """Abstract interface for service validation functionality."""

    @abstractmethod
    def validate_service_call(
        self, service_name: str, service_data: Dict[str, Any]
    ) -> bool:
        """Validate a service call.

        Args:
            service_name: Name of the service.
            service_data: Service call data.

        Returns:
            True if validation passes, False otherwise.
        """

    @abstractmethod
    def get_service_schema(self, service_name: str) -> Optional[Dict[str, Any]]:
        """Get the schema for a service.

        Args:
            service_name: Name of the service.

        Returns:
            Service schema or None if not found.
        """


class ServiceExecutorInterface(ABC):
    """Abstract interface for service execution functionality."""

    @abstractmethod
    async def execute_send_command(
        self, entity_id: str, command_data: Dict[str, Any]
    ) -> bool:
        """Execute send_command service.

        Args:
            entity_id: Target entity ID.
            command_data: Command data.

        Returns:
            True if execution successful, False otherwise.
        """

    @abstractmethod
    async def execute_force_verify(self, entity_id: str) -> bool:
        """Execute force_verify service.

        Args:
            entity_id: Target entity ID.

        Returns:
            True if execution successful, False otherwise.
        """

    @abstractmethod
    async def execute_calibrate(self, entity_id: str) -> bool:
        """Execute calibrate service.

        Args:
            entity_id: Target entity ID.

        Returns:
            True if execution successful, False otherwise.
        """
