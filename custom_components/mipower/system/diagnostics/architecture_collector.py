"""
Architecture Diagnostics Collector - Single Responsibility Principle

This module implements architecture diagnostics functionality following SOLID principles,
handling collection of SOLID architecture information for diagnostics.
"""

import logging
from typing import Any, Dict

from homeassistant.config_entries import ConfigEntry  # type: ignore[import]
from homeassistant.core import HomeAssistant  # type: ignore[import]

from ...const import DOMAIN
from .interface import ArchitectureDiagnosticsInterface

_LOGGER = logging.getLogger(__name__)


class ArchitectureDiagnosticsCollector(ArchitectureDiagnosticsInterface):
    """Handles collection of architecture diagnostics information.

    This class is responsible for gathering information about the SOLID architecture
    components, dependency injection container, plugin system, etc. for diagnostics.
    Follows Single Responsibility Principle by focusing only on architecture diagnostics.
    """

    def __init__(self):
        """Initialize the architecture diagnostics collector."""
        _LOGGER.debug("ArchitectureDiagnosticsCollector initialized")

    def collect_architecture_diagnostics(
        self, hass: HomeAssistant, entry: ConfigEntry
    ) -> Dict[str, Any]:
        """Collect architecture diagnostics information.

        Gathers comprehensive information about the SOLID architecture components
        including dependency injection, lazy loading, plugin system, and facade pattern.

        Args:
            hass: Home Assistant instance.
            entry: Configuration entry.

        Returns:
            Dictionary containing architecture diagnostics.
        """
        try:
            _LOGGER.debug(
                "Collecting architecture diagnostics for '%s' (ID: %s)",
                entry.title,
                entry.entry_id,
            )

            # Get integration data from new SOLID architecture
            integration_data = hass.data.get(DOMAIN, {}).get(entry.entry_id)

            if integration_data:
                coordinator = integration_data.get("coordinator")
                container = integration_data.get("container")
                facade = integration_data.get("facade")
                plugin_registry = integration_data.get("plugin_registry")
                lazy_loader = integration_data.get("lazy_loader")
                config_loader = integration_data.get("config_loader")

                # Coordinator information
                coordinator_info = {}
                if coordinator:
                    coordinator_info = {
                        "name": coordinator.name,
                        "update_interval": (
                            coordinator.update_interval.total_seconds()
                            if coordinator.update_interval
                            else None
                        ),
                        "last_update_success": coordinator.last_update_success,
                        "data": coordinator.data,
                    }

                # New architecture information
                architecture_diagnostics = {
                    "solid_architecture_enabled": True,
                    "coordinator": coordinator_info,
                    "dependency_injection": {
                        "container_available": container is not None,
                        "dependency_count": (
                            len(container._instances) if container else 0
                        ),
                        "registered_services": (
                            list(container._services.keys()) if container else []
                        ),
                    },
                    "lazy_loading": {
                        "enabled": lazy_loader is not None,
                        "loaded_components": (
                            [
                                comp
                                for comp in [
                                    "coordinator",
                                    "power_analyzer",
                                    "script_executor",
                                ]
                                if lazy_loader and lazy_loader.is_loaded(comp)
                            ]
                            if lazy_loader
                            else []
                        ),
                    },
                    "plugin_system": {
                        "enabled": plugin_registry is not None,
                        "registered_plugins": (
                            len(plugin_registry._plugins) if plugin_registry else 0
                        ),
                        "initialized_plugins": (
                            len(plugin_registry._initialized_plugins)
                            if plugin_registry
                            else 0
                        ),
                        "available_plugins": (
                            list(plugin_registry._plugins.keys())
                            if plugin_registry
                            else []
                        ),
                    },
                    "facade_pattern": {
                        "enabled": facade is not None,
                        "available_services": (
                            list(facade._services.keys()) if facade else []
                        ),
                    },
                    "configuration_driven": {
                        "config_loader_available": config_loader is not None,
                        "features_enabled": (
                            list(
                                config_loader.load_configuration()
                                .get("features", {})
                                .keys()
                            )
                            if config_loader
                            else []
                        ),
                        "active_configuration": (
                            config_loader.load_configuration() if config_loader else {}
                        ),
                    },
                }

                _LOGGER.debug(
                    "Architecture diagnostics collected successfully for '%s'",
                    entry.title,
                )

            else:
                # Fallback to old architecture
                _LOGGER.debug(
                    "Falling back to legacy architecture lookup for '%s'",
                    entry.title,
                )
                coordinator = hass.data.get(DOMAIN, {}).get(entry.entry_id)

                coordinator_info = {}
                if coordinator:
                    coordinator_info = {
                        "name": coordinator.name,
                        "update_interval": (
                            coordinator.update_interval.total_seconds()
                            if coordinator.update_interval
                            else None
                        ),
                        "last_update_success": coordinator.last_update_success,
                        "data": coordinator.data,
                    }

                architecture_diagnostics = {
                    "solid_architecture_enabled": False,
                    "coordinator": coordinator_info,
                    "note": "Using legacy architecture - integration may need restart",
                    "dependency_injection": {"enabled": False},
                    "lazy_loading": {"enabled": False},
                    "plugin_system": {"enabled": False},
                    "facade_pattern": {"enabled": False},
                    "configuration_driven": {"enabled": False},
                }

            return architecture_diagnostics

        except Exception as e:
            _LOGGER.error(
                "Error collecting architecture diagnostics for '%s': %s",
                getattr(
                    entry,
                    "title",
                    "Unknown",
                ),
                e,
                exc_info=True,
            )
            return {
                "error": "Failed to collect architecture diagnostics",
                "error_details": str(e),
            }
