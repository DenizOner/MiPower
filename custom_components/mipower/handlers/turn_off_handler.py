"""Turn-off handler for MiPower integration."""

import logging
import time

from homeassistant.core import HomeAssistant  # type: ignore[import]

from ..core.interfaces import ITurnOffHandler
from ..models import TimingOptions

_LOGGER = logging.getLogger(__name__)


class TurnOffHandler(ITurnOffHandler):
    """Handles turn-off operations for MiPower devices."""

    def __init__(self) -> None:
        """Initialize the turn-off handler."""
        self._last_call_time = 0
        self._hass = None

    def _get_media_player_name(self, entity_id: str) -> str:
        """Get the friendly name of the media player entity."""
        if self._hass:
            state = self._hass.states.get(entity_id)
            return (
                state.attributes.get("friendly_name", entity_id) if state else entity_id
            )
        return entity_id

    async def turn_off(
        self,
        hass: HomeAssistant,
        media_player_entity_id: str,
        timing_options: TimingOptions,
    ) -> None:
        """
        Turn off the device by calling media_player.turn_off service.

        Args:
            hass: The Home Assistant instance.
            media_player_entity_id: The entity ID of the media player.
            timing_options: Timing configuration.
        """
        if self._hass is None:
            self._hass = hass

        name = self._get_media_player_name(media_player_entity_id)

        if not media_player_entity_id:
            _LOGGER.warning(
                "[%s (%s)] No media_player entity linked. Cannot perform turn-off.",
                name,
                media_player_entity_id,
            )
            return

        now = time.time()
        off_debounce_seconds = timing_options.off_debounce
        if now - self._last_call_time < off_debounce_seconds:
            _LOGGER.warning(
                "[%s (%s)] Turn off called too frequently. Debounced for %s seconds.",
                name,
                media_player_entity_id,
                off_debounce_seconds,
            )
            return
        self._last_call_time = now

        _LOGGER.info(
            "[%s (%s)] Turning off media_player.", name, media_player_entity_id
        )

        try:
            await hass.services.async_call(
                "media_player",
                "turn_off",
                {"entity_id": media_player_entity_id},
                blocking=True,
            )
            _LOGGER.info(
                "[%s (%s)] Successfully turned off.", name, media_player_entity_id
            )
        except Exception as e:
            _LOGGER.error(
                "[%s (%s)] Error calling turn_off service: %s",
                name,
                media_player_entity_id,
                e,
                exc_info=True,
            )
