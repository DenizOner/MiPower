"""Entity Discovery Interface - Dependency Inversion for Entity Discovery

This module defines the abstraction layer for entity discovery operations,
allowing DIP by decoupling entity discovery logic from other components.
It provides a standardized interface for entity discovery and management
with error handling and logging capabilities.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class EntityDiscoveryInterface(ABC):
    """Interface for entity discovery operations.

    This abstract base class defines the contract for entity discovery components
    in Smartify, providing a consistent API for entity discovery and registry access
    with error handling.
    """

    @abstractmethod
    def discover_entities(
        self, domain: str, device_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Discover entities for a given domain and device.

        Args:
            domain: Entity domain (e.g., 'sensor', 'switch')
            device_id: Optional device ID to filter

        Returns:
            List of discovered entity information
        """

    @abstractmethod
    def register_entity(
        self,
        entity_id: str,
        config_entry_id: str,
        device_id: Optional[str] = None,
    ) -> None:
        """Register an entity in the registry.

        Args:
            entity_id: Entity ID
            config_entry_id: Configuration entry ID
            device_id: Optional device ID
        """

    @abstractmethod
    def disable_entity(self, entity_id: str) -> None:
        """Disable an entity.

        Args:
            entity_id: Entity ID to disable
        """

    @abstractmethod
    def enable_entity(self, entity_id: str) -> None:
        """Enable an entity.

        Args:
            entity_id: Entity ID to enable
        """
