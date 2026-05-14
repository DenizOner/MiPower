"""Configuration interfaces for Smartify integration.

Defines interfaces for config operations following SOLID principles.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class ValidationResult:
    """Result of configuration validation."""

    def __init__(
        self,
        is_valid: bool,
        errors: List[str],
        warnings: List[str],
        validated_value: Dict[str, Any],
    ):
        """Initialize validation result.

        Args:
            is_valid: Whether validation passed
            errors: List of error messages
            warnings: List of warning messages
            validated_value: Validated configuration value
        """
        self.is_valid = is_valid
        self.errors = errors
        self.warnings = warnings
        self.validated_value = validated_value


class ConfigMergerInterface(ABC):
    """Interface for config merging operations."""

    @abstractmethod
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
        pass


class ConfigValidatorInterface(ABC):
    """Interface for config validation operations."""

    @abstractmethod
    def validate_config(self, config: Dict[str, Any]) -> ValidationResult:
        """Validate config against schema.

        Args:
            config: Configuration to validate

        Returns:
            ValidationResult object
        """
        pass

    @abstractmethod
    async def is_valid(self, config: Dict[str, Any], schema: Dict[str, Any]) -> bool:
        """Check if config is valid.

        Args:
            config: Configuration to check
            schema: Validation schema

        Returns:
            True if valid, False otherwise
        """
        pass


class RegistryConfigLoaderInterface(ABC):
    """Interface for registry configuration loading operations.

    Follows Open-Closed Principle by allowing new config formats to be added
    without modifying existing code.
    """

    @abstractmethod
    async def load_registry_config(self, config_path: str) -> Dict[str, str]:
        """Load registry configuration from file.

        Args:
            config_path: Path to the configuration file

        Returns:
            Dictionary mapping interface names to implementation paths

        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If config format is invalid
        """
        pass

    @abstractmethod
    def get_supported_formats(self) -> List[str]:
        """Get list of supported configuration file formats.

        Returns:
            List of supported file extensions (e.g., ['.json', '.yaml'])
        """
        pass
