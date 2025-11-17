"""Custom exceptions for the MiPower integration."""

from enum import Enum


class MiPowerError(Exception):
    """Base exception for MiPower integration."""


class BluetoothConnectionError(MiPowerError):
    """Exception raised for errors in the Bluetooth connection."""


class DeviceNotFoundError(MiPowerError):
    """Exception raised when a device cannot be found."""


class TurnOnFailedReason(Enum):
    """Enum for specific reasons why turn-on logic might fail."""

    UNKNOWN = "An unknown error occurred."
    ALREADY_ON = "Media player is already on."
    BLUETOOTH_SERVICE_FAILED = "Bluetooth service failed to wake up the device."
    HA_SERVICE_CALL_FAILED = "Home Assistant media player turn on service call failed."
    SCAN_FAILED = "Bluetooth discovery failed to start or timed out."
    SIGNAL_FAILED = "Bluetooth signal sending timed out and device did not turn on."
    PROCESS_SPAWN_FAILED = "Bluetoothctl process failed to spawn or timed out."
    PROCESS_UNEXPECTEDLY_ENDED = "Bluetoothctl process ended unexpectedly."
