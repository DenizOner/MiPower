"""
Monitoring Package.

This module provides comprehensive performance monitoring functionality following SOLID principles,
including metrics collection, health checks, alerting, and statistical analysis.

All components follow SOLID principles with proper abstraction and separation of concerns.
"""

from .alert_manager import AlertManager
from .health_checker import HealthChecker
from .metrics_storage import MetricsStorage
from .monitoring import (
    MetricsCollector,
    get_global_collector,
    record_batch_metric,
    record_lock_metric,
)
from .monitoring_interface import (
    AlertManagerInterface,
    HealthCheckerInterface,
    MetricsCollectorInterface,
    MetricsStorageInterface,
    StatisticsCalculatorInterface,
)
from .monitoring_plugin import MonitoringPlugin
from .statistics_calculator import StatisticsCalculator

__all__ = [
    "MetricsCollector",
    "MetricsCollectorInterface",
    "MetricsStorageInterface",
    "HealthCheckerInterface",
    "AlertManagerInterface",
    "StatisticsCalculatorInterface",
    "MonitoringPlugin",
    "MetricsStorage",
    "HealthChecker",
    "AlertManager",
    "StatisticsCalculator",
    "get_global_collector",
    "record_batch_metric",
    "record_lock_metric",
]
