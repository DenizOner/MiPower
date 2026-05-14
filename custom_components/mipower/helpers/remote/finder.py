"""Remote device finder implementation for Smartify integration.

This module provides discovery functionality for remote control devices.
"""

import logging
from typing import Any, Dict, List

from homeassistant.helpers import device_registry as dr  # type: ignore[import]
from homeassistant.helpers import entity_registry as er  # type: ignore[import]

from ...di.container import DependencyContainer
from ..device.registry_service import DeviceRegistryService
from .remote_interface import RemoteDeviceFinderInterface

_LOGGER: logging.Logger = logging.getLogger(__name__)


class RemoteDeviceFinder(RemoteDeviceFinderInterface):
    """Implementation of remote device discovery."""

    def __init__(self, container: DependencyContainer):
        """Initialize the remote device finder."""
        self.container = container
        self.hass = container.hass

    async def _get_dependencies(self):
        """Get dependencies from container with fallback."""
        try:
            _LOGGER.debug(
                "Attempting to resolve RemoteDeviceValidatorInterface from container"
            )
            validator = await self.container.resolve("RemoteDeviceValidatorInterface")
            _LOGGER.debug("RemoteDeviceValidatorInterface resolved successfully")

            _LOGGER.debug("Attempting to resolve remote_criteria from container")
            remote_criteria = await self.container.resolve("remote_criteria")
            _LOGGER.debug("remote_criteria resolved successfully")

            device_registry_service = DeviceRegistryService()
            _LOGGER.debug("All dependencies resolved from container successfully")
            return validator, remote_criteria, device_registry_service
        except Exception as e:
            _LOGGER.debug(f"Container resolution failed: {e}, using fallbacks")
            _LOGGER.debug("Exception details", exc_info=True)
            from .criteria import (
                IR_CODE_KEYWORDS,
                REMOTE_INTEGRATIONS,
                RF_CODE_KEYWORDS,
                VALID_REMOTE_DOMAINS,
            )

            class MockValidator:
                """Mock validator for config flow."""

                def __init__(self, hass):
                    self.hass = hass

                async def is_valid_remote_device(self, device_entry, entity_registry):
                    try:
                        dev_entities = er.async_entries_for_device(
                            entity_registry,
                            device_entry.id,
                            include_disabled_entities=False,
                        )
                        for entity in dev_entities:
                            if entity.domain == "remote":
                                return True
                            if entity.domain == "text":
                                e_text = f"{entity.entity_id} {entity.name or ''}"
                                e_text = e_text.lower()
                                if any(k in e_text for k in IR_CODE_KEYWORDS):
                                    return True
                                if any(k in e_text for k in RF_CODE_KEYWORDS):
                                    return True
                        return False
                    except Exception:
                        return False

            class MockCriteria:
                """Mock criteria for config flow."""

                def __init__(self):
                    self.VALID_REMOTE_DOMAINS = VALID_REMOTE_DOMAINS
                    self.IR_CODE_KEYWORDS = IR_CODE_KEYWORDS
                    self.RF_CODE_KEYWORDS = RF_CODE_KEYWORDS
                    self.REMOTE_INTEGRATIONS = REMOTE_INTEGRATIONS

            validator = MockValidator(self.hass)
            remote_criteria = MockCriteria()
            device_registry_service = DeviceRegistryService()
            return validator, remote_criteria, device_registry_service

    async def find_remote_devices(self) -> List[Dict[str, Any]]:
        """Discover all valid remote control devices."""

        _LOGGER.info("Starting remote device discovery...")
        remote_devices: Dict[str, Dict[str, Any]] = {}

        try:
            validator, r_criteria, d_manager = await self._get_dependencies()

            device_registry = dr.async_get(self.hass)
            entity_registry = er.async_get(self.hass)

            device_entries = list(device_registry.devices.values())
            _LOGGER.debug("Evaluating %d devices in registry...", len(device_entries))

            for device_entry in device_entries:
                d_info = d_manager.get_device_by_id(self.hass, device_entry.id)
                d_name = (
                    d_info.name if d_info else device_entry.name or "Unknown Device"
                )

                try:
                    # Entegrasyon kontrolü
                    has_r_int = (
                        any(
                            self.hass.config_entries.async_get_entry(entry_id).domain
                            in r_criteria.REMOTE_INTEGRATIONS
                            for entry_id in device_entry.config_entries
                            if self.hass.config_entries.async_get_entry(entry_id)
                        )
                        if device_entry.config_entries
                        else False
                    )

                    is_valid = await validator.is_valid_remote_device(
                        device_entry, entity_registry
                    )

                    if is_valid or has_r_int:
                        remote_entity = None
                        d_entities = er.async_entries_for_device(
                            entity_registry,
                            device_entry.id,
                            include_disabled_entities=False,
                        )

                        # Önce remote domainini ara
                        for entity in d_entities:
                            if entity.domain == "remote":
                                remote_entity = entity.entity_id
                                break

                        # Yoksa anahtar kelimeli text domainini ara
                        if not remote_entity:
                            for entity in d_entities:
                                if entity.domain == "text":
                                    e_text = (
                                        f"{entity.entity_id} {entity.name or ''} "
                                        f"{entity.original_name or ''}"
                                    ).lower()
                                    if any(
                                        k.lower() in e_text
                                        for k in r_criteria.IR_CODE_KEYWORDS
                                    ):
                                        remote_entity = entity.entity_id
                                        break
                                    if any(
                                        k.lower() in e_text
                                        for k in r_criteria.RF_CODE_KEYWORDS
                                    ):
                                        remote_entity = entity.entity_id
                                        break

                        if remote_entity:
                            remote_devices[remote_entity] = {
                                "id": remote_entity,
                                "name": d_name,
                            }
                        else:
                            remote_devices[device_entry.id] = {
                                "id": device_entry.id,
                                "name": d_name,
                            }
                except Exception as e:
                    _LOGGER.error("Error validating device %s: %s", device_entry.id, e)
        except Exception as e:
            _LOGGER.error("Unexpected error during discovery: %s", e, exc_info=True)

        device_list = list(remote_devices.values())
        device_list.sort(key=lambda d: d["name"])
        _LOGGER.info(
            "Remote device discovery completed. Found %d valid devices",
            len(device_list),
        )
        return device_list
