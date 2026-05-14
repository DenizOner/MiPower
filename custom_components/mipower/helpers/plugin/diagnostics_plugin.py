"""
Diagnostics Plugin Implementation for Smartify.

This module implements the Diagnostics system as a plugin following SOLID principles,
Pure Dependency Injection, and Facade patterns.
"""

import logging
from typing import Any, Dict, Optional

from .plugin_interface import PluginInterface

_LOGGER = logging.getLogger(__name__)


class DiagnosticsPlugin(PluginInterface):
    """Plugin implementation for Diagnostics functionality.

    This plugin provides diagnostics capabilities with Pure Dependency Injection
    and configuration-driven behavior, following SOLID principles.
    """

    def __init__(
        self, diagnostics_orchestrator, config: Optional[Dict[str, Any]] = None
    ):
        """Initialize the diagnostics plugin with dependencies.

        Args:
            diagnostics_orchestrator: Diagnostics orchestrator instance (injected)
            config: Plugin configuration
        """
        self._diagnostics_orchestrator = diagnostics_orchestrator
        self._config = config or {}

    def get_name(self) -> str:
        """Get the unique name of this plugin."""
        return "diagnostics"

    def get_version(self) -> str:
        """Get the version of this plugin."""
        return "1.0.0"

    def get_description(self) -> str:
        """Get a human-readable description of the plugin."""
        return "Comprehensive system diagnostics and health monitoring"

    async def initialize(self, context: Dict[str, Any]) -> bool:
        """Initialize the plugin with the given context.

        Args:
            context: Initialization context containing dependencies and configuration

        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            # Plugin is already initialized through DI, just validate
            if not self._diagnostics_orchestrator:
                _LOGGER.error(
                    "Diagnostics orchestrator not provided through dependency injection",
                    exc_info=True,
                )
                return False

            _LOGGER.info("Diagnostics plugin initialized successfully")
            return True

        except Exception as e:
            _LOGGER.error(
                "Failed to initialize Diagnostics plugin: %s",
                e,
                exc_info=True,
            )
            return False

    async def cleanup(self) -> None:
        """Clean up plugin resources and perform shutdown operations."""
        if self._diagnostics_orchestrator and hasattr(
            self._diagnostics_orchestrator, "cleanup"
        ):
            try:
                await self._diagnostics_orchestrator.cleanup()
                _LOGGER.debug("Diagnostics plugin cleaned up")
            except Exception as e:
                _LOGGER.error(
                    "Error cleaning up Diagnostics plugin: %s",
                    e,
                    exc_info=True,
                )

    def get_capabilities(self) -> Dict[str, Any]:
        """Get the capabilities provided by this plugin.

        Returns:
            Dict[str, Any]: Dictionary of plugin capabilities
        """
        return {
            "system_diagnostics": True,
            "configuration_analysis": True,
            "entity_monitoring": True,
            "calibration_diagnostics": True,
            "architecture_inspection": True,
            "health_monitoring": True,
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
        return []  # Diagnostics is independent

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
                    "description": "Enable diagnostics plugin",
                },
                "enable_config_diagnostics": {
                    "type": "boolean",
                    "default": True,
                    "description": "Enable configuration diagnostics collection",
                },
                "enable_entity_diagnostics": {
                    "type": "boolean",
                    "default": True,
                    "description": "Enable entity diagnostics collection",
                },
                "enable_calibration_diagnostics": {
                    "type": "boolean",
                    "default": True,
                    "description": "Enable calibration diagnostics collection",
                },
                "enable_architecture_diagnostics": {
                    "type": "boolean",
                    "default": True,
                    "description": "Enable architecture diagnostics collection",
                },
                "diagnostics_cache_timeout": {
                    "type": "integer",
                    "default": 300,
                    "minimum": 60,
                    "maximum": 3600,
                    "description": "Cache timeout for diagnostics data in seconds",
                },
                "max_diagnostic_entries": {
                    "type": "integer",
                    "default": 1000,
                    "minimum": 100,
                    "maximum": 10000,
                    "description": "Maximum number of diagnostic entries to collect",
                },
                "enable_performance_metrics": {
                    "type": "boolean",
                    "default": True,
                    "description": "Enable performance metrics collection",
                },
            },
        }

    def get_diagnostics_orchestrator(self):
        """Get the diagnostics orchestrator instance.

        Returns:
            DiagnosticsOrchestrator instance or None if not initialized
        """
        return self._diagnostics_orchestrator

    async def collect_diagnostics(self, hass, entry) -> Dict[str, Any]:
        """Collect comprehensive diagnostics.

        Args:
            hass: Home Assistant instance
            entry: Configuration entry

        Returns:
            Dict[str, Any]: Diagnostics data
        """
        if not self._diagnostics_orchestrator:
            return {"error": "Diagnostics plugin not initialized"}

        try:
            diagnostics = await self._diagnostics_orchestrator.collect_diagnostics(
                hass, entry
            )
            return {
                "success": True,
                "diagnostics": diagnostics,
                "timestamp": diagnostics.get("timestamp", "unknown"),
            }
        except Exception as e:
            _LOGGER.error(
                "Error collecting diagnostics: %s",
                e,
                exc_info=True,
            )
            return {
                "success": False,
                "error": str(e),
            }

    def get_diagnostic_summary(self, diagnostics: Dict[str, Any]) -> Dict[str, Any]:
        """Get a summary of diagnostic data.

        Args:
            diagnostics: Full diagnostics data

        Returns:
            Dict[str, Any]: Diagnostic summary
        """
        if not diagnostics or "error" in diagnostics:
            return {"error": "No valid diagnostics data"}

        try:
            summary = {
                "total_sections": len(diagnostics),
                "has_config": "entry" in diagnostics,
                "has_entities": "entities" in diagnostics
                and isinstance(diagnostics["entities"], list),
                "has_architecture": "architecture" in diagnostics,
                "has_calibration": "calibration" in diagnostics,
                "entity_count": 0,
                "error_sections": [],
            }

            if summary["has_entities"]:
                summary["entity_count"] = len(diagnostics["entities"])

            # Count error sections
            for section_name, section_data in diagnostics.items():
                if isinstance(section_data, dict) and "error" in section_data:
                    summary["error_sections"].append(section_name)

            summary["error_count"] = len(summary["error_sections"])
            summary["health_score"] = max(0, 100 - (summary["error_count"] * 20))

            return summary

        except Exception as e:
            _LOGGER.error(
                "Error creating diagnostic summary: %s",
                e,
                exc_info=True,
            )
            return {"error": str(e)}

    def validate_diagnostics_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate diagnostics configuration.

        Args:
            config: Configuration to validate

        Returns:
            Dict[str, Any]: Validation result
        """
        errors = []
        warnings = []

        # Check required settings
        if config.get("max_diagnostic_entries", 0) > 10000:
            errors.append("max_diagnostic_entries too high (>10000)")

        if config.get("diagnostics_cache_timeout", 0) < 60:
            errors.append("diagnostics_cache_timeout too low (<60 seconds)")

        # Check for reasonable combinations
        enabled_features = [
            config.get("enable_config_diagnostics", True),
            config.get("enable_entity_diagnostics", True),
            config.get("enable_calibration_diagnostics", True),
            config.get("enable_architecture_diagnostics", True),
        ]

        if not any(enabled_features):
            warnings.append("All diagnostic features are disabled")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "enabled_features": sum(enabled_features),
        }

    def get_diagnostics_info(self) -> Dict[str, Any]:
        """Get comprehensive diagnostics information.

        Returns:
            Dict[str, Any]: Diagnostics system information
        """
        if not self._diagnostics_orchestrator:
            return {"error": "Diagnostics plugin not initialized"}

        return {
            "plugin_enabled": self.is_enabled(),
            "capabilities": self.get_capabilities(),
            "configuration": self._config,
            "supported_diagnostics": [
                "configuration",
                "entities",
                "architecture",
                "calibration",
                "performance",
            ],
            "orchestrator_status": (
                "active" if self._diagnostics_orchestrator else "inactive"
            ),
        }
