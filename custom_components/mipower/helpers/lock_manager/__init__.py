"""
Lock Manager Package.

This module provides advanced asynchronous locking functionality following SOLID principles,
including deadlock detection, hierarchical locking, and comprehensive statistics tracking.

All components follow SOLID principles with proper abstraction and separation of concerns.
"""

from .deadlock_detector import DeadlockDetector
from .lock_factory import LockFactory
from .lock_manager import LockManager
from .lock_manager_interface import (
    DeadlockDetectorInterface,
    LockFactoryInterface,
    LockManagerInterface,
    LockStatisticsInterface,
)
from .lock_manager_plugin import LockManagerPlugin
from .lock_statistics import LockStatisticsTracker

__all__ = [
    "LockManager",
    "LockManagerInterface",
    "DeadlockDetectorInterface",
    "LockFactoryInterface",
    "LockStatisticsInterface",
    "LockManagerPlugin",
    "DeadlockDetector",
    "LockFactory",
    "LockStatisticsTracker",
]
