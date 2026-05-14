"""Smartify power sensor validator module.

This module provides comprehensive validation functionality for power sensors
in Home Assistant. It includes entity registry validation, device association
checks, state validation, response time testing, and confidence scoring to
ensure power sensors are reliable for monitoring and analysis.

The module implements caching to optimize repeated validations and provides
detailed issue reporting for troubleshooting sensor problems.

Classes:
    ValidationResult: Data container for validation outcomes with confidence
        scoring and issue tracking.
    PowerSensorValidator: Main validator class performing comprehensive sensor
        validation with caching and retry logic.

Functions:
    get_power_entity_id: Simplified function to find and validate power entities
        for devices using keyword matching and basic validation.
"""

import asyncio
import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from homeassistant.core import HomeAssistant  # type: ignore[import]
from homeassistant.helpers import device_registry as dr  # type: ignore[import]
from homeassistant.helpers import entity_registry as er  # type: ignore[import]

_LOGGER = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Container for power sensor validation results.

    This dataclass holds the outcome of sensor validation including validity
    status, confidence score, associated device information, and any issues
    encountered during validation.

    Attributes:
        is_valid (bool): Whether the sensor passed all validation checks.
        entity_id (Optional[str]): The entity ID that was validated.
        device_id (Optional[str]): Associated device ID if found.
        device_name (Optional[str]): Human-readable device name.
        confidence (float): Validation confidence score (0.0 to 1.0).
        issues (List[str]): List of validation issues or warnings.
    """

    is_valid: bool
    entity_id: Optional[str] = None
    device_id: Optional[str] = None
    device_name: Optional[str] = None
    confidence: float = 0.0
    issues: List[str] = []

    def __post_init__(self):
        if self.issues is None:
            self.issues = []

    def add_issue(self, issue: str) -> None:
        self.issues.append(issue)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "entity_id": self.entity_id,
            "device_id": self.device_id,
            "device_name": self.device_name,
            "confidence": round(self.confidence, 3),
            "issues": self.issues.copy(),
        }


class PowerSensorValidator:
    """Comprehensive power sensor validator with caching and retry logic.

    This class performs detailed validation of power sensors including registry
    checks, device association, state validation, response time testing, and
    confidence scoring. It implements caching to optimize repeated validations
    and provides detailed issue reporting for troubleshooting.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        max_response_time: float = 2.0,
        retry_attempts: int = 2,
        valid_power_range: Tuple[float, float] = (0.0, 100000.0),
    ):
        """Initialize the power sensor validator.

        Args:
            hass (HomeAssistant): The Home Assistant instance.
            max_response_time (float): Maximum acceptable response time in seconds.
            retry_attempts (int): Number of retry attempts for response time validation.
            valid_power_range (Tuple[float, float]): Valid power value range (min, max).
        """

        self._hass = hass
        self.max_response_time = max_response_time
        self.retry_attempts = retry_attempts
        self.valid_power_range = valid_power_range
        self._validation_cache: Dict[str, Tuple[ValidationResult, float]] = {}
        _LOGGER.debug(
            "PowerSensorValidator initialized: response_time=%.1fs, retries=%d",
            max_response_time,
            retry_attempts,
        )

    async def validate_sensor(self, entity_id: str) -> ValidationResult:
        """Perform comprehensive validation of a power sensor.

        Args:
            entity_id (str): The entity ID of the power sensor to validate.

        Returns:
            ValidationResult: Detailed validation results including validity,
                confidence score, and any issues found.
        """

        _LOGGER.debug("Starting comprehensive validation for: %s", entity_id)
        cached_result = self._get_cached_result(entity_id)
        if cached_result:
            _LOGGER.debug("Using cached validation result for: %s", entity_id)
            return cached_result
        result = ValidationResult(is_valid=True, entity_id=entity_id, confidence=1.0)
        await self._validate_entity_registry(entity_id, result)
        if result.issues and any(
            issue in result.issues
            for issue in [
                "Entity not found in registry",
                "Entity not associated with device",
            ]
        ):
            result.is_valid = False
            result.confidence = 0.0
            self._cache_result(entity_id, result)
            return result
        await self._validate_device_association(entity_id, result)
        await self._validate_current_state(entity_id, result)
        await self._validate_response_time(entity_id, result)
        result.confidence = self._calculate_confidence(result)
        self._cache_result(entity_id, result)
        _LOGGER.info(
            "Validation complete for %s: %s (confidence: %.2f)",
            entity_id,
            "VALID" if result.is_valid else "INVALID",
            result.confidence,
        )
        return result

    async def _validate_entity_registry(
        self, entity_id: str, result: ValidationResult
    ) -> None:
        try:
            entity_registry = er.async_get(self._hass)
            entity_entry = entity_registry.async_get(entity_id)
            if not entity_entry:
                result.add_issue("Entity not found in registry")
                result.is_valid = False
                return
            if not entity_entry.disabled:
                pass
            else:
                result.add_issue("Entity is disabled in registry")
                result.is_valid = False
            if entity_entry.domain != "sensor":
                result.add_issue(
                    f"Entity domain is '{entity_entry.domain}', expected 'sensor'"
                )
                result.is_valid = False
        except Exception as e:
            result.add_issue(f"Registry validation error: {e}")
            result.is_valid = False

    async def _validate_device_association(
        self, entity_id: str, result: ValidationResult
    ) -> None:
        try:
            entity_registry = er.async_get(self._hass)
            entity_entry = entity_registry.async_get(entity_id)
            if not entity_entry or not entity_entry.device_id:
                result.add_issue("Entity not associated with any device")
                result.is_valid = False
                return
            device_registry = dr.async_get(self._hass)
            device_entry = device_registry.async_get(entity_entry.device_id)
            if not device_entry:
                result.add_issue("Associated device not found in device registry")
                result.is_valid = False
                return
            result.device_id = entity_entry.device_id
            result.device_name = (
                device_entry.name_by_user or device_entry.name or "Unknown Device"
            )
            # _LOGGER.debug(
            #     "Entity %s associated with device: %s (%s)",
            #     entity_id,
            #     result.device_name,
            #     result.device_id,
            # )
        except Exception as e:
            result.add_issue(f"Device association validation error: {e}")
            result.is_valid = False

    async def _validate_current_state(
        self, entity_id: str, result: ValidationResult
    ) -> None:
        try:
            state = self._hass.states.get(entity_id)
            if not state:
                result.add_issue("Entity state not available")
                result.is_valid = False
                return
            if state.state in ("unknown", "unavailable"):
                result.add_issue(f"Sensor state is '{state.state}'")
                result.is_valid = False
                return
            try:
                power_value = float(state.state)
                min_power, max_power = self.valid_power_range
                if not (min_power <= power_value <= max_power):
                    result.add_issue(
                        f"Power value {power_value:.2f}W outside valid range "
                        f"({min_power}W - {max_power}W)"
                    )
                    result.is_valid = False
            except (ValueError, TypeError):
                result.add_issue(f"Cannot parse power value: '{state.state}'")
                result.is_valid = False
        except Exception as e:
            result.add_issue(f"State validation error: {e}")
            result.is_valid = False

    async def _validate_response_time(
        self, entity_id: str, result: ValidationResult
    ) -> None:
        response_times = []
        for attempt in range(self.retry_attempts + 1):
            try:
                start_time = asyncio.get_event_loop().time()
                state = self._hass.states.get(entity_id)
                end_time = asyncio.get_event_loop().time()
                response_time = end_time - start_time
                if state and state.state not in ("unknown", "unavailable"):
                    response_times.append(response_time)
                    if response_time > self.max_response_time:
                        result.add_issue(
                            f"Slow response time: {response_time:.3f}s "
                            f"(max: {self.max_response_time:.3f}s)"
                        )
                if attempt < self.retry_attempts:
                    await asyncio.sleep(0.1)
            except Exception as e:
                result.add_issue(
                    f"Response time validation error (attempt {attempt + 1}): {e}"
                )
        # if response_times:
        # avg_response_time = sum(response_times) / len(response_times)
        # _LOGGER.debug(
        #     "Response time validation for %s: %.3fs average",
        #     entity_id,
        #     avg_response_time,
        # )

    def _calculate_confidence(self, result: ValidationResult) -> float:
        if not result.is_valid:
            return 0.0
        confidence = 1.0
        for issue in result.issues:
            if "slow response" in issue.lower():
                confidence *= 0.9
            elif "parse" in issue.lower():
                confidence *= 0.8
            elif "range" in issue.lower():
                confidence *= 0.7
        return round(confidence, 3)

    def _get_cached_result(self, entity_id: str) -> Optional[ValidationResult]:
        if entity_id in self._validation_cache:
            result, timestamp = self._validation_cache[entity_id]
            if asyncio.get_event_loop().time() - timestamp < 300:
                return result
            del self._validation_cache[entity_id]
        return None

    def _cache_result(self, entity_id: str, result: ValidationResult) -> None:
        timestamp = asyncio.get_event_loop().time()
        self._validation_cache[entity_id] = (result, timestamp)
        if len(self._validation_cache) > 100:
            oldest_keys = sorted(
                self._validation_cache.keys(),
                key=lambda k: self._validation_cache[k][1],
            )[:50]
            for key in oldest_keys:
                del self._validation_cache[key]

    def clear_cache(self) -> None:
        """Clear all cached validation results."""
        self._validation_cache.clear()
        _LOGGER.debug("Validation cache cleared")

    def get_cache_stats(self) -> Dict[str, int]:
        """Get statistics about the validation cache.

        Returns:
            Dict[str, int]: Dictionary with cache statistics including
                current entries count and maximum cache size.
        """
        return {
            "current_entries": len(self._validation_cache),
            "max_cache_size": 100,
        }


