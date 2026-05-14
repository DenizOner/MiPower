"""
Metrics Storage for Monitoring - Single Responsibility Principle

This module implements metrics storage functionality following SOLID principles,
handling time series data storage and retrieval for performance monitoring.
"""

import logging
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, Optional

from .monitoring_interface import (
    MetricSeries,
    MetricsStorageInterface,
)

_LOGGER = logging.getLogger(__name__)


class MetricsStorage(MetricsStorageInterface):
    """Handles storage and retrieval of metrics data.

    This class is responsible for managing metric time series,
    implementing data retention policies, and providing efficient
    access to historical metric data. Follows Single Responsibility
    Principle by focusing only on data storage operations.
    """

    def __init__(self, retention_period: int = 3600):
        """Initialize the metrics storage.

        Args:
            retention_period: How long to keep metrics in seconds.
        """
        self.retention_period = retention_period
        self._series: Dict[str, MetricSeries] = defaultdict(
            lambda: MetricSeries("", max_points=1000)
        )
        _LOGGER.debug(
            "MetricsStorage initialized with retention: %ds", retention_period
        )

    def store_metric_point(
        self, name: str, value: float, labels: Optional[Dict[str, str]] = None
    ) -> None:
        """Store a new metric point in the time series.

        Args:
            name: Metric name
            value: Metric value
            labels: Optional labels
        """
        if name not in self._series:
            self._series[name] = MetricSeries(name)

        self._series[name].add_point(value, labels)
        _LOGGER.debug("Stored metric point: %s = %.3f", name, value)

    def get_metric_series(self, name: str) -> Optional[MetricSeries]:
        """Get the full time series for a metric.

        Args:
            name: Metric name

        Returns:
            MetricSeries or None if not found
        """
        return self._series.get(name)

    def get_latest_value(self, name: str) -> Optional[float]:
        """Get the latest value of a metric.

        Args:
            name: Metric name

        Returns:
            Latest value or None if metric doesn't exist
        """
        series = self.get_metric_series(name)
        return series.get_latest_value() if series else None

    def get_average(
        self, name: str, time_window: Optional[int] = None
    ) -> Optional[float]:
        """Get the average value of a metric over a time window.

        Args:
            name: Metric name
            time_window: Time window in seconds

        Returns:
            Average value or None
        """
        series = self.get_metric_series(name)
        return series.get_average(time_window) if series else None

    def get_all_latest_values(self) -> Dict[str, Any]:
        """Get the latest values for all metrics.

        Returns:
            Dictionary of metric names to their latest values
        """
        return {
            name: series.get_latest_value()
            for name, series in self._series.items()
            if series.points
        }

    def clear_old_metrics(self) -> None:
        """Clear metrics older than the retention period."""
        cutoff_time = datetime.now().timestamp() - self.retention_period
        cleared_count = 0

        for series in self._series.values():
            original_count = len(series.points)
            # Keep only recent points
            series.points = [
                point
                for point in series.points
                if point.timestamp.timestamp() >= cutoff_time
            ]
            cleared_count += original_count - len(series.points)

        if cleared_count > 0:
            _LOGGER.debug("Cleared %d old metric points", cleared_count)

    def get_storage_stats(self) -> Dict[str, Any]:
        """Get storage statistics.

        Returns:
            Dictionary containing storage metrics.
        """
        total_points = sum(len(series.points) for series in self._series.values())

        return {
            "total_series": len(self._series),
            "total_points": total_points,
            "retention_period": self.retention_period,
            "average_points_per_series": total_points / max(len(self._series), 1),
        }

    def cleanup_empty_series(self) -> int:
        """Remove series that have no points.

        Returns:
            Number of empty series removed.
        """
        empty_series = [
            name for name, series in self._series.items() if not series.points
        ]

        for name in empty_series:
            del self._series[name]

        if empty_series:
            _LOGGER.debug("Cleaned up %d empty metric series", len(empty_series))

        return len(empty_series)
