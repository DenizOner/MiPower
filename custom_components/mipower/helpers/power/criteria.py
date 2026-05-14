"""Smartify power entity criteria module.

This module defines the criteria and constants used for identifying and validating
power-related entities in Home Assistant. It includes valid entity domains, suffixes,
and device classes that are used by power analysis components.

Constants:
    VALID_ENTITY_DOMAINS: Tuple of valid entity domains for power sensors.
    VALID_POWER_SUFFIXES: Tuple of valid entity ID suffixes for power sensors.
    VALID_POWER_DEVICE_CLASSES: Tuple of valid device classes for power sensors.
    INVALID_POWER_DEVICE_CLASSES: Tuple of invalid device classes to exclude.
"""

from typing import Tuple

from homeassistant.components.sensor import SensorDeviceClass  # type: ignore[import]

VALID_ENTITY_DOMAINS: Tuple[str, ...] = ("sensor",)
VALID_POWER_SUFFIXES: Tuple[str, ...] = ("_power", "_current", "_voltage")
VALID_POWER_DEVICE_CLASSES: Tuple[str, ...] = (
    SensorDeviceClass.POWER,
    SensorDeviceClass.CURRENT,
    SensorDeviceClass.VOLTAGE,
)
INVALID_POWER_DEVICE_CLASSES: Tuple[str, ...] = (SensorDeviceClass.BATTERY,)
