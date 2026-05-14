"""
Deadlock Detector for Lock Management - Single Responsibility Principle

This module implements deadlock detection functionality following SOLID principles,
handling wait-for graph analysis and cycle detection for concurrent lock management.
"""

import logging
from collections import defaultdict
from typing import Dict

from .lock_manager_interface import DeadlockDetectorInterface, LockInfo

_LOGGER = logging.getLogger(__name__)


class DeadlockDetector(DeadlockDetectorInterface):
    """Handles deadlock detection for lock management operations.

    This class is responsible for maintaining a wait-for graph and detecting
    cycles that would indicate deadlocks. Follows Single Responsibility
    Principle by focusing only on deadlock detection logic.
    """

    def __init__(self):
        """Initialize the deadlock detector with empty wait-for graph."""
        self._wait_for_graph: Dict[str, set[str]] = defaultdict(set)

    def detect_deadlock(
        self, owner: str, lock_id: str, active_locks: Dict[str, "LockInfo"]
    ) -> bool:
        """Detect if acquiring a lock would cause a deadlock using wait-for graph analysis.

        Implements cycle detection using DFS (Depth-First Search) algorithm.
        Maintains a wait-for graph where edges represent waiting relationships.

        Args:
            owner: The owner requesting the lock.
            lock_id: The lock being requested.
            active_locks: Dictionary of currently active locks.

        Returns:
            bool: True if deadlock would occur, False otherwise.
        """
        # Find who currently owns the lock
        current_owner = self._find_lock_owner(lock_id, active_locks)

        if not current_owner or current_owner == owner:
            return False

        # Add edge to wait-for graph: owner -> current_owner
        self._wait_for_graph[owner].add(current_owner)

        # Check for cycle using DFS
        if self._has_cycle(owner):
            # Remove the edge we just added since it causes deadlock
            self._wait_for_graph[owner].discard(current_owner)
            _LOGGER.error(
                "Deadlock detected involving owner %s waiting for %s",
                owner,
                current_owner,
                exc_info=True,
            )
            return True

        return False

    def _find_lock_owner(
        self, lock_id: str, active_locks: Dict[str, "LockInfo"]
    ) -> str:
        """Find the current owner of a lock.

        Args:
            lock_id: The lock ID to find owner for.
            active_locks: Dictionary of active locks.

        Returns:
            str: The owner of the lock, or empty string if not found.
        """
        for lock_info in active_locks.values():
            if lock_info.lock_id == lock_id:
                return lock_info.owner
        return ""

    def _has_cycle(self, start_node: str) -> bool:
        """Check for cycles in the wait-for graph using DFS.

        Args:
            start_node: The node to start DFS from.

        Returns:
            bool: True if a cycle is detected, False otherwise.
        """
        visited = set()
        rec_stack = set()

        def dfs(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)

            for neighbor in self._wait_for_graph.get(node, set()):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.remove(node)
            return False

        return dfs(start_node)

    def cleanup_wait_edges(self, released_owner: str) -> None:
        """Clean up wait-for graph edges when a lock is released.

        Removes all edges pointing to the released owner since they
        are no longer waiting for that owner.

        Args:
            released_owner: The owner who released their locks.
        """
        # Remove any edges pointing to this owner
        for waiting_owner in list(self._wait_for_graph.keys()):
            self._wait_for_graph[waiting_owner].discard(released_owner)
            if not self._wait_for_graph[waiting_owner]:
                del self._wait_for_graph[waiting_owner]

    def get_wait_for_graph(self) -> Dict[str, set[str]]:
        """Get a copy of the current wait-for graph.

        Returns:
            Dict[str, set[str]]: Copy of the wait-for graph for analysis.
        """
        return dict(self._wait_for_graph)

    def clear_graph(self) -> None:
        """Clear the entire wait-for graph."""
        self._wait_for_graph.clear()
        _LOGGER.debug("Wait-for graph cleared")
