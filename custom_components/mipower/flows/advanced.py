"""
Advanced setup flow for the MiPower integration.

This file defines the logic for the "Advanced Setup" path. This flow is a
multi-step process that gives the user more control over the configuration.
It is managed by the `AdvancedFlowManager` class, which is instantiated by the
main `MiPowerConfigFlow`.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import voluptuous as vol
from homeassistant.const import CONF_MAC
from homeassistant.helpers import (
    device_registry as dr,
    entity_registry as er,
    selector,
)
from homeassistant.helpers.selector import (
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
)

# Import constants from the main const.py file.
from ..const import (
    CONF_DEVICE_ID,
    CONF_INTER_STEP_DELAY,
    CONF_MEDIA_PLAYER_ENTITY_ID,
    CONF_OFF_DEBOUNCE,
    CONF_ON_DEBOUNCE,
    CONF_PAIR_TIMEOUT,
    CONF_SCAN_DURATION,
    CONF_SPAWN_TIMEOUT,
    CONF_TRUST_TIMEOUT,
    DEFAULT_DEVICE_NAME,
    DEFAULT_INTER_STEP_DELAY,
    DEFAULT_OFF_DEBOUNCE_SECONDS,
    DEFAULT_ON_DEBOUNCE_SECONDS,
    DEFAULT_PAIR_TIMEOUT,
    DEFAULT_SCAN_DURATION,
    DEFAULT_SPAWN_TIMEOUT,
    DEFAULT_TRUST_TIMEOUT,
    INTER_STEP_DELAY_RANGE,
    RANGE_OFF_DEBOUNCE,
    RANGE_ON_DEBOUNCE,
    SCAN_DURATION_RANGE,
    TIMEOUT_RANGE,
)

# This is a type-checking guard to prevent circular imports.
if TYPE_CHECKING:
    from homeassistant import config_entries
    from homeassistant.core import HomeAssistant
    from homeassistant.data_entry_flow import FlowResult

# Set up a specific logger for this file.
_LOGGER = logging.getLogger(__name__)


class AdvancedFlowManager:
    """Manages the multi-step advanced configuration flow."""

    def __init__(self, hass: HomeAssistant, flow: config_entries.ConfigFlow) -> None:
        """
        Initialize the advanced flow manager.

        Args:
            hass: The Home Assistant instance.
            flow: The parent MiPowerConfigFlow instance.
        """
        _LOGGER.debug("[Advanced Flow] Initializing AdvancedFlowManager.")
        self.hass = hass
        self.flow = flow
        # This dictionary will store the data collected from the user across all steps.
        self.flow_data: dict[str, Any] = {}

    async def async_handle_step(
        self, step_id: str, user_input: dict[str, Any] | None
    ) -> FlowResult:
        """
        Generic handler to route to the correct step function.

        Args:
            step_id: The ID of the current step.
            user_input: The data submitted by the user for the current step.

        Returns:
            The result of the step function.
        """
        _LOGGER.debug(
            "[Advanced Flow] Handling step '%s' with user_input: %s",
            step_id,
            user_input,
        )
        # If user_input is provided, it means a form was submitted.
        if user_input is not None:
            # Store the submitted data.
            self.flow_data.update(user_input)
            _LOGGER.debug("[Advanced Flow] Updated flow_data: %s", self.flow_data)

            # Determine the next step based on the current step_id.
            if step_id == "advanced_setup":
                _LOGGER.debug("[Advanced Flow] Proceeding to 'mac_address' step.")
                return await self.async_step_mac_address()
            if step_id == "mac_address":
                _LOGGER.debug("[Advanced Flow] Proceeding to 'settings' step.")
                return await self.async_step_settings()
            if step_id == "settings":
                _LOGGER.debug("[Advanced Flow] Final step. Creating config entry.")
                return await self.async_create_final_entry()

        # If user_input is None, show the form for the current step.
        if step_id == "advanced_setup":
            return await self.async_step_advanced_setup()

        # This should not be reached if the flow is logical.
        _LOGGER.error("[Advanced Flow] Unknown or out-of-order step: %s", step_id)
        return self.flow.async_abort(reason="unknown_step")

    async def async_step_advanced_setup(self) -> FlowResult:
        """
        Advanced Step 1: Show a dropdown of all media player devices.
        """
        _LOGGER.debug("[Advanced Flow] Step 1: Showing device selection form.")
        from ..api.discovery import get_all_media_player_devices

        all_media_player_devices = await get_all_media_player_devices(self.hass)
        _LOGGER.debug(
            "[Advanced Flow] Discovered media players: %s", all_media_player_devices
        )

        options = [
            selector.SelectOptionDict(value=device_id, label=name)
            for device_id, name in all_media_player_devices.items()
        ]

        schema = vol.Schema(
            {
                vol.Required(CONF_DEVICE_ID): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=options, mode=selector.SelectSelectorMode.DROPDOWN
                    )
                )
            }
        )
        return self.flow.async_show_form(
            step_id="advanced_setup", data_schema=schema
        )

    async def async_step_mac_address(self) -> FlowResult:
        """
        Advanced Step 2: Get the MAC address for the selected device.
        """
        _LOGGER.debug("[Advanced Flow] Step 2: Showing MAC address input form.")
        from ..api.discovery import (
            identifier_looks_like_bt,
            is_bluetooth_conn,
            normalize_mac,
        )

        device_id = self.flow_data[CONF_DEVICE_ID]
        device_registry = dr.async_get(self.hass)
        device = device_registry.async_get(device_id)
        _LOGGER.debug("[Advanced Flow] Looking for MAC on device: %s", device)

        default_mac = ""
        if device:
            # Try to find a MAC address from the device's connections.
            for conn in device.connections:
                if is_bluetooth_conn(conn) and (mac := normalize_mac(conn[1])):
                    default_mac = mac
                    _LOGGER.debug("[Advanced Flow] Found MAC '%s' in connections.", mac)
                    break
            # If not found, try to find it in the device's identifiers.
            if not default_mac:
                for ident in device.identifiers:
                    if identifier_looks_like_bt(ident):
                        candidate = normalize_mac(
                            ident[1] if isinstance(ident, (list, tuple)) and len(ident) >= 2 else
                            ident if isinstance(ident, str) else None
                        )
                        if candidate:
                            default_mac = candidate
                            _LOGGER.debug("[Advanced Flow] Found MAC '%s' in identifiers.", candidate)
                            break
        
        if not default_mac:
            _LOGGER.warning("[Advanced Flow] Could not automatically find a MAC address.")

        schema = vol.Schema({vol.Required(CONF_MAC, default=default_mac): str})
        return self.flow.async_show_form(step_id="mac_address", data_schema=schema)

    async def async_step_settings(self) -> FlowResult:
        """
        Advanced Step 3: Get timing and other advanced settings.
        """
        _LOGGER.debug("[Advanced Flow] Step 3: Showing timing settings form.")
        schema = vol.Schema(
            {
                vol.Required(
                    CONF_ON_DEBOUNCE, default=DEFAULT_ON_DEBOUNCE_SECONDS
                ): NumberSelector(
                    NumberSelectorConfig(
                        min=RANGE_ON_DEBOUNCE["min"],
                        max=RANGE_ON_DEBOUNCE["max"],
                        step=RANGE_ON_DEBOUNCE["step"],
                        mode=NumberSelectorMode.SLIDER,
                    )
                ),
                vol.Required(
                    CONF_OFF_DEBOUNCE, default=DEFAULT_OFF_DEBOUNCE_SECONDS
                ): NumberSelector(
                    NumberSelectorConfig(
                        min=RANGE_OFF_DEBOUNCE["min"],
                        max=RANGE_OFF_DEBOUNCE["max"],
                        step=RANGE_OFF_DEBOUNCE["step"],
                        mode=NumberSelectorMode.SLIDER,
                    )
                ),
                vol.Required(
                    CONF_INTER_STEP_DELAY, default=DEFAULT_INTER_STEP_DELAY
                ): NumberSelector(
                    NumberSelectorConfig(
                        min=INTER_STEP_DELAY_RANGE["min"],
                        max=INTER_STEP_DELAY_RANGE["max"],
                        step=INTER_STEP_DELAY_RANGE["step"],
                        mode=NumberSelectorMode.SLIDER,
                    )
                ),
                vol.Required(
                    CONF_SPAWN_TIMEOUT, default=DEFAULT_SPAWN_TIMEOUT
                ): NumberSelector(
                    NumberSelectorConfig(
                        min=TIMEOUT_RANGE["min"],
                        max=TIMEOUT_RANGE["max"],
                        step=TIMEOUT_RANGE["step"],
                        mode=NumberSelectorMode.SLIDER,
                    )
                ),
                vol.Required(
                    CONF_PAIR_TIMEOUT, default=DEFAULT_PAIR_TIMEOUT
                ): NumberSelector(
                    NumberSelectorConfig(
                        min=TIMEOUT_RANGE["min"],
                        max=TIMEOUT_RANGE["max"],
                        step=TIMEOUT_RANGE["step"],
                        mode=NumberSelectorMode.SLIDER,
                    )
                ),
                vol.Required(
                    CONF_TRUST_TIMEOUT, default=DEFAULT_TRUST_TIMEOUT
                ): NumberSelector(
                    NumberSelectorConfig(
                        min=TIMEOUT_RANGE["min"],
                        max=TIMEOUT_RANGE["max"],
                        step=TIMEOUT_RANGE["step"],
                        mode=NumberSelectorMode.SLIDER,
                    )
                ),
                vol.Required(
                    CONF_SCAN_DURATION, default=DEFAULT_SCAN_DURATION
                ): NumberSelector(
                    NumberSelectorConfig(
                        min=SCAN_DURATION_RANGE["min"],
                        max=SCAN_DURATION_RANGE["max"],
                        step=SCAN_DURATION_RANGE["step"],
                        mode=NumberSelectorMode.SLIDER,
                    )
                ),
            }
        )
        return self.flow.async_show_form(step_id="settings", data_schema=schema)

    async def async_create_final_entry(self) -> FlowResult:
        """
        Finalize the setup and create the config entry.
        """
        _LOGGER.debug("[Advanced Flow] Creating final config entry.")
        mac = self.flow_data[CONF_MAC]
        device_id = self.flow_data[CONF_DEVICE_ID]

        entity_registry = er.async_get(self.hass)
        device_registry = dr.async_get(self.hass)

        # Find the media_player entity associated with the selected device.
        media_player_entity_id = None
        for entity in er.async_entries_for_device(entity_registry, device_id):
            if entity.domain == "media_player":
                media_player_entity_id = entity.entity_id
                _LOGGER.debug("[Advanced Flow] Found media_player entity: %s", entity.entity_id)
                break

        if not media_player_entity_id:
            _LOGGER.error(
                "[Advanced Flow] No media_player entity found for device_id %s. Aborting.",
                device_id,
            )
            return self.flow.async_abort(reason="no_media_player_entity_found")

        # Get the device's name for the entry title.
        device = device_registry.async_get(device_id)
        name = (
            device.name_by_user or device.name if device else DEFAULT_DEVICE_NAME
        )

        # Set the unique ID and check for existing entries.
        await self.flow.async_set_unique_id(mac)
        self.flow._abort_if_unique_id_configured()
        _LOGGER.debug("[Advanced Flow] Unique ID set to %s. No existing entry found.", mac)

        # Consolidate all collected data for the config entry.
        data = {
            CONF_MAC: mac,
            CONF_MEDIA_PLAYER_ENTITY_ID: media_player_entity_id,
            **self.flow_data,  # Add all settings from the flow data
        }

        _LOGGER.debug(
            "[Advanced Flow] Creating entry with title '%s' and data: %s", name, data
        )
        return self.flow.async_create_entry(title=name, data=data)