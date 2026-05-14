"""
Plugin system helpers for Smartify integration.

This package provides plugin architecture components following SOLID principles,
Pure Dependency Injection, and Facade patterns.
"""

from .calibration_plugin import CalibrationPlugin
from .diagnostics_plugin import DiagnosticsPlugin
from .plugin_interface import PluginContext, PluginInterface
from .services_plugin import ServicesPlugin

__all__ = [
    "PluginInterface",
    "PluginContext",
    "CalibrationPlugin",
    "ServicesPlugin",
    "DiagnosticsPlugin",
]
