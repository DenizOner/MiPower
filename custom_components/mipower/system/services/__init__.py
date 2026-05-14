"""
Services Package.

This module provides service registration and management functionality following SOLID principles,
including service registry, validation, and execution for Smartify integration.

All components follow SOLID principles with proper abstraction and separation of concerns.
"""

from .interface import (
    ServiceExecutorInterface,
    ServiceRegistryInterface,
    ServiceValidatorInterface,
)
from .registry import ServiceRegistry
from .services_plugin import ServicesPlugin

__all__ = [
    "ServiceRegistry",
    "ServiceRegistryInterface",
    "ServiceValidatorInterface",
    "ServiceExecutorInterface",
    "ServicesPlugin",
]
