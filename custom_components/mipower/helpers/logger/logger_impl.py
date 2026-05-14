"""
Logger Implementation - Single Responsibility Principle

This module implements logging functionality following SOLID principles,
providing concrete implementations for logging interfaces.
"""

import logging

from .logger_interface import LoggerFactoryInterface, LoggerInterface


class LoggerImpl(LoggerInterface):
    """Concrete implementation of LoggerInterface using Python logging."""

    def __init__(self, logger: logging.Logger):
        """Initialize the logger implementation.

        Args:
            logger: The underlying Python logger instance.
        """
        self._logger = logger

    def debug(self, message: str) -> None:
        """Log a debug message."""
        self._logger.debug(message)

    def info(self, message: str) -> None:
        """Log an info message."""
        self._logger.info(message)

    def warning(self, message: str) -> None:
        """Log a warning message."""
        self._logger.warning(message)

    def error(self, message: str) -> None:
        """Log an error message."""
        self._logger.error(message)

    def critical(self, message: str) -> None:
        """Log a critical message."""
        self._logger.critical(
            message,
            exc_info=True,
        )


class LoggerFactory(LoggerFactoryInterface):
    """Factory for creating logger instances with proper configuration."""

    def __init__(self, namespace: str = "smartify"):
        """Initialize the logger factory.

        Args:
            namespace: The base namespace for loggers.
        """
        self.namespace = namespace

    def get_logger(self, name: str) -> LoggerInterface:
        """Get a logger instance for the specified name.

        Creates or returns an existing logger with proper configuration.

        Args:
            name: The name to append to the namespace.

        Returns:
            LoggerInterface: A configured logger instance.
        """
        logger = logging.getLogger(f"{self.namespace}.{name}")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.DEBUG)

        return LoggerImpl(logger)
