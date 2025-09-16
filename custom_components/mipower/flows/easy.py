# custom_components/mipower/flows/easy.py
"""Easy setup flow: list device-level media_player devices that have a Bluetooth MAC.
Sets unique_id using the Bluetooth MAC and aborts if already configured.
"""

from __future__ import annotations

import logging
import voluptuous as vol
import re
from typing import List

from homeassistant import config_entries

from ..const import CONF_DEVICE_ID, CONF_MAC, CONF_NAME

_LOGGER = logging.getLogger(__name__)

MAC_RE = re.compile(r"([0-9A-Fa-f]{2}(?:[:\-]?)){5}[0-9A-Fa-f]{2}")


def _normalize_mac(raw: str | None) -> str | None:
    if not raw:
        return None
    m = MAC_RE.search(raw)
    if not m:
        return None
    return m.group(0).upper().replace("-", ":")


def _is_bluetooth_conn(conn) -> bool:
    if not isinstance(conn, (list, tuple)) or len(conn) < 2:
        return False
    typ = str(conn[0]).lower()
    return typ in ("bluetooth", "bt", "ble", "mac", "ble_address")


def _identifier_looks_like_bt(ident) -> bool:
    if isinstance(ident, (list, tuple)) and len(ident) >= 1:
        key = str(ident[0]).lower()
        if "androidtv" in key or "remote" in key or "bt" in key:
            return True
    if isinstance(ident, str):
        lk = ident.lower()
        if "androidtv" in lk or "remote" in lk or "bt" in lk:
            return True
    return False


def _get_devices_with_bluetooth_mac(hass) -> List[dict]:
    options = []
    try:
        from homeassistant.helpers import device_registry as dr, entity_registry as er
    except Exception:
        _LOGGER.exception("MiPower.easy: registry import edilemedi")
        return options

    er_reg = er.async_get(hass)
    dr_reg = dr.async_get(hass)

    debug_reasons = []

    for device in dr_reg.devices.values():
        device_id = device.id

        # require at least one media_player entity
        has_media = any(ent.entity_id.startswith("media_player.") and ent.device_id == device_id for ent in er_reg.entities.values())
        if not has_media:
            debug_reasons.append((device_id, "no_media_player"))
            continue

        bt_mac = None
        for conn in getattr(device, "connections", set()) or set():
            try:
                if _is_bluetooth_conn(conn):
                    candidate = _normalize_mac(conn[1])
                    if candidate:
                        bt_mac = candidate
                        break
            except Exception:
                continue

        if not bt_mac:
            for ident in getattr(device, "identifiers", set()) or set():
                try:
                    if _identifier_looks_like_bt(ident):
                        if isinstance(ident, (list, tuple)) and len(ident) >= 2:
                            candidate = _normalize_mac(ident[1])
                        else:
                            candidate = _normalize_mac(ident if isinstance(ident, str) else None)
                        if candidate:
                            bt_mac = candidate
                            break
                except Exception:
                    continue

        if not bt_mac:
            debug_reasons.append((device_id, "no_bt_mac"))
            continue

        label = device.name or f"device_{device_id}"
        options.append({"label": f"{label} — {bt_mac}", "value": device_id, "mac": bt_mac, "device_name": label})

    _LOGGER.debug("MiPower.easy: found %s candidate device(s). Debug reasons: %s", len(options), debug_reasons)
    return options


async def async_step(flow: config_entries.ConfigFlow, user_input=None):
    hass = flow.hass
    options = _get_devices_with_bluetooth_mac(hass)

    selector_builder = None
    try:
        from homeassistant.helpers.selector import selector  # type: ignore
        selector_builder = selector
    except Exception:
        selector_builder = None

    if user_input is None:
        if not options:
            _LOGGER.debug("MiPower.easy: no bluetooth-MAC devices found; options list empty")
            return flow.async_show_form(step_id="easy", data_schema=vol.Schema({}), errors={"base": "no_devices_with_bt_mac"})
        if selector_builder:
            sel_options = [{"label": o["label"], "value": o["value"]} for o in options]
            schema = vol.Schema({vol.Required(CONF_DEVICE_ID): selector_builder({"select": {"options": sel_options, "mode": "dropdown", "custom_value": False}})})
        else:
            mapping = {o["value"]: o["label"] for o in options}
            schema = vol.Schema({vol.Required(CONF_DEVICE_ID): vol.In(mapping)})
        _LOGGER.debug("MiPower.easy: showing easy form with %s options", len(options))
        return flow.async_show_form(step_id="easy", data_schema=schema)

    device_id = user_input.get(CONF_DEVICE_ID, "").strip()
    _LOGGER.debug("MiPower.easy: user submitted device_id=%s", device_id)
    if not device_id:
        return flow.async_show_form(step_id="easy", data_schema=vol.Schema({vol.Required(CONF_DEVICE_ID): str}), errors={"base": "invalid_selection"})

    selected = next((o for o in options if o["value"] == device_id), None)
    if not selected:
        _LOGGER.debug("MiPower.easy: selected device not in current options; re-resolving registry")
        options = _get_devices_with_bluetooth_mac(hass)
        selected = next((o for o in options if o["value"] == device_id), None)
        if not selected:
            _LOGGER.warning("MiPower.easy: device not found after re-resolve: %s", device_id)
            return flow.async_show_form(step_id="easy", data_schema=vol.Schema({vol.Required(CONF_DEVICE_ID): str}), errors={"base": "device_not_found"})

    mac = selected["mac"]
    device_name = selected["device_name"]
    display_name = f"MiPower - {device_name}"

    _LOGGER.debug("MiPower.easy: creating entry for device_id=%s mac=%s name=%s", device_id, mac, display_name)

    # set unique id (mac) so HA can dedupe & show options reliably
    try:
        # flow is a ConfigFlow instance: set unique id and abort if it already exists
        await flow.async_set_unique_id(mac)
        flow._abort_if_unique_id_configured()
    except Exception:
        _LOGGER.debug("MiPower.easy: unique_id set/abort step failed or duplicate exists")

    data = {
        CONF_DEVICE_ID: device_id,
        CONF_MAC: mac,
        CONF_NAME: display_name,
    }
    return flow.async_create_entry(title=display_name, data=data)
