"""State manager for MiPower switch."""

import logging
from typing import Any, Dict

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_MAC

from ..const import (
    CONF_DEVICE_ID,
    CONF_INTER_STEP_DELAY,
    CONF_MEDIA_PLAYER_ENTITY_ID,
    CONF_OFF_DEBOUNCE,
    CONF_ON_DEBOUNCE,
    CONF_SCAN_DURATION,
    CONF_SCAN_STOP_TIMEOUT,
    CONF_SIGNAL_DURATION,
    CONF_SPAWN_TIMEOUT,
    DEFAULT_ENTITY_ICON,
    DEFAULT_INTER_STEP_DELAY,
    DEFAULT_OFF_DEBOUNCE_SECONDS,
    DEFAULT_ON_DEBOUNCE_SECONDS,
    DEFAULT_SCAN_DURATION,
    DEFAULT_SCAN_STOP_TIMEOUT,
    DEFAULT_SIGNAL_DURATION,
    DEFAULT_SPAWN_TIMEOUT,
    DEVICE_NAME_PREFIX,
    DOMAIN,
    MANUFACTURER,
)
from ..coordinator import MiPowerCoordinator
from ..models import DeviceDetails, TimingOptions

_LOGGER = logging.getLogger(__name__)


class StateManager:
    """Manages state and configuration for MiPower switch."""

    def __init__(self, coordinator: MiPowerCoordinator, entry: ConfigEntry) -> None:
        """
        Initialize the state manager.

        Args:
            coordinator: The data coordinator.
            entry: The config entry.
        """
        self.coordinator = coordinator
        self.entry = entry
        self._last_off_call_time = 0
        self._last_on_call_time = 0
        self._load_config()

    def _load_config(self) -> None:
        """Load and parse configuration from the ConfigEntry."""
        options = self.entry.options
        data = self.entry.data

        self.device_details = DeviceDetails(
            mac_address=data.get(CONF_MAC, ""),
            media_player_entity_id=data.get(CONF_MEDIA_PLAYER_ENTITY_ID, ""),
            device_id=data.get(CONF_DEVICE_ID),
            name=None,  # Varlık adını boş bırakarak cihaz adından türetilmesini sağla
        )

        self.timing_options = TimingOptions(
            on_debounce=options.get(
                CONF_ON_DEBOUNCE,
                data.get(
                    CONF_ON_DEBOUNCE,
                    DEFAULT_ON_DEBOUNCE_SECONDS,
                ),
            ),
            off_debounce=options.get(
                CONF_OFF_DEBOUNCE,
                data.get(CONF_OFF_DEBOUNCE, DEFAULT_OFF_DEBOUNCE_SECONDS),
            ),
            inter_step_delay=options.get(
                CONF_INTER_STEP_DELAY,
                data.get(CONF_INTER_STEP_DELAY, DEFAULT_INTER_STEP_DELAY),
            ),
            spawn_timeout=options.get(
                CONF_SPAWN_TIMEOUT,
                data.get(CONF_SPAWN_TIMEOUT, DEFAULT_SPAWN_TIMEOUT),
            ),
            signal_duration=options.get(
                CONF_SIGNAL_DURATION,
                data.get(CONF_SIGNAL_DURATION, DEFAULT_SIGNAL_DURATION),
            ),
            scan_duration=options.get(
                CONF_SCAN_DURATION,
                data.get(CONF_SCAN_DURATION, DEFAULT_SCAN_DURATION),
            ),
            scan_stop_timeout=options.get(
                CONF_SCAN_STOP_TIMEOUT,
                data.get(CONF_SCAN_STOP_TIMEOUT, DEFAULT_SCAN_STOP_TIMEOUT),
            ),
        )

    @property
    def is_on(self) -> bool:
        """Return the current state of the switch."""
        return self.coordinator.data

    @property
    def device_info(self) -> Dict[str, Any]:
        """Return device info for Home Assistant."""
        # The device name is the prefixed title of the config entry.
        device_info_data = {
            "identifiers": {(DOMAIN, self.entry.entry_id)},
            "name": f"{DEVICE_NAME_PREFIX}{self.entry.title}",
            "manufacturer": MANUFACTURER,
            "model": f"{DEVICE_NAME_PREFIX} Integration",
            "suggested_area": None,  # Konum modalını tetiklemek için eklendi
        }
        _LOGGER.debug("StateManager device_info: %s", device_info_data)
        return device_info_data

    @property
    def media_player_friendly_name(self) -> str:
        """Return the friendly name of the media player entity."""
        return self.entry.title

    @property
    def entity_attributes(self) -> Dict[str, Any]:
        """Return entity attributes."""
        entity_attributes_data = {
            "_attr_has_entity_name": True,
            "_attr_name": None,  # Varlık adını boş bırakarak cihaz adından türetilmesini sağla
            "_attr_icon": DEFAULT_ENTITY_ICON,
            "_attr_unique_id": self.entry.entry_id,
            "_attr_device_info": self.device_info,
        }
        _LOGGER.debug("StateManager entity_attributes: %s", entity_attributes_data)
        return entity_attributes_data

    def should_debounce_turn_off(self) -> bool:
        """Check if turn-off should be debounced."""
        import time

        now = time.time()
        off_debounce_seconds = self.timing_options.off_debounce
        if now - self._last_off_call_time < off_debounce_seconds:
            _LOGGER.warning(
                "[%s (%s)] Turn off called too frequently. Debounced for %s seconds.",
                self.media_player_friendly_name,
                self.device_details.media_player_entity_id,
                off_debounce_seconds,
            )
            return True
        self._last_off_call_time = now
        return False

    def should_debounce_turn_on(self) -> bool:
        """Check if turn-on should be debounced."""
        import time

        now = time.time()
        on_debounce_seconds = self.timing_options.on_debounce
        if now - self._last_on_call_time < on_debounce_seconds:
            _LOGGER.warning(
                "[%s (%s)] Turn on called too frequently. Debounced for %s seconds.",
                self.media_player_friendly_name,
                self.device_details.media_player_entity_id,
                on_debounce_seconds,
            )
            return True
        self._last_on_call_time = now
        return False
