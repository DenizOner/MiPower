"""
Discovery utility functions for the MiPower integration.

This file provides helper functions that are used during the configuration flow
to find and identify relevant devices and entities for the user. This includes
finding Bluetooth-enabled media players and all media players in general.
"""

import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr, entity_registry as er

# Import constants from the main const.py file.
from ..const import BT_CONNECTION_TYPES, BT_IDENTIFIER_KEYWORDS, MAC_RE

# Set up a specific logger for this file.
_LOGGER = logging.getLogger(__name__)


def normalize_mac(raw: str | None) -> str | None:
    """
    Normalize a MAC address string to a standard format.

    This function takes a raw string, searches for a MAC address pattern within it,
    and returns the MAC address in a consistent format (uppercase with colons).

    Args:
        raw: The raw string that might contain a MAC address.

    Returns:
        The normalized MAC address string (e.g., "00:11:22:AA:BB:CC"),
        or None if no valid MAC address is found.
    """
    if not raw:
        return None
    # Use the pre-compiled regex to find a MAC address pattern.
    match = MAC_RE.search(raw)
    if not match:
        return None
    # Standardize the found MAC address (uppercase, colons).
    normalized = match.group(0).upper().replace("-", ":")
    _LOGGER.debug("Normalized MAC address '%s' to '%s'", raw, normalized)
    return normalized


def is_bluetooth_conn(conn: tuple[str, str]) -> bool:
    """
    Check if a device connection tuple represents a Bluetooth connection.

    Args:
        conn: A connection tuple from a Home Assistant device entry.
              Example: ('bluetooth', '00:11:22:AA:BB:CC')

    Returns:
        True if the connection type is a known Bluetooth type, False otherwise.
    """
    if not isinstance(conn, (list, tuple)) or len(conn) < 2:
        return False
    # The connection type is the first element of the tuple.
    conn_type = str(conn[0]).lower()
    # Check against our known BT types and the official HA BT connection type.
    is_bt = conn_type in BT_CONNECTION_TYPES + (dr.CONNECTION_BLUETOOTH,)
    _LOGGER.debug("Checking connection '%s': type is '%s', is_bt=%s", conn, conn_type, is_bt)
    return is_bt


def identifier_looks_like_bt(ident: Any) -> bool:
    """
    Check if a device identifier hints at it being a Bluetooth device.

    This is a fallback method used when a clear Bluetooth connection is not available.
    It checks if keywords like 'bluetooth' or 'bt' are present in the identifier.

    Args:
        ident: A device identifier from a Home Assistant device entry.

    Returns:
        True if the identifier suggests a Bluetooth device, False otherwise.
    """
    ident_str = str(ident).lower()
    # Check if any of our predefined keywords are in the identifier string.
    for keyword in BT_IDENTIFIER_KEYWORDS:
        if keyword in ident_str:
            _LOGGER.debug("Identifier '%s' looks like a BT device because it contains '%s'", ident, keyword)
            return True
    return False


async def get_bt_media_players(hass: HomeAssistant) -> dict[str, dict[str, str]]:
    """
    Get a dictionary of all Bluetooth-enabled media players.

    This function scans the device and entity registries to find devices that
    have a media_player entity and a discernible Bluetooth MAC address.

    Args:
        hass: The Home Assistant instance.

    Returns:
        A dictionary mapping MAC addresses to device data (name and entity_id).
        Example: {"00:11:22:AA:BB:CC": {"name": "My TV", "entity_id": "media_player.my_tv"}}
    """
    _LOGGER.debug("Starting discovery of Bluetooth media players.")
    device_registry = dr.async_get(hass)
    entity_registry = er.async_get(hass)

    bt_media_players = {}
    # Iterate over all devices registered in Home Assistant.
    for device in device_registry.devices.values():
        _LOGGER.debug("Processing device: %s (ID: %s)", device.name, device.id)
        media_player_entity_id = None
        # Find the media_player entity associated with this device.
        for entity in er.async_entries_for_device(entity_registry, device.id):
            if entity.domain == "media_player":
                media_player_entity_id = entity.entity_id
                _LOGGER.debug("Found media_player entity '%s' for device '%s'", entity.entity_id, device.name)
                break

        # If the device doesn't have a media_player entity, we're not interested in it.
        if not media_player_entity_id:
            _LOGGER.debug("Device '%s' has no media_player entity. Skipping.", device.name)
            continue

        # Attempt to find a Bluetooth MAC address for the device.
        mac = None
        # First, check the device's connections for a Bluetooth MAC.
        for conn in device.connections:
            if is_bluetooth_conn(conn) and (candidate := normalize_mac(conn[1])):
                mac = candidate
                _LOGGER.debug("Found BT MAC '%s' for device '%s' in connections.", mac, device.name)
                break
        # If not found in connections, check the device's identifiers as a fallback.
        if not mac:
            for ident in device.identifiers:
                if identifier_looks_like_bt(ident):
                    # The identifier itself might be the MAC or part of a tuple.
                    ident_val = ident[1] if isinstance(ident, (list, tuple)) and len(ident) >= 2 else str(ident)
                    if candidate := normalize_mac(ident_val):
                        mac = candidate
                        _LOGGER.debug("Found BT MAC '%s' for device '%s' in identifiers.", mac, device.name)
                        break

        # If a MAC address was successfully found, add the device to our results.
        if mac:
            _LOGGER.info("Found compatible BT media player: %s (MAC: %s)", device.name, mac)
            bt_media_players[mac] = {
                "name": device.name_by_user or device.name,
                "entity_id": media_player_entity_id,
            }
        else:
            _LOGGER.debug("Device '%s' is a media player but no BT MAC found. Skipping.", device.name)

    _LOGGER.debug("Finished discovery. Found %d BT media players.", len(bt_media_players))
    return bt_media_players


async def get_all_media_player_devices(hass: HomeAssistant) -> dict[str, str]:
    """
    Get a dictionary of all devices that have a media_player entity.

    This function is used in the "Advanced Setup" flow to provide a list of all
    possible media players, not just Bluetooth ones.

    Args:
        hass: The Home Assistant instance.

    Returns:
        A dictionary mapping device IDs to device names.
    """
    _LOGGER.debug("Getting all devices with a media_player entity.")
    devices = {}
    entity_registry = er.async_get(hass)
    device_registry = dr.async_get(hass)

    # Iterate over all entities in the entity registry.
    for entity in entity_registry.entities.values():
        # If the entity is a media_player and is linked to a device, process it.
        if entity.domain == "media_player" and entity.device_id:
            device = device_registry.async_get(entity.device_id)
            if device:
                # Use the user-assigned name if available, otherwise the default name.
                device_name = device.name_by_user or device.name
                devices[device.id] = device_name
                _LOGGER.debug("Found media_player device: %s (ID: %s)", device_name, device.id)

    _LOGGER.debug("Finished. Found %d total media_player devices.", len(devices))
    return devices