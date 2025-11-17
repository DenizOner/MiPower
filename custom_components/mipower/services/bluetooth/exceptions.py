"""
Bluetooth-specific exceptions for MiPower integration.

This module defines exceptions specific to Bluetooth operations,
following the Single Responsibility Principle.
"""

from enum import Enum


class TurnOnFailedReason(Enum):
    """
    Enumeration of possible reasons for Bluetooth wake-up failure.

    Provides specific failure reasons for better error handling and logging.
    """

    UNKNOWN = "An unknown error occurred."
    ALREADY_ON = "Media player is already on."
    BLUETOOTH_SERVICE_FAILED = "Bluetooth service failed to wake up the device."
    HA_SERVICE_CALL_FAILED = "Home Assistant media player turn on service call failed."
    SCAN_FAILED = "Bluetooth discovery failed to start or timed out."
    SIGNAL_FAILED = "Bluetooth signal sending timed out and device did not turn on."
    PROCESS_SPAWN_FAILED = "Bluetoothctl process failed to spawn or timed out."
    PROCESS_UNEXPECTEDLY_ENDED = "Bluetoothctl process ended unexpectedly."
