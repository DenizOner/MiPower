"""Data update coordinator for the MiPower integration using SOLID principles."""
# This file defines the MiPowerCoordinator, which implements ICoordinator interface.
# Its sole responsibility is to track the state of a media_player entity and provide
# that state to subscribers. It follows the Single Responsibility Principle.

from __future__ import annotations

import logging

from homeassistant.const import STATE_ON
from homeassistant.core import Event, HomeAssistant, callback
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN
from .core.interfaces import ICoordinator

# Set up a specific logger for this file.
_LOGGER = logging.getLogger(__name__)


class MiPowerCoordinator(DataUpdateCoordinator[bool], ICoordinator):
    """
    Manages the state of the media_player to coordinate the switch state.

    This coordinator implements ICoordinator and follows SOLID principles:
    - Single Responsibility: Only manages media player state tracking
    - Open-Closed: Can be extended without modification
    - Liskov Substitution: Can replace any ICoordinator
    - Interface Segregation: Implements only relevant interface
    - Dependency Inversion: Depends on abstractions, not concretions

    The coordinator's data is a boolean value:
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
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
        )
        # Store the HomeAssistant instance and entity ID of the media player we need to track.
        self._hass = hass
        self._media_player_entity_id = media_player_entity_id
        # This will hold the function that unsubscribes from the state listener.
        self._unsubscribe = None
        _LOGGER.debug(
            "[%s (%s)] MiPowerCoordinator initialized.",
            self._get_media_player_name(),
            media_player_entity_id
        )

    async def async_setup(self) -> None:
        """
        Set up the coordinator and start listening for state changes.

        This method is called once when the integration is being set up.
        """
        name = self._get_media_player_name()
        _LOGGER.debug("[%s (%s)] Setting up coordinator.", name, self._media_player_entity_id)
        # Get the initial state of the media player.
        source_state = self.hass.states.get(self._media_player_entity_id)
        initial_is_on = source_state is not None and source_state.state == STATE_ON
        _LOGGER.debug(
            "[%s (%s)] Initial state is: %s. Coordinator data set to: %s",
            name,
            self._media_player_entity_id,
            source_state.state if source_state else "Not Found",
            initial_is_on,
        )

        # Set the initial data for the coordinator.
        self.async_set_updated_data(initial_is_on)

        # Subscribe to state changes of the media player.
        self._unsubscribe = async_track_state_change_event(
            self.hass, [self._media_player_entity_id], self._async_handle_update
        )
        _LOGGER.info(
            "[%s (%s)] Coordinator setup complete. Now tracking state changes.",
            name,
            self._media_player_entity_id,
        )

    async def async_unload(self) -> None:
        """
        Tear down the coordinator.

        This method is called when the integration is being unloaded.
        It's crucial to unsubscribe from the state listener to prevent memory leaks.
        """
        name = self._get_media_player_name()
        _LOGGER.debug("[%s (%s)] Unloading coordinator.", name, self._media_player_entity_id)
        if self._unsubscribe:
            # Call the unsubscribe function to stop listening for state changes.
            self._unsubscribe()
            self._unsubscribe = None
            _LOGGER.info(
                "[%s (%s)] Successfully unsubscribed from state changes.",
                name,
                self._media_player_entity_id,
            )

    @property
    def coordinator_data(self) -> bool | None:
        """
        Get current coordinator data.

        This implements the ICoordinator interface requirement.
        Returns the current state of the media player (True if on, False otherwise).
        """
        return super().data

    def _get_media_player_name(self) -> str:
        """Get the friendly name of the media player entity."""
        state = self._hass.states.get(self._media_player_entity_id)
        return (
            state.attributes.get("friendly_name", self._media_player_entity_id)
            if state
            else self._media_player_entity_id
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
