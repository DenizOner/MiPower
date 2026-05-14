"""
Logger Plugin for Smartify.

This module implements the Logger system as a plugin following the plugin architecture
pattern, allowing for dynamic loading and configuration-driven behavior.
"""

import logging
from typing import Any, Dict, Optional

from ..plugin.plugin_interface import PluginContext, PluginInterface

_LOGGER = logging.getLogger(__name__)


class LoggerPlugin(PluginInterface):
    """Plugin implementation for Logger functionality.

    This plugin provides logging capabilities with dependency injection
    and configuration-driven behavior, following SOLID principles.
    """

    def __init__(self):
        """Initialize the logger plugin."""
        self._logger_factory = None
        self._context: Optional[PluginContext] = None
        self._config = {}

    def get_name(self) -> str:
        """Get the unique name of this plugin."""
        return "logger"

    def get_version(self) -> str:
        """Get the version of this plugin."""
        return "1.0.0"

    def get_description(self) -> str:
        """Get a human-readable description of the plugin."""
        return "Comprehensive logging system with structured logging and device/entity tracking"

    async def initialize(self, context: Dict[str, Any]) -> bool:
        """Initialize the plugin with the given context.

        Args:
            context: Initialization context containing dependencies and configuration

        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            self._context = PluginContext(
                hass=context.get("hass"),
                entry=context.get("entry"),
                container=context.get("container"),
            )
            self._config = context.get("config", {})

            # Get container from context
            container = context.get("container")
            if not container:
                _LOGGER.error(
                    "Container not provided in plugin context",
                    exc_info=True,
                )
                return False

            # Create logger factory through container
            self._logger_factory = container.create_logger_factory()

            _LOGGER.info("Logger plugin initialized successfully")
            return True

        except Exception as e:
            _LOGGER.error(
                "Failed to initialize Logger plugin: %s",
                e,
                exc_info=True,
            )
            return False

    async def cleanup(self) -> None:
        """Clean up plugin resources and perform shutdown operations."""
        if self._logger_factory and hasattr(self._logger_factory, "cleanup"):
            try:
                await self._logger_factory.cleanup()
                _LOGGER.debug("Logger plugin cleaned up")
            except Exception as e:
                _LOGGER.error(
                    "Error cleaning up Logger plugin: %s",
                    e,
                    exc_info=True,
                )

        self._logger_factory = None
        self._context = None

    def get_capabilities(self) -> Dict[str, Any]:
        """Get the capabilities provided by this plugin.

        Returns:
            Dict[str, Any]: Dictionary of plugin capabilities
        """
        return {
            "structured_logging": True,
            "device_evaluation_logging": True,
            "entity_inspection_logging": True,
            "configurable_log_levels": True,
            "log_rotation": True,
            "performance_logging": True,
        }

    def is_enabled(self) -> bool:
        """Check if the plugin is currently enabled.

        Returns:
            bool: True if enabled, False otherwise
        """
        return self._config.get("enabled", True)

    def get_dependencies(self) -> list[str]:
        """Get list of plugin dependencies.

        Returns:
            list[str]: List of required plugin names
        """
        return []  # Logger is independent

    def get_configuration_schema(self) -> Optional[Dict[str, Any]]:
        """Get configuration schema for this plugin.

        Returns:
            Optional[Dict[str, Any]]: Configuration schema or None if no config needed
        """
        return {
            "type": "object",
            "properties": {
                "enabled": {
                    "type": "boolean",
                    "default": True,
                    "description": "Enable logger plugin",
                },
                "namespace": {
                    "type": "string",
                    "default": "smartify",
                    "description": "Base namespace for loggers",
                },
                "default_log_level": {
                    "type": "string",
                    "enum": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                    "default": "INFO",
                    "description": "Default log level",
                },
                "enable_device_logging": {
                    "type": "boolean",
                    "default": True,
                    "description": "Enable device evaluation logging",
                },
                "enable_entity_logging": {
                    "type": "boolean",
                    "default": True,
                    "description": "Enable entity inspection logging",
                },
                "enable_performance_logging": {
                    "type": "boolean",
                    "default": False,
                    "description": "Enable performance metrics logging",
                },
                "log_format": {
                    "type": "string",
                    "default": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    "description": "Log message format",
                },
                "max_log_files": {
                    "type": "integer",
                    "default": 5,
                    "minimum": 1,
                    "maximum": 20,
                    "description": "Maximum number of log files to keep",
                },
                "max_log_size_mb": {
                    "type": "integer",
                    "default": 10,
                    "minimum": 1,
                    "maximum": 100,
                    "description": "Maximum log file size in MB",
                },
            },
        }

    def get_logger_factory(self):
        """Get the logger factory instance.

        Returns:
            LoggerFactory instance or None if not initialized
        """
        return self._logger_factory

    def get_logger(self, name: str):
        """Get a logger instance for the specified name.

        Args:
            name: Logger name

        Returns:
            LoggerInterface instance or None if not initialized
        """
        if not self._logger_factory:
            _LOGGER.warning("Logger plugin not initialized")
            return None

        try:
            return self._logger_factory.get_logger(name)
        except Exception as e:
            _LOGGER.error(
                "Error getting logger: %s",
                e,
                exc_info=True,
            )
            return None

    def log_device_evaluation(
        self, device_name: str, device_id: str, success: bool, reason: str = ""
    ) -> None:
        """Log device evaluation results.

        Args:
            device_name: Name of the device
            device_id: Unique device identifier
            success: Whether evaluation was successful
            reason: Reason for success/failure
        """
        if not self._logger_factory:
            _LOGGER.warning("Logger plugin not initialized")
            return

        try:
            logger = self._logger_factory.get_logger("device_evaluation")
            status = "SUCCESS" if success else "FAILED"
            message = f"Device evaluation: {device_name} ({device_id}) - {status}"
            if reason:
                message += f" - {reason}"

            if success:
                logger.info(message)
            else:
                logger.warning(message)
        except Exception as e:
            _LOGGER.error(
                "Error logging device evaluation: %s",
                e,
                exc_info=True,
            )

    def log_entity_inspection(
        self, entity_id: str, criterion: str, passed: bool, details: str = ""
    ) -> None:
        """Log entity inspection results.

        Args:
            entity_id: Entity identifier
            criterion: Inspection criterion
            passed: Whether inspection passed
            details: Additional details
        """
        if not self._logger_factory:
            _LOGGER.warning("Logger plugin not initialized")
            return

        try:
            logger = self._logger_factory.get_logger("entity_inspection")
            status = "PASSED" if passed else "FAILED"
            message = f"Entity inspection: {entity_id} - {criterion} - {status}"
            if details:
                message += f" - {details}"

            if passed:
                logger.debug(message)
            else:
                logger.warning(message)
        except Exception as e:
            _LOGGER.error(
                "Error logging entity inspection: %s",
                e,
                exc_info=True,
            )

    def log_performance_metric(
        self, operation: str, duration: float, success: bool
    ) -> None:
        """Log performance metrics.

        Args:
            operation: Name of the operation
            duration: Duration in seconds
            success: Whether operation was successful
        """
        if not self._logger_factory:
            return

        try:
            logger = self._logger_factory.get_logger("performance")
            logger.info(".3f")
        except Exception as e:
            _LOGGER.error(
                "Error logging performance metric: %s",
                e,
                exc_info=True,
            )

    def set_log_level(self, level: str) -> bool:
        """Set the default log level.

        Args:
            level: Log level string

        Returns:
            bool: True if successful
        """
        try:
            level_map = {
                "DEBUG": logging.DEBUG,
                "INFO": logging.INFO,
                "WARNING": logging.WARNING,
                "ERROR": logging.ERROR,
                "CRITICAL": logging.CRITICAL,
            }

            if level.upper() not in level_map:
                _LOGGER.error(
                    "Invalid log level: %s",
                    level,
                    exc_info=True,
                )
                return False

            # Set level for smartify namespace
            smartify_logger = logging.getLogger("smartify")
            smartify_logger.setLevel(level_map[level.upper()])

            _LOGGER.info("Log level set to: %s", level)
            return True
        except Exception as e:
            _LOGGER.error(
                "Error setting log level: %s",
                e,
                exc_info=True,
            )
            return False

    def get_log_statistics(self) -> Dict[str, Any]:
        """Get logging statistics.

        Returns:
            Dict[str, Any]: Logging statistics
        """
        try:
            # Get all loggers under smartify namespace
            smartify_logger = logging.getLogger("smartify")
            all_loggers = []

            def collect_loggers(logger):
                all_loggers.append(
                    {
                        "name": logger.name,
                        "level": logging.getLevelName(logger.level),
                        "handlers": len(logger.handlers),
                    }
                )
                for child in logger.children.values():
                    collect_loggers(child)

            collect_loggers(smartify_logger)

            return {
                "namespace": "smartify",
                "total_loggers": len(all_loggers),
                "loggers": all_loggers,
                "plugin_enabled": self.is_enabled(),
            }
        except Exception as e:
            _LOGGER.error(
                "Error getting log statistics: %s",
                e,
                exc_info=True,
            )
            return {"error": str(e)}

    def validate_logger_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate logger configuration.

        Args:
            config: Configuration to validate

        Returns:
            Dict[str, Any]: Validation result
        """
        errors = []
        warnings = []

        # Check log level
        log_level = config.get("default_log_level", "INFO")
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if log_level not in valid_levels:
            errors.append(
                f"Invalid log level: {log_level}. Must be one of {valid_levels}"
            )

        # Check log format
        log_format = config.get("log_format", "")
        if "%(message)s" not in log_format:
            warnings.append("Log format should include %(message)s")

        # Check file limits
        max_files = config.get("max_log_files", 5)
        if max_files < 1 or max_files > 20:
            errors.append("max_log_files must be between 1 and 20")

        max_size = config.get("max_log_size_mb", 10)
        if max_size < 1 or max_size > 100:
            errors.append("max_log_size_mb must be between 1 and 100")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
        }

    def get_logger_info(self) -> Dict[str, Any]:
        """Get comprehensive logger information.

        Returns:
            Dict[str, Any]: Logger system information
        """
        if not self._logger_factory:
            return {"error": "Logger plugin not initialized"}

        return {
            "plugin_enabled": self.is_enabled(),
            "capabilities": self.get_capabilities(),
            "configuration": self._config,
            "supported_features": [
                "structured_logging",
                "device_evaluation_logging",
                "entity_inspection_logging",
                "configurable_log_levels",
                "performance_logging",
            ],
            "factory_status": "active" if self._logger_factory else "inactive",
        }
