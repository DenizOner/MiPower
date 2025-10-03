"""
Easy setup flow for the MiPower integration.

This file defines the logic for the "Easy Setup" path. This flow is designed
to be a simple, one-step process for the user. It automatically discovers
Bluetooth-enabled media players and presents them in a dropdown list.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import voluptuous as vol
from homeassistant.const import CONF_MAC
from homeassistant.helpers import selector

# Import constants from the main const.py file.
from ..const import (
    CONF_DEVICE,
    CONF_MEDIA_PLAYER_ENTITY_ID,
    CONF_ON_DEBOUNCE,
    DEFAULT_ON_DEBOUNCE_SECONDS,
)

# This is a type-checking guard to prevent circular imports.
# The `config_entries` module is only imported for type hinting.
if TYPE_CHECKING:
    from homeassistant import config_entries
    from homeassistant.data_entry_flow import FlowResult

# Set up a specific logger for this file.
_LOGGER = logging.getLogger(__name__)


async def async_show_easy_setup_form(
    flow: config_entries.ConfigFlow,
) -> FlowResult:
    """
    Show the form for the easy setup path.

    This function discovers Bluetooth media players, creates a dropdown list,
    and displays it to the user.

    Args:
        flow: The current config flow instance.

    Returns:
        The form to be displayed to the user.
    """
    _LOGGER.debug("[Easy Flow] Preparing to show easy setup form.")
    # We import the discovery function here locally to avoid potential circular
    # dependencies at the global level.
    from ..api.discovery import get_bt_media_players

    # Discover all available Bluetooth media players in Home Assistant.
    bt_media_players = await get_bt_media_players(flow.hass)
    _LOGGER.debug("[Easy Flow] Discovered BT media players: %s", bt_media_players)

    # If no compatible devices are found, we abort the flow and inform the user.
    if not bt_media_players:
        _LOGGER.warning("[Easy Flow] No Bluetooth media players found. Aborting easy setup.")
        return flow.async_abort(reason="no_bt_media_players_found_strict")

    # Create a list of `SelectOptionDict` objects for the dropdown menu.
    # The 'value' will be the device's MAC address, and the 'label' will be its friendly name.
    options = [
        selector.SelectOptionDict(value=mac, label=data["name"])
        for mac, data in bt_media_players.items()
    ]
    _LOGGER.debug("[Easy Flow] Created dropdown options: %s", options)

    # Define the schema for the form. It will contain a single dropdown field.
    # The key `CONF_DEVICE` will be used to retrieve the user's selection.
    schema = vol.Schema(
        {
            vol.Required(CONF_DEVICE): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=options, mode=selector.SelectSelectorMode.DROPDOWN
                )
            )
        }
    )

    # Show the form to the user. The `step_id` is 'easy_setup', which matches
    # the step ID defined in the main config flow.
    _LOGGER.debug("[Easy Flow] Displaying form.")
    return flow.async_show_form(step_id="easy_setup", data_schema=schema)


async def async_handle_easy_setup(
    flow: config_entries.ConfigFlow, user_input: dict[str, Any]
) -> FlowResult:
    """
    Handle the submission of the easy setup form.

    This function is called after the user selects a device from the dropdown
    and clicks "Submit". It retrieves the selected device's information and
    creates the final config entry.

    Args:
        flow: The current config flow instance.
        user_input: The data submitted by the user.

    Returns:
        A FlowResult indicating the creation of the entry or an abort.
    """
    _LOGGER.debug("[Easy Flow] Handling form submission with input: %s", user_input)
    # We import here to avoid circular dependencies.
    from ..api.discovery import get_bt_media_players

    # The user's selection (the MAC address) is under the `CONF_DEVICE` key.
    mac = user_input[CONF_DEVICE]
    _LOGGER.debug("[Easy Flow] User selected MAC: %s", mac)

    # Set the unique ID for the config entry. This is crucial to prevent
    # the same device from being configured multiple times.
    await flow.async_set_unique_id(mac)
    # Check if a config entry with this unique ID already exists. If so, abort.
    flow._abort_if_unique_id_configured()
    _LOGGER.debug("[Easy Flow] Unique ID set to %s. No existing entry found.", mac)

    # We need to get the device list again to find the entity ID and name
    # corresponding to the selected MAC address.
    devices = await get_bt_media_players(flow.hass)
    selected_device = devices.get(mac)

    # This is a safety check. If the selected device is somehow no longer
    # available, we abort.
    if not selected_device:
        _LOGGER.error(
            "[Easy Flow] The selected device with MAC %s could not be found. Aborting.",
            mac,
        )
        return flow.async_abort(reason="device_not_found")

    # Prepare the data for the new config entry.
    title = selected_device["name"]
    data = {
        CONF_MAC: mac,
        CONF_MEDIA_PLAYER_ENTITY_ID: selected_device["entity_id"],
        # For easy setup, we use a default value for the debounce setting.
        CONF_ON_DEBOUNCE: DEFAULT_ON_DEBOUNCE_SECONDS,
    }
    _LOGGER.debug(
        "[Easy Flow] Finalizing setup. Creating entry with title '%s' and data: %s",
        title,
        data,
    )

    # Create the config entry and finish the flow.
    return flow.async_create_entry(title=title, data=data)