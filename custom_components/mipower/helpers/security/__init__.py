"""Security utilities and helpers for Smartify integration.

This module provides security-related utilities and helpers for the Smartify
Home Assistant integration, including cryptographic functions, validation,
audit logging, rate limiting, and data sanitization capabilities. It serves
as the main entry point for all security functionality used throughout the
integration to ensure secure operations and data handling.

All components follow SOLID principles with proper abstraction and separation of concerns.
"""

import logging

from .audit_logger import AuditLogger
from .crypto_provider import CryptoProvider
from .data_validator import DataValidator
from .rate_limiter import RateLimiter
from .security_interfaces import (
    AuditLoggerInterface,
    CryptoProviderInterface,
    DataValidatorInterface,
    RateLimiterInterface,
    SecurityManagerInterface,
)
from .security_manager import SecurityManager
from .security_plugin import SecurityPlugin

_LOGGER = logging.getLogger(__name__)

__all__ = [
    "SecurityManager",
    "SecurityManagerInterface",
    "AuditLoggerInterface",
    "RateLimiterInterface",
    "DataValidatorInterface",
    "CryptoProviderInterface",
    "SecurityPlugin",
    "AuditLogger",
    "RateLimiter",
    "DataValidator",
    "CryptoProvider",
    "_LOGGER",
]
