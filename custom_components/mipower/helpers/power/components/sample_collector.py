"""
Sample Collector Component - Power Sample Collection

This module implements power sample collection from Home Assistant sensors.
It handles sensor data retrieval, validation, and PowerSample creation
with proper error handling and retry logic.

Classes:
    SampleCollector: Power sample collection from Home Assistant sensors.
"""

import logging
from typing import Optional

from homeassistant.core import HomeAssistant  # type: ignore[import]

from ....helpers.errors.exceptions import ValidationError
from ..power_analyzer_interface import SampleCollectorInterface
from ..sampler import PowerSample

_LOGGER = logging.getLogger(__name__)


class SampleCollector(SampleCollectorInterface):
    """Power sample collection from Home Assistant sensors.

    Handles sensor data retrieval, validation, and PowerSample creation
    with proper error handling and retry logic.
    """

    def __init__(self, hass: HomeAssistant, power_entity_id: str):
        """Initialize sample collector.

        Args:
            hass: Home Assistant instance.
            power_entity_id: Entity ID of power sensor.
        """
        if not power_entity_id or not isinstance(power_entity_id, str):
            raise ValidationError("power_entity_id must be a non-empty string")

        self._hass = hass
        self.power_entity_id = power_entity_id
        _LOGGER.debug("SampleCollector initialized for: %s", power_entity_id)

    async def collect_sample(self) -> Optional[PowerSample]:
        """Collect single power sample from sensor.

        Returns:
            Optional[PowerSample]: Validated sample or None if collection failed.
        """
        try:
            state = self._hass.states.get(self.power_entity_id)

            if not state:
                _LOGGER.debug("Sensor %s not available", self.power_entity_id)
                return None

            if state.state in ("unknown", "unavailable"):
                _LOGGER.debug("Sensor %s state: %s", self.power_entity_id, state.state)
                return None

            try:
                power_value = float(state.state)
            except (ValueError, TypeError):
                _LOGGER.warning(
                    "Invalid power value from %s: %s", self.power_entity_id, state.state
                )
                return None

            from datetime import datetime

            sample = PowerSample(
                value=power_value, timestamp=datetime.now(), state=state.state
            )

            if not sample.is_valid():
                _LOGGER.warning("Invalid power sample: %.2fW", power_value)
                return None

            return sample

        except Exception as e:
            _LOGGER.error(
                "Error collecting sample from %s: %s",
                self.power_entity_id,
                e,
                exc_info=True,
            )
            return None

    def get_entity_id(self) -> str:
        """Get the entity ID being monitored.

        Returns:
            str: The power sensor entity ID.
        """
        return self.power_entity_id

    def is_available(self) -> bool:
        """Check if the power sensor is currently available.

        Returns:
            bool: True if sensor exists and is not unavailable, False otherwise.
        """
        state = self._hass.states.get(self.power_entity_id)
        if not state:
            return False
        return state.state not in ("unknown", "unavailable")

    def get_current_value(self) -> Optional[float]:
        """Get the current power value without creating a sample.

        Returns:
            Optional[float]: Current power value or None if unavailable.
        """
        state = self._hass.states.get(self.power_entity_id)
        if not state or state.state in ("unknown", "unavailable"):
            return None

        try:
            return float(state.state)
        except (ValueError, TypeError):
            return None

    def get_sensor_state(self) -> Optional[str]:
        """Get the raw state string from the sensor.

        Returns:
            Optional[str]: Current state string or None if sensor not found.
        """
        state = self._hass.states.get(self.power_entity_id)
        return state.state if state else None
