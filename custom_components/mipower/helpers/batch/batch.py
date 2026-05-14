"""
Smartify helpers async batch module - SOLID Refactored Implementation.

This module provides batch processing functionality following SOLID principles,
using composition pattern with separated responsibilities for dependency resolution,
operation execution, and statistics tracking.
"""

import asyncio
import logging
from datetime import datetime
from typing import Any, Awaitable, Callable, Dict, List, Optional

from ..errors.exceptions import BatchOperationError
from ..logger.batch_logger import batch_operation_logging
from ..monitoring import record_batch_metric
from .batch_interface import (
    BatchCleanupInterface,
    BatchCreatorInterface,
    BatchExecutorInterface,
    BatchOperation,
    BatchQueryInterface,
    BatchResult,
    BatchStatus,
    PerformanceMonitorInterface,
)
from .dependency_resolver import DependencyResolver
from .statistics_tracker import StatisticsTracker

# HomeAssistant type for compatibility
HomeAssistant = Any

_LOGGER = logging.getLogger(__name__)


class BatchProcessor(
    BatchCreatorInterface,
    BatchExecutorInterface,
    BatchQueryInterface,
    PerformanceMonitorInterface,
    BatchCleanupInterface,
):
    """Manages batch processing of asynchronous operations with dependencies.

    This class implements BatchProcessorInterface and uses composition pattern
    with separated responsibilities following SOLID principles:
    - DependencyResolver for circular dependency detection
    - OperationExecutor for individual operation execution
    - StatisticsTracker for performance metrics

    Follows Single Responsibility Principle by delegating specific tasks
    to specialized components while orchestrating the overall process.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        max_concurrency: int = 5,
        max_batch_size: int = 100,
        default_timeout: float = 30.0,
        dependency_resolver=None,
        operation_executor=None,
        statistics_tracker=None,
    ):
        self._hass = hass
        self.max_concurrency = max_concurrency
        self.max_batch_size = max_batch_size
        self.default_timeout = default_timeout

        # Initialize SOLID components using composition with optional parameters for testability
        self._dependency_resolver = dependency_resolver or DependencyResolver()
        self._statistics_tracker = statistics_tracker or StatisticsTracker()

        # Core batch management
        self._batches: Dict[str, Dict[str, BatchOperation]] = {}
        self._batch_results: Dict[str, BatchResult] = {}
        self._semaphore = asyncio.Semaphore(max_concurrency)
        self._active_operations: Dict[str, asyncio.Task] = {}

        # Initialize operation executor with self-reference or provided instance
        if operation_executor:
            self._operation_executor = operation_executor
        else:
            from .operation_executor import OperationExecutor

            self._operation_executor = OperationExecutor(self)

        _LOGGER.debug(
            "BatchProcessor initialized with SOLID components: "
            "concurrency=%d, batch_size=%d",
            max_concurrency,
            max_batch_size,
        )

    @classmethod
    def create(
        cls,
        hass: HomeAssistant,
        max_concurrency: int = 5,
        max_batch_size: int = 100,
        default_timeout: float = 30.0,
        dependency_resolver=None,
        operation_executor=None,
        statistics_tracker=None,
    ):
        """Factory method for creating BatchProcessor instances with optional dependencies.

        This factory method enables interface mocking for testing by allowing
        injection of mock implementations for internal components.

        Args:
            hass: Home Assistant instance
            max_concurrency: Maximum concurrent operations
            max_batch_size: Maximum operations per batch
            default_timeout: Default operation timeout
            dependency_resolver: Optional DependencyResolverInterface implementation
            operation_executor: Optional OperationExecutorInterface implementation
            statistics_tracker: Optional StatisticsTrackerInterface implementation

        Returns:
            BatchProcessor: Configured instance
        """
        return cls(
            hass=hass,
            max_concurrency=max_concurrency,
            max_batch_size=max_batch_size,
            default_timeout=default_timeout,
            dependency_resolver=dependency_resolver,
            operation_executor=operation_executor,
            statistics_tracker=statistics_tracker,
        )

    @batch_operation_logging()
    async def create_batch(self, batch_id: str) -> str:
        if batch_id in self._batches:
            raise BatchOperationError(f"Batch {batch_id} already exists")
        self._batches[batch_id] = {}
        self._batch_results[batch_id] = BatchResult(
            batch_id=batch_id,
            status=BatchStatus.PENDING,
            total_operations=0,
            completed_operations=0,
            failed_operations=0,
        )
        _LOGGER.debug("Created batch: %s", batch_id)
        return batch_id

    @batch_operation_logging()
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
        if batch_id not in self._batches:
            await self.create_batch(batch_id)
        if operation_id in self._batches[batch_id]:
            raise BatchOperationError(
                f"Operation {operation_id} already exists in batch {batch_id}"
            )
        if len(self._batches[batch_id]) >= self.max_batch_size:
            raise BatchOperationError(f"Batch {batch_id} is at maximum capacity")
        operation = BatchOperation(
            operation_id=operation_id,
            operation_func=operation_func,
            args=args,
            kwargs=kwargs,
            priority=priority,
            dependencies=dependencies or [],
            status=BatchStatus.PENDING,
        )
        self._batches[batch_id][operation_id] = operation
        self._batch_results[batch_id].total_operations += 1
        _LOGGER.debug(
            "Added operation to batch %s: %s (priority=%d, deps=%d)",
            batch_id,
            operation_id,
            priority,
            len(dependencies or []),
        )

    @batch_operation_logging()
    async def execute_batch(self, batch_id: str) -> BatchResult:
        if batch_id not in self._batches:
            raise BatchOperationError(f"Batch {batch_id} does not exist")
        batch_result = self._batch_results[batch_id]
        batch_result.status = BatchStatus.RUNNING
        batch_result.start_time = datetime.now()
        _LOGGER.info(
            "Starting batch execution: %s (%d operations)",
            batch_id,
            batch_result.total_operations,
        )
        try:
            await self._execute_with_dependencies(batch_id)
            if batch_result.failed_operations == 0:
                batch_result.status = BatchStatus.COMPLETED
            else:
                batch_result.status = BatchStatus.FAILED
        except Exception as e:
            _LOGGER.error(
                "Batch execution failed: %s",
                e,
                exc_info=True,
            )
            batch_result.status = BatchStatus.FAILED
        finally:
            batch_result.end_time = datetime.now()
            duration = batch_result.get_duration() or 0
            success_rate = batch_result.get_success_rate()
            self._statistics_tracker.update_batch_statistics(batch_result)

            # Record monitoring metrics
            record_batch_metric("batch_duration", duration, batch_id)
            record_batch_metric("batch_success_rate", success_rate, batch_id)
            record_batch_metric(
                "batch_operations_total",
                batch_result.total_operations,
                batch_id,
            )
            record_batch_metric(
                "batch_operations_completed",
                batch_result.completed_operations,
                batch_id,
            )
            record_batch_metric(
                "batch_operations_failed",
                batch_result.failed_operations,
                batch_id,
            )

        _LOGGER.info(
            "Batch execution complete: %s (%.1f%% success rate, %.2fs)",
            batch_id,
            success_rate,
            duration,
        )
        return batch_result

    async def _execute_with_dependencies(self, batch_id: str) -> None:
        operations = self._batches[batch_id]
        completed_operations = set()
        in_progress = set()

        # Check for circular dependencies before execution
        if self._dependency_resolver.detect_circular_dependencies(operations):
            _LOGGER.error(
                "Circular dependency detected in batch %s",
                batch_id,
                exc_info=True,
            )
            for op_id, operation in operations.items():
                operation.status = BatchStatus.FAILED
                operation.error = RuntimeError(f"Circular dependency involving {op_id}")
                batch_result = self._batch_results[batch_id]
                batch_result.failed_operations += 1
                batch_result.errors[op_id] = operation.error
            return

        while len(completed_operations) < len(operations):
            ready_operations = []
            for op_id, operation in operations.items():
                if (
                    op_id not in completed_operations
                    and op_id not in in_progress
                    and all(
                        dep in completed_operations for dep in operation.dependencies
                    )
                ):
                    ready_operations.append(operation)

            if not ready_operations:
                if in_progress:
                    await asyncio.sleep(0.1)
                    continue
                else:
                    break

            ready_operations.sort(key=lambda op: op.priority, reverse=True)
            batch_size = min(len(ready_operations), self.max_concurrency)
            current_batch = ready_operations[:batch_size]

            tasks = []
            for operation in current_batch:
                task = asyncio.create_task(
                    self._operation_executor.execute_operation(batch_id, operation)
                )
                tasks.append(task)
                in_progress.add(operation.operation_id)

            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
                for op in current_batch:
                    in_progress.remove(op.operation_id)
                    completed_operations.add(op.operation_id)

    @batch_operation_logging()
    def get_batch_status(self, batch_id: str) -> Optional[BatchResult]:
        return self._batch_results.get(batch_id)

    @batch_operation_logging()
    def get_batch_operations(self, batch_id: str) -> Dict[str, BatchOperation]:
        return self._batches.get(batch_id, {})

    @batch_operation_logging()
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics from the statistics tracker.

        Returns:
            Dict[str, Any]: Performance metrics and statistics.
        """
        return self._statistics_tracker.get_statistics()

    @batch_operation_logging()
    def get_batch_summary(self) -> Dict[str, Any]:
        return {
            "active_batches": len(self._batches),
            "total_operations": sum(len(ops) for ops in self._batches.values()),
            "active_operations": len(self._active_operations),
            "max_concurrency": self.max_concurrency,
            "max_batch_size": self.max_batch_size,
            "performance_stats": self.get_performance_stats(),
        }

    @batch_operation_logging()
    async def cancel_batch(self, batch_id: str) -> bool:
        if batch_id not in self._batches:
            return False
        for operation_id, task in list(self._active_operations.items()):
            if operation_id.startswith(f"{batch_id}:"):
                task.cancel()
        if batch_id in self._batch_results:
            self._batch_results[batch_id].status = BatchStatus.CANCELLED
        _LOGGER.info("Batch cancelled: %s", batch_id)
        return True

    @batch_operation_logging()
    async def cleanup(self) -> None:
        for task in self._active_operations.values():
            if not task.done():
                task.cancel()
        self._active_operations.clear()
        self._batches.clear()
        self._batch_results.clear()
        self._statistics_tracker.reset_statistics()
        _LOGGER.info("BatchProcessor cleanup completed")


