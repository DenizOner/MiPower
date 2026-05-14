"""
Security Manager Implementation - SOLID Implementation of Security Operations

This module implements the security manager following SOLID principles,
using composition pattern with separated responsibilities.
"""

import logging
from typing import Any, Dict, Optional

from homeassistant.core import HomeAssistant  # type: ignore[import]

from .security_interfaces import (
    AuditLoggerInterface,
    CertificateValidatorInterface,
    CryptoProviderInterface,
    DataSanitizerInterface,
    DataValidatorInterface,
    RateLimitCheckerInterface,
    RateLimiterInterface,
    ScriptValidatorInterface,
    ServiceAuditorInterface,
    TokenGeneratorInterface,
)

_LOGGER = logging.getLogger(__name__)


class SecurityManager(
    DataSanitizerInterface,
    ScriptValidatorInterface,
    ServiceAuditorInterface,
    RateLimitCheckerInterface,
    TokenGeneratorInterface,
    CertificateValidatorInterface,
):
    """Manages security operations using SOLID principles.

    This class implements SecurityManagerInterface and uses composition pattern
    with separated responsibilities following SOLID principles:
    - AuditLogger for audit logging
    - RateLimiter for rate limiting
    - DataValidator for input validation
    - CryptoProvider for cryptographic operations

    Follows Single Responsibility Principle by delegating specific tasks
    to specialized components while orchestrating the overall security operations.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        audit_logger: Optional[AuditLoggerInterface] = None,
        rate_limiter: Optional[RateLimiterInterface] = None,
        data_validator: Optional[DataValidatorInterface] = None,
        crypto_provider: Optional[CryptoProviderInterface] = None,
    ):
        """Initialize the security manager with optional dependencies for testability.

        Args:
            hass: Home Assistant instance
            audit_logger: Optional audit logging component (creates default if None)
            rate_limiter: Optional rate limiting component (creates default if None)
            data_validator: Optional data validation component (creates default if None)
            crypto_provider: Optional cryptographic operations component (creates default if None)
        """
        self.hass = hass

        # Initialize components with defaults for testability
        if audit_logger is None:
            from .audit_logger import AuditLogger

            self.audit_logger = AuditLogger(hass)
        else:
            self.audit_logger = audit_logger

        if rate_limiter is None:
            from .rate_limiter import RateLimiter

            self.rate_limiter = RateLimiter(hass)
        else:
            self.rate_limiter = rate_limiter

        if data_validator is None:
            from .data_validator import DataValidator

            self.data_validator = DataValidator()
        else:
            self.data_validator = data_validator

        if crypto_provider is None:
            from .crypto_provider import CryptoProvider

            self.crypto_provider = CryptoProvider()
        else:
            self.crypto_provider = crypto_provider

        _LOGGER.debug("SecurityManager initialized with SOLID components")

    @classmethod
    def create(
        cls,
        hass: HomeAssistant,
        audit_logger: Optional[AuditLoggerInterface] = None,
        rate_limiter: Optional[RateLimiterInterface] = None,
        data_validator: Optional[DataValidatorInterface] = None,
        crypto_provider: Optional[CryptoProviderInterface] = None,
    ):
        """Factory method for creating SecurityManager instances with optional dependencies.

        This factory method enables interface mocking for testing by allowing
        injection of mock implementations for security components.

        Args:
            hass: Home Assistant instance
            audit_logger: Optional AuditLoggerInterface implementation
            rate_limiter: Optional RateLimiterInterface implementation
            data_validator: Optional DataValidatorInterface implementation
            crypto_provider: Optional CryptoProviderInterface implementation

        Returns:
            SecurityManager: Configured instance
        """
        return cls(
            hass=hass,
            audit_logger=audit_logger,
            rate_limiter=rate_limiter,
            data_validator=data_validator,
            crypto_provider=crypto_provider,
        )

    def sanitize_service_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize service data using the data validator.

        Args:
            data: Raw service data dictionary

        Returns:
            Dict[str, Any]: Sanitized data dictionary
        """
        return self.data_validator.sanitize_data(data)

    def validate_script_name(self, script_name: str) -> bool:
        """Validate a script name using the data validator.

        Args:
            script_name: Script name to validate

        Returns:
            bool: True if valid and safe
        """
        return self.data_validator.validate_script_name(script_name)

    def audit_service_call(
        self,
        service_name: str,
        data: Dict[str, Any],
        caller_info: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Audit a service call using the audit logger.

        Args:
            service_name: Name of the service being called
            data: Service call data
            caller_info: Information about the caller (optional)
        """
        self.audit_logger.log_service_call(service_name, data, caller_info)

        # Also check for suspicious patterns
        suspicious_patterns = self.data_validator.check_for_suspicious_patterns(data)
        if suspicious_patterns:
            self.audit_logger.log_security_event(
                "suspicious_service_call",
                {
                    "service_name": service_name,
                    "suspicious_patterns": suspicious_patterns,
                    "caller_info": caller_info,
                },
                "warning",
            )

    def check_rate_limit(self, service_name: str, client_id: str) -> bool:
        """Check if a service call is within rate limits.

        Args:
            service_name: Name of the service
            client_id: Client identifier

        Returns:
            bool: True if call is allowed
        """
        allowed = self.rate_limiter.is_allowed(service_name, client_id)
        if allowed:
            self.rate_limiter.record_request(service_name, client_id)
        else:
            self.audit_logger.log_security_event(
                "rate_limit_exceeded",
                {
                    "service_name": service_name,
                    "client_id": client_id,
                    "remaining_calls": self.rate_limiter.get_remaining_calls(
                        service_name, client_id
                    ),
                },
                "warning",
            )
        return allowed

    def generate_secure_token(self, length: int = 32) -> str:
        """Generate a cryptographically secure token.

        Args:
            length: Token length in bytes

        Returns:
            str: Secure token string
        """
        return self.crypto_provider.generate_token(length)

    def validate_certificate_fingerprint(self, fingerprint: str) -> bool:
        """Validate a certificate fingerprint.

        Args:
            fingerprint: Certificate fingerprint string

        Returns:
            bool: True if valid format
        """
        return self.crypto_provider.validate_fingerprint(fingerprint)

    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive security status information.

        Returns:
            Dict[str, Any]: Security status details
        """
        return {
            "security_components_initialized": True,
            "audit_logger_available": self.audit_logger is not None,
            "rate_limiter_available": self.rate_limiter is not None,
            "data_validator_available": self.data_validator is not None,
            "crypto_provider_available": self.crypto_provider is not None,
            "security_features": [
                "data_sanitization",
                "script_validation",
                "service_auditing",
                "rate_limiting",
                "token_generation",
                "certificate_validation",
            ],
        }

    async def cleanup(self) -> None:
        """Clean up security manager resources."""
        _LOGGER.debug("SecurityManager cleanup completed")


class SecurityManagerBuilder:
    """Builder for SecurityManager to handle complex dependency injection.

    This builder implements the Builder pattern to construct SecurityManager
    instances with multiple dependencies in a fluent, step-by-step manner.
    Follows SOLID principles: Single Responsibility (only builds security managers),
    Open-Closed (new steps can be added without modifying existing code).
    """

    def __init__(self) -> None:
        """Initialize builder with empty dependencies."""
        self._hass = None
        self._audit_logger = None
        self._rate_limiter = None
        self._data_validator = None
        self._crypto_provider = None

    def with_hass(self, hass):
        """Set Home Assistant instance."""
        self._hass = hass
        return self

    def with_audit_logger(self, audit_logger):
        """Set audit logger."""
        self._audit_logger = audit_logger
        return self

    def with_rate_limiter(self, rate_limiter):
        """Set rate limiter."""
        self._rate_limiter = rate_limiter
        return self

    def with_data_validator(self, data_validator):
        """Set data validator."""
        self._data_validator = data_validator
        return self

    def with_crypto_provider(self, crypto_provider):
        """Set crypto provider."""
        self._crypto_provider = crypto_provider
        return self

    def build(self):
        """Build SecurityManager instance.

        Validates that all required dependencies are provided before construction.

        Returns:
            SecurityManager: Fully configured security manager instance.

        Raises:
            ValueError: If any required dependency is missing.
        """
        required_deps = [
            self._hass,
            self._audit_logger,
            self._rate_limiter,
            self._data_validator,
            self._crypto_provider,
        ]

        if not all(required_deps):
            missing = []
            if not self._hass:
                missing.append("hass")
            if not self._audit_logger:
                missing.append("audit_logger")
            if not self._rate_limiter:
                missing.append("rate_limiter")
            if not self._data_validator:
                missing.append("data_validator")
            if not self._crypto_provider:
                missing.append("crypto_provider")
            raise ValueError(f"Missing required dependencies: {', '.join(missing)}")

        return SecurityManager(
            hass=self._hass,
            audit_logger=self._audit_logger,
            rate_limiter=self._rate_limiter,
            data_validator=self._data_validator,
            crypto_provider=self._crypto_provider,
        )
