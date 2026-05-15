"""Discovery services for MiPower integration using SOLID principles."""

import logging
from typing import Any, Dict, List, Tuple

from homeassistant.core import HomeAssistant  # type: ignore[import]
from homeassistant.helpers import device_registry as dr  # type: ignore[import]
from homeassistant.helpers import entity_registry as er  # type: ignore[import]

from ..core.interfaces import IDeviceDiscovery
from ..models import DiscoveryConstants

_LOGGER = logging.getLogger(__name__)


class BluetoothDiscoveryService(IDeviceDiscovery):
    """Service for discovering Bluetooth-enabled media players."""

    def __init__(self) -> None:
        """Initialize the Bluetooth discovery service."""
        pass

    @staticmethod
    def normalize_mac(raw: str | None) -> str | None:
        """Normalize a MAC address string."""
        if not raw:
            return None
        match = DiscoveryConstants.MAC_RE.search(raw)
        if not match:
            return None
        normalized = match.group(0).upper().replace("-", ":")
        _LOGGER.debug("Normalized MAC address '%s' to '%s'", raw, normalized)
        return normalized

    @staticmethod
    def is_bluetooth_conn(conn: Tuple[str, str]) -> bool:
        """Check if a device connection represents a Bluetooth connection."""
        if len(conn) < 2:
            return False
        conn_type = str(conn[0]).lower()
        is_bt = conn_type in DiscoveryConstants.BT_CONNECTION_TYPES + (
            dr.CONNECTION_BLUETOOTH,
        )
        _LOGGER.debug(
            "Checking connection '%s': type is '%s', is_bt=%s", conn, conn_type, is_bt
        )
        return is_bt

    @staticmethod
    def identifier_looks_like_bt(ident: Any) -> bool:
        """Check if a device identifier hints at it being a Bluetooth device."""
        ident_str = str(ident).lower()
        for keyword in DiscoveryConstants.BT_IDENTIFIER_KEYWORDS:
            if keyword in ident_str:
                _LOGGER.debug(
                    "Identifier '%s' looks like a BT device because it contains '%s'",
                    ident,
                    keyword,
                )
                return True
        return False

    async def discover_devices(self, hass: HomeAssistant) -> Dict[str, Dict[str, str]]:
        """
        Discover Bluetooth-enabled media players.

        Returns:
            Dictionary mapping MAC addresses to device data.
        """
        _LOGGER.debug("Starting discovery of Bluetooth media players.")
        device_registry = dr.async_get(hass)
        entity_registry = er.async_get(hass)

        bt_media_players = {}
        for device in device_registry.devices.values():
            _LOGGER.debug("Processing device: %s (ID: %s)", device.name, device.id)
            media_player_entity_id = None
            for entity in er.async_entries_for_device(entity_registry, device.id):
                if entity.domain == "media_player":
                    media_player_entity_id = entity.entity_id
                    _LOGGER.debug(
                        "Found media_player entity '%s' for device '%s'",
                        entity.entity_id,
                        device.name,
                    )
                    break

            if not media_player_entity_id:
                _LOGGER.debug(
                    "Device '%s' has no media_player entity. Skipping.", device.name
                )
                continue

            mac = None
            # Check connections for Bluetooth MAC
            for conn in device.connections:
                if self.is_bluetooth_conn(conn) and (
                    candidate := self.normalize_mac(conn[1])
                ):
                    mac = candidate
                    _LOGGER.debug(
                        "Found BT MAC '%s' for device '%s' in connections.",
                        mac,
                        device.name,
                    )
                    break

            # Fallback to identifiers
            if not mac:
                for ident in device.identifiers:
                    if self.identifier_looks_like_bt(ident):
                        ident_val = (
                            ident[1]
                            if isinstance(ident, (List, Tuple)) and len(ident) >= 2
                            else str(ident)
                        )
                        if candidate := self.normalize_mac(ident_val):
                            mac = candidate
                            _LOGGER.debug(
                                "Found BT MAC '%s' for device '%s' in identifiers.",
                                mac,
                                device.name,
                            )
                            break

            if mac:
                _LOGGER.info(
                    "Found compatible BT media player: %s (MAC: %s)", device.name, mac
                )
                bt_media_players[mac] = {
                    "name": device.name_by_user or device.name,
                    "entity_id": media_player_entity_id,
                }
            else:
                _LOGGER.debug(
                    "Device '%s' is a media player but no BT MAC found. Skipping.",
                    device.name,
                )

        _LOGGER.debug(
            "Finished discovery. Found %d BT media players.", len(bt_media_players)
        )
        return bt_media_players


class MediaPlayerDiscoveryService(IDeviceDiscovery):
    """Service for discovering all media player devices."""

    async def discover_devices(self, hass: HomeAssistant) -> Dict[str, str]:
        """
        Discover all devices that have a media_player entity.

        Returns:
            Dictionary mapping device IDs to device names.
        """
        _LOGGER.debug("Getting all devices with a media_player entity.")
        devices = {}
        entity_registry = er.async_get(hass)
        device_registry = dr.async_get(hass)

        for entity in entity_registry.entities.values():
            if entity.domain == "media_player" and entity.device_id:
                device = device_registry.async_get(entity.device_id)
                if device:
                    device_name = device.name_by_user or device.name
                    devices[device.id] = device_name
                    _LOGGER.debug(
                        "Found media_player device: %s (ID: %s)", device_name, device.id
                    )

        _LOGGER.debug("Finished. Found %d total media_player devices.", len(devices))
        return devices
