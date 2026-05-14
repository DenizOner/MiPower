"""Power analysis helpers package.

This package provides power analysis functionality for Smartify,
including outlier detection, trend analysis, and comprehensive power monitoring.
All components follow SOLID principles with proper abstraction and separation of concerns.
"""

from .analyzer import (
    OutlierDetector,
    PowerAnalysisResult,
    PowerAnalyzer,
    PowerSample,
    SampleCollector,
    SampleValidator,
    TrendAnalyzer,
)
from .power_analyzer_interface import (
    OutlierDetectorInterface,
    PowerAnalyzerInterface,
    SampleCollectorInterface,
    SampleValidatorInterface,
    TrendAnalyzerInterface,
)

__all__ = [
    "PowerAnalyzer",
    "PowerAnalysisResult",
    "PowerAnalyzerInterface",
    "OutlierDetectorInterface",
    "TrendAnalyzerInterface",
    "SampleCollectorInterface",
    "SampleValidatorInterface",
    "OutlierDetector",
    "TrendAnalyzer",
    "SampleCollector",
    "SampleValidator",
    "PowerSample",
]
