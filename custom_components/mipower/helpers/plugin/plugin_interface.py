"""
Plugin Interface for Smartify.

This module defines the base interfaces and types for the plugin architecture
in Smartify, allowing for extensible and modular functionality following SOLID principles.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

_LOGGER = logging.getLogger(__name__)


class PluginInterface(ABC):
    """Base interface for all Smartify plugins.

    This abstract base class defines the contract that all plugins must implement,
    providing lifecycle management and integration capabilities following SOLID principles.
    """

    @abstractmethod
    def get_name(self) -> str:
        """Get the unique name of this plugin.

        Returns:
            str: Plugin name identifier
        """
        pass

    @abstractmethod
    def get_version(self) -> str:
        """Get the version of this plugin.

        Returns:
            str: Plugin version string
        """
        pass

    @abstractmethod
    def get_description(self) -> str:
        """Get a human-readable description of the plugin.

        Returns:
            str: Plugin description
        """
        pass

    @abstractmethod
    async def initialize(self, context: Dict[str, Any]) -> bool:
        """Initialize the plugin with the given context.

        Args:
            context: Initialization context containing dependencies and configuration

        Returns:
            bool: True if initialization successful, False otherwise
        """
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """Clean up plugin resources and perform shutdown operations."""
        pass

    @abstractmethod
    def get_capabilities(self) -> Dict[str, Any]:
        """Get the capabilities provided by this plugin.

        Returns:
            Dict[str, Any]: Dictionary of plugin capabilities
        """
        pass

    @abstractmethod
    def is_enabled(self) -> bool:
        """Check if the plugin is currently enabled.

        Returns:
            bool: True if enabled, False otherwise
        """
        pass

    def get_dependencies(self) -> list[str]:
        """Get list of plugin dependencies.

        Returns:
            list[str]: List of required plugin names
        """
        return []

    def get_configuration_schema(self) -> Optional[Dict[str, Any]]:
        """Get configuration schema for this plugin.

        Returns:
            Optional[Dict[str, Any]]: Configuration schema or None if no config needed
        """
        return None


class PluginContext:
    """Context object passed to plugins during initialization.

    This class provides access to shared resources and dependencies
    that plugins may need during their lifecycle following Pure DI principles.
    """

    def __init__(self, hass, entry, container):
        """Initialize plugin context.

        Args:
            hass: Home Assistant instance
            entry: Configuration entry
            container: Dependency injection container
        """
        self.hass = hass
        self.entry = entry
        self.container = container
        self.shared_data: Dict[str, Any] = {}

    def set_shared_data(self, key: str, value: Any) -> None:
        """Set shared data accessible by all plugins.

        Args:
            key: Data key
            value: Data value
        """
        self.shared_data[key] = value

    def get_shared_data(self, key: str, default: Any = None) -> Any:
        """Get shared data.

        Args:
            key: Data key
            default: Default value if key not found

        Returns:
            Any: Shared data value or default
        """
        return self.shared_data.get(key, default)
