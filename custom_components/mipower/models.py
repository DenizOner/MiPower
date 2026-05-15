"""Data models for the MiPower integration."""

import re
from dataclasses import dataclass


@dataclass
class TimingOptions:
    """
    A structured data class for timing-related configuration options.

    This model ensures that timing settings are strongly typed and easily accessible,
    preventing common errors associated with dictionary key typos.
    """

    on_debounce: int
    off_debounce: float
    inter_step_delay: float
    spawn_timeout: float
    signal_duration: float
    scan_duration: int
    scan_stop_timeout: float


@dataclass
class DeviceDetails:
    """
    A structured data class for holding essential device information.

    This model consolidates device-related data, making it easier to pass around
    and manage within the integration.
    """

    mac_address: str
    media_player_entity_id: str
    device_id: str | None = None
    name: str | None = None  # Added friendly name for logging and display


# @dataclass
# class BluetoothCommandConstants:
#     """
#     A structured data class for Bluetooth command-line tool constants.
#
#     This model centralizes constants related to `bluetoothctl` operations,
#     improving maintainability and type safety.
#     """
#
#     BLUETOOTHCTL_COMMAND: str = "bluetoothctl"
#     BLUETOOTHCTL_PROMPT: re.Pattern[str] = re.compile(r"# ")
#     CMD_TRUST: str = "trust"
#     CMD_QUIT: str = "quit"
#     PEXPECT_TRUST_SUCCESS: str = "trust succeeded"


@dataclass
class DiscoveryConstants:
    """
    A structured data class for constants used in the discovery process.

    This model centralizes constants related to Bluetooth device discovery,
    improving maintainability and type safety.
    """

    MAC_RE: re.Pattern[str] = re.compile(r"([0-9A-Fa-f]{2}(?:[:\-]?)){5}[0-9A-Fa-f]{2}")
    BT_CONNECTION_TYPES: tuple[str, ...] = ("bluetooth", "bt", "ble", "ble_address")
    BT_IDENTIFIER_KEYWORDS: tuple[str, ...] = ("androidtv", "remote", "bt")
