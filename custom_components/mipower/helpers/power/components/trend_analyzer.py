"""
Trend Analyzer Component - Time Series Trend Analysis

This module implements trend analysis for power consumption data using
linear regression. It analyzes power consumption trends over time to
determine if consumption is increasing, decreasing, or stable.

Classes:
    TrendAnalyzer: Time-series trend analysis using linear regression.
"""

import logging
import statistics
from collections import deque
from typing import List

from ....helpers.errors.exceptions import ValidationError
from ..power_analyzer_interface import TrendAnalyzerInterface

_LOGGER = logging.getLogger(__name__)


class TrendAnalyzer(TrendAnalyzerInterface):
    """Time-series trend analysis using linear regression.

    Analyzes power consumption trends over time using statistical methods
    to determine if consumption is increasing, decreasing, or stable.
    """

    def __init__(self, window_size: int = 10):
        """Initialize trend analyzer.

        Args:
            window_size: Number of samples for trend analysis.
        """
        if window_size < 3:
            raise ValidationError("Window size must be at least 3")
        self.window_size = window_size
        self.power_history: deque[float] = deque(maxlen=window_size)

    def add_sample(self, power_value: float) -> None:
        """Add power value to trend analysis history.

        Args:
            power_value: Power consumption value to add.
        """
        if not isinstance(power_value, (int, float)):
            _LOGGER.warning("Invalid power value for trend: %s", power_value)
            return
        self.power_history.append(float(power_value))

    def analyze_trend(self) -> str:
        """Analyze current power consumption trend.

        Returns:
            str: Trend description ("increasing", "decreasing", "stable", "insufficient_data").
        """
        try:
            if len(self.power_history) < 3:
                return "insufficient_data"

            slope = self._calculate_slope(list(self.power_history))

            if slope > 1.0:
                return "increasing"
            elif slope < -1.0:
                return "decreasing"
            else:
                return "stable"

        except (statistics.StatisticsError, ZeroDivisionError):
            return "stable"

    def get_trend_strength(self) -> float:
        """Get trend strength normalized to 0.0-1.0 range.

        Returns:
            float: Trend strength between 0.0 and 1.0.
        """
        if len(self.power_history) < 3:
            return 0.0

        try:
            slope = self._calculate_slope(list(self.power_history))
            return min(1.0, abs(slope) / 10.0)
        except (statistics.StatisticsError, ZeroDivisionError):
            return 0.0

    def _calculate_slope(self, values: List[float]) -> float:
        """Calculate linear regression slope.

        Args:
            values: Power values in chronological order.

        Returns:
            float: Slope of regression line.
        """
        n = len(values)
        mean_x = (n - 1) / 2
        mean_y = statistics.mean(values)

        numerator = sum((i - mean_x) * (values[i] - mean_y) for i in range(n))
        denominator = sum((i - mean_x) ** 2 for i in range(n))

        return numerator / denominator if denominator != 0 else 0.0

    def get_slope(self) -> float:
        """Get the raw slope of the current trend.

        Returns:
            float: Raw slope value (can be positive, negative, or zero).
        """
        try:
            return self._calculate_slope(list(self.power_history))
        except (statistics.StatisticsError, ZeroDivisionError):
            return 0.0

    def get_correlation_coefficient(self) -> float:
        """Calculate the correlation coefficient (R-squared) for the trend.

        Returns:
            float: Correlation coefficient between 0.0 and 1.0.
        """
        try:
            if len(self.power_history) < 3:
                return 0.0

            values = list(self.power_history)
            n = len(values)

            # Calculate means
            mean_x = (n - 1) / 2
            mean_y = statistics.mean(values)

            # Calculate sums for correlation
            ss_xx = sum((i - mean_x) ** 2 for i in range(n))
            ss_yy = sum((y - mean_y) ** 2 for y in values)
            ss_xy = sum((i - mean_x) * (values[i] - mean_y) for i in range(n))

            if ss_xx == 0 or ss_yy == 0:
                return 0.0

            # Calculate correlation coefficient
            r = ss_xy / ((ss_xx * ss_yy) ** 0.5)
            r_squared = r**2

            return min(1.0, max(0.0, r_squared))

        except Exception as e:
            _LOGGER.error(
                "Error calculating correlation coefficient: %s",
                e,
                exc_info=True,
            )
            return 0.0

    def reset_history(self) -> None:
        """Reset the power history."""
        self.power_history.clear()
        _LOGGER.debug("Trend analyzer history reset")

    def get_history_size(self) -> int:
        """Get the number of samples in history.

        Returns:
            int: Number of samples currently stored.
        """
        return len(self.power_history)

    def get_statistics(self) -> dict[str, float]:
        """Get statistical summary of the power history.

        Returns:
            dict[str, float]: Statistical measures.
        """
        try:
            if len(self.power_history) < 2:
                return {
                    "count": len(self.power_history),
                    "mean": 0.0,
                    "slope": 0.0,
                    "trend_strength": 0.0,
                }

            values = list(self.power_history)
            return {
                "count": len(values),
                "mean": statistics.mean(values),
                "slope": self.get_slope(),
                "trend_strength": self.get_trend_strength(),
                "correlation": self.get_correlation_coefficient(),
                "min": min(values),
                "max": max(values),
            }

        except Exception as e:
            _LOGGER.error(
                "Error getting statistics: %s",
                e,
                exc_info=True,
            )
            return {
                "count": 0,
                "mean": 0.0,
                "slope": 0.0,
                "trend_strength": 0.0,
            }
