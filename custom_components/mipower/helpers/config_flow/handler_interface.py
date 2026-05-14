"""Config flow handler interface for Smartify."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from homeassistant.config_entries import ConfigFlowResult  # type: ignore[import]
from homeassistant.data_entry_flow import FlowResult  # type: ignore[import]


class ConfigFlowHandlerInterface(ABC):
    """Interface for config flow step handlers."""

    @abstractmethod
    async def handle_user_step(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle the initial user step of the configuration flow.

        Args:
            user_input: Optional dictionary containing user-submitted form data.

        Returns:
            The result of the configuration flow step.
        """
        pass

    @abstractmethod
    async def handle_scripts_step(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> ConfigFlowResult:
        """Handle the scripts selection step of the configuration flow.

        Args:
            user_input: Optional dictionary containing script selection data.

        Returns:
            The result of the configuration flow step.
        """
        pass
