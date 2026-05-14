"""Options validator for Smartify integration.

This module provides functionality to validate options data using schemas.
"""

from typing import Any, Dict

import voluptuous as vol  # type: ignore[import]

from .schema_builder import OptionsSchemaBuilder
from ...di.container import DependencyContainer


class OptionsValidator:
    """Service for validating options data.

    This class applies generated options schemas to validate and normalize
    user input data for Smartify integration options.
    """

    def __init__(self, container: DependencyContainer):
        """Initialize the options validator."""
        self._container = container
        self.logger = container.get("logger")
        self.schema_builder = OptionsSchemaBuilder()

    def validate_data(
        self, data: Dict[str, Any], has_outlet_switch: bool = False
    ) -> Dict[str, Any]:
        """Validate user-provided options data against the schema.

        Applies the generated options schema to validate and normalize user input data.
        Ensures all provided options conform to expected types, ranges, and constraints.
        Can be configured for device-specific validation based on outlet switch capabilities.

        Args:
            data (Dict[str, Any]): Raw user input data containing option values to validate.
            has_outlet_switch (bool): Whether to include outlet switch related options
                in validation. If True, validates pre-turn-on options as well. Defaults to False
                for general validation.

        Returns:
            Dict[str, Any]: Validated and normalized options data with defaults applied
                for missing optional fields.

        Raises:
            vol.Invalid: If the provided data fails validation (e.g., invalid types,
                out-of-range values, or missing required fields).
        """
        schema = self.schema_builder.build_schema(has_outlet_switch)

        try:
            validated_data = schema(data)
            self.logger.debug("Options data validated successfully")
            return validated_data
        except vol.Invalid as e:
            self.logger.error(
                "Options validation failed: %s",
                e,
                exc_info=True,
            )
            raise
