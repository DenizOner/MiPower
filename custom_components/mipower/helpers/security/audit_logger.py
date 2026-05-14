"""
Audit Logger Implementation - SOLID Implementation of Audit Logging

This module implements the audit logger following SOLID principles.
"""

import logging
from typing import Any, Dict, Optional

from homeassistant.core import HomeAssistant  # type: ignore[import]

from .security_interfaces import AuditLoggerInterface

_LOGGER = logging.getLogger(__name__)


class AuditLogger(AuditLoggerInterface):
    """Handles audit logging for security events.

    This class implements AuditLoggerInterface and provides
    comprehensive audit logging functionality.
    """

    def __init__(self, hass: HomeAssistant):
        """Initialize the audit logger.

        Args:
            hass: Home Assistant instance
        """
        self.hass = hass

    def log_service_call(
        self,
        service_name: str,
        data: Dict[str, Any],
        caller_info: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log a service call for audit purposes.

        Args:
            service_name: Name of the service being called
            data: Service call data
            caller_info: Information about the caller
        """
        # Sanitize data for logging
        sanitized_data = self._sanitize_for_logging(data)

        audit_entry = {
            "event": "service_call",
            "service": service_name,
            "data": sanitized_data,
            "caller": caller_info or {},
        }

        _LOGGER.info("AUDIT: Service call - %s: %s", service_name, audit_entry)

    def log_security_event(
        self,
        event_type: str,
        details: Dict[str, Any],
        severity: str = "info",
    ) -> None:
        """Log a security-related event.

        Args:
            event_type: Type of security event
            details: Event details
            severity: Event severity level
        """
        log_method = getattr(_LOGGER, severity, _LOGGER.info)

        audit_entry = {
            "event": event_type,
            "details": details,
            "severity": severity,
        }

        log_method("AUDIT: Security event - %s: %s", event_type, audit_entry)

    def _sanitize_for_logging(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize data for safe logging.

        Args:
            data: Raw data dictionary

        Returns:
            Dict[str, Any]: Sanitized data
        """
        sanitized = {}

        for key, value in data.items():
            if (
                "password" in key.lower()
                or "token" in key.lower()
                or "secret" in key.lower()
                or "key" in key.lower()
            ):
                sanitized[key] = "***MASKED***"
            elif "entity_id" in key.lower():
                sanitized[key] = str(value)
            elif isinstance(value, (str, int, float, bool)):
                sanitized[key] = value
            elif isinstance(value, dict):
                sanitized[key] = self._sanitize_for_logging(value)
            else:
                sanitized[key] = f"<{type(value).__name__}>"

        return sanitized
