"""Validation utilities for script entities in Smartify integration.

This module provides validation functions to ensure that script entities are
valid and compatible with the Smartify integration requirements. It checks
entity domains against allowed script domains and provides detailed logging
for validation results.
"""

import logging

from homeassistant.helpers import entity_registry as er  # type: ignore[import]

from .criteria import VALID_SCRIPT_DOMAINS

_LOGGER = logging.getLogger(__name__)


def is_valid_script_entity(entity: er.RegistryEntry) -> bool:
    """Validate if an entity is a valid script entity for Smartify.

    Checks whether the given entity belongs to an allowed script domain
    as defined in the VALID_SCRIPT_DOMAINS criteria. Provides detailed
    logging for validation steps and results.

    Args:
        entity (er.RegistryEntry): The entity registry entry to validate.

    Returns:
        bool: True if the entity is a valid script entity, False otherwise.
    """

    # _LOGGER.debug(f"[Entity: {entity.entity_id}] Running script validation...")
    if entity.domain not in VALID_SCRIPT_DOMAINS:
        # _LOGGER.debug(
        #     f"[Entity: {
        #         entity.entity_id}] -> FAILED: Domain '{
        #         entity.domain}' is not in {VALID_SCRIPT_DOMAINS}."
        # )
        return False
    # _LOGGER.debug(
    #     f"[Entity: {entity.entity_id}] -> SUCCESS: Domain is '{entity.domain}'. Validation passed."
    # )
    return True
