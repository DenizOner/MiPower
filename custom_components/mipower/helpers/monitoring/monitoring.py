"""
Smartify helpers async monitoring module - SOLID Refactored Implementation.

This module provides monitoring functionality following SOLID principles,
using composition pattern with separated responsibilities for metrics collection,
health checking, alerting, and statistics calculation.
"""

import logging
from typing import Any, Dict, List, Optional

from .alert_manager import AlertManager
from .health_checker import HealthChecker
from .metrics_storage import MetricsStorage
from .monitoring_interface import (
    MetricsCollectorInterface,
    MetricSeries,
)
from .statistics_calculator import StatisticsCalculator

_LOGGER = logging.getLogger(__name__)


class MetricsCollector(MetricsCollectorInterface):
    """Collects and manages metrics for monitoring purposes.

    This class implements MetricsCollectorInterface and uses composition pattern
    with separated responsibilities following SOLID principles:
    - MetricsStorage for data persistence and retrieval
    - HealthChecker for system health monitoring
    - AlertManager for alert handling
    - StatisticsCalculator for metric analysis

    Follows Single Responsibility Principle by delegating specific tasks
    to specialized components while orchestrating the overall monitoring system.
    """

    def __init__(self, retention_period: int = 3600):
        """Initialize the MetricsCollector with SOLID components.

        Args:
            retention_period: How long to keep metrics in seconds.
        """
        # Initialize SOLID components using composition
        self._metrics_storage = MetricsStorage(retention_period)
        self._health_checker = HealthChecker()
        self._alert_manager = AlertManager()
        self._statistics_calculator = StatisticsCalculator()

        _LOGGER.debug(
            "MetricsCollector initialized with SOLID components, retention: %ds",
            retention_period,
        )

    def record_metric(
        self, name: str, value: float, labels: Optional[Dict[str, str]] = None
    ) -> None:
        """Record a metric value using metrics storage.

        Args:
            name: Metric name
            value: Metric value
            labels: Optional labels
        """
        self._metrics_storage.store_metric_point(name, value, labels)
        _LOGGER.debug("Recorded metric: %s = %.3f", name, value)

    def increment_counter(
        self, name: str, labels: Optional[Dict[str, str]] = None
    ) -> None:
        """Increment a counter metric.

        Args:
            name: Counter name
            labels: Optional labels
        """
        current_value = self._metrics_storage.get_latest_value(name) or 0
        self.record_metric(name, current_value + 1, labels)

    def record_histogram(
        self, name: str, value: float, buckets: Optional[List[float]] = None
    ) -> None:
        """Record a histogram metric.

        Args:
            name: Histogram name
            value: Observed value
            buckets: Bucket boundaries
        """
        if buckets is None:
            buckets = [0.1, 0.5, 1.0, 2.5, 5.0, 10.0]

        # Record the observed value
        self.record_metric(f"{name}_observed", value)

        # Update histogram buckets
        for bucket in buckets:
            if value <= bucket:
                self.increment_counter(f"{name}_bucket_{bucket}")

        # Update count and sum
        self.increment_counter(f"{name}_count")
        current_sum = self._metrics_storage.get_latest_value(f"{name}_sum") or 0
        self.record_metric(f"{name}_sum", current_sum + value)

    def get_metric_value(self, name: str) -> Optional[float]:
        """Get the latest value of a metric.

        Args:
            name: Metric name

        Returns:
            Latest value or None if metric doesn't exist
        """
        return self._metrics_storage.get_latest_value(name)

    def get_metric_average(
        self, name: str, time_window: Optional[int] = None
    ) -> Optional[float]:
        """Get the average value of a metric over a time window.

        Args:
            name: Metric name
            time_window: Time window in seconds

        Returns:
            Average value or None
        """
        return self._metrics_storage.get_average(name, time_window)

    def get_all_metrics(self) -> Dict[str, Any]:
        """Get all current metric values.

        Returns:
            Dictionary of metric names to their latest values
        """
        return self._metrics_storage.get_all_latest_values()

    def get_metric_series(self, name: str) -> Optional[MetricSeries]:
        """Get the full time series for a metric.

        Args:
            name: Metric name

        Returns:
            MetricSeries or None if not found
        """
        return self._metrics_storage.get_metric_series(name)

    def set_health_check(self, check_name: str, healthy: bool) -> None:
        """Set the status of a health check using health checker.

        Args:
            check_name: Health check name
            healthy: Whether the check is healthy
        """
        self._health_checker.set_health_check(check_name, healthy)

    def get_health_status(self) -> Dict[str, Any]:
        """Get overall health status from health checker.

        Returns:
            Health status information
        """
        return self._health_checker.get_health_status()

    def add_alert(
        self,
        alert_name: str,
        message: str,
        severity: str = "warning",
        labels: Optional[Dict[str, str]] = None,
    ) -> None:
        """Add an alert using alert manager.

        Args:
            alert_name: Alert name
            message: Alert message
            severity: Alert severity (info, warning, error, critical)
            labels: Optional labels
        """
        self._alert_manager.add_alert(alert_name, message, severity, labels)

    def get_alerts(
        self, severity: Optional[str] = None, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get recent alerts from alert manager.

        Args:
            severity: Filter by severity
            limit: Maximum number of alerts to return

        Returns:
            List of alerts
        """
        return self._alert_manager.get_alerts(severity, limit)

    def clear_old_metrics(self) -> None:
        """Clear metrics older than the retention period using metrics storage."""
        self._metrics_storage.clear_old_metrics()

    def get_summary(self) -> Dict[str, Any]:
        """Get a comprehensive summary from statistics calculator.

        Returns:
            Summary dictionary containing all monitoring data
        """
        return self._statistics_calculator.get_summary()


# Global metrics collector instance
_global_collector = MetricsCollector()


def get_global_collector() -> MetricsCollector:
    """Get the global metrics collector instance.

    Returns:
        Global MetricsCollector instance
    """
    return _global_collector


def record_batch_metric(name: str, value: float, batch_id: str) -> None:
    """Record a batch-related metric.

    Args:
        name: Metric name
        value: Metric value
        batch_id: Batch ID for labeling
    """
    _global_collector.record_metric(name, value, {"batch_id": batch_id})


def record_lock_metric(name: str, value: float, lock_id: str, owner: str) -> None:
    """Record a lock-related metric.

    Args:
        name: Metric name
        value: Metric value
        lock_id: Lock ID
        owner: Lock owner
    """
    _global_collector.record_metric(name, value, {"lock_id": lock_id, "owner": owner})


def check_system_health() -> Dict[str, Any]:
    """Perform system health checks.

    Returns:
        Health check results
    """
    # This is a placeholder - in a real implementation, you would
    # check various system components
    _global_collector.set_health_check("system_memory", True)
    _global_collector.set_health_check("system_cpu", True)
    _global_collector.set_health_check("async_operations", True)

    return _global_collector.get_health_status()
