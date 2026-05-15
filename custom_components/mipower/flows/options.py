"""
Options flow for the MiPower integration using SOLID principles.

This file implements the options flow following SOLID principles.
It allows users to re-configure the integration after setup.
"""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol  # type: ignore[import]
from homeassistant import config_entries  # type: ignore[import]
from homeassistant.const import CONF_MAC  # type: ignore[import]
from homeassistant.data_entry_flow import FlowResult  # type: ignore[import]
from homeassistant.helpers.selector import (  # type: ignore[import]
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
)

from ..const import (
    CONF_INTER_STEP_DELAY,
    CONF_MEDIA_PLAYER_ENTITY_ID,
    CONF_OFF_DEBOUNCE,
    CONF_ON_DEBOUNCE,
    CONF_SCAN_DURATION,
    CONF_SIGNAL_DURATION,
    CONF_SPAWN_TIMEOUT,
    DEFAULT_INTER_STEP_DELAY,
    DEFAULT_OFF_DEBOUNCE_SECONDS,
    DEFAULT_ON_DEBOUNCE_SECONDS,
    DEFAULT_SCAN_DURATION,
    DEFAULT_SIGNAL_DURATION,
    DEFAULT_SPAWN_TIMEOUT,
    RANGE_INTER_STEP_DELAY,
    RANGE_OFF_DEBOUNCE,
    RANGE_ON_DEBOUNCE,
    RANGE_SCAN_DURATION,
    RANGE_SIGNAL_DURATION,
    RANGE_SPAWN_TIMEOUT,
)

_LOGGER = logging.getLogger(__name__)


