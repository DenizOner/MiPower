"""Custom exception classes for Smartify integration.

This module defines a comprehensive exception hierarchy for Smartify integration,
providing structured error handling with categorization, severity levels, and
contextual information.

Exception Hierarchy:
    SmartifyError (base)
    ├── ConfigurationError
    ├── ValidationError
    ├── NetworkError
    ├── CalibrationError
    ├── PowerSensorError
    ├── HardwareError
    ├── BatchOperationError
    ├── LockManagementError
    ├── DataOperationError
    ├── ScriptExecutionError
    ├── EntityRegistryError
    ├── PluginError
    └── DependencyInjectionError

Usage Examples:

    # Raise a calibration error with specific code
    raise CalibrationError(
        "Power sensor unavailable",
        "power_sensor_unavailable"
    )

    # Raise a validation error
    raise ValidationError("Invalid threshold value")

    # Raise an error with context
    raise HardwareError(
        "Sensor communication failed",
        context={"sensor_id": "sensor.power", "device": "device.tv"}
    )
"""

from enum import Enum
from typing import Any, Dict, Optional


class ErrorSeverity(Enum):
    """Error severity levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Error category classifications."""

    SOFTWARE = "software"
    CONFIGURATION = "configuration"
    VALIDATION = "validation"
    NETWORK = "network"
    TIMEOUT = "timeout"
    HARDWARE = "hardware"
    CALIBRATION = "calibration"
    SCRIPT = "script"
    BATCH = "batch"
    LOCK = "lock"
    DATA = "data"
    USER = "user"


