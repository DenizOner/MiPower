"""
Health Checker for Monitoring - Single Responsibility Principle

This module implements health checking functionality following SOLID principles,
handling system health monitoring and status reporting.
"""

import logging
from typing import Any, Dict

from .monitoring_interface import HealthCheckerInterface

_LOGGER = logging.getLogger(__name__)


class HealthChecker(HealthCheckerInterface):
    """Handles system health checking and status reporting.

    This class is responsible for maintaining health check states,
    calculating overall system health, and providing health status
    information. Follows Single Responsibility Principle by focusing
    only on health monitoring operations.
    """

    def __init__(self):
        """Initialize the health checker with empty check registry."""
        self._health_checks: Dict[str, bool] = {}
        _LOGGER.debug("HealthChecker initialized")

    def set_health_check(self, check_name: str, healthy: bool) -> None:
        """Set the status of a health check.

        Args:
            check_name: Health check name
            healthy: Whether the check is healthy
        """
        previous_state = self._health_checks.get(check_name)
        self._health_checks[check_name] = healthy

        if previous_state != healthy:
            status = "healthy" if healthy else "unhealthy"
            log_level = logging.INFO if healthy else logging.WARNING
            _LOGGER.log(log_level, "Health check %s: %s", check_name, status)

    def get_health_status(self) -> Dict[str, Any]:
        """Get overall health status.

        Returns:
            Health status information including individual checks
            and overall health assessment.
        """
        total_checks = len(self._health_checks)
        healthy_checks = sum(1 for healthy in self._health_checks.values() if healthy)
        unhealthy_checks = total_checks - healthy_checks

        return {
            "overall_healthy": unhealthy_checks == 0,
            "total_checks": total_checks,
            "healthy_checks": healthy_checks,
            "unhealthy_checks": unhealthy_checks,
            "checks": self._health_checks.copy(),
        }

    def get_unhealthy_checks(self) -> list[str]:
        """Get the names of all unhealthy checks.

        Returns:
            List of unhealthy check names.
        """
        return [name for name, healthy in self._health_checks.items() if not healthy]

    def get_healthy_checks(self) -> list[str]:
        """Get the names of all healthy checks.

        Returns:
            List of healthy check names.
        """
        return [name for name, healthy in self._health_checks.items() if healthy]

    def is_healthy(self) -> bool:
        """Check if the overall system is healthy.

        Returns:
            True if all checks are healthy, False otherwise.
        """
        return all(self._health_checks.values())

    def get_health_percentage(self) -> float:
        """Get the percentage of healthy checks.

        Returns:
            Health percentage (0.0 to 100.0).
        """
        if not self._health_checks:
            return 100.0

        healthy_count = sum(1 for healthy in self._health_checks.values() if healthy)
        return (healthy_count / len(self._health_checks)) * 100.0

    def reset_checks(self) -> None:
        """Reset all health checks to unknown state."""
        self._health_checks.clear()
        _LOGGER.debug("Health checks reset")

    def remove_check(self, check_name: str) -> bool:
        """Remove a health check.

        Args:
            check_name: Name of the check to remove.

        Returns:
            True if check was removed, False if it didn't exist.
        """
        if check_name in self._health_checks:
            del self._health_checks[check_name]
            _LOGGER.debug("Removed health check: %s", check_name)
            return True
        return False
