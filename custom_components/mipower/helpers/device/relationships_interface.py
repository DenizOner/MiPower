"""Device Relationships Interface - Dependency Inversion for Device Relationship Management

This module defines the abstraction layer for device relationship operations,
allowing DIP by decoupling device relationship logic from the coordinator.
It provides a standardized interface for managing parent-child device relationships.
"""

from abc import ABC, abstractmethod
from typing import Set


class DeviceRelationshipsInterface(ABC):
    """Interface for device relationship operations.

    This abstract base class defines the contract for device relationship components
    in Smartify, providing a consistent API for managing device hierarchies and
    dependencies.
    """

    @abstractmethod
    def add_relationship(self, parent_device: str, child_device: str) -> None:
        """Add a parent-child relationship between devices.

        Args:
            parent_device: Parent device ID
            child_device: Child device ID
        """

    @abstractmethod
    def remove_relationship(self, parent_device: str, child_device: str) -> None:
        """Remove a parent-child relationship.

        Args:
            parent_device: Parent device ID
            child_device: Child device ID
        """

    @abstractmethod
    def get_children(self, parent_device: str) -> Set[str]:
        """Get all child devices for a parent device.

        Args:
            parent_device: Parent device ID

        Returns:
            Set of child device IDs
        """

    @abstractmethod
    def get_parents(self, child_device: str) -> Set[str]:
        """Get all parent devices for a child device.

        Args:
            child_device: Child device ID

        Returns:
            Set of parent device IDs
        """

    @abstractmethod
    def has_relationship(self, parent_device: str, child_device: str) -> bool:
        """Check if a relationship exists.

        Args:
            parent_device: Parent device ID
            child_device: Child device ID

        Returns:
            True if relationship exists
        """
