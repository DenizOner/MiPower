"""
Smartify Advanced Power Analyzer - Main Implementation

This module provides the main PowerAnalyzer class that combines all power
analysis functionality using composition pattern with specialized components.
"""

import asyncio
import logging
import statistics
import time
from collections import deque
from typing import Any, Dict, List, Optional

from homeassistant.core import HomeAssistant  # type: ignore[import]

from ...helpers.errors.exceptions import ValidationError
from ...const import SAMPLE_INTERVAL, SAMPLES
from .components.outlier_detector import OutlierDetector
from .components.sample_collector import SampleCollector
from .components.sample_validator import SampleValidator
from .components.trend_analyzer import TrendAnalyzer
from .power_analyzer_interface import PowerAnalysisResult, PowerAnalyzerInterface
from .sampler import PowerSample

_LOGGER = logging.getLogger(__name__)


class PowerAnalyzer(PowerAnalyzerInterface):
    """Advanced power analyzer combining all features and SOLID design.

    Implements comprehensive power analysis with concurrent sampling,
    batch processing, sample compression, and performance monitoring.
    Uses composition pattern with specialized components for each responsibility.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        power_entity_id: str,
        outlier_sensitivity: float = 2.0,
        trend_window_size: int = 10,
        max_sample_buffer: int = 100,
        enable_compression: bool = True,
        compression_threshold: float = 0.1,
        max_concurrent_samples: int = 10,
    ):
        """Initialize advanced power analyzer.

        Args:
            hass: Home Assistant instance.
            power_entity_id: Power sensor entity ID.
            outlier_sensitivity: Z-score threshold for outliers.
            trend_window_size: Samples for trend analysis.
            max_sample_buffer: Maximum samples to buffer.
            enable_compression: Whether to compress similar samples.
            compression_threshold: Compression similarity threshold.
            max_concurrent_samples: Maximum concurrent sampling operations.
        """
        # Input validation
        if not power_entity_id or not isinstance(power_entity_id, str):
            raise ValidationError("power_entity_id must be a non-empty string")
        if trend_window_size < 3:
            raise ValidationError("trend_window_size must be at least 3")
        if max_sample_buffer < 10:
            raise ValidationError("max_sample_buffer must be at least 10")

        # Initialize SOLID components
        self._sample_collector = SampleCollector(hass, power_entity_id)
        self._outlier_detector = OutlierDetector(outlier_sensitivity)
        self._trend_analyzer = TrendAnalyzer(trend_window_size)
        self._sample_validator = SampleValidator()

        # Core state
        self.sample_buffer: deque[PowerSample] = deque(maxlen=max_sample_buffer)
        self._lock = asyncio.Lock()
        self._semaphore = asyncio.Semaphore(max_concurrent_samples)

        # Configuration
        self._enable_compression = enable_compression
        self._compression_threshold = compression_threshold

        # Performance metrics
        self._metrics = {
            "total_samples_collected": 0,
            "analysis_count": 0,
            "cache_hit_ratio": 0.0,
            "average_analysis_time": 0.0,
            "compression_savings": 0,
        }

        _LOGGER.info(
            "PowerAnalyzer initialized for %s (compression: %s, concurrent: %d)",
            power_entity_id,
            enable_compression,
            max_concurrent_samples,
        )

    async def collect_sample(self) -> Optional[PowerSample]:
        """Collect single power sample using SampleCollector.

        Returns:
            Optional[PowerSample]: Collected sample or None if failed.
        """
        async with self._semaphore:
            sample = await self._sample_collector.collect_sample()
            if sample:
                self._metrics["total_samples_collected"] += 1
            return sample

    async def collect_and_analyze(
        self,
        samples: int = SAMPLES["default"],
        interval: float = SAMPLE_INTERVAL["default"],
        validate_samples: bool = True,
        use_concurrent: bool = True,
        reset_history: bool = False,
    ) -> PowerAnalysisResult:
        """Collect samples and perform comprehensive analysis.

        Supports both sequential and concurrent sampling modes.

        Args:
            samples: Number of samples to collect (1-1000).
            interval: Time interval between samples in seconds (0.1-60).
            validate_samples: Whether to validate samples for outliers.
            use_concurrent: Whether to use concurrent sampling.
            reset_history: Whether to clear outlier/trend history before analysis.

        Returns:
            PowerAnalysisResult: Comprehensive analysis results.
        """
        # Input validation
        if not (1 <= samples <= 1000):
            raise ValidationError("samples must be between 1 and 1000")
        if not (0.1 <= interval <= 60):
            raise ValidationError("interval must be between 0.1 and 60 seconds")

        async with self._lock:
            if reset_history:
                _LOGGER.debug("Resetting analyzer history for fresh analysis")
                self._outlier_detector.reset_history()
                self._trend_analyzer.power_history.clear()

            start_time = time.time()

            _LOGGER.debug(
                "Starting power analysis: %d samples, %.1fs interval, concurrent=%s",
                samples,
                interval,
                use_concurrent,
            )

            if use_concurrent and samples > 1:
                result = await self._collect_and_analyze_concurrent(
                    samples, interval, validate_samples
                )
            else:
                result = await self._collect_and_analyze_sequential(
                    samples, interval, validate_samples
                )

            # Update metrics
            self._metrics["analysis_count"] += 1
            analysis_time = time.time() - start_time
            self._metrics["average_analysis_time"] = (
                (
                    self._metrics["average_analysis_time"]
                    * (self._metrics["analysis_count"] - 1)
                )
                + analysis_time
            ) / self._metrics["analysis_count"]

            _LOGGER.info(
                "Analysis complete in %.2fs: %.2fW avg, %s trend, %d anomalies",
                analysis_time,
                result.average_power,
                result.trend,
                result.anomalies_detected,
            )

            return result

    async def _collect_and_analyze_sequential(
        self, samples: int, interval: float, validate_samples: bool
    ) -> PowerAnalysisResult:
        """Collect samples sequentially and analyze."""
        collected_samples = []
        valid_samples = []

        for i in range(samples):
            sample = await self.collect_sample()
            if sample:
                collected_samples.append(sample)
                self._outlier_detector.add_sample(sample.value)
                self._trend_analyzer.add_sample(sample.value)

                if not validate_samples or self._sample_validator.validate_sample(
                    sample, self._outlier_detector
                ):
                    valid_samples.append(sample)
                    self._add_to_buffer(sample)
                else:
                    _LOGGER.debug("Sample %d/%d excluded as outlier", i + 1, samples)

            if i < samples - 1:
                await asyncio.sleep(interval)

        return self._process_analysis_results(collected_samples, valid_samples)

    async def _collect_and_analyze_concurrent(
        self, samples: int, interval: float, validate_samples: bool
    ) -> PowerAnalysisResult:
        """Collect samples concurrently for better performance."""
        _LOGGER.debug("Using concurrent sampling mode")

        # Create concurrent sampling tasks
        tasks = []
        for i in range(samples):
            task = asyncio.create_task(
                self._collect_sample_with_timing(i, interval, validate_samples)
            )
            tasks.append(task)

        # Wait for all samples to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        collected_samples = []
        valid_samples = []

        for result in results:
            if isinstance(result, Exception):
                _LOGGER.error("Concurrent sampling error: %s", result)
                continue

            if result and isinstance(result, PowerSample):
                collected_samples.append(result)
                self._outlier_detector.add_sample(result.value)
                self._trend_analyzer.add_sample(result.value)

                if not validate_samples or self._sample_validator.validate_sample(
                    result, self._outlier_detector
                ):
                    valid_samples.append(result)
                    self._add_to_buffer(result)

        return self._process_analysis_results(collected_samples, valid_samples)

    async def _collect_sample_with_timing(
        self, sample_index: int, base_interval: float, validate_samples: bool
    ) -> Optional[PowerSample]:
        """Collect sample with timing offset for concurrent execution."""
        if sample_index > 0:
            await asyncio.sleep(base_interval * sample_index)

        return await self.collect_sample()

    def _add_to_buffer(self, sample: PowerSample) -> None:
        """Add sample to buffer with optional compression."""
        if self._enable_compression and len(self.sample_buffer) > 0:
            last_sample = self.sample_buffer[-1]
            if (
                abs(sample.value - last_sample.value) / max(last_sample.value, 0.1)
                < self._compression_threshold
            ):
                self._metrics["compression_savings"] += 1
                return  # Skip adding similar sample

        self.sample_buffer.append(sample)

    def _process_analysis_results(
        self, collected_samples: List[PowerSample], valid_samples: List[PowerSample]
    ) -> PowerAnalysisResult:
        """Process collected samples and return analysis results."""
        if len(valid_samples) < 2:
            if collected_samples:
                # Fallback: use collected samples if validation too strict
                fallback_values = [s.value for s in collected_samples]
                fallback_avg = statistics.mean(fallback_values)
                _LOGGER.warning(
                    "Insufficient valid samples (%d), using fallback average %.2fW",
                    len(valid_samples),
                    fallback_avg,
                )
                return PowerAnalysisResult(
                    average_power=fallback_avg,
                    sample_count=len(collected_samples),
                    confidence=0.1,
                    trend="insufficient_data",
                    anomalies_detected=len(collected_samples) - len(valid_samples),
                )
            else:
                _LOGGER.debug("No samples collected for analysis")
                return PowerAnalysisResult(
                    average_power=0.0,
                    sample_count=0,
                    confidence=0.0,
                    trend="insufficient_data",
                    anomalies_detected=0,
                )

        power_values = [sample.value for sample in valid_samples]
        avg_power = statistics.mean(power_values)

        try:
            stdev_power = statistics.stdev(power_values)
            confidence = max(0.1, 1.0 - (stdev_power / max(avg_power, 1.0)))
        except statistics.StatisticsError:
            confidence = 0.5

        trend = self._trend_analyzer.analyze_trend()
        anomalies = len(collected_samples) - len(valid_samples)

        return PowerAnalysisResult(
            average_power=avg_power,
            sample_count=len(valid_samples),
            confidence=confidence,
            trend=trend,
            anomalies_detected=anomalies,
        )

    def get_sample_history(self, limit: Optional[int] = None) -> List[PowerSample]:
        """Get historical power samples from buffer.

        Args:
            limit: Maximum number of samples to return.

        Returns:
            List[PowerSample]: Historical samples.
        """
        try:
            samples = list(self.sample_buffer)
            if limit:
                return samples[-limit:]
            return samples
        except Exception as e:
            _LOGGER.error("Error getting sample history: %s", e, exc_info=True)
            return []

    def get_analysis_summary(self) -> Dict[str, Any]:
        """Get comprehensive analyzer state summary.

        Returns:
            Dict[str, Any]: Summary with thresholds, trends, and metrics.
        """
        try:
            return {
                "power_entity_id": self._sample_collector.power_entity_id,
                "sample_buffer_size": len(self.sample_buffer),
                "compression_enabled": self._enable_compression,
                "compression_savings": self._metrics["compression_savings"],
                "outlier_thresholds": self._outlier_detector.get_thresholds(),
                "trend_analysis": {
                    "current_trend": self._trend_analyzer.analyze_trend(),
                    "trend_strength": self._trend_analyzer.get_trend_strength(),
                    "history_size": len(self._trend_analyzer.power_history),
                },
                "performance_metrics": self._metrics.copy(),
            }
        except Exception as e:
            _LOGGER.error("Error getting analysis summary: %s", e, exc_info=True)
            return {
                "power_entity_id": getattr(
                    self._sample_collector, "power_entity_id", "unknown"
                ),
                "sample_buffer_size": 0,
                "compression_enabled": self._enable_compression,
                "error": str(e),
            }

    async def cleanup(self) -> None:
        """Clean up analyzer resources and clear all buffers."""
        try:
            async with self._lock:
                self.sample_buffer.clear()
                self._outlier_detector.reset_history()
                self._trend_analyzer.power_history.clear()

                # Reset metrics except totals
                self._metrics["cache_hit_ratio"] = 0.0
                self._metrics["average_analysis_time"] = 0.0

            entity_id = self._sample_collector.power_entity_id
            _LOGGER.info("PowerAnalyzer cleanup completed for %s", entity_id)
        except Exception as e:
            entity_id = getattr(self._sample_collector, "power_entity_id", "unknown")
            _LOGGER.error(
                "Error during PowerAnalyzer cleanup for %s: %s",
                entity_id,
                e,
                exc_info=True,
            )
