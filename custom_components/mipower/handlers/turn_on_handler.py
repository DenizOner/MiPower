"""Turn-on handler for MiPower integration."""

import logging
import time

from homeassistant.core import HomeAssistant

from ..core.interfaces import IBluetoothService, ITurnOnHandler
from ..models import TimingOptions
from ..services.bluetooth import BluetoothService, TurnOnFailedReason

_LOGGER = logging.getLogger(__name__)


class TurnOnHandler(ITurnOnHandler):
    """Handles turn-on operations for MiPower devices."""

    def __init__(
        self,
        hass: HomeAssistant,
        media_player_entity_id: str,
        bluetooth_service: IBluetoothService | None = None,
    ) -> None:
        """
        Initialize the turn-on handler.

        Args:
            hass: The Home Assistant instance.
            media_player_entity_id: The entity ID of the associated media player.
            bluetooth_service: An instance of a class that implements IBluetoothService.
                               This allows for dependency injection and easier testing.
        """
        self._hass = hass
        self._media_player_entity_id = media_player_entity_id
        self._last_call_time = 0
        self._bluetooth_service = bluetooth_service or BluetoothService()

    async def turn_on(
        self, name: str, mac_address: str, timing_options: TimingOptions
    ) -> bool | TurnOnFailedReason:
        """
        Turn on the device via Bluetooth.

        Args:
            name: The name of the media player.
            mac_address: The MAC address of the device.
            timing_options: Timing configuration options.

        Returns:
            True if successful, False otherwise.
        """
        now = time.time()
        debounce_seconds = timing_options.on_debounce

        if now - self._last_call_time < debounce_seconds:
            _LOGGER.warning(
                "[%s (%s)] Turn on called too frequently. Debounced for %s seconds.",
                name,
                self._media_player_entity_id,
                debounce_seconds,
            )
            return TurnOnFailedReason.ALREADY_ON

        _LOGGER.info(
            "[%s (%s)] Attempting to wake up using Bluetooth.",
            name,
            self._media_player_entity_id,
        )

        # Check if media player is already on
        media_player_state = self._hass.states.get(self._media_player_entity_id)
        if media_player_state and media_player_state.state == "on":
            _LOGGER.info(
                "[%s (%s)] Media player is already on. No action needed.",
                name,
                self._media_player_entity_id,
            )
            self._last_call_time = now
            return True

        # Delegate the Bluetooth wake-up call to the injected service.
        result = await self._bluetooth_service.wake_up(
            self._hass, name, mac_address, self._media_player_entity_id, timing_options
        )

        if result is True:
            self._last_call_time = now
            return True
        else:
            # If result is not True, it's a TurnOnFailedReason
            _LOGGER.warning(
                "[%s (%s)] Bluetooth wake-up failed: %s",
                name,
                self._media_player_entity_id,
                result.value
                if isinstance(result, TurnOnFailedReason)
                else "An unknown error occurred",
            )
            return result
