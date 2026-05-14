"""
Lock Manager Plugin for Smartify.

This module implements the LockManager as a plugin following the plugin architecture
pattern, allowing for dynamic loading and configuration-driven behavior.
"""

import logging
from typing import Any, Dict, Optional

from ..errors.exceptions import LockManagementError
from ..plugin.plugin_interface import PluginContext, PluginInterface

_LOGGER = logging.getLogger(__name__)


class LockManagerPlugin(PluginInterface):
    """Plugin implementation for Lock Manager functionality.

    This plugin provides lock management capabilities with dependency injection
    and configuration-driven behavior, following SOLID principles.
    """

    def __init__(self):
        """Initialize the lock manager plugin."""
        self._lock_manager = None
        self._context: Optional[PluginContext] = None
        self._config = {}

    def get_name(self) -> str:
        """Get the unique name of this plugin."""
        return "lock_manager"

    def get_version(self) -> str:
        """Get the version of this plugin."""
        return "1.0.0"

    def get_description(self) -> str:
        """Get a human-readable description of the plugin."""
        return "Advanced lock management with deadlock detection and statistics"

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

            # Create lock manager through container
            self._lock_manager = container.create_lock_manager()

            _LOGGER.info("LockManager plugin initialized successfully")
            return True

        except Exception as e:
            _LOGGER.error(
                "Failed to initialize LockManager plugin: %s",
                e,
                exc_info=True,
            )
            return False

    async def cleanup(self) -> None:
        """Clean up plugin resources and perform shutdown operations."""
        if self._lock_manager and hasattr(self._lock_manager, "cleanup"):
            try:
                await self._lock_manager.cleanup()
                _LOGGER.debug("LockManager plugin cleaned up")
            except Exception as e:
                _LOGGER.error(
                    "Error cleaning up LockManager plugin: %s",
                    e,
                    exc_info=True,
                )

        self._lock_manager = None
        self._context = None

    def get_capabilities(self) -> Dict[str, Any]:
        """Get the capabilities provided by this plugin.

        Returns:
            Dict[str, Any]: Dictionary of plugin capabilities
        """
        return {
            "lock_management": True,
            "deadlock_detection": True,
            "statistics_tracking": True,
            "hierarchical_locking": True,
            "async_operations": True,
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
        return []  # Lock manager is independent

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
                    "description": "Enable lock manager plugin",
                },
                "default_timeout": {
                    "type": "number",
                    "default": 30.0,
                    "description": "Default lock acquisition timeout in seconds",
                },
                "max_lock_time": {
                    "type": "number",
                    "default": 300.0,
                    "description": "Maximum allowed lock hold time in seconds",
                },
                "cleanup_interval": {
                    "type": "integer",
                    "default": 60,
                    "description": "Interval for lock cleanup in seconds",
                },
                "enable_statistics": {
                    "type": "boolean",
                    "default": True,
                    "description": "Enable lock statistics tracking",
                },
                "enable_deadlock_detection": {
                    "type": "boolean",
                    "default": True,
                    "description": "Enable deadlock detection",
                },
            },
        }

    def get_lock_manager(self):
        """Get the lock manager instance.

        Returns:
            LockManager instance or None if not initialized
        """
        return self._lock_manager

    async def execute_with_lock(
        self, lock_id: str, owner: str, operation, *args, **kwargs
    ):
        """Execute an operation with lock protection.

        Args:
            lock_id: Unique identifier for the lock
            owner: Identifier of the lock owner
            operation: The async operation to execute
            *args: Positional arguments for the operation
            **kwargs: Keyword arguments for the operation

        Returns:
            Result of the operation
        """
        if not self._lock_manager:
            raise LockManagementError("LockManager plugin not initialized")

        return await self._lock_manager.execute_with_lock(
            lock_id, owner, operation, *args, **kwargs
        )

    def get_lock_statistics(self) -> Dict[str, Any]:
        """Get lock statistics.

        Returns:
            Dict[str, Any]: Lock statistics
        """
        if not self._lock_manager:
            return {"error": "LockManager plugin not initialized"}

        return self._lock_manager.get_lock_statistics()
