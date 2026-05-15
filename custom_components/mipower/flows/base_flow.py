"""Base configuration flow for MiPower integration using SOLID principles."""

from abc import ABC, abstractmethod
from typing import Any, Dict

from homeassistant import config_entries  # type: ignore[import]
from homeassistant.data_entry_flow import FlowResult  # type: ignore[import]


class BaseConfigFlow(config_entries.ConfigFlow, ABC):
    """Base configuration flow with common functionality."""

    def __init__(self) -> None:
        """Initialize the base config flow."""
        super().__init__()
        self.flow_data: Dict[str, Any] = {}

    @abstractmethod
    async def async_step_user(
        self, user_input: Dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial user step."""
        pass

    def store_user_input(self, user_input: Dict[str, Any]) -> None:
        """Store user input in flow data."""
        if user_input:
            self.flow_data.update(user_input)

    def get_stored_data(self, key: str, default: Any = None) -> Any:
        """Get stored data by key."""
        return self.flow_data.get(key, default)

    def clear_flow_data(self) -> None:
        """Clear all stored flow data."""
        self.flow_data.clear()
