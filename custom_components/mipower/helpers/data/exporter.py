"""Smartify helpers data exporter module.

This module provides data export functionality for Smartify, supporting
multiple formats (JSON, CSV, YAML) with optional compression and various
export configurations.
"""

import csv
import gzip
import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from ..errors.exceptions import DataOperationError
from .exporter_interface import DataExporterInterface

_LOGGER = logging.getLogger(__name__)


@dataclass
class ExportConfig:
    """Configuration for data export operations.

    Attributes:
        format: Export format ('json', 'csv', 'yaml').
        compression: Whether to compress the output file.
        include_state_history: Include state history in exports.
        include_performance_metrics: Include performance metrics.
        include_configuration: Include configuration data.
        include_device_info: Include device information.
        date_range: Date range for data filtering.
        max_records: Maximum number of records to export.
        output_path: Custom output path.
    """

    format: str = "json"
    compression: bool = False
    include_state_history: bool = True
    include_performance_metrics: bool = True
    include_configuration: bool = True
    include_device_info: bool = True
    date_range: Optional[tuple[datetime, datetime]] = None
    max_records: Optional[int] = None
    output_path: Optional[str] = None

    def __post_init__(self):
        """Validate the export configuration."""
        valid_formats = ["json", "csv", "yaml"]
        if self.format not in valid_formats:
            raise DataOperationError(f"Invalid export format: {self.format}")


