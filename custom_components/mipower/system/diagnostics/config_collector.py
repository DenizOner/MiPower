"""
Configuration Diagnostics Collector - Single Responsibility Principle

This module implements configuration diagnostics functionality following SOLID principles,
handling collection of configuration entry information for diagnostics.
"""

import logging
from typing import Any, Dict

from homeassistant.config_entries import ConfigEntry  # type: ignore[import]

from .interface import ConfigurationDiagnosticsInterface

_LOGGER = logging.getLogger(__name__)


class ConfigurationDiagnosticsCollector(ConfigurationDiagnosticsInterface):
    """Handles collection of configuration diagnostics information.

    This class is responsible for gathering configuration entry details
    for diagnostic purposes. Follows Single Responsibility Principle by
    focusing only on configuration diagnostics collection.
    """

    def __init__(self):
        """Initialize the configuration diagnostics collector."""
        _LOGGER.debug("ConfigurationDiagnosticsCollector initialized")

    def collect_config_diagnostics(self, entry: ConfigEntry) -> Dict[str, Any]:
        """Collect configuration entry diagnostics.

        Gathers comprehensive information about the configuration entry
        including title, ID, data, and options for troubleshooting.

        Args:
            entry: Configuration entry to analyze.

        Returns:
            Dictionary containing configuration diagnostics.
        """
        try:
            _LOGGER.debug(
                "Collecting configuration diagnostics for '%s' (ID: %s)",
                entry.title,
                entry.entry_id,
            )

            config_diagnostics = {
                "title": entry.title,
                "entry_id": entry.entry_id,
                "data": dict(entry.data),
                "options": dict(entry.options),
                "version": getattr(entry, "version", None),
                "minor_version": getattr(entry, "minor_version", None),
                "domain": entry.domain,
                "source": getattr(entry, "source", None),
                "state": getattr(entry, "state", None),
                "unique_id": getattr(entry, "unique_id", None),
                "discovery_keys": getattr(entry, "discovery_keys", {}),
                "created_at": getattr(entry, "created_at", None),
                "modified_at": getattr(entry, "modified_at", None),
            }

            _LOGGER.debug(
                "Configuration diagnostics collected successfully for '%s'",
                entry.title,
            )

            return config_diagnostics

        except Exception as e:
            _LOGGER.error(
                "Error collecting configuration diagnostics for '%s': %s",
                getattr(
                    entry,
                    "title",
                    "Unknown",
                ),
                e,
                exc_info=True,
            )
            return {
                "error": "Failed to collect configuration diagnostics",
                "error_details": str(e),
            }
