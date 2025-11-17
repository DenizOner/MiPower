"""
Easy setup flow for the MiPower integration using SOLID principles.

This file implements the easy setup flow following SOLID principles.
It uses dependency injection and proper separation of concerns.
"""

from __future__ import annotations

import logging
from typing import Any

try:
    import voluptuous as vol
    from homeassistant.helpers.selector import (
        SelectOptionDict,
        SelectSelector,
        SelectSelectorConfig,
        SelectSelectorMode,
    )
except ImportError:

    class vol:
        @staticmethod
        def Schema(schema_dict):
            return schema_dict

        class Required:
            def __init__(self, key, default=None):
                self.key = key
                self.default = default

    class SelectSelector:
        def __init__(self, config):
            self.config = config

    class SelectSelectorConfig:
        def __init__(self, options=None, mode=None):
            self.options = options
            self.mode = mode

    class SelectSelectorMode:
        DROPDOWN = "dropdown"

    class SelectOptionDict:
        def __init__(self, value=None, label=None):
            self.value = value
            self.label = label


try:
    from homeassistant import config_entries
    from homeassistant.data_entry_flow import FlowResult
except ImportError:

    class config_entries:
        ConfigFlow = object

    class FlowResult:
        pass


from homeassistant.const import CONF_MAC

from ..const import (
    CONF_DEVICE,
    CONF_MEDIA_PLAYER_ENTITY_ID,
    DEFAULT_INTER_STEP_DELAY,
    DEFAULT_OFF_DEBOUNCE_SECONDS,
    DEFAULT_ON_DEBOUNCE_SECONDS,
    DEFAULT_SCAN_DURATION,
    DEFAULT_SCAN_STOP_TIMEOUT,
    DEFAULT_SIGNAL_DURATION,
    DEFAULT_SPAWN_TIMEOUT,
)
from ..models import TimingOptions
from ..services.discovery_service import BluetoothDiscoveryService

_LOGGER = logging.getLogger(__name__)


class EasyFlowManager:
    """
    Manages the easy setup flow using SOLID principles.

    This class follows SOLID principles:
    - Single Responsibility: Only manages easy flow logic
    - Open-Closed: Can be extended without modification
    - Liskov Substitution: Can replace any flow manager
    - Interface Segregation: Uses minimal interfaces
    - Dependency Inversion: Depends on abstractions
    """

    def __init__(self) -> None:
        """Initialize the easy flow manager with dependency injection."""
        # Inject discovery service
        self.discovery_service = BluetoothDiscoveryService()

    async def async_show_form(self, flow: config_entries.ConfigFlow) -> FlowResult:
        """
        Show the form for the easy setup path.

        Args:
            flow: The current config flow instance.

        Returns:
            The form to be displayed to the user.
        """
        _LOGGER.debug("[Easy Flow] Preparing to show easy setup form.")

        # Use injected discovery service
        bt_media_players = await self.discovery_service.discover_devices(flow.hass)
        _LOGGER.debug("[Easy Flow] Discovered BT media players: %s", bt_media_players)

        # If no compatible devices are found, we abort the flow and inform the user.
        if not bt_media_players:
            _LOGGER.warning(
                "[Easy Flow] No Bluetooth media players found. Aborting easy setup."
            )
            return flow.async_abort(reason="no_bt_media_players_found_strict")

        # Create a list of `SelectOptionDict` objects for the dropdown menu.
        options = [
            SelectOptionDict(value=mac, label=data["name"])
            for mac, data in bt_media_players.items()
        ]
        _LOGGER.debug("[Easy Flow] Created dropdown options: %s", options)

        # Define the schema for the form.
        schema = vol.Schema(
            {
                vol.Required(CONF_DEVICE): SelectSelector(
                    SelectSelectorConfig(
                        options=options, mode=SelectSelectorMode.DROPDOWN
                    )
                )
            }
        )

        _LOGGER.debug("[Easy Flow] Displaying form.")
        return flow.async_show_form(step_id="easy_setup", data_schema=schema)

    async def async_handle_submission(
        self, flow: config_entries.ConfigFlow, user_input: dict[str, Any]
    ) -> FlowResult:
        """
        Handle the submission of the easy setup form.

        Args:
            flow: The current config flow instance.
            user_input: The data submitted by the user.

        Returns:
            A FlowResult indicating the creation of the entry or an abort.
        """
        _LOGGER.debug("[Easy Flow] Handling form submission with input: %s", user_input)

        # The user's selection (the MAC address) is under the `CONF_DEVICE` key.
        mac = user_input[CONF_DEVICE]
        _LOGGER.debug("[Easy Flow] User selected MAC: %s", mac)

        # Set the unique ID for the config entry.
        await flow.async_set_unique_id(mac)
        flow._abort_if_unique_id_configured()
        _LOGGER.debug("[Easy Flow] Unique ID set to %s. No existing entry found.", mac)

        # Get the device list again to find the entity ID and name
        devices = await self.discovery_service.discover_devices(flow.hass)
        selected_device = devices.get(mac)

        # Safety check
        if not selected_device:
            _LOGGER.error(
                "[Easy Flow] The selected device with MAC %s could not be found. Aborting.",
                mac,
            )
            return flow.async_abort(reason="device_not_found")

        # Prepare the data for the new config entry.
        # Use the media player's friendly name as the title for the config entry.
        # This will be used as the base for the entity name.
        title = selected_device["name"]  # Doğrudan cihazın adını kullan
        timing_options = TimingOptions(
            on_debounce=DEFAULT_ON_DEBOUNCE_SECONDS,
            off_debounce=DEFAULT_OFF_DEBOUNCE_SECONDS,
            inter_step_delay=DEFAULT_INTER_STEP_DELAY,
            spawn_timeout=DEFAULT_SPAWN_TIMEOUT,
            signal_duration=DEFAULT_SIGNAL_DURATION,
            scan_duration=DEFAULT_SCAN_DURATION,
            scan_stop_timeout=DEFAULT_SCAN_STOP_TIMEOUT,  # Yeni eklendi
        )
        data = {
            CONF_MAC: mac,
            CONF_MEDIA_PLAYER_ENTITY_ID: selected_device["entity_id"],
            **timing_options.__dict__,
        }
        _LOGGER.debug(
            "[Easy Flow] Finalizing setup. Creating entry with title '%s' and data: %s",
            title,
            data,
        )
        _LOGGER.info(
            "[Easy Flow] Easy setup completed successfully. Creating config entry."
        )
        try:
            # Create the config entry and finish the flow.
            return flow.async_create_entry(title=title, data=data)
        except Exception as e:
            _LOGGER.error(
                "[Easy Flow] Error creating config entry: %s", e, exc_info=True
            )
            return flow.async_abort(reason="config_entry_creation_failed")


# Backward compatibility functions
_easy_flow_manager = EasyFlowManager()


async def async_show_easy_setup_form(flow: config_entries.ConfigFlow) -> FlowResult:
    """Backward compatibility function."""
    return await _easy_flow_manager.async_show_form(flow)


async def async_handle_easy_setup(
    flow: config_entries.ConfigFlow, user_input: dict[str, Any]
) -> FlowResult:
    """Backward compatibility function."""
    return await _easy_flow_manager.async_handle_submission(flow, user_input)
