"""Options schema builder for Smartify integration.

This module provides functionality to build voluptuous schemas for options flow.
"""

from typing import Any, Dict, List

import voluptuous as vol  # type: ignore[import]
from homeassistant.helpers import config_validation as cv  # type: ignore[import]
from homeassistant.helpers.selector import (  # type: ignore[import]
    BooleanSelector,
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
)
from voluptuous import Coerce  # type: ignore[import]

from ...const import (
    COMMAND_TIMEOUT,
    CONF_COMMAND_TIMEOUT,
    CONF_EVENT_COOLDOWN,
    CONF_OFF_DEBOUNCE_TIME,
    CONF_OFF_THRESHOLD,
    CONF_ON_DEBOUNCE_TIME,
    CONF_ON_THRESHOLD,
    CONF_POST_COMMAND_DELAY,
    CONF_POWER_CHANGE_THRESHOLD,
    CONF_PRE_TURN_ON,
    CONF_PRE_TURN_ON_DELAY,
    CONF_RETRY_COUNT,
    CONF_RETRY_INTERVAL,
    CONF_STATE_VERIFICATION_INTERVAL,
    CONF_STATE_VERIFICATION_RETRIES,
    CONF_VERIFY_DELAY,
    EVENT_COOLDOWN,
    OFF_DEBOUNCE_TIME,
    OFF_THRESHOLD,
    ON_DEBOUNCE_TIME,
    ON_THRESHOLD,
    POST_COMMAND_DELAY,
    POWER_CHANGE_THRESHOLD,
    PRE_TURN_ON,
    PRE_TURN_ON_DELAY,
    RETRY_COUNT,
    RETRY_INTERVAL,
    STATE_VERIFICATION_INTERVAL,
    STATE_VERIFICATION_RETRIES,
    VERIFY_DELAY,
)

from ..config_flow.schema_builder_interface import ConfigSchemaBuilderInterface


