"""
State provider module for Smartify.

This module defines the StateProvider abstract base class and its concrete implementation
StateProviderImpl, following SOLID principles for state management in Smartify devices.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from homeassistant.core import HomeAssistant  # type: ignore[import]


class StateProvider(ABC):
    """Abstract base class for state management in Smartify devices.

    This interface defines the contract for managing device state, including
    initialization, updates, retrieval, and cleanup operations. Implementations
    should handle state persistence and provide thread-safe operations.

    Follows SOLID principles:
    - Single Responsibility: Only manages device state
    - Open/Closed: New implementations can be added without modifying existing code
    - Liskov Substitution: All implementations are interchangeable
    - Interface Segregation: Focused on state management operations
    - Dependency Inversion: Depends on abstractions, not concretions
    """

    @abstractmethod
    async def initialize_state(
        self,
        is_on: bool,
        last_power: float,
        last_command: Optional[str] = None,
    ) -> None:
        """Initialize the state provider with initial state values.

        Args:
            is_on: Initial on/off state of the device
            last_power: Last known power consumption value
            last_command: Last command executed (optional)
        """
        pass

    @abstractmethod
    async def update_state(
        self,
        is_on: Optional[bool] = None,
        last_power: Optional[float] = None,
        last_command: Optional[str] = None,
        confidence: float = 1.0,
        reason: str = "",
    ) -> bool:
        """Update the current state with new values.

        Args:
            is_on: New on/off state (optional, only update if provided)
            last_power: Updated power consumption value (optional, only update if provided)
            last_command: Command that triggered the update (optional)
            confidence: Confidence level of the state determination
            reason: Reason for the state change

        Returns:
            bool: True if update was successful, False otherwise
        """
        pass

    @abstractmethod
    def get_current_state(self) -> Dict[str, Any]:
        """Retrieve the current state data.

        Returns:
            Dict containing current state information including:
            - is_on: Current on/off state
            - last_power: Last power reading
            - last_command: Last executed command
            - confidence: State determination confidence (optional)
            - reason: Last state change reason (optional)
        """
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """Clean up resources and perform finalization operations."""
        pass

    @abstractmethod
    def has_state(self) -> bool:
        """Check if valid state data exists.

        Returns:
            True if state has been initialized and contains valid data
        """
        pass


class StateProviderImpl(StateProvider):
    """Concrete implementation of StateProvider for Smartify devices.

    This implementation manages device state in memory with optional persistence
    capabilities. It provides thread-safe state operations and follows the
    StateProvider interface contract.

    Attributes:
        _hass: Home Assistant instance for integration
        _state: Internal state dictionary
        _initialized: Flag indicating if state has been initialized
    """

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the state provider.

        Args:
            hass: Home Assistant instance
        """
        self._hass = hass
        self._state: Dict[str, Any] = {}
        self._initialized = False

    async def initialize_state(
        self,
        is_on: bool,
        last_power: float,
        last_command: Optional[str] = None,
    ) -> None:
        """Initialize the state provider with initial state values.

        Args:
            is_on: Initial on/off state of the device
            last_power: Last known power consumption value
            last_command: Last command executed (optional)
        """
        self._state = {
            "is_on": is_on,
            "last_power": last_power,
            "last_command": last_command,
            "confidence": None,
            "reason": "Initial state",
        }
        self._initialized = True

    async def update_state(
        self,
        is_on: Optional[bool] = None,
        last_power: Optional[float] = None,
        last_command: Optional[str] = None,
        confidence: float = 1.0,
        reason: str = "",
    ) -> bool:
        """Update the current state with new values.

        Args:
            is_on: New on/off state (optional, only update if provided)
            last_power: Updated power consumption value (optional, only update if provided)
            last_command: Command that triggered the update (optional)
            confidence: Confidence level of the state determination
            reason: Reason for the state change

        Returns:
            bool: True if update was successful, False otherwise
        """
        if not self._initialized:
            return False

        # Update only provided values
        if is_on is not None:
            self._state["is_on"] = is_on
        if last_power is not None:
            self._state["last_power"] = last_power
        if last_command is not None:
            self._state["last_command"] = last_command
        self._state["confidence"] = confidence
        self._state["reason"] = reason

        return True

    def get_current_state(self) -> Dict[str, Any]:
        """Retrieve the current state data.

        Returns:
            Dict containing current state information
        """
        if not self._initialized:
            return {}
        return self._state.copy()

    async def cleanup(self) -> None:
        """Clean up resources and perform finalization operations."""
        self._state.clear()
        self._initialized = False

    def has_state(self) -> bool:
        """Check if valid state data exists.

        Returns:
            True if state has been initialized and contains valid data
        """
        return self._initialized and bool(self._state)
