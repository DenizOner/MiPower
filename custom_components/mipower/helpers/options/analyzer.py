"""Device capabilities analyzer for Smartify integration.

This module provides functionality to analyze device capabilities for options flow.
"""

import logging
from typing import Any, Dict

from homeassistant.config_entries import ConfigEntry  # type: ignore[import]

from ...const import CONF_POWER_ENTITY

_LOGGER = logging.getLogger(__name__)


class DeviceCapabilitiesAnalyzer:
    """Service for analyzing device capabilities.

    This class analyzes Smartify device configurations to determine available
    features such as power sensing, outlet control, and remote control capabilities.
    """

    def __init__(self, hass):
        """Initialize the device capabilities analyzer.

        Args:
            hass: Home Assistant instance
        """
        self.hass = hass

    async def analyze_capabilities(self, config_entry: ConfigEntry) -> Dict[str, Any]:
        """Analyze and determine the capabilities of a Smartify device.

        Examines the device configuration to identify available features such as
        power sensing, outlet control, and remote control capabilities. This information
        is used to customize the options form and validation schema.

        Args:
            config_entry (ConfigEntry): The configuration entry for the device to analyze.

        Returns:
            Dict[str, Any]: A dictionary containing capability flags:
                - has_outlet_switch (bool): Whether the device has controllable outlet switch
                - has_power_sensor (bool): Whether the device has power measurement capability
                - has_remote_control (bool): Whether the device supports remote control (always True)
        """
        capabilities = {
            "has_outlet_switch": False,
            "has_power_sensor": False,
            "has_remote_control": False,
        }

        try:
            power_entity_id = config_entry.data.get(CONF_POWER_ENTITY)
            if power_entity_id:
                capabilities["has_power_sensor"] = True
                # Use entity discovery helper to find switch
                from ..entity.discovery import find_switch_for_power_entity

                plug_switch_entity_id = find_switch_for_power_entity(
                    self.hass, power_entity_id
                )
                capabilities["has_outlet_switch"] = plug_switch_entity_id is not None
            capabilities["has_remote_control"] = True
        except Exception as e:
            _LOGGER.warning("Error analyzing device capabilities: %s", e)

        _LOGGER.debug("Device capabilities: %s", capabilities)
        return capabilities
