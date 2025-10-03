"""Data update coordinator for the MiPower integration."""
# This file defines the MiPowerCoordinator, which is a central piece of the integration.
# Its primary job is to listen for state changes of a specified media_player entity
# and to hold the "on"/"off" status. The switch entity will then subscribe to this
# coordinator to get its state, ensuring that the switch accurately reflects the
# media player's status. This pattern is efficient because the state is fetched
# only once by the coordinator, and all entities share it.

from __future__ import annotations

import logging

from homeassistant.core import Event, HomeAssistant, callback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.const import STATE_ON

from .const import DOMAIN

# Set up a specific logger for this file.
_LOGGER = logging.getLogger(__name__)


class MiPowerCoordinator(DataUpdateCoordinator[bool]):
    """
    Manages the state of the media_player to coordinate the switch state.

    This coordinator's data is a boolean value:
    - True if the linked media_player is 'on'.
    - False otherwise.
    """

    def __init__(self, hass: HomeAssistant, media_player_entity_id: str) -> None:
        """
        Initialize the data update coordinator.

        Args:
            hass: The Home Assistant instance.
            media_player_entity_id: The entity ID of the media player to monitor.
        """
        # Call the superclass constructor.
        # We provide the logger and a name for the coordinator.
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
        )
        # Store the entity ID of the media player we need to track.
        self._media_player_entity_id = media_player_entity_id
        # This will hold the function that unsubscribes from the state listener.
        # It's important to store this so we can clean up properly when the integration is unloaded.
        self._unsubscribe = None
        _LOGGER.debug(
            "MiPowerCoordinator initialized for entity: %s", media_player_entity_id
        )

    async def async_setup(self) -> None:
        """
        Set up the coordinator and start listening for state changes.

        This method is called once when the integration is being set up.
        """
        _LOGGER.debug(
            "Setting up coordinator for %s.", self._media_player_entity_id
        )
        # Get the initial state of the media player.
        # This is important to ensure the switch has the correct state on startup.
        source_state = self.hass.states.get(self._media_player_entity_id)
        initial_is_on = source_state is not None and source_state.state == STATE_ON
        _LOGGER.debug(
            "Initial state of %s is: %s. Coordinator data set to: %s",
            self._media_player_entity_id,
            source_state.state if source_state else "Not Found",
            initial_is_on,
        )

        # Set the initial data for the coordinator.
        self.async_set_updated_data(initial_is_on)

        # Subscribe to state changes of the media player.
        # The '_async_handle_update' method will be called as a callback whenever the
        # state of the specified media player changes.
        self._unsubscribe = async_track_state_change_event(
            self.hass, [self._media_player_entity_id], self._async_handle_update
        )
        _LOGGER.info(
            "Coordinator setup complete. Now tracking state changes for %s.",
            self._media_player_entity_id,
        )

    async def async_unload(self) -> None:
        """
        Tear down the coordinator.

        This method is called when the integration is being unloaded.
        It's crucial to unsubscribe from the state listener to prevent memory leaks.
        """
        _LOGGER.debug(
            "Unloading coordinator for %s.", self._media_player_entity_id
        )
        if self._unsubscribe:
            # Call the unsubscribe function to stop listening for state changes.
            self._unsubscribe()
            self._unsubscribe = None
            _LOGGER.info(
                "Successfully unsubscribed from state changes for %s.",
                self._media_player_entity_id,
            )

    @callback
    def _async_handle_update(self, event: Event) -> None:
        """
        Handle state changes of the source media_player.

        This is a callback method that is triggered by the state change listener.

        Args:
            event: The event object containing information about the state change.
        """
        _LOGGER.debug("Received state update event: %s", event.data)
        # Extract the new state object from the event payload.
        new_state = event.data.get("new_state")

        # Determine the new 'on' status.
        is_on = new_state is not None and new_state.state == STATE_ON
        _LOGGER.debug(
            "New state is '%s'. Coordinator 'is_on' status updated to: %s",
            new_state.state if new_state else "None",
            is_on,
        )

        # Update the coordinator's data and notify all listeners (our switch entity).
        self.async_set_updated_data(is_on)
        _LOGGER.debug("Coordinator data updated and listeners notified.")
