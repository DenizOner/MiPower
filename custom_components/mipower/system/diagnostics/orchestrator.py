"""
Diagnostics Orchestrator - Composition Pattern

This module implements the main diagnostics orchestrator following SOLID principles,
coordinating all diagnostics collectors using composition pattern.
"""

import logging
from typing import Any, Dict

from homeassistant.config_entries import ConfigEntry  # type: ignore[import]
from homeassistant.core import HomeAssistant  # type: ignore[import]

from .architecture_collector import ArchitectureDiagnosticsCollector
from .calibration_collector import CalibrationDiagnosticsCollector
from .config_collector import ConfigurationDiagnosticsCollector
from .entity_collector import EntityDiagnosticsCollector
from .interface import DiagnosticsCollectorInterface

_LOGGER = logging.getLogger(__name__)


class DiagnosticsOrchestrator(DiagnosticsCollectorInterface):
    """Main diagnostics orchestrator using composition pattern.

    This class coordinates all diagnostics collectors using the composition pattern
    from SOLID principles. Each collector has a single responsibility, and this
    orchestrator combines them to provide comprehensive diagnostics.
    """

    def __init__(self):
        """Initialize the diagnostics orchestrator with all collectors."""
        _LOGGER.debug("DiagnosticsOrchestrator initialized with SOLID collectors")

        # Initialize all collectors using composition
        self._config_collector = ConfigurationDiagnosticsCollector()
        self._architecture_collector = ArchitectureDiagnosticsCollector()
        self._entity_collector = EntityDiagnosticsCollector()
        self._calibration_collector = CalibrationDiagnosticsCollector()

    async def collect_diagnostics(
        self, hass: HomeAssistant, entry: ConfigEntry
    ) -> Dict[str, Any]:
        """Collect comprehensive diagnostics using all collectors.

        Orchestrates the collection of diagnostics from all specialized collectors,
        combining their results into a comprehensive diagnostic report.

        Args:
            hass: Home Assistant instance.
            entry: Configuration entry to analyze.

        Returns:
            Dictionary containing comprehensive diagnostic information.
        """
        diagnostics_data = {}
        try:
            _LOGGER.info(
                "Starting comprehensive diagnostics collection for '%s' (Entry ID: %s)",
                entry.title,
                entry.entry_id,
            )

            # Collect configuration diagnostics
            try:
                diagnostics_data["entry"] = (
                    self._config_collector.collect_config_diagnostics(entry)
                )
                _LOGGER.debug("Configuration diagnostics collected")
            except Exception as e:
                _LOGGER.error(
                    "Error collecting configuration diagnostics: %s",
                    e,
                    exc_info=True,
                )
                diagnostics_data["entry"] = {
                    "error": "Failed to collect configuration diagnostics"
                }

            # Collect architecture diagnostics
            try:
                diagnostics_data["architecture"] = (
                    self._architecture_collector.collect_architecture_diagnostics(
                        hass, entry
                    )
                )
                _LOGGER.debug("Architecture diagnostics collected")
            except Exception as e:
                _LOGGER.error(
                    "Error collecting architecture diagnostics: %s",
                    e,
                    exc_info=True,
                )
                diagnostics_data["architecture"] = {
                    "error": "Failed to collect architecture diagnostics"
                }

            # Collect entity diagnostics
            try:
                diagnostics_data[
                    "entities"
                ] = await self._entity_collector.collect_entity_diagnostics(hass, entry)
                _LOGGER.debug(
                    "Entity diagnostics collected (%d entities)",
                    len(diagnostics_data["entities"]),
                )
            except Exception as e:
                _LOGGER.error(
                    "Error collecting entity diagnostics: %s",
                    e,
                    exc_info=True,
                )
                diagnostics_data["entities"] = [
                    {"error": "Failed to collect entity diagnostics"}
                ]

            # Collect calibration diagnostics
            try:
                diagnostics_data[
                    "calibration"
                ] = await self._calibration_collector.collect_calibration_diagnostics(
                    entry
                )
                _LOGGER.debug("Calibration diagnostics collected")
            except Exception as e:
                _LOGGER.error(
                    "Error collecting calibration diagnostics: %s",
                    e,
                    exc_info=True,
                )
                diagnostics_data["calibration"] = {
                    "error": "Failed to collect calibration diagnostics"
                }

            _LOGGER.info(
                "Comprehensive diagnostics completed for '%s'. Contains %d sections.",
                entry.title,
                len(diagnostics_data),
            )

            return diagnostics_data

        except Exception as e:
            _LOGGER.error(
                "Critical error in diagnostics orchestrator for '%s': %s. Returning partial data.",
                getattr(
                    entry,
                    "title",
                    "Unknown",
                ),
                e,
                exc_info=True,
            )
            return {
                "error": "Critical diagnostics failure",
                "error_details": str(e),
                "partial_data": (
                    diagnostics_data if "diagnostics_data" in locals() else {}
                ),
            }
