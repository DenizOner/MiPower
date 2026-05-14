"""State management implementation for Smartify integration.

This module provides a concrete implementation of state management for Smartify devices,
following SOLID principles with state persistence, transition tracking, observer patterns,
and automatic cleanup. It implements the StateProvider interface with thread-safe operations
and comprehensive state validation and monitoring capabilities.

SOLID Principles Applied:
- Single Responsibility: State management and persistence only
- Open-Closed: Extensible through observer pattern and configuration
- Liskov Substitution: Compatible with any StateProvider interface implementation
- Interface Segregation: Focused state management interface
- Dependency Inversion: Depends on StateProvider abstraction, not concretions
"""

import asyncio
import logging
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Deque, Dict, List, Optional

from homeassistant.core import HomeAssistant  # type: ignore[import]

from ....smartify.helpers.errors.exceptions import ValidationError
from .provider import StateProvider

_LOGGER = logging.getLogger(__name__)


@dataclass
class StateData:
    """Represents the current state of a Smartify device.

    Attributes:
        is_on (bool): Whether the device is currently on.
        last_power (float): Last measured power consumption in watts.
        last_command (Optional[str]): Last executed command, if any.
        timestamp (datetime): Timestamp of the state measurement.
        confidence (float): Confidence level of the state (0.0 to 1.0).
    """

    is_on: bool = False
    last_power: float = 0.0
    last_command: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    confidence: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert state data to dictionary format.

        Returns:
            Dict[str, Any]: Dictionary representation with rounded values and ISO timestamp.
        """
        try:
            return {
                "is_on": self.is_on,
                "last_power": round(self.last_power, 2),
                "last_command": self.last_command,
                "timestamp": self.timestamp.isoformat(),
                "confidence": self.confidence,
            }
        except Exception as e:
            _LOGGER.error(
                "Error converting StateData to dict: %s",
                e,
                exc_info=True,
            )
            return {
                "is_on": False,
                "last_power": 0.0,
                "last_command": None,
                "timestamp": datetime.now().isoformat(),
                "confidence": 0.0,
            }


@dataclass
class StateTransition:
    """Represents a transition between device states.

    Attributes:
        from_state (bool): The state before the transition.
        to_state (bool): The state after the transition.
        timestamp (datetime): When the transition occurred.
        reason (str): Reason for the state change.
        power_value (float): Power measurement at the time of transition.
    """

    from_state: bool
    to_state: bool
    timestamp: datetime = field(default_factory=datetime.now)
    reason: str = ""
    power_value: float = 0.0

    def __str__(self) -> str:
        """Convert transition to readable string format.

        Returns:
            str: Formatted string showing timestamp, state change, and reason.
        """
        try:
            return f"{self.timestamp}: {self.from_state} -> {self.to_state} ({self.reason})"
        except Exception as e:
            _LOGGER.error(
                "Error converting StateTransition to string: %s",
                e,
                exc_info=True,
            )
            return f"Error: {e}"


class StateValidator:
    """Static validation utilities for state data.

    Provides static methods for validating power values, confidence levels,
    and state consistency to ensure data integrity in state management.
    """

    @staticmethod
    def validate_power_value(power_value: float) -> bool:
        """Validate that a power value is within acceptable range.

        Args:
            power_value (float): Power consumption value in watts.

        Returns:
            bool: True if power value is between 0 and 100,000 watts.
        """
        try:
            return 0.0 <= power_value <= 100000.0
        except Exception as e:
            _LOGGER.error(
                "Error validating power value: %s",
                e,
                exc_info=True,
            )
            return False

    @staticmethod
    def validate_confidence(confidence: float) -> bool:
        """Validate that a confidence value is within acceptable range.

        Args:
            confidence (float): Confidence level (0.0 to 1.0).

        Returns:
            bool: True if confidence is between 0.0 and 1.0.
        """
        try:
            return 0.0 <= confidence <= 1.0
        except Exception as e:
            _LOGGER.error(
                "Error validating confidence: %s",
                e,
                exc_info=True,
            )
            return False

    @staticmethod
    def validate_state_consistency(
        current_state: StateData,
        new_state: StateData,
        max_power_jump: float = 1000.0,
    ) -> bool:
        """Validate consistency between current and new state data.

        Checks for reasonable power jumps and valid confidence levels
        to prevent invalid state transitions.

        Args:
            current_state (StateData): Current device state.
            new_state (StateData): Proposed new device state.
            max_power_jump (float): Maximum allowed power difference in watts.

        Returns:
            bool: True if state transition is consistent and valid.
        """
        try:
            if abs(new_state.last_power - current_state.last_power) > max_power_jump:
                return False
            if not StateValidator.validate_confidence(new_state.confidence):
                return False
            return True
        except Exception as e:
            _LOGGER.error(
                "Error validating state consistency: %s",
                e,
                exc_info=True,
            )
            return False


class StateManager(StateProvider):
    """Concrete implementation of StateProvider with full state management.

    Provides comprehensive state management including persistence, transition tracking,
    observer patterns, validation, and automatic cleanup. Thread-safe operations
    ensure reliable state handling in concurrent environments.

    Attributes:
        _hass (HomeAssistant): Home Assistant instance for async operations.
        _max_history (int): Maximum number of transitions to keep in history.
        _max_power_jump (float): Maximum allowed power difference for validation.
        _auto_cleanup_interval (int): Interval in seconds for automatic cleanup.
        _enable_observer_gc (bool): Whether to enable garbage collection for observers.
        _lock (asyncio.Lock): Thread synchronization lock.
        _current_state (Optional[StateData]): Current device state data.
        _state_history (Deque[StateTransition]): History of state transitions.
        _observers (List[Callable]): List of registered observer callbacks.
        _cleanup_timer (Optional[asyncio.TimerHandle]): Automatic cleanup timer.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        max_history: int = 50,
        max_power_jump: float = 1000.0,
        auto_cleanup_interval: int = 300,
        enable_observer_gc: bool = True,
    ):
        """Initialize the StateManager with configuration parameters.

        Args:
            hass (HomeAssistant): Home Assistant instance for async operations.
            max_history (int): Maximum number of transitions to keep in history.
            max_power_jump (float): Maximum allowed power difference for validation.
            auto_cleanup_interval (int): Interval in seconds for automatic cleanup.
            enable_observer_gc (bool): Whether to enable garbage collection for observers.

        Raises:
            ValueError: If configuration parameters are invalid.
        """
        # Enhanced configuration validation
        if not isinstance(max_history, int) or max_history < 1 or max_history > 1000:
            raise ValidationError(
                f"max_history must be an integer between 1 and 1000, got {max_history}"
            )
        if (
            not isinstance(max_power_jump, (int, float))
            or max_power_jump <= 0
            or max_power_jump > 10000
        ):
            raise ValidationError(
                f"max_power_jump must be a number between 0 and 10000, got {max_power_jump}"
            )
        if (
            not isinstance(auto_cleanup_interval, (int, float))
            or auto_cleanup_interval < 30
            or auto_cleanup_interval > 3600
        ):
            raise ValidationError(
                f"auto_cleanup_interval must be between 30 and 3600 seconds, got {auto_cleanup_interval}"
            )

        self._hass = hass
        self._max_history = max_history
        self._max_power_jump = max_power_jump
        self._auto_cleanup_interval = auto_cleanup_interval
        self._enable_observer_gc = enable_observer_gc
        self._lock = asyncio.Lock()
        self._current_state: Optional[StateData] = None
        self._state_history: Deque[StateTransition] = deque(maxlen=max_history)
        if enable_observer_gc:
            try:
                import weakref

                self._observers: List[Callable[[StateData, StateData], None]] = []
                self._observer_refs: List[weakref.ReferenceType] = []
            except ImportError:
                self._observers: List[Callable[[StateData, StateData], None]] = []
                self._observer_refs = []
        else:
            self._observers: List[Callable[[StateData, StateData], None]] = []
        self._cleanup_timer: Optional[asyncio.TimerHandle] = None
        self._start_auto_cleanup()
        self._update_count = 0
        self._last_cleanup = datetime.now()

        # Performance monitoring metrics
        self._performance_metrics = {
            "total_updates": 0,
            "successful_updates": 0,
            "failed_updates": 0,
            "average_update_time": 0.0,
            "total_transitions": 0,
            "observer_notifications": 0,
            "memory_usage_estimate": 0,
            "start_time": datetime.now(),
        }
        self._update_times: Deque[float] = deque(
            maxlen=100
        )  # Keep last 100 update times
        _LOGGER.debug(
            "StateManager initialized: max_history=%d, max_power_jump=%.1fW, gc=%s",
            max_history,
            max_power_jump,
            enable_observer_gc,
        )

    @property
    def current_state(self) -> Optional[StateData]:
        """Get the current state data object.

        Returns:
            Optional[StateData]: The current state data, or None if not initialized.
        """
        return self._current_state

    def has_state(self) -> bool:
        """Check if state has been initialized.

        Returns:
            bool: True if state has been initialized, False otherwise.
        """
        result = self._current_state is not None
        _LOGGER.debug("has_state called: result=%s", result)
        return result

    def add_observer(self, callback: Callable[[StateData, StateData], None]) -> None:
        """Add a state change observer callback.

        Args:
            callback: Function to call when state changes, receives (old_state, new_state).
        """
        self._observers.append(callback)
        _LOGGER.debug("Added state observer, total: %d", len(self._observers))

    def remove_observer(self, callback: Callable[[StateData, StateData], None]) -> None:
        """Remove a state change observer callback.

        Args:
            callback: The observer callback function to remove.
        """
        if callback in self._observers:
            self._observers.remove(callback)
            _LOGGER.debug("Removed state observer, total: %d", len(self._observers))

    async def initialize_state(
        self,
        is_on: bool = False,
        last_power: float = 0.0,
        last_command: Optional[str] = None,
    ) -> None:
        """Initialize the state manager with initial values.

        Args:
            is_on (bool): Initial power state of the device.
            last_power (float): Last measured power consumption in watts.
            last_command (Optional[str]): Last executed command, if any.
        """
        async with self._lock:
            initial_state = StateData(
                is_on=is_on, last_power=last_power, last_command=last_command
            )
            if self._current_state is not None:
                _LOGGER.warning("Overwriting existing state during initialization")
            self._current_state = initial_state
            _LOGGER.info(
                "State initialized: is_on=%s, last_power=%.2fW",
                is_on,
                last_power,
            )

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
            is_on (Optional[bool]): New power state, if changed.
            last_power (Optional[float]): New power measurement in watts.
            last_command (Optional[str]): New command that was executed.
            confidence (float): Confidence level of the update (0.0 to 1.0).
            reason (str): Reason for the state update.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        _LOGGER.debug(
            "update_state called: is_on=%s, last_power=%s, last_command=%s, confidence=%s, reason=%s",
            is_on,
            last_power,
            last_command,
            confidence,
            reason,
        )
        import time

        start_time = time.time()

        async with self._lock:
            self._performance_metrics["total_updates"] += 1

            if self._current_state is None:
                _LOGGER.error(
                    "Cannot update state: not initialized",
                    exc_info=True,
                )
                self._performance_metrics["failed_updates"] += 1
                return False

            new_state = StateData(
                is_on=(is_on if is_on is not None else self._current_state.is_on),
                last_power=(
                    last_power
                    if last_power is not None
                    else self._current_state.last_power
                ),
                last_command=(
                    last_command
                    if last_command is not None
                    else self._current_state.last_command
                ),
                confidence=confidence,
            )

            if not self._validate_state_update(self._current_state, new_state):
                _LOGGER.warning("State update validation failed: %s", reason)
                self._performance_metrics["failed_updates"] += 1
                return False

            old_state = self._current_state
            self._current_state = new_state

            if old_state.is_on != new_state.is_on:
                transition = StateTransition(
                    from_state=old_state.is_on,
                    to_state=new_state.is_on,
                    reason=reason,
                    power_value=new_state.last_power,
                )
                self._state_history.append(transition)
                self._performance_metrics["total_transitions"] += 1
                _LOGGER.info(
                    "State transition: %s -> %s (%.2fW) - %s",
                    old_state.is_on,
                    new_state.is_on,
                    new_state.last_power,
                    reason,
                )

            await self._notify_observers(old_state, new_state)
            self._performance_metrics["successful_updates"] += 1

            # Update performance metrics
            update_duration = time.time() - start_time
            self._update_times.append(update_duration)
            self._performance_metrics["average_update_time"] = sum(
                self._update_times
            ) / len(self._update_times)

            return True

    def _validate_state_update(
        self, old_state: StateData, new_state: StateData
    ) -> bool:
        """Validate a state update against consistency rules.

        Args:
            old_state (StateData): Current state before update.
            new_state (StateData): Proposed new state.

        Returns:
            bool: True if the update is valid and consistent.
        """
        return StateValidator.validate_state_consistency(
            old_state, new_state, self._max_power_jump
        )

    def _cleanup_dead_observers(self) -> None:
        """Cleanup dead observers using weak references."""
        if self._observer_refs:
            alive_refs = []
            current_observers = []
            for ref in self._observer_refs:
                observer = ref()
                if observer is not None:
                    alive_refs.append(ref)
                    current_observers.append(observer)
            self._observer_refs = alive_refs
            self._observers = current_observers

    async def _notify_observers(
        self, old_state: StateData, new_state: StateData
    ) -> None:
        """Notify all registered observers of state changes.

        Args:
            old_state (StateData): State before the change.
            new_state (StateData): State after the change.
        """
        if (
            old_state.is_on == new_state.is_on
            and old_state.last_power == new_state.last_power
        ):
            return
        if self._enable_observer_gc and hasattr(self, "_observer_refs"):
            self._cleanup_dead_observers()
        for observer in self._observers[:]:
            try:
                self._hass.async_create_task(
                    self._safe_notify_observer(observer, old_state, new_state)
                )
                self._performance_metrics["observer_notifications"] += 1
            except Exception as e:
                _LOGGER.error(
                    "Error scheduling observer notification: %s",
                    e,
                    exc_info=True,
                )

    async def _safe_notify_observer(
        self,
        observer: Callable[[StateData, StateData], None],
        old_state: StateData,
        new_state: StateData,
    ) -> None:
        """Safely notify a single observer with error handling.

        Args:
            observer: The observer callback function.
            old_state (StateData): State before the change.
            new_state (StateData): State after the change.
        """
        try:
            observer(old_state, new_state)
        except Exception as e:
            _LOGGER.error(
                "Error in state observer: %s",
                e,
                exc_info=True,
            )

    def get_history(self, limit: Optional[int] = None) -> List[StateTransition]:
        """Get the state transition history.

        Args:
            limit (Optional[int]): Maximum number of transitions to return.

        Returns:
            List[StateTransition]: List of state transitions, most recent first.
        """
        try:
            history = list(self._state_history)
            if limit:
                return history[-limit:]
            return history
        except Exception as e:
            _LOGGER.error(
                "Error getting state history: %s",
                e,
                exc_info=True,
            )
            return []

    def get_state_summary(self) -> Dict[str, Any]:
        """Get a comprehensive summary of the current state and history.

        Returns:
            Dict[str, Any]: Summary including current state, history count,
                last transition, and uptime ratio.
        """
        try:
            if not self._current_state:
                return {"error": "No state initialized"}
            return {
                "current_state": self._current_state.to_dict(),
                "history_count": len(self._state_history),
                "last_transition": (
                    str(self._state_history[-1]) if self._state_history else None
                ),
                "uptime_ratio": self._calculate_uptime_ratio(),
            }
        except Exception as e:
            _LOGGER.error(
                "Error getting state summary: %s",
                e,
                exc_info=True,
            )
            return {"error": "Failed to get state summary"}

    def _calculate_uptime_ratio(self) -> float:
        """Calculate the ratio of time the device has been ON.

        Returns:
            float: Ratio between 0.0 and 1.0 representing uptime percentage.
        """
        try:
            if not self._state_history:
                return 0.0 if self._current_state else 0.5
            on_time = 0
            total_time = 0
            current_time = datetime.now()
            if self._current_state:
                state_start = self._current_state.timestamp
                total_time += (current_time - state_start).total_seconds()
                if self._current_state.is_on:
                    on_time += (current_time - state_start).total_seconds()
            for i in range(len(self._state_history) - 1):
                current_transition = self._state_history[i]
                next_transition = self._state_history[i + 1]
                duration = (
                    next_transition.timestamp - current_transition.timestamp
                ).total_seconds()
                total_time += duration
                if current_transition.to_state:
                    on_time += duration
            return on_time / total_time if total_time > 0 else 0.0
        except Exception as e:
            _LOGGER.error(
                "Error calculating uptime ratio: %s",
                e,
                exc_info=True,
            )
            return 0.0

    def _start_auto_cleanup(self) -> None:
        """Start the automatic cleanup timer.

        Returns:
            None
        """
        try:
            if self._cleanup_timer:
                self._cleanup_timer.cancel()
            self._cleanup_timer = self._hass.loop.call_later(
                self._auto_cleanup_interval, self._auto_cleanup
            )
        except Exception as e:
            _LOGGER.error(
                "Error starting auto cleanup: %s",
                e,
                exc_info=True,
            )

    def _auto_cleanup(self) -> None:
        """Perform automatic cleanup of resources.

        Returns:
            None
        """
        try:
            # Only log every 10th cleanup to reduce log spam if debug is enabled
            self._update_count += 1
            if self._update_count % 10 == 0:
                _LOGGER.debug("Auto cleanup performed")
            self._start_auto_cleanup()
        except Exception as e:
            _LOGGER.error(
                "Error in auto cleanup: %s",
                e,
                exc_info=True,
            )

    def get_current_state(self) -> Dict[str, Any]:
        """Get current state for StateProvider interface compatibility.

        Returns:
            Dict[str, Any]: Current state information or default values if uninitialized.
        """
        if self._current_state:
            return self._current_state.to_dict()
        return {"is_on": False, "last_power": 0.0, "last_command": None}

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get comprehensive performance metrics for monitoring.

        Returns:
            Dict[str, Any]: Performance metrics including update counts, timing,
                success rates, and resource usage estimates.
        """
        try:
            uptime = (
                datetime.now() - self._performance_metrics["start_time"]
            ).total_seconds()
            self._performance_metrics["memory_usage_estimate"] = (
                self._calculate_memory_usage()
            )

            return {
                "total_updates": self._performance_metrics["total_updates"],
                "successful_updates": self._performance_metrics["successful_updates"],
                "failed_updates": self._performance_metrics["failed_updates"],
                "success_rate": (
                    self._performance_metrics["successful_updates"]
                    / max(self._performance_metrics["total_updates"], 1)
                ),
                "average_update_time": round(
                    self._performance_metrics["average_update_time"], 4
                ),
                "total_transitions": self._performance_metrics["total_transitions"],
                "observer_notifications": self._performance_metrics[
                    "observer_notifications"
                ],
                "memory_usage_estimate_kb": self._performance_metrics[
                    "memory_usage_estimate"
                ],
                "uptime_seconds": round(uptime, 2),
                "updates_per_second": round(
                    self._performance_metrics["total_updates"] / max(uptime, 1),
                    2,
                ),
            }
        except Exception as e:
            _LOGGER.error(
                "Error getting performance metrics: %s",
                e,
                exc_info=True,
            )
            return {"error": "Failed to get performance metrics"}

    def _calculate_memory_usage(self) -> int:
        """Calculate estimated memory usage in kilobytes.

        Returns:
            int: Estimated memory usage in KB.
        """
        try:
            # Rough estimation based on data structures
            base_usage = 1024  # Base class overhead
            state_usage = 512 if self._current_state else 0  # StateData object
            history_usage = len(self._state_history) * 256  # Each StateTransition
            observers_usage = len(self._observers) * 128  # Observer references
            metrics_usage = 2048  # Performance metrics and update times
            total_kb = (
                base_usage
                + state_usage
                + history_usage
                + observers_usage
                + metrics_usage
            ) // 1024
            return max(total_kb, 1)  # At least 1KB
        except Exception as e:
            _LOGGER.error(
                "Error calculating memory usage: %s",
                e,
                exc_info=True,
            )
            return 0

    async def cleanup(self) -> None:
        """Clean up all resources and reset state manager.

        Cancels timers, clears observers, history, and current state.
        Should be called when the manager is no longer needed.
        """
        try:
            if self._cleanup_timer:
                self._cleanup_timer.cancel()
                self._cleanup_timer = None
            async with self._lock:
                self._observers.clear()
                self._state_history.clear()
                self._current_state = None
            _LOGGER.info("StateManager cleanup completed")
        except Exception as e:
            _LOGGER.error(
                "Error during StateManager cleanup: %s",
                e,
                exc_info=True,
            )
