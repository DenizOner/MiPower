"""
State Management Package.

This module provides comprehensive state management functionality following SOLID principles,
supporting state persistence, transition tracking, observer patterns, and performance monitoring.

All components follow SOLID principles with proper abstraction and separation of concerns.
"""

from .manager import StateManager
from .provider import StateProvider
from .registry_interface import StateInterface
from .state_plugin import StatePlugin
from .state_service import StateService

__all__ = [
    "StateManager",
    "StateProvider",
    "StateInterface",
    "StatePlugin",
    "StateService",
]
