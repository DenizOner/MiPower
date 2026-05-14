"""Error handler implementation for Smartify integration.

Provides comprehensive error handling with recovery strategies, listeners, and categorization.
"""

import asyncio
import logging
from typing import Any, Callable, Dict, List, Optional

from .context import ErrorContext
from .exceptions import (
    BatchOperationError,
    ConfigurationError,
    DataOperationError,
    DependencyInjectionError,
    EntityRegistryError,
    ErrorCategory,
    ErrorSeverity,
    HardwareError,
    LockManagementError,
    NetworkError,
    PluginError,
    PowerSensorError,
    ScriptExecutionError,
    SmartifyError,
    ValidationError,
)
from .handler_interface import ErrorHandlerInterface

_LOGGER = logging.getLogger(__name__)


class ErrorHandler(ErrorHandlerInterface):
    """Advanced error handler with recovery strategies and categorization."""

    def __init__(self, hass=None):
        """Initialize the error handler.

        Args:
            hass: Home Assistant instance (optional, for dependency injection)
        """
        self.hass = hass
        self._error_counts: Dict[str, int] = {}
        self._recovery_strategies: Dict[type, Callable[[Exception], Any]] = {}
        self._error_listeners: List[Callable[[Exception], Any]] = []
        self._error_log: List[Dict[str, Any]] = []

    def handle_error(
        self,
        error: Exception,
        context: Optional[Dict[str, Any]] = None,
        raise_error: bool = True,
    ) -> Any:
        """Handle an error with context and optional recovery.

        Args:
            error: The exception to handle
            context: Additional context info
            raise_error: Whether to raise the error after handling

        Returns:
            Recovery result if recovery was successful, None otherwise
        """
        classified_error = self._classify_error(error)

        # Update error counts
        error_key = (
            f"{classified_error.category.value}_{classified_error.severity.value}"
        )
        self._error_counts[error_key] = self._error_counts.get(error_key, 0) + 1

        # Log the error
        self._log_error(classified_error)

        # Try recovery
        recovery_result = self._try_recovery(classified_error)

        # Notify listeners
        self._notify_listeners(classified_error)

        # Log the error
        self._log_error_to_storage(classified_error, context)

        if recovery_result is not None:
            return recovery_result

        if raise_error:
            raise classified_error

        return None

    async def handle_async_error(
        self,
        error: Exception,
        context: Optional[Dict[str, Any]] = None,
        raise_error: bool = True,
    ) -> Any:
        """Handle an async error with context and optional recovery.

        Args:
            error: The exception to handle
            context: Additional context info
            raise_error: Whether to raise the error after handling

        Returns:
            Recovery result if recovery was successful, None otherwise
        """
        classified_error = self._classify_error(error)

        # Update error counts
        error_key = (
            f"{classified_error.category.value}_{classified_error.severity.value}"
        )
        self._error_counts[error_key] = self._error_counts.get(error_key, 0) + 1

        # Log the error
        self._log_error(classified_error)

        # Try async recovery
        recovery_result = await self._try_async_recovery(classified_error)

        # Notify listeners asynchronously
        await self._notify_listeners_async(classified_error)

        # Log the error
        self._log_error_to_storage(classified_error, context)

        if recovery_result is not None:
            return recovery_result

        if raise_error:
            raise classified_error

        return None

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
        try:
            if asyncio.iscoroutinefunction(operation_func):
                return await operation_func(**kwargs)
            else:
                return operation_func(**kwargs)
        except Exception as e:
            # Create enhanced context if not provided
            if context is None:
                context = ErrorContext(
                    component="unknown",
                    operation=operation_name,
                    additional_data=kwargs,
                )

            # Try to handle and recover
            recovery_result = await self.handle_async_error(e, raise_error=False)

            if recovery_result is not None:
                _LOGGER.info("Recovered from error in operation: %s", operation_name)
                return recovery_result

            # If no recovery, re-raise with context
            raise SmartifyError(
                f"Operation '{operation_name}' failed: {e}",
                context={
                    "original_error": str(e),
                    "operation_context": context.to_dict(),
                },
            ) from e

    def register_recovery_strategy(
        self, error_type: type, recovery_func: Callable[[Exception], Any]
    ) -> None:
        """Register a recovery strategy for a specific error type.

        Args:
            error_type: The type of error to recover from
            recovery_func: Function to call for recovery
        """
        self._recovery_strategies[error_type] = recovery_func
        _LOGGER.debug("Registered recovery strategy for: %s", error_type.__name__)

    def add_error_listener(self, listener: Callable[[Exception], Any]) -> None:
        """Add an error listener.

        Args:
            listener: Function to call when errors occur
        """
        if listener not in self._error_listeners:
            self._error_listeners.append(listener)
            _LOGGER.debug("Added error listener")

    def remove_error_listener(self, listener: Callable[[Exception], Any]) -> None:
        """Remove an error listener.

        Args:
            listener: The listener to remove
        """
        if listener in self._error_listeners:
            self._error_listeners.remove(listener)
            _LOGGER.debug("Removed error listener")

    def get_error_statistics(self) -> Dict[str, Any]:
        """Get error statistics.

        Returns:
            Dictionary containing error statistics
        """
        return {
            "total_errors": sum(self._error_counts.values()),
            "recovery_strategies": len(self._recovery_strategies),
            "error_counts": self._error_counts.copy(),
            "active_listeners": len(self._error_listeners),
        }

    def reset_error_counts(self) -> None:
        """Reset error counts."""
        self._error_counts.clear()
        _LOGGER.debug("Reset error counts")

    def get_error_log(self) -> List[Dict[str, Any]]:
        """Get the list of handled errors.

        Returns:
            List of error information
        """
        return self._error_log.copy()

    def clear_error_log(self) -> None:
        """Clear the error log."""
        self._error_log.clear()
        _LOGGER.debug("Cleared error log")

    async def cleanup(self) -> None:
        """Clean up resources."""
        self._error_listeners.clear()
        self._recovery_strategies.clear()
        self._error_counts.clear()
        self._error_log.clear()
        _LOGGER.debug("Error handler cleanup completed")

    def _classify_error(self, error: Exception) -> SmartifyError:
        """Classify an error into appropriate Smartify error type.

        Args:
            error: The original exception

        Returns:
            Classified Smartify error
        """
        error_msg = str(error)

        # Check for specific error types first
        if isinstance(error, SmartifyError):
            return error

        # Classify by error type and message content
        if "timeout" in error_msg.lower():
            return SmartifyError(
                error_msg,
                category=ErrorCategory.TIMEOUT,
                severity=ErrorSeverity.MEDIUM,
            )
        elif isinstance(error, ValueError):
            # Classify ValueError based on context
            if "batch" in error_msg.lower():
                return BatchOperationError(error_msg)
            elif "lock" in error_msg.lower():
                return LockManagementError(error_msg)
            elif (
                "data" in error_msg.lower()
                or "import" in error_msg.lower()
                or "export" in error_msg.lower()
            ):
                return DataOperationError(error_msg)
            elif "script" in error_msg.lower():
                return ScriptExecutionError(error_msg)
            elif "entity" in error_msg.lower() or "registry" in error_msg.lower():
                return EntityRegistryError(error_msg)
            elif "plugin" in error_msg.lower():
                return PluginError(error_msg)
            elif "dependency" in error_msg.lower() or "injection" in error_msg.lower():
                return DependencyInjectionError(error_msg)
            else:
                return ValidationError(error_msg)
        elif isinstance(error, RuntimeError):
            # Classify RuntimeError based on context
            if "power" in error_msg.lower() or "sensor" in error_msg.lower():
                return PowerSensorError(error_msg)
            elif "hardware" in error_msg.lower():
                return HardwareError(error_msg)
            elif "batch" in error_msg.lower():
                return BatchOperationError(error_msg)
            elif "lock" in error_msg.lower():
                return LockManagementError(error_msg)
            elif "entity" in error_msg.lower():
                return EntityRegistryError(error_msg)
            else:
                return SmartifyError(error_msg, category=ErrorCategory.SOFTWARE)
        elif isinstance(error, ConnectionError):
            return NetworkError(error_msg)
        elif isinstance(error, KeyError):
            return ConfigurationError(error_msg)
        elif isinstance(error, ImportError):
            return DependencyInjectionError(error_msg)
        elif "config" in error_msg.lower():
            return ConfigurationError(error_msg)

        # Default classification
        return SmartifyError(error_msg)

    def _try_recovery(self, error: SmartifyError) -> Any:
        """Try to recover from an error using registered strategies.

        Args:
            error: The classified error

        Returns:
            Recovery result or None
        """
        for error_type, recovery_func in self._recovery_strategies.items():
            if isinstance(error, error_type):
                try:
                    result = recovery_func(error)
                    _LOGGER.info("Successfully recovered from %s", error_type.__name__)
                    return result
                except Exception as recovery_error:
                    _LOGGER.error(
                        "Recovery failed for %s: %s",
                        error_type.__name__,
                        recovery_error,
                        exc_info=True,
                    )
                    break

        return None

    async def _try_async_recovery(self, error: SmartifyError) -> Any:
        """Try to recover from an error using async registered strategies.

        Args:
            error: The classified error

        Returns:
            Recovery result or None
        """
        for error_type, recovery_func in self._recovery_strategies.items():
            if isinstance(error, error_type):
                try:
                    if asyncio.iscoroutinefunction(recovery_func):
                        result = await recovery_func(error)
                    else:
                        result = recovery_func(error)
                    _LOGGER.info("Successfully recovered from %s", error_type.__name__)
                    return result
                except Exception as recovery_error:
                    _LOGGER.error(
                        "Recovery failed for %s: %s",
                        error_type.__name__,
                        recovery_error,
                        exc_info=True,
                    )
                    break

        return None

    def _notify_listeners(self, error: SmartifyError) -> None:
        """Notify error listeners.

        Args:
            error: The error to notify about
        """
        for listener in self._error_listeners:
            try:
                listener(error)
            except Exception as listener_error:
                _LOGGER.error(
                    "Error listener failed: %s",
                    listener_error,
                    exc_info=True,
                )

    async def _notify_listeners_async(self, error: SmartifyError) -> None:
        """Notify error listeners asynchronously.

        Args:
            error: The error to notify about
        """
        for listener in self._error_listeners:
            try:
                if asyncio.iscoroutinefunction(listener):
                    await listener(error)
                else:
                    listener(error)
            except Exception as listener_error:
                _LOGGER.error(
                    "Async error listener failed: %s",
                    listener_error,
                    exc_info=True,
                )

    def _log_error(self, error: SmartifyError) -> None:
        """Log an error based on its severity.

        Args:
            error: The error to log
        """
        log_message = f"Smartify error: {error.message}"
        if error.severity == ErrorSeverity.CRITICAL:
            _LOGGER.critical(
                log_message,
                exc_info=True,
            )
        elif error.severity == ErrorSeverity.HIGH:
            _LOGGER.error(
                log_message,
                exc_info=True,
            )
        elif error.severity == ErrorSeverity.MEDIUM:
            _LOGGER.warning(log_message)
        else:
            _LOGGER.info(log_message)

    def _log_error_to_storage(
        self, error: SmartifyError, context: Optional[Dict[str, Any]]
    ) -> None:
        """Log error to internal storage.

        Args:
            error: The error to log
            context: Additional context
        """
        error_entry = {
            "timestamp": self._get_timestamp(),
            "message": error.message,
            "severity": error.severity.value,
            "category": error.category.value,
            "recoverable": error.recoverable,
            "context": context or {},
            "error_type": error.__class__.__name__,
        }
        self._error_log.append(error_entry)

    def _get_timestamp(self) -> str:
        """Get current timestamp.

        Returns:
            Current timestamp string
        """
        from datetime import datetime

        return datetime.now().isoformat()
