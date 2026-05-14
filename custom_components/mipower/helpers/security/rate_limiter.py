"""
Rate Limiter Implementation - SOLID Implementation of Rate Limiting

This module implements the rate limiter following SOLID principles.
"""

import logging
import time
from typing import Dict

from homeassistant.core import HomeAssistant  # type: ignore[import]

from .security_interfaces import RateLimiterInterface

_LOGGER = logging.getLogger(__name__)


class RateLimiter(RateLimiterInterface):
    """Handles rate limiting for service calls.

    This class implements RateLimiterInterface and provides
    configurable rate limiting functionality.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        max_calls: int = 60,
        window_seconds: int = 60,
    ):
        """Initialize the rate limiter.

        Args:
            hass: Home Assistant instance
            max_calls: Maximum calls allowed in the window
            window_seconds: Time window in seconds
        """
        self.hass = hass
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self._call_history: Dict[str, list[float]] = {}

    def is_allowed(self, service_name: str, client_id: str) -> bool:
        """Check if a request is allowed based on rate limits.

        Args:
            service_name: Name of the service
            client_id: Client identifier

        Returns:
            bool: True if request is allowed
        """
        key = f"{service_name}:{client_id}"
        current_time = time.time()

        if key not in self._call_history:
            self._call_history[key] = []

        # Clean old calls outside the window
        cutoff_time = current_time - self.window_seconds
        self._call_history[key] = [
            call_time
            for call_time in self._call_history[key]
            if call_time > cutoff_time
        ]

        # Check if under limit
        if len(self._call_history[key]) >= self.max_calls:
            return False

        return True

    def record_request(self, service_name: str, client_id: str) -> None:
        """Record a request for rate limiting purposes.

        Args:
            service_name: Name of the service
            client_id: Client identifier
        """
        key = f"{service_name}:{client_id}"
        current_time = time.time()

        if key not in self._call_history:
            self._call_history[key] = []

        self._call_history[key].append(current_time)

    def get_remaining_calls(self, service_name: str, client_id: str) -> int:
        """Get remaining allowed calls for a client.

        Args:
            service_name: Name of the service
            client_id: Client identifier

        Returns:
            int: Number of remaining calls
        """
        key = f"{service_name}:{client_id}"
        current_time = time.time()

        if key not in self._call_history:
            return self.max_calls

        # Clean old calls outside the window
        cutoff_time = current_time - self.window_seconds
        self._call_history[key] = [
            call_time
            for call_time in self._call_history[key]
            if call_time > cutoff_time
        ]

        return max(0, self.max_calls - len(self._call_history[key]))
