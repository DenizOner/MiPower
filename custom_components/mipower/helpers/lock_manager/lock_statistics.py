"""
Lock Statistics for Lock Management - Single Responsibility Principle

This module implements lock statistics tracking following SOLID principles,
handling performance metrics and lock usage statistics.
"""

import logging
from collections import defaultdict
from typing import Any, Dict

from .lock_manager_interface import (
    LockInfo,
    LockStatistics,
    LockStatisticsInterface,
)

_LOGGER = logging.getLogger(__name__)


class LockStatisticsTracker(LockStatisticsInterface):
    """Tracks comprehensive statistics for lock management operations.

    This class is responsible for maintaining and updating performance metrics
    for lock operations. Follows Single Responsibility Principle by focusing
    only on statistics management.
    """

    def __init__(self):
        """Initialize the statistics tracker with default values."""
        self._global_stats = LockStatistics()
        self._lock_stats: Dict[str, LockStatistics] = defaultdict(LockStatistics)

    def update_lock_statistics(self, lock_info: "LockInfo") -> None:
        """Update statistics when a lock is released.

        Calculates hold time and updates global and per-lock statistics.

        Args:
            lock_info: Information about the released lock.
        """
        hold_time = lock_info.get_duration()

        # Update global statistics
        self._global_stats.update_hold_time(hold_time)

        # Update per-lock statistics
        lock_id = lock_info.lock_id
        self._lock_stats[lock_id].update_hold_time(hold_time)

        _LOGGER.debug(
            "Updated statistics for lock %s: hold_time=%.3fs",
            lock_id,
            hold_time,
        )

    def record_timeout(self, lock_id: str) -> None:
        """Record a lock acquisition timeout.

        Args:
            lock_id: The lock that timed out.
        """
        self._global_stats.record_timeout()
        self._lock_stats[lock_id].record_timeout()

    def record_deadlock(self, lock_id: str) -> None:
        """Record a deadlock detection.

        Args:
            lock_id: The lock involved in the deadlock.
        """
        self._global_stats.record_deadlock()
        self._lock_stats[lock_id].record_deadlock()

    def record_contention(self, lock_id: str) -> None:
        """Record lock contention.

        Args:
            lock_id: The contended lock.
        """
        self._global_stats.record_contention()
        self._lock_stats[lock_id].record_contention()

    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive lock statistics.

        Returns:
            Dict[str, Any]: Complete statistics including global and per-lock metrics.
        """
        return {
            "global_stats": {
                "total_acquisitions": self._global_stats.total_acquisitions,
                "total_releases": self._global_stats.total_releases,
                "total_timeouts": self._global_stats.total_timeouts,
                "average_hold_time": round(self._global_stats.average_hold_time, 3),
                "max_hold_time": round(self._global_stats.max_hold_time, 3),
                "contention_count": self._global_stats.contention_count,
                "deadlock_count": self._global_stats.deadlock_count,
            },
            "lock_stats": {
                lock_id: {
                    "total_acquisitions": stats.total_acquisitions,
                    "total_timeouts": stats.total_timeouts,
                    "average_hold_time": round(stats.average_hold_time, 3),
                    "max_hold_time": round(stats.max_hold_time, 3),
                    "contention_count": stats.contention_count,
                    "deadlock_count": stats.deadlock_count,
                }
                for lock_id, stats in self._lock_stats.items()
            },
            "summary": self._get_summary_stats(),
        }

    def _get_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics for quick overview.

        Returns:
            Dict[str, Any]: Key performance indicators.
        """
        total_acquisitions = self._global_stats.total_acquisitions
        total_timeouts = self._global_stats.total_timeouts
        total_deadlocks = self._global_stats.deadlock_count

        success_rate = 0.0
        if total_acquisitions > 0:
            successful_acquisitions = total_acquisitions - total_timeouts
            success_rate = (successful_acquisitions / total_acquisitions) * 100

        return {
            "total_locks_tracked": len(self._lock_stats),
            "overall_success_rate": round(success_rate, 2),
            "total_timeouts": total_timeouts,
            "total_deadlocks": total_deadlocks,
            "average_hold_time": round(self._global_stats.average_hold_time, 3),
            "max_hold_time": round(self._global_stats.max_hold_time, 3),
        }

    def get_lock_specific_stats(self, lock_id: str) -> Dict[str, Any]:
        """Get statistics for a specific lock.

        Args:
            lock_id: The lock to get statistics for.

        Returns:
            Dict[str, Any]: Statistics for the specific lock.
        """
        stats = self._lock_stats.get(lock_id, LockStatistics())
        return {
            "lock_id": lock_id,
            "total_acquisitions": stats.total_acquisitions,
            "total_timeouts": stats.total_timeouts,
            "average_hold_time": round(stats.average_hold_time, 3),
            "max_hold_time": round(stats.max_hold_time, 3),
            "contention_count": stats.contention_count,
            "deadlock_count": stats.deadlock_count,
        }

    def reset_statistics(self) -> None:
        """Reset all statistics to initial values."""
        self._global_stats = LockStatistics()
        self._lock_stats.clear()
        _LOGGER.debug("Lock statistics reset to initial values")

    def get_health_indicators(self) -> Dict[str, Any]:
        """Get health indicators based on statistics.

        Returns:
            Dict[str, Any]: Health status indicators.
        """
        stats = self._global_stats

        # Define health thresholds
        high_timeout_rate = stats.total_timeouts > (
            stats.total_acquisitions * 0.1
        )  # >10%
        high_deadlock_rate = stats.deadlock_count > 5  # More than 5 deadlocks
        high_contention = stats.contention_count > (
            stats.total_acquisitions * 0.05
        )  # >5%

        overall_healthy = not (
            high_timeout_rate or high_deadlock_rate or high_contention
        )

        return {
            "overall_healthy": overall_healthy,
            "high_timeout_rate": high_timeout_rate,
            "high_deadlock_rate": high_deadlock_rate,
            "high_contention": high_contention,
            "recommendations": self._get_health_recommendations(
                high_timeout_rate, high_deadlock_rate, high_contention
            ),
        }

    def _get_health_recommendations(
        self, high_timeout: bool, high_deadlock: bool, high_contention: bool
    ) -> list[str]:
        """Get health recommendations based on issues detected.

        Args:
            high_timeout: Whether timeout rate is high.
            high_deadlock: Whether deadlock rate is high.
            high_contention: Whether contention is high.

        Returns:
            list[str]: List of recommendations.
        """
        recommendations = []

        if high_timeout:
            recommendations.append(
                "Consider increasing lock timeouts or reducing lock contention"
            )
        if high_deadlock:
            recommendations.append("Review lock acquisition order to prevent deadlocks")
        if high_contention:
            recommendations.append(
                "Consider reducing lock granularity or using read-write locks"
            )

        if not recommendations:
            recommendations.append("Lock performance is healthy")

        return recommendations
