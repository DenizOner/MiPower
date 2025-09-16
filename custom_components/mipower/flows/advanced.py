# custom_components/mipower/flows/advanced.py
"""Advanced setup flow: require device selection and full fields (all required).
Sets unique_id using MAC if available.
"""

from __future__ import annotations

import logging
import re
import voluptuous as vol

from homeassistant import config_entries

from ..const import CONF_NAME, CONF_MAC, CONF_DEVICE_ID, DEFAULT_OFF_DEBOUNCE

_LOGGER = logging.getLogger(__name__)

MAC_RE = re.compile(r"([0-9A-Fa-f]{2}(?:[:\-]?)){5}[0-9A-Fa-f]{2}")


def _norm_mac(raw: str | None) -> str | None:
    if not raw:
        return None
    m = MAC_RE.search(raw)
    if not m:
        return None
    return m.group(0).upper().replace("-", ":")


def _get_all_media_player_devices(hass) -> list[dict]:
    options = []
    try:
        from homeassistant.helpers import device_registry as dr, entity_registry as er
    except Exception:
        _LOGGER.exception("MiPower.advanced: registry import edilemedi")
        return options

    er_reg = er.async_get(hass)
    dr_reg = dr.async_get(hass)

    seen = set()
    for ent in er_reg.entities.values():
        if not ent.entity_id.startswith("media_player."):
            continue
        if not ent.device_id:
            continue
        if ent.device_id in seen:
            continue
        device = dr_reg.async_get(ent.device_id)
        if not device:
            continue
        label = device.name or f"device_{device.id}"
        options.append({"label": f"{label} ({device.id})", "value": device.id})
        seen.add(device.id)

    _LOGGER.debug("MiPower.advanced: found %s media_player devices", len(options))
    return options


async def async_step(flow: config_entries.ConfigFlow, user_input=None):
    hass = flow.hass
    device_options = _get_all_media_player_devices(hass)

    selector_builder = None
    try:
        from homeassistant.helpers.selector import selector  # type: ignore
        selector_builder = selector
    except Exception:
        selector_builder = None

    # Build schema with all fields REQUIRED
    if selector_builder and device_options:
        sel_opts = [{"label": o["label"], "value": o["value"]} for o in device_options]
        schema = vol.Schema(
            {
                vol.Required(CONF_DEVICE_ID): selector_builder({"select": {"options": sel_opts, "mode": "dropdown", "custom_value": False}}),
                vol.Required(CONF_NAME, default=""): str,
                vol.Required(CONF_MAC, default=""): str,
                vol.Required("off_debounce", default=DEFAULT_OFF_DEBOUNCE): int,
                vol.Required("connect_failure_threshold", default=3): int,
            }
        )
    else:
        schema = vol.Schema(
            {
                vol.Required(CONF_DEVICE_ID): str,
                vol.Required(CONF_NAME, default=""): str,
                vol.Required(CONF_MAC, default=""): str,
                vol.Required("off_debounce", default=DEFAULT_OFF_DEBOUNCE): int,
                vol.Required("connect_failure_threshold", default=3): int,
            }
        )

    if user_input is None:
        _LOGGER.debug("MiPower.advanced: showing advanced form")
        return flow.async_show_form(step_id="advanced", data_schema=schema)

    # Validate required fields presence
    device_id = user_input.get(CONF_DEVICE_ID, "").strip()
    name = user_input.get(CONF_NAME, "").strip()
    mac_raw = user_input.get(CONF_MAC, "").strip()
    off_debounce = int(user_input.get("off_debounce", DEFAULT_OFF_DEBOUNCE))
    connect_failure_threshold = int(user_input.get("connect_failure_threshold", 3))

    if not device_id:
        return flow.async_show_form(step_id="advanced", data_schema=schema, errors={"base": "device_required"})
    if not name:
        return flow.async_show_form(step_id="advanced", data_schema=schema, errors={"base": "name_required"})
    mac = _norm_mac(mac_raw)
    if not mac:
        # try auto-resolve from device registry
        try:
            from homeassistant.helpers import device_registry as dr
            dr_reg = dr.async_get(hass)
            device = dr_reg.async_get(device_id)
            if device:
                for conn in getattr(device, "connections", set()) or set():
                    if isinstance(conn, (list, tuple)) and len(conn) >= 2 and str(conn[0]).lower() in ("bluetooth", "bt", "mac"):
                        candidate = _norm_mac(conn[1])
                        if candidate:
                            mac = candidate
                            break
        except Exception:
            _LOGGER.exception("MiPower.advanced: device lookup hata")
    if not mac:
        return flow.async_show_form(step_id="advanced", data_schema=schema, errors={"mac": "required"})

    # set unique id to mac to dedupe and allow options to appear reliably
    try:
        await flow.async_set_unique_id(mac)
        flow._abort_if_unique_id_configured()
    except Exception:
        _LOGGER.debug("MiPower.advanced: unique_id set/abort step failed or duplicate exists")

    data = {
        CONF_DEVICE_ID: device_id,
        CONF_MAC: mac,
        CONF_NAME: name,
        "off_debounce": off_debounce,
        "connect_failure_threshold": connect_failure_threshold,
    }

    _LOGGER.debug("MiPower.advanced: creating entry for device_id=%s mac=%s name=%s", device_id, mac, name)
    return flow.async_create_entry(title=name, data=data)
