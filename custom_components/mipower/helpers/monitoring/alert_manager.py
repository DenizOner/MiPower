"""
Alert Manager for Monitoring - Single Responsibility Principle

This module implements alert management functionality following SOLID principles,
handling alert creation, storage, filtering, and retrieval.
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from .monitoring_interface import AlertManagerInterface

_LOGGER = logging.getLogger(__name__)


class AlertManager(AlertManagerInterface):
    """Handles alert management and notification system.

    This class is responsible for storing alerts, managing alert history,
    filtering alerts by severity and other criteria, and providing
    access to alert information. Follows Single Responsibility Principle
    by focusing only on alert management operations.
    """

    def __init__(self, max_alerts: int = 1000):
        """Initialize the alert manager.

        Args:
            max_alerts: Maximum number of alerts to keep in history.
        """
        self.max_alerts = max_alerts
        self._alerts: List[Dict[str, Any]] = []
        _LOGGER.debug("AlertManager initialized with max_alerts: %d", max_alerts)

    def add_alert(
        self,
        alert_name: str,
        message: str,
        severity: str = "warning",
        labels: Optional[Dict[str, str]] = None,
    ) -> None:
        """Add an alert to the system.

        Args:
            alert_name: Unique name for the alert.
            message: Descriptive message for the alert.
            severity: Severity level (info, warning, error, critical).
            labels: Optional labels for categorization.
        """
        alert = {
            "name": alert_name,
            "message": message,
            "severity": severity,
            "timestamp": datetime.now(),
            "labels": labels or {},
        }

        self._alerts.append(alert)

        # Maintain maximum alert history
        if len(self._alerts) > self.max_alerts:
            removed_count = len(self._alerts) - self.max_alerts
            self._alerts = self._alerts[-self.max_alerts :]
            _LOGGER.debug("Trimmed %d old alerts to maintain limit", removed_count)

        # Log the alert
        log_level = self._get_log_level(severity)
        _LOGGER.log(log_level, "Alert raised: %s - %s", alert_name, message)

    def get_alerts(
        self,
        severity: Optional[str] = None,
        limit: int = 100,
        alert_name: Optional[str] = None,
        since: Optional[datetime] = None,
    ) -> List[Dict[str, Any]]:
        """Get alerts with optional filtering.

        Args:
            severity: Filter by severity level.
            limit: Maximum number of alerts to return.
            alert_name: Filter by specific alert name.
            since: Filter alerts since this timestamp.

        Returns:
            List of alerts matching the criteria.
        """
        alerts = self._alerts

        # Apply filters
        if severity:
            alerts = [a for a in alerts if a["severity"] == severity]

        if alert_name:
            alerts = [a for a in alerts if a["name"] == alert_name]

        if since:
            alerts = [a for a in alerts if a["timestamp"] >= since]

        # Return most recent alerts up to limit
        return alerts[-limit:] if alerts else []

    def get_alert_count(
        self, severity: Optional[str] = None, since: Optional[datetime] = None
    ) -> int:
        """Get the count of alerts matching criteria.

        Args:
            severity: Filter by severity level.
            since: Filter alerts since this timestamp.

        Returns:
            Number of matching alerts.
        """
        return len(
            self.get_alerts(severity=severity, since=since, limit=self.max_alerts)
        )

    def get_recent_alerts(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get alerts from the last N hours.

        Args:
            hours: Number of hours to look back.

        Returns:
            List of recent alerts.
        """
        since = datetime.now().replace(hour=datetime.now().hour - hours)
        return self.get_alerts(since=since, limit=self.max_alerts)

    def get_alerts_by_severity(self) -> Dict[str, int]:
        """Get alert count grouped by severity.

        Returns:
            Dictionary mapping severity levels to alert counts.
        """
        severity_counts = {}
        for alert in self._alerts:
            severity = alert["severity"]
            severity_counts[severity] = severity_counts.get(severity, 0) + 1

        return severity_counts

    def clear_alerts(
        self,
        severity: Optional[str] = None,
        alert_name: Optional[str] = None,
        before: Optional[datetime] = None,
    ) -> int:
        """Clear alerts matching the specified criteria.

        Args:
            severity: Clear only alerts with this severity.
            alert_name: Clear only alerts with this name.
            before: Clear only alerts before this timestamp.

        Returns:
            Number of alerts cleared.
        """
        original_count = len(self._alerts)

        # Build filter function
        def should_keep(alert):
            if severity and alert["severity"] == severity:
                return False
            if alert_name and alert["name"] == alert_name:
                return False
            if before and alert["timestamp"] < before:
                return False
            return True

        self._alerts = [alert for alert in self._alerts if should_keep(alert)]
        cleared_count = original_count - len(self._alerts)

        if cleared_count > 0:
            _LOGGER.debug("Cleared %d alerts", cleared_count)

        return cleared_count

    def get_alert_summary(self) -> Dict[str, Any]:
        """Get a summary of alert activity.

        Returns:
            Dictionary containing alert statistics and recent activity.
        """
        if not self._alerts:
            return {
                "total_alerts": 0,
                "severity_breakdown": {},
                "most_recent_alert": None,
                "alerts_last_24h": 0,
            }

        recent_alerts = self.get_recent_alerts(24)

        return {
            "total_alerts": len(self._alerts),
            "severity_breakdown": self.get_alerts_by_severity(),
            "most_recent_alert": (self._alerts[-1]["name"] if self._alerts else None),
            "alerts_last_24h": len(recent_alerts),
            "oldest_alert": (self._alerts[0]["timestamp"] if self._alerts else None),
            "newest_alert": (self._alerts[-1]["timestamp"] if self._alerts else None),
        }

    def _get_log_level(self, severity: str) -> int:
        """Convert severity string to logging level.

        Args:
            severity: Severity string (info, warning, error, critical).

        Returns:
            Corresponding logging level constant.
        """
        severity_map = {
            "info": logging.INFO,
            "warning": logging.WARNING,
            "error": logging.ERROR,
            "critical": logging.CRITICAL,
        }
        return severity_map.get(severity.lower(), logging.WARNING)

    def reset(self) -> None:
        """Reset the alert manager by clearing all alerts."""
        self._alerts.clear()
        _LOGGER.debug("Alert manager reset")

    def get_storage_stats(self) -> Dict[str, Any]:
        """Get storage statistics for alerts.

        Returns:
            Dictionary containing storage metrics.
        """
        return {
            "current_alerts": len(self._alerts),
            "max_capacity": self.max_alerts,
            "utilization_percentage": (len(self._alerts) / self.max_alerts) * 100,
        }
