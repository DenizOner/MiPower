"""Calibration logging decorator for detailed error tracking.

This module provides decorators for comprehensive logging in calibration operations,
following SOLID principles with separation of concerns.
"""

import asyncio
import functools
import logging
import time
from typing import Any, Callable, Dict, Optional, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


class CalibrationLogger:
    """Logger for calibration operations with detailed tracking."""

    def __init__(self, logger: logging.Logger):
        """Initialize the calibration logger.

        Args:
            logger: Logger instance to use for logging
        """
        self.logger = logger

    def log_function_call(
        self,
        func_name: str,
        args: tuple,
        kwargs: dict,
        start_time: float,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log function call details.

        Args:
            func_name: Name of the function being called
            args: Positional arguments
            kwargs: Keyword arguments
            start_time: Call start time
            context: Additional context information
        """
        try:
            # Sanitize args and kwargs for logging
            safe_args = self._sanitize_args(args)
            safe_kwargs = self._sanitize_kwargs(kwargs)

            context_str = f" [Context: {context}]" if context else ""
            self.logger.debug(
                f"Calling {func_name} with args={safe_args}, kwargs={safe_kwargs}{context_str}"
            )
        except Exception as e:
            self.logger.warning(f"Error logging function call details: {e}")

    def log_function_success(
        self,
        func_name: str,
        result: Any,
        duration: float,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log successful function completion.

        Args:
            func_name: Name of the completed function
            result: Function result
            duration: Execution duration
            context: Additional context information
        """
        try:
            result_type = type(result).__name__
            context_str = f" [Context: {context}]" if context else ""
            self.logger.info(
                f"{func_name} completed successfully in {duration:.3f}s, "
                f"returned {result_type}{context_str}"
            )
        except Exception as e:
            self.logger.warning(f"Error logging function success: {e}")

    def log_function_error(
        self,
        func_name: str,
        error: Exception,
        duration: float,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log function error with full details.

        Args:
            func_name: Name of the failed function
            error: The exception that occurred
            duration: Execution duration before failure
            context: Additional context information
        """
        try:
            context_str = f" [Context: {context}]" if context else ""
            self.logger.error(
                f"{func_name} failed after {duration:.3f}s with {type(error).__name__}: "
                f"{error}{context_str}",
                exc_info=True,
            )
        except Exception as e:
            self.logger.critical(f"Error logging function failure: {e}", exc_info=True)

    def log_function_finally(
        self,
        func_name: str,
        total_duration: float,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log function cleanup/finalization.

        Args:
            func_name: Name of the function
            total_duration: Total execution duration
            context: Additional context information
        """
        try:
            context_str = f" [Context: {context}]" if context else ""
            self.logger.debug(
                f"{func_name} cleanup completed in {total_duration:.3f}s{context_str}"
            )
        except Exception as e:
            self.logger.warning(f"Error logging function cleanup: {e}")

    def _sanitize_args(self, args: tuple) -> tuple:
        """Sanitize positional arguments for safe logging.

        Args:
            args: Original arguments

        Returns:
            Sanitized arguments
        """
        sanitized = []
        for arg in args:
            if self._is_sensitive_arg(arg):
                sanitized.append("***MASKED***")
            elif isinstance(arg, (str, int, float, bool, type(None))):
                sanitized.append(arg)
            else:
                sanitized.append(f"<{type(arg).__name__}>")
        return tuple(sanitized)

    def _sanitize_kwargs(self, kwargs: dict) -> dict:
        """Sanitize keyword arguments for safe logging.

        Args:
            kwargs: Original keyword arguments

        Returns:
            Sanitized keyword arguments
        """
        sanitized = {}
        for key, value in kwargs.items():
            if self._is_sensitive_key(key):
                sanitized[key] = "***MASKED***"
            elif isinstance(value, (str, int, float, bool, type(None))):
                sanitized[key] = value
            elif isinstance(value, dict):
                sanitized[key] = self._sanitize_kwargs(value)
            else:
                sanitized[key] = f"<{type(value).__name__}>"
        return sanitized

    def _is_sensitive_arg(self, arg: Any) -> bool:
        """Check if an argument contains sensitive information.

        Args:
            arg: Argument to check

        Returns:
            True if sensitive
        """
        if isinstance(arg, str):
            sensitive_keywords = ["password", "token", "secret", "key", "auth"]
            return any(keyword in arg.lower() for keyword in sensitive_keywords)
        return False

    def _is_sensitive_key(self, key: str) -> bool:
        """Check if a key indicates sensitive information.

        Args:
            key: Key to check

        Returns:
            True if sensitive
        """
        sensitive_keywords = [
            "password",
            "token",
            "secret",
            "key",
            "auth",
            "credential",
        ]
        return any(keyword in key.lower() for keyword in sensitive_keywords)


def calibration_logging(
    context_provider: Optional[Callable[[], Dict[str, Any]]] = None,
    logger_name: str = "calibration",
    container=None,
) -> Callable[[F], F]:
    """Decorator for comprehensive calibration function logging.

    This decorator wraps async functions with try-catch-finally blocks,
    logging all function calls, successes, failures, and cleanup operations.

    Args:
        context_provider: Optional callable that provides context information
        logger_name: Name for the logger instance
        container: Optional DI container for dependency injection

    Returns:
        Decorated function

    Example:
        @calibration_logging()
        async def my_function(self, arg1, arg2=None):
            return "result"
    """

    def decorator(func: F) -> F:
        # DIP: Resolve logger from container instead of direct instantiation
        if container:
            logger_factory = container._instances.get("logger_factory")
            if logger_factory:
                resolved_logger = logger_factory.get_logger(logger_name)
                logger = CalibrationLogger(resolved_logger)
            else:
                # Fallback to standard logging if factory not available
                resolved_logger = logging.getLogger(f"smartify.{logger_name}")
                logger = CalibrationLogger(resolved_logger)
        else:
            # Fallback for backward compatibility
            resolved_logger = logging.getLogger(f"smartify.{logger_name}")
            logger = CalibrationLogger(resolved_logger)

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            func_name = f"{func.__module__}.{func.__qualname__}"
            start_time = time.time()
            context = context_provider() if context_provider else None

            try:
                # Log function call
                logger.log_function_call(func_name, args, kwargs, start_time, context)

                # Execute function
                result = await func(*args, **kwargs)

                # Calculate duration
                call_duration = time.time() - start_time

                # Log success
                logger.log_function_success(func_name, result, call_duration, context)

                return result

            except Exception as e:
                # Calculate duration
                error_duration = time.time() - start_time

                # Log error
                logger.log_function_error(func_name, e, error_duration, context)

                # Re-raise to maintain original behavior
                raise

            finally:
                # Calculate total duration
                total_duration = time.time() - start_time

                # Log cleanup
                logger.log_function_finally(func_name, total_duration, context)

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            func_name = f"{func.__module__}.{func.__qualname__}"
            start_time = time.time()
            context = context_provider() if context_provider else None

            try:
                # Log function call
                logger.log_function_call(func_name, args, kwargs, start_time, context)

                # Execute function
                result = func(*args, **kwargs)

                # Calculate duration
                call_duration = time.time() - start_time

                # Log success
                logger.log_function_success(func_name, result, call_duration, context)

                return result

            except Exception as e:
                # Calculate duration
                error_duration = time.time() - start_time

                # Log error
                logger.log_function_error(func_name, e, error_duration, context)

                # Re-raise to maintain original behavior
                raise

            finally:
                # Calculate total duration
                total_duration = time.time() - start_time

                # Log cleanup
                logger.log_function_finally(func_name, total_duration, context)

        # Return appropriate wrapper based on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper  # type: ignore
        else:
            return sync_wrapper  # type: ignore

    return decorator


# Convenience decorators for specific use cases
def calibration_step_logging(step_name: str) -> Callable[[F], F]:
    """Decorator for calibration step functions.

    Args:
        step_name: Name of the calibration step

    Returns:
        Decorated function
    """

    def context_provider():
        return {"step": step_name, "operation": "calibration_step"}

    return calibration_logging(
        context_provider=context_provider, logger_name="calibration.steps"
    )


def facade_method_logging(facade_name: str) -> Callable[[F], F]:
    """Decorator for facade methods.

    Args:
        facade_name: Name of the facade

    Returns:
        Decorated function
    """

    def context_provider():
        return {"facade": facade_name, "operation": "facade_method"}

    return calibration_logging(
        context_provider=context_provider, logger_name=f"calibration.{facade_name}"
    )


def handler_method_logging(handler_name: str) -> Callable[[F], F]:
    """Decorator for handler methods.

    Args:
        handler_name: Name of the handler

    Returns:
        Decorated function
    """

    def context_provider():
        return {"handler": handler_name, "operation": "handler_method"}

    return calibration_logging(
        context_provider=context_provider, logger_name=f"calibration.{handler_name}"
    )
