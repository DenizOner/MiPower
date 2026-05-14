"""Step handlers for Smartify configuration flow.

This module provides step handling services following SOLID principles,
separating step logic from the main configuration flow.
"""

import logging
from typing import Any, Dict, List, Optional, Tuple

from homeassistant.config_entries import ConfigFlowResult  # type: ignore
from homeassistant.data_entry_flow import FlowResult  # type: ignore
from homeassistant.helpers import device_registry as dr  # type: ignore
from homeassistant.helpers import entity_registry as er  # type: ignore

from ...helpers.errors.exceptions import ScriptExecutionError
from ...calibration.const import CALIBRATION_POINTS
from ...const import (
    COMMAND_TIMEOUT,
    CONF_NAME,
    CONF_OFF_SCRIPT,
    CONF_ON_SCRIPT,
    CONF_ON_THRESHOLD,
    CONF_POWER_DEVICE_ID,
    CONF_POWER_ENTITY,
    CONF_REMOTE_DEVICE_ID,
    OFF_THRESHOLD,
    ON_THRESHOLD,
    PRE_TURN_ON,
    PRE_TURN_ON_DELAY,
    SAMPLE_INTERVAL,
    SAMPLES,
)
from ...di.container import DependencyContainer
from ...helpers.config.validator import (
    ConfigValidator,
    create_full_config_schema,
)
from ...helpers.config_flow.discovery_interface import (
    DiscoveryInterface,
)
from ...helpers.config_flow.handler_interface import ConfigFlowHandlerInterface
from ...helpers.config_flow.schema_builder_interface import (
    ConfigSchemaBuilderInterface,
)
from ...helpers.config_flow.validator_interface import (
    ConfigValidatorInterface,
)
from ...helpers.logger.config_flow_logger import handler_method_logging

_LOGGER = logging.getLogger(__name__)

# Constants for magic strings
WARNING_NO_POWER_DEVICES = (
    "No power devices found automatically, falling back to manual entry."
)
WARNING_NO_REMOTE_DEVICES = (
    "No remote devices found automatically, continuing with fallback."
)
ERROR_DEVICE_HAS_NO_POWER_ENTITY = (
    "Could not find power entity for device ID: {device_id}"
)
ERROR_INVALID_POWER_ENTITY = (
    "Validation failed: Selected entity '{entity_id}' is not a valid power entity."
)
ERROR_VALIDATION_ERROR = "Error during power device validation: {error}"
ERROR_UNKNOWN_ERROR = "An unexpected error occurred in the {step} step: {error}"
ERROR_CONFIG_VALIDATION_FAILED = "Configuration validation failed: {errors}"
ERROR_NO_SCRIPTS_FOUND = "No scripts found for the selected remote device. Please create ON and OFF scripts for your remote device first."


