"""
Batch Processing Interface - Dependency Inversion for Async Operations

This module defines the abstraction layer for batch processing in Smartify,
implementing Dependency Inversion Principle (DIP) by decoupling batch execution
logic from the coordinator and other high-level components.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Awaitable, Callable, Dict, List, Optional


class BatchStatus(Enum):
    """Enumeration of possible batch operation statuses.

    This enum represents the various states a batch or individual operation
    can be in during its lifecycle.
    """

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class BatchOperation:
    """Represents a single operation within a batch.

    This dataclass contains all the information needed to execute and track
    an individual asynchronous operation within a batch processing context.
    """

    operation_id: str
    operation_func: Callable[..., Awaitable[Any]]
    args: tuple = field(default_factory=tuple)
    kwargs: Dict[str, Any] = field(default_factory=dict)
    priority: int = 0
    dependencies: List[str] = field(default_factory=list)
    status: BatchStatus = BatchStatus.PENDING
    result: Any = None
    error: Optional[Exception] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    retry_count: int = 0
    max_retries: int = 3
    retry_delay: float = 1.0

    def get_duration(self) -> Optional[float]:
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "operation_id": self.operation_id,
            "status": self.status.value,
            "priority": self.priority,
            "dependencies": self.dependencies.copy(),
            "duration": self.get_duration(),
            "has_result": self.result is not None,
            "has_error": self.error is not None,
        }


@dataclass
class BatchResult:
    """Contains the results and statistics of a batch execution.

    This dataclass holds all information about a completed batch operation,
    including execution times, success rates, and individual operation results.
    """

    batch_id: str
    status: BatchStatus
    total_operations: int
    completed_operations: int
    failed_operations: int
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    results: Dict[str, Any] = field(default_factory=dict)
    errors: Dict[str, Exception] = field(default_factory=dict)

    def get_duration(self) -> Optional[float]:
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None

    def get_success_rate(self) -> float:
        if self.total_operations == 0:
            return 100.0
        return (self.completed_operations / self.total_operations) * 100.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "batch_id": self.batch_id,
            "status": self.status.value,
            "total_operations": self.total_operations,
            "completed_operations": self.completed_operations,
            "failed_operations": self.failed_operations,
            "duration": self.get_duration(),
            "success_rate": round(self.get_success_rate(), 2),
            "results_count": len(self.results),
            "errors_count": len(self.errors),
        }


class BatchCreatorInterface(ABC):
    """Abstract interface for batch creation functionality."""

    @abstractmethod
    async def create_batch(self, batch_id: str) -> str:
        """Create a new batch with the given ID.

        Args:
            batch_id: Unique identifier for the batch.

        Returns:
            str: The batch ID that was created.
        """

    @abstractmethod
    async def add_operation(
        self,
        batch_id: str,
        operation_id: str,
        operation_func: Callable[..., Awaitable[Any]],
        priority: int = 0,
        dependencies: Optional[List[str]] = None,
        *args,
        **kwargs,
    ) -> None:
        """Add an operation to an existing batch.

        Args:
            batch_id: The batch to add the operation to.
            operation_id: Unique identifier for the operation.
            operation_func: The async function to execute.
            priority: Priority level for execution order.
            dependencies: List of operation IDs this operation depends on.
            *args: Positional arguments for the operation function.
            **kwargs: Keyword arguments for the operation function.
        """


class BatchExecutorInterface(ABC):
    """Abstract interface for batch execution functionality."""

    @abstractmethod
    async def execute_batch(self, batch_id: str) -> BatchResult:
        """Execute all operations in the specified batch.

        Args:
            batch_id: The batch to execute.

        Returns:
            BatchResult: Results and statistics of the batch execution.
        """

    @abstractmethod
    async def cancel_batch(self, batch_id: str) -> bool:
        """Cancel execution of a batch.

        Args:
            batch_id: The batch to cancel.

        Returns:
            bool: True if cancellation was successful.
        """


class BatchQueryInterface(ABC):
    """Abstract interface for batch querying functionality."""

    @abstractmethod
    def get_batch_status(self, batch_id: str) -> Optional[BatchResult]:
        """Get the current status of a batch.

        Args:
            batch_id: The batch to query.

        Returns:
            Optional[BatchResult]: Current batch status or None if not found.
        """

    @abstractmethod
    def get_batch_operations(self, batch_id: str) -> Dict[str, BatchOperation]:
        """Get all operations in a batch.

        Args:
            batch_id: The batch to query.

        Returns:
            Dict[str, BatchOperation]: Dictionary of operation ID to operation.
        """


class PerformanceMonitorInterface(ABC):
    """Abstract interface for performance monitoring functionality."""

    @abstractmethod
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics for the batch processor.

        Returns:
            Dict[str, Any]: Performance metrics and statistics.
        """


class BatchCleanupInterface(ABC):
    """Abstract interface for batch cleanup functionality."""

    @abstractmethod
    async def cleanup(self) -> None:
        """Clean up resources and reset the batch processor."""


class DependencyResolverInterface(ABC):
    """Abstract interface for dependency resolution functionality."""

    @abstractmethod
    def detect_circular_dependencies(
        self, operations: Dict[str, BatchOperation]
    ) -> bool:
        """Detect circular dependencies in a set of operations.

        Args:
            operations: Dictionary of operation ID to operation.

        Returns:
            bool: True if circular dependencies are detected.
        """


class OperationExecutorInterface(ABC):
    """Abstract interface for operation execution functionality."""

    @abstractmethod
    async def execute_operation(self, batch_id: str, operation: BatchOperation) -> None:
        """Execute a single operation.

        Args:
            batch_id: The batch the operation belongs to.
            operation: The operation to execute.
        """


class StatisticsTrackerInterface(ABC):
    """Abstract interface for statistics tracking functionality."""

    @abstractmethod
    def update_batch_statistics(self, batch_result: BatchResult) -> None:
        """Update statistics based on batch execution results.

        Args:
            batch_result: The results of a batch execution.
        """

    @abstractmethod
    def get_statistics(self) -> Dict[str, Any]:
        """Get current statistics.

        Returns:
            Dict[str, Any]: Current statistics data.
        """


class BatchProcessorInterface(
    BatchCreatorInterface,
    BatchExecutorInterface,
    BatchQueryInterface,
    PerformanceMonitorInterface,
    BatchCleanupInterface,
    ABC,
):
    """Unified interface for batch processing functionality.

    This interface combines all batch processing interfaces into a single
    abstraction, following the Interface Segregation Principle by allowing
    clients to depend on the complete batch processing contract.
    """
