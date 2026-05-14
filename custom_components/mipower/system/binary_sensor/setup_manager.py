"""
Binary Sensor Setup Manager - Single Responsibility Principle

This module implements binary sensor setup functionality following SOLID principles,
handling binary sensor platform setup and entity registration.
"""

import logging

from homeassistant.config_entries import ConfigEntry  # type: ignore[import]
from homeassistant.core import HomeAssistant  # type: ignore[import]
from homeassistant.helpers.entity_platform import AddEntitiesCallback  # type: ignore[import]

from ...const import DOMAIN
from .interface import BinarySensorSetupInterface

_LOGGER = logging.getLogger(__name__)


class BinarySensorSetupManager(BinarySensorSetupInterface):
    """Manages binary sensor setup and registration for Smartify.

    This class handles the setup of binary sensor entities for the Smartify integration,
    using dependency injection to receive the BinarySensorFactory and coordinating their
    registration with Home Assistant.
    """

    def __init__(self, sensor_factory):
        """Initialize the binary sensor setup manager.

        Args:
            sensor_factory: Binary sensor factory instance for dependency injection
        """
        self._sensor_factory = sensor_factory
        _LOGGER.debug("BinarySensorSetupManager initialized")

    async def setup_binary_sensors(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
    ) -> None:
        """Set up all binary sensors for the integration.

        Retrieves the coordinator from integration data and uses the sensor factory
        to create all sensor instances, then registers them with Home Assistant.

        Args:
            hass: Home Assistant instance.
            entry: Configuration entry.
            async_add_entities: Callback to add entities.
        """
        try:
            _LOGGER.info(
                f"Setting up binary sensors for Smartify integration '{entry.title}'"
            )

            # Get integration data from new architecture
            integration_data = hass.data[DOMAIN][entry.entry_id]
            coordinator = integration_data["coordinator"]

            # Create all binary sensors using the factory
            sensors = self._sensor_factory.create_all_binary_sensors(entry, coordinator)

            # Add sensors to Home Assistant
            async_add_entities(sensors)

            _LOGGER.info(
                f"Successfully set up {len(sensors)} binary sensors for '{entry.title}'"
            )

        except KeyError as e:
            _LOGGER.error(
                f"Missing integration data for entry {entry.entry_id}: {e}",
                exc_info=True,
            )
            raise
        except Exception as e:
            _LOGGER.error(
                f"Error setting up binary sensors for '{entry.title}': {e}",
                exc_info=True,
            )
            raise
