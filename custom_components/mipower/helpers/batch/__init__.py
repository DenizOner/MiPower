"""
Batch Processing Package.

This module provides comprehensive batch processing functionality following SOLID principles,
supporting operation dependencies, priority queuing, retry mechanisms, and performance monitoring.

All components follow SOLID principles with proper abstraction and separation of concerns.
"""

from .batch import BatchProcessor
from .batch_interface import (
    BatchProcessorInterface,
    DependencyResolverInterface,
    OperationExecutorInterface,
    StatisticsTrackerInterface,
)
from .batch_plugin import BatchPlugin
from .dependency_resolver import DependencyResolver
from .operation_executor import OperationExecutor
from .statistics_tracker import StatisticsTracker

__all__ = [
    "BatchProcessor",
    "BatchProcessorInterface",
    "DependencyResolverInterface",
    "OperationExecutorInterface",
    "StatisticsTrackerInterface",
    "BatchPlugin",
    "DependencyResolver",
    "OperationExecutor",
    "StatisticsTracker",
]
