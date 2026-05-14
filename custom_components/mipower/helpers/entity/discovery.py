"""Entity discovery service for Smartify integration.

Handles automatic discovery and registration of entities in Home Assistant.
Follows SOLID principles with dependency injection and interface implementation.
"""

import logging
from typing import Any, Dict, List, Optional

from homeassistant.helpers.entity_registry import EntityRegistry  # type: ignore[import]

from .discovery_interface import EntityDiscoveryInterface

_LOGGER = logging.getLogger(__name__)


class EntityDiscoveryService(EntityDiscoveryInterface):
    """Service for discovering and managing entities.

    Implements EntityDiscoveryInterface following SOLID principles.
    Provides entity discovery, registration, and management operations.
    """

    def __init__(self, entity_registry: EntityRegistry):
        """Initialize the entity discovery service.

        Args:
            entity_registry: Home Assistant entity registry instance
        """
        self._entity_registry = entity_registry

    def discover_entities(
        self, domain: str, device_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Discover entities for a given domain and device.

        Args:
            domain: Entity domain (e.g., 'sensor', 'switch')
            device_id: Optional device ID to filter

        Returns:
            List of discovered entity information
        """
        entities = []
        for entity_entry in self._entity_registry.entities.values():
            if entity_entry.domain == domain:
                if device_id is None or entity_entry.device_id == device_id:
                    entities.append(
                        {
                            "entity_id": entity_entry.entity_id,
                            "name": entity_entry.name,
                            "device_id": entity_entry.device_id,
                            "disabled": entity_entry.disabled,
                        }
                    )
        return entities

    def register_entity(
        self,
        entity_id: str,
        config_entry_id: str,
        device_id: Optional[str] = None,
    ) -> None:
        """Register an entity in the registry.

        Args:
            entity_id: Entity ID
            config_entry_id: Configuration entry ID
            device_id: Optional device ID
        """
        self._entity_registry.async_get_or_create(
            entity_id=entity_id,
            config_entry_id=config_entry_id,
            device_id=device_id,
        )

    def disable_entity(self, entity_id: str) -> None:
        """Disable an entity.

        Args:
            entity_id: Entity ID to disable
        """
        self._entity_registry.async_update_entity(entity_id, disabled=True)

    def enable_entity(self, entity_id: str) -> None:
        """Enable an entity.

        Args:
            entity_id: Entity ID to enable
        """
        self._entity_registry.async_update_entity(entity_id, disabled=False)


def find_switch_for_power_entity(hass, power_entity_id: str) -> Optional[str]:
    """Find switch entity associated with a power sensor entity.

    Looks for a switch entity that is likely controlling the same device
    as the given power sensor. This is done by finding switches that share
    the same device or have similar naming patterns.

    Args:
        hass: Home Assistant instance
        power_entity_id: Power sensor entity ID

    Returns:
        Switch entity ID if found, None otherwise
    """
    try:
        from homeassistant.helpers import device_registry as dr  # type: ignore[import]
        from homeassistant.helpers import entity_registry as er  # type: ignore[import]

        entity_registry = er.async_get(hass)
        device_registry = dr.async_get(hass)

        # Get power entity entry
        power_entry = entity_registry.async_get(power_entity_id)
        if not power_entry or not power_entry.device_id:
            return None

        # Get device info
        device = device_registry.async_get(power_entry.device_id)
        if not device:
            return None

        # Look for switches associated with the same device
        for entity_entry in entity_registry.entities.values():
            if (
                entity_entry.domain == "switch"
                and entity_entry.device_id == power_entry.device_id
            ):
                return entity_entry.entity_id

        # Fallback: Look for switches with similar names in same area
        power_area = device.area_id
        power_name = power_entry.name or power_entity_id.split(".")[-1]

        for entity_entry in entity_registry.entities.values():
            if entity_entry.domain == "switch":
                switch_device = device_registry.async_get(entity_entry.device_id)
                if (
                    switch_device
                    and switch_device.area_id == power_area
                    and power_name.lower() in (entity_entry.name or "").lower()
                ):
                    return entity_entry.entity_id

        return None
    except Exception as e:
        _LOGGER.error(
            "Error finding switch for power entity %s: %s",
            power_entity_id,
            e,
            exc_info=True,
        )
        return None
