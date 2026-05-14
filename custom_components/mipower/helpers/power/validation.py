"""Smartify power entity validation module.

This module provides validation and discovery functionality for power-related
entities in Home Assistant. It implements criteria-based filtering to identify
valid power sensors that meet Smartify's requirements for power monitoring,
excluding battery-powered devices and validating entity domains, device classes,
and naming patterns.

The module ensures that only appropriate power entities are selected for
monitoring, preventing false positives and ensuring accurate power consumption
tracking.

Functions:
    get_power_entity_id: Validates and finds the appropriate power entity
        for a given device based on established criteria.
"""

import logging
from typing import Optional

from homeassistant.core import HomeAssistant  # type: ignore[import]
from homeassistant.helpers import entity_registry as er  # type: ignore[import]

from ..device.registry_service import DeviceRegistryService
from .criteria import (
    INVALID_POWER_DEVICE_CLASSES,
    VALID_ENTITY_DOMAINS,
    VALID_POWER_SUFFIXES,
    VALID_POWER_DEVICE_CLASSES,
)

_LOGGER = logging.getLogger(__name__)


async def get_power_entity_id(
    hass: HomeAssistant,
    entity_registry: er.EntityRegistry,
    device_id: str,
) -> Optional[str]:
    """Find and validate the power entity for a given device.

    This function searches through all entities associated with a device and
    identifies the appropriate power sensor based on validation criteria:
    - Entity domain must be in VALID_ENTITY_DOMAINS
    - Entity suffix must match VALID_POWER_SUFFIXES
    - Device class must be in VALID_POWER_DEVICE_CLASSES
    - Device must not have battery entities (unless it's a plug)

    Args:
        hass (HomeAssistant): The Home Assistant instance.
        entity_registry (er.EntityRegistry): The entity registry to search.
        device_id (str): The device ID to find power entity for.

    Returns:
        Optional[str]: The entity ID of the valid power sensor, or None if
            no suitable entity is found or validation fails.
    """

    device_manager = DeviceRegistryService()
    device_info = device_manager.get_device_by_id(hass, device_id)
    device_display_name = (
        getattr(device_info, "name", None)
        if device_info
        else None or f"Device {device_id}"
    )
    _LOGGER.debug("[%s] Starting power entity search.", device_display_name)
    try:
        device_entities = er.async_entries_for_device(
            entity_registry, device_id, include_disabled_entities=False
        )
        _LOGGER.debug(
            "[%s] Found %d entities to inspect.",
            device_display_name,
            len(device_entities),
        )
        for entity in device_entities:
            live_state = hass.states.get(entity.entity_id)
            if (
                live_state
                and live_state.attributes.get("device_class")
                in INVALID_POWER_DEVICE_CLASSES
            ):
                _LOGGER.debug(
                    "[%s] -> DISQUALIFIED: Device has battery entity '%s'",
                    device_display_name,
                    entity.entity_id,
                )
                return None
        for entity in device_entities:
            # _LOGGER.debug(
            #     "[%s] --- Inspecting entity: %s ---",
            #     device_display_name,
            #     entity.entity_id,
            # )
            if entity.domain not in VALID_ENTITY_DOMAINS:
                # _LOGGER.debug(
                #     "[%s] [Entity: %s] -> SKIPPED: Domain '%s' not in %s",
                #     device_display_name,
                #     entity.entity_id,
                #     entity.domain,
                #     VALID_ENTITY_DOMAINS,
                # )
                continue
            # _LOGGER.debug(
            #     "[%s] [Entity: %s] -> OK: Domain '%s' is valid.",
            #     device_display_name,
            #     entity.entity_id,
            #     entity.domain,
            # )
            live_state = hass.states.get(entity.entity_id)
            if not live_state:
                # _LOGGER.debug(
                #     "[%s] [Entity: %s] -> SKIPPED: No live state",
                #     device_display_name,
                #     entity.entity_id,
                # )
                continue
            actual_class = live_state.attributes.get("device_class")
            has_valid_suffix = any(
                entity.entity_id.endswith(s) for s in VALID_POWER_SUFFIXES
            )
            if not has_valid_suffix:
                # _LOGGER.debug(
                #     "[%s] [Entity: %s] -> SKIPPED: Suffix not in %s",
                #     device_display_name,
                #     entity.entity_id,
                #     VALID_POWER_SUFFIXES,
                # )
                continue
            # _LOGGER.debug(
            #     "[%s] [Entity: %s] -> OK: Suffix is valid.",
            #     device_display_name,
            #     entity.entity_id,
            # )
            if actual_class in VALID_POWER_DEVICE_CLASSES:
                # _LOGGER.debug(
                #     "[%s] [Entity: %s] -> SUCCESS: Valid device_class '%s'",
                #     device_display_name,
                #     entity.entity_id,
                #     actual_class,
                # )
                return entity.entity_id
            # else:
            #     # _LOGGER.debug(
            #     #     "[%s] [Entity: %s] -> FAILED: Invalid device_class '%s'",
            #     #     device_display_name,
            #     #     entity.entity_id,
            #     #     actual_class,
            #     # )
        _LOGGER.debug(
            "[%s] -> FAILED: No entity matched all criteria.", device_display_name
        )
        return None
    except Exception as e:
        _LOGGER.error(
            "An unexpected error occurred during power entity search for device %s: %s",
            device_display_name,
            e,
            exc_info=True,
        )
