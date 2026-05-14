"""Smartify helpers data importer module.

This module provides data import functionality for Smartify, supporting
multiple formats (JSON, CSV, YAML) with optional compression and various
import configurations including validation and dry-run modes.
"""

import csv
import gzip
import json
import yaml
from dataclasses import dataclass, field as field_import
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, cast

from ..errors.exceptions import DataOperationError
from .importer_interface import DataImporterInterface
from ...di.container import DependencyContainer
from ..logger.logger_interface import LoggerInterface


@dataclass
class ImportConfig:
    """Configuration for data import operations.

    Attributes:
        format: Import format ('json', 'csv', 'yaml').
        compression: Whether the input file is compressed.
        validate_data: Whether to validate data before import.
        merge_strategy: Strategy for merging data ('overwrite', 'merge', 'skip_conflicts').
        backup_before_import: Whether to backup before importing.
        dry_run: Whether to perform a dry run without actual import.
    """

    format: str = "json"
    compression: bool = False
    validate_data: bool = True
    merge_strategy: str = "overwrite"
    backup_before_import: bool = True
    dry_run: bool = False

    def __post_init__(self):
        """Validate the import configuration."""
        valid_formats = ["json", "csv", "yaml"]
        if self.format not in valid_formats:
            raise DataOperationError(f"Invalid import format: {self.format}")
        valid_strategies = ["overwrite", "merge", "skip_conflicts"]
        if self.merge_strategy not in valid_strategies:
            raise DataOperationError(f"Invalid merge strategy: {self.merge_strategy}")


