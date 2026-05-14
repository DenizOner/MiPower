"""State transition management for Smartify integration.

This module provides classes and utilities for managing device state transitions
based on power consumption analysis. It implements direct threshold-based logic,
stability checking, oscillation prevention, and confidence-based decision making
for reliable ON/OFF state detection in smart devices.
"""

import logging
import statistics
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Deque, Dict, Optional, Tuple

from ...helpers.errors.exceptions import ValidationError

_LOGGER = logging.getLogger(__name__)


@dataclass
class TransitionConfig:
    """Configuration for state transition analysis.

    Defines thresholds and parameters for determining when a device should
    transition between ON and OFF states based on power consumption.
    Uses direct OFF threshold for state transitions.
    """

    on_threshold: float = 10.0
    off_threshold: float = 1.5
    min_stable_samples: int = 3
    max_oscillation_period: int = 30
    confidence_threshold: float = 0.7

    def __post_init__(self):
        """Post-initialization to validate config."""
        # Enhanced validation
        if not isinstance(self.on_threshold, (int, float)) or self.on_threshold <= 0:
            raise ValidationError(
                f"on_threshold must be a positive number, got {self.on_threshold}"
            )
        if not isinstance(self.off_threshold, (int, float)) or self.off_threshold < 0:
            raise ValidationError(
                f"off_threshold must be a non-negative number, got {self.off_threshold}"
            )
        if self.off_threshold >= self.on_threshold:
            raise ValidationError(
                f"off_threshold ({self.off_threshold}) must be less than on_threshold ({self.on_threshold})"
            )
        if not isinstance(self.min_stable_samples, int) or self.min_stable_samples < 1:
            raise ValidationError(
                f"min_stable_samples must be an integer >= 1, got {self.min_stable_samples}"
            )
        if (
            not isinstance(self.max_oscillation_period, (int, float))
            or self.max_oscillation_period <= 0
        ):
            raise ValidationError(
                f"max_oscillation_period must be positive, got {self.max_oscillation_period}"
            )
        if (
            not isinstance(self.confidence_threshold, (int, float))
            or not 0.0 <= self.confidence_threshold <= 1.0
        ):
            raise ValidationError(
                f"confidence_threshold must be between 0.0 and 1.0, got {self.confidence_threshold}"
            )

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary format.

        Returns:
            Dict[str, Any]: Dictionary representation of all configuration parameters.
        """
        return {
            "on_threshold": self.on_threshold,
            "off_threshold": self.off_threshold,
            "min_stable_samples": self.min_stable_samples,
            "max_oscillation_period": self.max_oscillation_period,
            "confidence_threshold": self.confidence_threshold,
        }


@dataclass
class TransitionSample:
    """Represents a single power consumption sample for transition analysis.

    Contains power measurement data with timestamp and confidence level
    for use in state transition decision making.
    """

    power_value: float
    timestamp: datetime = field(default_factory=datetime.now)
    confidence: float = 1.0

    def is_valid(self) -> bool:
        """Check if the sample contains valid values.

        Returns:
            bool: True if power value and confidence are within valid ranges.
        """
        return 0.0 <= self.power_value <= 100000.0 and 0.0 <= self.confidence <= 1.0


class TransitionStatistics:
    """Manages statistical analysis of power consumption samples.

    Maintains rolling windows of power and confidence values to calculate
    stability metrics and determine if readings are stable enough for
    transition decisions.
    """

    def __init__(self, window_size: int = 10):
        """Initialize statistics tracker with specified window size.

        Args:
            window_size (int): Maximum number of samples to keep in rolling window.
        """
        self.window_size = window_size
        self.power_samples: Deque[float] = deque(maxlen=window_size)
        self.confidence_samples: Deque[float] = deque(maxlen=window_size)

    def add_sample(self, power_value: float, confidence: float = 1.0) -> None:
        """Add a new power sample to the statistics window.

        Args:
            power_value (float): Power consumption value in watts.
            confidence (float): Confidence level of the measurement (0.0 to 1.0).
        """
        self.power_samples.append(power_value)
        self.confidence_samples.append(confidence)

    def get_stability_metrics(self) -> Dict[str, float]:
        """Calculate stability metrics from current sample window.

        Computes stability as inverse of coefficient of variation, along with
        other statistical measures of the power consumption data.

        Returns:
            Dict[str, float]: Dictionary containing stability, confidence,
                sample count, mean power, and standard deviation.
        """
        if len(self.power_samples) < 2:
            return {"stability": 0.0, "confidence": 0.0}
        try:
            power_stdev = statistics.stdev(self.power_samples)
            power_mean = statistics.mean(self.power_samples)
            stability = max(0.0, 1.0 - (power_stdev / max(power_mean, 1.0)))
            avg_confidence = statistics.mean(self.confidence_samples)
            return {
                "stability": round(stability, 3),
                "confidence": round(avg_confidence, 3),
                "sample_count": len(self.power_samples),
                "power_mean": round(power_mean, 2),
                "power_stdev": round(power_stdev, 2),
            }
        except statistics.StatisticsError:
            return {"stability": 0.0, "confidence": 0.0}

    def is_stable(self, min_stability: float = 0.7) -> bool:
        """Check if current samples indicate stable power consumption.

        Args:
            min_stability (float): Minimum stability threshold (0.0 to 1.0).

        Returns:
            bool: True if stability meets or exceeds the minimum threshold.
        """
        metrics = self.get_stability_metrics()
        return metrics["stability"] >= min_stability


class StateTransitionManager:
    """Manages device state transitions based on power consumption analysis.

    This class implements direct threshold-based state transition logic with stability
    checking, oscillation prevention, and confidence-based decision making.
    It analyzes power consumption samples to determine when devices should
    transition between ON and OFF states.
    """

    def __init__(self, config: TransitionConfig):
        """Initialize the state transition manager.

        Args:
            config (TransitionConfig): Configuration parameters for transition analysis.
        """
        self.config = config
        self.current_state: bool = False
        self.last_transition: Optional[datetime] = None
        self.statistics = TransitionStatistics()
        self.sample_buffer: Deque[TransitionSample] = deque(maxlen=20)
        self.transition_history: Deque[Tuple[bool, datetime]] = deque(maxlen=10)
        _LOGGER.debug(
            "StateTransitionManager initialized: on_threshold=%.2fW, off_threshold=%.2fW",
            config.on_threshold,
            config.off_threshold,
        )

    def analyze_sample(
        self, power_value: float, confidence: float = 1.0
    ) -> Dict[str, Any]:
        """Analyze a power consumption sample and determine state transition.

        Processes a new power measurement, validates it, and determines if a
        state transition should occur based on configured thresholds, stability,
        and oscillation prevention.

        Args:
            power_value (float): Current power consumption in watts.
            confidence (float): Confidence level of the measurement (0.0 to 1.0).

        Returns:
            Dict[str, Any]: Analysis result containing:
                - should_transition (bool): Whether to change state
                - new_state (bool): The determined new state
                - confidence (float): Confidence in the decision
                - reason (str): Explanation of the decision
        """
        sample = TransitionSample(power_value, confidence=confidence)
        if not sample.is_valid():
            return {
                "should_transition": False,
                "new_state": self.current_state,
                "confidence": 0.0,
                "reason": "Invalid sample values",
            }
        self.sample_buffer.append(sample)
        self.statistics.add_sample(power_value, confidence)
        stability_metrics = self.statistics.get_stability_metrics()
        if self._is_oscillating():
            return {
                "should_transition": False,
                "new_state": self.current_state,
                "confidence": 0.0,
                "reason": "Oscillation prevention active",
            }
        transition_result = self._analyze_transition(stability_metrics)
        _LOGGER.debug(
            "Sample analysis: %.2fW (state=%s, stability=%.2f) -> %s",
            power_value,
            self.current_state,
            stability_metrics["stability"],
            transition_result["reason"],
        )
        return transition_result

    def _analyze_transition(
        self, stability_metrics: Dict[str, float]
    ) -> Dict[str, Any]:
        """Analyze recent samples to determine if a state transition should occur.

        Uses direct threshold logic with stability and confidence checks to decide
        whether to transition from current state based on power thresholds.

        Args:
            stability_metrics (Dict[str, float]): Current stability metrics from statistics.

        Returns:
            Dict[str, Any]: Transition analysis result with decision details.
        """
        if len(self.sample_buffer) < self.config.min_stable_samples:
            return {
                "should_transition": False,
                "new_state": self.current_state,
                "confidence": 0.0,
                "reason": "Insufficient samples for analysis",
            }
        recent_samples = list(self.sample_buffer)[-self.config.min_stable_samples :]
        avg_power = statistics.mean(sample.power_value for sample in recent_samples)
        avg_confidence = statistics.mean(sample.confidence for sample in recent_samples)
        if not stability_metrics["stability"] >= 0.6:
            return {
                "should_transition": False,
                "new_state": self.current_state,
                "confidence": 0.0,
                "reason": f"Insufficient stability ({stability_metrics['stability']:.2f})",
            }
        if self.current_state is False:
            if avg_power >= self.config.on_threshold:
                return {
                    "should_transition": True,
                    "new_state": True,
                    "confidence": avg_confidence * stability_metrics["stability"],
                    "reason": f"OFF->ON: {avg_power:.1f}W >= {self.config.on_threshold:.1f}W",
                }
        else:
            if avg_power <= self.config.off_threshold:
                return {
                    "should_transition": True,
                    "new_state": False,
                    "confidence": avg_confidence * stability_metrics["stability"],
                    "reason": f"ON->OFF: {avg_power:.1f}W <= {self.config.off_threshold:.1f}W",
                }
        return {
            "should_transition": False,
            "new_state": self.current_state,
            "confidence": avg_confidence,
            "reason": f"No transition: {avg_power:.1f}W (between thresholds)",
        }

    def _is_oscillating(self) -> bool:
        """Check if the system is oscillating between states too frequently.

        Analyzes recent transition history to detect rapid state changes
        that indicate oscillation, which should be prevented.

        Returns:
            bool: True if oscillation is detected and should be prevented.
        """
        if len(self.transition_history) < 4:
            return False
        recent_transitions = list(self.transition_history)[-4:]
        for i in range(len(recent_transitions) - 1):
            current_state, current_time = recent_transitions[i]
            next_state, next_time = recent_transitions[i + 1]
            if (
                current_state != next_state
                and (next_time - current_time).total_seconds()
                < self.config.max_oscillation_period
            ):
                return True
        return False

    def force_transition(
        self, new_state: bool, reason: str = "Manual override"
    ) -> None:
        """Force an immediate state transition regardless of power analysis.

        Updates the current state and transition history immediately.
        Used for manual overrides or external state changes.

        Args:
            new_state (bool): The new state to force (True for ON, False for OFF).
            reason (str): Reason for the forced transition.
        """
        old_state = self.current_state
        self.current_state = new_state
        self.last_transition = datetime.now()
        self.transition_history.append((new_state, datetime.now()))
        _LOGGER.info("Forced transition: %s -> %s (%s)", old_state, new_state, reason)

    def get_transition_summary(self) -> Dict[str, Any]:
        """Get a comprehensive summary of the current transition state.

        Returns detailed information about current state, configuration,
        statistics, and transition history for monitoring and debugging.

        Returns:
            Dict[str, Any]: Summary containing current state, config, statistics,
                buffer size, transition count, and last transition timestamp.
        """
        return {
            "current_state": self.current_state,
            "config": self.config.to_dict(),
            "statistics": self.statistics.get_stability_metrics(),
            "sample_buffer_size": len(self.sample_buffer),
            "transition_count": len(self.transition_history),
            "last_transition": (
                self.last_transition.isoformat() if self.last_transition else None
            ),
        }

    def reset(self) -> None:
        """Reset the transition manager to its initial state.

        Clears all buffers, statistics, and history, resetting to OFF state.
        Used for reinitialization or error recovery.
        """
        self.current_state = False
        self.last_transition = None
        self.sample_buffer.clear()
        self.transition_history.clear()
        self.statistics = TransitionStatistics()
        _LOGGER.info("StateTransitionManager reset to initial state")

    def update_config(self, config: TransitionConfig) -> None:
        """Update the transition configuration parameters.

        Changes the thresholds and parameters used for transition analysis.
        Maintains existing state and history.

        Args:
            config (TransitionConfig): New configuration parameters to apply.
        """
        old_threshold = self.config.on_threshold
        self.config = config
        _LOGGER.info(
            "Transition config updated: threshold %.2fW -> %.2fW, off_threshold %.2fW",
            old_threshold,
            config.on_threshold,
            config.off_threshold,
        )


# Alias for backward compatibility
Transitions = StateTransitionManager
