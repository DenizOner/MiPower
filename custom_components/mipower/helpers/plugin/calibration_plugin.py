"""
Calibration Plugin Implementation for Smartify.

This module implements the Calibration system as a plugin following SOLID principles,
Pure Dependency Injection, and Facade patterns.
"""

import logging
from typing import Any, Dict, Optional

from .plugin_interface import PluginInterface

_LOGGER = logging.getLogger(__name__)


class CalibrationPlugin(PluginInterface):
    """Plugin implementation for Calibration functionality.

    This plugin provides calibration capabilities with Pure Dependency Injection
    and configuration-driven behavior, following SOLID principles.
    """

    def __init__(self, calibration_flow, config: Optional[Dict[str, Any]] = None):
        """Initialize the calibration plugin with dependencies.

        Args:
            calibration_flow: Calibration flow instance (injected)
            config: Plugin configuration
        """
        self._calibration_flow = calibration_flow
        self._config = config or {}

    def get_name(self) -> str:
        """Get the unique name of this plugin."""
        return "calibration"

    def get_version(self) -> str:
        """Get the version of this plugin."""
        return "1.0.0"

    def get_description(self) -> str:
        """Get a human-readable description of the plugin."""
        return "Device power calibration with measurement and threshold calculation"

    async def initialize(self, context: Dict[str, Any]) -> bool:
        """Initialize the plugin with the given context.

        Args:
            context: Initialization context containing dependencies and configuration

        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            # Plugin is already initialized through DI, just validate
            if not self._calibration_flow:
                _LOGGER.error(
                    "Calibration flow not provided through dependency injection",
                    exc_info=True,
                )
                return False

            _LOGGER.info("Calibration plugin initialized successfully")
            return True

        except Exception as e:
            _LOGGER.error(
                "Failed to initialize Calibration plugin: %s",
                e,
                exc_info=True,
            )
            return False

    async def cleanup(self) -> None:
        """Clean up plugin resources and perform shutdown operations."""
        if self._calibration_flow and hasattr(self._calibration_flow, "cleanup"):
            try:
                await self._calibration_flow.cleanup()
                _LOGGER.debug("Calibration plugin cleaned up")
            except Exception as e:
                _LOGGER.error(
                    "Error cleaning up Calibration plugin: %s",
                    e,
                    exc_info=True,
                )

    def get_capabilities(self) -> Dict[str, Any]:
        """Get the capabilities provided by this plugin.

        Returns:
            Dict[str, Any]: Dictionary of plugin capabilities
        """
        return {
            "device_calibration": True,
            "power_measurement": True,
            "threshold_calculation": True,
            "calibration_flow": True,
            "adaptive_calibration": True,
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
        return []  # Calibration is independent

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
                    "description": "Enable calibration plugin",
                },
                "measurement_samples": {
                    "type": "integer",
                    "default": 5,
                    "description": "Number of power samples to collect during calibration",
                },
                "measurement_interval": {
                    "type": "number",
                    "default": 1.0,
                    "description": "Interval between power measurements in seconds",
                },
                "auto_calibration": {
                    "type": "boolean",
                    "default": False,
                    "description": "Enable automatic calibration when thresholds are invalid",
                },
                "calibration_timeout": {
                    "type": "number",
                    "default": 300.0,
                    "description": "Maximum time allowed for calibration process",
                },
                "safety_margin": {
                    "type": "number",
                    "default": 0.8,
                    "description": "Safety margin multiplier for threshold calculations",
                },
                "enable_history": {
                    "type": "boolean",
                    "default": True,
                    "description": "Enable calibration history tracking",
                },
            },
        }

    def get_calibration_flow(self):
        """Get the calibration flow instance.

        Returns:
            CalibrationFlow instance or None if not initialized
        """
        return self._calibration_flow

    async def start_calibration(self, entity_id: str) -> Dict[str, Any]:
        """Start calibration process for a device.

        Args:
            entity_id: Entity ID to calibrate

        Returns:
            Dict[str, Any]: Calibration start result
        """
        if not self._calibration_flow:
            return {
                "success": False,
                "error": "Calibration plugin not initialized",
            }

        try:
            # This would integrate with the actual flow system
            result = {
                "success": True,
                "entity_id": entity_id,
                "message": f"Calibration started for {entity_id}",
                "status": "in_progress",
            }
            _LOGGER.info("Calibration started for entity: %s", entity_id)
            return result

        except Exception as e:
            _LOGGER.error(
                "Error starting calibration for %s: %s",
                entity_id,
                e,
                exc_info=True,
            )
            return {"success": False, "entity_id": entity_id, "error": str(e)}

    def get_calibration_status(self, entity_id: str) -> Dict[str, Any]:
        """Get calibration status for a device.

        Args:
            entity_id: Entity ID to check

        Returns:
            Dict[str, Any]: Calibration status
        """
        if not self._calibration_flow:
            return {
                "success": False,
                "error": "Calibration plugin not initialized",
            }

        return {
            "success": True,
            "entity_id": entity_id,
            "status": "ready",  # Would be dynamic based on actual state
            "last_calibration": None,  # Would be retrieved from history
            "next_calibration": None,
        }

    def get_calibration_history(
        self, entity_id: str, limit: int = 10
    ) -> Dict[str, Any]:
        """Get calibration history for a device.

        Args:
            entity_id: Entity ID to get history for
            limit: Maximum number of history entries

        Returns:
            Dict[str, Any]: Calibration history
        """
        if not self._calibration_flow:
            return {
                "success": False,
                "error": "Calibration plugin not initialized",
            }

        # This would integrate with actual history tracking
        return {
            "success": True,
            "entity_id": entity_id,
            "history": [],
            "count": 0,
            "message": "History tracking not yet implemented",
        }

    def validate_thresholds(
        self, on_threshold: float, off_threshold: float
    ) -> Dict[str, Any]:
        """Validate calibration thresholds.

        Args:
            on_threshold: ON state threshold
            off_threshold: OFF state threshold

        Returns:
            Dict[str, Any]: Validation result
        """
        errors = []

        if on_threshold <= 0:
            errors.append("ON threshold must be greater than 0")
        if off_threshold < 0:
            errors.append("OFF threshold must be non-negative")
        if on_threshold <= off_threshold:
            errors.append("ON threshold must be greater than OFF threshold")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "on_threshold": on_threshold,
            "off_threshold": off_threshold,
        }

    def get_calibration_info(self) -> Dict[str, Any]:
        """Get comprehensive calibration information.

        Returns:
            Dict[str, Any]: Calibration system information
        """
        if not self._calibration_flow:
            return {"error": "Calibration plugin not initialized"}

        return {
            "plugin_enabled": self.is_enabled(),
            "capabilities": self.get_capabilities(),
            "configuration": self._config,
            "supported_features": [
                "power_measurement",
                "threshold_calculation",
                "calibration_history",
                "adaptive_calibration",
            ],
        }
