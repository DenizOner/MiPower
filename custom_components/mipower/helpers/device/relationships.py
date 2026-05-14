"""
Device Relationships Manager - Single Responsibility Principle

This module implements device relationship operations following SOLID
principles, handling device relationship management and hierarchy operations.
"""

import logging
from typing import Dict, Set

from .relationships_interface import DeviceRelationshipsInterface

_LOGGER = logging.getLogger(__name__)


class DeviceRelationshipsManager(DeviceRelationshipsInterface):
    """Manages device relationships and dependencies."""

    def __init__(self):
        """Initialize the relationships manager."""
        self._relationships: Dict[str, Set[str]] = {}

    def add_relationship(self, parent_device: str, child_device: str) -> None:
        """Add a parent-child relationship between devices.

        Args:
            parent_device: Parent device ID
            child_device: Child device ID
        """
        if parent_device not in self._relationships:
            self._relationships[parent_device] = set()
        self._relationships[parent_device].add(child_device)

    def remove_relationship(self, parent_device: str, child_device: str) -> None:
        """Remove a parent-child relationship.

        Args:
            parent_device: Parent device ID
            child_device: Child device ID
        """
        if parent_device in self._relationships:
            self._relationships[parent_device].discard(child_device)
            if not self._relationships[parent_device]:
                del self._relationships[parent_device]

    def get_children(self, parent_device: str) -> Set[str]:
        """Get all child devices for a parent device.

        Args:
            parent_device: Parent device ID

        Returns:
            Set of child device IDs
        """
        return self._relationships.get(parent_device, set()).copy()

    def get_parents(self, child_device: str) -> Set[str]:
        """Get all parent devices for a child device.

        Args:
            child_device: Child device ID

        Returns:
            Set of parent device IDs
        """
        parents = set()
        for parent, children in self._relationships.items():
            if child_device in children:
                parents.add(parent)
        return parents

    def has_relationship(self, parent_device: str, child_device: str) -> bool:
        """Check if a relationship exists.

        Args:
            parent_device: Parent device ID
            child_device: Child device ID

        Returns:
            True if relationship exists
        """
        return child_device in self._relationships.get(parent_device, set())
