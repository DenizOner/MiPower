"""Options form builder for Smartify integration.

This module provides functionality to build options forms for the options flow.
"""

from homeassistant.config_entries import ConfigEntry  # type: ignore[import]
from homeassistant.data_entry_flow import FlowResult  # type: ignore[import]

from .analyzer import DeviceCapabilitiesAnalyzer
from ...di.container import DependencyContainer


class OptionsFormBuilder:
    """Service for building options forms.

    This class generates complete form configurations for the options flow,
    including dynamic schema generation based on device capabilities.
    """

    def __init__(self, hass, container: DependencyContainer):
        """Initialize the options form builder.

        Args:
            hass: Home Assistant instance
            container: Dependency injection container
        """
        self.hass = hass
        self._container = container
        self.logger = container.get("logger")
        self.capabilities_analyzer = DeviceCapabilitiesAnalyzer(hass)

    async def build_form(self, config_entry: ConfigEntry) -> FlowResult:
        """Create an options form configuration for the Smartify device.

        Generates a complete form configuration for the options flow, including
        dynamic schema generation based on device capabilities and proper error handling.

        Args:
            config_entry (ConfigEntry): The configuration entry for the device whose
                options form is being created.

        Returns:
            FlowResult: A form configuration dictionary with schema, placeholders,
                and step information for the options flow.

        Raises:
            Exception: If form creation fails, returns an abort result with reason.
        """
        try:
            capabilities = await self.capabilities_analyzer.analyze_capabilities(
                config_entry
            )

            result = {
                "type": "form",
                "step_id": "manual_options",
                "data_schema": None,  # Will be set by caller using schema builder
                "description_placeholders": {"device_name": config_entry.title},
                "capabilities": capabilities,  # Pass capabilities for schema building
            }

            self.logger.debug("Created options form for device: %s", config_entry.title)
            return result

        except Exception as e:
            self.logger.error(
                "Error creating options form: %s",
                e,
                exc_info=True,
            )
            return {"type": "abort", "reason": "form_creation_failed"}
