"""
Switch platform for the MiPower integration.

This file defines the main switch entity for the integration. The MiPowerSwitch class
is the core of this platform. It represents the switch in Home Assistant and handles
all the logic for turning a device on and off using SOLID principles.

- Turning On: Handled by TurnOnHandler via Bluetooth commands.
- Turning Off: Handled by TurnOffHandler via media_player service calls.
- State Management: Handled by StateManager and MiPowerCoordinator.
"""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import MiPowerCoordinator
from .exceptions import MiPowerError, TurnOnFailedReason
from .handlers.state_manager import StateManager
from .handlers.turn_off_handler import TurnOffHandler
from .handlers.turn_on_handler import TurnOnHandler

# Set up a specific logger for this file.
_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """
    Set up the MiPower switch platform from a config entry.

    This function is called by Home Assistant as part of the integration setup process
    (specifically, after the __init__.py's async_setup_entry runs). Its job is to
    create the switch entity and add it to Home Assistant.

    Args:
        hass: The Home Assistant instance.
        entry: The config entry for this integration instance.
        async_add_entities: A callback function to add the new entities to HA.
    """
    _LOGGER.debug(
        "[%s (%s)] Setting up MiPower switch.",
        entry.title,
        entry.entry_id,
    )

    # Retrieve the coordinator that was created and stored in __init__.py.
    # The coordinator is essential as it manages the state for our switch.
    coordinator: MiPowerCoordinator = hass.data[DOMAIN][entry.entry_id]
    _LOGGER.debug(
        "[%s (%s)] Retrieved coordinator from hass.data.",
        entry.title,
        coordinator._media_player_entity_id,
    )

    # Create an instance of the MiPowerSwitch entity.
    mipower_switch = MiPowerSwitch(coordinator, entry)
    _LOGGER.debug(
        "[%s (%s)] MiPowerSwitch entity created.",
        mipower_switch.device_info["name"],
        mipower_switch._state_manager.device_details.media_player_entity_id,
    )

    # Log all attributes of the switch entity before adding it to Home Assistant
    _LOGGER.debug(
        "MiPowerSwitch attributes before adding to HA: %s", mipower_switch.__dict__
    )
    _LOGGER.debug("MiPowerSwitch unique_id: %s", mipower_switch.unique_id)
    _LOGGER.debug("MiPowerSwitch name: %s", mipower_switch.name)
    _LOGGER.debug("MiPowerSwitch device_info: %s", mipower_switch.device_info)

    # Add the newly created switch entity to Home Assistant.
    async_add_entities([mipower_switch])
    _LOGGER.info("MiPower switch has been set up and added to Home Assistant.")
    _LOGGER.debug("Final MiPowerSwitch entity_id: %s", mipower_switch.entity_id)
    _LOGGER.debug("Final MiPowerSwitch name: %s", mipower_switch.name)
    _LOGGER.debug("Final MiPowerSwitch unique_id: %s", mipower_switch.unique_id)
    _LOGGER.debug("Final MiPowerSwitch device_info: %s", mipower_switch.device_info)


