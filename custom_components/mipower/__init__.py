"""The MiPower integration."""
# This file is the main entry point for the MiPower integration.
# It is responsible for setting up the integration when a user adds it from the UI,
# and for unloading it when the user removes it.

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback

from .const import CONF_MEDIA_PLAYER_ENTITY_ID, DOMAIN
from .coordinator import MiPowerCoordinator

# A list of platforms that this integration will set up.
# In this case, we only have a 'switch' platform.
PLATFORMS: list[str] = ["switch"]

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """
    Set up MiPower from a config entry.

    This function is called by Home Assistant when a user has successfully
    configured a new instance of the integration.

    Args:
        hass: The Home Assistant instance.
        entry: The config entry that holds the user's configuration.

    Returns:
        True if the setup was successful, False otherwise.
    """
    _LOGGER.debug("Setting up MiPower entry with entry_id: %s", entry.entry_id)

    # The hass.data dictionary is a global place to store data for integrations.
    # We create a dictionary for our domain if it doesn't already exist.
    hass.data.setdefault(DOMAIN, {})
    _LOGGER.debug("Hass.data structure for domain '%s' initialized.", DOMAIN)

    # Retrieve the media player entity ID from the config entry's data.
    # This was saved during the configuration flow.
    media_player_entity_id = entry.data.get(CONF_MEDIA_PLAYER_ENTITY_ID)
    _LOGGER.debug("Retrieved media_player_entity_id: %s", media_player_entity_id)

    # Create an instance of our data coordinator.
    # The coordinator is responsible for fetching and holding the state
    # that our switch entity will use.
    coordinator = MiPowerCoordinator(hass, media_player_entity_id)
    _LOGGER.debug("MiPowerCoordinator instance created.")

    # Set up the coordinator. This involves setting its initial state and
    # starting the listener for the media player's state changes.
    await coordinator.async_setup()
    _LOGGER.debug("Coordinator setup completed.")

    # Store the coordinator instance in hass.data, keyed by the config entry's ID.
    # This makes it accessible to the platform setup (e.g., in switch.py).
    hass.data[DOMAIN][entry.entry_id] = coordinator
    _LOGGER.debug("Coordinator stored in hass.data[%s][%s]", DOMAIN, entry.entry_id)

    # Forward the setup to the switch platform.
    # This tells Home Assistant to load the 'switch' platform from this integration
    # and call its async_setup_entry function.
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    _LOGGER.debug("Forwarded setup to platforms: %s", PLATFORMS)

    # Add an update listener. This function will be called when the user
    # changes the integration's options in the UI.
    entry.async_on_unload(entry.add_update_listener(_update_listener))
    _LOGGER.debug("Added update listener for options flow.")

    # Return True to indicate that the setup was successful.
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """
    Unload a config entry.

    This function is called by Home Assistant when a user removes the integration.
    It needs to clean up all resources that were set up.

    Args:
        hass: The Home Assistant instance.
        entry: The config entry to unload.

    Returns:
        True if the unload was successful.
    """
    _LOGGER.debug("Unloading MiPower entry with entry_id: %s", entry.entry_id)

    # Unload the platforms that were set up. This will remove the entities.
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    _LOGGER.debug("Unloaded platforms with result: %s", unload_ok)

    # If the platform unload was successful, clean up our coordinator.
    if unload_ok:
        # Remove the coordinator from hass.data.
        coordinator: MiPowerCoordinator = hass.data[DOMAIN].pop(entry.entry_id)
        _LOGGER.debug("Popped coordinator from hass.data.")

        # Unload the coordinator itself to stop its listeners.
        await coordinator.async_unload()
        _LOGGER.debug("Coordinator unloaded successfully.")

    return unload_ok


async def _update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """
    Handle options update.

    This function is called when the user saves changes in the options flow.
    The standard practice is to reload the integration to apply the new settings.

    Args:
        hass: The Home Assistant instance.
        entry: The config entry that was updated.
    """
    _LOGGER.debug("Options updated for entry %s, reloading integration.", entry.entry_id)
    # Reload the integration. This will call async_unload_entry and then async_setup_entry.
    await hass.config_entries.async_reload(entry.entry_id)
