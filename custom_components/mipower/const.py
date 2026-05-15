"""
Constants for the MiPower integration.

This file serves as a central repository for all constant values used throughout the
integration. Defining constants in one place makes the code more readable by avoiding
"magic strings" or numbers, and it simplifies maintenance, as values can be updated
in a single location.
"""

# --- Core Integration Constants ---

# The domain of the integration. Unique identifier within HA.
# Must match the integration's directory name.
DOMAIN = "mipower"

# --- Default Values ---

# Fallback device name if proper name cannot be determined.
DEFAULT_DEVICE_NAME = "Unknown Device"
# Manufacturer name for device info panel in HA.
MANUFACTURER = "MiPower"
# Default icon for power switch entity, from Material Design Icons.
DEFAULT_ENTITY_ICON = "mdi:power"
# Default icon for device, from Material Design Icons.
DEFAULT_DEVICE_ICON = "mdi:power-settings"
# Prefix for device name to identify as MiPower device.
DEVICE_NAME_PREFIX = "MiPower - "


# --- Configuration Keys ---
# Keys for config entry data/options. Using constants prevents typos.

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
# Key for the duration of the Bluetooth signal (in seconds).
CONF_SIGNAL_DURATION = "signal_duration"
# Key for the device selection in the "Easy Setup" flow.
CONF_DEVICE = "device"
# Key for the device ID selection in the "Advanced Setup" flow.
CONF_DEVICE_ID = "device_id"
# Key for the Bluetooth scan duration setting (in seconds).
CONF_SCAN_DURATION = "scan_duration"
# Key for the timeout when stopping the Bluetooth scan (in seconds).
CONF_SCAN_STOP_TIMEOUT = "scan_stop_timeout"


# --- bluetoothctl Command Constants ---
# These constants are related to the execution of the `bluetoothctl` command-line tool.

# The command to execute for all Bluetooth operations.
BLUETOOTHCTL_COMMAND = "bluetoothctl"
# The expected prompt from the bluetoothctl utility. pexpect waits for this prompt
# to know that the tool is ready to receive the next command.
BLUETOOTHCTL_PROMPT = r"\[bluetoothctl\]> "
# The 'pair' subcommand string.
CMD_PAIR = "pair"
# The 'scan on' subcommand string.
CMD_SCAN_ON = "scan on"
# The 'scan off' subcommand string.
CMD_SCAN_OFF = "scan off"
# The 'quit' subcommand string.
CMD_QUIT = "quit"


# --- Default Timing Values (in seconds or fractions of seconds) ---
# These are the default values for all timing-related settings. They are used if the
# user does not override them during the setup or in the options flow.

# Default debounce time to prevent rapid 'turn_on' calls.
DEFAULT_ON_DEBOUNCE_SECONDS = 25
# Default debounce time to prevent rapid 'turn_off' calls.
DEFAULT_OFF_DEBOUNCE_SECONDS = 1.0
# Default delay between bluetoothctl commands. A small delay can improve reliability.
DEFAULT_INTER_STEP_DELAY = 0.05
# Default timeout for spawning the bluetoothctl process.
DEFAULT_SPAWN_TIMEOUT = 2.0
# Default duration for the Bluetooth signal.
DEFAULT_SIGNAL_DURATION = 0.15
# Default duration for the initial Bluetooth scan to find the device.
DEFAULT_SCAN_DURATION = 10
# Default timeout for stopping the Bluetooth scan.
DEFAULT_SCAN_STOP_TIMEOUT = 1.0


# --- UI Selector Ranges ---
# These dictionaries define the valid range (min, max) and step for the number
# selectors (sliders) that are displayed in the configuration and options UI.

# Defines the range for the 'on_debounce' slider.
RANGE_ON_DEBOUNCE = {"min": 1, "max": 30, "step": 1}
# Defines the range for the 'off_debounce' slider.
RANGE_OFF_DEBOUNCE = {"min": 0.1, "max": 5.0, "step": 0.1}
# Defines the range for the 'inter_step_delay' slider.
RANGE_INTER_STEP_DELAY = {"min": 0.01, "max": 1.0, "step": 0.01}
# Defines the range for the 'spawn_timeout' slider.
RANGE_SPAWN_TIMEOUT = {"min": 1.0, "max": 5.0, "step": 0.1}
# Defines the range for the 'signal_duration' slider.
RANGE_SIGNAL_DURATION = {"min": 0.05, "max": 1.0, "step": 0.05}
# Defines the range for the 'scan_duration' slider.
RANGE_SCAN_DURATION = {"min": 5, "max": 20, "step": 1}
# Defines the range for the 'scan_stop_timeout' slider.
RANGE_SCAN_STOP_TIMEOUT = {"min": 0.1, "max": 3.0, "step": 0.1}
