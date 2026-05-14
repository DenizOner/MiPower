"""
Monitoring Plugin for Smartify.

This module implements the Monitoring system as a plugin following the plugin architecture
pattern, allowing for dynamic loading and configuration-driven behavior.
"""

import logging
from typing import Any, Dict, Optional

from custom_components.smartify.helpers.plugin.plugin_interface import (
    PluginContext,
    PluginInterface,
)

_LOGGER = logging.getLogger(__name__)


class MonitoringPlugin(PluginInterface):
    """Plugin implementation for Monitoring functionality.

    This plugin provides comprehensive monitoring capabilities with dependency injection
    and configuration-driven behavior, following SOLID principles.
    """

    def __init__(self):
        """Initialize the monitoring plugin."""
        self._metrics_collector = None
        self._context: Optional[PluginContext] = None
        self._config = {}

    def get_name(self) -> str:
        """Get the unique name of this plugin."""
        return "monitoring"

    def get_version(self) -> str:
        """Get the version of this plugin."""
        return "1.0.0"

    def get_description(self) -> str:
        """Get a human-readable description of the plugin."""
        return "Comprehensive performance monitoring with metrics, health checks, and alerting"

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

            # Create metrics collector through container
            self._metrics_collector = container.create_metrics_collector()

            _LOGGER.info("Monitoring plugin initialized successfully")
            return True

        except Exception as e:
            _LOGGER.error(
                "Failed to initialize Monitoring plugin: %s",
                e,
                exc_info=True,
            )
            return False

    async def cleanup(self) -> None:
        """Clean up plugin resources and perform shutdown operations."""
        if self._metrics_collector and hasattr(self._metrics_collector, "cleanup"):
            try:
                await self._metrics_collector.cleanup()
                _LOGGER.debug("Monitoring plugin cleaned up")
            except Exception as e:
                _LOGGER.error(
                    "Error cleaning up Monitoring plugin: %s",
                    e,
                    exc_info=True,
                )

        self._metrics_collector = None
        self._context = None

    def get_capabilities(self) -> Dict[str, Any]:
        """Get the capabilities provided by this plugin.

        Returns:
            Dict[str, Any]: Dictionary of plugin capabilities
        """
        return {
            "metrics_collection": True,
            "health_checking": True,
            "alert_management": True,
            "statistics_calculation": True,
            "performance_monitoring": True,
            "time_series_storage": True,
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
        return []  # Monitoring is independent

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
                    "description": "Enable monitoring plugin",
                },
                "retention_period": {
                    "type": "integer",
                    "default": 3600,
                    "description": "How long to keep metrics in seconds",
                },
                "max_alerts": {
                    "type": "integer",
                    "default": 1000,
                    "description": "Maximum number of alerts to keep",
                },
                "enable_health_checks": {
                    "type": "boolean",
                    "default": True,
                    "description": "Enable automatic health checks",
                },
                "enable_statistics": {
                    "type": "boolean",
                    "default": True,
                    "description": "Enable statistics calculation",
                },
                "alert_severities": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["info", "warning", "error", "critical"],
                    },
                    "default": ["warning", "error", "critical"],
                    "description": "Alert severities to track",
                },
            },
        }

    def get_metrics_collector(self):
        """Get the metrics collector instance.

        Returns:
            MetricsCollector instance or None if not initialized
        """
        return self._metrics_collector

    def record_metric(
        self, name: str, value: float, labels: Optional[Dict[str, str]] = None
    ):
        """Record a metric.

        Args:
            name: Metric name
            value: Metric value
            labels: Optional labels
        """
        if self._metrics_collector:
            self._metrics_collector.record_metric(name, value, labels)

    def get_metric_value(self, name: str) -> Optional[float]:
        """Get the latest value of a metric.

        Args:
            name: Metric name

        Returns:
            Latest value or None
        """
        if self._metrics_collector:
            return self._metrics_collector.get_metric_value(name)
        return None

    def add_alert(
        self,
        alert_name: str,
        message: str,
        severity: str = "warning",
        labels: Optional[Dict[str, str]] = None,
    ):
        """Add an alert.

        Args:
            alert_name: Alert name
            message: Alert message
            severity: Alert severity
            labels: Optional labels
        """
        if self._metrics_collector:
            self._metrics_collector.add_alert(alert_name, message, severity, labels)

    def get_health_status(self) -> Dict[str, Any]:
        """Get health status.

        Returns:
            Health status information
        """
        if self._metrics_collector:
            return self._metrics_collector.get_health_status()
        return {"error": "Monitoring plugin not initialized"}

    def get_monitoring_summary(self) -> Dict[str, Any]:
        """Get comprehensive monitoring summary.

        Returns:
            Monitoring summary
        """
        if not self._metrics_collector:
            return {"error": "Monitoring plugin not initialized"}

        return {
            "metrics": self._metrics_collector.get_all_metrics(),
            "health": self._metrics_collector.get_health_status(),
            "alerts": self._metrics_collector.get_alerts(limit=50),
            "summary": self._metrics_collector.get_summary(),
        }
