"""Smartify helpers data validator module.

This module provides data validation functionality for Smartify, including
schema-based validation, cross-field validation, and caching for performance.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Type, Union

from .validator_interface import DataValidatorInterface

_LOGGER = logging.getLogger(__name__)


@dataclass
class ValidationRule:
    """A validation rule for data fields.

    Attributes:
        name: Unique name of the validation rule.
        validator: Callable that validates a value and returns bool.
        error_message: Error message to show when validation fails.
        severity: Severity level ('error' or 'warning').
    """

    name: str
    validator: Callable[[Any], bool]
    error_message: str
    severity: str = "error"

    def validate(self, value: Any) -> tuple[bool, str]:
        """Validate a value using this rule.

        Args:
            value: The value to validate.

        Returns:
            Tuple of (is_valid, error_message).
        """

        try:
            is_valid = self.validator(value)
            return is_valid, "" if is_valid else self.error_message
        except Exception as e:
            return False, f"Validation error: {e}"


@dataclass
class DataSchema:
    """Schema definition for a data field.

    Attributes:
        name: The field name.
        required: Whether the field is required.
        data_type: Expected type of the field value.
        allowed_values: List of allowed values, if restricted.
        min_value: Minimum allowed value for numeric types.
        max_value: Maximum allowed value for numeric types.
        validation_rules: List of validation rules to apply.
        default_value: Default value for the field.
    """

    name: str
    required: bool = False
    data_type: Optional[Type] = None
    allowed_values: Optional[List[Any]] = None
    min_value: Optional[Union[int, float]] = None
    max_value: Optional[Union[int, float]] = None
    validation_rules: List[ValidationRule] = field(default_factory=list)
    default_value: Optional[Any] = None

    def __post_init__(self):
        """Initialize validation rules based on schema constraints."""

        if self.data_type:
            self.validation_rules.append(
                ValidationRule(
                    name=f"type_check_{self.name}",
                    validator=lambda v: isinstance(v, self.data_type)
                    if self.data_type
                    else True,
                    error_message=f"Field '{self.name}' must be of type {
                        self.data_type.__name__
                    }",
                )
            )
        if self.min_value is not None:
            self.validation_rules.append(
                ValidationRule(
                    name=f"min_check_{self.name}",
                    validator=lambda v: v >= self.min_value,
                    error_message=f"Field '{self.name}' must be >= {self.min_value}",
                )
            )
        if self.max_value is not None:
            self.validation_rules.append(
                ValidationRule(
                    name=f"max_check_{self.name}",
                    validator=lambda v: v <= self.max_value,
                    error_message=f"Field '{self.name}' must be <= {self.max_value}",
                )
            )
        if self.allowed_values:
            self.validation_rules.append(
                ValidationRule(
                    name=f"allowed_values_{self.name}",
                    validator=lambda v: v in self.allowed_values,
                    error_message=f"Field '{self.name}' must be one of: {
                        self.allowed_values
                    }",
                )
            )


@dataclass
class ValidationResult:
    """Result of a data validation operation.

    Attributes:
        is_valid: Whether the data is valid.
        errors: List of validation errors.
        warnings: List of validation warnings.
        validated_data: The validated and processed data.
        validation_timestamp: When the validation was performed.
    """

    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    validated_data: Dict[str, Any] = field(default_factory=dict)
    validation_timestamp: datetime = field(default_factory=datetime.now)

    def add_error(self, message: str) -> None:
        """Add a validation error.

        Args:
            message: The error message.
        """
        self.errors.append(message)
        self.is_valid = False

    def add_warning(self, message: str) -> None:
        """Add a validation warning.

        Args:
            message: The warning message.
        """
        self.warnings.append(message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the result to a dictionary.

        Returns:
            Dictionary representation of the validation result.
        """

        return {
            "is_valid": self.is_valid,
            "errors": self.errors.copy(),
            "warnings": self.warnings.copy(),
            "validated_data": self.validated_data.copy(),
            "validation_timestamp": self.validation_timestamp.isoformat(),
        }


