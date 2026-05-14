"""Smartify helpers data exporter interface module.

This module defines the interface for data export functionality.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class DataExporterInterface(ABC):
    """Abstract interface for data export functionality."""

    @abstractmethod
    async def export_configuration(
        self,
        config_data: Dict[str, Any],
        export_config: Optional[Any] = None,
    ) -> Any:
        """Export Smartify configuration data.

        Args:
            config_data: The configuration data to export.
            export_config: Optional export configuration.

        Returns:
            ExportResult with details about the export operation.
        """
        pass

    @abstractmethod
    async def export_state_history(
        self, state_manager, export_config: Optional[Any] = None
    ) -> Any:
        """Export Smartify state history data.

        Args:
            state_manager: The state manager to export history from.
            export_config: Optional export configuration.

        Returns:
            ExportResult with details about the export operation.
        """
        pass

    @abstractmethod
    async def export_power_analysis(
        self, power_analyzer, export_config: Optional[Any] = None
    ) -> Any:
        """Export power analysis data.

        Args:
            power_analyzer: The power analyzer to export data from.
            export_config: Optional export configuration.

        Returns:
            ExportResult with details about the export operation.
        """
        pass

    @abstractmethod
    async def export_comprehensive_report(
        self,
        state_manager=None,
        power_analyzer=None,
        error_handler=None,
        export_config: Optional[Any] = None,
    ) -> Any:
        """Export a comprehensive report with multiple data types.

        Args:
            state_manager: Optional state manager for history.
            power_analyzer: Optional power analyzer for metrics.
            error_handler: Optional error handler for reports.
            export_config: Optional export configuration.

        Returns:
            ExportResult with details about the export operation.
        """
        pass

    @abstractmethod
    def get_export_stats(self) -> Dict[str, Any]:
        """Get statistics about export operations.

        Returns:
            Dictionary with export statistics.
        """
        pass

    @abstractmethod
    def list_export_files(self) -> list[Dict[str, Any]]:
        """List all exported files with metadata.

        Returns:
            List of dictionaries with file information.
        """
        pass

    @abstractmethod
    async def cleanup_old_exports(self, retention_days: int = 30) -> int:
        """Clean up old export files.

        Args:
            retention_days: Number of days to keep files.

        Returns:
            Number of files cleaned up.
        """
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """Perform full cleanup of old export files."""
        pass