@dataclass
class ExportResult:
    """Result of a data export operation.

    Attributes:
        success: Whether the export was successful.
        file_path: Path to the exported file.
        record_count: Number of records exported.
        file_size: Size of the exported file in bytes.
        export_time: Time taken for export in seconds.
        format: Format of the exported file.
        timestamp: When the export was performed.
        errors: List of errors encountered during export.
    """

    success: bool
    file_path: Optional[str] = None
    record_count: int = 0
    file_size: int = 0
    export_time: float = 0.0
    format: str = "json"
    timestamp: datetime = field(default_factory=datetime.now)
    errors: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the export result to a dictionary.

        Returns:
            Dictionary representation of the export result.
        """

        return {
            "success": self.success,
            "file_path": self.file_path,
            "record_count": self.record_count,
            "file_size": self.file_size,
            "export_time": round(self.export_time, 3),
            "format": self.format,
            "timestamp": self.timestamp.isoformat(),
            "errors": self.errors.copy(),
        }


class DataExporter(DataExporterInterface):
    """Data exporter for Smartify with multiple format support."""

    def __init__(self, export_dir: Path):
        """Initialize the DataExporter.

        Args:
            export_dir: Export directory path.
        """
        self.export_dir = export_dir
        self.export_dir.mkdir(parents=True, exist_ok=True)
        self._export_stats = {
            "total_exports": 0,
            "total_records": 0,
            "total_size": 0,
            "by_format": {},
            "errors": 0,
        }
        _LOGGER.debug("DataExporter initialized: export_dir=%s", self.export_dir)

    async def export_configuration(
        self,
        config_data: Dict[str, Any],
        export_config: Optional[ExportConfig] = None,
    ) -> ExportResult:
        """Export Smartify configuration data.

        Args:
            config_data: The configuration data to export.
            export_config: Optional export configuration.

        Returns:
            ExportResult with details about the export operation.
        """

        config = export_config or ExportConfig()
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"smartify_config_{timestamp}.{config.format}"
            if config.compression:
                filename += ".gz"
            filepath = self.export_dir / filename
            start_time = datetime.now()
            if config.format == "json":
                await self._export_json(config_data, filepath, config.compression)
            elif config.format == "yaml":
                await self._export_yaml(config_data, filepath, config.compression)
            else:
                raise DataOperationError(f"Unsupported export format: {config.format}")
            export_time = (datetime.now() - start_time).total_seconds()
            file_size = filepath.stat().st_size if filepath.exists() else 0
            result = ExportResult(
                success=True,
                file_path=str(filepath),
                record_count=1,
                file_size=file_size,
                export_time=export_time,
                format=config.format,
            )
            self._update_export_stats(result)
            _LOGGER.info(
                "Configuration exported successfully: %s (%d bytes, %.2fs)",
                filepath,
                file_size,
                export_time,
            )
            return result
        except Exception as e:
            _LOGGER.error(
                "Configuration export failed: %s",
                e,
                exc_info=True,
            )
            return ExportResult(success=False, errors=[str(e)], format=config.format)

    async def export_state_history(
        self, state_manager, export_config: Optional[ExportConfig] = None
    ) -> ExportResult:
        """Export Smartify state history data.

        Args:
            state_manager: The state manager to export history from.
            export_config: Optional export configuration.

        Returns:
            ExportResult with details about the export operation.
        """
        config = export_config or ExportConfig()
        try:
            history = state_manager.get_history()
            if not history:
                _LOGGER.warning("No state history to export")
                return ExportResult(
                    success=False, errors=["No state history available"]
                )
            if config.date_range:
                start_date, end_date = config.date_range
                history = [h for h in history if start_date <= h.timestamp <= end_date]
            if config.max_records:
                history = history[-config.max_records :]
            _LOGGER.debug(
                "config.date_range type: %s, value: %s",
                type(config.date_range),
                config.date_range,
            )
            export_data = {
                "export_info": {
                    "type": "state_history",
                    "export_timestamp": datetime.now().isoformat(),
                    "record_count": len(history),
                    "date_range": (
                        {
                            "start": config.date_range[0].isoformat(),
                            "end": config.date_range[1].isoformat(),
                        }
                        if config.date_range
                        else None
                    ),
                },
                "state_history": [
                    {
                        "from_state": h.from_state,
                        "to_state": h.to_state,
                        "timestamp": h.timestamp.isoformat(),
                        "reason": h.reason,
                        "power_value": h.power_value,
                    }
                    for h in history
                ],
            }
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"smartify_state_history_{timestamp}.{config.format}"
            if config.compression:
                filename += ".gz"
            filepath = self.export_dir / filename
            start_time = datetime.now()
            if config.format == "json":
                await self._export_json(export_data, filepath, config.compression)
            elif config.format == "csv":
                await self._export_csv(
                    export_data["state_history"], filepath, config.compression
                )
            else:
                raise DataOperationError(f"Unsupported export format: {config.format}")
            export_time = (datetime.now() - start_time).total_seconds()
            file_size = filepath.stat().st_size if filepath.exists() else 0
            result = ExportResult(
                success=True,
                file_path=str(filepath),
                record_count=len(history),
                file_size=file_size,
                export_time=export_time,
                format=config.format,
            )
            self._update_export_stats(result)
            _LOGGER.info(
                "State history exported successfully: %s (%d records, %d bytes, %.2fs)",
                filepath,
                len(history),
                file_size,
                export_time,
            )
            return result
        except Exception as e:
            _LOGGER.error(
                "State history export failed: %s",
                e,
                exc_info=True,
            )
            return ExportResult(success=False, errors=[str(e)], format=config.format)

    async def export_power_analysis(
        self, power_analyzer, export_config: Optional[ExportConfig] = None
    ) -> ExportResult:
        """Export power analysis data.

        Args:
            power_analyzer: The power analyzer to export data from.
            export_config: Optional export configuration.

        Returns:
            ExportResult with details about the export operation.
        """

        config = export_config or ExportConfig()
        try:
            samples = power_analyzer.get_sample_history()
            if not samples:
                _LOGGER.warning("No power analysis data to export")
                return ExportResult(
                    success=False, errors=["No power analysis data available"]
                )
            if config.max_records:
                samples = samples[-config.max_records :]
            export_data = {
                "export_info": {
                    "type": "power_analysis",
                    "export_timestamp": datetime.now().isoformat(),
                    "record_count": len(samples),
                    "power_entity_id": power_analyzer.power_entity_id,
                },
                "power_samples": [
                    {
                        "value": sample.value,
                        "timestamp": sample.timestamp.isoformat(),
                        "confidence": sample.confidence,
                        "state": sample.state,
                    }
                    for sample in samples
                ],
                "analysis_summary": power_analyzer.get_analysis_summary(),
            }
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"smartify_power_analysis_{timestamp}.{config.format}"
            if config.compression:
                filename += ".gz"
            filepath = self.export_dir / filename
            start_time = datetime.now()
            if config.format == "json":
                await self._export_json(export_data, filepath, config.compression)
            elif config.format == "csv":
                await self._export_csv(
                    export_data["power_samples"], filepath, config.compression
                )
            else:
                raise DataOperationError(f"Unsupported export format: {config.format}")
            export_time = (datetime.now() - start_time).total_seconds()
            file_size = filepath.stat().st_size if filepath.exists() else 0
            result = ExportResult(
                success=True,
                file_path=str(filepath),
                record_count=len(samples),
                file_size=file_size,
                export_time=export_time,
                format=config.format,
            )
            self._update_export_stats(result)
            _LOGGER.info(
                "Power analysis exported successfully: %s (%d samples, %d bytes, %.2fs)",
                filepath,
                len(samples),
                file_size,
                export_time,
            )
            return result
        except Exception as e:
            _LOGGER.error(
                "Power analysis export failed: %s",
                e,
                exc_info=True,
            )
            return ExportResult(success=False, errors=[str(e)], format=config.format)

    async def _export_json(
        self, data: Any, filepath: Path, compression: bool = False
    ) -> None:
        if compression:
            with gzip.open(filepath, "wt", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        else:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

    async def _export_yaml(
        self, data: Any, filepath: Path, compression: bool = False
    ) -> None:
        if compression:
            with gzip.open(filepath, "wt", encoding="utf-8") as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
        else:
            with open(filepath, "w", encoding="utf-8") as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

    async def _export_csv(
        self,
        data: List[Dict[str, Any]],
        filepath: Path,
        compression: bool = False,
    ) -> None:
        if not data:
            raise DataOperationError("No data to export as CSV")
        all_keys = set()
        for item in data:
            all_keys.update(item.keys())
        headers = sorted(list(all_keys))
        if compression:
            with gzip.open(filepath, "wt", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(data)
        else:
            with open(filepath, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(data)

    def _update_export_stats(self, result: ExportResult) -> None:
        self._export_stats["total_exports"] += 1
        self._export_stats["total_records"] += result.record_count
        self._export_stats["total_size"] += result.file_size
        format_key = result.format
        if format_key not in self._export_stats["by_format"]:
            self._export_stats["by_format"][format_key] = {
                "count": 0,
                "records": 0,
                "size": 0,
            }
        self._export_stats["by_format"][format_key]["count"] += 1
        self._export_stats["by_format"][format_key]["records"] += result.record_count
        self._export_stats["by_format"][format_key]["size"] += result.file_size
        if not result.success:
            self._export_stats["errors"] += 1

    def get_export_stats(self) -> Dict[str, Any]:
        """Get statistics about export operations.

        Returns:
            Dictionary with export statistics.
        """
        return self._export_stats.copy()

    def list_export_files(self) -> List[Dict[str, Any]]:
        """List all exported files with metadata.

        Returns:
            List of dictionaries with file information.
        """
        files = []
        try:
            for export_file in self.export_dir.glob("smartify_*"):
                if export_file.is_file():
                    stat = export_file.stat()
                    files.append(
                        {
                            "filename": export_file.name,
                            "filepath": str(export_file),
                            "size": stat.st_size,
                            "created": datetime.fromtimestamp(
                                stat.st_ctime
                            ).isoformat(),
                            "modified": datetime.fromtimestamp(
                                stat.st_mtime
                            ).isoformat(),
                        }
                    )
        except Exception as e:
            _LOGGER.error(
                "Error listing export files: %s",
                e,
                exc_info=True,
            )
        return sorted(files, key=lambda x: x["modified"], reverse=True)

    async def cleanup_old_exports(self, retention_days: int = 30) -> int:
        """Clean up old export files.

        Args:
            retention_days: Number of days to keep files.

        Returns:
            Number of files cleaned up.
        """
        cleanup_count = 0
        cutoff_date = datetime.now().timestamp() - (retention_days * 24 * 3600)
        try:
            for export_file in self.export_dir.glob("smartify_*"):
                if export_file.is_file() and export_file.stat().st_mtime < cutoff_date:
                    export_file.unlink()
                    cleanup_count += 1
            _LOGGER.info("Cleaned up %d old export files", cleanup_count)
        except Exception as e:
            _LOGGER.error(
                "Error during export cleanup: %s",
                e,
                exc_info=True,
            )
        return cleanup_count

    async def export_comprehensive_report(
        self,
        state_manager=None,
        power_analyzer=None,
        error_handler=None,
        export_config: Optional[ExportConfig] = None,
    ) -> ExportResult:
        """Export a comprehensive report with multiple data types.

        Args:
            state_manager: Optional state manager for history.
            power_analyzer: Optional power analyzer for metrics.
            error_handler: Optional error handler for reports.
            export_config: Optional export configuration.

        Returns:
            ExportResult with details about the export operation.
        """

        config = export_config or ExportConfig()
        try:
            report_data = {
                "export_info": {
                    "type": "comprehensive_report",
                    "export_timestamp": datetime.now().isoformat(),
                    "components_included": [],
                },
                "configuration": {},
                "state_history": [],
                "power_analysis": {},
                "error_history": {},
                "performance_metrics": {},
            }
            if config.include_configuration:
                report_data["components_included"].append("configuration")
            if config.include_state_history and state_manager:
                history = state_manager.get_history()
                report_data["state_history"] = [
                    {
                        "from_state": h.from_state,
                        "to_state": h.to_state,
                        "timestamp": h.timestamp.isoformat(),
                        "reason": h.reason,
                        "power_value": h.power_value,
                    }
                    for h in history
                ]
                report_data["components_included"].append("state_history")
            if config.include_performance_metrics and power_analyzer:
                report_data["power_analysis"] = power_analyzer.get_analysis_summary()
                report_data["components_included"].append("power_analysis")
            if config.include_performance_metrics and error_handler:
                report_data["error_history"] = error_handler.get_error_summary()
                report_data["components_included"].append("error_history")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"smartify_comprehensive_report_{timestamp}.{config.format}"
            if config.compression:
                filename += ".gz"
            filepath = self.export_dir / filename
            start_time = datetime.now()
            if config.format == "json":
                await self._export_json(report_data, filepath, config.compression)
            elif config.format == "yaml":
                await self._export_yaml(report_data, filepath, config.compression)
            else:
                raise DataOperationError(f"Unsupported export format: {config.format}")
            export_time = (datetime.now() - start_time).total_seconds()
            file_size = filepath.stat().st_size if filepath.exists() else 0
            result = ExportResult(
                success=True,
                file_path=str(filepath),
                record_count=len(report_data.get("state_history", [])),
                file_size=file_size,
                export_time=export_time,
                format=config.format,
            )
            self._update_export_stats(result)
            _LOGGER.info(
                "Comprehensive report exported successfully: %s (%d bytes, %.2fs)",
                filepath,
                file_size,
                export_time,
            )
            return result
        except Exception as e:
            _LOGGER.error(
                "Comprehensive report export failed: %s",
                e,
                exc_info=True,
            )
            return ExportResult(success=False, errors=[str(e)], format=config.format)

    async def cleanup(self) -> None:
        """Perform full cleanup of old export files."""
        await self.cleanup_old_exports(30)
        _LOGGER.info("DataExporter cleanup completed")
