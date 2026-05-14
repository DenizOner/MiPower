"""Config merger implementation for Smartify integration.

Provides deep merge functionality for config dictionaries following SOLID principles.
"""

import copy
from typing import Any, Dict

from .config_interfaces import ConfigMergerInterface
from ..logger.config_logger import config_merger_logging


class ConfigMerger(ConfigMergerInterface):
    """Merges config dictionaries with deep merge support."""

    @config_merger_logging("deep_merger")
    async def merge_configs(
        self, base: Dict[str, Any], override: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Merge two config dicts with deep merge.

        Args:
            base: Base config dictionary
            override: Override config dictionary

        Returns:
            Merged config dictionary
        """
        result = copy.deepcopy(base)

        for key, value in override.items():
            if (
                key in result
                and isinstance(result[key], dict)
                and isinstance(value, dict)
            ):
                result[key] = await self.merge_configs(result[key], value)
            else:
                result[key] = value

        return result
