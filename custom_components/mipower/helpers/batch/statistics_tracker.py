"""
Statistics Tracker for Batch Operations - Single Responsibility Principle

This module implements statistics tracking functionality following SOLID principles,
handling performance metrics and batch execution statistics.
"""

import logging
from typing import Any, Dict

from ..logger.batch_logger import statistics_logging
from .batch_interface import (
    BatchResult,
    BatchStatus,
    StatisticsTrackerInterface,
)

_LOGGER = logging.getLogger(__name__)


class StatisticsTracker(StatisticsTrackerInterface):
    """Tracks performance statistics for batch operations.

    This class is responsible for maintaining and updating performance metrics
    for batch processing operations. Follows Single Responsibility Principle
    by focusing only on statistics management.
    """

    def __init__(self):
        """Initialize the statistics tracker with default values."""
        self._stats = {
            "total_batches": 0,
            "total_operations": 0,
            "successful_operations": 0,
            "failed_operations": 0,
            "average_batch_time": 0.0,
            "average_operation_time": 0.0,
        }

    @statistics_logging()
    def update_batch_statistics(self, batch_result: BatchResult) -> None:
        """Update statistics based on completed batch execution.

        Calculates running averages and updates counters based on batch results.

        Args:
            batch_result: The results of a completed batch execution.
        """
        # Update counters
        self._stats["total_batches"] += 1
        self._stats["total_operations"] += batch_result.total_operations

        if batch_result.status == BatchStatus.COMPLETED:
            self._stats["successful_operations"] += batch_result.completed_operations
        else:
            self._stats["failed_operations"] += batch_result.failed_operations

        # Update average batch time
        batch_duration = batch_result.get_duration() or 0
        total_batches = self._stats["total_batches"]
        self._stats["average_batch_time"] = (
            (self._stats["average_batch_time"] * (total_batches - 1)) + batch_duration
        ) / total_batches

        # Update average operation time
        if batch_result.total_operations > 0:
            avg_op_time = batch_duration / batch_result.total_operations
            total_ops = self._stats["total_operations"]
            prev_total_ops = total_ops - batch_result.total_operations
            self._stats["average_operation_time"] = (
                (self._stats["average_operation_time"] * prev_total_ops) + avg_op_time
            ) / total_ops

        _LOGGER.debug(
            "Updated statistics for batch %s: duration=%.2fs, success_rate=%.1f%%",
            batch_result.batch_id,
            batch_duration,
            batch_result.get_success_rate(),
        )

    @statistics_logging()
    def get_statistics(self) -> Dict[str, Any]:
        """Get current statistics with calculated metrics.

        Returns:
            Dict[str, Any]: Comprehensive statistics dictionary including
                success rates and performance metrics.
        """
        stats = self._stats.copy()

        # Calculate derived metrics
        total_ops = stats["total_operations"]
        if total_ops > 0:
            stats["success_rate"] = (stats["successful_operations"] / total_ops) * 100
            stats["failure_rate"] = (stats["failed_operations"] / total_ops) * 100
        else:
            stats["success_rate"] = 0.0
            stats["failure_rate"] = 0.0

        return stats

    @statistics_logging()
    def reset_statistics(self) -> None:
        """Reset all statistics to initial values."""
        self._stats = {
            "total_batches": 0,
            "total_operations": 0,
            "successful_operations": 0,
            "failed_operations": 0,
            "average_batch_time": 0.0,
            "average_operation_time": 0.0,
        }
        _LOGGER.debug("Statistics reset to initial values")

    @statistics_logging()
    def get_summary_report(self) -> Dict[str, Any]:
        """Get a summary report of current statistics.

        Returns:
            Dict[str, Any]: Formatted summary with key performance indicators.
        """
        stats = self.get_statistics()
        return {
            "performance_summary": {
                "total_batches_processed": stats["total_batches"],
                "total_operations_processed": stats["total_operations"],
                "overall_success_rate": round(stats["success_rate"], 2),
                "average_batch_duration": round(stats["average_batch_time"], 3),
                "average_operation_duration": round(stats["average_operation_time"], 3),
            },
            "health_indicators": {
                "is_healthy": stats["total_batches"] > 0
                and stats["success_rate"] > 80.0,
                "operations_per_batch": round(
                    stats["total_operations"] / max(stats["total_batches"], 1),
                    2,
                ),
                "failure_rate_acceptable": stats["failure_rate"] < 20.0,
            },
            "raw_statistics": stats,
        }
