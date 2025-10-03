"""
Switch platform for the MiPower integration.

This file defines the main switch entity for the integration. The MiPowerSwitch class
is the core of this platform. It represents the switch in Home Assistant and handles
all the logic for turning a device on and off.

- Turning On: Is handled by executing a Bluetooth command (`bluetoothctl`).
- Turning Off: Is handled by calling the 'turn_off' service on the linked media_player entity.
- State Management: The switch's state (on/off) is not managed by the switch itself,
  but is coordinated by the MiPowerCoordinator. The switch entity subscribes to the
  coordinator, which tracks the state of the linked media_player entity. This ensures
  the switch is always in sync with the actual device state.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_MAC
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

# Import constants and other necessary components from within the integration.
from .const import (
    CONF_MEDIA_PLAYER_ENTITY_ID,
    CONF_OFF_DEBOUNCE,
    CONF_ON_DEBOUNCE,
    CONF_INTER_STEP_DELAY,
    CONF_PAIR_TIMEOUT,
    CONF_SCAN_DURATION,
    CONF_SPAWN_TIMEOUT,
    CONF_TRUST_TIMEOUT,
    DEFAULT_DEVICE_ICON,
    DEFAULT_ENTITY_ICON,
    DEFAULT_INTER_STEP_DELAY,
    DEFAULT_OFF_DEBOUNCE_SECONDS,
    DEFAULT_ON_DEBOUNCE_SECONDS,
    DEFAULT_PAIR_TIMEOUT,
    DEFAULT_SCAN_DURATION,
    DEFAULT_SPAWN_TIMEOUT,
    DEFAULT_TRUST_TIMEOUT,
    DEVICE_NAME_PREFIX,
    DOMAIN,
    MANUFACTURER,
)
from .coordinator import MiPowerCoordinator
from .api.turn_off import perform_turn_off
from .api.turn_on import perform_turn_on_sync

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
    _LOGGER.debug("Setting up MiPower switch for entry_id: %s", entry.entry_id)

    # Retrieve the coordinator that was created and stored in __init__.py.
    # The coordinator is essential as it manages the state for our switch.
    coordinator: MiPowerCoordinator = hass.data[DOMAIN][entry.entry_id]
    _LOGGER.debug("Retrieved coordinator from hass.data.")

    # Create an instance of the MiPowerSwitch entity.
    mipower_switch = MiPowerSwitch(coordinator, entry)
    _LOGGER.debug("MiPowerSwitch entity created.")

    # Add the newly created switch entity to Home Assistant.
    async_add_entities([mipower_switch])
    _LOGGER.info("MiPower switch has been set up and added to Home Assistant.")


class MiPowerSwitch(CoordinatorEntity[MiPowerCoordinator], SwitchEntity):
    """
    Represents a MiPower switch entity.

    This class inherits from CoordinatorEntity, which links it to the MiPowerCoordinator,
    and SwitchEntity, which makes it a switch. The state is automatically managed by the
    CoordinatorEntity parent class.
    """

    # This attribute tells Home Assistant that the entity's name should be derived
    # from the device name. When set to True and the entity's `name` is None,
    # the entity will inherit the device's name. This is the recommended best practice.
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MiPowerCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """
        Initialize the MiPowerSwitch.

        Args:
            coordinator: The data update coordinator that manages the switch's state.
            entry: The config entry containing the user's configuration.
        """
        _LOGGER.debug("Initializing MiPowerSwitch with entry_id: %s", entry.entry_id)
        # Initialize the parent CoordinatorEntity. This links the switch to the
        # coordinator, so it gets state updates automatically.
        super().__init__(coordinator)

        # Store the config entry object on the instance so we can access its
        # data and options throughout the class.
        self._entry = entry

        # This timestamp is used to handle "debouncing" for the turn_off action,
        # preventing it from being called too frequently in a short period.
        self._last_off_call_time = 0

        # --- Entity Attributes ---
        # These attributes define the core properties of the entity in Home Assistant.

        # By setting the name to None (in combination with _attr_has_entity_name = True),
        # we tell Home Assistant to use the device's name as the entity's friendly name.
        self._attr_name = None

        # Set the icon that will be displayed in the Home Assistant UI.
        self._attr_icon = DEFAULT_ENTITY_ICON

        # Set a unique ID for the entity. This is crucial for Home Assistant to
        # track the entity across restarts. We use the config entry's unique ID.
        self._attr_unique_id = entry.entry_id
        _LOGGER.debug("Unique ID set to: %s", self._attr_unique_id)

        # --- Device Information ---
        # This links the entity to a device in Home Assistant's device registry.
        # It allows users to see all entities for a physical device grouped together.
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": f"{DEVICE_NAME_PREFIX}{entry.title}",
            "manufacturer": MANUFACTURER,
            "model": f"{DEVICE_NAME_PREFIX}Home Assistant custom integration",
        }
        _LOGGER.debug("Device info set to: %s", self._attr_device_info)

    @property
    def is_on(self) -> bool:
        """
        Return the current state of the switch.

        This property is automatically kept up-to-date by the CoordinatorEntity
        parent class. It simply returns the latest data from the coordinator.
        """
        # self.coordinator.data is the boolean state managed by our MiPowerCoordinator.
        is_on_state = self.coordinator.data
        _LOGGER.debug("Reporting switch state as: %s", is_on_state)
        return is_on_state

    @property
    def _mac_address(self) -> str:
        """Return the MAC address from the config entry."""
        # This is a helper property to conveniently access the MAC address.
        mac = self._entry.data.get(CONF_MAC)
        _LOGGER.debug("Retrieved MAC address: %s", mac)
        return mac

    @property
    def _timing_options(self) -> dict[str, int | float]:
        """
        Return all timing-related options from the config entry.

        This helper property consolidates all timing settings, falling back from
        user-configured options to the initial setup data, and finally to the
        default constants. This ensures the most specific setting is always used.
        """
        # For each timing setting, we check options, then data, then use the default.
        options = self._entry.options
        data = self._entry.data
        timings = {
            CONF_ON_DEBOUNCE: options.get(CONF_ON_DEBOUNCE, data.get(CONF_ON_DEBOUNCE, DEFAULT_ON_DEBOUNCE_SECONDS)),
            CONF_OFF_DEBOUNCE: options.get(CONF_OFF_DEBOUNCE, data.get(CONF_OFF_DEBOUNCE, DEFAULT_OFF_DEBOUNCE_SECONDS)),
            CONF_INTER_STEP_DELAY: options.get(CONF_INTER_STEP_DELAY, data.get(CONF_INTER_STEP_DELAY, DEFAULT_INTER_STEP_DELAY)),
            CONF_SPAWN_TIMEOUT: options.get(CONF_SPAWN_TIMEOUT, data.get(CONF_SPAWN_TIMEOUT, DEFAULT_SPAWN_TIMEOUT)),
            CONF_PAIR_TIMEOUT: options.get(CONF_PAIR_TIMEOUT, data.get(CONF_PAIR_TIMEOUT, DEFAULT_PAIR_TIMEOUT)),
            CONF_TRUST_TIMEOUT: options.get(CONF_TRUST_TIMEOUT, data.get(CONF_TRUST_TIMEOUT, DEFAULT_TRUST_TIMEOUT)),
            CONF_SCAN_DURATION: options.get(CONF_SCAN_DURATION, data.get(CONF_SCAN_DURATION, DEFAULT_SCAN_DURATION)),
        }
        _LOGGER.debug("Retrieved timing options: %s", timings)
        return timings

    async def async_turn_on(self, **kwargs: Any) -> None:
        """
        Turn the switch on.

        This method is called when a user toggles the switch on in Home Assistant.
        It runs the synchronous 'turn_on' bluetoothctl logic in a separate thread
        to avoid blocking the main Home Assistant event loop.
        """
        _LOGGER.debug("async_turn_on called.")
        # The coordinator already tells us the state, so we check if it's already on.
        if self.is_on:
            _LOGGER.warning("Turn on called, but switch is already on. Ignoring.")
            return

        # Get the latest timing settings from our helper property.
        timing = self._timing_options
        _LOGGER.info("Executing turn-on logic for MAC: %s", self._mac_address)

        # The `perform_turn_on_sync` function contains blocking I/O (subprocess calls),
        # so it must be run in an executor thread to not block Home Assistant's event loop.
        await self.hass.async_add_executor_job(
            perform_turn_on_sync,
            self._mac_address,
            timing[CONF_ON_DEBOUNCE],
            timing[CONF_SPAWN_TIMEOUT],
            timing[CONF_PAIR_TIMEOUT],
            timing[CONF_TRUST_TIMEOUT],
            timing[CONF_INTER_STEP_DELAY],
            timing[CONF_SCAN_DURATION],
        )
        _LOGGER.info("Turn-on logic has been executed.")

    async def async_turn_off(self, **kwargs: Any) -> None:
        """
        Turn the switch off.

        This method is called when a user toggles the switch off in Home Assistant.
        It calls the 'turn_off' service on the linked media_player entity.
        """
        _LOGGER.debug("async_turn_off called.")
        # Get the latest timing settings.
        timing = self._timing_options
        off_debounce_seconds = timing[CONF_OFF_DEBOUNCE]
        now = time.time()

        # Debouncing prevents the turn_off logic from running too frequently.
        # This can be useful if the switch is toggled rapidly.
        if now - self._last_off_call_time < off_debounce_seconds:
            _LOGGER.warning(
                "Turn off called too frequently. Debounced for %s seconds. Ignoring call.",
                off_debounce_seconds,
            )
            return

        # Update the timestamp of the last call.
        self._last_off_call_time = now

        # Get the entity ID of the media player to turn off.
        media_player_entity_id = self._entry.data[CONF_MEDIA_PLAYER_ENTITY_ID]
        _LOGGER.info(
            "Executing turn-off logic for media_player: %s", media_player_entity_id
        )

        # Call the asynchronous turn_off function.
        await perform_turn_off(self.hass, media_player_entity_id)
        _LOGGER.info("Turn-off logic has been executed.")