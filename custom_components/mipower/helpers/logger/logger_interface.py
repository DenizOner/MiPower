"""
Logger Interface - Dependency Inversion for Logging

This module defines the abstraction layer for logging functionality in Smartify,
implementing Dependency Inversion Principle (DIP) by decoupling logging operations
from the core components.
"""

from abc import ABC, abstractmethod


class LoggerInterface(ABC):
    """Abstract interface for logging functionality."""

    @abstractmethod
    def debug(self, message: str) -> None:
        """Log a debug message."""

    @abstractmethod
    def info(self, message: str) -> None:
        """Log an info message."""

    @abstractmethod
    def warning(self, message: str) -> None:
        """Log a warning message."""

    @abstractmethod
    def error(self, message: str) -> None:
        """Log an error message."""

    @abstractmethod
    def critical(self, message: str) -> None:
        """Log a critical message."""


class LoggerFactoryInterface(ABC):
    """Abstract interface for logger factory functionality."""

    @abstractmethod
    def get_logger(self, name: str) -> LoggerInterface:
        """Get a logger instance for the specified name.

        Args:
            name: The name to append to the namespace.

        Returns:
            LoggerInterface: A configured logger instance.
        """


class DeviceLoggerInterface(ABC):
    """Abstract interface for device evaluation logging."""

    @abstractmethod
    def log_device_evaluation(
        self,
        device_name: str,
        device_id: str,
        success: bool,
        reason: str = "",
    ) -> None:
        """Log device evaluation results with standardized formatting."""


class EntityLoggerInterface(ABC):
    """Abstract interface for entity inspection logging."""

    @abstractmethod
    def log_entity_inspection(
        self,
        entity_id: str,
        criterion: str,
        passed: bool,
        details: str = "",
    ) -> None:
        """Log entity inspection results with standardized formatting."""
