"""Logger factory for Smartify integration.

This module provides centralized logger factory functionality following SOLID principles.
"""

import logging
from typing import Any, Dict, Optional

from ...di.container import DependencyContainer

_LOGGER = logging.getLogger(__name__)


class LoggerFactory:
    """Factory for creating and managing loggers."""

    def __init__(self, container: Optional[DependencyContainer] = None):
        """Initialize the logger factory."""
        self.container = container
        self._loggers: Dict[str, logging.Logger] = {}

    def get_logger(self, name: str) -> logging.Logger:
        """Get a logger instance with caching."""
        if name not in self._loggers:
            logger = logging.getLogger(f"custom_components.smartify.{name}")
            self._loggers[name] = logger
            if self.container:
                # Configure logger from container settings if available
                self._configure_logger_from_container(logger)
        return self._loggers[name]

    def _configure_logger_from_container(self, logger: logging.Logger) -> None:
        """Configure logger from container settings."""
        if not self.container:
            return

        try:
            # Get logging configuration from container
            log_config = self.container._plugin_config.get("logging", {})
            level = log_config.get("level", logging.INFO)

            # Set logger level
            logger.setLevel(level)

            # Add handlers if configured
            handlers = log_config.get("handlers", [])
            for handler_config in handlers:
                handler = self._create_handler(handler_config)
                if handler:
                    logger.addHandler(handler)

            _LOGGER.debug(f"Configured logger {logger.name} with level {level}")
        except Exception as e:
            _LOGGER.error(f"Failed to configure logger from container: {e}")

    def _create_handler(
        self, handler_config: Dict[str, Any]
    ) -> Optional[logging.Handler]:
        """Create a logging handler from configuration."""
        try:
            handler_type = handler_config.get("type", "stream")

            if handler_type == "stream":
                handler = logging.StreamHandler()
            elif handler_type == "file":
                filename = handler_config.get("filename")
                if filename:
                    handler = logging.FileHandler(filename)
                else:
                    return None
            else:
                return None

            # Configure handler
            level = handler_config.get("level", logging.INFO)
            handler.setLevel(level)

            # Add formatter if configured
            formatter_config = handler_config.get("formatter")
            if formatter_config:
                formatter = self._create_formatter(formatter_config)
                if formatter:
                    handler.setFormatter(formatter)

            return handler
        except Exception as e:
            _LOGGER.error(f"Failed to create handler: {e}")
            return None

    def _create_formatter(
        self, formatter_config: Dict[str, Any]
    ) -> Optional[logging.Formatter]:
        """Create a logging formatter from configuration."""
        try:
            fmt = formatter_config.get(
                "format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            datefmt = formatter_config.get("datefmt")
            return logging.Formatter(fmt, datefmt)
        except Exception as e:
            _LOGGER.error(f"Failed to create formatter: {e}")
            return None

    def configure_logging(self, level: int = logging.INFO) -> bool:
        """Configure logging for the integration."""
        try:
            logging.getLogger("custom_components.smartify").setLevel(level)
            _LOGGER.debug(f"Configured logging level to {level}")
            return True
        except Exception as e:
            _LOGGER.error(f"Failed to configure logging: {e}")
            return False

    def get_logging_status(self) -> Dict[str, Any]:
        """Get the status of logging configuration."""
        return {
            "logging_enabled": True,
            "current_level": logging.getLogger("custom_components.smartify").level,
            "effective_level": logging.getLogger(
                "custom_components.smartify"
            ).getEffectiveLevel(),
        }
