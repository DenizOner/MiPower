"""
Device Logger - Single Responsibility Principle

This module implements device evaluation logging following SOLID principles,
providing specialized logging for device evaluation operations.
"""

from .logger_interface import DeviceLoggerInterface, LoggerInterface


class DeviceLogger(DeviceLoggerInterface):
    """Handles device evaluation logging with standardized formatting.

    This class is responsible for logging device evaluation results,
    providing consistent formatting and visual indicators for success/failure.
    Follows Single Responsibility Principle by focusing only on device logging.
    """

    def __init__(self, logger: LoggerInterface):
        """Initialize the device logger.

        Args:
            logger: The logger interface to use for logging.
        """
        self._logger = logger

    def log_device_evaluation(
        self,
        device_name: str,
        device_id: str,
        success: bool,
        reason: str = "",
    ) -> None:
        """Log device evaluation results with standardized formatting.

        Logs device evaluation outcomes with visual indicators for success/skipping,
        including optional reason details.

        Args:
            device_name: Name of the device being evaluated.
            device_id: Unique identifier of the device.
            success: Whether the evaluation was successful.
            reason: Optional reason for the evaluation result.
        """
        status = "[V] SUCCESS" if success else "[X] SKIPPED"
        message = f"{status}: Device '{device_name}' (ID: {device_id})"
        if reason:
            message += f" - {reason}"
        self._logger.debug(message)


class EntityLogger(DeviceLoggerInterface):
    """Handles entity inspection logging with standardized formatting.

    Note: This class implements DeviceLoggerInterface for backward compatibility,
    but handles entity-specific logging. Consider renaming or refactoring
    interface hierarchy in future versions.
    """

    def __init__(self, logger: LoggerInterface):
        """Initialize the entity logger.

        Args:
            logger: The logger interface to use for logging.
        """
        self._logger = logger

    def log_device_evaluation(
        self,
        device_name: str,
        device_id: str,
        success: bool,
        reason: str = "",
    ) -> None:
        """Log entity inspection results with standardized formatting.

        This method maps entity inspection to device evaluation logging
        for interface compatibility.

        Args:
            device_name: Entity ID being inspected (used as device_name).
            device_id: Entity ID again for consistency.
            success: Whether the inspection passed.
            reason: Optional details about the inspection result.
        """
        status = "OK" if success else "FAILED"
        message = f"[Entity: {device_name}] Inspection -> {status}"
        if reason:
            message += f": {reason}"
        self._logger.debug(message)
