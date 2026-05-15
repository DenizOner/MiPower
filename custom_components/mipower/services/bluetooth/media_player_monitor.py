"""
Media player monitor for MiPower integration.

This module handles media player state monitoring,
following the Single Responsibility Principle.
"""

import logging

from homeassistant.core import HomeAssistant  # type: ignore[import]

_LOGGER = logging.getLogger(__name__)


class MediaPlayerMonitor:
    """
    Monitors media player state and availability.

    Handles checking if media players are on, available, and triggering HA services.
    """

    def __init__(self, hass: HomeAssistant, media_player_entity_id: str) -> None:  # type: ignore
        """
        Initialize the media player monitor.

        Args:
            hass: Home Assistant instance
            media_player_entity_id: Media player entity ID to monitor
        """
        self._hass = hass
        self._media_player_entity_id = media_player_entity_id

    def is_media_player_on(self) -> bool:
        """
        Check if the media player is currently on.

        Returns:
            True if media player is on, False otherwise
        """
        state = self._hass.states.get(self._media_player_entity_id)  # type: ignore
        if state:
            _LOGGER.debug(
                "[%s] Media player state check: %s",
                self._media_player_entity_id,
                state.state,
            )
            return state.state == "on"
        _LOGGER.debug("[%s] Media player state not found", self._media_player_entity_id)
        return False

    def is_media_player_available(self) -> bool:
        """
        Check if the media player entity is available (not 'unavailable').

        Returns:
            True if media player is available, False otherwise
        """
        state = self._hass.states.get(self._media_player_entity_id)  # type: ignore
        if state:
            _LOGGER.debug(
                "[%s] Media player availability check: %s",
                self._media_player_entity_id,
                state.state,
            )
            return state.state != "unavailable"
        _LOGGER.debug(
            "[%s] Media player state not found for availability check",
            self._media_player_entity_id,
        )
        return False

    def try_turn_on_via_ha_service(self) -> bool:
        """
        Try to turn on the media player via Home Assistant service.

        Returns:
            True if service call was successful, False otherwise
        """
        try:
            _LOGGER.info(
                "[%s] Media player is available, attempting HA media_player.turn_on "
                "service call.",
                self._media_player_entity_id,
            )

            # Call HA's media_player.turn_on service
            self._hass.services.call(  # type: ignore
                "media_player",
                "turn_on",
                {"entity_id": self._media_player_entity_id},
                blocking=True,
            )

            # Check if it actually turned on
            if self.is_media_player_on():
                _LOGGER.info(
                    "[%s] HA media_player.turn_on command successful after "
                    "availability.",
                    self._media_player_entity_id,
                )
                return True

            return False

        except Exception as e:
            _LOGGER.warning(
                "[%s] HA media_player.turn_on service call failed after "
                "availability. Error: %s",
                self._media_player_entity_id,
                e,
            )
            return False
