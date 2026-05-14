"""
Diagnostics Package.

This module provides comprehensive diagnostics functionality following SOLID principles,
supporting system health monitoring, configuration analysis, and performance diagnostics.

All components follow SOLID principles with proper abstraction and separation of concerns.
"""

from .architecture_collector import ArchitectureDiagnosticsCollector
from .calibration_collector import CalibrationDiagnosticsCollector
from .config_collector import ConfigurationDiagnosticsCollector
from .diagnostics_plugin import DiagnosticsPlugin
from .entity_collector import EntityDiagnosticsCollector
from .interface import (
    ArchitectureDiagnosticsInterface,
    CalibrationDiagnosticsInterface,
    ConfigurationDiagnosticsInterface,
    CoordinatorDiagnosticsInterface,
    DiagnosticsCollectorInterface,
    EntityDiagnosticsInterface,
)
from .orchestrator import DiagnosticsOrchestrator

__all__ = [
    "DiagnosticsOrchestrator",
    "DiagnosticsCollectorInterface",
    "ConfigurationDiagnosticsInterface",
    "CoordinatorDiagnosticsInterface",
    "EntityDiagnosticsInterface",
    "CalibrationDiagnosticsInterface",
    "ArchitectureDiagnosticsInterface",
    "ConfigurationDiagnosticsCollector",
    "EntityDiagnosticsCollector",
    "CalibrationDiagnosticsCollector",
    "ArchitectureDiagnosticsCollector",
    "DiagnosticsPlugin",
]