class DataValidator(DataValidatorInterface):
    """Data validator using schema-based validation with caching."""

    def __init__(self, schema: Dict[str, DataSchema]):
        """Initialize the DataValidator.

        Args:
            schema: Dictionary of field schemas for validation.
        """
        self.schema = schema
        self._validation_cache: Dict[str, tuple[ValidationResult, float]] = {}
        _LOGGER.debug("DataValidator initialized with %d fields", len(schema))

    def validate_data(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate data against the schema.

        Args:
            data: The data dictionary to validate.

        Returns:
            ValidationResult containing validation status and details.
        """

        _LOGGER.debug("Starting data validation")
        result = ValidationResult(is_valid=True)
        data_key = self._get_data_key(data)
        cached_result = self._get_cached_result(data_key)
        if cached_result:
            _LOGGER.debug("Using cached validation result")
            return cached_result
        for field_name, field_schema in self.schema.items():
            field_value = data.get(field_name)
            if field_schema.required and field_value is None:
                result.add_error(f"Required field '{field_name}' is missing")
                continue
            if field_value is None:
                if field_schema.data_type:
                    result.validated_data[field_name] = None
                continue
            field_result = self._validate_field(field_name, field_value, field_schema)
            result.validated_data[field_name] = field_result["value"]
            if field_result["errors"]:
                result.errors.extend(field_result["errors"])
            if field_result["warnings"]:
                result.warnings.extend(field_result["warnings"])
        cross_validation_result = self._validate_cross_fields(result.validated_data)
        if cross_validation_result["errors"]:
            result.errors.extend(cross_validation_result["errors"])
        if cross_validation_result["warnings"]:
            result.warnings.extend(cross_validation_result["warnings"])
        result.is_valid = len(result.errors) == 0
        self._cache_result(data_key, result)
        _LOGGER.info(
            "Data validation complete: %s (%d errors, %d warnings)",
            "VALID" if result.is_valid else "INVALID",
            len(result.errors),
            len(result.warnings),
        )
        return result

    def _validate_field(
        self, field_name: str, field_value: Any, field_schema: DataSchema
    ) -> Dict[str, Any]:
        """Validate a single field against its schema.

        Args:
            field_name: Name of the field.
            field_value: Value of the field.
            field_schema: Schema definition for the field.

        Returns:
            Dictionary with validated value, errors, and warnings.
        """
        result = {"value": field_value, "errors": [], "warnings": []}
        for rule in field_schema.validation_rules:
            is_valid, error_message = rule.validate(field_value)
            if not is_valid:
                if rule.severity == "error":
                    result["errors"].append(error_message)
                else:
                    result["warnings"].append(error_message)
        if field_schema.data_type and not isinstance(
            field_value, field_schema.data_type
        ):
            try:
                if field_schema.data_type is int and isinstance(field_value, str):
                    result["value"] = int(float(field_value))
                elif field_schema.data_type is float and isinstance(field_value, str):
                    result["value"] = float(field_value)
                elif field_schema.data_type is bool and isinstance(field_value, str):
                    result["value"] = field_value.lower() in (
                        "true",
                        "1",
                        "yes",
                        "on",
                    )
                else:
                    result["value"] = field_schema.data_type(field_value)
            except (ValueError, TypeError) as e:
                result["errors"].append(
                    f"Cannot convert '{field_name}' to {
                        field_schema.data_type.__name__
                    }: {e}"
                )
        return result

    def _validate_cross_fields(self, data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Validate relationships between fields.

        Args:
            data: The validated data.

        Returns:
            Dictionary with errors and warnings from cross-field validation.
        """
        errors = []
        warnings = []
        if "on_threshold" in data and "off_threshold" in data:
            if data["off_threshold"] >= data["on_threshold"]:
                warnings.append("off_threshold should be less than on_threshold")
        if "samples" in data and "sample_interval" in data:
            total_sample_time = data["samples"] * data["sample_interval"]
            if total_sample_time > 30.0:
                warnings.append(
                    f"Total sample time ({
                        total_sample_time:.1f}s) is quite long and may affect responsiveness"
                )
        return {"errors": errors, "warnings": warnings}

    def _get_data_key(self, data: Dict[str, Any]) -> str:
        """Generate a cache key for the data.

        Args:
            data: The data dictionary.

        Returns:
            String key for caching.
        """
        sorted_items = sorted(data.items())
        key_parts = [f"{k}:{v}" for k, v in sorted_items]
        return "|".join(key_parts)

    def _get_cached_result(self, data_key: str) -> Optional[ValidationResult]:
        """Retrieve a cached validation result.

        Args:
            data_key: The cache key.

        Returns:
            Cached ValidationResult if available and not expired.
        """
        import time

        if data_key in self._validation_cache:
            result, timestamp = self._validation_cache[data_key]
            if time.time() - timestamp < 300:
                return result
            del self._validation_cache[data_key]
        return None

    def _cache_result(self, data_key: str, result: ValidationResult) -> None:
        """Cache a validation result.

        Args:
            data_key: The cache key.
            result: The validation result to cache.
        """
        import time

        timestamp = time.time()
        self._validation_cache[data_key] = (result, timestamp)
        if len(self._validation_cache) > 50:
            oldest_keys = sorted(
                self._validation_cache.keys(),
                key=lambda k: self._validation_cache[k][1],
            )[:25]
            for key in oldest_keys:
                del self._validation_cache[key]

    def clear_cache(self) -> None:
        """Clear the validation cache."""
        self._validation_cache.clear()
        _LOGGER.debug("Validation cache cleared")

    def get_cache_stats(self) -> Dict[str, int]:
        """Get statistics about the validation cache.

        Returns:
            Dictionary with cache statistics.
        """
        return {
            "cached_entries": len(self._validation_cache),
            "max_cache_size": 50,
        }

    def get_schema_summary(self) -> Dict[str, Any]:
        """Get a summary of the validation schema.

        Returns:
            Dictionary with schema information and cache stats.
        """

        required_fields = []
        optional_fields = []
        for name, schema in self.schema.items():
            if schema.required:
                required_fields.append(name)
            else:
                optional_fields.append(name)
        return {
            "total_fields": len(self.schema),
            "required_fields": required_fields,
            "optional_fields": optional_fields,
            "cache_stats": self.get_cache_stats(),
        }


