"""
Script Executor Interface - Dependency Inversion for Script Execution

This module defines the abstraction layer for script execution in Smartify,
allowing DIP by decoupling execution logic from the coordinator. It provides
a standardized interface for executing Home Assistant scripts with timeout
handling and resource cleanup capabilities.
"""

from abc import ABC, abstractmethod
from typing import Optional

from .types import ExecutionResult


class ScriptExecutorInterface(ABC):
    """Interface for script execution functionality.

    This abstract base class defines the contract for script execution components
    in Smartify, providing a consistent API for executing Home Assistant scripts
    with timeout handling, capability detection, and resource management.
    """

    @abstractmethod
    async def execute_script(
        self, script_entity_id: str, timeout: Optional[float] = None
    ) -> ExecutionResult:
        """Execute a script by entity ID.

        Executes the specified Home Assistant script with optional timeout handling.
        Implementation should handle script execution asynchronously and return
        detailed execution results.

        Args:
            script_entity_id (str): The entity ID of the script to execute.
            timeout (Optional[float]): Maximum execution time in seconds. If None,
                uses default timeout behavior.

        Returns:
            ExecutionResult: Detailed result of the script execution including
                success status, execution time, and any error information.
        """

    @abstractmethod
    def get_supported_scripts(self) -> list[str]:
        """Get list of supported script entity IDs.

        Returns a list of script entity IDs that this executor can handle.
        Used for validation and capability checking.

        Returns:
            list[str]: List of supported script entity IDs that can be executed
                by this implementation.
        """

    @abstractmethod
    async def cleanup(self) -> None:
        """Clean up resources.

        Performs any necessary cleanup operations such as closing connections,
        canceling pending tasks, or releasing resources. Should be called
        when the executor is no longer needed.
        """
