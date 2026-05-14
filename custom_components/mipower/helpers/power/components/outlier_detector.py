"""
Outlier Detector Component - Statistical Anomaly Detection

This module implements statistical outlier detection using Z-score analysis
for power consumption data. It maintains sample history and detects anomalous
readings using configurable sensitivity thresholds.

Classes:
    OutlierDetector: Statistical outlier detection with Z-score analysis.
"""

import logging
import statistics
from collections import deque
from typing import Dict

from ....helpers.errors.exceptions import ValidationError
from ..power_analyzer_interface import OutlierDetectorInterface

_LOGGER = logging.getLogger(__name__)


class OutlierDetector(OutlierDetectorInterface):
    """Statistical outlier detection using Z-score analysis.

    Maintains sample history and detects anomalous power readings using
    statistical methods with configurable sensitivity.
    """

    def __init__(self, sensitivity: float = 3.0, max_history: int = 50):
        """Initialize outlier detector.

        Args:
            sensitivity: Z-score threshold for outlier detection.
            max_history: Maximum samples to keep in history.
        """
        if sensitivity <= 0:
            raise ValidationError("Sensitivity must be positive")
        self.sensitivity = sensitivity
        self.sample_history: deque[float] = deque(maxlen=max_history)
        _LOGGER.debug("OutlierDetector initialized with sensitivity: %.1f", sensitivity)

    def add_sample(self, value: float) -> None:
        """Add power value to sample history.

        Args:
            value: Power consumption value to add.
        """
        if not isinstance(value, (int, float)) or not (0 <= value <= 100000):
            _LOGGER.warning("Invalid sample value: %s", value)
            return
        self.sample_history.append(float(value))

    def is_outlier(self, value: float) -> bool:
        """Check if value is statistical outlier.

        Args:
            value: Value to check for outlier status.

        Returns:
            bool: True if value is outlier, False otherwise.
        """
        try:
            # We need at least 5 samples to establish a baseline
            if len(self.sample_history) < 5:
                return False

            # Calculate stats on EXISTING history, excluding the value being checked
            # if it was already added (which happens in analyzer.py)
            history = list(self.sample_history)

            # If the value is already in history (added by analyzer.py before validation)
            # we should exclude it from the baseline calculation to avoid bias
            if history and history[-1] == value:
                history = history[:-1]

            if len(history) < 3:
                return False

            mean_val = statistics.mean(history)
            stdev_val = statistics.stdev(history)

            # If standard deviation is very low, any significant absolute change
            # might be flagged. We use a minimum threshold for stdev.
            effective_stdev = max(stdev_val, 2.0)  # Minimum 2.0W variation baseline

            z_score = abs(value - mean_val) / effective_stdev

            is_anomaly = z_score > self.sensitivity

            if is_anomaly:
                _LOGGER.debug(
                    "Outlier detected: %.2fW (mean: %.2fW, stdev: %.2fW, z: %.2f)",
                    value,
                    mean_val,
                    stdev_val,
                    z_score,
                )

            return is_anomaly

        except (statistics.StatisticsError, ZeroDivisionError):
            return False

    def get_thresholds(self) -> Dict[str, float]:
        """Get current outlier detection thresholds.

        Returns:
            Dict[str, float]: Threshold information including mean and stdev.
        """
        try:
            if len(self.sample_history) < 5:
                return {"lower": 0.0, "upper": 1000.0}

            mean_val = statistics.mean(self.sample_history)
            stdev_val = statistics.stdev(self.sample_history)

            return {
                "lower": mean_val - (self.sensitivity * stdev_val),
                "upper": mean_val + (self.sensitivity * stdev_val),
                "mean": mean_val,
                "stdev": stdev_val,
            }
        except statistics.StatisticsError:
            return {"lower": 0.0, "upper": 1000.0}

    def reset_history(self) -> None:
        """Reset sample history."""
        self.sample_history.clear()
        _LOGGER.debug("Outlier detector history reset")

    def get_sample_count(self) -> int:
        """Get the number of samples in history.

        Returns:
            int: Number of samples currently stored.
        """
        return len(self.sample_history)

    def get_statistics(self) -> Dict[str, float]:
        """Get statistical summary of the sample history.

        Returns:
            Dict[str, float]: Statistical measures.
        """
        try:
            if len(self.sample_history) < 2:
                return {
                    "count": len(self.sample_history),
                    "mean": 0.0,
                    "stdev": 0.0,
                }

            try:
                return {
                    "count": len(self.sample_history),
                    "mean": statistics.mean(self.sample_history),
                    "stdev": statistics.stdev(self.sample_history),
                    "min": min(self.sample_history),
                    "max": max(self.sample_history),
                }
            except statistics.StatisticsError:
                return {
                    "count": len(self.sample_history),
                    "mean": 0.0,
                    "stdev": 0.0,
                }

        except Exception as e:
            _LOGGER.error(
                "Error getting statistics: %s",
                e,
                exc_info=True,
            )
            return {"count": 0, "mean": 0.0, "stdev": 0.0}
