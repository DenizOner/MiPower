"""Config flow schema builder interface for Smartify."""

from abc import ABC, abstractmethod
from typing import List

import voluptuous as vol  # type: ignore[import]


class ConfigSchemaBuilderInterface(ABC):
    """Interface for config flow schema builders."""

    @abstractmethod
    def build_device_config_schema(
        self, power_devices: List[dict], remote_devices: List[dict]
    ) -> vol.Schema:
        """Build the advanced configuration schema for device setup.

        Args:
            power_devices: List of available power sensor devices.
            remote_devices: List of available remote devices.

        Returns:
            vol.Schema: Configuration schema with device selection fields.
        """
        pass

    @abstractmethod
    def build_scripts_schema(self, device_scripts: List[dict]) -> vol.Schema:
        """Build the scripts selection schema.

        Args:
            device_scripts: List of available script dictionaries.

        Returns:
            vol.Schema: Scripts selection schema with dropdown selectors.
        """
        pass

    @abstractmethod
    def _build_fallback_schema(self) -> vol.Schema:
        """Build a fallback schema for error recovery.

        Returns:
            vol.Schema: Basic string input schema for fallback.
        """
        pass
