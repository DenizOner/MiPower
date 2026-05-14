"""Entity helper modules for Smartify integration.

This package contains utilities for entity management and discovery operations.
Updated to follow SOLID principles with dependency injection.
"""

from .discovery import EntityDiscoveryService
from .discovery_interface import EntityDiscoveryInterface
from .registry_interface import EntityRegistryInterface
from .registry_service import EntityRegistryService

__all__ = [
    "EntityDiscoveryService",
    "EntityDiscoveryInterface",
    "EntityRegistryInterface",
    "EntityRegistryService",
]