class SmartifyError(Exception):
    """Base exception class for Smartify integration errors.

    Provides structured error information with severity, category, and context.
    """

    def __init__(
        self,
        message: str,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        category: ErrorCategory = ErrorCategory.SOFTWARE,
        recoverable: bool = True,
        context: Optional[Dict[str, Any]] = None,
    ):
        """Initialize Smartify error.

        Args:
            message: Error message
            severity: Error severity level
            category: Error category
            recoverable: Whether the error is recoverable
            context: Additional context information
        """
        super().__init__(message)
        self.message = message
        self.severity = severity
        self.category = category
        self.recoverable = recoverable
        self.context = context or {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary representation.

        Returns:
            Dictionary containing error information
        """
        return {
            "message": self.message,
            "severity": self.severity.value,
            "category": self.category.value,
            "recoverable": self.recoverable,
            "context": self.context,
        }


class ConfigurationError(SmartifyError):
    """Configuration-related errors."""

    def __init__(
        self,
        message: str,
        recoverable: bool = True,
        context: Optional[Dict[str, Any]] = None,
    ):
        """Initialize configuration error.

        Args:
            message: Error message
            recoverable: Whether the error is recoverable
            context: Additional context information
        """
        super().__init__(
            message,
            severity=ErrorSeverity.HIGH,
            category=ErrorCategory.CONFIGURATION,
            recoverable=recoverable,
            context=context,
        )


class ValidationError(SmartifyError):
    """Validation-related errors."""

    def __init__(
        self,
        message: str,
        recoverable: bool = True,
        context: Optional[Dict[str, Any]] = None,
    ):
        """Initialize validation error.

        Args:
            message: Error message
            recoverable: Whether the error is recoverable
            context: Additional context information
        """
        super().__init__(
            message,
            severity=ErrorSeverity.LOW,
            category=ErrorCategory.VALIDATION,
            recoverable=recoverable,
            context=context,
        )


class NetworkError(SmartifyError):
    """Network-related errors."""

    def __init__(
        self,
        message: str,
        recoverable: bool = True,
        context: Optional[Dict[str, Any]] = None,
    ):
        """Initialize network error.

        Args:
            message: Error message
            recoverable: Whether the error is recoverable
            context: Additional context information
        """
        super().__init__(
            message,
            severity=ErrorSeverity.MEDIUM,
            category=ErrorCategory.NETWORK,
            recoverable=recoverable,
            context=context,
        )


# Calibration and Hardware Errors
class CalibrationError(SmartifyError):
    """Calibration-related errors with error codes for UI display."""

    def __init__(
        self,
        message: str,
        error_code: str,
        recoverable: bool = True,
        context: Optional[Dict[str, Any]] = None,
    ):
        """Initialize calibration error.

        Args:
            message: Error message
            error_code: Machine-readable error code for UI display
            recoverable: Whether the error is recoverable
            context: Additional context information
        """
        super().__init__(
            message,
            severity=ErrorSeverity.HIGH,
            category=ErrorCategory.CALIBRATION,
            recoverable=recoverable,
            context=context,
        )
        self.error_code = error_code


class PowerSensorError(SmartifyError):
    """Power sensor and measurement errors."""

    def __init__(
        self,
        message: str,
        recoverable: bool = True,
        context: Optional[Dict[str, Any]] = None,
    ):
        """Initialize power sensor error.

        Args:
            message: Error message
            recoverable: Whether the error is recoverable
            context: Additional context information
        """
        super().__init__(
            message,
            severity=ErrorSeverity.HIGH,
            category=ErrorCategory.HARDWARE,
            recoverable=recoverable,
            context=context,
        )


class HardwareError(SmartifyError):
    """General hardware and sensor errors."""

    def __init__(
        self,
        message: str,
        recoverable: bool = True,
        context: Optional[Dict[str, Any]] = None,
    ):
        """Initialize hardware error.

        Args:
            message: Error message
            recoverable: Whether the error is recoverable
            context: Additional context information
        """
        super().__init__(
            message,
            severity=ErrorSeverity.HIGH,
            category=ErrorCategory.HARDWARE,
            recoverable=recoverable,
            context=context,
        )


# System Operation Errors
class BatchOperationError(SmartifyError):
    """Batch processing errors."""

    def __init__(
        self,
        message: str,
        recoverable: bool = True,
        context: Optional[Dict[str, Any]] = None,
    ):
        """Initialize batch operation error.

        Args:
            message: Error message
            recoverable: Whether the error is recoverable
            context: Additional context information
        """
        super().__init__(
            message,
            severity=ErrorSeverity.MEDIUM,
            category=ErrorCategory.BATCH,
            recoverable=recoverable,
            context=context,
        )


class LockManagementError(SmartifyError):
    """Lock and synchronization errors."""

    def __init__(
        self,
        message: str,
        recoverable: bool = True,
        context: Optional[Dict[str, Any]] = None,
    ):
        """Initialize lock management error.

        Args:
            message: Error message
            recoverable: Whether the error is recoverable
            context: Additional context information
        """
        super().__init__(
            message,
            severity=ErrorSeverity.HIGH,
            category=ErrorCategory.LOCK,
            recoverable=recoverable,
            context=context,
        )


class DataOperationError(SmartifyError):
    """Import/export and data processing errors."""

    def __init__(
        self,
        message: str,
        recoverable: bool = True,
        context: Optional[Dict[str, Any]] = None,
    ):
        """Initialize data operation error.

        Args:
            message: Error message
            recoverable: Whether the error is recoverable
            context: Additional context information
        """
        super().__init__(
            message,
            severity=ErrorSeverity.MEDIUM,
            category=ErrorCategory.DATA,
            recoverable=recoverable,
            context=context,
        )


# Script and Execution Errors
class ScriptExecutionError(SmartifyError):
    """Script execution and control errors."""

    def __init__(
        self,
        message: str,
        recoverable: bool = True,
        context: Optional[Dict[str, Any]] = None,
    ):
        """Initialize script execution error.

        Args:
            message: Error message
            recoverable: Whether the error is recoverable
            context: Additional context information
        """
        super().__init__(
            message,
            severity=ErrorSeverity.MEDIUM,
            category=ErrorCategory.SCRIPT,
            recoverable=recoverable,
            context=context,
        )


# Configuration and System Errors
class EntityRegistryError(SmartifyError):
    """Entity registry access errors."""

    def __init__(
        self,
        message: str,
        recoverable: bool = True,
        context: Optional[Dict[str, Any]] = None,
    ):
        """Initialize entity registry error.

        Args:
            message: Error message
            recoverable: Whether the error is recoverable
            context: Additional context information
        """
        super().__init__(
            message,
            severity=ErrorSeverity.HIGH,
            category=ErrorCategory.CONFIGURATION,
            recoverable=recoverable,
            context=context,
        )


class PluginError(SmartifyError):
    """Plugin system errors."""

    def __init__(
        self,
        message: str,
        recoverable: bool = True,
        context: Optional[Dict[str, Any]] = None,
    ):
        """Initialize plugin error.

        Args:
            message: Error message
            recoverable: Whether the error is recoverable
            context: Additional context information
        """
        super().__init__(
            message,
            severity=ErrorSeverity.HIGH,
            category=ErrorCategory.SOFTWARE,
            recoverable=recoverable,
            context=context,
        )


class DependencyInjectionError(SmartifyError):
    """DI container and service resolution errors."""

    def __init__(
        self,
        message: str,
        recoverable: bool = False,
        context: Optional[Dict[str, Any]] = None,
    ):
        """Initialize dependency injection error.

        Args:
            message: Error message
            recoverable: Whether the error is recoverable (usually False for DI errors)
            context: Additional context information
        """
        super().__init__(
            message,
            severity=ErrorSeverity.CRITICAL,
            category=ErrorCategory.SOFTWARE,
            recoverable=recoverable,
            context=context,
        )
