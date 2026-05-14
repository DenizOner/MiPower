"""
Batch Plugin for Smartify.

This module implements the Batch processing system as a plugin following the plugin architecture
pattern, allowing for dynamic loading and configuration-driven behavior.
"""

import logging
from typing import Any, Dict, Optional

from ..plugin.plugin_interface import PluginContext, PluginInterface

_LOGGER = logging.getLogger(__name__)


class BatchPlugin(PluginInterface):
    """Plugin implementation for Batch processing functionality.

    This plugin provides batch processing capabilities with dependency injection
    and configuration-driven behavior, following SOLID principles.
    """

    def __init__(self):
        """Initialize the batch plugin."""
        self._batch_processor = None
        self._context: Optional[PluginContext] = None
        self._config = {}

    def get_name(self) -> str:
        """Get the unique name of this plugin."""
        return "batch"

    def get_version(self) -> str:
        """Get the version of this plugin."""
        return "1.0.0"

    def get_description(self) -> str:
        """Get a human-readable description of the plugin."""
        return "Asynchronous batch processing with dependency resolution and statistics"

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

            # Create batch processor through container
            self._batch_processor = container.create_batch_processor()

            _LOGGER.info("Batch plugin initialized successfully")
            return True

        except Exception as e:
            _LOGGER.error(
                "Failed to initialize Batch plugin: %s",
                e,
                exc_info=True,
            )
            return False

    async def cleanup(self) -> None:
        """Clean up plugin resources and perform shutdown operations."""
        if self._batch_processor and hasattr(self._batch_processor, "cleanup"):
            try:
                await self._batch_processor.cleanup()
                _LOGGER.debug("Batch plugin cleaned up")
            except Exception as e:
                _LOGGER.error(
                    "Error cleaning up Batch plugin: %s",
                    e,
                    exc_info=True,
                )

        self._batch_processor = None
        self._context = None

    def get_capabilities(self) -> Dict[str, Any]:
        """Get the capabilities provided by this plugin.

        Returns:
            Dict[str, Any]: Dictionary of plugin capabilities
        """
        return {
            "batch_processing": True,
            "dependency_resolution": True,
            "concurrent_execution": True,
            "statistics_tracking": True,
            "priority_scheduling": True,
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
        return []  # Batch is independent

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
                    "description": "Enable batch processing plugin",
                },
                "max_concurrency": {
                    "type": "integer",
                    "default": 5,
                    "minimum": 1,
                    "maximum": 20,
                    "description": "Maximum number of concurrent operations",
                },
                "max_batch_size": {
                    "type": "integer",
                    "default": 100,
                    "minimum": 1,
                    "maximum": 1000,
                    "description": "Maximum number of operations per batch",
                },
                "default_timeout": {
                    "type": "number",
                    "default": 30.0,
                    "minimum": 1.0,
                    "maximum": 300.0,
                    "description": "Default timeout for operations in seconds",
                },
                "enable_dependency_resolution": {
                    "type": "boolean",
                    "default": True,
                    "description": "Enable automatic dependency resolution",
                },
                "enable_statistics": {
                    "type": "boolean",
                    "default": True,
                    "description": "Enable batch statistics tracking",
                },
                "enable_priority_scheduling": {
                    "type": "boolean",
                    "default": True,
                    "description": "Enable priority-based operation scheduling",
                },
            },
        }

    def get_batch_processor(self):
        """Get the batch processor instance.

        Returns:
            BatchProcessor instance or None if not initialized
        """
        return self._batch_processor

    async def create_batch(self, batch_id: str) -> Dict[str, Any]:
        """Create a new batch.

        Args:
            batch_id: Unique identifier for the batch

        Returns:
            Dict[str, Any]: Creation result
        """
        if not self._batch_processor:
            return {"success": False, "error": "Batch plugin not initialized"}

        try:
            await self._batch_processor.create_batch(batch_id)
            return {
                "success": True,
                "batch_id": batch_id,
                "message": f"Batch {batch_id} created successfully",
            }
        except Exception as e:
            _LOGGER.error(
                "Error creating batch %s: %s",
                batch_id,
                e,
                exc_info=True,
            )
            return {"success": False, "batch_id": batch_id, "error": str(e)}

    async def add_operation(
        self, batch_id: str, operation_id: str, operation_func, *args, **kwargs
    ) -> Dict[str, Any]:
        """Add an operation to a batch.

        Args:
            batch_id: The batch to add the operation to
            operation_id: Unique identifier for the operation
            operation_func: The async function to execute
            *args: Positional arguments for the operation
            **kwargs: Keyword arguments for the operation

        Returns:
            Dict[str, Any]: Addition result
        """
        if not self._batch_processor:
            return {"success": False, "error": "Batch plugin not initialized"}

        try:
            priority = kwargs.pop("priority", 0)
            dependencies = kwargs.pop("dependencies", None)

            await self._batch_processor.add_operation(
                batch_id,
                operation_id,
                operation_func,
                priority=priority,
                dependencies=dependencies,
                *args,
                **kwargs,
            )
            return {
                "success": True,
                "batch_id": batch_id,
                "operation_id": operation_id,
                "message": f"Operation {operation_id} added to batch {batch_id}",
            }
        except Exception as e:
            _LOGGER.error(
                "Error adding operation %s to batch %s: %s",
                operation_id,
                batch_id,
                e,
                exc_info=True,
            )
            return {
                "success": False,
                "batch_id": batch_id,
                "operation_id": operation_id,
                "error": str(e),
            }

    async def execute_batch(self, batch_id: str) -> Dict[str, Any]:
        """Execute all operations in a batch.

        Args:
            batch_id: The batch to execute

        Returns:
            Dict[str, Any]: Execution result
        """
        if not self._batch_processor:
            return {"success": False, "error": "Batch plugin not initialized"}

        try:
            result = await self._batch_processor.execute_batch(batch_id)
            return {
                "success": True,
                "batch_id": batch_id,
                "result": result.to_dict(),
                "status": result.status.value,
                "duration": result.get_duration(),
                "success_rate": result.get_success_rate(),
            }
        except Exception as e:
            _LOGGER.error(
                "Error executing batch %s: %s",
                batch_id,
                e,
                exc_info=True,
            )
            return {"success": False, "batch_id": batch_id, "error": str(e)}

    def get_batch_status(self, batch_id: str) -> Dict[str, Any]:
        """Get the status of a batch.

        Args:
            batch_id: The batch to query

        Returns:
            Dict[str, Any]: Batch status
        """
        if not self._batch_processor:
            return {"success": False, "error": "Batch plugin not initialized"}

        try:
            status = self._batch_processor.get_batch_status(batch_id)
            if status:
                return {
                    "success": True,
                    "batch_id": batch_id,
                    "status": status.to_dict(),
                }
            else:
                return {
                    "success": False,
                    "batch_id": batch_id,
                    "error": "Batch not found",
                }
        except Exception as e:
            _LOGGER.error(
                "Error getting batch status for %s: %s",
                batch_id,
                e,
                exc_info=True,
            )
            return {"success": False, "batch_id": batch_id, "error": str(e)}

    def get_batch_operations(self, batch_id: str) -> Dict[str, Any]:
        """Get all operations in a batch.

        Args:
            batch_id: The batch to query

        Returns:
            Dict[str, Any]: Batch operations
        """
        if not self._batch_processor:
            return {"success": False, "error": "Batch plugin not initialized"}

        try:
            operations = self._batch_processor.get_batch_operations(batch_id)
            return {
                "success": True,
                "batch_id": batch_id,
                "operations": {op_id: op.to_dict() for op_id, op in operations.items()},
                "count": len(operations),
            }
        except Exception as e:
            _LOGGER.error(
                "Error getting batch operations for %s: %s",
                batch_id,
                e,
                exc_info=True,
            )
            return {"success": False, "batch_id": batch_id, "error": str(e)}

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics.

        Returns:
            Dict[str, Any]: Performance statistics
        """
        if not self._batch_processor:
            return {"success": False, "error": "Batch plugin not initialized"}

        try:
            stats = self._batch_processor.get_performance_stats()
            return {"success": True, "statistics": stats}
        except Exception as e:
            _LOGGER.error(
                "Error getting performance stats: %s",
                e,
                exc_info=True,
            )
            return {"success": False, "error": str(e)}

    def get_batch_summary(self) -> Dict[str, Any]:
        """Get a comprehensive batch processing summary.

        Returns:
            Dict[str, Any]: Batch processing summary
        """
        if not self._batch_processor:
            return {"success": False, "error": "Batch plugin not initialized"}

        try:
            summary = self._batch_processor.get_batch_summary()
            return {"success": True, "summary": summary}
        except Exception as e:
            _LOGGER.error(
                "Error getting batch summary: %s",
                e,
                exc_info=True,
            )
            return {"success": False, "error": str(e)}
