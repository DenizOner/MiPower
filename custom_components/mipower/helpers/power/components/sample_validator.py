"""
Sample Validator Component - Sample Quality Assessment

This module implements sample validation and quality assessment for power
samples. It validates samples for statistical consistency, range checks,
and outlier filtering using configurable criteria.

Classes:
    SampleValidator: Sample quality assessment and validation.
"""

import logging

from ..power_analyzer_interface import (
    OutlierDetectorInterface,
    SampleValidatorInterface,
)
from ..sampler import PowerSample

_LOGGER = logging.getLogger(__name__)


class SampleValidator(SampleValidatorInterface):
    """Sample quality assessment and validation.

    Validates power samples for statistical consistency, range checks,
    and outlier filtering using configurable criteria.
    """

    def __init__(self):
        """Initialize sample validator."""
        _LOGGER.debug("SampleValidator initialized")

    def validate_sample(
        self, sample: PowerSample, outlier_detector: OutlierDetectorInterface
    ) -> bool:
        """Validate sample for quality and statistical consistency.

        Args:
            sample: Sample to validate.
            outlier_detector: Detector for outlier analysis.

        Returns:
            bool: True if sample passes all validation checks.
        """
        if not sample.is_valid():
            return False

        if outlier_detector.is_outlier(sample.value):
            return False

        return self._is_in_reasonable_range(sample.value)

    def _is_in_reasonable_range(self, value: float) -> bool:
        """Check if power value is within reasonable consumption bounds.

        Args:
            value: Power consumption value in watts.

        Returns:
            bool: True if value is reasonable, False otherwise.
        """
        MIN_POWER = 0.0
        MAX_POWER = 50000.0  # 50kW covers most use cases

        return MIN_POWER <= value <= MAX_POWER

    def validate_sample_basic(self, sample: PowerSample) -> bool:
        """Perform basic validation without statistical outlier detection.

        Args:
            sample: The sample to validate.

        Returns:
            bool: True if basic validation passes, False otherwise.
        """
        if not sample.is_valid():
            return False

        return self._is_in_reasonable_range(sample.value)

    def validate_samples_batch(
        self,
        samples: list[PowerSample],
        outlier_detector: OutlierDetectorInterface,
    ) -> list[bool]:
        """Validate a batch of samples.

        Args:
            samples: List of samples to validate.
            outlier_detector: Detector for outlier analysis.

        Returns:
            list[bool]: List of boolean validation results.
        """
        results = []
        for sample in samples:
            results.append(self.validate_sample(sample, outlier_detector))
        return results

    def filter_valid_samples(
        self,
        samples: list[PowerSample],
        outlier_detector: OutlierDetectorInterface,
    ) -> list[PowerSample]:
        """Filter a list to return only valid samples.

        Args:
            samples: List of samples to filter.
            outlier_detector: Detector for outlier analysis.

        Returns:
            list[PowerSample]: List containing only valid samples.
        """
        valid_samples = []
        for sample in samples:
            if self.validate_sample(sample, outlier_detector):
                valid_samples.append(sample)
        return valid_samples

    def get_validation_stats(
        self,
        samples: list[PowerSample],
        outlier_detector: OutlierDetectorInterface,
    ) -> dict[str, int | float]:
        """Get validation statistics for a batch of samples.

        Args:
            samples: List of samples to analyze.
            outlier_detector: Detector for outlier analysis.

        Returns:
            dict[str, int]: Dictionary with validation statistics.
        """
        total_samples = len(samples)
        valid_samples = self.filter_valid_samples(samples, outlier_detector)
        invalid_samples = total_samples - len(valid_samples)

        # Count different failure reasons
        basic_invalid = sum(1 for s in samples if not s.is_valid())
        outlier_count = 0
        range_invalid = 0

        for sample in samples:
            if sample.is_valid():
                if outlier_detector.is_outlier(sample.value):
                    outlier_count += 1
                elif not self._is_in_reasonable_range(sample.value):
                    range_invalid += 1

        return {
            "total_samples": total_samples,
            "valid_samples": len(valid_samples),
            "invalid_samples": invalid_samples,
            "basic_invalid": basic_invalid,
            "outliers_detected": outlier_count,
            "range_invalid": range_invalid,
            "validation_rate": (
                len(valid_samples) / total_samples if total_samples > 0 else 0.0
            ),
        }

    def is_sample_suspicious(self, sample: PowerSample) -> bool:
        """Check if a sample shows suspicious characteristics.

        Args:
            sample: The sample to check.

        Returns:
            bool: True if sample shows suspicious patterns, False otherwise.
        """
        # Check for suspicious values (like exact zeros when device should be on)
        if sample.value == 0.0:
            # Zero might be valid for standby, but could be suspicious
            _LOGGER.debug("Zero power value detected - may be suspicious")
            return True

        # Check for suspiciously round numbers
        if sample.value == round(sample.value) and sample.value > 100:
            # Exact integers above 100W might indicate sensor issues
            _LOGGER.debug("Suspiciously round power value: %.0f", sample.value)
            return True

        # Check for extreme precision (too many decimal places)
        value_str = str(sample.value)
        if "." in value_str:
            decimal_places = len(value_str.split(".")[-1])
            if decimal_places > 3:  # More than 3 decimal places suspicious
                _LOGGER.debug("Excessive decimal precision: %s", value_str)
                return True

        return False
