"""
Entity Diagnostics Collector - Single Responsibility Principle

This module implements entity diagnostics functionality following SOLID principles,
handling collection of entity information for diagnostics.
"""

import logging
from typing import Any, Dict, List

from homeassistant.config_entries import ConfigEntry  # type: ignore[import]
from homeassistant.core import HomeAssistant  # type: ignore[import]
from homeassistant.helpers import entity_registry as er  # type: ignore[import]

from .interface import EntityDiagnosticsInterface

_LOGGER = logging.getLogger(__name__)


class EntityDiagnosticsCollector(EntityDiagnosticsInterface):
    """Handles collection of entity diagnostics information.

    This class is responsible for gathering information about entities
    associated with a configuration entry for diagnostic purposes.
    Follows Single Responsibility Principle by focusing only on entity diagnostics.
    """

    def __init__(self):
        """Initialize the entity diagnostics collector."""
        _LOGGER.debug("EntityDiagnosticsCollector initialized")

    async def collect_entity_diagnostics(
        self, hass: HomeAssistant, entry: ConfigEntry
    ) -> List[Dict[str, Any]]:
        """Collect entity diagnostics information.

        Gathers comprehensive information about all entities associated
        with the configuration entry including their states and attributes.

        Args:
            hass: Home Assistant instance.
            entry: Configuration entry.

        Returns:
            List of dictionaries containing entity diagnostics.
        """
        try:
            _LOGGER.debug(
                "Collecting entity diagnostics for '%s' (ID: %s)",
                entry.title,
                entry.entry_id,
            )

            entity_registry = er.async_get(hass)
            entities = er.async_entries_for_config_entry(
                entity_registry, entry.entry_id
            )

            _LOGGER.debug(
                "Found %d entities associated with configuration entry '%s'",
                len(entities),
                entry.title,
            )

            entity_diagnostics = []

            for entity_entry in entities:
                _LOGGER.debug(
                    "Processing entity: %s (Domain: %s)",
                    entity_entry.entity_id,
                    entity_entry.domain,
                )

                try:
                    state = hass.states.get(entity_entry.entity_id)
                    entity_info = {
                        "entity_id": entity_entry.entity_id,
                        "domain": entity_entry.domain,
                        "unique_id": entity_entry.unique_id,
                        "original_name": entity_entry.original_name,
                        "disabled": entity_entry.disabled,
                        "disabled_by": entity_entry.disabled_by,
                        "state": state.state if state else None,
                        "attributes": dict(state.attributes) if state else {},
                        "last_changed": (
                            getattr(state, "last_changed", None) if state else None
                        ),
                        "last_updated": (
                            getattr(state, "last_updated", None) if state else None
                        ),
                    }
                    entity_diagnostics.append(entity_info)

                    _LOGGER.debug(
                        "Entity '%s' added to diagnostics report",
                        entity_entry.entity_id,
                    )

                except Exception as entity_error:
                    _LOGGER.error(
                        "Error processing entity '%s': %s",
                        entity_entry.entity_id,
                        entity_error,
                        exc_info=True,
                    )
                    # Add error information for this entity
                    entity_diagnostics.append(
                        {
                            "entity_id": entity_entry.entity_id,
                            "domain": entity_entry.domain,
                            "error": "Failed to collect entity information",
                            "error_details": str(entity_error),
                        }
                    )
                    continue

            _LOGGER.debug(
                "Entity diagnostics collected successfully for '%s' (%d entities)",
                entry.title,
                len(entity_diagnostics),
            )

            return entity_diagnostics

        except Exception as e:
            _LOGGER.error(
                "Error collecting entity diagnostics for '%s': %s",
                getattr(
                    entry,
                    "title",
                    "Unknown",
                ),
                e,
                exc_info=True,
            )
            return [
                {
                    "error": "Failed to collect entity diagnostics",
                    "error_details": str(e),
                }
            ]
