# custom_components/mipower/switch.py
"""Switch platform entry: create entities from config entries."""

from __future__ import annotations

import logging
from typing import List, Optional

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import MiPowerSwitch

from .const import DOMAIN, CONF_MAC, CONF_NAME, CONF_DEVICE_ID

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    """Set up switch entities from a config entry."""
    _LOGGER.debug("MiPower.switch: async_setup_entry for %s", entry.entry_id)

    data = entry.data or {}
    options = entry.options or {}

    mac = data.get(CONF_MAC) or options.get(CONF_MAC)
    name = data.get(CONF_NAME) or options.get(CONF_NAME)
    device_id = data.get(CONF_DEVICE_ID) or options.get(CONF_DEVICE_ID)

    # Compose friendly name with prefix
    if not name:
        friendly = None
        try:
            if device_id:
                from homeassistant.helpers import device_registry as dr
                dr_reg = dr.async_get(hass)
                device = dr_reg.async_get(device_id)
                if device and getattr(device, "name", None):
                    friendly = device.name
            if not friendly and mac:
                friendly = mac
        except Exception:
            _LOGGER.debug("MiPower.switch: friendly name lookup hata", exc_info=True)
        if friendly:
            name = f"MiPower - {friendly}"
        else:
            name = f"MiPower_{(mac or '').replace(':','')[-6:]}"

    # get coordinator (must exist)
    coordinator = hass.data.get(DOMAIN, {}).get(entry.entry_id, {}).get("coordinator")

    entities: List[MiPowerSwitch] = []
    entities.append(MiPowerSwitch(hass, entry.entry_id, name, mac, device_id=device_id, coordinator=coordinator))

    async_add_entities(entities, True)
