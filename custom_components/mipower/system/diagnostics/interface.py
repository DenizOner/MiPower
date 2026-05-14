"""
Diagnostics Interface - Dependency Inversion for Diagnostics

This module defines the abstraction layer for diagnostics functionality in Smartify,
implementing Dependency Inversion Principle (DIP) by decoupling diagnostics operations
from the core components.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from homeassistant.config_entries import ConfigEntry  # type: ignore[import]
from homeassistant.core import HomeAssistant  # type: ignore[import]


class DiagnosticsCollectorInterface(ABC):
    """Abstract interface for diagnostics collection functionality."""

    @abstractmethod
    async def collect_diagnostics(
        self, hass: HomeAssistant, entry: ConfigEntry
    ) -> Dict[str, Any]:
        """Collect diagnostic information.

        Args:
            hass: Home Assistant instance.
            entry: Configuration entry.

        Returns:
            Dictionary containing diagnostic information.
        """


class ConfigurationDiagnosticsInterface(ABC):
    """Abstract interface for configuration diagnostics."""

    @abstractmethod
    def collect_config_diagnostics(self, entry: ConfigEntry) -> Dict[str, Any]:
        """Collect configuration entry diagnostics.

        Args:
            entry: Configuration entry.

        Returns:
            Configuration diagnostics dictionary.
        """


class CoordinatorDiagnosticsInterface(ABC):
    """Abstract interface for coordinator diagnostics."""

    @abstractmethod
    def collect_coordinator_diagnostics(
        self, hass: HomeAssistant, entry: ConfigEntry
    ) -> Dict[str, Any]:
        """Collect coordinator diagnostics.

        Args:
            hass: Home Assistant instance.
            entry: Configuration entry.

        Returns:
            Coordinator diagnostics dictionary.
        """


class EntityDiagnosticsInterface(ABC):
    """Abstract interface for entity diagnostics."""

    @abstractmethod
    async def collect_entity_diagnostics(
        self, hass: HomeAssistant, entry: ConfigEntry
    ) -> List[Dict[str, Any]]:
        """Collect entity diagnostics.

        Args:
            hass: Home Assistant instance.
            entry: Configuration entry.

        Returns:
            List of entity diagnostics dictionaries.
        """


class CalibrationDiagnosticsInterface(ABC):
    """Abstract interface for calibration diagnostics."""

    @abstractmethod
    async def collect_calibration_diagnostics(
        self, entry: ConfigEntry
    ) -> Dict[str, Any]:
        """Collect calibration diagnostics.

        Args:
            entry: Configuration entry.

        Returns:
            Calibration diagnostics dictionary.
        """


class ArchitectureDiagnosticsInterface(ABC):
    """Abstract interface for architecture diagnostics."""

    @abstractmethod
    def collect_architecture_diagnostics(
        self, hass: HomeAssistant, entry: ConfigEntry
    ) -> Dict[str, Any]:
        """Collect architecture diagnostics.

        Args:
            hass: Home Assistant instance.
            entry: Configuration entry.

        Returns:
            Architecture diagnostics dictionary.
        """
