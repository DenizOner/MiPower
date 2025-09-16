# custom_components/mipower/options_flow.py
"""Options flow for MiPower integration.
"""

from __future__ import annotations

import logging
import voluptuous as vol

from homeassistant import config_entries

from .const import DEFAULT_OFF_DEBOUNCE, CONF_DEVICE_ID, CONF_NAME, CONF_MAC

_LOGGER = logging.getLogger(__name__)


def _get_media_player_devices(hass):
    """Return list of dicts {'label','value'} for device registry devices that have media_player entities."""
    results = []
    try:
        from homeassistant.helpers import device_registry as dr, entity_registry as er
    except Exception:
        _LOGGER.exception("MiPower.options: registry import edilemedi")
        return results

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
        results.append({"label": f"{label} ({device.id})", "value": device.id})
        seen.add(ent.device_id)

    _LOGGER.debug("MiPower.options: found %s media_player device(s)", len(results))
    return results


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options for an existing config entry. All fields required."""

    def __init__(self) -> None:
        # Home Assistant will set self.config_entry
        self._logger = _LOGGER

    async def async_step_init(self, user_input=None):
        """Show options form and handle submission."""
        try:
            current = {}
            if self.config_entry is not None:
                current = self.config_entry.options or {}

            # discover media_player devices for the selector
            device_options = _get_media_player_devices(self.hass)
            sel_builder = None
            try:
                from homeassistant.helpers.selector import selector  # type: ignore
                sel_builder = selector
            except Exception:
                sel_builder = None

            # defaults (fallback to entry.data if options empty)
            defaults = {
                CONF_NAME: current.get(CONF_NAME, (self.config_entry.data.get(CONF_NAME) if self.config_entry else "")),
                CONF_MAC: current.get(CONF_MAC, (self.config_entry.data.get(CONF_MAC) if self.config_entry else "")),
                CONF_DEVICE_ID: current.get(CONF_DEVICE_ID, (self.config_entry.data.get(CONF_DEVICE_ID) if self.config_entry else "")),
                "off_debounce": current.get("off_debounce", DEFAULT_OFF_DEBOUNCE),
                "on_debounce": current.get("on_debounce", 0),
                "connect_timeout": current.get("connect_timeout", 5),
                "retry_interval": current.get("retry_interval", 5),
                "cleanup_on_unload": current.get("cleanup_on_unload", True),
            }

            # Build schema with selector if available and devices found
            if sel_builder and device_options:
                sel_opts = [{"label": o["label"], "value": o["value"]} for o in device_options]
                schema = vol.Schema(
                    {
                        vol.Required(CONF_NAME, default=defaults[CONF_NAME]): str,
                        vol.Required(CONF_MAC, default=defaults[CONF_MAC]): str,
                        vol.Required(CONF_DEVICE_ID, default=defaults[CONF_DEVICE_ID]): sel_builder(
                            {"select": {"options": sel_opts, "mode": "dropdown", "custom_value": False}}
                        ),
                        vol.Required("off_debounce", default=defaults["off_debounce"]): int,
                        vol.Required("on_debounce", default=defaults["on_debounce"]): int,
                        vol.Required("connect_timeout", default=defaults["connect_timeout"]): int,
                        vol.Required("retry_interval", default=defaults["retry_interval"]): int,
                        vol.Required("cleanup_on_unload", default=defaults["cleanup_on_unload"]): bool,
                    }
                )
            else:
                # Fallback: use list of device_ids (values) or free-form string if none
                mapping = {o["value"]: o["label"] for o in device_options} if device_options else {}
                device_field = (vol.In(list(mapping.keys())) if mapping else str)
                schema = vol.Schema(
                    {
                        vol.Required(CONF_NAME, default=defaults[CONF_NAME]): str,
                        vol.Required(CONF_MAC, default=defaults[CONF_MAC]): str,
                        vol.Required(CONF_DEVICE_ID, default=defaults[CONF_DEVICE_ID]): device_field,
                        vol.Required("off_debounce", default=defaults["off_debounce"]): int,
                        vol.Required("on_debounce", default=defaults["on_debounce"]): int,
                        vol.Required("connect_timeout", default=defaults["connect_timeout"]): int,
                        vol.Required("retry_interval", default=defaults["retry_interval"]): int,
                        vol.Required("cleanup_on_unload", default=defaults["cleanup_on_unload"]): bool,
                    }
                )

            if user_input is None:
                return self.async_show_form(step_id="init", data_schema=schema)

            errors = {}

            # Validate required string fields (non-empty)
            name = user_input.get(CONF_NAME)
            if not name or not str(name).strip():
                errors[CONF_NAME] = "required_field"

            mac = user_input.get(CONF_MAC)
            if not mac or not str(mac).strip():
                errors[CONF_MAC] = "required_field"

            device_id = user_input.get(CONF_DEVICE_ID)
            if not device_id or (isinstance(device_id, str) and not device_id.strip()):
                errors[CONF_DEVICE_ID] = "required_field"

            # Validate numeric fields are ints and non-negative
            for k in ("off_debounce", "on_debounce", "connect_timeout", "retry_interval"):
                val = user_input.get(k)
                if not isinstance(val, int):
                    errors[k] = "invalid_value"
                else:
                    if val < 0:
                        errors[k] = "invalid_value"

            # Validate cleanup_on_unload is bool
            cleanup_flag = user_input.get("cleanup_on_unload")
            if not isinstance(cleanup_flag, bool):
                errors["cleanup_on_unload"] = "required_field"

            if errors:
                return self.async_show_form(step_id="init", data_schema=schema, errors=errors)

            # Save options
            return self.async_create_entry(title="", data=user_input)

        except Exception as exc:
            _LOGGER.exception("MiPower.options_flow: unexpected error in async_step_init: %s", exc)
            return self.async_show_form(step_id="init", data_schema=vol.Schema({}), errors={"base": "unknown"})
