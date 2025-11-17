"""
Bluetooth services package for MiPower integration.

This package contains Bluetooth-specific services following SOLID principles.
All components are designed with single responsibility and high cohesion.
"""

from .exceptions import TurnOnFailedReason
from .interfaces import IBluetoothService
from .media_player_monitor import MediaPlayerMonitor
from .pair_sender import BluetoothPairSender
from .process_manager import BluetoothProcessManager
from .scanner import BluetoothScanner
from .service import BluetoothService
from .wake_coordinator import BluetoothWakeCoordinator

__all__ = [
    # Main service
    "BluetoothService",
    # Core interfaces and exceptions
    "IBluetoothService",
    "TurnOnFailedReason",
    # Coordinator
    "BluetoothWakeCoordinator",
    # Specialized components
    "BluetoothProcessManager",
    "BluetoothScanner",
    "BluetoothPairSender",
    "MediaPlayerMonitor",
]