async def process_batch_operations(
    operations: List[Callable[..., Awaitable[Any]]],
    max_concurrency: int = 5,
    timeout: float = 30.0,
) -> List[Any]:
    """Process a list of operations with controlled concurrency.

    Executes multiple asynchronous operations concurrently using a semaphore
    to limit the number of simultaneous operations.

    Args:
        operations: List of callable operations to execute.
        max_concurrency: Maximum number of operations to run concurrently.
        timeout: Timeout in seconds for each individual operation.

    Returns:
        List of results from the operations, with exceptions for failed operations.
    """

    semaphore = asyncio.Semaphore(max_concurrency)
    results = [None] * len(operations)
    errors = [None] * len(operations)

    async def execute_with_semaphore(
        index: int, operation: Callable[..., Awaitable[Any]]
    ):
        async with semaphore:
            try:
                results[index] = await asyncio.wait_for(operation(), timeout=timeout)
            except Exception as e:
                errors[index] = e  # type: ignore[assignment]

    tasks = [
        asyncio.create_task(execute_with_semaphore(i, op))
        for i, op in enumerate(operations)
    ]
    await asyncio.gather(*tasks, return_exceptions=True)
    final_results = []
    for i, (result, error) in enumerate(zip(results, errors)):
        if error:
            final_results.append(error)
        else:
            final_results.append(result)
    return final_results


async def execute_with_priority(
    operations: List[tuple[Callable[..., Awaitable[Any]], int]],
    max_concurrency: int = 5,
) -> List[Any]:
    """Execute operations with priority ordering and concurrency control.

    Processes a list of operations sorted by priority (highest first) using
    a priority queue and semaphore for controlled concurrent execution.

    Args:
        operations: List of tuples containing (operation_callable, priority).
        max_concurrency: Maximum number of operations to run concurrently.

    Returns:
        List of results from the operations in original order, with exceptions
        for failed operations.
    """

    sorted_ops = sorted(operations, key=lambda x: x[1], reverse=True)
    priority_queue = asyncio.PriorityQueue()
    for i, (op, priority) in enumerate(sorted_ops):
        await priority_queue.put((-priority, i, op))
    semaphore = asyncio.Semaphore(max_concurrency)
    results = [None] * len(operations)
    result_index = 0

    async def process_from_queue():
        nonlocal result_index
        while not priority_queue.empty():
            _, original_index, operation = await priority_queue.get()
            async with semaphore:
                try:
                    results[original_index] = await operation()
                except Exception as e:
                    results[original_index] = e  # type: ignore[assignment]
            result_index += 1

    await process_from_queue()
    return results