def create_smartify_data_schema() -> Dict[str, DataSchema]:
    """Create the default data schema for Smartify.

    Returns:
        Dictionary mapping field names to their schema definitions.
    """
    return {
        "device_name": DataSchema(name="device_name", required=True, data_type=str),
        "power_entity": DataSchema(name="power_entity", required=True, data_type=str),
        "on_script": DataSchema(name="on_script", required=True, data_type=str),
        "off_script": DataSchema(name="off_script", required=True, data_type=str),
        "on_threshold": DataSchema(
            name="on_threshold",
            required=False,
            data_type=float,
            min_value=0.1,
            max_value=1000.0,
            default_value=10.0,
        ),
        "off_threshold": DataSchema(
            name="off_threshold",
            required=False,
            data_type=float,
            min_value=0.0,
            max_value=50.0,
            default_value=1.0,
        ),
        "samples": DataSchema(
            name="samples",
            required=False,
            data_type=int,
            min_value=1,
            max_value=20,
            default_value=5,
        ),
        "sample_interval": DataSchema(
            name="sample_interval",
            required=False,
            data_type=float,
            min_value=0.1,
            max_value=10.0,
            default_value=1.0,
        ),
        "command_timeout": DataSchema(
            name="command_timeout",
            required=False,
            data_type=float,
            min_value=1.0,
            max_value=300.0,
            default_value=30.0,
        ),
        "pre_turn_on": DataSchema(
            name="pre_turn_on",
            required=False,
            data_type=bool,
            default_value=False,
        ),
        "pre_turn_on_delay": DataSchema(
            name="pre_turn_on_delay",
            required=False,
            data_type=float,
            min_value=0.1,
            max_value=30.0,
            default_value=2.0,
        ),
    }


def validate_data_consistency(
    datasets: List[Dict[str, Any]],
    consistency_rules: Optional[List[Callable]] = None,
) -> Dict[str, List[str]]:
    """Validate consistency across multiple datasets.

    Args:
        datasets: List of data dictionaries to validate.
        consistency_rules: Optional list of custom consistency rules.

    Returns:
        Dictionary with issues and warnings about consistency.
    """

    issues = []
    warnings = []
    if len(datasets) < 2:
        return {"issues": issues, "warnings": warnings}
    [f"dataset_{i}" for i in range(len(datasets))]
    all_keys = set()
    for dataset in datasets:
        all_keys.update(dataset.keys())
    for key in all_keys:
        values = [dataset.get(key) for dataset in datasets]
        types = [type(v) for v in values if v is not None]
        if len(set(types)) > 1:
            warnings.append(f"Type inconsistency for field '{key}': {types}")
    return {"issues": issues, "warnings": warnings}
