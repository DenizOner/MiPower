"""
Advanced setup flow for the MiPower integration using SOLID principles.

This file implements the advanced setup flow following SOLID principles.
It uses dependency injection and proper separation of concerns.
"""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol  # type: ignore[import]
from homeassistant import config_entries  # type: ignore[import]
from homeassistant.const import CONF_MAC  # type: ignore[attr-defined]
from homeassistant.core import HomeAssistant  # type: ignore[import]
from homeassistant.data_entry_flow import FlowResult  # type: ignore[import]
from homeassistant.helpers import device_registry as dr  # type: ignore[import]
from homeassistant.helpers import entity_registry as er  # type: ignore[import]
from homeassistant.helpers.selector import (  # type: ignore[import]
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from ..const import (
    CONF_DEVICE_ID,
    CONF_INTER_STEP_DELAY,
    CONF_MEDIA_PLAYER_ENTITY_ID,
    CONF_OFF_DEBOUNCE,
    CONF_ON_DEBOUNCE,
    CONF_SCAN_DURATION,
    CONF_SCAN_STOP_TIMEOUT,
    CONF_SIGNAL_DURATION,
    CONF_SPAWN_TIMEOUT,
    DEFAULT_DEVICE_NAME,
    DEFAULT_INTER_STEP_DELAY,
    DEFAULT_OFF_DEBOUNCE_SECONDS,
    DEFAULT_ON_DEBOUNCE_SECONDS,
    DEFAULT_SCAN_DURATION,
    DEFAULT_SCAN_STOP_TIMEOUT,
    DEFAULT_SIGNAL_DURATION,
    DEFAULT_SPAWN_TIMEOUT,
    RANGE_INTER_STEP_DELAY,
    RANGE_OFF_DEBOUNCE,
    RANGE_ON_DEBOUNCE,
    RANGE_SCAN_DURATION,
    RANGE_SCAN_STOP_TIMEOUT,
    RANGE_SIGNAL_DURATION,
    RANGE_SPAWN_TIMEOUT,
)
from ..models import TimingOptions
from ..services.discovery_service import (
    BluetoothDiscoveryService,
    MediaPlayerDiscoveryService,
)

_LOGGER = logging.getLogger(__name__)


class AdvancedFlowManager:
    """
    Manages the multi-step advanced configuration flow using SOLID principles.

    This class follows SOLID principles:
    - Single Responsibility: Only manages advanced flow logic
    - Open-Closed: Can be extended without modification
    - Liskov Substitution: Can replace any flow manager
    - Interface Segregation: Uses minimal interfaces
    - Dependency Inversion: Depends on abstractions
    """

    def __init__(self, hass: HomeAssistant, flow: config_entries.ConfigFlow) -> None:
        """
        Initialize the advanced flow manager with dependency injection.

        Args:
            hass: The Home Assistant instance.
            flow: The parent MiPowerConfigFlow instance.
        """
        _LOGGER.debug("[Advanced Flow] Initializing AdvancedFlowManager.")
        self.hass = hass
        self.flow = flow
        self.flow_data: dict[str, Any] = {}
        # Inject discovery services
        self.media_player_discovery = MediaPlayerDiscoveryService()
        self.bluetooth_discovery = BluetoothDiscoveryService()

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
        _LOGGER.error(
            "[Advanced Flow] Unknown or out-of-order step: %s", step_id, exc_info=True
        )
        return self.flow.async_abort(reason="unknown_step")

    async def async_step_advanced_setup(self) -> FlowResult:
        """
        Advanced Step 1: Show a dropdown of all media player devices.
        """
        _LOGGER.debug("[Advanced Flow] Step 1: Showing device selection form.")

        # Use injected discovery service
        all_media_player_devices = await self.media_player_discovery.discover_devices(
            self.hass
        )
        _LOGGER.debug(
            "[Advanced Flow] Discovered media players: %s", all_media_player_devices
        )

        options = [
            SelectOptionDict(value=device_id, label=name)
            for device_id, name in all_media_player_devices.items()
        ]

        schema = vol.Schema(
            {
                vol.Required(CONF_DEVICE_ID): SelectSelector(
                    SelectSelectorConfig(
                        options=options, mode=SelectSelectorMode.DROPDOWN
                    )
                )
            }
        )
        return self.flow.async_show_form(step_id="advanced_setup", data_schema=schema)

    async def async_step_mac_address(self) -> FlowResult:
        """
        Advanced Step 2: Get the MAC address for the selected device.
        """
        _LOGGER.debug("[Advanced Flow] Step 2: Showing MAC address input form.")

        device_id = self.flow_data[CONF_DEVICE_ID]
        device_registry = dr.async_get(self.hass)
        device = device_registry.async_get(device_id)
        _LOGGER.debug("[Advanced Flow] Looking for MAC on device: %s", device)

        default_mac = ""
        if device:
            # Try to find a MAC address from the device's connections.
            for conn in device.connections:
                if self.bluetooth_discovery.is_bluetooth_conn(conn) and (
                    mac := self.bluetooth_discovery.normalize_mac(conn[1])
                ):
                    default_mac = mac
                    _LOGGER.debug("[Advanced Flow] Found MAC '%s' in connections.", mac)
                    break
            # If not found, try to find it in the device's identifiers.
            if not default_mac:
                for ident in device.identifiers:
                    if self.bluetooth_discovery.identifier_looks_like_bt(ident):
                        candidate = self.bluetooth_discovery.normalize_mac(
                            ident[1]
                            if isinstance(ident, (list, tuple)) and len(ident) >= 2
                            else ident
                            if isinstance(ident, str)
                            else None
                        )
                        if candidate:
                            default_mac = candidate
                            _LOGGER.debug(
                                "[Advanced Flow] Found MAC '%s' in identifiers.",
                                candidate,
                            )
                            break

        if not default_mac:
            _LOGGER.warning(
                "[Advanced Flow] Could not automatically find a MAC address."
            )

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
                        min=RANGE_INTER_STEP_DELAY["min"],
                        max=RANGE_INTER_STEP_DELAY["max"],
                        step=RANGE_INTER_STEP_DELAY["step"],
                        mode=NumberSelectorMode.SLIDER,
                    )
                ),
                vol.Required(
                    CONF_SPAWN_TIMEOUT, default=DEFAULT_SPAWN_TIMEOUT
                ): NumberSelector(
                    NumberSelectorConfig(
                        min=RANGE_SPAWN_TIMEOUT["min"],
                        max=RANGE_SPAWN_TIMEOUT["max"],
                        step=RANGE_SPAWN_TIMEOUT["step"],
                        mode=NumberSelectorMode.SLIDER,
                    )
                ),
                vol.Required(
                    CONF_SIGNAL_DURATION, default=DEFAULT_SIGNAL_DURATION
                ): NumberSelector(
                    NumberSelectorConfig(
                        min=RANGE_SIGNAL_DURATION["min"],
                        max=RANGE_SIGNAL_DURATION["max"],
                        step=RANGE_SIGNAL_DURATION["step"],
                        mode=NumberSelectorMode.SLIDER,
                    )
                ),
                vol.Required(
                    CONF_SCAN_DURATION, default=DEFAULT_SCAN_DURATION
                ): NumberSelector(
                    NumberSelectorConfig(
                        min=RANGE_SCAN_DURATION["min"],
                        max=RANGE_SCAN_DURATION["max"],
                        step=RANGE_SCAN_DURATION["step"],
                        mode=NumberSelectorMode.SLIDER,
                    )
                ),
                vol.Required(
                    CONF_SCAN_STOP_TIMEOUT, default=DEFAULT_SCAN_STOP_TIMEOUT
                ): NumberSelector(
                    NumberSelectorConfig(
                        min=RANGE_SCAN_STOP_TIMEOUT["min"],
                        max=RANGE_SCAN_STOP_TIMEOUT["max"],
                        step=RANGE_SCAN_STOP_TIMEOUT["step"],
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
                _LOGGER.debug(
                    "[Advanced Flow] Found media_player entity: %s", entity.entity_id
                )
                break

        if not media_player_entity_id:
            _LOGGER.error(
                "[Advanced Flow] No media_player entity found for device_id %s. Aborting.",
                device_id,
                exc_info=True,
            )
            return self.flow.async_abort(reason="no_media_player_entity_found")

        # Get the device's name for the entry title.
        # Use the media player's friendly name as the title for the config entry.
        # This will be used as the base for the entity name.
        device_entry = device_registry.async_get(device_id)
        name = (
            device_entry.name
            if device_entry and device_entry.name
            else DEFAULT_DEVICE_NAME
        )

        # Set the unique ID and check for existing entries.
        await self.flow.async_set_unique_id(mac)
        self.flow._abort_if_unique_id_configured()
        _LOGGER.debug(
            "[Advanced Flow] Unique ID set to %s. No existing entry found.", mac
        )

        # Consolidate all collected data for the config entry.
        timing_options = TimingOptions(
            on_debounce=self.flow_data[CONF_ON_DEBOUNCE],
            off_debounce=self.flow_data[CONF_OFF_DEBOUNCE],
            inter_step_delay=self.flow_data[CONF_INTER_STEP_DELAY],
            spawn_timeout=self.flow_data[CONF_SPAWN_TIMEOUT],
            signal_duration=self.flow_data[CONF_SIGNAL_DURATION],
            scan_duration=self.flow_data[CONF_SCAN_DURATION],
            scan_stop_timeout=self.flow_data[CONF_SCAN_STOP_TIMEOUT],
        )

        data = {
            CONF_MAC: mac,
            CONF_MEDIA_PLAYER_ENTITY_ID: media_player_entity_id,
            CONF_DEVICE_ID: device_id,
            "name": name,  # Add the friendly name to the data
            **timing_options.__dict__,
        }

        try:
            _LOGGER.debug(
                "[Advanced Flow] Creating entry with title '%s' and data: %s",
                name,
                data,
            )
            _LOGGER.info(
                "[Advanced Flow] Advanced setup completed successfully. Creating config entry."
            )
            return self.flow.async_create_entry(title=name, data=data)
        except Exception as e:
            _LOGGER.error(
                "[Advanced Flow] Error creating config entry: %s", e, exc_info=True
            )
            return self.flow.async_abort(reason="config_entry_creation_failed")
