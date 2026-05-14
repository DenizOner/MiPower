"""Device discovery services for Smartify configuration flow.

This module provides device discovery services following SOLID principles,
separating device discovery logic from the main configuration flow.
"""

import logging

from homeassistant.core import HomeAssistant  # type: ignore

from ...helpers.config_flow.discovery_interface import (
    DiscoveryInterface,
)
from ...helpers.logger.config_flow_logger import discovery_service_logging
from ...helpers.power.finder import find_power_devices
from ...helpers.script.finder import find_scripts_for_device

_LOGGER = logging.getLogger(__name__)


class DiscoveryService(DiscoveryInterface):
    """Service for discovering devices following Single Responsibility Principle."""

    @discovery_service_logging()
    def __init__(self, hass: HomeAssistant):
        """Initialize the device discovery service.

        Args:
            hass: Home Assistant instance
        """
        try:
            _LOGGER.info(
                "DiscoveryService __init__ started - comprehensive logging active"
            )
            _LOGGER.debug(f"Home Assistant instance: {hass}")
            self.hass = hass
            _LOGGER.debug("Hass instance successfully assigned")
            _LOGGER.info("DiscoveryService __init__ completed successfully")
        except Exception as e:
            _LOGGER.error(f"DiscoveryService __init__ error: {e}", exc_info=True)
            raise
        finally:
            _LOGGER.debug("DiscoveryService __init__ finally block executed")

    @discovery_service_logging()
    async def discover_power_devices(self) -> list:
        """Discover available power sensor devices.

        Returns:
            list: List of available power devices with id/name.
        """
        try:
            _LOGGER.debug("Discovering power devices")
            devices = await find_power_devices(self.hass)
            _LOGGER.debug(f"Found {len(devices)} power devices")
            return devices
        except Exception as e:
            _LOGGER.error(
                f"Error discovering power devices: {e}",
                exc_info=True,
            )
            return []

    @discovery_service_logging()
    async def discover_remote_devices(self) -> list:
        """Discover available remote devices.

        For config flow, use simplified discovery without full container setup.

        Returns:
            list: List of available remote devices with id/name.
        """
        try:
            _LOGGER.debug("Discovering remote devices for config flow")
            # Use simplified discovery for config flow (no full container needed)
            from ...di.container import DependencyContainer
            from ...helpers.remote.finder import RemoteDeviceFinder

            # Create minimal container for config flow (null entry is ok here)
            # The RemoteDeviceFinder will handle null entry gracefully
            container = DependencyContainer(self.hass, None)
            finder = RemoteDeviceFinder(container)
            devices = await finder.find_remote_devices()
            _LOGGER.debug(f"Found {len(devices)} remote devices")
            return devices
        except Exception as e:
            _LOGGER.error(
                f"Error discovering remote devices: {e}",
                exc_info=True,
            )
            return []

    @discovery_service_logging()
    async def discover_scripts_for_device(self, device_id: str) -> list:
        """Discover scripts available for a specific device.

        Args:
            device_id: The device ID to find scripts for.

        Returns:
            list: List of available scripts for the device.
        """
        try:
            _LOGGER.debug(f"Discovering scripts for device: {device_id}")
            # Create a new event loop for the sync function
            import concurrent.futures

            # Run the sync function in a thread pool to avoid blocking
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(find_scripts_for_device, self.hass, device_id)
                scripts = future.result(timeout=60)  # 60 second timeout
            _LOGGER.debug(f"Found {len(scripts)} scripts for device {device_id}")
            return scripts
        except Exception as e:
            _LOGGER.error(
                f"Error discovering scripts for device {device_id}: {e}",
                exc_info=True,
            )
            return []