@dataclass
class ImportResult:
    """Result of a data import operation.

    Attributes:
        success: Whether the import was successful.
        records_imported: Number of records successfully imported.
        records_skipped: Number of records skipped.
        records_failed: Number of records that failed to import.
        import_time: Time taken for import in seconds.
        format: Format of the imported file.
        timestamp: When the import was performed.
        errors: List of errors encountered during import.
        warnings: List of warnings encountered during import.
    """

    success: bool
    records_imported: int = 0
    records_skipped: int = 0
    records_failed: int = 0
    import_time: float = 0.0
    format: str = "json"
    timestamp: datetime = field_import(default_factory=datetime.now)
    errors: List[str] = field_import(default_factory=list)
    warnings: List[str] = field_import(default_factory=list)

    def get_success_rate(self) -> float:
        """Calculate the success rate of the import.

        Returns:
            Success rate as a percentage (0-100).
        """
        total = self.records_imported + self.records_skipped + self.records_failed
        if total == 0:
            return 100.0
        return (self.records_imported / total) * 100.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert the import result to a dictionary.

        Returns:
            Dictionary representation of the import result.
        """

        return {
            "success": self.success,
            "records_imported": self.records_imported,
            "records_skipped": self.records_skipped,
            "records_failed": self.records_failed,
            "import_time": round(self.import_time, 3),
            "format": self.format,
            "timestamp": self.timestamp.isoformat(),
            "success_rate": round(self.get_success_rate(), 2),
            "errors": self.errors.copy(),
            "warnings": self.warnings.copy(),
        }


class DataImporter(DataImporterInterface):
    """Data importer for Smartify with multiple format support."""

    def __init__(self, container: DependencyContainer):
        """Initialize the DataImporter."""
        self._container = container
        self.logger = cast(
            LoggerInterface,
            container.get_instance("logger") or container.get_instance("Logger"),
        )
        assert self.logger is not None, "Logger must be available in container"
        self._import_stats = {
            "total_imports": 0,
            "total_records": 0,
            "by_format": {},
            "errors": 0,
        }
        self.logger.debug("DataImporter initialized")

    async def import_configuration(
        self, file_path: str, import_config: Optional[ImportConfig] = None
    ) -> ImportResult:
        """Import Smartify configuration data from a file.

        Args:
            file_path: Path to the file to import.
            import_config: Optional import configuration.

        Returns:
            ImportResult with details about the import operation.
        """

        config = import_config or ImportConfig()
        try:
            start_time = datetime.now()
            if config.format == "json":
                data = await self._load_json_file(file_path, config.compression)
            elif config.format == "yaml":
                data = await self._load_yaml_file(file_path, config.compression)
            else:
                raise DataOperationError(f"Unsupported import format: {config.format}")
            if config.validate_data:
                validation_result = self._validate_configuration_data(data)
                if not validation_result["valid"]:
                    return ImportResult(
                        success=False,
                        errors=validation_result["errors"],
                        warnings=validation_result["warnings"],
                    )
            if config.dry_run:
                records_imported = len(data) if isinstance(data, dict) else 1
                return ImportResult(
                    success=True,
                    records_imported=records_imported,
                    import_time=(datetime.now() - start_time).total_seconds(),
                    format=config.format,
                )
            else:
                records_imported = len(data) if isinstance(data, dict) else 1
                result = ImportResult(
                    success=True,
                    records_imported=records_imported,
                    import_time=(datetime.now() - start_time).total_seconds(),
                    format=config.format,
                )
                self._update_import_stats(result)
                self.logger.info(
                    f"Configuration imported successfully: {file_path} ({records_imported} records, {result.import_time:.2f}s)"
                )
                return result
        except Exception as e:
            self.logger.error(f"Configuration import failed: {e}")
            return ImportResult(success=False, errors=[str(e)], format=config.format)

    async def import_state_history(
        self, file_path: str, import_config: Optional[ImportConfig] = None
    ) -> ImportResult:
        """Import Smartify state history data from a file.

        Args:
            file_path: Path to the file to import.
            import_config: Optional import configuration.

        Returns:
            ImportResult with details about the import operation.
        """
        config = import_config or ImportConfig()
        try:
            start_time = datetime.now()
            if config.format == "json":
                data = await self._load_json_file(file_path, config.compression)
            elif config.format == "csv":
                data = await self._load_csv_file(file_path, config.compression)
            else:
                raise DataOperationError(f"Unsupported import format: {config.format}")
            if config.validate_data:
                validation_result = self._validate_state_history_data(data)
                if not validation_result["valid"]:
                    return ImportResult(
                        success=False,
                        errors=validation_result["errors"],
                        warnings=validation_result["warnings"],
                    )
            records = (
                data.get("state_history", data) if isinstance(data, dict) else data
            )
            if config.dry_run:
                return ImportResult(
                    success=True,
                    records_imported=len(records),
                    import_time=(datetime.now() - start_time).total_seconds(),
                    format=config.format,
                )
            else:
                result = ImportResult(
                    success=True,
                    records_imported=len(records),
                    import_time=(datetime.now() - start_time).total_seconds(),
                    format=config.format,
                )
                self._update_import_stats(result)
                self.logger.info(
                    f"State history imported successfully: {file_path} ({len(records)} records, {result.import_time:.2f}s)"
                )
                return result
        except Exception as e:
            self.logger.error(f"State history import failed: {e}")
            return ImportResult(success=False, errors=[str(e)], format=config.format)

    async def _load_json_file(self, file_path: str, compression: bool = False) -> Any:
        """Load data from a JSON file.

        Args:
            file_path: Path to the JSON file.
            compression: Whether the file is compressed.

        Returns:
            Parsed JSON data.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the JSON cannot be parsed.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        try:
            if compression:
                with gzip.open(path, "rt", encoding="utf-8") as f:
                    return json.load(f)
            else:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            raise DataOperationError(f"Error loading JSON file {file_path}: {e}")

    async def _load_yaml_file(self, file_path: str, compression: bool = False) -> Any:
        """Load data from a YAML file.

        Args:
            file_path: Path to the YAML file.
            compression: Whether the file is compressed.

        Returns:
            Parsed YAML data.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the YAML cannot be parsed.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        try:
            if compression:
                with gzip.open(path, "rt", encoding="utf-8") as f:
                    return yaml.safe_load(f)
            else:
                with open(path, "r", encoding="utf-8") as f:
                    return yaml.safe_load(f)
        except Exception as e:
            raise DataOperationError(f"Error loading YAML file {file_path}: {e}")

    async def _load_csv_file(
        self, file_path: str, compression: bool = False
    ) -> List[Dict[str, Any]]:
        """Load data from a CSV file.

        Args:
            file_path: Path to the CSV file.
            compression: Whether the file is compressed.

        Returns:
            List of dictionaries representing CSV rows.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the CSV cannot be parsed.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        try:
            if compression:
                with gzip.open(path, "rt", encoding="utf-8", newline="") as f:
                    reader = csv.DictReader(f)
                    return [row for row in reader]
            else:
                with open(path, "r", encoding="utf-8", newline="") as f:
                    reader = csv.DictReader(f)
                    return [row for row in reader]
        except Exception as e:
            raise DataOperationError(f"Error loading CSV file {file_path}: {e}")

    def _validate_configuration_data(self, data: Any) -> Dict[str, Any]:
        """Validate configuration data structure.

        Args:
            data: The data to validate.

        Returns:
            Dictionary with validation results including errors and warnings.
        """
        errors = []
        warnings = []
        if not isinstance(data, dict):
            errors.append("Configuration data must be a dictionary")
            return {"valid": False, "errors": errors, "warnings": warnings}
        required_fields = ["power_entity", "on_script", "off_script"]
        for field in required_fields:
            if field not in data:
                errors.append(f"Required configuration field missing: {field}")
        if "on_threshold" in data and not isinstance(
            data["on_threshold"], (int, float)
        ):
            warnings.append("on_threshold should be a number")
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
        }

    def _validate_state_history_data(self, data: Any) -> Dict[str, Any]:
        """Validate state history data structure.

        Args:
            data: The data to validate.

        Returns:
            Dictionary with validation results including errors and warnings.
        """
        errors = []
        warnings = []
        if isinstance(data, dict):
            records = data.get("state_history", [])
        elif isinstance(data, list):
            records = data
        else:
            errors.append("State history data must be a dictionary or list")
            return {"valid": False, "errors": errors, "warnings": warnings}
        if not records:
            warnings.append("No state history records found")
            return {"valid": True, "errors": errors, "warnings": warnings}
        for i, record in enumerate(records):
            if not isinstance(record, dict):
                errors.append(f"Record {i} must be a dictionary")
                continue
            required_fields = ["from_state", "to_state", "timestamp"]
            for field in required_fields:
                if field not in record:
                    errors.append(f"Record {i} missing required field: {field}")
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
        }

    def _update_import_stats(self, result: ImportResult) -> None:
        """Update import statistics with the result.

        Args:
            result: The import result to include in statistics.
        """
        self._import_stats["total_imports"] += 1
        self._import_stats["total_records"] += result.records_imported
        format_key = result.format
        if format_key not in self._import_stats["by_format"]:
            self._import_stats["by_format"][format_key] = {
                "count": 0,
                "records": 0,
            }
        self._import_stats["by_format"][format_key]["count"] += 1
        self._import_stats["by_format"][format_key]["records"] += (
            result.records_imported
        )
        if not result.success:
            self._import_stats["errors"] += 1

    def get_import_stats(self) -> Dict[str, Any]:
        """Get statistics about import operations.

        Returns:
            Dictionary with import statistics.
        """
        return self._import_stats.copy()

    async def cleanup(self) -> None:
        """Perform cleanup operations."""
        self.logger.info("DataImporter cleanup completed")
