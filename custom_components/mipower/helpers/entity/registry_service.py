"""
Entity Registry Service - Single Responsibility Principle

This module implements entity registry operations following SOLID principles,
handling entity registry access and entity lookup functionality.
Follows pure dependency injection pattern.
"""

import logging
from typing import Any, List

from homeassistant.core import HomeAssistant  # type: ignore[import]
from homeassistant.helpers import entity_registry as er  # type: ignore[import]

from ...helpers.errors.exceptions import EntityRegistryError
from .registry_interface import EntityRegistryInterface

_LOGGER = logging.getLogger(__name__)


class EntityRegistryService(EntityRegistryInterface):
    """Handles entity registry operations with error handling and logging.

    This class is responsible for accessing the Home Assistant entity registry
    and performing entity-related operations. Follows Single Responsibility
    Principle by focusing only on entity registry operations.
    Uses dependency injection for Home Assistant instance.
    """

    def __init__(self, hass: HomeAssistant):
        """Initialize the entity registry service.

        Args:
            hass: Home Assistant instance
        """
        self.hass = hass
        _LOGGER.debug("EntityRegistryService initialized")

    def get_entity_registry(self, hass: HomeAssistant) -> Any:
        """Get the Home Assistant entity registry.

        Args:
            hass: Home Assistant instance.

        Returns:
            Entity registry instance.

        Raises:
            RuntimeError: If accessing the registry fails.
        """
        try:
            registry = er.async_get(hass)
            _LOGGER.debug("Entity registry accessed successfully")
            return registry
        except Exception as e:
            _LOGGER.error(
                "Failed to access entity registry: %s",
                e,
                exc_info=True,
            )
            raise EntityRegistryError(f"Failed to access entity registry: {e}")

    def get_entities_for_device(self, hass: HomeAssistant, device_id: str) -> List[Any]:
        """Get all entities associated with a specific device.

        Args:
            hass: Home Assistant instance.
            device_id: The device ID to get entities for.

        Returns:
            List of entity entries for the device, empty list on error.
        """
        try:
            entity_registry = self.get_entity_registry(hass)
            entities = er.async_entries_for_device(
                entity_registry, device_id, include_disabled_entities=False
            )

            _LOGGER.debug("Found %d entities for device %s", len(entities), device_id)

            return entities

        except Exception as e:
            _LOGGER.error(
                "Error getting entities for device %s: %s",
                device_id,
                e,
                exc_info=True,
            )
            return []