class MiPowerOptionsFlowHandler(config_entries.OptionsFlow):
    """
    Handle the options flow for the MiPower integration using SOLID principles.

    This class follows SOLID principles:
    - Single Responsibility: Only manages options flow
    - Open-Closed: Can be extended without modification
    - Liskov Substitution: Can replace any OptionsFlow
    - Interface Segregation: Uses minimal interfaces
    - Dependency Inversion: Depends on abstractions
    """

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """
        Manage the options for the integration.

        This is the primary step of the options flow, where the user can view and edit settings.
        """
        media_player_entity_id = self.config_entry.data.get(CONF_MEDIA_PLAYER_ENTITY_ID)
        media_player_name = self.config_entry.title

        _LOGGER.debug(
            "[%s (%s)] Entering async_step_init. User input: %s",
            media_player_name,
            media_player_entity_id,
            user_input,
        )

        # Handle form submission
        if user_input is not None:
            _LOGGER.debug(
                "[%s (%s)] User submitted new options: %s",
                media_player_name,
                media_player_entity_id,
                user_input,
            )
            return self.async_create_entry(title="", data=user_input)

        _LOGGER.debug(
            "[%s (%s)] No user input, preparing to show the form.",
            media_player_name,
            media_player_entity_id,
        )

        # Gather data for description placeholders
        media_player_entity_id = self.config_entry.data.get(CONF_MEDIA_PLAYER_ENTITY_ID)
        mac_address = self.config_entry.data.get(CONF_MAC)
        # Config entry title'ı, easy.py ve advanced.py'de cihazın adı olarak ayarlandı.
        # Bu nedenle, medya oynatıcı adını doğrudan config entry'nin başlığından alabiliriz.
        media_player_name = self.config_entry.title
        _LOGGER.debug(
            "[%s (%s)] Media player entity ID: %s, MAC: %s, Name: %s",
            media_player_name,
            media_player_entity_id,
            media_player_entity_id,
            mac_address,
            media_player_name,
        )

        # Gather current values for all configurable settings
        options = self.config_entry.options
        data = self.config_entry.data
        on_debounce = options.get(
            CONF_ON_DEBOUNCE, data.get(CONF_ON_DEBOUNCE, DEFAULT_ON_DEBOUNCE_SECONDS)
        )
        off_debounce = options.get(
            CONF_OFF_DEBOUNCE, data.get(CONF_OFF_DEBOUNCE, DEFAULT_OFF_DEBOUNCE_SECONDS)
        )
        inter_step_delay = options.get(
            CONF_INTER_STEP_DELAY,
            data.get(CONF_INTER_STEP_DELAY, DEFAULT_INTER_STEP_DELAY),
        )
        spawn_timeout = options.get(
            CONF_SPAWN_TIMEOUT, data.get(CONF_SPAWN_TIMEOUT, DEFAULT_SPAWN_TIMEOUT)
        )
        signal_duration = options.get(
            CONF_SIGNAL_DURATION,
            data.get(CONF_SIGNAL_DURATION, DEFAULT_SIGNAL_DURATION),
        )
        scan_duration = options.get(
            CONF_SCAN_DURATION, data.get(CONF_SCAN_DURATION, DEFAULT_SCAN_DURATION)
        )

        _LOGGER.debug(
            "[%s (%s)] Current settings gathered for form fields.",
            media_player_name,
            media_player_entity_id,
        )

        # Define the schema for the options form
        schema = vol.Schema(
            {
                vol.Required(CONF_ON_DEBOUNCE, default=on_debounce): NumberSelector(
                    NumberSelectorConfig(
                        min=RANGE_ON_DEBOUNCE["min"],
                        max=RANGE_ON_DEBOUNCE["max"],
                        step=RANGE_ON_DEBOUNCE["step"],
                        mode=NumberSelectorMode.SLIDER,
                    )
                ),
                vol.Required(CONF_OFF_DEBOUNCE, default=off_debounce): NumberSelector(
                    NumberSelectorConfig(
                        min=RANGE_OFF_DEBOUNCE["min"],
                        max=RANGE_OFF_DEBOUNCE["max"],
                        step=RANGE_OFF_DEBOUNCE["step"],
                        mode=NumberSelectorMode.SLIDER,
                    )
                ),
                vol.Required(CONF_SPAWN_TIMEOUT, default=spawn_timeout): NumberSelector(
                    NumberSelectorConfig(
                        min=RANGE_SPAWN_TIMEOUT["min"],
                        max=RANGE_SPAWN_TIMEOUT["max"],
                        step=RANGE_SPAWN_TIMEOUT["step"],
                        mode=NumberSelectorMode.SLIDER,
                    )
                ),
                vol.Required(CONF_SCAN_DURATION, default=scan_duration): NumberSelector(
                    NumberSelectorConfig(
                        min=RANGE_SCAN_DURATION["min"],
                        max=RANGE_SCAN_DURATION["max"],
                        step=RANGE_SCAN_DURATION["step"],
                        mode=NumberSelectorMode.SLIDER,
                    )
                ),
                vol.Required(
                    CONF_SIGNAL_DURATION, default=signal_duration
                ): NumberSelector(
                    NumberSelectorConfig(
                        min=RANGE_SIGNAL_DURATION["min"],
                        max=RANGE_SIGNAL_DURATION["max"],
                        step=RANGE_SIGNAL_DURATION["step"],
                        mode=NumberSelectorMode.SLIDER,
                    )
                ),
                vol.Required(
                    CONF_INTER_STEP_DELAY, default=inter_step_delay
                ): NumberSelector(
                    NumberSelectorConfig(
                        min=RANGE_INTER_STEP_DELAY["min"],
                        max=RANGE_INTER_STEP_DELAY["max"],
                        step=RANGE_INTER_STEP_DELAY["step"],
                        mode=NumberSelectorMode.SLIDER,
                    )
                ),
            }
        )

        _LOGGER.debug(
            "[%s (%s)] Showing form with description placeholders.",
            media_player_name,
            media_player_entity_id,
        )

        # Show the form to the user
        return self.async_show_form(
            step_id="init",
            data_schema=schema,
            description_placeholders={
                "media_player_name": media_player_name,
                "mac_address": mac_address,
            },
        )
