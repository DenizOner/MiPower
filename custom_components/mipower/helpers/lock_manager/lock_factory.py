"""
Lock Factory for Lock Management - Single Responsibility Principle

This module implements lock creation and management following SOLID principles,
handling hierarchical lock instantiation and validation.
"""

import logging
from typing import Any, Dict, Optional, cast

from .lock_manager_interface import LockFactoryInterface
from .lock_types import HierarchicalLock

_LOGGER = logging.getLogger(__name__)


class LockFactory(LockFactoryInterface):
    """Factory for creating and managing lock instances.

    This class is responsible for lock creation, retrieval, and hierarchy validation.
    Follows Single Responsibility Principle by focusing only on lock lifecycle management.
    """

    def __init__(self):
        """Initialize the lock factory with empty registries."""
        self._locks: Dict[str, HierarchicalLock] = {}
        self._lock_hierarchy: Dict[str, int] = {}

    def create_lock(self, lock_id: str, hierarchy_level: int = 0) -> HierarchicalLock:
        """Create a new hierarchical lock instance.

        Args:
            lock_id: Unique identifier for the lock.
            hierarchy_level: Hierarchical level for lock ordering.

        Returns:
            HierarchicalLock: The created lock instance.
        """
        if lock_id in self._locks:
            _LOGGER.warning(
                "Lock %s already exists, returning existing instance", lock_id
            )
            return self._locks[lock_id]

        lock = HierarchicalLock(lock_id, hierarchy_level)
        self._locks[lock_id] = lock
        self._lock_hierarchy[lock_id] = hierarchy_level

        _LOGGER.debug(
            "Created new hierarchical lock: %s (level %d)",
            lock_id,
            hierarchy_level,
        )
        return lock

    def get_lock(self, lock_id: str) -> Optional[HierarchicalLock]:
        """Get an existing lock instance.

        Args:
            lock_id: Unique identifier for the lock.

        Returns:
            Optional[HierarchicalLock]: The lock instance or None if not found.
        """
        return self._locks.get(lock_id)

    def get_or_create_lock(
        self, lock_id: str, hierarchy_level: int = 0
    ) -> HierarchicalLock:
        """Get an existing lock or create a new one if it doesn't exist.

        Args:
            lock_id: Unique identifier for the lock.
            hierarchy_level: Hierarchical level for new locks.

        Returns:
            HierarchicalLock: The lock instance.
        """
        lock = self.get_lock(lock_id)
        if lock is None:
            lock = self.create_lock(lock_id, hierarchy_level)
        return lock

    def validate_hierarchy(self, lock_id: str, new_level: int) -> bool:
        """Validate lock hierarchy constraints.

        Ensures that lock acquisition follows hierarchical ordering to prevent
        potential deadlocks. Higher level locks should be acquired before lower level ones.

        Args:
            lock_id: The lock to validate.
            new_level: The hierarchical level attempting to acquire the lock.

        Returns:
            bool: True if hierarchy is valid, False otherwise.
        """
        current_level = self._lock_hierarchy.get(lock_id, -1)

        # If lock doesn't exist, hierarchy is valid (will be set when created)
        if current_level == -1:
            return True

        # Validate hierarchy: new level must be >= current level
        is_valid = new_level >= current_level

        if not is_valid:
            _LOGGER.warning(
                "Lock hierarchy violation: lock %s (level %d) cannot be acquired "
                "by level %d (must be >= %d)",
                lock_id,
                current_level,
                new_level,
                current_level,
            )

        return is_valid

    def update_hierarchy_level(self, lock_id: str, new_level: int) -> bool:
        """Update the hierarchy level of an existing lock.

        Args:
            lock_id: The lock to update.
            new_level: The new hierarchy level.

        Returns:
            bool: True if update was successful, False if lock doesn't exist.
        """
        if lock_id not in self._locks:
            _LOGGER.warning(
                "Cannot update hierarchy for non-existent lock: %s", lock_id
            )
            return False

        old_level = self._lock_hierarchy[lock_id]
        self._lock_hierarchy[lock_id] = new_level

        _LOGGER.debug(
            "Updated hierarchy level for lock %s: %d -> %d",
            lock_id,
            old_level,
            new_level,
        )
        return True

    def get_lock_info(self, lock_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a lock.

        Args:
            lock_id: The lock to get information for.

        Returns:
            Optional[Dict[str, any]]: Lock information or None if not found.
        """
        lock = self.get_lock(lock_id)
        if lock is None:
            return None

        return {
            "lock_id": lock_id,
            "hierarchy_level": self._lock_hierarchy.get(lock_id, 0),
            "is_owned": lock._owner is not None,
            "owner": lock._owner,
            "hold_time": lock.get_hold_time(),
        }

    def get_all_locks_info(self) -> Dict[str, Dict[str, Any]]:
        """Get information about all managed locks.

        Returns:
            Dict[str, Dict[str, any]]: Information for all locks.
        """
        return {lock_id: cast(Dict[str, Any], self.get_lock_info(lock_id)) for lock_id in self._locks.keys()}

    def get_locks_by_hierarchy_level(self, level: int) -> list[str]:
        """Get all lock IDs at a specific hierarchy level.

        Args:
            level: The hierarchy level to filter by.

        Returns:
            list[str]: List of lock IDs at the specified level.
        """
        return [
            lock_id
            for lock_id, lock_level in self._lock_hierarchy.items()
            if lock_level == level
        ]

    def cleanup_lock(self, lock_id: str) -> bool:
        """Remove a lock from management.

        Args:
            lock_id: The lock to remove.

        Returns:
            bool: True if lock was removed, False if it didn't exist.
        """
        if lock_id not in self._locks:
            return False

        # Force release if owned
        lock = self._locks[lock_id]
        if lock._owner is not None:
            lock.release(lock._owner)
            _LOGGER.warning("Force released lock %s during cleanup", lock_id)

        del self._locks[lock_id]
        del self._lock_hierarchy[lock_id]

        _LOGGER.debug("Cleaned up lock: %s", lock_id)
        return True

    def cleanup_all_locks(self) -> int:
        """Remove all locks from management.

        Returns:
            int: Number of locks that were cleaned up.
        """
        lock_count = len(self._locks)
        lock_ids = list(self._locks.keys())

        for lock_id in lock_ids:
            self.cleanup_lock(lock_id)

        _LOGGER.debug("Cleaned up %d locks", lock_count)
        return lock_count

    def get_statistics(self) -> Dict[str, Any]:
        """Get factory statistics.

        Returns:
            Dict[str, any]: Statistics about lock management.
        """
        hierarchy_levels = set(self._lock_hierarchy.values())

        return {
            "total_locks": len(self._locks),
            "hierarchy_levels": len(hierarchy_levels),
            "locks_per_level": {
                level: len(self.get_locks_by_hierarchy_level(level))
                for level in sorted(hierarchy_levels)
            },
        }
