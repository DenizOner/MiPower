"""
Security Interfaces - Dependency Inversion for Security Operations

This module defines the abstraction layer for security functionality in Smartify,
implementing Dependency Inversion Principle (DIP) by decoupling security operations
from the core components.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class DataSanitizerInterface(ABC):
    """Abstract interface for data sanitization functionality."""

    @abstractmethod
    def sanitize_service_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize service data for safe logging and processing.

        Args:
            data: Raw service data dictionary

        Returns:
            Dict[str, Any]: Sanitized data dictionary
        """
        pass


class ScriptValidatorInterface(ABC):
    """Abstract interface for script validation functionality."""

    @abstractmethod
    def validate_script_name(self, script_name: str) -> bool:
        """Validate a script name for security.

        Args:
            script_name: Script name to validate

        Returns:
            bool: True if valid and safe
        """
        pass


class ServiceAuditorInterface(ABC):
    """Abstract interface for service auditing functionality."""

    @abstractmethod
    def audit_service_call(
        self,
        service_name: str,
        data: Dict[str, Any],
        caller_info: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Audit a service call for security monitoring.

        Args:
            service_name: Name of the service being called
            data: Service call data
            caller_info: Information about the caller (optional)
        """
        pass


class RateLimitCheckerInterface(ABC):
    """Abstract interface for rate limit checking functionality."""

    @abstractmethod
    def check_rate_limit(self, service_name: str, client_id: str) -> bool:
        """Check if a service call is within rate limits.

        Args:
            service_name: Name of the service
            client_id: Client identifier

        Returns:
            bool: True if call is allowed
        """
        pass


class TokenGeneratorInterface(ABC):
    """Abstract interface for token generation functionality."""

    @abstractmethod
    def generate_secure_token(self, length: int = 32) -> str:
        """Generate a cryptographically secure token.

        Args:
            length: Token length in bytes

        Returns:
            str: Secure token string
        """
        pass


class CertificateValidatorInterface(ABC):
    """Abstract interface for certificate validation functionality."""

    @abstractmethod
    def validate_certificate_fingerprint(self, fingerprint: str) -> bool:
        """Validate a certificate fingerprint.

        Args:
            fingerprint: Certificate fingerprint string

        Returns:
            bool: True if valid format
        """
        pass


class AuditLoggerInterface(ABC):
    """Abstract interface for audit logging functionality."""

    @abstractmethod
    def log_service_call(
        self,
        service_name: str,
        data: Dict[str, Any],
        caller_info: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log a service call for audit purposes.

        Args:
            service_name: Name of the service
            data: Service call data
            caller_info: Information about the caller
        """
        pass

    @abstractmethod
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
        pass


class RateLimiterInterface(ABC):
    """Abstract interface for rate limiting functionality."""

    @abstractmethod
    def is_allowed(self, service_name: str, client_id: str) -> bool:
        """Check if a request is allowed based on rate limits.

        Args:
            service_name: Name of the service
            client_id: Client identifier

        Returns:
            bool: True if request is allowed
        """
        pass

    @abstractmethod
    def record_request(self, service_name: str, client_id: str) -> None:
        """Record a request for rate limiting purposes.

        Args:
            service_name: Name of the service
            client_id: Client identifier
        """
        pass

    @abstractmethod
    def get_remaining_calls(self, service_name: str, client_id: str) -> int:
        """Get remaining allowed calls for a client.

        Args:
            service_name: Name of the service
            client_id: Client identifier

        Returns:
            int: Number of remaining calls
        """
        pass


class DataValidatorInterface(ABC):
    """Abstract interface for data validation functionality."""

    @abstractmethod
    def validate_script_name(self, script_name: str) -> bool:
        """Validate a script name.

        Args:
            script_name: Script name to validate

        Returns:
            bool: True if valid
        """
        pass

    @abstractmethod
    def sanitize_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize data by removing dangerous content.

        Args:
            data: Raw data dictionary

        Returns:
            Dict[str, Any]: Sanitized data
        """
        pass

    @abstractmethod
    def check_for_suspicious_patterns(self, data: Dict[str, Any]) -> list[str]:
        """Check data for suspicious patterns.

        Args:
            data: Data to check

        Returns:
            List[str]: List of suspicious patterns found
        """
        pass


class CryptoProviderInterface(ABC):
    """Abstract interface for cryptographic functionality."""

    @abstractmethod
    def generate_token(self, length: int = 32) -> str:
        """Generate a cryptographically secure token.

        Args:
            length: Token length in bytes

        Returns:
            str: Secure token
        """
        pass

    @abstractmethod
    def validate_fingerprint(self, fingerprint: str) -> bool:
        """Validate a cryptographic fingerprint.

        Args:
            fingerprint: Fingerprint to validate

        Returns:
            bool: True if valid
        """
        pass


class SecurityManagerInterface(ABC):
    """Abstract interface for security management functionality."""

    @abstractmethod
    def sanitize_service_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize service data for safe logging and processing.

        Args:
            data: Raw service data dictionary

        Returns:
            Dict[str, Any]: Sanitized data dictionary
        """
        pass

    @abstractmethod
    def validate_script_name(self, script_name: str) -> bool:
        """Validate a script name for security.

        Args:
            script_name: Script name to validate

        Returns:
            bool: True if valid and safe
        """
        pass

    @abstractmethod
    def audit_service_call(
        self,
        service_name: str,
        data: Dict[str, Any],
        caller_info: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Audit a service call for security monitoring.

        Args:
            service_name: Name of the service being called
            data: Service call data
            caller_info: Information about the caller (optional)
        """
        pass

    @abstractmethod
    def check_rate_limit(self, service_name: str, client_id: str) -> bool:
        """Check if a service call is within rate limits.

        Args:
            service_name: Name of the service
            client_id: Client identifier

        Returns:
            bool: True if call is allowed
        """
        pass

    @abstractmethod
    def generate_secure_token(self, length: int = 32) -> str:
        """Generate a cryptographically secure token.

        Args:
            length: Token length in bytes

        Returns:
            str: Secure token string
        """
        pass

    @abstractmethod
    def validate_certificate_fingerprint(self, fingerprint: str) -> bool:
        """Validate a certificate fingerprint.

        Args:
            fingerprint: Certificate fingerprint string

        Returns:
            bool: True if valid format
        """
        pass

    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive security status information.

        Returns:
            Dict[str, Any]: Security status details
        """
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """Clean up security manager resources."""
        pass
