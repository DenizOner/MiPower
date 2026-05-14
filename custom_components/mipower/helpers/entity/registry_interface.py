"""Entity Registry Interface - Dependency Inversion for Entity Management

This module defines the abstraction layer for entity registry operations,
allowing DIP by decoupling entity registry logic from the coordinator.
It provides a standardized interface for entity lookup and registry access
with error handling and logging capabilities.
"""

from abc import ABC, abstractmethod
from typing import Any, List

from homeassistant.core import HomeAssistant  # type: ignore[import]


class EntityRegistryInterface(ABC):
    """Interface for entity registry operations.

    This abstract base class defines the contract for entity registry components
    in Smartify, providing a consistent API for entity registry access and
    entity lookup with error handling.
    """

    @abstractmethod
    def get_entity_registry(self, hass: HomeAssistant) -> Any:
        """Get the Home Assistant entity registry.

        Args:
            hass: Home Assistant instance.

        Returns:
            Entity registry instance.

        Raises:
            RuntimeError: If accessing the registry fails.
        """

    @abstractmethod
    def get_entities_for_device(self, hass: HomeAssistant, device_id: str) -> List[Any]:
        """Get all entities associated with a specific device.

        Args:
            hass: Home Assistant instance.
            device_id: The device ID to get entities for.

        Returns:
            List of entity entries for the device.
        """
