"""
Logger helpers package.

This module provides comprehensive logging functionality for Smartify,
including SOLID architecture with separated responsibilities for logger creation,
device logging, entity logging, and standardized formatting.

All components follow SOLID principles with proper abstraction and separation of concerns.
"""

from .device_logger import DeviceLogger, EntityLogger
from .logger import (
    get_device_logger,
    get_entity_logger,
    get_logger,
    get_solid_logger,
    log_device_evaluation,
    log_entity_inspection,
)
from .logger_impl import LoggerFactory, LoggerImpl
from .logger_interface import (
    DeviceLoggerInterface,
    EntityLoggerInterface,
    LoggerFactoryInterface,
    LoggerInterface,
)
from .logger_plugin import LoggerPlugin

__all__ = [
    "get_logger",
    "log_device_evaluation",
    "log_entity_inspection",
    "get_solid_logger",
    "get_device_logger",
    "get_entity_logger",
    "DeviceLogger",
    "EntityLogger",
    "LoggerImpl",
    "LoggerFactory",
    "LoggerInterface",
    "LoggerFactoryInterface",
    "DeviceLoggerInterface",
    "EntityLoggerInterface",
    "LoggerPlugin",
]
