"""
Sensor Setup Manager - Single Responsibility Principle

This module implements sensor setup functionality following SOLID principles,
handling sensor platform setup and entity registration.
"""

import logging

from homeassistant.config_entries import ConfigEntry  # type: ignore[import]
from homeassistant.core import HomeAssistant  # type: ignore[import]
from homeassistant.helpers.entity_platform import AddEntitiesCallback  # type: ignore[import]

from ...const import DOMAIN
from .interface import SensorFactoryInterface, SensorSetupInterface

_LOGGER = logging.getLogger(__name__)


class SensorSetupManager(SensorSetupInterface):
    """Manages sensor setup and registration for Smartify.

    This class handles the setup of sensor entities for the Smartify integration,
    using the SensorFactory to create sensor instances and coordinating their
    registration with Home Assistant.
    """

    def __init__(self, sensor_factory: SensorFactoryInterface):
        """Initialize the sensor setup manager.

        Args:
            sensor_factory: Factory for creating sensor instances
        """
        self._sensor_factory = sensor_factory
        _LOGGER.debug("SensorSetupManager initialized with injected factory")

    async def setup_sensors(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
    ) -> None:
        """Set up all sensors for the integration.

        Retrieves the coordinator from integration data and uses the sensor factory
        to create all sensor instances, then registers them with Home Assistant.

        Args:
            hass: Home Assistant instance.
            entry: Configuration entry.
            async_add_entities: Callback to add entities.
        """
        try:
            _LOGGER.info(f"Setting up sensors for Smartify integration '{entry.title}'")

            # Get integration data from new architecture
            integration_data = hass.data[DOMAIN][entry.entry_id]
            coordinator = integration_data["coordinator"]

            # Create all sensors using the factory
            sensors = self._sensor_factory.create_all_sensors(entry, coordinator, hass)

            # Add sensors to Home Assistant
            async_add_entities(sensors)

            _LOGGER.info(
                f"Successfully set up {len(sensors)} sensors for '{entry.title}'"
            )

        except KeyError as e:
            _LOGGER.error(
                f"Missing integration data for entry {entry.entry_id}: {e}",
                exc_info=True,
            )
            raise
        except Exception as e:
            _LOGGER.error(
                f"Error setting up sensors for '{entry.title}': {e}",
                exc_info=True,
            )
            raise
