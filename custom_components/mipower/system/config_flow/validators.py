"""Validators for Smartify configuration flow.

This module provides validation services following SOLID principles,
separating validation logic from the main configuration flow.
"""

import logging
from types import ModuleType
from typing import Optional

from homeassistant.core import HomeAssistant  # type: ignore

from ...di.container import DependencyContainer
from ...helpers.config_flow.validator_interface import ConfigValidatorInterface
from ...helpers.device.registry_service import DeviceRegistryService
from ...helpers.entity.registry_service import EntityRegistryService
from ...helpers.logger.config_flow_logger import validator_logging

_LOGGER = logging.getLogger(__name__)


class ConfigValidator(ConfigValidatorInterface):
    """Validator for configuration data following Single Responsibility Principle."""

    def __init__(self):
        """Private constructor - use create() factory method instead."""
        self.container: Optional[DependencyContainer] = None
        self.hass: Optional[HomeAssistant] = None
        self.remote_criteria: Optional[ModuleType] = None
        # Registry services for SOLID compliance
        self.device_registry_service: Optional[DeviceRegistryService] = None
        self.entity_registry_service: Optional[EntityRegistryService] = None

    @validator_logging()
    @staticmethod
    async def create(container: DependencyContainer):
        """Create and initialize the validator with dependency injection container.

        Args:
            container: The dependency injection container

        Returns:
            ConfigValidator: Initialized validator instance
        """
        validator = ConfigValidator()
        validator.container = container
        validator.hass = container.hass
        # Resolve dependencies for SOLID DIP compliance
        validator.remote_criteria = await container.resolve("RemoteCriteria")
        # Initialize registry services for SOLID principle compliance
        validator.device_registry_service = DeviceRegistryService()
        validator.entity_registry_service = EntityRegistryService(validator.hass)
        return validator

    @validator_logging()
    async def validate_power_entity(self, entity_id: str) -> bool:
        """Validate that the selected entity is a valid power entity.

        Checks if the provided entity ID corresponds to a valid power measurement
        sensor (power, current, or voltage) with appropriate attributes and no
        conflicting battery sensors on the same device.

        Args:
            entity_id: The entity ID to validate.

        Returns:
            bool: True if the entity is a valid power sensor, False otherwise.
        """
        try:
            # Check if registry services are initialized for SOLID compliance
            if not self.entity_registry_service:
                _LOGGER.error(
                    "Entity registry service not initialized",
                    exc_info=True,
                )
                return False

            # Use helpers/entity for SOLID compliance
            entity_registry = self.entity_registry_service.get_entity_registry(
                self.hass
            )
            entity_entry = entity_registry.async_get(entity_id)
            if not entity_entry:
                _LOGGER.warning(f"Entity '{entity_id}' not found in registry")
                return False

            # Domain check
            if entity_entry.domain not in ["sensor"]:
                _LOGGER.warning(
                    f"Entity '{entity_id}' is not a sensor "
                    f"(domain: {entity_entry.domain})"
                )
                return False

            # Suffix check
            has_valid_suffix = any(
                entity_id.endswith(s) for s in ["_power", "_current", "_voltage"]
            )
            if not has_valid_suffix:
                _LOGGER.warning(
                    f"Entity '{entity_id}' does not have valid power suffix"
                )
                return False

            # Check if entity meets power criteria (live state is optional for setup)
            # Check hass availability for SOLID compliance
            if not self.hass:
                _LOGGER.error(
                    "Home Assistant instance not available",
                    exc_info=True,
                )
                return False
            live_state = self.hass.states.get(entity_id)
            if live_state:
                # Device class check if state is available
                actual_class = live_state.attributes.get("device_class")
                if actual_class and actual_class not in [
                    "power",
                    "current",
                    "voltage",
                ]:
                    _LOGGER.warning(
                        f"Entity '{entity_id}' has invalid device_class: {actual_class}"
                    )
                    return False
            else:
                _LOGGER.info(
                    f"Entity '{entity_id}' has no live state yet (this is OK during setup)"
                )

            # Battery check - ensure no battery sensor on same device (use helpers/entity)
            device_entities = self.entity_registry_service.get_entities_for_device(
                self.hass, entity_entry.device_id
            )
            for ent in device_entities:
                if ent.entity_id != entity_id:
                    state = self.hass.states.get(ent.entity_id)
                    if state and state.attributes.get("device_class") == "battery":
                        _LOGGER.warning(
                            f"Device has battery sensor '{ent.entity_id}', "
                            "skipping power sensor"
                        )
                        return False

            return True
        except Exception as e:
            _LOGGER.error(
                f"Error validating power entity {entity_id}: {e}",
                exc_info=True,
            )
            return False

    @validator_logging()
    def convert_remote_device_to_entity(self, remote_device_id: str) -> str:
        """Convert remote device ID to entity ID if needed.

        Args:
            remote_device_id: The remote device or entity ID.

        Returns:
            str: The entity ID for the remote device.
        """
        # Check if registry services are initialized for SOLID compliance
        if not self.entity_registry_service:
            _LOGGER.error(
                "Entity registry service not initialized",
                exc_info=True,
            )
            return remote_device_id

        entity_registry = self.entity_registry_service.get_entity_registry(self.hass)
        entity_entry = entity_registry.async_get(remote_device_id)
        if entity_entry:
            # It's already an entity ID
            return remote_device_id
        else:
            # Check if it's a device ID by looking for remote entities on this device
            try:
                # Use helpers/entity for SOLID DIP compliance
                device_entries = self.entity_registry_service.get_entities_for_device(
                    self.hass, remote_device_id
                )
                # Check remote_criteria availability for SOLID compliance
                if not self.remote_criteria or not hasattr(
                    self.remote_criteria, "VALID_REMOTE_DOMAINS"
                ):
                    _LOGGER.error(
                        "Remote criteria not initialized or missing VALID_REMOTE_DOMAINS",
                        exc_info=True,
                    )
                    return remote_device_id
                remote_entity = next(
                    (
                        ent
                        for ent in device_entries
                        if ent.domain in self.remote_criteria.VALID_REMOTE_DOMAINS
                    ),
                    None,
                )
                if remote_entity:
                    return remote_entity.entity_id
                else:
                    # Get device friendly name using helpers/device
                    device_name = self._get_device_name(remote_device_id)
                    _LOGGER.warning(
                        f"No remote entity found for device '{device_name} "
                        f"({remote_device_id})'. Using device ID as entity ID."
                    )
                    # For now, use the device ID as entity ID if no remote entity found
                    return remote_device_id
            except Exception as device_error:
                # Get device friendly name using helpers/device
                device_name = self._get_device_name(remote_device_id)
                _LOGGER.warning(
                    f"Error looking up device '{device_name} ({remote_device_id})': "
                    f"{device_error}. Assuming it's already an entity ID."
                )
                # If device lookup fails, assume it's already an entity ID
                return remote_device_id

    @validator_logging()
    def _get_device_name(self, device_id: str) -> str:
        """Get device friendly name from device registry using helpers/device."""
        try:
            # Check if device registry service is initialized for SOLID compliance
            if not self.device_registry_service:
                _LOGGER.error(
                    "Device registry service not initialized",
                    exc_info=True,
                )
                return "Unknown Device"

            # Use helpers/device for SOLID compliance
            device_entry = self.device_registry_service.get_device_by_id(
                self.hass, device_id
            )
            return device_entry.name if device_entry else "Unknown Device"
        except Exception:
            return "Unknown Device"