async def get_power_entity_id(
    hass: HomeAssistant, entity_registry: er.EntityRegistry, device_id: str
) -> Optional[str]:
    """Find and validate a power entity for a given device using keyword matching.

    This simplified function searches for power entities associated with a device
    by looking for keywords in entity IDs, then validates the best candidate
    using comprehensive validation.

    Args:
        hass (HomeAssistant): The Home Assistant instance.
        entity_registry (er.EntityRegistry): The entity registry to search.
        device_id (str): The device ID to find power entity for.

    Returns:
        Optional[str]: The entity ID of a valid power sensor, or None if
            no suitable entity is found.
    """

    try:
        device_entities = er.async_entries_for_device(
            entity_registry, device_id, include_disabled_entities=False
        )
        power_candidates = []
        for entity in device_entities:
            if entity.domain == "sensor":
                entity_id_lower = entity.entity_id.lower()
                if any(
                    keyword in entity_id_lower
                    for keyword in ["power", "consumption", "watt", "energy"]
                ):
                    power_candidates.append(entity.entity_id)
        if not power_candidates and device_entities:
            sensor_entities = [e for e in device_entities if e.domain == "sensor"]
            if sensor_entities:
                power_candidates.append(sensor_entities[0].entity_id)
        if power_candidates:
            validator = PowerSensorValidator(hass)
            best_entity = power_candidates[0]
            result = await validator.validate_sensor(best_entity)
            if result.is_valid:
                _LOGGER.debug(
                    "Found valid power entity for device %s: %s",
                    device_id,
                    best_entity,
                )
                return best_entity
            else:
                _LOGGER.debug(
                    "Power entity candidate %s failed validation: %s",
                    best_entity,
                    result.issues,
                )
        _LOGGER.debug("No valid power entity found for device: %s", device_id)
        return None
    except Exception as e:
        _LOGGER.error(
            "Error finding power entity for device %s: %s",
            device_id,
            e,
            exc_info=True,
        )
        return None