class OptionsSchemaBuilder(ConfigSchemaBuilderInterface):
    """Service for building options schemas.

    This class generates voluptuous validation schemas for Smartify options configuration,
    dynamically including outlet switch-related options when available.
    """

    @staticmethod
    def build_schema(
        has_outlet_switch: bool = False, slider_mode: bool = False
    ) -> vol.Schema:
        """Generate a voluptuous schema for Smartify options configuration.

        Creates a validation schema for Smartify integration options, dynamically
        including outlet switch-related options if the device has outlet control capabilities.

        Args:
            has_outlet_switch (bool): Whether the device has outlet switch capabilities.
                If True, includes pre-turn-on options in the schema.

        Returns:
            vol.Schema: A voluptuous schema object containing all available configuration
                options with their validation rules, defaults, and constraints.
        """
        schema = vol.Schema({})

        if has_outlet_switch:
            schema = schema.extend(
                {
                    vol.Optional(CONF_PRE_TURN_ON, default=PRE_TURN_ON): cv.boolean,
                    vol.Optional(
                        CONF_PRE_TURN_ON_DELAY,
                        default=PRE_TURN_ON_DELAY["default"],
                    ): vol.All(
                        vol.Coerce(float),
                        vol.Range(
                            min=PRE_TURN_ON_DELAY["min"],
                            max=PRE_TURN_ON_DELAY["max"],
                        ),
                    ),
                }
            )

        schema = schema.extend(
            {
                vol.Optional(
                    CONF_ON_THRESHOLD, default=ON_THRESHOLD["default"]
                ): vol.All(
                    Coerce(float),
                    vol.Range(min=ON_THRESHOLD["min"], max=ON_THRESHOLD["max"]),
                ),
                vol.Optional(
                    CONF_OFF_THRESHOLD, default=OFF_THRESHOLD["default"]
                ): vol.All(
                    Coerce(float),
                    vol.Range(min=OFF_THRESHOLD["min"], max=OFF_THRESHOLD["max"]),
                ),
                vol.Optional(
                    CONF_RETRY_INTERVAL, default=RETRY_INTERVAL["default"]
                ): vol.All(
                    Coerce(float),
                    vol.Range(min=RETRY_INTERVAL["min"], max=RETRY_INTERVAL["max"]),
                ),
                vol.Optional(CONF_RETRY_COUNT, default=RETRY_COUNT["default"]): vol.All(
                    Coerce(float),
                    vol.Range(min=RETRY_COUNT["min"], max=RETRY_COUNT["max"]),
                ),
                vol.Optional(
                    CONF_VERIFY_DELAY, default=VERIFY_DELAY["default"]
                ): vol.All(
                    Coerce(float),
                    vol.Range(min=VERIFY_DELAY["min"], max=VERIFY_DELAY["max"]),
                ),
                vol.Optional(
                    CONF_COMMAND_TIMEOUT, default=COMMAND_TIMEOUT["default"]
                ): vol.All(
                    Coerce(float),
                    vol.Range(min=COMMAND_TIMEOUT["min"], max=COMMAND_TIMEOUT["max"]),
                ),
                vol.Optional(
                    CONF_ON_DEBOUNCE_TIME, default=ON_DEBOUNCE_TIME["default"]
                ): vol.All(
                    Coerce(float),
                    vol.Range(min=ON_DEBOUNCE_TIME["min"], max=ON_DEBOUNCE_TIME["max"]),
                ),
                vol.Optional(
                    CONF_OFF_DEBOUNCE_TIME, default=OFF_DEBOUNCE_TIME["default"]
                ): vol.All(
                    Coerce(float),
                    vol.Range(
                        min=OFF_DEBOUNCE_TIME["min"], max=OFF_DEBOUNCE_TIME["max"]
                    ),
                ),
                vol.Optional(
                    CONF_POST_COMMAND_DELAY,
                    default=POST_COMMAND_DELAY["default"],
                ): vol.All(
                    Coerce(float),
                    vol.Range(
                        min=POST_COMMAND_DELAY["min"],
                        max=POST_COMMAND_DELAY["max"],
                    ),
                ),
                vol.Optional(
                    CONF_STATE_VERIFICATION_RETRIES,
                    default=STATE_VERIFICATION_RETRIES["default"],
                ): vol.All(
                    Coerce(float),
                    vol.Range(
                        min=STATE_VERIFICATION_RETRIES["min"],
                        max=STATE_VERIFICATION_RETRIES["max"],
                    ),
                ),
                vol.Optional(
                    CONF_STATE_VERIFICATION_INTERVAL,
                    default=STATE_VERIFICATION_INTERVAL["default"],
                ): vol.All(
                    Coerce(float),
                    vol.Range(
                        min=STATE_VERIFICATION_INTERVAL["min"],
                        max=STATE_VERIFICATION_INTERVAL["max"],
                    ),
                ),
                vol.Optional(
                    CONF_POWER_CHANGE_THRESHOLD,
                    default=POWER_CHANGE_THRESHOLD["default"],
                ): vol.All(
                    Coerce(float),
                    vol.Range(
                        min=POWER_CHANGE_THRESHOLD["min"],
                        max=POWER_CHANGE_THRESHOLD["max"],
                    ),
                ),
                vol.Optional(
                    CONF_EVENT_COOLDOWN,
                    default=EVENT_COOLDOWN["default"],
                ): vol.All(
                    Coerce(float),
                    vol.Range(
                        min=EVENT_COOLDOWN["min"],
                        max=EVENT_COOLDOWN["max"],
                    ),
                ),
            }
        )

        # Return the schema as-is, slider configuration will be handled differently
        return schema

    @staticmethod
    def build_voluptuous_schema_with_defaults(
        has_outlet_switch: bool = False,
        current_options: Dict[str, Any] | None = None,
    ) -> vol.Schema:
        """Generate a voluptuous schema with current values as defaults and slider mode.

        Args:
            has_outlet_switch (bool): Whether the device has outlet switch capabilities.
            current_options (Dict[str, Any] | None): Current options to use as defaults.

        Returns:
            vol.Schema: A voluptuous schema with current values as defaults.
        """
        current_options = current_options or {}

        schema = vol.Schema({})

        if has_outlet_switch:
            schema = schema.extend(
                {
                    vol.Optional(
                        CONF_PRE_TURN_ON,
                        default=current_options.get(CONF_PRE_TURN_ON, PRE_TURN_ON),
                    ): cv.boolean,
                    vol.Optional(
                        CONF_PRE_TURN_ON_DELAY,
                        default=current_options.get(
                            CONF_PRE_TURN_ON_DELAY,
                            PRE_TURN_ON_DELAY["default"],
                        ),
                    ): vol.All(
                        vol.Coerce(float),
                        vol.Range(
                            min=PRE_TURN_ON_DELAY["min"],
                            max=PRE_TURN_ON_DELAY["max"],
                        ),
                    ),
                }
            )

        # Base number fields with current values as defaults
        number_field_defaults = {
            CONF_ON_THRESHOLD: current_options.get(
                CONF_ON_THRESHOLD, ON_THRESHOLD["default"]
            ),
            CONF_OFF_THRESHOLD: current_options.get(
                CONF_OFF_THRESHOLD, OFF_THRESHOLD["default"]
            ),
            CONF_RETRY_INTERVAL: current_options.get(
                CONF_RETRY_INTERVAL, RETRY_INTERVAL["default"]
            ),
            CONF_RETRY_COUNT: current_options.get(
                CONF_RETRY_COUNT, RETRY_COUNT["default"]
            ),
            CONF_VERIFY_DELAY: current_options.get(
                CONF_VERIFY_DELAY, VERIFY_DELAY["default"]
            ),
            CONF_COMMAND_TIMEOUT: current_options.get(
                CONF_COMMAND_TIMEOUT, COMMAND_TIMEOUT["default"]
            ),
            CONF_ON_DEBOUNCE_TIME: current_options.get(
                CONF_ON_DEBOUNCE_TIME, ON_DEBOUNCE_TIME["default"]
            ),
            CONF_OFF_DEBOUNCE_TIME: current_options.get(
                CONF_OFF_DEBOUNCE_TIME, OFF_DEBOUNCE_TIME["default"]
            ),
            CONF_POST_COMMAND_DELAY: current_options.get(
                CONF_POST_COMMAND_DELAY, POST_COMMAND_DELAY["default"]
            ),
            CONF_STATE_VERIFICATION_RETRIES: current_options.get(
                CONF_STATE_VERIFICATION_RETRIES,
                STATE_VERIFICATION_RETRIES["default"],
            ),
            CONF_STATE_VERIFICATION_INTERVAL: current_options.get(
                CONF_STATE_VERIFICATION_INTERVAL,
                STATE_VERIFICATION_INTERVAL["default"],
            ),
            CONF_POWER_CHANGE_THRESHOLD: current_options.get(
                CONF_POWER_CHANGE_THRESHOLD, POWER_CHANGE_THRESHOLD["default"]
            ),
            CONF_EVENT_COOLDOWN: current_options.get(
                CONF_EVENT_COOLDOWN, EVENT_COOLDOWN["default"]
            ),
        }

        schema = schema.extend(
            {
                vol.Optional(
                    CONF_ON_THRESHOLD,
                    default=number_field_defaults[CONF_ON_THRESHOLD],
                ): vol.All(
                    Coerce(float),
                    vol.Range(min=ON_THRESHOLD["min"], max=ON_THRESHOLD["max"]),
                ),
                vol.Optional(
                    CONF_OFF_THRESHOLD,
                    default=number_field_defaults[CONF_OFF_THRESHOLD],
                ): vol.All(
                    Coerce(float),
                    vol.Range(min=OFF_THRESHOLD["min"], max=OFF_THRESHOLD["max"]),
                ),
                vol.Optional(
                    CONF_RETRY_INTERVAL,
                    default=number_field_defaults[CONF_RETRY_INTERVAL],
                ): vol.All(
                    Coerce(float),
                    vol.Range(min=RETRY_INTERVAL["min"], max=RETRY_INTERVAL["max"]),
                ),
                vol.Optional(
                    CONF_RETRY_COUNT,
                    default=number_field_defaults[CONF_RETRY_COUNT],
                ): vol.All(
                    Coerce(float),
                    vol.Range(min=RETRY_COUNT["min"], max=RETRY_COUNT["max"]),
                ),
                vol.Optional(
                    CONF_VERIFY_DELAY,
                    default=number_field_defaults[CONF_VERIFY_DELAY],
                ): vol.All(
                    Coerce(float),
                    vol.Range(min=VERIFY_DELAY["min"], max=VERIFY_DELAY["max"]),
                ),
                vol.Optional(
                    CONF_COMMAND_TIMEOUT,
                    default=number_field_defaults[CONF_COMMAND_TIMEOUT],
                ): vol.All(
                    Coerce(float),
                    vol.Range(min=COMMAND_TIMEOUT["min"], max=COMMAND_TIMEOUT["max"]),
                ),
                vol.Optional(
                    CONF_ON_DEBOUNCE_TIME,
                    default=number_field_defaults[CONF_ON_DEBOUNCE_TIME],
                ): vol.All(
                    Coerce(float),
                    vol.Range(min=ON_DEBOUNCE_TIME["min"], max=ON_DEBOUNCE_TIME["max"]),
                ),
                vol.Optional(
                    CONF_OFF_DEBOUNCE_TIME,
                    default=number_field_defaults[CONF_OFF_DEBOUNCE_TIME],
                ): vol.All(
                    Coerce(float),
                    vol.Range(
                        min=OFF_DEBOUNCE_TIME["min"], max=OFF_DEBOUNCE_TIME["max"]
                    ),
                ),
                vol.Optional(
                    CONF_POST_COMMAND_DELAY,
                    default=number_field_defaults[CONF_POST_COMMAND_DELAY],
                ): vol.All(
                    Coerce(float),
                    vol.Range(
                        min=POST_COMMAND_DELAY["min"],
                        max=POST_COMMAND_DELAY["max"],
                    ),
                ),
                vol.Optional(
                    CONF_STATE_VERIFICATION_RETRIES,
                    default=number_field_defaults[CONF_STATE_VERIFICATION_RETRIES],
                ): vol.All(
                    Coerce(float),
                    vol.Range(
                        min=STATE_VERIFICATION_RETRIES["min"],
                        max=STATE_VERIFICATION_RETRIES["max"],
                    ),
                ),
                vol.Optional(
                    CONF_STATE_VERIFICATION_INTERVAL,
                    default=number_field_defaults[CONF_STATE_VERIFICATION_INTERVAL],
                ): vol.All(
                    Coerce(float),
                    vol.Range(
                        min=STATE_VERIFICATION_INTERVAL["min"],
                        max=STATE_VERIFICATION_INTERVAL["max"],
                    ),
                ),
                vol.Optional(
                    CONF_POWER_CHANGE_THRESHOLD,
                    default=number_field_defaults[CONF_POWER_CHANGE_THRESHOLD],
                ): vol.All(
                    Coerce(float),
                    vol.Range(
                        min=POWER_CHANGE_THRESHOLD["min"],
                        max=POWER_CHANGE_THRESHOLD["max"],
                    ),
                ),
                vol.Optional(
                    CONF_EVENT_COOLDOWN,
                    default=number_field_defaults[CONF_EVENT_COOLDOWN],
                ): vol.All(
                    Coerce(float),
                    vol.Range(
                        min=EVENT_COOLDOWN["min"],
                        max=EVENT_COOLDOWN["max"],
                    ),
                ),
            }
        )

        # Return schema - slider mode handled by HA for number fields
        return schema

    @staticmethod
    def build_simple_schema(
        has_outlet_switch: bool = False,
        current_options: Dict[str, Any] | None = None,
    ) -> vol.Schema:
        """
        Generate a simple voluptuous schema with current values as defaults.

        Based on MiPower integration pattern - uses pure voluptuous without selectors.

        Args:
            has_outlet_switch (bool): Whether the device has outlet switch capabilities.
            current_options (Dict[str, Any] | None): Current config entries to use as defaults.

        Returns:
            vol.Schema: A voluptuous schema with current values as defaults.
        """
        current_options = current_options or {}

        schema = vol.Schema({})

        if has_outlet_switch:
            schema = schema.extend(
                {
                    vol.Optional(
                        CONF_PRE_TURN_ON,
                        default=current_options.get(CONF_PRE_TURN_ON, PRE_TURN_ON),
                    ): cv.boolean,
                    vol.Optional(
                        CONF_PRE_TURN_ON_DELAY,
                        default=current_options.get(
                            CONF_PRE_TURN_ON_DELAY,
                            PRE_TURN_ON_DELAY["default"],
                        ),
                    ): vol.All(
                        vol.Coerce(float),
                        vol.Range(
                            min=PRE_TURN_ON_DELAY["min"],
                            max=PRE_TURN_ON_DELAY["max"],
                        ),
                    ),
                }
            )

        # Number fields with slider-compatible range validators
        schema = schema.extend(
            {
                vol.Optional(
                    CONF_ON_THRESHOLD,
                    default=current_options.get(
                        CONF_ON_THRESHOLD, ON_THRESHOLD["default"]
                    ),
                ): vol.All(
                    Coerce(float),
                    vol.Range(min=ON_THRESHOLD["min"], max=ON_THRESHOLD["max"]),
                ),
                vol.Optional(
                    CONF_OFF_THRESHOLD,
                    default=current_options.get(
                        CONF_OFF_THRESHOLD, OFF_THRESHOLD["default"]
                    ),
                ): vol.All(
                    Coerce(float),
                    vol.Range(min=OFF_THRESHOLD["min"], max=OFF_THRESHOLD["max"]),
                ),
                vol.Optional(
                    CONF_RETRY_INTERVAL,
                    default=current_options.get(
                        CONF_RETRY_INTERVAL, RETRY_INTERVAL["default"]
                    ),
                ): vol.All(
                    Coerce(float),
                    vol.Range(min=RETRY_INTERVAL["min"], max=RETRY_INTERVAL["max"]),
                ),
                vol.Optional(
                    CONF_RETRY_COUNT,
                    default=current_options.get(
                        CONF_RETRY_COUNT, RETRY_COUNT["default"]
                    ),
                ): vol.All(
                    Coerce(float),
                    vol.Range(min=RETRY_COUNT["min"], max=RETRY_COUNT["max"]),
                ),
                vol.Optional(
                    CONF_VERIFY_DELAY,
                    default=current_options.get(
                        CONF_VERIFY_DELAY, VERIFY_DELAY["default"]
                    ),
                ): vol.All(
                    Coerce(float),
                    vol.Range(min=VERIFY_DELAY["min"], max=VERIFY_DELAY["max"]),
                ),
                vol.Optional(
                    CONF_COMMAND_TIMEOUT,
                    default=current_options.get(
                        CONF_COMMAND_TIMEOUT, COMMAND_TIMEOUT["default"]
                    ),
                ): vol.All(
                    Coerce(float),
                    vol.Range(min=COMMAND_TIMEOUT["min"], max=COMMAND_TIMEOUT["max"]),
                ),
                vol.Optional(
                    CONF_ON_DEBOUNCE_TIME,
                    default=current_options.get(
                        CONF_ON_DEBOUNCE_TIME, ON_DEBOUNCE_TIME["default"]
                    ),
                ): vol.All(
                    Coerce(float),
                    vol.Range(min=ON_DEBOUNCE_TIME["min"], max=ON_DEBOUNCE_TIME["max"]),
                ),
                vol.Optional(
                    CONF_OFF_DEBOUNCE_TIME,
                    default=current_options.get(
                        CONF_OFF_DEBOUNCE_TIME, OFF_DEBOUNCE_TIME["default"]
                    ),
                ): vol.All(
                    Coerce(float),
                    vol.Range(
                        min=OFF_DEBOUNCE_TIME["min"], max=OFF_DEBOUNCE_TIME["max"]
                    ),
                ),
                vol.Optional(
                    CONF_POST_COMMAND_DELAY,
                    default=current_options.get(
                        CONF_POST_COMMAND_DELAY, POST_COMMAND_DELAY["default"]
                    ),
                ): vol.All(
                    Coerce(float),
                    vol.Range(
                        min=POST_COMMAND_DELAY["min"],
                        max=POST_COMMAND_DELAY["max"],
                    ),
                ),
                vol.Optional(
                    CONF_STATE_VERIFICATION_RETRIES,
                    default=current_options.get(
                        CONF_STATE_VERIFICATION_RETRIES,
                        STATE_VERIFICATION_RETRIES["default"],
                    ),
                ): vol.All(
                    Coerce(float),
                    vol.Range(
                        min=STATE_VERIFICATION_RETRIES["min"],
                        max=STATE_VERIFICATION_RETRIES["max"],
                    ),
                ),
                vol.Optional(
                    CONF_STATE_VERIFICATION_INTERVAL,
                    default=current_options.get(
                        CONF_STATE_VERIFICATION_INTERVAL,
                        STATE_VERIFICATION_INTERVAL["default"],
                    ),
                ): vol.All(
                    Coerce(float),
                    vol.Range(
                        min=STATE_VERIFICATION_INTERVAL["min"],
                        max=STATE_VERIFICATION_INTERVAL["max"],
                    ),
                ),
                vol.Optional(
                    CONF_POWER_CHANGE_THRESHOLD,
                    default=current_options.get(
                        CONF_POWER_CHANGE_THRESHOLD,
                        POWER_CHANGE_THRESHOLD["default"],
                    ),
                ): vol.All(
                    Coerce(float),
                    vol.Range(
                        min=POWER_CHANGE_THRESHOLD["min"],
                        max=POWER_CHANGE_THRESHOLD["max"],
                    ),
                ),
                vol.Optional(
                    CONF_EVENT_COOLDOWN,
                    default=current_options.get(
                        CONF_EVENT_COOLDOWN,
                        EVENT_COOLDOWN["default"],
                    ),
                ): vol.All(
                    Coerce(float),
                    vol.Range(
                        min=EVENT_COOLDOWN["min"],
                        max=EVENT_COOLDOWN["max"],
                    ),
                ),
            }
        )

        return schema

    @staticmethod
    def build_selector_schema(
        has_outlet_switch: bool = False,
        current_options: Dict[str, Any] | None = None,
    ) -> vol.Schema:
        """Generate a voluptuous schema with NumberSelector slider controls.

        Based on MiPower integration pattern using NumberSelector with NumberSelectorMode.SLIDER.

        Args:
            has_outlet_switch (bool): Whether the device has outlet switch capabilities.
            current_options (Dict[str, Any] | None): Current config entries to use as defaults.

        Returns:
            vol.Schema: A voluptuous schema with NumberSelector elements for slider inputs.
        """

        current_options = current_options or {}

        # Define the schema structure
        schema_dict = {}

        if has_outlet_switch:
            schema_dict.update(
                {
                    vol.Required(
                        CONF_PRE_TURN_ON,
                        default=current_options.get(CONF_PRE_TURN_ON, PRE_TURN_ON),
                    ): BooleanSelector(),
                    vol.Required(
                        CONF_PRE_TURN_ON_DELAY,
                        default=current_options.get(
                            CONF_PRE_TURN_ON_DELAY,
                            PRE_TURN_ON_DELAY["default"],
                        ),
                    ): NumberSelector(
                        NumberSelectorConfig(
                            min=PRE_TURN_ON_DELAY["min"],
                            max=PRE_TURN_ON_DELAY["max"],
                            step=(
                                PRE_TURN_ON_DELAY["step"]
                                if "step" in PRE_TURN_ON_DELAY
                                else 0.1
                            ),
                            unit_of_measurement="s",
                            mode=NumberSelectorMode.SLIDER,
                        )
                    ),
                }
            )

        # Number fields with slider mode
        number_fields = {
            CONF_ON_THRESHOLD: ON_THRESHOLD,
            CONF_OFF_THRESHOLD: OFF_THRESHOLD,
            CONF_RETRY_INTERVAL: RETRY_INTERVAL,
            CONF_RETRY_COUNT: RETRY_COUNT,
            CONF_VERIFY_DELAY: VERIFY_DELAY,
            CONF_COMMAND_TIMEOUT: COMMAND_TIMEOUT,
            CONF_ON_DEBOUNCE_TIME: ON_DEBOUNCE_TIME,
            CONF_OFF_DEBOUNCE_TIME: OFF_DEBOUNCE_TIME,
            CONF_POST_COMMAND_DELAY: POST_COMMAND_DELAY,
            CONF_STATE_VERIFICATION_RETRIES: STATE_VERIFICATION_RETRIES,
            CONF_STATE_VERIFICATION_INTERVAL: STATE_VERIFICATION_INTERVAL,
            CONF_POWER_CHANGE_THRESHOLD: POWER_CHANGE_THRESHOLD,
            CONF_EVENT_COOLDOWN: EVENT_COOLDOWN,
        }

        for conf_key, params in number_fields.items():
            step = params.get(
                "step",
                (
                    0.1
                    if isinstance(params["min"], float)
                    or isinstance(params["max"], float)
                    else 1
                ),
            )
            schema_dict[
                vol.Required(
                    conf_key,
                    default=current_options.get(conf_key, params["default"]),
                )
            ] = NumberSelector(
                NumberSelectorConfig(
                    min=params["min"],
                    max=params["max"],
                    step=step,
                    unit_of_measurement=params.get("unit", ""),
                    mode=NumberSelectorMode.SLIDER,
                )
            )

        return vol.Schema(schema_dict)

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
        # This is a simplified implementation - in a real scenario,
        # this would build a schema based on the provided devices
        return self._build_fallback_schema()

    def build_scripts_schema(self, device_scripts: List[dict]) -> vol.Schema:
        """Build the scripts selection schema.

        Args:
            device_scripts: List of available script dictionaries.

        Returns:
            vol.Schema: Scripts selection schema with dropdown selectors.
        """
        # This is a simplified implementation - in a real scenario,
        # this would build a schema based on the provided scripts
        return self._build_fallback_schema()

    def _build_fallback_schema(self) -> vol.Schema:
        """Build a fallback schema for error recovery.

        Returns:
            vol.Schema: Basic string input schema for fallback.
        """
        return vol.Schema(
            {
                vol.Required("name", default=""): str,
            }
        )
