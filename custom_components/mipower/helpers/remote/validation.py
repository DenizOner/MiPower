"""Remote device validation implementation for Smartify integration.

This module provides functionality to validate whether a device is a valid
remote control device based on multiple criteria including native remote
domain detection, integration-based detection, and entity keyword analysis.
"""

import logging

from homeassistant.core import HomeAssistant  # type: ignore[import]
from homeassistant.helpers import device_registry as dr  # type: ignore[import]
from homeassistant.helpers import entity_registry as er  # type: ignore[import]

from ...di.container import DependencyContainer
from ..device.registry_service import DeviceRegistryService
from .criteria import (
    IR_CODE_KEYWORDS,
    REMOTE_INTEGRATIONS,
    RF_CODE_KEYWORDS,
    VALID_REMOTE_DOMAINS,
)
from .remote_interface import RemoteDeviceValidatorInterface


_LOGGER: logging.Logger = logging.getLogger(__name__)


class RemoteCriteria:
    """Criteria for remote device validation."""

    def __init__(self):
        """Initialize remote criteria."""
        self.valid_domains = ["remote", "text"]
        self.ir_keywords = ["ir", "code", "send"]
        self.rf_keywords = ["rf", "radio"]
        self.remote_integrations = ["broadlink", "xiaomi_miio"]

    def is_valid_domain(self, domain: str) -> bool:
        """Check if domain is valid for remote devices."""
        return domain in self.valid_domains

    def has_ir_keywords(self, entity_id: str) -> bool:
        """Check if entity ID has IR-related keywords."""
        eid_lower = entity_id.lower()
        return any(k in eid_lower for k in self.ir_keywords)

    def has_rf_keywords(self, entity_id: str) -> bool:
        """Check if entity ID has RF-related keywords."""
        eid_lower = entity_id.lower()
        return any(k in eid_lower for k in self.rf_keywords)

    def is_remote_integration(self, integration: str) -> bool:
        """Check if integration is remote-related."""
        return integration in self.remote_integrations


class RemoteDeviceValidator(RemoteDeviceValidatorInterface):
    """Implementation of remote device validation."""

    def __init__(self, container: DependencyContainer):
        """Initialize the remote device validator with dependency injection.

        Args:
            container: Dependency injection container
        """
        self.container = container
        self.hass: HomeAssistant = (
            container.hass if container and hasattr(container, "hass") else None
        )

    async def _get_device_registry_service(self) -> DeviceRegistryService:
        """Get device registry service from container (async resolve)."""
        device_manager = DeviceRegistryService()
        return device_manager

    async def _get_remote_criteria(self):
        """Get remote criteria from container."""
        return await self.container.resolve("RemoteCriteria")

    async def is_valid_remote_device(
        self,
        device_entry: dr.DeviceEntry,
        entity_registry: er.EntityRegistry,
    ) -> bool:
        """Validates if a device is a valid remote control device.

        Criteria include:
        1. Native remote domain detection (domain == 'remote')
        2. Integration-based detection (remote-related integrations)
        3. Entity keyword analysis (keywords in specific domains)
        """

        device_registry_service = DeviceRegistryService()
        device_info = device_registry_service.get_device_by_id(
            self.hass, device_entry.id
        )
        d_name = device_info.name if device_info else f"Device {device_entry.id}"

        _LOGGER.debug("[%s] Beginning remote device validation", d_name)
        try:
            device_entities = er.async_entries_for_device(
                entity_registry, device_entry.id, include_disabled_entities=False
            )
            e_count = len(device_entities)
            _LOGGER.debug("[%s] Analyzing %d entities", d_name, e_count)

            # Criterion 1: Native remote domain detection
            _LOGGER.debug("[%s] Applying Criterion 1: Native remote check", d_name)
            for entity in device_entities:
                if entity.domain == "remote":
                    _LOGGER.debug(
                        "[%s] ✓ PASS: Native 'remote' entity: %s",
                        d_name,
                        entity.entity_id,
                    )
                    return True

            # Criterion 2: Integration-based detection
            _LOGGER.debug("[%s] Applying Criterion 2: Integration check", d_name)
            if device_entry.config_entries and self.hass is not None:
                for entry_id in device_entry.config_entries:
                    entry = self.hass.config_entries.async_get_entry(entry_id)
                    if entry and entry.domain in REMOTE_INTEGRATIONS:
                        _LOGGER.debug(
                            "[%s] ✓ PASS: Remote integration: %s", d_name, entry.domain
                        )
                        return True
            elif self.hass is None:
                _LOGGER.error(
                    "[%s] Home Assistant instance is None, cannot check config entries",
                    d_name,
                )
            else:
                _LOGGER.debug("[%s] No configuration entries for analysis", d_name)

            # Criterion 3: Entity keyword analysis for specific domains
            _LOGGER.debug("[%s] Applying Criterion 3: Keyword analysis", d_name)
            for entity in device_entities:
                if entity.domain not in VALID_REMOTE_DOMAINS:
                    continue

                eid_l = entity.entity_id.lower()
                en_l = (entity.name or "").lower()
                on_l = (entity.original_name or "").lower()

                search_text = f"{eid_l} {en_l} {on_l}"

                ir_match = any(k.lower() in search_text for k in IR_CODE_KEYWORDS)
                rf_match = any(k.lower() in search_text for k in RF_CODE_KEYWORDS)

                if ir_match or rf_match:
                    m_type = "IR" if ir_match else "RF"
                    _LOGGER.debug(
                        "[%s] ✓ PASS: %s keywords in entity: %s",
                        d_name,
                        m_type,
                        entity.entity_id,
                    )
                    return True

            _LOGGER.debug("[%s] ✗ FAIL: No remote criteria met", d_name)
            return False
        except Exception as e:
            _LOGGER.error(
                "Error validating remote device '%s': %s", d_name, e, exc_info=True
            )
            return False
