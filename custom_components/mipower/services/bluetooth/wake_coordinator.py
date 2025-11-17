"""
Bluetooth wake coordinator for MiPower integration.

This module coordinates all Bluetooth wake-up operations,
following the Single Responsibility Principle.
"""

import asyncio
import logging
import time
from typing import Union

from homeassistant.core import HomeAssistant

from ...models import TimingOptions
from .exceptions import TurnOnFailedReason
from .media_player_monitor import MediaPlayerMonitor
from .pair_sender import BluetoothPairSender
from .process_manager import BluetoothProcessManager
from .scanner import BluetoothScanner

_LOGGER = logging.getLogger(__name__)


class BluetoothWakeCoordinator:
    """
    Coordinates Bluetooth wake-up operations.

    Orchestrates all components to perform device wake-up through Bluetooth.
    """

    def __init__(self) -> None:
        """Initialize the wake coordinator."""
        self._process_manager = BluetoothProcessManager()
        self._scanner = BluetoothScanner(self._process_manager)
        self._pair_sender = BluetoothPairSender(self._process_manager)

    async def wake_up(
        self,
        hass: HomeAssistant,
        name: str,
        mac_address: str,
        media_player_entity_id: str,
        timing_options: TimingOptions,
    ) -> Union[bool, TurnOnFailedReason]:
        """Perform the Bluetooth wake operation."""
        # Run the synchronous operation in an executor
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self._sync_wake_up,
            hass,  # type: ignore
            name,
            mac_address,
            media_player_entity_id,
            timing_options,
        )

    def _sync_wake_up(
        self,
        hass: HomeAssistant,  # type: ignore
        name: str,
        mac_address: str,
        media_player_entity_id: str,
        timing_options: TimingOptions,
    ) -> Union[bool, TurnOnFailedReason]:
        """
        Synchronous Bluetooth wake-up operation.

        Coordinates all steps: spawn process, scan, pair, and monitor.
        """
        # Log operation start
        _LOGGER.info(
            "[%s (%s)] Starting Bluetooth wake operation for device %s",
            name,
            media_player_entity_id,
            mac_address,
        )

        start_time = time.monotonic()

        try:
            # Initialize media player monitor
            media_monitor = MediaPlayerMonitor(hass, media_player_entity_id)

            # Step 1: Spawn bluetoothctl process
            step_start = time.monotonic()
            _LOGGER.info(
                "[%s (%s)] [Step 1: Spawning] Spawning bluetoothctl process",
                name,
                media_player_entity_id,
            )
            result = self._process_manager.spawn_process(timing_options)
            step_duration = time.monotonic() - step_start
            if result:
                _LOGGER.warning(
                    "[%s (%s)] [Step 1: Spawning] Failed after %.2fs (Timeout: %ss, Total elapsed: %.2fs)",
                    name,
                    media_player_entity_id,
                    step_duration,
                    timing_options.spawn_timeout,
                    time.monotonic() - start_time,
                )
                return result
            _LOGGER.info(
                "[%s (%s)] [Step 1: Spawning] Completed in %.2fs (Timeout: %ss, Total elapsed: %.2fs)",
                name,
                media_player_entity_id,
                step_duration,
                timing_options.spawn_timeout,
                time.monotonic() - start_time,
            )

            # Inter-step delay
            time.sleep(timing_options.inter_step_delay)

            # Step 2: Scan for device
            step_start = time.monotonic()
            _LOGGER.info(
                "[%s (%s)] [Step 2: Scanning] Scanning for device %s",
                name,
                media_player_entity_id,
                mac_address,
            )
            result = self._scanner.scan_for_device(
                name,
                media_player_entity_id,
                mac_address,
                timing_options,
                media_monitor.is_media_player_on,
            )
            step_duration = time.monotonic() - step_start
            if result:
                _LOGGER.warning(
                    "[%s (%s)] [Step 2: Scanning] Failed after %.2fs (Timeout: %ss, Total elapsed: %.2fs)",
                    name,
                    media_player_entity_id,
                    step_duration,
                    timing_options.scan_duration,
                    time.monotonic() - start_time,
                )
                return result
            _LOGGER.info(
                "[%s (%s)] [Step 2: Scanning] Completed in %.2fs (Timeout: %ss, Total elapsed: %.2fs)",
                name,
                media_player_entity_id,
                step_duration,
                timing_options.scan_duration,
                time.monotonic() - start_time,
            )

            # Inter-step delay
            time.sleep(timing_options.inter_step_delay)

            # Step 3: Stop scanning
            step_start = time.monotonic()
            _LOGGER.info(
                "[%s (%s)] [Step 3: Stopping] Stopping scan",
                name,
                media_player_entity_id,
            )
            result = self._scanner.stop_scan(
                name, media_player_entity_id, timing_options
            )
            step_duration = time.monotonic() - step_start
            if result:
                _LOGGER.warning(
                    "[%s (%s)] [Step 3: Stopping] Failed after %.2fs (Timeout: %ss, Total elapsed: %.2fs)",
                    name,
                    media_player_entity_id,
                    step_duration,
                    timing_options.scan_stop_timeout,
                    time.monotonic() - start_time,
                )
                return result
            _LOGGER.info(
                "[%s (%s)] [Step 3: Stopping] Completed in %.2fs (Timeout: %ss, Total elapsed: %.2fs)",
                name,
                media_player_entity_id,
                step_duration,
                timing_options.scan_stop_timeout,
                time.monotonic() - start_time,
            )

            # Inter-step delay
            time.sleep(timing_options.inter_step_delay)

            # Check media player state before broadcasting pair signal
            _LOGGER.info(
                "[%s (%s)] Checking media player state before pair signal broadcast",
                name,
                media_player_entity_id,
            )

            if media_monitor.is_media_player_on():
                _LOGGER.info(
                    "[%s (%s)] Media player is already on. Stopping all operations.",
                    name,
                    media_player_entity_id,
                )
                _LOGGER.info(
                    "[%s (%s)] Operation completed successfully (Total elapsed: %.2fs)",
                    name,
                    media_player_entity_id,
                    time.monotonic() - start_time,
                )
                return True

            if media_monitor.is_media_player_available():
                _LOGGER.info(
                    "[%s (%s)] Media player is available. Calling turn_on service.",
                    name,
                    media_player_entity_id,
                )
                if media_monitor.try_turn_on_via_ha_service():
                    _LOGGER.info(
                        "[%s (%s)] Operation completed successfully (Total elapsed: %.2fs)",
                        name,
                        media_player_entity_id,
                        time.monotonic() - start_time,
                    )
                    return True

            # Step 4: Broadcast pair signal with monitoring
            step_start = time.monotonic()
            _LOGGER.info(
                "[%s (%s)] [Step 4: Broadcasting] Broadcasting pair signal",
                name,
                media_player_entity_id,
            )
            result = self._broadcast_pair_signal(
                name,
                media_player_entity_id,
                mac_address,
                timing_options,
                media_monitor,
                start_time,
            )
            step_duration = time.monotonic() - step_start
            if isinstance(result, TurnOnFailedReason):
                _LOGGER.warning(
                    "[%s (%s)] [Step 4: Broadcasting] Failed after %.2fs (Timeout: %ss, Total elapsed: %.2fs)",
                    name,
                    media_player_entity_id,
                    step_duration,
                    timing_options.signal_duration,
                    time.monotonic() - start_time,
                )
                return result
            _LOGGER.info(
                "[%s (%s)] [Step 4: Broadcasting] Completed in %.2fs (Timeout: %ss, Total elapsed: %.2fs)",
                name,
                media_player_entity_id,
                step_duration,
                timing_options.signal_duration,
                time.monotonic() - start_time,
            )

            # Inter-step delay
            time.sleep(timing_options.inter_step_delay)

            # Step 5: Wait for media player to become available
            step_start = time.monotonic()
            total_elapsed_time = time.monotonic() - start_time
            wait_timeout = max(0, timing_options.on_debounce - total_elapsed_time)
            _LOGGER.info(
                "[%s (%s)] [Step 5: Waiting] Waiting for media player availability",
                name,
                media_player_entity_id,
            )
            result = self._wait_for_media_player_available(
                name, media_player_entity_id, timing_options, media_monitor, start_time
            )
            step_duration = time.monotonic() - step_start
            if isinstance(result, TurnOnFailedReason):
                _LOGGER.warning(
                    "[%s (%s)] [Step 5: Waiting] Failed after %.2fs (Timeout: %.2fs, Total elapsed: %.2fs)",
                    name,
                    media_player_entity_id,
                    step_duration,
                    wait_timeout,
                    time.monotonic() - start_time,
                )
                return result
            _LOGGER.info(
                "[%s (%s)] [Step 5: Waiting] Completed in %.2fs (Timeout: %.2fs, Total elapsed: %.2fs)",
                name,
                media_player_entity_id,
                step_duration,
                wait_timeout,
                time.monotonic() - start_time,
            )

            _LOGGER.info(
                "[%s (%s)] Operation completed successfully (Timeout: %.2fs, Total elapsed: %.2fs)",
                name,
                media_player_entity_id,
                timing_options.on_debounce,
                time.monotonic() - start_time,
            )
            return True  # Success

        except Exception as e:
            elapsed_time = time.monotonic() - start_time
            _LOGGER.error(
                "[%s (%s)] Unexpected error after %.2fs: %s",
                name,
                media_player_entity_id,
                elapsed_time,
                e,
                exc_info=True,
            )
            raise
        finally:
            # Cleanup
            self._process_manager.cleanup()

            total_elapsed_time = time.monotonic() - start_time
            _LOGGER.info(
                "[%s (%s)] Total Bluetooth wake operation time: %.2fs",
                name,
                media_player_entity_id,
                total_elapsed_time,
            )

    def _broadcast_pair_signal(
        self,
        name: str,
        media_player_entity_id: str,
        mac_address: str,
        timing_options: TimingOptions,
        media_monitor: MediaPlayerMonitor,
        start_time: float,
    ) -> Union[bool, TurnOnFailedReason]:
        """
        Broadcast pair signal for signal_duration seconds.

        Stops early if media_player becomes available during broadcast.

        Args:
            name: Device name
            media_player_entity_id: Media player entity ID
            mac_address: Target MAC address
            timing_options: Timing configuration
            media_monitor: Media player monitor instance
            start_time: Operation start time for calculating elapsed time

        Returns:
            True if successful, TurnOnFailedReason if failed
        """
        broadcast_start = time.monotonic()
        _LOGGER.info(
            "[%s (%s)] Broadcasting pair signal to %s for %s seconds (Total elapsed: %.2fs).",
            name,
            media_player_entity_id,
            mac_address,
            timing_options.signal_duration,
            time.monotonic() - start_time,
        )

        signal_end_time = time.monotonic() + timing_options.signal_duration

        while time.monotonic() < signal_end_time:
            # Send pair command
            result = self._pair_sender.send_pair_command(
                name, media_player_entity_id, mac_address, timing_options
            )
            if result:
                return result

            # Check if media player became available during broadcast
            if media_monitor.is_media_player_available():
                _LOGGER.info(
                    "[%s (%s)] Media player became available during signal broadcast "
                    "(completed in %.2fs of %ss, Total elapsed: %.2fs).",
                    name,
                    media_player_entity_id,
                    time.monotonic() - broadcast_start,
                    timing_options.signal_duration,
                    time.monotonic() - start_time,
                )
                return True

            # Wait before next pair command (1 second interval)
            time.sleep(1.0)

        return True

    def _wait_for_media_player_available(
        self,
        name: str,
        media_player_entity_id: str,
        timing_options: TimingOptions,
        media_monitor: MediaPlayerMonitor,
        start_time: float,
    ) -> Union[bool, TurnOnFailedReason]:
        """
        Wait for media player to become available after pair signal broadcast.

        Wait time is ON_DEBOUNCE - total_elapsed_time.

        Args:
            name: Device name
            media_player_entity_id: Media player entity ID
            timing_options: Timing configuration
            media_monitor: Media player monitor instance
            start_time: Operation start time for calculating elapsed time

        Returns:
            True if successful, TurnOnFailedReason if failed
        """
        total_elapsed_time = time.monotonic() - start_time
        wait_timeout = max(0, timing_options.on_debounce - total_elapsed_time)
        wait_start = time.monotonic()

        wait_end_time = time.monotonic() + wait_timeout

        while time.monotonic() < wait_end_time:
            # Check if media player is on (stop all operations)
            if media_monitor.is_media_player_on():
                wait_duration = time.monotonic() - wait_start
                _LOGGER.info(
                    "[%s (%s)] Media player is now on. Stopping all operations "
                    "(waited %.2fs of %.2fs).",
                    name,
                    media_player_entity_id,
                    wait_duration,
                    wait_timeout,
                )
                return True

            # Check if media player became available
            if media_monitor.is_media_player_available():
                wait_duration = time.monotonic() - wait_start
                _LOGGER.info(
                    "[%s (%s)] Media player became available. Calling turn_on service "
                    "(waited %.2fs of %.2fs).",
                    name,
                    media_player_entity_id,
                    wait_duration,
                    wait_timeout,
                )
                if media_monitor.try_turn_on_via_ha_service():
                    return True

            # Wait before next check (1 second interval)
            time.sleep(1.0)

        # Timeout
        wait_duration = time.monotonic() - wait_start
        _LOGGER.warning(
            "[%s (%s)] Media player did not become available within %.2f seconds "
            "(waited %.2fs).",
            name,
            media_player_entity_id,
            wait_timeout,
            wait_duration,
        )
        return TurnOnFailedReason.SIGNAL_FAILED
