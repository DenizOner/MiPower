"""Options processor for Smartify integration.

This module provides functionality to process and save options updates.
"""

from typing import Any, Dict

import voluptuous as vol  # type: ignore[import]
from homeassistant.config_entries import ConfigEntry  # type: ignore[import]
from homeassistant.data_entry_flow import FlowResult  # type: ignore[import]

from .analyzer import DeviceCapabilitiesAnalyzer
from .validator import OptionsValidator
from ...di.container import DependencyContainer


class OptionsProcessor:
    """Service for processing options updates.

    This class validates user-provided options data, logs updates, and creates
    configuration entries with new options.
    """

    def __init__(self, hass, container: DependencyContainer):
        """Initialize the options processor.

        Args:
            hass: Home Assistant instance
            container: Dependency injection container
        """
        self.hass = hass
        self._container = container
        self.logger = container.get("logger")
        self.capabilities_analyzer = DeviceCapabilitiesAnalyzer(hass)
        self.validator = OptionsValidator(container)

    async def process_update(
        self,
        config_entry: ConfigEntry,
        user_input: Dict[str, Any],
        options_flow_handler=None,
    ) -> FlowResult:
        """Process and save updated options for a Smartify device.

        Validates the user-provided options data using device-specific validation,
        logs the update, and creates a configuration entry with the new options.
        Handles validation errors and other processing exceptions gracefully.

        Args:
            config_entry (ConfigEntry): The configuration entry for the device being updated.
            user_input (Dict[str, Any]): Raw user input data containing the new option values.
            options_flow_handler: The OptionsFlow handler to call create_entry/abort on.

        Returns:
            FlowResult: Either a successful create_entry result with the validated options,
                or an abort result with an appropriate error reason.
        """
        try:
            capabilities = await self.capabilities_analyzer.analyze_capabilities(
                config_entry
            )
            validated_data = self.validator.validate_data(
                user_input, capabilities["has_outlet_switch"]
            )

            self.logger.info(
                "Options updated for device '%s': %s",
                config_entry.title,
                validated_data,
            )

            # Call create_entry directly on the options flow handler
            if options_flow_handler is not None:
                return options_flow_handler.async_create_entry(
                    title="", data=validated_data
                )
            else:
                # Fallback for backward compatibility
                return {
                    "type": "create_entry",
                    "title": "",
                    "data": validated_data,
                }

        except vol.Invalid as e:
            self.logger.error(
                "Options validation failed: %s",
                e,
                exc_info=True,
            )
            # Call abort directly on the options flow handler
            if options_flow_handler is not None:
                return options_flow_handler.async_abort(reason="validation_failed")
            else:
                return {
                    "type": "abort",
                    "reason": "validation_failed",
                }

        except Exception as e:
            self.logger.error(
                "Unexpected error processing options: %s",
                e,
                exc_info=True,
            )
            # Call abort directly on the options flow handler
            if options_flow_handler is not None:
                return options_flow_handler.async_abort(reason="processing_failed")
            else:
                return {
                    "type": "abort",
                    "reason": "processing_failed",
                }
