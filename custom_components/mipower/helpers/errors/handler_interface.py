"""Error handler interface for Smartify integration.

Defines the contract for error handling following SOLID principles.
"""

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional

from .context import ErrorContext


class ErrorHandlerInterface(ABC):
    """Abstract interface for error handling."""

    @abstractmethod
    def handle_error(
        self,
        error: Exception,
        context: Optional[Dict[str, Any]] = None,
        raise_error: bool = True,
    ) -> Any:
        """Handle an error with context.

        Args:
            error: The exception to handle
            context: Additional context
            raise_error: Whether to raise the error after handling

        Returns:
            Recovery result if recovery was successful, None otherwise
        """
        pass

    @abstractmethod
    async def handle_async_error(
        self,
        error: Exception,
        context: Optional[Dict[str, Any]] = None,
        raise_error: bool = True,
    ) -> Any:
        """Handle an async error with context.

        Args:
            error: The exception to handle
            context: Additional context
            raise_error: Whether to raise the error after handling

        Returns:
            Recovery result if recovery was successful, None otherwise
        """
        pass

    @abstractmethod
    async def handle_operation(
        self,
        operation_name: str,
        operation_func: Callable,
        context: Optional[ErrorContext] = None,
        **kwargs,
    ) -> Any:
        """Handle an operation with automatic error handling and recovery.

        Args:
            operation_name: Name of the operation
            operation_func: The operation function to execute
            context: Error context information
            **kwargs: Arguments to pass to the operation function

        Returns:
            Result of the operation if successful
        """
        pass

    @abstractmethod
    def register_recovery_strategy(
        self, error_type: type, recovery_func: Callable[[Exception], Any]
    ) -> None:
        """Register a recovery strategy for a specific error type.

        Args:
            error_type: The type of error to recover from
            recovery_func: Function to call for recovery
        """
        pass

    @abstractmethod
    def add_error_listener(self, listener: Callable[[Exception], Any]) -> None:
        """Add an error listener.

        Args:
            listener: Function to call when errors occur
        """
        pass

    @abstractmethod
    def remove_error_listener(self, listener: Callable[[Exception], Any]) -> None:
        """Remove an error listener.

        Args:
            listener: The listener to remove
        """
        pass

    @abstractmethod
    def get_error_statistics(self) -> Dict[str, Any]:
        """Get error statistics.

        Returns:
            Dictionary containing error statistics
        """
        pass

    @abstractmethod
    def reset_error_counts(self) -> None:
        """Reset error counts."""
        pass

    @abstractmethod
    def get_error_log(self) -> List[Dict[str, Any]]:
        """Get the list of handled errors.

        Returns:
            List of error information
        """
        pass

    @abstractmethod
    def clear_error_log(self) -> None:
        """Clear the error log."""
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """Clean up resources."""
        pass
