"""
Diagnostics support for the MiPower integration.

This file is responsible for gathering and returning diagnostic information about
the integration and its associated devices. When a user clicks "Download Diagnostics"
on the integration's entry, Home Assistant calls the `async_get_config_entry_diagnostics`
function in this file. The data returned is crucial for troubleshooting user issues.
"""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr, entity_registry as er

# Import constants and the coordinator from within the integration.
from .const import DOMAIN
from .coordinator import MiPowerCoordinator

# Set up a specific logger for this file.
_LOGGER = logging.getLogger(__name__)


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """
    Return diagnostics for a specific config entry.

    This function gathers a comprehensive set of data related to the config entry,
    including its configuration, the state of the coordinator, details about the
    associated device and its entities, and the results of discovery scans.

    Args:
        hass: The Home Assistant instance.
        entry: The config entry for which to gather diagnostics.

    Returns:
        A dictionary containing the diagnostic information.
    """
    _LOGGER.debug("Gathering diagnostics for entry_id: %s", entry.entry_id)

    # We import discovery functions here locally to avoid potential circular dependencies.
    from .api.discovery import get_all_media_player_devices, get_bt_media_players

    # --- Retrieve Core Objects ---
    # Get the coordinator instance associated with this config entry.
    coordinator: MiPowerCoordinator = hass.data[DOMAIN][entry.entry_id]
    _LOGGER.debug("Retrieved coordinator for diagnostics.")

    # Get the device and entity registry instances.
    device_registry = dr.async_get(hass)
    entity_registry = er.async_get(hass)
    _LOGGER.debug("Retrieved device and entity registries.")

    # --- Gather Device and Entity Information ---
    # Find the device associated with this config entry using its unique identifier.
    device = device_registry.async_get_device(identifiers={(DOMAIN, entry.entry_id)})

    related_entities_diagnostics = []
    if device:
        _LOGGER.debug("Found associated device: %s", device.name)
        # If a device is found, gather information about all entities linked to it.
        entities = er.async_entries_for_device(entity_registry, device.id)
        for entity in entities:
            related_entities_diagnostics.append(
                {
                    "entity_id": entity.entity_id,
                    "original_name": entity.original_name,
                    "disabled": entity.disabled,
                    "disabled_by": str(entity.disabled_by),  # Convert enum to string
                }
            )
        _LOGGER.debug(
            "Found %d related entities for device '%s'.",
            len(related_entities_diagnostics),
            device.name,
        )
    else:
        _LOGGER.warning("No associated device found for entry_id: %s", entry.entry_id)

    # --- Gather Discovery Information ---
    # Run the discovery functions to see what devices the integration can currently see.
    # This is very useful for debugging setup issues.
    _LOGGER.debug("Running discovery functions for diagnostics.")
    bt_media_players_found = await get_bt_media_players(hass)
    all_media_players_found = await get_all_media_player_devices(hass)
    _LOGGER.debug(
        "Discovery found %d BT media players and %d total media players.",
        len(bt_media_players_found),
        len(all_media_players_found),
    )

    # --- Assemble Final Diagnostics Dictionary ---
    # This dictionary is serialized to JSON and downloaded by the user.
    # It's structured to be easily readable and provide a complete picture.
    diagnostics_data = {
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
            "entities": related_entities_diagnostics,
        },
        "discovery_results": {
            "bt_media_players_found": bt_media_players_found,
            "all_media_players_found": all_media_players_found,
        },
    }
    _LOGGER.debug("Finished gathering diagnostics.")
    return diagnostics_data
