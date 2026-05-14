"""Smartify remote device criteria module.

This module defines the validation criteria and constants used for identifying
and filtering remote control devices in Home Assistant. It includes sets of
integrations, entity keywords, and domains that are considered valid for
remote device functionality.

The criteria are used throughout the Smartify integration to ensure that only
appropriate entities are selected for remote control operations, including
IR and RF code transmission, device learning, and remote control automation.
"""

from typing import Set

# Set of integration domains that provide remote control functionality
REMOTE_INTEGRATIONS: Set[str] = {"broadlink", "tuya", "xiaomi_miio"}

# Keywords used to identify IR (infrared) code related entities
IR_CODE_KEYWORDS: Set[str] = {"ir_code", "ir_command", "send_ir", "learn_ir"}

# Keywords used to identify RF (radio frequency) code related entities
RF_CODE_KEYWORDS: Set[str] = {"rf_code", "rf_command", "send_rf", "learn_rf"}

# Valid entity domains that can be used for remote control operations
VALID_REMOTE_DOMAINS: Set[str] = {"remote", "text"}
