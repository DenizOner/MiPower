"""Registry helper functions for Smartify integration.

This module provides convenient wrapper functions for accessing Home Assistant
registries and states through the dependency injection container and facades.
Updated to use pure DI pattern following SOLID principles.
"""

from typing import Any, Optional

from homeassistant.core import HomeAssistant  # type: ignore[import]

from ..di.container import DependencyContainer


async def get_device_registry_via_facade(
    container: DependencyContainer, hass: HomeAssistant
) -> Any:
    """Get the Home Assistant device registry using facade pattern.

    Args:
        container: Dependency injection container
        hass: Home Assistant instance.

    Returns:
        Device registry instance.
    """
    facade = container.create_device_facade()
    return await facade.get_device_registry(hass)


async def get_device_by_id_via_facade(
    container: DependencyContainer, hass: HomeAssistant, device_id: str
) -> Optional[Any]:
    """Retrieve a device from the registry by its ID using facade pattern.

    Args:
        container: Dependency injection container
        hass: Home Assistant instance.
        device_id: The device ID to look up.

    Returns:
        Device entry if found, None otherwise.
    """
    facade = container.create_device_facade()
    return await facade.get_device_by_id(hass, device_id)


# Facade-based functions following SOLID principles and DI pattern


async def discover_entities_via_facade(
    container: DependencyContainer,
    domain: str,
    device_id: Optional[str] = None,
) -> dict:
    """Discover entities using the entity facade (recommended approach).

    Delegates to the entity facade for proper separation of concerns.

    Args:
        container: Dependency injection container
        domain: Entity domain (e.g., 'sensor', 'switch')
        device_id: Optional device ID to filter

    Returns:
        Dict with discovery results
    """
    facade = container.create_entity_facade()
    return await facade.discover_entities(domain, device_id)


async def register_entity_via_facade(
    container: DependencyContainer,
    entity_id: str,
    config_entry_id: str,
    device_id: Optional[str] = None,
) -> dict:
    """Register an entity using the entity facade (recommended approach).

    Delegates to the entity facade for proper registration and state management.

    Args:
        container: Dependency injection container
        entity_id: Entity ID
        config_entry_id: Configuration entry ID
        device_id: Optional device ID

    Returns:
        Dict with registration results
    """
    facade = container.create_entity_facade()
    return await facade.register_entity(entity_id, config_entry_id, device_id)


async def get_entities_for_device_via_facade(
    container: DependencyContainer, device_id: str
) -> dict:
    """Get entities for device using the entity facade (recommended approach).

    Delegates to the entity facade for device-entity relationship queries.

    Args:
        container: Dependency injection container
        device_id: The device ID to get entities for

    Returns:
        Dict with entities for device
    """
    facade = container.create_entity_facade()
    return await facade.get_entities_for_device(device_id)
