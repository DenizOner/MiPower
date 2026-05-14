"""
State Service - Single Responsibility Principle

This module implements entity state operations following SOLID principles,
handling entity state access and retrieval functionality.
"""

import logging
from typing import Any, Optional

from homeassistant.core import HomeAssistant  # type: ignore[import]

from .registry_interface import StateInterface

_LOGGER = logging.getLogger(__name__)


class StateService(StateInterface):
    """Handles entity state operations with error handling and logging.

    This class is responsible for accessing Home Assistant entity states
    and performing state-related operations. Follows Single Responsibility
    Principle by focusing only on entity state operations.
    """

    def __init__(self):
        """Initialize the state service."""
        _LOGGER.debug("StateService initialized")

    def get_entity_state(self, hass: HomeAssistant, entity_id: str) -> Optional[Any]:
        """Get the current state of an entity.

        Args:
            hass: Home Assistant instance.
            entity_id: The entity ID to get the state for.

        Returns:
            The entity state object if found, None otherwise.
        """
        try:
            state = hass.states.get(entity_id)

            if state:
                _LOGGER.debug(
                    "State retrieved for entity %s: %s", entity_id, state.state
                )
            else:
                _LOGGER.debug("No state found for entity %s", entity_id)

            return state

        except Exception as e:
            _LOGGER.error(
                "Error getting state for entity %s: %s",
                entity_id,
                e,
                exc_info=True,
            )
            return None
