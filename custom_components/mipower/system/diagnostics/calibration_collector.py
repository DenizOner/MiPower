"""
Calibration Diagnostics Collector - Single Responsibility Principle

This module implements calibration diagnostics functionality following SOLID principles,
handling collection of calibration history and analysis for diagnostics.
"""

import logging
from typing import Any, Dict

from homeassistant.config_entries import ConfigEntry  # type: ignore[import]

from ...calibration.history import CalibrationHistory
from .interface import CalibrationDiagnosticsInterface

_LOGGER = logging.getLogger(__name__)


class CalibrationDiagnosticsCollector(CalibrationDiagnosticsInterface):
    """Handles collection of calibration diagnostics information.

    This class is responsible for gathering calibration history, trends,
    and adaptive parameters for diagnostic purposes.
    Follows Single Responsibility Principle by focusing only on calibration diagnostics.
    """

    def __init__(self):
        """Initialize the calibration diagnostics collector."""
        _LOGGER.debug("CalibrationDiagnosticsCollector initialized")

    async def collect_calibration_diagnostics(
        self, entry: ConfigEntry
    ) -> Dict[str, Any]:
        """Collect calibration diagnostics information.

        Gathers comprehensive information about calibration history,
        trends, and adaptive parameters for the configuration entry.

        Args:
            entry: Configuration entry.

        Returns:
            Dictionary containing calibration diagnostics.
        """
        try:
            _LOGGER.debug(
                "Collecting calibration diagnostics for '%s' (ID: %s)",
                entry.title,
                entry.entry_id,
            )

            # Initialize calibration history
            history = CalibrationHistory()

            # Get recent calibrations
            recent_calibrations = history.get_recent_calibrations(
                entry.entry_id, limit=5
            )

            calibration_diagnostics = {
                "recent_calibrations": recent_calibrations,
                "calibration_count": len(recent_calibrations),
            }

            # Get trend analysis
            trends = history.get_trends(entry.entry_id, days=30)
            if trends:
                calibration_diagnostics["trends"] = {
                    "analysis_period_days": trends.get("analysis_period_days"),
                    "total_calibrations": trends.get("total_calibrations"),
                    "threshold_stats": trends.get("threshold_stats"),
                    "trend_direction": trends.get("trend_direction"),
                    "last_calibration": trends.get("last_calibration"),
                    "power_stability": trends.get("power_stability", {}).get(
                        "power_stability"
                    ),
                    "recommended_recalibration_days": trends.get(
                        "recommended_recalibration_days"
                    ),
                }
            else:
                calibration_diagnostics["trends"] = None

            # Get adaptive parameters
            adaptive_params = history.get_adaptive_parameters(entry.entry_id)
            if adaptive_params:
                calibration_diagnostics["adaptive_parameters"] = adaptive_params
            else:
                calibration_diagnostics["adaptive_parameters"] = None

            # Current threshold information from options
            current_thresholds = {
                "on_threshold": entry.options.get("on_threshold"),
                "off_threshold": entry.options.get("off_threshold"),
                "power_change_threshold": entry.options.get("power_change_threshold"),
                "on_debounce_time": entry.options.get("on_debounce_time"),
                "off_debounce_time": entry.options.get("off_debounce_time"),
                "verify_delay": entry.options.get("verify_delay"),
            }
            calibration_diagnostics["current_thresholds"] = current_thresholds

            _LOGGER.debug(
                "Calibration diagnostics collected successfully for '%s'",
                entry.title,
            )

            return calibration_diagnostics

        except Exception as e:
            _LOGGER.error(
                "Error collecting calibration diagnostics for '%s': %s",
                getattr(
                    entry,
                    "title",
                    "Unknown",
                ),
                e,
                exc_info=True,
            )
            return {
                "error": "Failed to collect calibration diagnostics",
                "error_details": str(e),
            }
