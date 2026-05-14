"""
Operation Executor for Batch Operations - Single Responsibility Principle

This module implements operation execution functionality following SOLID principles,
handling individual operation execution with retry logic and concurrency control.
"""

import asyncio
import logging
from datetime import datetime

from ..logger.batch_logger import execution_logging
from .batch import BatchProcessor
from .batch_interface import (
    BatchOperation,
    BatchStatus,
    OperationExecutorInterface,
)

_LOGGER = logging.getLogger(__name__)


class OperationExecutor(OperationExecutorInterface):
    """Handles execution of individual batch operations.

    This class is responsible for executing single operations with retry logic,
    timeout handling, and proper error management. Follows Single Responsibility
    Principle by focusing only on operation execution.
    """

    def __init__(self, batch_processor: "BatchProcessor"):
        """Initialize the operation executor.

        Args:
            batch_processor: Reference to the parent batch processor for result tracking.
        """
        self.batch_processor = batch_processor
        self._semaphore = batch_processor._semaphore
        self._default_timeout = batch_processor.default_timeout

    @execution_logging()
    async def execute_operation(self, batch_id: str, operation: BatchOperation) -> None:
        """Execute a single operation with retry logic and error handling.

        Implements exponential backoff retry strategy and proper resource management.
        Updates operation and batch result status throughout execution.

        Args:
            batch_id: The batch this operation belongs to.
            operation: The operation to execute.
        """
        operation.start_time = operation.start_time or datetime.now()
        last_exception = None

        # Execute with retry logic
        while operation.retry_count <= operation.max_retries:
            try:
                _LOGGER.debug(
                    "Executing operation: %s (attempt %d/%d)",
                    operation.operation_id,
                    operation.retry_count + 1,
                    operation.max_retries + 1,
                )

                # Execute operation with concurrency control and timeout
                async with self._semaphore:
                    operation.result = await asyncio.wait_for(
                        operation.operation_func(*operation.args, **operation.kwargs),
                        timeout=self._default_timeout,
                    )

                # Mark operation as completed
                operation.status = BatchStatus.COMPLETED
                operation.end_time = datetime.now()

                # Update batch results
                batch_result = self.batch_processor._batch_results[batch_id]
                batch_result.completed_operations += 1
                batch_result.results[operation.operation_id] = operation.result

                _LOGGER.debug(
                    "Operation %s completed successfully in %.3fs",
                    operation.operation_id,
                    operation.get_duration() or 0,
                )
                return

            except asyncio.TimeoutError as e:
                last_exception = e
                _LOGGER.warning(
                    "Operation %s timed out (attempt %d/%d)",
                    operation.operation_id,
                    operation.retry_count + 1,
                    operation.max_retries + 1,
                )

            except Exception as e:
                last_exception = e
                _LOGGER.warning(
                    "Operation %s failed (attempt %d/%d): %s",
                    operation.operation_id,
                    operation.retry_count + 1,
                    operation.max_retries + 1,
                    e,
                )

            # Increment retry count and check if we should retry
            operation.retry_count += 1

            if operation.retry_count <= operation.max_retries:
                # Exponential backoff delay
                delay = operation.retry_delay * (2 ** (operation.retry_count - 1))
                _LOGGER.debug(
                    "Retrying operation %s in %.2fs",
                    operation.operation_id,
                    delay,
                )
                await asyncio.sleep(delay)
            else:
                # Max retries exceeded, mark as failed
                _LOGGER.error(
                    "Operation %s failed after %d attempts: %s",
                    operation.operation_id,
                    operation.max_retries + 1,
                    last_exception,
                    exc_info=True,
                )

                operation.status = BatchStatus.FAILED
                operation.error = last_exception
                operation.end_time = datetime.now()

                # Update batch results
                batch_result = self.batch_processor._batch_results[batch_id]
                batch_result.failed_operations += 1
                batch_result.errors[operation.operation_id] = last_exception
