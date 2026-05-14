"""Device discovery service implementation for Smartify config flow."""

from typing import Any, List, Protocol, runtime_checkable

from .discovery_interface import DiscoveryInterface


@runtime_checkable
class DiscoveryProvider(Protocol):
    """Protocol for device discovery providers."""

    async def find_power_devices(self) -> List[dict]:
        """Find available power devices."""
        ...

    async def find_remote_devices(self) -> List[dict]:
        """Find available remote devices."""
        ...

    async def find_scripts_for_device(self, device_id: str) -> List[dict]:
        """Find scripts for a specific device."""
        ...


class DiscoveryService(DiscoveryInterface):
    """Service for discovering devices using Home Assistant registries."""

    def __init__(self, hass: Any) -> None:
        """Initialize the device discovery service.

        Args:
            hass: Home Assistant instance for accessing helpers.
        """
        self.hass = hass

    async def discover_power_devices(self) -> List[dict]:
        """Discover available power sensor devices.

        Returns:
            List[dict]: List of available power devices with id and name.
        """
        from ..power.finder import find_power_devices

        power_devices = await find_power_devices(self.hass)

        # Transform to expected format
        return [
            {"id": device["id"], "name": device["name"]} for device in power_devices
        ]

    async def discover_remote_devices(self) -> List[dict]:
        """Discover available remote devices.

        Returns:
            List[dict]: List of available remote devices with id and name.
        """
        from ..remote.finder import RemoteDeviceFinder
        from ...di.container import DependencyContainer

        container = DependencyContainer(self.hass, None)
        finder = RemoteDeviceFinder(container)
        remote_devices = await finder.find_remote_devices()

        # Transform to expected format
        return [
            {"id": device["id"], "name": device["name"]} for device in remote_devices
        ]

    async def discover_scripts_for_device(self, device_id: str) -> List[dict]:
        """Discover scripts available for a specific device.

        Args:
            device_id: The device ID to find scripts for.

        Returns:
            List[dict]: List of available scripts for the device.
        """
        from ..script.finder import find_scripts_for_device

        scripts = find_scripts_for_device(self.hass, device_id)

        # Transform to expected format
        return [{"id": script["id"], "name": script["name"]} for script in scripts]
