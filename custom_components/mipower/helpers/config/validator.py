"""Config validator implementation for Smartify integration.

Provides validation functionality for configuration dictionaries following SOLID principles.
"""

from typing import Any, Dict

from .config_interfaces import ConfigValidatorInterface, ValidationResult
from ..logger.config_logger import config_validator_logging


@config_validator_logging("schema_builder")
def create_full_config_schema() -> Dict[str, Any]:
    """Create the full configuration schema for Smartify.

    Returns:
        Dict containing the complete configuration schema
    """
    return {
        "power_entity": {
            "type": str,
            "required": True,
        },
        "remote_device_id": {
            "type": str,
            "required": False,
        },
        "on_script": {
            "type": str,
            "required": False,
        },
        "off_script": {
            "type": str,
            "required": False,
        },
        "on_threshold": {
            "type": float,
            "required": False,
        },
        "off_threshold": {
            "type": float,
            "required": False,
        },
        "samples": {
            "type": int,
            "required": False,
        },
        "sample_interval": {
            "type": float,
            "required": False,
        },
        "power_change_threshold": {
            "type": float,
            "required": False,
        },
        "event_cooldown": {
            "type": float,
            "required": False,
        },
        "command_ignore_duration": {
            "type": float,
            "required": False,
        },
    }


class ConfigValidator(ConfigValidatorInterface):
    """Validates configuration dictionaries against schemas."""

    def __init__(self, schema: Dict[str, Any]):
        """Initialize validator with schema.

        Args:
            schema: Validation schema
        """
        self.schema = schema

    @config_validator_logging("config_validator")
    def validate_config(self, config: Dict[str, Any]) -> ValidationResult:
        """Validate config against schema.

        Args:
            config: Configuration to validate

        Returns:
            ValidationResult object
        """
        errors = []
        warnings = []
        validated_value = config.copy()

        for key, rules in self.schema.items():
            if key not in config and rules.get("required", False):
                errors.append(f"Missing required key: {key}")
            elif key in config:
                value = config[key]
                expected_type = rules.get("type")
                if expected_type and not isinstance(value, expected_type):
                    errors.append(
                        f"Invalid type for {key}: expected {expected_type.__name__}, got {type(value).__name__}"
                    )

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            validated_value=validated_value,
        )

    @config_validator_logging("config_validator")
    async def is_valid(self, config: Dict[str, Any], schema: Dict[str, Any]) -> bool:
        """Check if config is valid.

        Args:
            config: Configuration to check
            schema: Validation schema

        Returns:
            True if valid, False otherwise
        """
        result = self.validate_config(config)
        return result.is_valid
