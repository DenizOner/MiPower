"""Smartify power sampler module.

This module defines the abstraction layer for power data collection in Smartify,
implementing SOLID principles by decoupling power sampling logic from the
coordinator components. It provides standardized interfaces for collecting
power measurements with proper validation, timestamping, and confidence scoring.

Following SOLID principles:
- Single Responsibility: Power sampling logic only
- Open-Closed: Extensible through interface implementation
- Liskov Substitution: Interface implementations are interchangeable
- Interface Segregation: Focused sampling interface
- Dependency Inversion: Depends on abstractions, not concretions

The module includes:
- PowerSample: Data class representing individual power measurements with
  validation and serialization capabilities.
- PowerSampler: Abstract base class defining the contract for power data
  collection implementations.

Classes:
    PowerSample: Data container for power measurements with validation.
    PowerSampler: Abstract interface for power sampling implementations.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class PowerSample:
    """Data class representing a single power measurement sample.

    This class encapsulates power consumption data with validation,
    timestamping, and confidence scoring for reliable power monitoring.
    """

    value: float
    timestamp: datetime = field(default_factory=datetime.now)
    confidence: float = 1.0
    state: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert the sample to a dictionary representation.

        Returns:
            Dict[str, Any]: Dictionary containing rounded value, ISO timestamp,
                and confidence score.
        """
        return {
            "value": round(self.value, 2),
            "timestamp": self.timestamp.isoformat(),
            "confidence": self.confidence,
        }

    def is_valid(self) -> bool:
        """Validate the power sample data.

        Returns:
            bool: True if the sample has valid value (0-100000W) and confidence
                (0.0-1.0), False otherwise.
        """
        return 0.0 <= self.value <= 100000.0 and 0.0 <= self.confidence <= 1.0


class PowerSampler(ABC):
    """Abstract base class defining the interface for power data collection.

    This interface provides a standardized contract for implementing power
    sampling functionality, allowing different sampling strategies while
    maintaining consistent behavior across the system.
    """

    @abstractmethod
    async def collect_sample(self) -> Optional[PowerSample]:
        """Collect a single power measurement from the monitored entity.

        Returns:
            Optional[PowerSample]: A validated power sample, or None if
                collection failed.
        """

    @abstractmethod
    async def collect_multiple_samples(
        self, samples: int, interval: float
    ) -> list[PowerSample]:
        """Collect multiple power samples with timing control.

        Args:
            samples (int): Number of samples to collect.
            interval (float): Time interval in seconds between samples.

        Returns:
            list[PowerSample]: List of collected power samples. May be shorter
                than requested if some collections failed.
        """

    @abstractmethod
    async def cleanup(self) -> None:
        """Clean up resources and release any held connections."""

    @property
    @abstractmethod
    def power_entity_id(self) -> str:
        """Get the entity ID of the power sensor being monitored.

        Returns:
            str: The Home Assistant entity ID for the power sensor.
        """
