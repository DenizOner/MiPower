"""
Power Analyzer Interface - Dependency Inversion for Power Analysis

This module defines the abstraction layer for power analysis functionality in Smartify,
implementing Dependency Inversion Principle (DIP) by decoupling power analysis operations
from the coordinator and other high-level components.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from .sampler import PowerSample


@dataclass
class PowerAnalysisResult:
    """Data container for power analysis results.

    Attributes:
        average_power: Average power consumption in watts.
        sample_count: Number of samples used in analysis.
        confidence: Confidence level of the analysis (0.0 to 1.0).
        trend: Current power consumption trend.
        anomalies_detected: Number of anomalous readings detected.
        analysis_timestamp: When the analysis was performed.
    """

    average_power: float
    sample_count: int
    confidence: float
    trend: str
    anomalies_detected: int
    analysis_timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the analysis result to a dictionary.

        Returns:
            Dict[str, Any]: Dictionary representation of the analysis result.
        """
        return {
            "average_power": round(self.average_power, 2),
            "sample_count": self.sample_count,
            "confidence": round(self.confidence, 3),
            "trend": self.trend,
            "anomalies_detected": self.anomalies_detected,
            "analysis_timestamp": self.analysis_timestamp.isoformat(),
        }


class OutlierDetectorInterface(ABC):
    """Abstract interface for outlier detection functionality."""

    @abstractmethod
    def add_sample(self, value: float) -> None:
        """Add a power value to the sample history.

        Args:
            value: Power consumption value to add.
        """

    @abstractmethod
    def is_outlier(self, value: float) -> bool:
        """Check if a value is an outlier.

        Args:
            value: Value to check for outlier status.

        Returns:
            True if the value is an outlier, False otherwise.
        """

    @abstractmethod
    def get_thresholds(self) -> Dict[str, float]:
        """Get the current outlier detection thresholds.

        Returns:
            Dictionary with threshold information.
        """

    @abstractmethod
    def reset_history(self) -> None:
        """Reset the sample history."""


class TrendAnalyzerInterface(ABC):
    """Abstract interface for trend analysis functionality."""

    @abstractmethod
    def add_sample(self, power_value: float) -> None:
        """Add a power value to the trend analysis history.

        Args:
            power_value: Power consumption value to add.
        """

    @abstractmethod
    def analyze_trend(self) -> str:
        """Analyze the current power consumption trend.

        Returns:
            Trend description string.
        """

    @abstractmethod
    def get_trend_strength(self) -> float:
        """Get the strength of the current trend.

        Returns:
            Trend strength normalized to 0.0-1.0 range.
        """


class SampleCollectorInterface(ABC):
    """Abstract interface for power sample collection."""

    @abstractmethod
    async def collect_sample(self) -> Optional[PowerSample]:
        """Collect a single power sample from the sensor.

        Returns:
            The collected sample or None if collection failed.
        """


class SampleValidatorInterface(ABC):
    """Abstract interface for sample validation functionality."""

    @abstractmethod
    def validate_sample(
        self, sample: PowerSample, outlier_detector: OutlierDetectorInterface
    ) -> bool:
        """Validate a power sample.

        Args:
            sample: The sample to validate.
            outlier_detector: Detector to use for outlier checking.

        Returns:
            True if sample is valid, False otherwise.
        """


class PowerAnalyzerInterface(ABC):
    """Abstract interface for comprehensive power analysis functionality."""

    @abstractmethod
    async def collect_and_analyze(
        self,
        samples: int = 5,
        interval: float = 1.0,
        validate_samples: bool = True,
    ) -> PowerAnalysisResult:
        """Collect multiple samples and perform comprehensive analysis.

        Args:
            samples: Number of samples to collect.
            interval: Time interval between samples in seconds.
            validate_samples: Whether to validate samples for outliers.

        Returns:
            Analysis results including average power, trend, etc.
        """

    @abstractmethod
    def get_sample_history(self, limit: Optional[int] = None) -> List[PowerSample]:
        """Get the history of collected power samples.

        Args:
            limit: Maximum number of samples to return.

        Returns:
            List of power samples from history.
        """

    @abstractmethod
    def get_analysis_summary(self) -> Dict[str, Any]:
        """Get a comprehensive summary of the analyzer's current state.

        Returns:
            Summary including thresholds, trends, and statistics.
        """

    @abstractmethod
    async def cleanup(self) -> None:
        """Clean up analyzer resources and clear all buffers."""
