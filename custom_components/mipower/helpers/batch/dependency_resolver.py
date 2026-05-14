"""
Dependency Resolver for Batch Operations - Single Responsibility Principle

This module implements dependency resolution functionality following SOLID principles,
specifically handling circular dependency detection and topological sorting.
"""

import logging
from collections import deque
from typing import Dict

from ..logger.batch_logger import dependency_logging
from .batch_interface import BatchOperation, DependencyResolverInterface

_LOGGER = logging.getLogger(__name__)


class DependencyResolver(DependencyResolverInterface):
    """Handles dependency resolution for batch operations.

    This class is responsible for detecting circular dependencies and
    ensuring operations can be executed in the correct order.
    Follows Single Responsibility Principle by focusing only on dependency logic.
    """

    @dependency_logging()
    def detect_circular_dependencies(
        self, operations: Dict[str, BatchOperation]
    ) -> bool:
        """Detect circular dependencies using optimized topological sort algorithm.

        Implements Kahn's algorithm with early cycle detection for performance.
        Uses deque for O(1) queue operations.

        Args:
            operations: Dictionary of operation ID to BatchOperation.

        Returns:
            bool: True if circular dependencies are detected, False otherwise.
        """
        if not operations:
            return False

        # Build adjacency list and indegree map for topological sort
        adj_list = {op_id: [] for op_id in operations}
        indegree = {op_id: 0 for op_id in operations}

        # Populate adjacency list and indegree counts
        for op_id, operation in operations.items():
            for dep in operation.dependencies:
                if (
                    dep in operations
                ):  # Only consider dependencies that exist in this batch
                    adj_list[dep].append(op_id)
                    indegree[op_id] += 1

        # Initialize queue with nodes having no dependencies (indegree 0)
        queue = deque(op_id for op_id, degree in indegree.items() if degree == 0)
        processed = 0
        total_operations = len(operations)

        # Process nodes in topological order
        while queue:
            current = queue.popleft()
            processed += 1

            # Early exit: if we've processed all nodes, no cycle exists
            if processed == total_operations:
                return False

            # Reduce indegree of neighbors and add to queue if indegree becomes 0
            for neighbor in adj_list[current]:
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    queue.append(neighbor)

        # If not all operations were processed, there's a cycle
        has_cycle = processed != total_operations
        if has_cycle:
            _LOGGER.warning(
                "Circular dependency detected in operations: %s",
                list(operations.keys()),
            )

        return has_cycle

    @dependency_logging()
    def get_execution_order(self, operations: Dict[str, BatchOperation]) -> list:
        """Get the execution order for operations based on dependencies.

        Returns a valid execution order if no circular dependencies exist.
        If circular dependencies are detected, returns an empty list.

        Args:
            operations: Dictionary of operation ID to BatchOperation.

        Returns:
            list: List of operation IDs in execution order, or empty list if cycle detected.
        """
        if self.detect_circular_dependencies(operations):
            return []

        # Build adjacency list and indegree map
        adj_list = {op_id: [] for op_id in operations}
        indegree = {op_id: 0 for op_id in operations}

        for op_id, operation in operations.items():
            for dep in operation.dependencies:
                if dep in operations:
                    adj_list[dep].append(op_id)
                    indegree[op_id] += 1

        # Topological sort using Kahn's algorithm
        queue = deque(op_id for op_id, degree in indegree.items() if degree == 0)
        execution_order = []

        while queue:
            current = queue.popleft()
            execution_order.append(current)

            for neighbor in adj_list[current]:
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    queue.append(neighbor)

        return execution_order if len(execution_order) == len(operations) else []
