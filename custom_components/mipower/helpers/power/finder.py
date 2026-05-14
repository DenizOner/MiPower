"""Smartify power device finder module.

This module provides functionality for discovering and identifying power-related
devices and entities within a Home Assistant installation. It integrates with
the device and entity registries to automatically detect power sensors that
meet specific criteria for power monitoring and analysis.

The main functionality includes filtering devices based on entity domains,
device classes, naming patterns, and excluding battery-powered devices to
ensure accurate power consumption tracking.

Functions:
    find_power_devices: Asynchronously discovers all valid power devices
        in the Home Assistant instance that meet power monitoring criteria.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional, cast

from homeassistant.core import HomeAssistant  # type: ignore[import]
from homeassistant.helpers import device_registry as dr  # type: ignore[import]
from homeassistant.helpers import entity_registry as er  # type: ignore[import]

from ..device.registry_service import DeviceRegistryService
from .criteria import (
    VALID_ENTITY_DOMAINS,
    VALID_POWER_DEVICE_CLASSES,
    VALID_POWER_SUFFIXES,
    INVALID_POWER_DEVICE_CLASSES,
)

_LOGGER = logging.getLogger(__name__)


class OptimizedDeviceDiscovery:
    """Enterprise-grade device discovery with controlled parallelism and caching."""

    def __init__(
        self, max_concurrency: int = 8, batch_size: int = 20, timeout: float = 10.0
    ):
        self.max_concurrency = max_concurrency
        self.batch_size = batch_size
        self.timeout = timeout
        self._validation_cache: Dict[str, Optional[str]] = {}
        self._semaphore = asyncio.Semaphore(max_concurrency)

    async def validate_device_with_cache(
        self,
        hass: HomeAssistant,
        entity_registry: er.EntityRegistry,
        device_entry: dr.DeviceEntry,
        device_manager: DeviceRegistryService,
    ) -> Optional[Dict[str, Any]]:
        """Validate device with caching to avoid repeated expensive operations."""

        device_id = device_entry.id

        # Check cache first
        if device_id in self._validation_cache:
            cached_result = self._validation_cache[device_id]
            if cached_result is None:
                return None

            # Reconstruct device info from cache
            device_info = device_manager.get_device_by_id(hass, device_id)
            device_name = (
                (getattr(device_info, "name", None) if device_info else None)
                or device_entry.name
                or f"Device {device_id}"
            )

            return {
                "id": cached_result,
                "name": device_name,
            }

        # Validate and cache
        async with self._semaphore:
            try:
                # Get device entities
                device_entities = er.async_entries_for_device(
                    entity_registry, device_id, include_disabled_entities=False
                )

                # Check for invalid battery entities
                for entity in device_entities:
                    live_state = hass.states.get(entity.entity_id)
                    if (
                        live_state
                        and live_state.attributes.get("device_class")
                        in INVALID_POWER_DEVICE_CLASSES
                    ):
                        _LOGGER.debug(
                            "[%s] -> DISQUALIFIED: Device has battery entity '%s'",
                            device_entry.name or f"Device {device_id}",
                            entity.entity_id,
                        )
                        self._validation_cache[device_id] = None
                        return None

                # Find valid power entity
                for entity in device_entities:
                    if entity.domain not in VALID_ENTITY_DOMAINS:
                        continue

                    live_state = hass.states.get(entity.entity_id)
                    if not live_state:
                        continue

                    actual_class = live_state.attributes.get("device_class")
                    has_valid_suffix = any(
                        entity.entity_id.endswith(s) for s in VALID_POWER_SUFFIXES
                    )
                    if not has_valid_suffix:
                        continue

                    if actual_class in VALID_POWER_DEVICE_CLASSES:
                        entity_entry_reg = entity_registry.async_get(entity.entity_id)
                        entity_name = (
                            entity_entry_reg.name or entity.entity_id
                            if entity_entry_reg
                            else entity.entity_id
                        )

                        device_info = device_manager.get_device_by_id(hass, device_id)
                        device_name = (
                            (
                                getattr(device_info, "name", None)
                                if device_info
                                else None
                            )
                            or device_entry.name
                            or f"Device {device_id}"
                        )

                        _LOGGER.debug(
                            "[V] SUCCESS: '%s' valid power device. Entity: %s (%s)",
                            device_name,
                            entity.entity_id,
                            entity_name,
                        )

                        # Cache successful result
                        self._validation_cache[device_id] = entity.entity_id

                        return {
                            "id": entity.entity_id,
                            "name": device_name,
                        }

                # No valid entity found
                _LOGGER.debug(
                    "[%s] -> FAILED: No entity matched all criteria.",
                    device_entry.name or f"Device {device_id}",
                )
                self._validation_cache[device_id] = None
                return None

            except Exception as e:
                _LOGGER.debug(f"Error validating device {device_id}: {e}")
                # Cache negative result on error
                self._validation_cache[device_id] = None
                return None

    async def process_batch(
        self,
        hass: HomeAssistant,
        entity_registry: er.EntityRegistry,
        device_batch: List[dr.DeviceEntry],
        device_manager: DeviceRegistryService,
    ) -> List[Dict[str, Any]]:
        """Process a batch of devices with controlled parallelism."""

        tasks = [
            self.validate_device_with_cache(
                hass, entity_registry, device_entry, device_manager
            )
            for device_entry in device_batch
        ]

        try:
            # Wait for all tasks in batch with timeout
            results = await asyncio.wait_for(
                asyncio.gather(*tasks, return_exceptions=True), timeout=self.timeout
            )
        except asyncio.TimeoutError:
            _LOGGER.warning(f"Batch processing timed out after {self.timeout}s")
            return []

        # Filter out exceptions and None results
        valid_devices = []
        for result in results:
            if isinstance(result, Exception):
                _LOGGER.debug(f"Batch task failed: {type(result).__name__}")
            elif result is not None:
                valid_devices.append(result)

        return valid_devices

    async def discover_devices_optimized(
        self, hass: HomeAssistant
    ) -> List[Dict[str, Any]]:
        """Optimized device discovery using parallel batch processing."""

        if hass is None:
            _LOGGER.error("Home Assistant instance is None")
            return []

        _LOGGER.info("🚀 Starting optimized power device discovery...")

        try:
            device_registry = dr.async_get(hass)
            entity_registry = er.async_get(hass)
            device_manager = DeviceRegistryService()

            device_entries = list(device_registry.devices.values())
            total_devices = len(device_entries)

            _LOGGER.info(
                f"📊 Found {total_devices} devices, processing in parallel batches of {self.batch_size}"
            )

            all_valid_devices = []

            # Create batches
            batches = []
            for i in range(0, total_devices, self.batch_size):
                batch = device_entries[i : i + self.batch_size]
                batches.append(batch)

            # Process all batches in parallel with controlled concurrency
            batch_semaphore = asyncio.Semaphore(3)  # Max 3 concurrent batches

            async def process_batch_with_semaphore(batch, batch_num, total_batches):
                async with batch_semaphore:
                    _LOGGER.debug(
                        f"⚡ Processing batch {batch_num}/{total_batches} ({len(batch)} devices)"
                    )

                    batch_results = await self.process_batch(
                        hass, entity_registry, batch, device_manager
                    )

                    _LOGGER.debug(
                        f"✅ Batch {batch_num} complete: {len(batch_results)} valid devices found"
                    )
                    return batch_results

            # Create parallel tasks for all batches
            batch_tasks = [
                process_batch_with_semaphore(batch, i + 1, len(batches))
                for i, batch in enumerate(batches)
            ]

            # Execute all batch tasks in parallel
            batch_results_list = await asyncio.gather(
                *batch_tasks, return_exceptions=True
            )

            # Collect results
            for result in batch_results_list:
                if isinstance(result, Exception):
                    _LOGGER.warning(f"Batch processing failed: {type(result).__name__}")
                else:
                    all_valid_devices.extend(cast(List[Dict[str, Any]], result))

            # Sort results
            all_valid_devices.sort(key=lambda x: x["name"])

            _LOGGER.info(
                f"🎉 Discovery complete! Found {len(all_valid_devices)} power devices"
            )
            return all_valid_devices

        except Exception as e:
            _LOGGER.error(
                f"Unexpected error during optimized discovery: {e}", exc_info=True
            )
            return []


async def find_power_devices(hass: HomeAssistant) -> List[Dict[str, Any]]:
    """Discover all valid power devices in the Home Assistant instance.

    Enterprise-grade implementation using parallel batch processing and caching
    for optimal performance in config flow scenarios.

    Args:
        hass (HomeAssistant): The Home Assistant instance to search for devices.

    Returns:
        List[Dict[str, Any]]: List of dictionaries containing power device
            information, sorted by device name. Each dictionary contains:
            - id: Power entity ID (str)
            - name: Device name (str)
    """
    # Use optimized discovery for enterprise-grade performance
    optimizer = OptimizedDeviceDiscovery(
        max_concurrency=8,  # Max 8 concurrent validations
        batch_size=15,  # Process 15 devices per batch
        timeout=8.0,  # 8 second timeout per batch
    )

    return await optimizer.discover_devices_optimized(hass)
