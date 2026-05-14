"""
Crypto Provider Implementation - SOLID Implementation of Cryptographic Operations

This module implements the crypto provider following SOLID principles.
"""

import logging
import secrets

from .security_interfaces import CryptoProviderInterface

_LOGGER = logging.getLogger(__name__)


class CryptoProvider(CryptoProviderInterface):
    """Handles cryptographic operations.

    This class implements CryptoProviderInterface and provides
    secure token generation and fingerprint validation functionality.
    """

    def __init__(self):
        """Initialize the crypto provider."""
        pass

    def generate_token(self, length: int = 32) -> str:
        """Generate a cryptographically secure token.

        Args:
            length: Token length in bytes

        Returns:
            str: Secure token string
        """
        try:
            # Ensure reasonable length limits
            if length < 16:
                _LOGGER.warning(
                    f"Token length {length} below recommended minimum, using 16"
                )
                length = 16
            if length > 128:
                _LOGGER.warning(
                    f"Token length {length} above recommended maximum, using 128"
                )
                length = 128

            # Use secrets module for cryptographically secure random generation
            token = secrets.token_urlsafe(length)
            _LOGGER.debug(f"Generated secure token of length {len(token)}")
            return token

        except Exception as e:
            _LOGGER.error(
                f"Failed to generate secure token: {e}",
                exc_info=True,
            )
            # Fallback to less secure method
            import random
            import string

            characters = string.ascii_letters + string.digits
            fallback_token = "".join(random.choice(characters) for _ in range(length))
            _LOGGER.warning("Using fallback token generation method")
            return fallback_token

    def validate_fingerprint(self, fingerprint: str) -> bool:
        """Validate a cryptographic fingerprint.

        Args:
            fingerprint: Fingerprint to validate

        Returns:
            bool: True if valid format
        """
        try:
            import re

            # Basic validation for common fingerprint formats
            # SHA-256 (64 hex chars)
            if re.match(r"^[a-fA-F0-9]{64}$", fingerprint):
                return True
            # SHA-1 (40 hex chars)
            if re.match(r"^[a-fA-F0-9]{40}$", fingerprint):
                return True
            # MD5 (32 hex chars) - legacy but still used
            if re.match(r"^[a-fA-F0-9]{32}$", fingerprint):
                return True

            _LOGGER.warning(f"Invalid fingerprint format: {fingerprint[:16]}...")
            return False

        except Exception as e:
            _LOGGER.error(
                f"Error validating fingerprint: {e}",
                exc_info=True,
            )
            return False
