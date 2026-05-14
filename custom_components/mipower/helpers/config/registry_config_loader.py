"""Registry configuration loader for Smartify integration.

This module provides configuration-driven loading of dependency injection registry
mappings from JSON/YAML files, following SOLID principles and Open-Closed Principle
for extensibility.
"""

import asyncio
import json
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List

import yaml

from .config_interfaces import RegistryConfigLoaderInterface
from ..logger.config_logger import registry_config_loader_logging

_LOGGER = logging.getLogger(__name__)


class BaseRegistryConfigLoader(RegistryConfigLoaderInterface, ABC):
    """Base class for registry config loaders with common functionality.

    Implements Template Method pattern for loading process while allowing
    format-specific parsing to be overridden by subclasses.
    """

    def __init__(self):
        """Initialize the config loader."""
        self._supported_formats = []

    @registry_config_loader_logging("base_loader")
    async def load_registry_config(self, config_path: str) -> Dict[str, str]:
        """Load registry configuration using template method pattern.

        Args:
            config_path: Path to the configuration file

        Returns:
            Dictionary mapping interface names to implementation paths

        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If config format is invalid
        """
        config_file = Path(config_path)

        # Validate file exists
        if not config_file.exists():
            raise FileNotFoundError(f"Registry config file not found: {config_path}")

        # Validate file extension
        if config_file.suffix.lower() not in self._supported_formats:
            raise ValueError(
                f"Unsupported config format: {config_file.suffix}. "
                f"Supported formats: {self._supported_formats}"
            )

        # Load and parse config
        try:
            raw_config = await self._load_file_content(config_file)
            parsed_config = self._parse_config(raw_config)
            validated_config = self._validate_config(parsed_config)

            _LOGGER.debug(f"Successfully loaded registry config from {config_path}")
            return validated_config

        except Exception as e:
            _LOGGER.error(f"Failed to load registry config from {config_path}: {e}")
            raise ValueError(f"Invalid registry config: {e}") from e

    @abstractmethod
    async def _load_file_content(self, config_file: Path) -> str:
        """Load raw file content.

        Args:
            config_file: Path to config file

        Returns:
            Raw file content as string
        """
        pass

    @abstractmethod
    def _parse_config(self, raw_content: str) -> Dict[str, str]:
        """Parse raw content into registry mapping.

        Args:
            raw_content: Raw file content

        Returns:
            Parsed registry mapping
        """
        pass

    @registry_config_loader_logging("base_loader")
    def _validate_config(self, config: Dict[str, str]) -> Dict[str, str]:
        """Validate parsed config structure.

        Args:
            config: Parsed configuration

        Returns:
            Validated configuration

        Raises:
            ValueError: If config structure is invalid
        """
        if not isinstance(config, dict):
            raise ValueError("Registry config must be a dictionary")

        if not config:
            raise ValueError("Registry config cannot be empty")

        # Validate each mapping
        for interface_name, impl_path in config.items():
            if not isinstance(interface_name, str):
                raise ValueError(
                    f"Interface name must be string, got {type(interface_name)}: {interface_name}"
                )

            if not isinstance(impl_path, str):
                raise ValueError(
                    f"Implementation path must be string for {interface_name}, got {type(impl_path)}"
                )

            if not interface_name.strip():
                raise ValueError("Interface name cannot be empty")

            if not impl_path.strip():
                raise ValueError(
                    f"Implementation path cannot be empty for {interface_name}"
                )

            # Basic path validation
            if not self._is_valid_module_path(impl_path):
                raise ValueError(
                    f"Invalid module path format for {interface_name}: {impl_path}"
                )

        return config

    @registry_config_loader_logging("base_loader")
    def _is_valid_module_path(self, path: str) -> bool:
        """Validate module path format.

        Args:
            path: Module path to validate

        Returns:
            True if valid, False otherwise
        """
        # Basic validation: should contain dots and end with class name
        parts = path.split(".")
        return len(parts) >= 2 and all(part.strip() for part in parts)


class JsonRegistryConfigLoader(BaseRegistryConfigLoader):
    """JSON-based registry configuration loader.

    Loads registry mappings from JSON files with validation.
    """

    def __init__(self):
        """Initialize JSON config loader."""
        super().__init__()
        self._supported_formats = [".json"]

    @registry_config_loader_logging("json_loader")
    def get_supported_formats(self) -> List[str]:
        """Get supported formats."""
        return self._supported_formats.copy()

    @registry_config_loader_logging("json_loader")
    async def _load_file_content(self, config_file: Path) -> str:
        """Load JSON file content."""
        return await asyncio.to_thread(config_file.read_text, encoding="utf-8")

    @registry_config_loader_logging("json_loader")
    def _parse_config(self, raw_content: str) -> Dict[str, str]:
        """Parse JSON content."""
        try:
            return json.loads(raw_content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}") from e


class YamlRegistryConfigLoader(BaseRegistryConfigLoader):
    """YAML-based registry configuration loader.

    Loads registry mappings from YAML files with validation.
    """

    def __init__(self):
        """Initialize YAML config loader."""
        super().__init__()
        self._supported_formats = [".yaml", ".yml"]

    @registry_config_loader_logging("yaml_loader")
    def get_supported_formats(self) -> List[str]:
        """Get supported formats."""
        return self._supported_formats.copy()

    @registry_config_loader_logging("yaml_loader")
    async def _load_file_content(self, config_file: Path) -> str:
        """Load YAML file content."""
        return await asyncio.to_thread(config_file.read_text, encoding="utf-8")

    @registry_config_loader_logging("yaml_loader")
    def _parse_config(self, raw_content: str) -> Dict[str, str]:
        """Parse YAML content."""
        try:
            return yaml.safe_load(raw_content)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML format: {e}") from e


class RegistryConfigLoaderFactory:
    """Factory for creating registry config loaders.

    Follows Factory pattern and Open-Closed Principle by allowing
    new loader types to be registered without modifying existing code.
    """

    def __init__(self):
        """Initialize factory with default loaders."""
        self._loaders = {
            ".json": JsonRegistryConfigLoader,
            ".yaml": YamlRegistryConfigLoader,
            ".yml": YamlRegistryConfigLoader,
        }

    @registry_config_loader_logging("factory")
    def register_loader(self, extension: str, loader_class):
        """Register a new config loader for a file extension.

        Args:
            extension: File extension (e.g., '.json')
            loader_class: Loader class that implements RegistryConfigLoaderInterface
        """
        self._loaders[extension.lower()] = loader_class

    @registry_config_loader_logging("factory")
    def create_loader(self, config_path: str) -> RegistryConfigLoaderInterface:
        """Create appropriate loader for the given config file.

        Args:
            config_path: Path to config file

        Returns:
            Config loader instance

        Raises:
            ValueError: If no loader available for the file extension
        """
        from pathlib import Path

        extension = Path(config_path).suffix.lower()

        if extension not in self._loaders:
            supported = list(self._loaders.keys())
            raise ValueError(
                f"No loader available for {extension}. Supported: {supported}"
            )

        return self._loaders[extension]()
