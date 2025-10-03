# This file is responsible for defining the options flow for the MiPower integration.
# The options flow allows users to re-configure the integration after it has already been set up.
# For example, users can tweak timing settings for the Bluetooth commands.

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_MAC
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.selector import NumberSelector, NumberSelectorConfig, NumberSelectorMode

# Import constants from the const.py file to ensure consistency across the integration.
from ..const import (
    CONF_MEDIA_PLAYER_ENTITY_ID,
    CONF_ON_DEBOUNCE,
    CONF_OFF_DEBOUNCE,
    CONF_INTER_STEP_DELAY,
    CONF_PAIR_TIMEOUT,
    CONF_SPAWN_TIMEOUT,
    CONF_TRUST_TIMEOUT,
    CONF_SCAN_DURATION,
    DEFAULT_ON_DEBOUNCE_SECONDS,
    DEFAULT_OFF_DEBOUNCE_SECONDS,
    DEFAULT_INTER_STEP_DELAY,
    DEFAULT_PAIR_TIMEOUT,
    DEFAULT_SPAWN_TIMEOUT,
    DEFAULT_TRUST_TIMEOUT,
    DEFAULT_SCAN_DURATION,
    RANGE_ON_DEBOUNCE,
    RANGE_OFF_DEBOUNCE,
    TIMEOUT_RANGE,
    INTER_STEP_DELAY_RANGE,
    SCAN_DURATION_RANGE,
)

# Set up a specific logger for this file, allowing for targeted debugging.
_LOGGER = logging.getLogger(__name__)

class MiPowerOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle the options flow for the MiPower integration."""

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """
        Manage the options for the integration.
        This is the primary step of the options flow, where the user can view and edit settings.
        """
        _LOGGER.debug("[Options Flow] Entering async_step_init. User input: %s", user_input)

        # This block is executed when the user submits the form with new settings.
        if user_input is not None:
            _LOGGER.debug("[Options Flow] User submitted new options: %s", user_input)
            # `async_create_entry` saves the user's input into the `options` dictionary
            # of the config entry and finishes the flow.
            return self.async_create_entry(title="", data=user_input)

        _LOGGER.debug("[Options Flow] No user input, preparing to show the form.")

        # --- Gather data for description placeholders ---
        # These placeholders are used to display dynamic information in the form's description.
        media_player_entity_id = self.config_entry.data.get(CONF_MEDIA_PLAYER_ENTITY_ID)
        mac_address = self.config_entry.data.get(CONF_MAC)
        _LOGGER.debug("[Options Flow] Media player entity ID: %s, MAC: %s", media_player_entity_id, mac_address)

        # Get the entity registry to find more details about the linked media player.
        entity_registry = er.async_get(self.hass)
        media_player_entry = entity_registry.async_get(media_player_entity_id)
        
        # Determine the friendly name of the media player to show to the user.
        media_player_name = "Unknown Media Player"
        if media_player_entry:
            # Use the user-assigned name, or the original name, or the entity ID as a fallback.
            media_player_name = media_player_entry.name or media_player_entry.original_name or media_player_entity_id
            _LOGGER.debug("[Options Flow] Found media player name: %s", media_player_name)
        else:
            _LOGGER.warning("[Options Flow] Could not find media player entry for: %s", media_player_entity_id)

        # --- Gather current values for all configurable settings ---
        # We need to pre-fill the form fields with the currently saved values.
        # The logic is: check `options` first, then `data`, then use the default constant.
        # This ensures that user-configured options are always prioritized.
        options = self.config_entry.options
        data = self.config_entry.data
        on_debounce = options.get(CONF_ON_DEBOUNCE, data.get(CONF_ON_DEBOUNCE, DEFAULT_ON_DEBOUNCE_SECONDS))
        off_debounce = options.get(CONF_OFF_DEBOUNCE, data.get(CONF_OFF_DEBOUNCE, DEFAULT_OFF_DEBOUNCE_SECONDS))
        inter_step_delay = options.get(CONF_INTER_STEP_DELAY, data.get(CONF_INTER_STEP_DELAY, DEFAULT_INTER_STEP_DELAY))
        spawn_timeout = options.get(CONF_SPAWN_TIMEOUT, data.get(CONF_SPAWN_TIMEOUT, DEFAULT_SPAWN_TIMEOUT))
        pair_timeout = options.get(CONF_PAIR_TIMEOUT, data.get(CONF_PAIR_TIMEOUT, DEFAULT_PAIR_TIMEOUT))
        trust_timeout = options.get(CONF_TRUST_TIMEOUT, data.get(CONF_TRUST_TIMEOUT, DEFAULT_TRUST_TIMEOUT))
        scan_duration = options.get(CONF_SCAN_DURATION, data.get(CONF_SCAN_DURATION, DEFAULT_SCAN_DURATION))

        _LOGGER.debug("[Options Flow] Current settings gathered for form fields.")

        # --- Define the schema for the options form ---
        # This schema tells Home Assistant what fields to display in the form.
        # Each field is defined with a type (NumberSelector) and configuration (min, max, step).
        # The `default` value is set to the current setting we just retrieved.
        schema = vol.Schema({
            # 'on_debounce' slider
            vol.Required(CONF_ON_DEBOUNCE, default=on_debounce): NumberSelector(NumberSelectorConfig(min=RANGE_ON_DEBOUNCE["min"], max=RANGE_ON_DEBOUNCE["max"], step=RANGE_ON_DEBOUNCE["step"], mode=NumberSelectorMode.SLIDER)),
            # 'off_debounce' slider
            vol.Required(CONF_OFF_DEBOUNCE, default=off_debounce): NumberSelector(NumberSelectorConfig(min=RANGE_OFF_DEBOUNCE["min"], max=RANGE_OFF_DEBOUNCE["max"], step=RANGE_OFF_DEBOUNCE["step"], mode=NumberSelectorMode.SLIDER)),
            # 'inter_step_delay' slider
            vol.Required(CONF_INTER_STEP_DELAY, default=inter_step_delay): NumberSelector(NumberSelectorConfig(min=INTER_STEP_DELAY_RANGE["min"], max=INTER_STEP_DELAY_RANGE["max"], step=INTER_STEP_DELAY_RANGE["step"], mode=NumberSelectorMode.SLIDER)),
            # 'spawn_timeout' slider
            vol.Required(CONF_SPAWN_TIMEOUT, default=spawn_timeout): NumberSelector(NumberSelectorConfig(min=TIMEOUT_RANGE["min"], max=TIMEOUT_RANGE["max"], step=TIMEOUT_RANGE["step"], mode=NumberSelectorMode.SLIDER)),
            # 'pair_timeout' slider
            vol.Required(CONF_PAIR_TIMEOUT, default=pair_timeout): NumberSelector(NumberSelectorConfig(min=TIMEOUT_RANGE["min"], max=TIMEOUT_RANGE["max"], step=TIMEOUT_RANGE["step"], mode=NumberSelectorMode.SLIDER)),
            # 'trust_timeout' slider
            vol.Required(CONF_TRUST_TIMEOUT, default=trust_timeout): NumberSelector(NumberSelectorConfig(min=TIMEOUT_RANGE["min"], max=TIMEOUT_RANGE["max"], step=TIMEOUT_RANGE["step"], mode=NumberSelectorMode.SLIDER)),
            # 'scan_duration' slider
            vol.Required(CONF_SCAN_DURATION, default=scan_duration): NumberSelector(NumberSelectorConfig(min=SCAN_DURATION_RANGE["min"], max=SCAN_DURATION_RANGE["max"], step=SCAN_DURATION_RANGE["step"], mode=NumberSelectorMode.SLIDER)),
        })
        
        _LOGGER.debug("[Options Flow] Showing form with description placeholders.")

        # Show the form to the user.
        # `step_id` is 'init', the first and only step in this options flow.
        # `data_schema` defines the form fields.
        # `description_placeholders` replaces placeholders in the translation file
        # (e.g., {media_player_name}) with the actual values we gathered.
        return self.async_show_form(
            step_id="init",
            data_schema=schema,
            description_placeholders={
                "media_player_name": media_player_name,
                "mac_address": mac_address
            }
        )
