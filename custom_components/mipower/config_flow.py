"""
Main config flow for the MiPower integration.

This file acts as the router for the entire configuration process when a user adds
the MiPower integration. It doesn't contain much logic itself but instead directs
the user to the appropriate setup flow (Easy or Advanced) based on their choice.
It is the first Python file that is hit when a user clicks "Add Integration" and
selects MiPower.
"""

from __future__ import annotations

import logging
from typing import Any

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

# Import constants and flow handlers from other files within the integration.
from .const import DOMAIN
from .flows.advanced import AdvancedFlowManager
from .flows.easy import async_handle_easy_setup, async_show_easy_setup_form
from .flows.options import MiPowerOptionsFlowHandler

# Set up a specific logger for this file.
_LOGGER = logging.getLogger(__name__)


class MiPowerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """
    Main configuration flow router for MiPower.

    This class orchestrates the setup process by presenting the user with
    initial choices and then delegating the subsequent steps to other handlers
    (e.g., AdvancedFlowManager or the easy setup functions).
    """

    # The version of the config flow. This is used by Home Assistant to handle
    # migrations if the configuration flow changes in future versions.
    VERSION = 1

    def __init__(self) -> None:
        """Initialize the main config flow."""
        _LOGGER.debug("Initializing MiPowerConfigFlow.")
        # This property will hold an instance of the AdvancedFlowManager if the
        # user chooses the advanced setup path. It's initialized to None.
        self.advanced_flow_manager: AdvancedFlowManager | None = None

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> "MiPowerOptionsFlowHandler":
        """
        Get the options flow for this handler.

        This method is called by Home Assistant when a user clicks "Configure"
        on an already-setup MiPower integration. It returns an instance of our
        options flow handler, which is defined in `flows/options.py`.
        """
        _LOGGER.debug(
            "Request to get options flow for entry_id: %s", config_entry.entry_id
        )
        # The handler is initialized without arguments. Home Assistant will attach the
        # config_entry to the handler instance automatically before calling async_step_init.
        return MiPowerOptionsFlowHandler()

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """
        Show the initial choice: Easy or Advanced setup.

        This is the very first step the user sees. It presents a simple menu.
        The options in the menu ('easy_setup', 'advanced_setup') correspond to
        the next step IDs that will be called.
        """
        _LOGGER.debug("Executing step: user")
        # We use `async_show_menu` to display a list of choices to the user.
        # The `step_id` is 'user', which is the default first step.
        return self.async_show_menu(
            step_id="user",
            menu_options=["easy_setup", "advanced_setup"],
        )

    async def async_step_easy_setup(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """
        Handle the "Easy Setup" path.

        This step is triggered when the user selects "Easy Setup" from the user menu.
        It delegates the logic to functions defined in `flows/easy.py`.
        """
        _LOGGER.debug("Executing step: easy_setup")
        # If user_input is None, it means we need to show the form to the user.
        if user_input is None:
            _LOGGER.debug("Showing easy setup form.")
            return await async_show_easy_setup_form(self)

        # If user_input is not None, the user has submitted the form.
        _LOGGER.debug("Handling easy setup form submission.")
        return await async_handle_easy_setup(self, user_input)

    # The following methods handle the multi-step "Advanced Setup" flow.
    # This router class defines the step IDs (`advanced_setup`, `mac_address`, `settings`),
    # but the logic for each step is managed and delegated to the AdvancedFlowManager.

    async def async_step_advanced_setup(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """
        Handle the first step of the advanced flow (device selection).
        """
        _LOGGER.debug("Executing step: advanced_setup")
        # Initialize the manager for the advanced flow if it doesn't exist yet.
        if not self.advanced_flow_manager:
            _LOGGER.debug("Initializing AdvancedFlowManager.")
            self.advanced_flow_manager = AdvancedFlowManager(self.hass, self)

        # Delegate the handling of this step to the manager.
        return await self.advanced_flow_manager.async_handle_step(
            "advanced_setup", user_input
        )

    async def async_step_mac_address(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """
        Handle the second step of the advanced flow (MAC address input).
        """
        _LOGGER.debug("Executing step: mac_address")
        # This step should only be reached if the manager is already initialized.
        if not self.advanced_flow_manager:
            _LOGGER.error("Advanced flow manager not initialized for mac_address step.")
            return self.async_abort(reason="unknown_error")

        # Delegate the handling of this step to the manager.
        return await self.advanced_flow_manager.async_handle_step(
            "mac_address", user_input
        )

    async def async_step_settings(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """
        Handle the final step of the advanced flow (timing settings).
        """
        _LOGGER.debug("Executing step: settings")
        # This step should only be reached if the manager is already initialized.
        if not self.advanced_flow_manager:
            _LOGGER.error("Advanced flow manager not initialized for settings step.")
            return self.async_abort(reason="unknown_error")

        # Delegate the handling of this step to the manager.
        return await self.advanced_flow_manager.async_handle_step("settings", user_input)
