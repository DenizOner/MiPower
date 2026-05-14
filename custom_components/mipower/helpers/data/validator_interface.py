"""Smartify helpers data validator interface module.

This module defines the interface for data validation functionality.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class DataValidatorInterface(ABC):
    """Abstract interface for data validation functionality."""

    @abstractmethod
    def validate_data(self, data: Dict[str, Any]) -> Any:
        """Validate data against the schema.

        Args:
            data: The data dictionary to validate.

        Returns:
            ValidationResult containing validation status and details.
        """
        pass

    @abstractmethod
    def clear_cache(self) -> None:
        """Clear the validation cache."""
        pass

    @abstractmethod
    def get_cache_stats(self) -> Dict[str, int]:
        """Get statistics about the validation cache.

        Returns:
            Dictionary with cache statistics.
        """
        pass

    @abstractmethod
    def get_schema_summary(self) -> Dict[str, Any]:
        """Get a summary of the validation schema.

        Returns:
            Dictionary with schema information and cache stats.
        """
        pass
