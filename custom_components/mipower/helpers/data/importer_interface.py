"""Smartify helpers data importer interface module.

This module defines the interface for data import functionality.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class DataImporterInterface(ABC):
    """Abstract interface for data import functionality."""

    @abstractmethod
    async def import_configuration(
        self, file_path: str, import_config: Optional[Any] = None
    ) -> Any:
        """Import Smartify configuration data from a file.

        Args:
            file_path: Path to the file to import.
            import_config: Optional import configuration.

        Returns:
            ImportResult with details about the import operation.
        """
        pass

    @abstractmethod
    async def import_state_history(
        self, file_path: str, import_config: Optional[Any] = None
    ) -> Any:
        """Import Smartify state history data from a file.

        Args:
            file_path: Path to the file to import.
            import_config: Optional import configuration.

        Returns:
            ImportResult with details about the import operation.
        """
        pass

    @abstractmethod
    def get_import_stats(self) -> Dict[str, Any]:
        """Get statistics about import operations.

        Returns:
            Dictionary with import statistics.
        """
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """Perform cleanup operations."""
        pass
