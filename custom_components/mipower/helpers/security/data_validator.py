"""
Data Validator Implementation - SOLID Implementation of Data Validation

This module implements the data validator following SOLID principles.
"""

import logging
import re
from typing import Any, Dict, List

from .security_interfaces import DataValidatorInterface

_LOGGER = logging.getLogger(__name__)


class DataValidator(DataValidatorInterface):
    """Handles data validation and sanitization.

    This class implements DataValidatorInterface and provides
    comprehensive data validation and sanitization functionality.
    """

    def __init__(self):
        """Initialize the data validator."""
        # Suspicious keywords to monitor
        self.suspicious_keywords = [
            "script",
            "eval",
            "exec",
            "import",
            "system",
            "shell",
            "bash",
            "cmd",
            "powershell",
            "os",
            "subprocess",
            "file",
            "open",
            "read",
            "write",
            "delete",
        ]

    def validate_script_name(self, script_name: str) -> bool:
        """Validate a script name.

        Args:
            script_name: Script name to validate

        Returns:
            bool: True if valid
        """
        if not isinstance(script_name, str):
            return False

        # Check for valid characters (alphanumeric, underscore, dot)
        if not re.match(r"^[a-zA-Z0-9_.]+$", script_name):
            _LOGGER.warning(f"Script name contains invalid characters: {script_name}")
            return False

        # Check for directory traversal
        if ".." in script_name or "/" in script_name or "\\" in script_name:
            _LOGGER.warning(f"Script name contains directory traversal: {script_name}")
            return False

        # Check for hidden files
        if script_name.startswith("."):
            _LOGGER.warning(f"Script name starts with dot: {script_name}")
            return False

        # Check length
        if len(script_name) > 255:
            _LOGGER.warning(f"Script name too long: {script_name}")
            return False

        return True

    def sanitize_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize data by removing dangerous content.

        Args:
            data: Raw data dictionary

        Returns:
            Dict[str, Any]: Sanitized data
        """
        sanitized = {}

        for key, value in data.items():
            if isinstance(value, str):
                original_value = value
                # Remove dangerous characters
                sanitized_value = re.sub(r'[<>"\'`;\s]', "", value)
                if original_value != sanitized_value:
                    _LOGGER.warning(
                        f"Sanitized input: '{original_value}' -> '{sanitized_value}'"
                    )
                sanitized[key] = sanitized_value
            elif isinstance(value, dict):
                sanitized[key] = self.sanitize_data(value)
            elif isinstance(value, list):
                sanitized[key] = [
                    (
                        self.sanitize_data({"item": item})["item"]
                        if isinstance(item, dict)
                        else item
                    )
                    for item in value
                ]
            else:
                sanitized[key] = value

        return sanitized

    def check_for_suspicious_patterns(self, data: Dict[str, Any]) -> List[str]:
        """Check data for suspicious patterns.

        Args:
            data: Data to check

        Returns:
            List[str]: List of suspicious patterns found
        """
        suspicious_patterns = []

        def check_value(value: Any) -> None:
            if isinstance(value, str):
                value_lower = value.lower()
                for keyword in self.suspicious_keywords:
                    if keyword in value_lower:
                        if keyword not in suspicious_patterns:
                            suspicious_patterns.append(keyword)
            elif isinstance(value, dict):
                for v in value.values():
                    check_value(v)
            elif isinstance(value, list):
                for item in value:
                    check_value(item)

        check_value(data)
        return suspicious_patterns
