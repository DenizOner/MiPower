"""
Statistics Calculator for Monitoring - Single Responsibility Principle

This module implements statistics calculation functionality following SOLID principles,
handling metric analysis and statistical computations for performance monitoring.
"""

import logging
from typing import Any, Dict, Optional

from .monitoring_interface import StatisticsCalculatorInterface

_LOGGER = logging.getLogger(__name__)


class StatisticsCalculator(StatisticsCalculatorInterface):
    """Handles statistical calculations for monitoring data.

    This class is responsible for computing averages, aggregations,
    and statistical analysis of monitoring metrics. Follows Single
    Responsibility Principle by focusing only on statistical operations.
    """

    def __init__(self):
        """Initialize the statistics calculator."""
        _LOGGER.debug("StatisticsCalculator initialized")

    def get_metric_average(
        self, name: str, time_window: Optional[int] = None
    ) -> Optional[float]:
        """Get the average value of a metric over a time window.

        Note: This method requires access to the metrics storage.
        In a real implementation, this would be injected as a dependency.

        Args:
            name: Metric name
            time_window: Time window in seconds

        Returns:
            Average value or None
        """
        # This is a placeholder - actual implementation would need metrics storage
        _LOGGER.debug(
            "Calculating average for metric %s over %s seconds",
            name,
            time_window,
        )
        return None

    def get_summary(self) -> Dict[str, Any]:
        """Get a comprehensive summary of monitoring data.

        Note: This method requires access to multiple storage components.
        In a real implementation, these would be injected as dependencies.

        Returns:
            Dictionary containing comprehensive monitoring summary.
        """
        # This is a placeholder - actual implementation would aggregate from all sources
        return {
            "metrics_summary": {
                "total_series": 0,
                "total_points": 0,
                "active_metrics": 0,
            },
            "health_summary": {
                "overall_healthy": True,
                "total_checks": 0,
                "healthy_percentage": 100.0,
            },
            "alerts_summary": {
                "total_alerts": 0,
                "critical_alerts": 0,
                "warnings_today": 0,
            },
            "performance_indicators": {
                "data_retention_hours": 24,
                "average_response_time": 0.0,
                "error_rate": 0.0,
            },
        }

    def calculate_percentile(
        self, values: list[float], percentile: float
    ) -> Optional[float]:
        """Calculate a percentile from a list of values.

        Args:
            values: List of numeric values.
            percentile: Percentile to calculate (0.0 to 100.0).

        Returns:
            The calculated percentile value or None if no values.
        """
        if not values:
            return None

        sorted_values = sorted(values)
        index = (len(sorted_values) - 1) * (percentile / 100.0)
        lower_index = int(index)
        upper_index = min(lower_index + 1, len(sorted_values) - 1)

        if lower_index == upper_index:
            return sorted_values[lower_index]

        # Linear interpolation between values
        weight = index - lower_index
        return (
            sorted_values[lower_index] * (1 - weight)
            + sorted_values[upper_index] * weight
        )

    def calculate_trend(
        self, values: list[float], window_size: int = 5
    ) -> Optional[float]:
        """Calculate trend (slope) from recent values using linear regression.

        Args:
            values: List of values in chronological order.
            window_size: Number of recent values to use for trend calculation.

        Returns:
            Trend slope or None if insufficient data.
        """
        if len(values) < window_size:
            return None

        # Use only the most recent values
        recent_values = values[-window_size:]

        # Simple linear regression
        n = len(recent_values)
        x_values = list(range(n))  # Time indices

        sum_x = sum(x_values)
        sum_y = sum(recent_values)
        sum_xy = sum(x * y for x, y in zip(x_values, recent_values))
        sum_xx = sum(x * x for x in x_values)

        # Calculate slope
        numerator = n * sum_xy - sum_x * sum_y
        denominator = n * sum_xx - sum_x * sum_x

        if denominator == 0:
            return 0.0

        return numerator / denominator

    def detect_anomalies(
        self, values: list[float], threshold_std: float = 2.0
    ) -> list[bool]:
        """Detect anomalies in a series of values using standard deviation.

        Args:
            values: List of values to analyze.
            threshold_std: Number of standard deviations for anomaly threshold.

        Returns:
            List of boolean values indicating which points are anomalies.
        """
        if len(values) < 3:
            return [False] * len(values)

        # Calculate mean and standard deviation
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        std_dev = variance**0.5

        if std_dev == 0:
            return [False] * len(values)

        # Identify anomalies
        anomalies = []
        for value in values:
            z_score = abs(value - mean) / std_dev
            anomalies.append(z_score > threshold_std)

        return anomalies

    def calculate_rate_of_change(self, values: list[float]) -> list[Optional[float]]:
        """Calculate rate of change between consecutive values.

        Args:
            values: List of values in chronological order.

        Returns:
            List of rate of change values (None for first value).
        """
        if not values:
            return []

        rates: list[Optional[float]] = [None]  # First value has no previous value

        for i in range(1, len(values)):
            if values[i - 1] != 0:
                rate = (values[i] - values[i - 1]) / values[i - 1]
                rates.append(rate)
            else:
                rates.append(None)  # Avoid division by zero

        return rates

    def get_distribution_stats(self, values: list[float]) -> Dict[str, Any]:
        """Calculate comprehensive distribution statistics.

        Args:
            values: List of numeric values.

        Returns:
            Dictionary containing various statistical measures.
        """
        if not values:
            return {
                "count": 0,
                "mean": None,
                "median": None,
                "min": None,
                "max": None,
                "std_dev": None,
                "percentiles": {},
            }

        sorted_values = sorted(values)
        n = len(values)

        # Basic statistics
        mean = sum(values) / n
        median = (
            sorted_values[n // 2]
            if n % 2 == 1
            else (sorted_values[n // 2 - 1] + sorted_values[n // 2]) / 2
        )
        min_val = min(values)
        max_val = max(values)

        # Standard deviation
        variance = sum((x - mean) ** 2 for x in values) / n
        std_dev = variance**0.5

        # Percentiles
        percentiles = {
            "25th": self.calculate_percentile(values, 25),
            "50th": median,
            "75th": self.calculate_percentile(values, 75),
            "90th": self.calculate_percentile(values, 90),
            "95th": self.calculate_percentile(values, 95),
            "99th": self.calculate_percentile(values, 99),
        }

        return {
            "count": n,
            "mean": mean,
            "median": median,
            "min": min_val,
            "max": max_val,
            "std_dev": std_dev,
            "range": max_val - min_val,
            "percentiles": percentiles,
        }