class StepHandler(ConfigFlowHandlerInterface):
    """Handler for configuration flow steps following Single Responsibility Principle."""

    @handler_method_logging("step_handler")
    def __init__(
        self,
        config_flow_instance,
        container: Optional[DependencyContainer],
        schema_builder: ConfigSchemaBuilderInterface,
        validator: ConfigValidatorInterface,
        discovery: DiscoveryInterface,
    ):
        """Initialize the step handler.

        Args:
            config_flow_instance: The parent ConfigFlow instance.
            container: Dependency injection container.
            schema_builder: Schema builder service.
            validator: Configuration validator.
            discovery: Discovery service.
        """
        try:
            _LOGGER.info("StepHandler.__init__ started - comprehensive logging active")
            _LOGGER.debug("StepHandler.__init__ started")
            _LOGGER.debug(f"Config flow instance: {config_flow_instance}")
            _LOGGER.debug(f"Container: {container}")
            self.config_flow = config_flow_instance
            self.hass = config_flow_instance.hass
            _LOGGER.debug("Hass instance assigned")
            self._user_input = config_flow_instance._user_input
            _LOGGER.debug("User input assigned")
            self._container = container
            _LOGGER.debug("Container assigned")

            # Inject dependencies
            _LOGGER.debug("Injecting dependencies")
            self.schema_builder = schema_builder
            _LOGGER.debug("Schema builder injected")
            self.validator = validator
            _LOGGER.debug("Validator injected")
            self.discovery = discovery
            _LOGGER.debug("Discovery injected")
            _LOGGER.debug("StepHandler initialized successfully")
            _LOGGER.info("StepHandler.__init__ completed successfully")
        except Exception as e:
            _LOGGER.error(f"StepHandler.__init__ error: {e}", exc_info=True)
            _LOGGER.error(
                f"Error context - config_flow_instance: {config_flow_instance}, container: {container}"
            )
            raise
        finally:
            _LOGGER.debug("StepHandler.__init__ finally block executed")

    @handler_method_logging("step_handler")
    async def _convert_device_id_to_entity_id(self, device_id: str) -> Optional[str]:
        """Convert a device ID to its associated power sensor entity ID.

        Args:
            device_id: The device ID to convert.

        Returns:
            The power sensor entity ID for the device, or None if not found.
        """
        try:
            _LOGGER.info(
                f"_convert_device_id_to_entity_id started - comprehensive logging active, device_id: {device_id}"
            )
            # This is needed if CONF_POWER_DEVICE_ID contains actual device IDs
            # instead of entity IDs from device discovery
            from ...helpers.power.validation import get_power_entity_id

            _LOGGER.debug("get_power_entity_id imported")

            _LOGGER.debug("Getting entity registry")
            entity_registry = er.async_get(self.hass)
            _LOGGER.debug("Getting device registry")
            device_registry = dr.async_get(self.hass)

            _LOGGER.debug(f"Checking device ID: {device_id}")
            if device_id not in device_registry.devices:
                _LOGGER.warning(f"Device ID {device_id} not found in device registry")
                _LOGGER.debug("Device not found, returning None")
                return None

            _LOGGER.debug("Getting power entity ID")
            result = await get_power_entity_id(self.hass, entity_registry, device_id)
            _LOGGER.debug(f"Power entity ID retrieved: {result}")
            _LOGGER.info(
                f"_convert_device_id_to_entity_id completed successfully - result: {result}"
            )
            return result
        except Exception as e:
            _LOGGER.error(
                f"Error converting device ID to entity ID: {e}", exc_info=True
            )
            _LOGGER.error(
                f"Error context - device_id: {device_id}, hass available: {self.hass is not None}"
            )
            return None
        finally:
            _LOGGER.debug("_convert_device_id_to_entity_id finally block executed")

    @handler_method_logging("step_handler")
    def _create_form_response(
        self, step_id: str, schema, errors: Dict[str, str]
    ) -> FlowResult:
        """Create standardized form response.

        Args:
            step_id: The step ID for the form.
            schema: The form schema.
            errors: Dict of errors to display.

        Returns:
            FlowResult for form display.
        """
        try:
            _LOGGER.info(
                f"_create_form_response started - comprehensive logging active, step_id: {step_id}"
            )
            _LOGGER.debug(
                f"Creating form response - step_id: {step_id}, errors: {errors}"
            )
            result = self.config_flow.async_show_form(
                step_id=step_id, data_schema=schema, errors=errors
            )
            _LOGGER.debug("Form response created successfully")
            _LOGGER.info("_create_form_response completed successfully")
            return result
        except Exception as e:
            _LOGGER.error(f"_create_form_response error: {e}", exc_info=True)
            _LOGGER.error(f"Error context - step_id: {step_id}, errors: {errors}")
            raise
        finally:
            _LOGGER.debug("_create_form_response finally block executed")

    @handler_method_logging("step_handler")
    async def _handle_discovery_error(self, operation: str, error: Exception) -> list:
        """Handle device discovery errors with standardized logging.

        Args:
            operation: Description of the operation that failed.
            error: The exception that occurred.

        Returns:
            Empty list as fallback.
        """
        _LOGGER.warning(f"Error during {operation}: %s", error)
        return []

    @handler_method_logging("step_handler")
    async def _validate_user_input(
        self, user_input: Dict[str, Any]
    ) -> Tuple[Dict[str, str], bool]:
        """Validate user input for the user step.

        Args:
            user_input: User submitted form data.

        Returns:
            Tuple of (errors_dict, should_proceed_to_scripts).
        """
        errors: Dict[str, str] = {}

        try:
            _LOGGER.debug("Validating user's power device selection.")
            selected_device_id = user_input[CONF_POWER_DEVICE_ID]

            # Check if selected_device_id is a device ID (starts with letter) or entity ID
            if selected_device_id.startswith(("sensor.", "switch.", "binary_sensor.")):
                # It's already an entity ID
                selected_entity_id = selected_device_id
                _LOGGER.debug(f"Selected power entity ID: {selected_entity_id}")
            else:
                # It's a device ID, find the corresponding power entity
                selected_entity_id = await self._convert_device_id_to_entity_id(
                    selected_device_id
                )
                if not selected_entity_id:
                    _LOGGER.error(
                        ERROR_DEVICE_HAS_NO_POWER_ENTITY.format(
                            device_id=selected_device_id
                        ),
                        exc_info=True,
                    )
                    errors["base"] = "device_has_no_power_entity"
                    return errors, False
                else:
                    _LOGGER.debug(
                        f"Converted device ID to power entity ID: {selected_entity_id}"
                    )

            # Power entity validation
            _LOGGER.info("Power entity validation started")
            if not await self.validator.validate_power_entity(selected_entity_id):
                _LOGGER.error(
                    ERROR_INVALID_POWER_ENTITY.format(entity_id=selected_entity_id),
                    exc_info=True,
                )
                errors["base"] = "invalid_power_entity"
                return errors, False

            _LOGGER.debug(
                f"Validation successful for power entity: {selected_entity_id}"
            )
            self._user_input[CONF_POWER_ENTITY] = selected_entity_id

            # Convert remote device ID to entity ID
            remote_entity_id = self.validator.convert_remote_device_to_entity(
                user_input[CONF_REMOTE_DEVICE_ID]
            )
            self._user_input[CONF_REMOTE_DEVICE_ID] = remote_entity_id
            _LOGGER.debug(
                f"Converted remote device ID to entity ID: {remote_entity_id}"
            )

            return errors, True

        except Exception as validation_error:
            _LOGGER.error(
                ERROR_VALIDATION_ERROR.format(error=validation_error),
                exc_info=True,
            )
            errors["base"] = "validation_error"
            return errors, False

    @handler_method_logging("step_handler")
    async def _discover_devices(self) -> Tuple[List[Any], List[Any], Dict[str, str]]:
        """Discover power and remote devices.

        Returns:
            Tuple of (power_devices, remote_devices, errors).
        """
        errors: Dict[str, str] = {}

        _LOGGER.info("Device discovery started")

        # Discover power devices
        try:
            _LOGGER.info("Power device discovery started")
            power_devices = await self.discovery.discover_power_devices()
            _LOGGER.info(
                f"Power device discovery completed, found {len(power_devices)} power devices"
            )
        except Exception as e:
            power_devices = await self._handle_discovery_error(
                "power device discovery (possibly during config flow init)", e
            )

        # Discover remote devices
        try:
            _LOGGER.info("Remote device discovery started")
            remote_devices = await self.discovery.discover_remote_devices()
            _LOGGER.info(
                f"Remote device discovery completed, found {len(remote_devices)} remote devices"
            )
        except Exception as e:
            remote_devices = await self._handle_discovery_error(
                "remote device discovery", e
            )

        return power_devices, remote_devices, errors

    @handler_method_logging("step_handler")
    async def handle_user_step(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle the initial user step of the configuration flow.

        Args:
            user_input: Optional dictionary containing user-submitted form data.

        Returns:
            The result of the configuration flow step.
        """
        _LOGGER.info("handle_user_step started")
        errors: Dict[str, str] = {}
        _LOGGER.debug("Executing config flow step: user")

        try:
            if user_input is not None:
                return await self._handle_user_input_with_progress(user_input)

            return await self._handle_discovery_flow(errors)

        except Exception as e:
            _LOGGER.critical(
                ERROR_UNKNOWN_ERROR.format(step="user", error=e),
                exc_info=True,
            )
            errors["base"] = "unknown"
            return self._create_form_response(
                "user",
                self.schema_builder._build_fallback_schema(),
                errors,
            )

    @handler_method_logging("step_handler")
    async def _handle_user_input_with_progress(
        self, user_input: Dict[str, Any]
    ) -> FlowResult:
        """Handle user input with progress indication.

        Args:
            user_input: User submitted form data.

        Returns:
            FlowResult for next step or error form.
        """
        # Show progress for device discovery
        self.config_flow.async_show_progress(
            step_id="user",
            progress_action="device_discovery",
            progress_task="Discovering power and remote devices...",
        )
        _LOGGER.debug(f"User submitted data for the 'user' step: {user_input}")
        self._user_input.update(user_input)

        errors, should_proceed = await self._validate_user_input(user_input)

        if should_proceed:
            return await self.config_flow.async_step_scripts()

        # Return form with validation errors
        return self._create_form_response(
            "user",
            self.schema_builder._build_fallback_schema(),
            errors,
        )

    @handler_method_logging("step_handler")
    async def _handle_discovery_flow(self, errors: Dict[str, str]) -> FlowResult:
        """Handle device discovery flow when no user input provided.

        Args:
            errors: Current error dictionary.

        Returns:
            FlowResult for device selection or fallback form.
        """
        power_devices, remote_devices, discovery_errors = await self._discover_devices()
        errors.update(discovery_errors)

        # Handle cases with no devices found
        if not power_devices:
            _LOGGER.warning(WARNING_NO_POWER_DEVICES)
            schema = self.schema_builder._build_fallback_schema()
            return self._create_form_response("user", schema, errors)

        if not remote_devices:
            _LOGGER.warning(WARNING_NO_REMOTE_DEVICES)
            schema = self.schema_builder._build_fallback_schema()
            return self._create_form_response("user", schema, errors)

        # Build schema with discovered devices
        schema = self.schema_builder.build_device_config_schema(
            power_devices, remote_devices
        )
        return self._create_form_response("user", schema, errors)

    @handler_method_logging("step_handler")
    async def handle_scripts_step(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> ConfigFlowResult:
        """Handle the scripts selection step of the configuration flow.

        Args:
            user_input: Optional dictionary containing script selection data.

        Returns:
            The result of the configuration flow step.
        """
        _LOGGER.info("handle_scripts_step started")
        _LOGGER.debug("Executing config flow step: scripts")

        try:
            remote_entity_id = self._user_input[CONF_REMOTE_DEVICE_ID]
            device_scripts = await self._discover_scripts_for_device(remote_entity_id)

            if user_input is not None:
                return await self._process_script_selection(user_input, device_scripts)

            return self._create_script_selection_form(device_scripts)

        except Exception as e:
            _LOGGER.critical(
                ERROR_UNKNOWN_ERROR.format(step="scripts", error=e),
                exc_info=True,
            )
            return self.config_flow.async_abort(reason="unknown")

    @handler_method_logging("step_handler")
    async def _discover_scripts_for_device(self, remote_entity_id: str) -> list:
        """Discover scripts for the selected remote device.

        Args:
            remote_entity_id: Remote device entity ID.

        Returns:
            List of discovered scripts.

        Raises:
            Exception: If no scripts are found for the device.
        """
        _LOGGER.debug("Preparing script list for the script selection form.")
        _LOGGER.debug("Selected remote entity ID: %s", remote_entity_id)

        _LOGGER.info("Script discovery started")
        device_scripts = await self.discovery.discover_scripts_for_device(
            remote_entity_id
        )
        _LOGGER.info(f"Script discovery completed, found {len(device_scripts)} scripts")

        if not device_scripts:
            _LOGGER.critical(ERROR_NO_SCRIPTS_FOUND, exc_info=True)
            raise ScriptExecutionError("No scripts found for device")

        return device_scripts

    @handler_method_logging("step_handler")
    async def _process_script_selection(
        self, user_input: Dict[str, Any], device_scripts: list
    ) -> FlowResult:
        """Process user script selection and create config entry.

        Args:
            user_input: User script selection data.
            device_scripts: Available scripts for the device.

        Returns:
            FlowResult for config entry creation or error form.
        """
        _LOGGER.debug(f"User submitted script selection data: {user_input}")
        self._user_input.update(user_input)

        final_data = self._build_final_config_data()
        validation_result = await self._validate_final_config(final_data)

        if not validation_result.is_valid:
            _LOGGER.error(
                ERROR_CONFIG_VALIDATION_FAILED.format(errors=validation_result.errors),
                exc_info=True,
            )
            return self._create_form_response(
                "scripts",
                self.schema_builder.build_scripts_schema(device_scripts),
                {},
            )

        return await self._create_config_entry(final_data)

    @handler_method_logging("step_handler")
    def _build_final_config_data(self) -> Dict[str, Any]:
        """Build final configuration data from user input.

        Returns:
            Dict containing final configuration data.
        """
        device_name = (self._user_input.get(CONF_NAME) or "").strip() or "Device"
        return {
            CONF_NAME: device_name,
            CONF_POWER_ENTITY: self._user_input[CONF_POWER_ENTITY],
            CONF_REMOTE_DEVICE_ID: self._user_input[CONF_REMOTE_DEVICE_ID],
            CONF_ON_SCRIPT: self._user_input[CONF_ON_SCRIPT],
            CONF_OFF_SCRIPT: self._user_input[CONF_OFF_SCRIPT],
            CONF_ON_THRESHOLD: ON_THRESHOLD["default"],
        }

    @handler_method_logging("step_handler")
    async def _validate_final_config(self, final_data: Dict[str, Any]) -> Any:
        """Validate final configuration data.

        Args:
            final_data: Configuration data to validate.

        Returns:
            Validation result object.
        """
        schema = create_full_config_schema()
        config_validator = ConfigValidator(schema)
        return config_validator.validate_config(final_data)

    @handler_method_logging("step_handler")
    async def _create_config_entry(self, final_data: Dict[str, Any]) -> FlowResult:
        """Create the final config entry.

        Args:
            final_data: Validated configuration data.

        Returns:
            FlowResult for config entry.
        """
        suggested_title = final_data[CONF_NAME]
        _LOGGER.info(
            f"Configuration flow completed. Creating new entry: '{suggested_title}'"
        )

        # Default options
        options_data = {
            "on_threshold": ON_THRESHOLD["default"],
            "off_threshold": OFF_THRESHOLD["default"],
            "samples": SAMPLES["default"],
            "sample_interval": SAMPLE_INTERVAL["default"],
            "command_timeout": COMMAND_TIMEOUT["default"],
            "pre_turn_on": PRE_TURN_ON,
            "pre_turn_on_delay": PRE_TURN_ON_DELAY["default"],
            "calibration_points": CALIBRATION_POINTS["default"],
        }

        entry = self.config_flow.async_create_entry(
            title=suggested_title,
            data=final_data,
            options=options_data,
        )

        return entry

    @handler_method_logging("step_handler")
    def _create_script_selection_form(self, device_scripts: list) -> FlowResult:
        """Create the script selection form.

        Args:
            device_scripts: Available scripts for the device.

        Returns:
            FlowResult for script selection form.
        """
        schema = self.schema_builder.build_scripts_schema(device_scripts)
        return self._create_form_response("scripts", schema, {})
