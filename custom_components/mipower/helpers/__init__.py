"""Helpers package for Smartify integration.

This package provides various utility modules and functions for the Smartify
Home Assistant integration, including common utilities for device and entity
management, validation functions, and helper classes for different aspects
of the integration.
"""

# Import facade-based functions following SOLID principles
from .registry import (
    discover_entities_via_facade,
    get_device_by_id_via_facade,
    get_device_registry_via_facade,
    get_entities_for_device_via_facade,
    register_entity_via_facade,
)

__all__ = [
    "discover_entities_via_facade",
    "get_device_by_id_via_facade",
    "get_device_registry_via_facade",
    "get_entities_for_device_via_facade",
    "register_entity_via_facade",
]
