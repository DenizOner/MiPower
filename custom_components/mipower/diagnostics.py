"""
Diagnostics support for the MiPower integration using SOLID principles.

This file implements diagnostics gathering following SOLID principles.
It uses dependency injection and proper separation of concerns.
"""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er

from .const import DOMAIN
from .coordinator import MiPowerCoordinator
from .services.discovery_service import (
    BluetoothDiscoveryService,
    MediaPlayerDiscoveryService,
)

_LOGGER = logging.getLogger(__name__)


class DiagnosticsService:
    """
    Service for gathering diagnostic information using SOLID principles.

    This class follows SOLID principles:
    - Single Responsibility: Only manages diagnostics gathering
    - Open-Closed: Can be extended without modification
    - Liskov Substitution: Can replace any diagnostics service
    - Interface Segregation: Uses minimal interfaces
    - Dependency Inversion: Depends on abstractions
    """

    def __init__(
        self,
        bt_discovery_service: BluetoothDiscoveryService | None = None,
        media_player_discovery_service: MediaPlayerDiscoveryService | None = None,
    ) -> None:
        """
        Initialize the diagnostics service with dependency injection.

        Args:
            bt_discovery_service: Bluetooth discovery service instance.
            media_player_discovery_service: Media player discovery service instance.
        """
        # Inject discovery services or create defaults
        self.bt_discovery = bt_discovery_service or BluetoothDiscoveryService()
        self.media_player_discovery = (
            media_player_discovery_service or MediaPlayerDiscoveryService()
        )

    async def gather_diagnostics(
        self, hass: HomeAssistant, entry: ConfigEntry
    ) -> dict[str, Any]:
        """
        Gather comprehensive diagnostic information.

        Args:
            hass: The Home Assistant instance.
            entry: The config entry for diagnostics.

        Returns:
            Dictionary containing diagnostic information.
        """
        _LOGGER.debug(
            "[%s (%s)] Gathering diagnostics.",
            entry.title,
            entry.entry_id,
        )

        # Retrieve core objects
        coordinator: MiPowerCoordinator = hass.data[DOMAIN][entry.entry_id]
        device_registry = dr.async_get(hass)
        entity_registry = er.async_get(hass)

        # Gather device and entity information
        device = device_registry.async_get_device(
            identifiers={(DOMAIN, entry.entry_id)}
        )
        related_entities = self._gather_entity_diagnostics(entity_registry, device)

        # Gather discovery information
        bt_devices = await self.bt_discovery.discover_devices(hass)
        all_devices = await self.media_player_discovery.discover_devices(hass)

        # Assemble diagnostics data
        return {
            "entry": {
                "title": entry.title,
                "data": dict(entry.data),
                "options": dict(entry.options),
            },
            "coordinator": {
                "data": coordinator.data,
                "last_update_success": coordinator.last_update_success,
            },
            "device": {
                "name": device.name if device else None,
                "manufacturer": device.manufacturer if device else None,
                "model": device.model if device else None,
                "connections": list(device.connections) if device else [],
                "identifiers": list(device.identifiers) if device else [],
                "entities": related_entities,
            },
            "discovery_results": {
                "bt_media_players_found": bt_devices,
                "all_media_players_found": all_devices,
            },
        }

    def _gather_entity_diagnostics(
        self, entity_registry: er.EntityRegistry, device: dr.DeviceEntry | None
    ) -> list[dict[str, Any]]:
        """
        Gather diagnostic information about entities.

        Args:
            entity_registry: The entity registry.
            device: The device entry.

        Returns:
            List of entity diagnostic information.
        """
        if not device:
            _LOGGER.warning("[Diagnostics] No device found for diagnostics.")
            return []

        _LOGGER.debug(
            "[Diagnostics] Found associated device: %s (%s)",
            device.name,
            device.id,
        )
        entities = er.async_entries_for_device(entity_registry, device.id)
        diagnostics = []

        for entity in entities:
            diagnostics.append(
                {
                    "entity_id": entity.entity_id,
                    "original_name": entity.original_name,
                    "disabled": entity.disabled,
                    "disabled_by": str(entity.disabled_by),
                }
            )

        _LOGGER.debug(
            "[Diagnostics] Found %d related entities for device '%s' (%s).",
            len(diagnostics),
            device.name,
            device.id,
        )
        return diagnostics


# Global instance for backward compatibility
_diagnostics_service = DiagnosticsService()


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """
    Return diagnostics for a specific config entry.

    This function uses the DiagnosticsService following SOLID principles.

    Args:
        hass: The Home Assistant instance.
        entry: The config entry for which to gather diagnostics.

    Returns:
        A dictionary containing the diagnostic information.
    """
    return await _diagnostics_service.gather_diagnostics(hass, entry)
