"""
Constants for the MiPower integration.

This file serves as a central repository for all constant values used throughout the
integration. Defining constants in one place makes the code more readable by avoiding
"magic strings" or numbers, and it simplifies maintenance, as values can be updated
in a single location.
"""

import re

# --- Core Integration Constants ---

# The domain of the integration. This is a unique identifier for this integration
# within Home Assistant. It must match the name of the integration's directory.
DOMAIN = "mipower"

# --- Default Values ---

# A default name for the device, used as a fallback if a proper name cannot be determined.
DEFAULT_DEVICE_NAME = "Unknown Device"
# The manufacturer name to be displayed in the device information panel in Home Assistant.
MANUFACTURER = "MiPower"
# The default icon for the power switch entity, from Material Design Icons.
DEFAULT_ENTITY_ICON = "mdi:power"
# The default icon for the device, from Material Design Icons.
DEFAULT_DEVICE_ICON = "mdi:power-settings"
# The prefix used for the device name to clearly identify it as a MiPower device.
DEVICE_NAME_PREFIX = "MiPower - "


# --- Configuration Keys ---
# These keys are used consistently to access data within the config entry's `data` and `options`
# dictionaries. Using constants for these keys prevents typos and ensures consistency.

# Key for the entity ID of the linked media player.
CONF_MEDIA_PLAYER_ENTITY_ID = "media_player_entity_id"
# Key for the turn-on debounce time setting (in seconds).
CONF_ON_DEBOUNCE = "on_debounce"
# Key for the turn-off debounce time setting (in seconds).
CONF_OFF_DEBOUNCE = "off_debounce"
# Key for the delay between consecutive bluetoothctl commands (in seconds).
CONF_INTER_STEP_DELAY = "inter_step_delay"
# Key for the timeout when spawning a pexpect process (in seconds).
CONF_SPAWN_TIMEOUT = "spawn_timeout"
# Key for the timeout for the 'pair' command in pexpect (in seconds).
CONF_PAIR_TIMEOUT = "pair_timeout"
# Key for the timeout for the 'trust' command in pexpect (in seconds).
CONF_TRUST_TIMEOUT = "trust_timeout"
# Key for the device selection in the "Easy Setup" flow.
CONF_DEVICE = "device"
# Key for the device ID selection in the "Advanced Setup" flow.
CONF_DEVICE_ID = "device_id"
# Key for the Bluetooth scan duration setting (in seconds).
CONF_SCAN_DURATION = "scan_duration"


# --- Default Timing Values (in seconds or fractions of seconds) ---
# These are the default values for all timing-related settings. They are used if the
# user does not override them during the setup or in the options flow.

# Default debounce time to prevent rapid 'turn_on' calls.
DEFAULT_ON_DEBOUNCE_SECONDS = 10
# Default debounce time to prevent rapid 'turn_off' calls.
DEFAULT_OFF_DEBOUNCE_SECONDS = 0
# Default delay between bluetoothctl commands. A small delay can improve reliability.
DEFAULT_INTER_STEP_DELAY = 0.1
# Default timeout for spawning the bluetoothctl process.
DEFAULT_SPAWN_TIMEOUT = 20
# Default timeout for the 'pair' command to complete.
DEFAULT_PAIR_TIMEOUT = 20
# Default timeout for the 'trust' command to complete.
DEFAULT_TRUST_TIMEOUT = 5
# Default duration for the initial Bluetooth scan to find the device.
DEFAULT_SCAN_DURATION = 10


# --- UI Selector Ranges ---
# These dictionaries define the valid range (min, max) and step for the number
# selectors (sliders) that are displayed in the configuration and options UI.

# Defines the range for the 'on_debounce' slider.
RANGE_ON_DEBOUNCE = {"min": 0, "max": 60, "step": 1}
# Defines the range for the 'off_debounce' slider.
RANGE_OFF_DEBOUNCE = {"min": 0, "max": 60, "step": 1}
# Defines a generic range for most timeout-related sliders.
TIMEOUT_RANGE = {"min": 5, "max": 120, "step": 1}
# Defines the range for the 'inter_step_delay' slider.
INTER_STEP_DELAY_RANGE = {"min": 0, "max": 10, "step": 0.1}
# Defines the range for the 'scan_duration' slider.
SCAN_DURATION_RANGE = {"min": 1, "max": 60, "step": 1}


# --- Discovery Constants ---
# These constants are used in the discovery process to find and identify Bluetooth devices.

# A pre-compiled regular expression to efficiently find and validate MAC addresses
# in various formats (e.g., with colons, hyphens, or no separators).
MAC_RE = re.compile(r"([0-9A-Fa-f]{2}(?:[:\-]?)){5}[0-9A-Fa-f]{2}")
# A tuple of strings used to identify a device connection as being Bluetooth-related.
BT_CONNECTION_TYPES = ("bluetooth", "bt", "ble", "ble_address")
# A tuple of keywords used to guess if a device is a Bluetooth device by looking
# at its identifiers, as a fallback when a clear connection type is not available.
BT_IDENTIFIER_KEYWORDS = ("androidtv", "remote", "bt")


# --- bluetoothctl Command Constants ---
# These constants are related to the execution of the `bluetoothctl` command-line tool.

# The command to execute for all Bluetooth operations.
BLUETOOTHCTL_COMMAND = "bluetoothctl"
# The expected prompt from the bluetoothctl utility. pexpect waits for this prompt
# to know that the tool is ready to receive the next command.
BLUETOOTHCTL_PROMPT = r"# "
# The 'pair' subcommand string.
CMD_PAIR = "pair"
# The 'trust' subcommand string.
CMD_TRUST = "trust"
# The 'quit' subcommand string.
CMD_QUIT = "quit"
# A list of possible string responses from bluetoothctl after a 'pair' command.
# pexpect will wait for one of these strings to determine the outcome.
PEXPECT_PAIR_RESPONSES = [
    "Pairing successful",
    "Failed to pair",
    "Device already paired",
    "AuthenticationFailed",
]
# The expected response string from bluetoothctl after a successful 'trust' command.
PEXPECT_TRUST_SUCCESS = "trust succeeded"
