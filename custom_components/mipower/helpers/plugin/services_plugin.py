"""
Services Plugin Implementation for Smartify.

This module implements the Services system as a plugin following SOLID principles,
Pure Dependency Injection, and Facade patterns.
"""

import logging
from typing import Any, Dict, Optional

from .plugin_interface import PluginInterface

_LOGGER = logging.getLogger(__name__)


class ServicesPlugin(PluginInterface):
    """Plugin implementation for Services functionality.

    This plugin provides service registration and management capabilities with
    Pure Dependency Injection and configuration-driven behavior, following SOLID principles.
    """

    def __init__(self, service_registry, hass, config: Optional[Dict[str, Any]] = None):
        """Initialize the services plugin with dependencies.

        Args:
            service_registry: Service registry instance (injected)
            hass: Home Assistant instance (injected)
            config: Plugin configuration
        """
        self._service_registry = service_registry
        self._hass = hass
        self._config = config or {}

    def get_name(self) -> str:
        """Get the unique name of this plugin."""
        return "services"

    def get_version(self) -> str:
        """Get the version of this plugin."""
        return "1.0.0"

    def get_description(self) -> str:
        """Get a human-readable description of the plugin."""
        return "Service registration and management for Smartify integration"

    async def initialize(self, context: Dict[str, Any]) -> bool:
        """Initialize the plugin with the given context.

        Args:
            context: Initialization context containing dependencies and configuration

        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            # Plugin is already initialized through DI, just validate
            if not self._service_registry:
                _LOGGER.error(
                    "Service registry not provided through dependency injection",
                    exc_info=True,
                )
                return False

            if not self._hass:
                _LOGGER.error(
                    "Home Assistant instance not provided through dependency injection",
                    exc_info=True,
                )
                return False

            _LOGGER.info("Services plugin initialized successfully")
            return True

        except Exception as e:
            _LOGGER.error(
                "Failed to initialize Services plugin: %s",
                e,
                exc_info=True,
            )
            return False

    async def cleanup(self) -> None:
        """Clean up plugin resources and perform shutdown operations."""
        if self._service_registry:
            try:
                self._service_registry.unregister_services(self._hass)
                _LOGGER.debug("Services plugin cleaned up")
            except Exception as e:
                _LOGGER.error(
                    "Error cleaning up Services plugin: %s",
                    e,
                    exc_info=True,
                )

    def get_capabilities(self) -> Dict[str, Any]:
        """Get the capabilities provided by this plugin.

        Returns:
            Dict[str, Any]: Dictionary of plugin capabilities
        """
        return {
            "service_registration": True,
            "service_management": True,
            "command_execution": True,
            "calibration_services": True,
            "verification_services": True,
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
        return []  # Services is independent

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
                    "description": "Enable services plugin",
                },
                "auto_register": {
                    "type": "boolean",
                    "default": True,
                    "description": "Automatically register services on startup",
                },
                "service_timeout": {
                    "type": "number",
                    "default": 30.0,
                    "description": "Default timeout for service execution",
                },
                "enable_validation": {
                    "type": "boolean",
                    "default": True,
                    "description": "Enable service call validation",
                },
                "supported_services": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["send_command", "force_verify", "calibrate"],
                    },
                    "default": ["send_command", "force_verify", "calibrate"],
                    "description": "List of supported services",
                },
            },
        }

    def get_service_registry(self):
        """Get the service registry instance.

        Returns:
            ServiceRegistry instance or None if not initialized
        """
        return self._service_registry

    async def register_services(self):
        """Register services with Home Assistant.

        Returns:
            bool: True if registration successful
        """
        if not self._service_registry:
            return False

        return await self._service_registry.register_services(self._hass)

    def unregister_services(self):
        """Unregister services from Home Assistant.

        Returns:
            bool: True if unregistration successful
        """
        if not self._service_registry:
            return False

        return self._service_registry.unregister_services(self._hass)

    def get_services_info(self) -> Dict[str, Any]:
        """Get information about registered services.

        Returns:
            Dict[str, Any]: Services information
        """
        if not self._service_registry:
            return {"error": "Services plugin not initialized"}

        return {
            "plugin_enabled": self.is_enabled(),
            "services_registered": True,  # Assuming if plugin is initialized, services are registered
            "supported_services": [
                "send_command",
                "force_verify",
                "calibrate",
            ],
            "configuration": self._config,
        }
