# custom_components/mipower/__init__.py
"""MiPower integration - setup, per-entry coordinator, device registration and automatic cleanup handling.
Also export async_get_options_flow at package level so frontend reliably sees the Options gear.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, DEFAULT_OFF_DEBOUNCE, CONF_MAC, CONF_NAME

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the integration (root)."""
    _LOGGER.debug("MiPower: async_setup")
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """
    Set up a config entry:
     - create a DataUpdateCoordinator per entry
     - register a cleanup service
     - ensure default options exist (cleanup_on_unload default = True)
     - create device registry entry if mac available
     - forward setup to platforms (switch)
    """
    _LOGGER.debug("MiPower: async_setup_entry %s", entry.entry_id)

    hass.data.setdefault(DOMAIN, {})

    # Ensure default options exist
    try:
        if not entry.options:
            defaults = {
                "off_debounce": DEFAULT_OFF_DEBOUNCE,
                "connect_failure_threshold": 3,
                "cleanup_on_unload": True,
            }
            hass.config_entries.async_update_entry(entry, options=defaults)
            _LOGGER.debug("MiPower: default options set for entry %s: %s", entry.entry_id, defaults)
    except Exception:
        _LOGGER.exception("MiPower: could not set default options")

    # Create per-entry coordinator (minimal)
    async def async_update_data() -> dict[str, Any]:
        return {"entry_id": entry.entry_id, "data": dict(entry.data)}

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f"MiPower coordinator {entry.entry_id}",
        update_method=async_update_data,
    )
    await coordinator.async_refresh()

    hass.data[DOMAIN][entry.entry_id] = {"coordinator": coordinator, "entry": entry}

    # Register cleanup service (wrapper around helper)
    try:
        from .helpers import cleanup_pycache as cp  # type: ignore

        async def _svc_cleanup(call):
            await hass.async_add_executor_job(cp.cleanup_pycache, Path(__file__).parent)

        try:
            hass.services.async_register(DOMAIN, "cleanup_pycache", _svc_cleanup)
            _LOGGER.debug("MiPower: registered service mipower.cleanup_pycache")
        except Exception:
            _LOGGER.exception("MiPower: failed to async_register service (continuing)")
    except Exception:
        _LOGGER.exception("MiPower: could not register cleanup service (helper import failed)")

    # Create/ensure device registry entry linked to this config entry (improves UI)
    try:
        mac = entry.data.get(CONF_MAC) or entry.options.get(CONF_MAC)
        name = entry.data.get(CONF_NAME) or entry.options.get(CONF_NAME) or f"MiPower {entry.entry_id}"
        if mac:
            try:
                from homeassistant.helpers import device_registry as dr
                dr_reg = dr.async_get(hass)
                identifiers = {(DOMAIN, mac.upper())}
                device = dr_reg.async_get_or_create(
                    config_entry_id=entry.entry_id,
                    identifiers=identifiers,
                    manufacturer="MiPower Project",
                    model="MiPower",
                    name=name,
                )
                _LOGGER.debug("MiPower: device registry entry created/ensured %s -> %s", entry.entry_id, device.id)
            except Exception:
                _LOGGER.exception("MiPower: device registry create failed")
    except Exception:
        _LOGGER.exception("MiPower: device registry block failed")

    # Forward to platforms (switch)
    try:
        await hass.config_entries.async_forward_entry_setups(entry, ["switch"])
    except Exception:
        _LOGGER.exception("MiPower: forward_entry_setup(switch) sırasında hata")

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """
    Unload and optionally cleanup:
     - Unload platforms
     - If options.cleanup_on_unload True -> perform automatic cleanup (A-only)
     - Otherwise create persistent notification guiding user to manual cleanup service
    """
    _LOGGER.debug("MiPower: async_unload_entry %s", entry.entry_id)

    try:
        unloaded = await hass.config_entries.async_forward_entry_unload(entry, "switch")
    except Exception:
        _LOGGER.exception("MiPower: forward_entry_unload(switch) sırasında hata")
        unloaded = False

    # cleanup behavior (A-only if enabled)
    try:
        from .helpers import cleanup_pycache as cp  # type: ignore
        integration_dir = Path(__file__).parent
        cleanup_flag = entry.options.get("cleanup_on_unload", True)
        if cleanup_flag:
            _LOGGER.debug("MiPower: cleanup_on_unload true, cleaning __pycache__ (automatic)")
            await hass.async_add_executor_job(cp.cleanup_pycache, integration_dir)
        else:
            try:
                from homeassistant.components.persistent_notification import async_create as pn_create

                pn_create(
                    hass,
                    f"MiPower: config entry '{entry.title}' removed. To cleanup cached files, call the service mipower.cleanup_pycache from Developer Tools → Services.",
                    title="MiPower: cleanup available",
                )
            except Exception:
                _LOGGER.debug("MiPower: could not create persistent notification")
    except Exception:
        _LOGGER.exception("MiPower: cleanup attempt failed or module missing")

    # remove coordinator from hass.data if present
    try:
        hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
    except Exception:
        pass

    return unloaded


# --- Export config_flow's async_get_options_flow at package level ---------------------
# Keep this as extra redundancy; earlier we added package-level export to help frontend find it.

try:
    from . import config_flow as _config_flow_module  # type: ignore

    if hasattr(_config_flow_module, "async_get_options_flow"):
        async_get_options_flow = getattr(_config_flow_module, "async_get_options_flow")
        _LOGGER.debug("MiPower: exported async_get_options_flow at package level")
    else:
        _LOGGER.debug("MiPower: config_flow module has no async_get_options_flow to export")
except Exception:
    _LOGGER.exception("MiPower: failed to import config_flow for exporting async_get_options_flow")
