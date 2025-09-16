# custom_components/mipower/diagnostics.py
"""Diagnostics helpers for MiPower (HA expects this file at root for Diagnostics menu)."""

from __future__ import annotations

from typing import Dict, Any
import logging
from pathlib import Path

_LOGGER = logging.getLogger(__name__)


async def async_get_integration_diagnostics(hass) -> Dict[str, Any]:
    """
    Integration-level diagnostics (called without a specific config entry).
    Provide general integration state and a preview of __pycache__.
    """
    try:
        from .helpers import cleanup_pycache as cp  # type: ignore
        integration_dir = Path(__file__).parent
        try:
            previews = await hass.async_add_executor_job(list, cp._iter_pycache_dirs(integration_dir))
            previews = [str(p) for p in previews]
        except Exception:
            previews = "preview_failed"

        return {"mipower_integration": {"version": "1.0.5", "cleanup_preview": previews}}
    except Exception:
        _LOGGER.exception("MiPower.diagnostics(integration): unexpected error")
        return {"error": "diagnostics integration failed"}


async def async_get_config_entry_diagnostics(hass, config_entry) -> Dict[str, Any]:
    """Return diagnostics for a config entry (called when user clicks Diagnostics on an entry)."""
    try:
        from .helpers import cleanup_pycache as cp  # type: ignore
        from homeassistant.helpers import entity_registry as er, device_registry as dr

        er_reg = er.async_get(hass)
        dr_reg = dr.async_get(hass)

        entities = []
        for ent in er_reg.entities.values():
            if ent.config_entry_id == config_entry.entry_id:
                entities.append({"entity_id": ent.entity_id, "unique_id": ent.unique_id, "platform": ent.platform})

        device_info = {}
        if "device_id" in config_entry.data:
            device = dr_reg.async_get(config_entry.data.get("device_id"))
            if device:
                device_info = {
                    "name": getattr(device, "name", None),
                    "manufacturer": getattr(device, "manufacturer", None),
                    "model": getattr(device, "model", None),
                    "connections": list(getattr(device, "connections", [])),
                    "identifiers": list(getattr(device, "identifiers", [])),
                }

        integration_dir = Path(__file__).parent
        try:
            cleanup_preview = await hass.async_add_executor_job(list, cp._iter_pycache_dirs(integration_dir))
            cleanup_preview = [str(p) for p in cleanup_preview]
        except Exception:
            cleanup_preview = "preview_failed"

        return {
            "mipower_diagnostics": {
                "entry": dict(config_entry.data),
                "options": dict(config_entry.options),
                "entities": entities,
                "device_info": device_info,
                "cleanup_preview": cleanup_preview,
            }
        }
    except Exception:
        _LOGGER.exception("MiPower.diagnostics(entry): unexpected error")
        return {"error": "diagnostics failed"}
