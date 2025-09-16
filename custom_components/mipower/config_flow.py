# custom_components/mipower/config_flow.py
"""Main config flow for MiPower. Provides the ConfigFlow class and module-level async_get_options_flow
so Home Assistant reliably finds the options flow (this is important for the Options (dişli) button).

Updated to avoid passing config_entry into OptionsFlowHandler constructor (deprecated).
"""

from __future__ import annotations

import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class MiPowerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Main config flow orchestration class."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Show first form to choose easy / advanced."""
        try:
            if user_input is None:
                schema = vol.Schema(
                    {
                        vol.Required("mode", default="easy"): vol.In(
                            {"easy": "Kolay kurulum", "advanced": "Gelişmiş kurulum"}
                        )
                    }
                )
                return self.async_show_form(step_id="user", data_schema=schema)

            mode = user_input.get("mode")
            if mode == "easy":
                return await self.async_step_easy()
            return await self.async_step_advanced()
        except Exception as exc:
            _LOGGER.exception("MiPower: config flow orchestrator hata: %s", exc)
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({vol.Required("mode", default="easy"): vol.In({"easy": "Kolay", "advanced": "Gelişmiş"})}),
                errors={"base": "unknown"},
            )

    async def async_step_easy(self, user_input=None):
        """Delegate to flows.easy."""
        try:
            from .flows import easy as easy_flow  # type: ignore
            return await easy_flow.async_step(self, user_input)
        except Exception:
            _LOGGER.exception("MiPower: easy flow import/çalıştırma hatası")
            return self.async_show_form(step_id="easy", data_schema=vol.Schema({}), errors={"base": "unknown"})

    async def async_step_advanced(self, user_input=None):
        """Delegate to flows.advanced."""
        try:
            from .flows import advanced as adv_flow  # type: ignore
            return await adv_flow.async_step(self, user_input)
        except Exception:
            _LOGGER.exception("MiPower: advanced flow import/çalıştırma hatası")
            return self.async_show_form(step_id="advanced", data_schema=vol.Schema({}), errors={"base": "unknown"})

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """
        Staticmethod on the ConfigFlow class itself — Home Assistant may call this directly.
        Return an OptionsFlowHandler instance tied to the provided config_entry.

        IMPORTANT: Do NOT pass config_entry into the OptionsFlowHandler constructor.
        Return OptionsFlowHandler() and let HA populate self.config_entry.
        """
        try:
            from .options_flow import OptionsFlowHandler  # type: ignore
            return OptionsFlowHandler()
        except Exception:
            _LOGGER.exception("MiPower: OptionsFlowHandler import edilemedi (fallback kullanılacak)")

            class FallbackOptions(config_entries.OptionsFlow):
                def __init__(self):
                    self._cfg = None

                async def async_step_init(self, user_input=None):
                    if user_input is None:
                        schema = vol.Schema({vol.Optional("off_debounce", default=8): int})
                        return self.async_show_form(step_id="init", data_schema=schema)
                    return self.async_create_entry(title="", data=user_input)

            return FallbackOptions()


@callback
def async_get_options_flow(config_entry):
    """
    Module-level callback Home Assistant uses to get the options flow handler.
    We keep this too (redundancy) to maximize compatibility with different HA versions.

    IMPORTANT: return OptionsFlowHandler() (no constructor argument).
    """
    try:
        from .options_flow import OptionsFlowHandler  # type: ignore
        return OptionsFlowHandler()
    except Exception:
        _LOGGER.exception("MiPower: options flow import edilemedi; fallback kullanılacak")

        class FallbackOptions(config_entries.OptionsFlow):
            def __init__(self):
                self._cfg = None

            async def async_step_init(self, user_input=None):
                if user_input is None:
                    schema = vol.Schema({vol.Optional("off_debounce", default=8): int})
                    return self.async_show_form(step_id="init", data_schema=schema)
                return self.async_create_entry(title="", data=user_input)

        return FallbackOptions()
