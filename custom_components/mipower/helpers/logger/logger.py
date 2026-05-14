"""
Smartify helpers common logger module - SOLID Refactored Implementation.

This module provides logging utilities following SOLID principles,
using composition pattern with separated responsibilities for logger creation,
device logging, and entity logging.
"""

import logging

from .device_logger import DeviceLogger, EntityLogger
from .logger_impl import LoggerFactory
from .logger_interface import LoggerInterface

# Global logger factory instance
_logger_factory = LoggerFactory()


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for the specified name with proper configuration.

    This function maintains backward compatibility while using SOLID architecture.

    Args:
        name: The name to append to the 'smartify' namespace for the logger.

    Returns:
        logging.Logger: A configured logger instance.
    """
    logger = logging.getLogger(f"smartify.{name}")
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    return logger


def get_solid_logger(name: str) -> LoggerInterface:
    """Get a SOLID logger instance for the specified name.

    Returns a logger interface implementation following SOLID principles.

    Args:
        name: The name to append to the namespace.

    Returns:
        LoggerInterface: A configured logger interface instance.
    """
    return _logger_factory.get_logger(name)


def get_device_logger(name: str = "device") -> DeviceLogger:
    """Get a device logger instance with standardized formatting.

    Args:
        name: The logger name to use.

    Returns:
        DeviceLogger: A configured device logger instance.
    """
    logger = get_solid_logger(name)
    return DeviceLogger(logger)


def get_entity_logger(name: str = "entity") -> EntityLogger:
    """Get an entity logger instance with standardized formatting.

    Args:
        name: The logger name to use.

    Returns:
        EntityLogger: A configured entity logger instance.
    """
    logger = get_solid_logger(name)
    return EntityLogger(logger)


def log_device_evaluation(
    logger: logging.Logger,
    device_name: str,
    device_id: str,
    success: bool,
    reason: str = "",
) -> None:
    """Log device evaluation results with standardized formatting.

    This function maintains backward compatibility. For new code,
    consider using DeviceLogger class instead.

    Args:
        logger: The logger instance to use for logging.
        device_name: Name of the device being evaluated.
        device_id: Unique identifier of the device.
        success: Whether the evaluation was successful.
        reason: Optional reason for the evaluation result.
    """
    status = "[V] SUCCESS" if success else "[X] SKIPPED"
    message = f"{status}: Device '{device_name}' (ID: {device_id})"
    if reason:
        message += f" - {reason}"
    logger.debug(message)


def log_entity_inspection(
    logger: logging.Logger,
    entity_id: str,
    criterion: str,
    passed: bool,
    details: str = "",
) -> None:
    """Log entity inspection results with standardized formatting.

    This function maintains backward compatibility. For new code,
    consider using EntityLogger class instead.

    Args:
        logger: The logger instance to use for logging.
        entity_id: The entity ID being inspected.
        criterion: The inspection criterion or test name.
        passed: Whether the entity passed the inspection.
        details: Optional additional details about the inspection result.
    """
    status = "OK" if passed else "FAILED"
    message = f"[Entity: {entity_id}] {criterion} -> {status}"
    if details:
        message += f": {details}"
    logger.debug(message)
