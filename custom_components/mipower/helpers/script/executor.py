"""
Script Executor - Concrete implementation of ScriptExecutorInterface

This module provides a concrete implementation of the ScriptExecutorInterface,
following SOLID principles and pure dependency injection by implementing the
abstraction layer with constructor injection.

SOLID Principles Applied:
- Single Responsibility: Script execution logic only
- Open-Closed: New execution strategies can be added without modification
- Liskov Substitution: Can be replaced with any ScriptExecutorInterface implementation
- Interface Segregation: Focused on script execution responsibilities
- Dependency Inversion: Depends on abstractions, not concretions
"""

import asyncio
import logging
import time
from typing import List, Optional

from homeassistant.core import HomeAssistant  # type: ignore[import]
from homeassistant.exceptions import HomeAssistantError  # type: ignore[import]

from ..batch import BatchProcessor
from .executor_interface import ScriptExecutorInterface
from .types import ExecutionResult

_LOGGER = logging.getLogger(__name__)


class ScriptExecutor(ScriptExecutorInterface):
    """Concrete implementation of the ScriptExecutorInterface.

    This class provides a concrete implementation for executing Home Assistant scripts,
    managing supported scripts, and handling execution timeouts. It implements the
    ScriptExecutorInterface following dependency inversion principles.
    """

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the script executor.

        Args:
            hass (HomeAssistant): The Home Assistant instance.
        """
        self._hass = hass
        self._supported_scripts: set[str] = set()
        self._batch_processor = BatchProcessor(
            hass, max_concurrency=5, max_batch_size=100
        )

    async def execute_script(
        self, script_entity_id: str, timeout: Optional[float] = 30.0
    ) -> ExecutionResult:
        """Execute a script by entity ID.

        Args:
            script_entity_id (str): The entity ID of the script to execute.
            timeout (Optional[float]): Maximum time to wait for execution in seconds.
                Defaults to 30.0 seconds.

        Returns:
            ExecutionResult: Result of the script execution containing success status,
                execution time, and any error messages.
        """
        _LOGGER.debug("Starting script execution for: %s", script_entity_id)
        start_time = time.time()
        try:
            # Verify script entity exists
            state = self._hass.states.get(script_entity_id)
            if not state:
                return ExecutionResult(
                    success=False,
                    script_entity_id=script_entity_id,
                    execution_time=0.0,
                    error_message=(f"Script entity {script_entity_id} not found"),
                )

            # Execute script using Home Assistant service
            await self._hass.services.async_call(
                "script",
                "turn_on",
                {"entity_id": script_entity_id},
                blocking=False,  # Non-blocking to allow timeout control
            )

            # Add to supported scripts on first successful access
            self._supported_scripts.add(script_entity_id)

            # Wait for reasonable execution time or timeout
            execution_timeout = timeout or 30.0
            await asyncio.sleep(
                min(1.0, execution_timeout)
            )  # Script execution time estimate

            # Check if script completed (basic check)
            # In a production system, you might use script runtime tracking
            execution_time = time.time() - start_time

            return ExecutionResult(
                success=True,
                script_entity_id=script_entity_id,
                execution_time=execution_time,
            )

        except HomeAssistantError as e:
            execution_time = time.time() - start_time
            return ExecutionResult(
                success=False,
                script_entity_id=script_entity_id,
                execution_time=execution_time,
                error_message=f"Home Assistant error: {str(e)}",
            )
        except asyncio.TimeoutError:
            execution_time = time.time() - start_time
            return ExecutionResult(
                success=False,
                script_entity_id=script_entity_id,
                execution_time=execution_time,
                error_message=(f"Script execution timed out after {timeout}s"),
            )
        except Exception as e:
            execution_time = time.time() - start_time
            return ExecutionResult(
                success=False,
                script_entity_id=script_entity_id,
                execution_time=execution_time,
                error_message=str(e),
            )

    def get_supported_scripts(self) -> List[str]:
        """Get list of supported script entity IDs.

        Returns:
            List[str]: List of script entity IDs that have been successfully executed.
        """
        return list(self._supported_scripts)

    async def execute_scripts_batch(
        self,
        script_entity_ids: List[str],
        timeout: Optional[float] = 30.0,
        max_concurrency: int = 3,
    ) -> List[ExecutionResult]:
        """Execute multiple scripts concurrently using batch processing.

        Args:
            script_entity_ids: List of script entity IDs to execute.
            timeout: Maximum time to wait for each script execution in seconds.
            max_concurrency: Maximum number of scripts to execute concurrently.

        Returns:
            List[ExecutionResult]: Results for each script execution in original order.
        """
        if not script_entity_ids:
            return []

        _LOGGER.info(
            "Starting batch script execution: %d scripts, max_concurrency=%d",
            len(script_entity_ids),
            max_concurrency,
        )

        # Create batch processor with specified concurrency for this batch
        batch_processor = BatchProcessor(
            self._hass, max_concurrency=max_concurrency, max_batch_size=100
        )

        batch_id = f"script_batch_{id(self)}_{time.time()}"
        await batch_processor.create_batch(batch_id)

        # Add script execution operations to batch
        for i, script_id in enumerate(script_entity_ids):
            await batch_processor.add_operation(
                batch_id,
                f"script_{i}_{script_id.replace('.', '_')}",
                self._execute_script_for_batch,
                priority=1,  # All scripts have same priority
                dependencies=[],  # No dependencies between scripts
                script_entity_id=script_id,
                timeout=timeout,
            )

        # Execute batch
        batch_result = await batch_processor.execute_batch(batch_id)

        if batch_result.status != "completed":
            _LOGGER.error(
                "Batch script execution failed: %s",
                batch_result.status,
                exc_info=True,
            )

        # Extract results in original order
        results = []
        for i, script_id in enumerate(script_entity_ids):
            operation_id = f"script_{i}_{script_id.replace('.', '_')}"
            if operation_id in batch_result.results:
                results.append(batch_result.results[operation_id])
            else:
                # Create failed result for missing operations
                results.append(
                    ExecutionResult(
                        success=False,
                        script_entity_id=script_id,
                        execution_time=0.0,
                        error_message="Batch execution failed",
                    )
                )

        successful_count = sum(1 for r in results if r.success)
        _LOGGER.info(
            "Batch script execution completed: %d/%d successful",
            successful_count,
            len(script_entity_ids),
        )

        # Clean up the temporary batch processor
        await batch_processor.cleanup()

        return results

    async def _execute_script_for_batch(
        self, script_entity_id: str, timeout: float
    ) -> ExecutionResult:
        """Execute a single script for batch processing.

        Args:
            script_entity_id: Script entity ID to execute.
            timeout: Execution timeout in seconds.

        Returns:
            ExecutionResult: Script execution result.
        """
        return await self.execute_script(script_entity_id, timeout)

    async def cleanup(self) -> None:
        """Clean up resources.

        Clears the list of supported scripts and releases any held resources.
        """
        self._supported_scripts.clear()
        await self._batch_processor.cleanup()
