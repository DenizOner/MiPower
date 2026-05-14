"""
Monitoring Interface for Smartify - Dependency Inversion for Monitoring

This module defines the abstraction layer for monitoring in Smartify,
implementing Dependency Inversion Principle (DIP) by decoupling monitoring
logic from the coordinator and other high-level components.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class MetricPoint:
    """Represents a single metric measurement point.

    Attributes:
        name: Metric name
        value: Metric value
        timestamp: When the metric was recorded
        labels: Additional labels for the metric
    """

    name: str
    value: float
    timestamp: datetime = field(default_factory=datetime.now)
    labels: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert metric point to dictionary.

        Returns:
            Dictionary representation of the metric point.
        """
        return {
            "name": self.name,
            "value": self.value,
            "timestamp": self.timestamp.isoformat(),
            "labels": self.labels.copy(),
        }


@dataclass
class MetricSeries:
    """Represents a time series of metric measurements.

    Attributes:
        name: Metric name
        points: List of metric points
        max_points: Maximum number of points to keep
    """

    name: str
    points: List[MetricPoint] = field(default_factory=list)
    max_points: int = 1000

    def add_point(self, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        """Add a new metric point.

        Args:
            value: Metric value
            labels: Optional labels
        """
        point = MetricPoint(name=self.name, value=value, labels=labels or {})
        self.points.append(point)

        # Keep only the most recent points
        if len(self.points) > self.max_points:
            self.points = self.points[-self.max_points :]

    def get_latest_value(self) -> Optional[float]:
        """Get the latest metric value.

        Returns:
            Latest value or None if no points exist
        """
        if not self.points:
            return None
        return self.points[-1].value

    def get_average(self, time_window: Optional[int] = None) -> Optional[float]:
        """Get average value over a time window.

        Args:
            time_window: Time window in seconds (None for all points)

        Returns:
            Average value or None if no points in window
        """
        if not self.points:
            return None

        if time_window is None:
            values = [p.value for p in self.points]
        else:
            cutoff = datetime.now().timestamp() - time_window
            values = [p.value for p in self.points if p.timestamp.timestamp() >= cutoff]

        return sum(values) / len(values) if values else None


class MetricsCollectorInterface(ABC):
    """Abstract interface for metrics collection functionality."""

    @abstractmethod
    def record_metric(
        self, name: str, value: float, labels: Optional[Dict[str, str]] = None
    ) -> None:
        """Record a metric value.

        Args:
            name: Metric name
            value: Metric value
            labels: Optional labels
        """

    @abstractmethod
    def get_metric_value(self, name: str) -> Optional[float]:
        """Get the latest value of a metric.

        Args:
            name: Metric name

        Returns:
            Latest value or None if metric doesn't exist
        """

    @abstractmethod
    def get_all_metrics(self) -> Dict[str, Any]:
        """Get all current metric values.

        Returns:
            Dictionary of metric names to their latest values
        """


class HealthCheckerInterface(ABC):
    """Abstract interface for health checking functionality."""

    @abstractmethod
    def set_health_check(self, check_name: str, healthy: bool) -> None:
        """Set the status of a health check.

        Args:
            check_name: Health check name
            healthy: Whether the check is healthy
        """

    @abstractmethod
    def get_health_status(self) -> Dict[str, Any]:
        """Get overall health status.

        Returns:
            Health status information
        """


class AlertManagerInterface(ABC):
    """Abstract interface for alert management functionality."""

    @abstractmethod
    def add_alert(
        self,
        alert_name: str,
        message: str,
        severity: str = "warning",
        labels: Optional[Dict[str, str]] = None,
    ) -> None:
        """Add an alert.

        Args:
            alert_name: Alert name
            message: Alert message
            severity: Alert severity
            labels: Optional labels
        """

    @abstractmethod
    def get_alerts(
        self, severity: Optional[str] = None, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get recent alerts.

        Args:
            severity: Filter by severity
            limit: Maximum number of alerts to return

        Returns:
            List of alerts
        """


class StatisticsCalculatorInterface(ABC):
    """Abstract interface for statistics calculation functionality."""

    @abstractmethod
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

    @abstractmethod
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of all monitoring data.

        Returns:
            Summary dictionary
        """


class MetricsStorageInterface(ABC):
    """Abstract interface for metrics storage functionality."""

    @abstractmethod
    def clear_old_metrics(self) -> None:
        """Clear metrics older than the retention period."""

    @abstractmethod
    def get_metric_series(self, name: str) -> Optional[Any]:
        """Get the full time series for a metric.

        Args:
            name: Metric name

        Returns:
            MetricSeries or None if not found
        """
