"""
Service Registry - Single Responsibility Principle

This module implements service registration functionality following SOLID principles,
handling service registration and unregistration for Smartify integration.
"""

import logging

import homeassistant.helpers.config_validation as cv  # type: ignore[import]
import voluptuous as vol  # type: ignore[import]
from homeassistant.core import HomeAssistant  # type: ignore[import]
from homeassistant.helpers import entity_platform  # type: ignore[import]

from ...const import (
    ATTR_SCRIPT_ENTITY_ID,
    SERVICE_CALIBRATE,
    SERVICE_FORCE_VERIFY,
    SERVICE_SEND_COMMAND,
)
from .interface import ServiceRegistryInterface

_LOGGER = logging.getLogger(__name__)


class ServiceRegistry(ServiceRegistryInterface):
    """Handles service registration and unregistration for Smartify.

    This class is responsible for registering and unregistering Smartify services
    with Home Assistant. Follows Single Responsibility Principle by focusing only
    on service registry operations.
    """

    def __init__(self):
        """Initialize the service registry."""
        _LOGGER.debug("ServiceRegistry initialized")

    async def register_services(self, hass: HomeAssistant) -> bool:
        """Register all Smartify services with Home Assistant.

        Registers send_command, force_verify, and calibrate services
        on the entity platform.

        Args:
            hass: Home Assistant instance.

        Returns:
            True if all services registered successfully, False otherwise.
        """
        try:
            _LOGGER.info(
                "Registering Smartify services with SOLID architecture support"
            )

            platform = entity_platform.async_get_current_platform()

            if platform is None:
                _LOGGER.warning(
                    "No current platform set, skipping service registration"
                )
                return False

            # Register send_command service
            try:
                platform.async_register_entity_service(
                    SERVICE_SEND_COMMAND,
                    {vol.Required(ATTR_SCRIPT_ENTITY_ID): cv.entity_id},
                    "async_send_command",
                )
                _LOGGER.debug("send_command service registered successfully")
            except Exception as err:
                _LOGGER.error(
                    "Error registering send_command service: %s",
                    err,
                    exc_info=True,
                )
                return False

            # Register force_verify service
            try:
                platform.async_register_entity_service(
                    SERVICE_FORCE_VERIFY, {}, "async_force_verify"
                )
                _LOGGER.debug("force_verify service registered successfully")
            except Exception as err:
                _LOGGER.error(
                    "Error registering force_verify service: %s",
                    err,
                    exc_info=True,
                )
                return False

            # Register calibrate service
            try:
                platform.async_register_entity_service(
                    SERVICE_CALIBRATE, {}, "async_calibrate"
                )
                _LOGGER.debug("calibrate service registered successfully")
            except Exception as err:
                _LOGGER.error(
                    "Error registering calibrate service: %s",
                    err,
                    exc_info=True,
                )
                return False

            _LOGGER.info("All Smartify services registered successfully")
            return True

        except Exception as e:
            _LOGGER.error(
                "Critical error during service registration: %s",
                e,
                exc_info=True,
            )
            return False

    def unregister_services(self, hass: HomeAssistant) -> bool:
        """Unregister Smartify services from Home Assistant.

        Services are automatically handled by the entity platform during
        component unloading, so this method primarily logs the operation.

        Args:
            hass: Home Assistant instance.

        Returns:
            True if unregistration completed successfully.
        """
        try:
            _LOGGER.info("Unregistering Smartify services")
            _LOGGER.debug(
                "Services will be automatically removed by the entity platform"
            )
            return True
        except Exception as e:
            _LOGGER.error(
                "Error during service unregistration: %s",
                e,
                exc_info=True,
            )
            return False
