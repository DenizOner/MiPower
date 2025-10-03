"""
Turn-off logic for the MiPower integration.

This file contains the logic for turning off the device. The approach is simple:
it calls the standard `media_player.turn_off` service on the entity that the
user linked during the configuration process.
"""

import logging

from homeassistant.core import HomeAssistant

# Set up a specific logger for this file.
_LOGGER = logging.getLogger(__name__)


async def perform_turn_off(hass: HomeAssistant, media_player_entity_id: str) -> None:
    """
    Turn off the associated media_player entity.

    This function is called when the MiPower switch is turned off in Home Assistant.

    Args:
        hass: The Home Assistant instance, used to call services.
        media_player_entity_id: The entity ID of the media player to turn off.
    """
    # A safety check to ensure a media player entity is actually linked.
    if not media_player_entity_id:
        _LOGGER.warning(
            "MiPower switch was turned off, but no media_player entity is linked. Cannot perform any action."
        )
        return

    _LOGGER.info(
        "MiPower switch is turning off. Calling 'media_player.turn_off' for entity: %s",
        media_player_entity_id,
    )

    # Use the Home Assistant service bus to call the 'turn_off' service
    # for the 'media_player' domain.
    try:
        await hass.services.async_call(
            "media_player",
            "turn_off",
            {"entity_id": media_player_entity_id},
            blocking=True,  # 'blocking=True' waits for the service call to complete.
        )
        _LOGGER.info(
            "Successfully called turn_off service for %s.", media_player_entity_id
        )
    except Exception as e:
        _LOGGER.error(
            "An error occurred while calling turn_off service for %s: %s",
            media_player_entity_id,
            e,
            exc_info=True,
        )
