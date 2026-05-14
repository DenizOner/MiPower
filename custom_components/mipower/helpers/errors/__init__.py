"""
Error Handler Package.

This package provides centralized error handling functionality
for the Smartify integration, following SOLID principles.
"""

from .context import ErrorContext
from .exceptions import (
    ConfigurationError,
    ErrorCategory,
    ErrorSeverity,
    NetworkError,
    SmartifyError,
    ValidationError,
)
from .handler import ErrorHandler
from .handler_interface import ErrorHandlerInterface

__all__ = [
    "ErrorHandler",
    "ErrorHandlerInterface",
    "ErrorContext",
    "SmartifyError",
    "ConfigurationError",
    "ValidationError",
    "NetworkError",
    "ErrorSeverity",
    "ErrorCategory",
]
