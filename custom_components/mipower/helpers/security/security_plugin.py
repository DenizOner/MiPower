"""
Security Plugin for Smartify.

This module implements the Security system as a plugin following the plugin architecture
pattern, allowing for dynamic loading and configuration-driven behavior.
"""

import logging
from typing import Any, Dict, Optional

from ..plugin.plugin_interface import PluginContext, PluginInterface

_LOGGER = logging.getLogger(__name__)


class SecurityPlugin(PluginInterface):
    """Plugin implementation for Security functionality.

    This plugin provides security capabilities with dependency injection
    and configuration-driven behavior, following SOLID principles.
    """

    def __init__(self):
        """Initialize the security plugin."""
        self._security_manager = None
        self._context: Optional[PluginContext] = None
        self._config = {}

    def get_name(self) -> str:
        """Get the unique name of this plugin."""
        return "security"

    def get_version(self) -> str:
        """Get the version of this plugin."""
        return "1.0.0"

    def get_description(self) -> str:
        """Get a human-readable description of the plugin."""
        return "Security utilities including validation, auditing, and cryptography"

    async def initialize(self, context: Dict[str, Any]) -> bool:
        """Initialize the plugin with the given context.

        Args:
            context: Initialization context containing dependencies and configuration

        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            self._context = PluginContext(
                hass=context.get("hass"),
                entry=context.get("entry"),
                container=context.get("container"),
            )
            self._config = context.get("config", {})

            # Get container from context
            container = context.get("container")
            if not container:
                _LOGGER.error(
                    "Container not provided in plugin context",
                    exc_info=True,
                )
                return False

            # Create security manager through container
            self._security_manager = container.create_security_manager()

            _LOGGER.info("Security plugin initialized successfully")
            return True

        except Exception as e:
            _LOGGER.error(
                "Failed to initialize Security plugin: %s",
                e,
                exc_info=True,
            )
            return False

    async def cleanup(self) -> None:
        """Clean up plugin resources and perform shutdown operations."""
        if self._security_manager and hasattr(self._security_manager, "cleanup"):
            try:
                await self._security_manager.cleanup()
                _LOGGER.debug("Security plugin cleaned up")
            except Exception as e:
                _LOGGER.error(
                    "Error cleaning up Security plugin: %s",
                    e,
                    exc_info=True,
                )

        self._security_manager = None
        self._context = None

    def get_capabilities(self) -> Dict[str, Any]:
        """Get the capabilities provided by this plugin.

        Returns:
            Dict[str, Any]: Dictionary of plugin capabilities
        """
        return {
            "data_validation": True,
            "audit_logging": True,
            "cryptographic_functions": True,
            "rate_limiting": True,
            "input_sanitization": True,
            "security_monitoring": True,
        }

    def is_enabled(self) -> bool:
        """Check if the plugin is currently enabled.

        Returns:
            bool: True if enabled, False otherwise
        """
        return self._config.get("enabled", True)

    def get_dependencies(self) -> list[str]:
        """Get list of plugin dependencies.

        Returns:
            list[str]: List of required plugin names
        """
        return []  # Security is independent

    def get_configuration_schema(self) -> Optional[Dict[str, Any]]:
        """Get configuration schema for this plugin.

        Returns:
            Optional[Dict[str, Any]]: Configuration schema or None if no config needed
        """
        return {
            "type": "object",
            "properties": {
                "enabled": {
                    "type": "boolean",
                    "default": True,
                    "description": "Enable security plugin",
                },
                "enable_audit_logging": {
                    "type": "boolean",
                    "default": True,
                    "description": "Enable audit logging for service calls",
                },
                "enable_rate_limiting": {
                    "type": "boolean",
                    "default": True,
                    "description": "Enable rate limiting for service calls",
                },
                "rate_limit_max_calls": {
                    "type": "integer",
                    "default": 60,
                    "minimum": 1,
                    "maximum": 1000,
                    "description": "Maximum calls per time window",
                },
                "rate_limit_window_seconds": {
                    "type": "integer",
                    "default": 60,
                    "minimum": 10,
                    "maximum": 3600,
                    "description": "Time window for rate limiting in seconds",
                },
                "enable_input_validation": {
                    "type": "boolean",
                    "default": True,
                    "description": "Enable input validation and sanitization",
                },
                "enable_cryptographic_functions": {
                    "type": "boolean",
                    "default": True,
                    "description": "Enable cryptographic token generation",
                },
                "token_length": {
                    "type": "integer",
                    "default": 32,
                    "minimum": 16,
                    "maximum": 128,
                    "description": "Default token length in bytes",
                },
                "suspicious_keywords_monitoring": {
                    "type": "boolean",
                    "default": True,
                    "description": "Monitor for suspicious keywords in service calls",
                },
            },
        }

    def get_security_manager(self):
        """Get the security manager instance.

        Returns:
            SecurityManager instance or None if not initialized
        """
        return self._security_manager

    def sanitize_service_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize service data for safe logging and processing.

        Args:
            data: Raw service data

        Returns:
            Dict[str, Any]: Sanitized data
        """
        if not self._security_manager:
            _LOGGER.warning("Security plugin not initialized, returning original data")
            return data

        return self._security_manager.sanitize_service_data(data)

    def validate_script_name(self, script_name: str) -> bool:
        """Validate a script name for security.

        Args:
            script_name: Script name to validate

        Returns:
            bool: True if valid
        """
        if not self._security_manager:
            _LOGGER.warning("Security plugin not initialized, allowing script")
            return True

        return self._security_manager.validate_script_name(script_name)

    def audit_service_call(
        self,
        service_name: str,
        data: Dict[str, Any],
        caller_info: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Audit a service call.

        Args:
            service_name: Name of the service
            data: Service call data
            caller_info: Information about the caller
        """
        if not self._security_manager:
            _LOGGER.warning("Security plugin not initialized, skipping audit")
            return

        self._security_manager.audit_service_call(service_name, data, caller_info)

    def check_rate_limit(self, service_name: str, client_id: str) -> bool:
        """Check if a service call is within rate limits.

        Args:
            service_name: Name of the service
            client_id: Client identifier

        Returns:
            bool: True if call is allowed
        """
        if not self._security_manager:
            _LOGGER.warning("Security plugin not initialized, allowing call")
            return True

        return self._security_manager.check_rate_limit(service_name, client_id)

    def generate_secure_token(self, length: Optional[int] = None) -> str:
        """Generate a cryptographically secure token.

        Args:
            length: Token length (uses default if None)

        Returns:
            str: Secure token
        """
        if not self._security_manager:
            _LOGGER.warning("Security plugin not initialized, returning empty token")
            return ""

        token_length = length or self._config.get("token_length", 32)
        return self._security_manager.generate_secure_token(token_length)

    def validate_certificate_fingerprint(self, fingerprint: str) -> bool:
        """Validate a certificate fingerprint.

        Args:
            fingerprint: Fingerprint to validate

        Returns:
            bool: True if valid
        """
        if not self._security_manager:
            _LOGGER.warning("Security plugin not initialized, rejecting fingerprint")
            return False

        return self._security_manager.validate_certificate_fingerprint(fingerprint)

    def get_security_status(self) -> Dict[str, Any]:
        """Get comprehensive security status information.

        Returns:
            Dict[str, Any]: Security status
        """
        if not self._security_manager:
            return {"error": "Security plugin not initialized"}

        return {
            "plugin_enabled": self.is_enabled(),
            "capabilities": self.get_capabilities(),
            "configuration": self._config,
            "security_features": {
                "audit_logging": self._config.get("enable_audit_logging", True),
                "rate_limiting": self._config.get("enable_rate_limiting", True),
                "input_validation": self._config.get("enable_input_validation", True),
                "cryptographic_functions": self._config.get(
                    "enable_cryptographic_functions", True
                ),
            },
            "rate_limit_settings": {
                "max_calls": self._config.get("rate_limit_max_calls", 60),
                "window_seconds": self._config.get("rate_limit_window_seconds", 60),
            },
        }