class MiPowerSwitch(CoordinatorEntity[MiPowerCoordinator], SwitchEntity):
    """
    Represents a MiPower switch entity using SOLID principles.

    This class uses dependency injection with separate handlers for different responsibilities:
    - StateManager: Manages state and configuration
    - TurnOnHandler: Handles turn-on operations
    - TurnOffHandler: Handles turn-off operations
    """

    def __init__(
        self,
        coordinator: MiPowerCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """
        Initialize the MiPowerSwitch with dependency injection.

        Args:
            coordinator: The data update coordinator.
            entry: The config entry.
        """
        _LOGGER.debug(
            "[%s (%s)] Initializing MiPowerSwitch.",
            entry.title,
            entry.entry_id,
        )

        # Initialize the parent CoordinatorEntity
        super().__init__(coordinator)

        # Inject dependencies
        self._state_manager = StateManager(coordinator, entry)
        self._turn_on_handler = TurnOnHandler(
            coordinator.hass, self._state_manager.device_details.media_player_entity_id
        )
        self._turn_off_handler = TurnOffHandler()

        # Set entity attributes from state manager
        attrs = self._state_manager.entity_attributes
        for key, value in attrs.items():
            setattr(self, key, value)

        _LOGGER.debug(
            "[%s (%s)] MiPowerSwitch initialized with handlers.",
            self.device_info["name"],
            self._state_manager.device_details.media_player_entity_id,
        )
        # Log all attributes of the switch entity after setting them from state manager
        _LOGGER.debug(
            "[%s (%s)] MiPowerSwitch attributes after state manager: %s",
            self.device_info["name"],
            self._state_manager.device_details.media_player_entity_id,
            self.__dict__,
        )
        _LOGGER.debug(
            "[%s (%s)] MiPowerSwitch unique_id (from state manager): %s",
            self.device_info["name"],
            self._state_manager.device_details.media_player_entity_id,
            self.unique_id,
        )
        _LOGGER.debug(
            "[%s (%s)] MiPowerSwitch name (from state manager): %s",
            self.device_info["name"],
            self._state_manager.device_details.media_player_entity_id,
            self.name,
        )
        _LOGGER.debug(
            "[%s (%s)] MiPowerSwitch device_info (from state manager): %s",
            self.device_info["name"],
            self._state_manager.device_details.media_player_entity_id,
            self.device_info,
        )

    @property
    def is_on(self) -> bool:
        """Return the current state of the switch."""
        return self._state_manager.is_on

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return True

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on using the turn-on handler."""
        device_details = self._state_manager.device_details
        timing_options = self._state_manager.timing_options

        _LOGGER.debug(
            "[%s (%s)] async_turn_on called.",
            self.device_info["name"],
            device_details.media_player_entity_id,
        )

        if self._state_manager.should_debounce_turn_on():
            return

        if self.is_on:
            _LOGGER.warning(
                "[%s (%s)] Turn on called, but switch is already on. Ignoring.",
                self._state_manager.media_player_friendly_name,
                device_details.media_player_entity_id,
            )
            return

        _LOGGER.info(
            "[%s (%s)] Executing turn-on logic for %s",
            self._state_manager.media_player_friendly_name,
            device_details.media_player_entity_id,
            f"{self._state_manager.media_player_friendly_name} ({device_details.mac_address})",
        )
        try:
            result = await self._turn_on_handler.turn_on(
                self.device_info["name"], device_details.mac_address, timing_options
            )

            if result is True:
                _LOGGER.info(
                    "[%s (%s)] Turn-on logic completed successfully.",
                    self.device_info["name"],
                    device_details.media_player_entity_id,
                )
            else:
                # If result is not True, it's a TurnOnFailedReason
                _LOGGER.warning(
                    "[%s (%s)] Turn-on logic failed: %s",
                    self.device_info["name"],
                    device_details.media_player_entity_id,
                    result.value
                    if isinstance(result, TurnOnFailedReason)
                    else "Bilinmeyen bir hata",
                )
        except MiPowerError as e:
            _LOGGER.error(
                "[%s (%s)] Failed to turn on device: %s",
                self.device_info["name"],
                device_details.media_player_entity_id,
                e,
                exc_info=True,
            )

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off using the turn-off handler."""
        device_details = self._state_manager.device_details
        timing_options = self._state_manager.timing_options

        _LOGGER.debug(
            "[%s (%s)] async_turn_off called.",
            self.device_info["name"],
            device_details.media_player_entity_id,
        )

        if self._state_manager.should_debounce_turn_off():
            _LOGGER.warning(
                "[%s (%s)] Turn off called too frequently. Debounced.",
                self.device_info["name"],
                device_details.media_player_entity_id,
            )
            return

        _LOGGER.info(
            "[%s (%s)] Executing turn-off logic for media_player: %s",
            self._state_manager.media_player_friendly_name,
            device_details.media_player_entity_id,
            f"{self._state_manager.media_player_friendly_name} ({device_details.media_player_entity_id})",
        )
        await self._turn_off_handler.turn_off(
            self.hass, device_details.media_player_entity_id, timing_options
        )
        _LOGGER.info(
            "[%s (%s)] Turn-off logic completed.",
            self.device_info["name"],
            device_details.media_player_entity_id,
        )
