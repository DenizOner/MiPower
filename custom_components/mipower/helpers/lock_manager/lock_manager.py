"""
Smartify helpers async lock_manager module - SOLID Refactored Implementation.

This module provides advanced locking mechanisms following SOLID principles,
using composition pattern with separated responsibilities for deadlock detection,
statistics tracking, and lock creation.
"""

import asyncio
import logging
import time
from contextlib import asynccontextmanager
from typing import Any, Awaitable, Callable, Dict, List, Optional

from homeassistant.core import HomeAssistant  # type: ignore[import]

from ..errors.exceptions import LockManagementError
from ..monitoring import record_lock_metric
from .deadlock_detector import DeadlockDetector
from .lock_factory import LockFactory
from .lock_manager_interface import (
    LockAcquirerInterface,
    LockCleanupInterface,
    LockInfo,
    LockQueryInterface,
    LockStatisticsProviderInterface,
)
from .lock_statistics import LockStatisticsTracker

_LOGGER = logging.getLogger(__name__)


class LockManager(
    LockAcquirerInterface,
    LockQueryInterface,
    LockStatisticsProviderInterface,
    LockCleanupInterface,
):
    """Manages lock operations following SOLID principles.

    This class implements LockManagerInterface and uses composition pattern
    with separated responsibilities following SOLID principles:
    - DeadlockDetector for deadlock detection
    - LockStatisticsTracker for performance metrics
    - LockFactory for lock creation and management

    Follows Single Responsibility Principle by delegating specific tasks
    to specialized components while orchestrating the overall process.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        default_timeout: float = 30.0,
        max_lock_time: float = 300.0,
        cleanup_interval: int = 60,
        deadlock_detector=None,
        statistics_tracker=None,
        lock_factory=None,
    ):
        self._hass = hass
        self.default_timeout = default_timeout
        self.max_lock_time = max_lock_time

        # Initialize SOLID components using composition with optional parameters for testability
        self._deadlock_detector = deadlock_detector or DeadlockDetector()
        self._statistics_tracker = statistics_tracker or LockStatisticsTracker()
        self._lock_factory = lock_factory or LockFactory()

        # Core lock management
        self._active_locks: Dict[str, LockInfo] = {}
        self._cleanup_timer: Optional[asyncio.TimerHandle] = None

        self._start_cleanup_timer(cleanup_interval)
        _LOGGER.debug(
            "LockManager initialized with SOLID components: "
            "timeout=%.1fs, max_time=%.1fs",
            default_timeout,
            max_lock_time,
        )

    @classmethod
    def create(
        cls,
        hass: HomeAssistant,
        default_timeout: float = 30.0,
        max_lock_time: float = 300.0,
        cleanup_interval: int = 60,
        deadlock_detector=None,
        statistics_tracker=None,
        lock_factory=None,
    ):
        """Factory method for creating LockManager instances with optional dependencies.

        This factory method enables interface mocking for testing by allowing
        injection of mock implementations for internal components.

        Args:
            hass: Home Assistant instance
            default_timeout: Default lock timeout
            max_lock_time: Maximum lock hold time
            cleanup_interval: Cleanup timer interval
            deadlock_detector: Optional DeadlockDetectorInterface implementation
            statistics_tracker: Optional LockStatisticsInterface implementation
            lock_factory: Optional LockFactoryInterface implementation

        Returns:
            LockManager: Configured instance
        """
        return cls(
            hass=hass,
            default_timeout=default_timeout,
            max_lock_time=max_lock_time,
            cleanup_interval=cleanup_interval,
            deadlock_detector=deadlock_detector,
            statistics_tracker=statistics_tracker,
            lock_factory=lock_factory,
        )

    @asynccontextmanager
    async def acquire_lock(
        self,
        lock_id: str,
        owner: str,
        timeout: Optional[float] = None,
        hierarchy_level: int = 0,
    ):
        """Acquire a lock using SOLID components.

        Orchestrates lock acquisition using specialized components:
        - LockFactory for lock creation and hierarchy validation
        - DeadlockDetector for deadlock prevention
        - LockStatisticsTracker for metrics collection
        """
        acquisition_timeout = timeout or self.default_timeout

        # Validate hierarchy using factory
        if not self._lock_factory.validate_hierarchy(lock_id, hierarchy_level):
            raise LockManagementError(f"Lock hierarchy violation for {lock_id}")

        # Get or create lock using factory
        lock = self._lock_factory.get_or_create_lock(lock_id, hierarchy_level)

        # Check for deadlock using detector
        if self._deadlock_detector.detect_deadlock(owner, lock_id, self._active_locks):
            self._statistics_tracker.record_deadlock(lock_id)
            raise LockManagementError(
                f"Deadlock detected while acquiring lock {lock_id} for {owner}"
            )

        # Attempt lock acquisition
        acquired = await lock.acquire(owner, acquisition_timeout)
        if not acquired:
            self._statistics_tracker.record_timeout(lock_id)
            raise asyncio.TimeoutError(
                f"Failed to acquire lock {lock_id} within {acquisition_timeout}s"
            )

        # Track active lock
        lock_info = LockInfo(lock_id=lock_id, owner=owner, timeout=acquisition_timeout)
        self._active_locks[f"{lock_id}:{owner}"] = lock_info

        _LOGGER.debug("Lock acquired: %s by %s", lock_id, owner)
        record_lock_metric("lock_acquired", 1, lock_id, owner)

        try:
            yield True
        finally:
            lock.release(owner)
            self._release_lock(lock_id, owner)
            _LOGGER.debug("Lock released: %s by %s", lock_id, owner)

    def _release_lock(self, lock_id: str, owner: str) -> None:
        """Release a lock and update statistics using SOLID components."""
        lock_key = f"{lock_id}:{owner}"
        if lock_key in self._active_locks:
            lock_info = self._active_locks[lock_key]
            hold_time = lock_info.get_duration()

            # Update statistics using tracker
            self._statistics_tracker.update_lock_statistics(lock_info)

            # Record monitoring metrics
            record_lock_metric("lock_hold_time", hold_time, lock_id, owner)
            record_lock_metric("lock_released", 1, lock_id, owner)

            del self._active_locks[lock_key]

        # Clean up wait-for graph using detector
        self._deadlock_detector.cleanup_wait_edges(owner)

    async def execute_with_lock(
        self,
        lock_id: str,
        owner: str,
        operation: Callable[..., Awaitable[Any]],
        *args,
        **kwargs,
    ) -> Any:
        async with self.acquire_lock(lock_id, owner):
            return await operation(*args, **kwargs)

    def get_lock_info(self, lock_id: str) -> Optional[LockInfo]:
        for lock_key, lock_info in self._active_locks.items():
            if lock_info.lock_id == lock_id:
                return lock_info
        return None

    def get_locks_by_owner(self, owner: str) -> List[LockInfo]:
        return [
            lock_info
            for lock_key, lock_info in self._active_locks.items()
            if lock_info.owner == owner
        ]

    def get_lock_statistics(self) -> Dict[str, Any]:
        """Get comprehensive lock statistics from statistics tracker."""
        stats = self._statistics_tracker.get_statistics()
        stats.update(
            {
                "active_locks": len(self._active_locks),
                "registered_locks": self._lock_factory.get_statistics()["total_locks"],
            }
        )
        return stats

    def get_long_held_locks(self, threshold: Optional[float] = None) -> List[LockInfo]:
        if threshold is None:
            threshold = self.max_lock_time
        long_held = []
        for lock_info in self._active_locks.values():
            if lock_info.is_expired(threshold):
                long_held.append(lock_info)
        return long_held

    def _start_cleanup_timer(self, interval: int) -> None:
        if self._cleanup_timer:
            self._cleanup_timer.cancel()
        self._cleanup_timer = self._hass.loop.call_later(interval, self._cleanup_locks)

    def _cleanup_locks(self) -> None:
        time.time()
        long_held = self.get_long_held_locks()
        for lock_info in long_held:
            _LOGGER.warning(
                "Lock %s held by %s for %.1fs (max: %.1fs)",
                lock_info.lock_id,
                lock_info.owner,
                lock_info.get_duration(),
                self.max_lock_time,
            )
        self._start_cleanup_timer(60)

    async def cleanup(self) -> None:
        """Clean up resources using SOLID components."""
        if self._cleanup_timer:
            self._cleanup_timer.cancel()
            self._cleanup_timer = None

        # Release all active locks using factory
        for lock_key, lock_info in list(self._active_locks.items()):
            lock = self._lock_factory.get_lock(lock_info.lock_id)
            if lock:
                lock.release(lock_info.owner)

        # Clear all data structures
        self._lock_factory.cleanup_all_locks()
        self._active_locks.clear()
        self._deadlock_detector.clear_graph()
        self._statistics_tracker.reset_statistics()

        _LOGGER.info("LockManager cleanup completed")


class ReadWriteLock:
    def __init__(self):
        self._read_lock = asyncio.Lock()
        self._write_lock = asyncio.Lock()
        self._readers: set[str] = set()
        self._writer: Optional[str] = None

    async def acquire_read(self, owner: str) -> None:
        async with self._read_lock:
            while self._writer is not None:
                await asyncio.sleep(0.01)
            self._readers.add(owner)
            _LOGGER.debug(
                "Read lock acquired by %s (total readers: %d)",
                owner,
                len(self._readers),
            )

    async def release_read(self, owner: str) -> None:
        async with self._read_lock:
            if owner in self._readers:
                self._readers.remove(owner)
                _LOGGER.debug(
                    "Read lock released by %s (remaining readers: %d)",
                    owner,
                    len(self._readers),
                )
            else:
                _LOGGER.warning(
                    "Attempted to release read lock by %s who doesn't own it",
                    owner,
                )

    async def acquire_write(self, owner: str) -> None:
        async with self._write_lock:
            while self._writer is not None or len(self._readers) > 0:
                await asyncio.sleep(0.01)
            self._writer = owner
            _LOGGER.debug("Write lock acquired by %s", owner)

    async def release_write(self, owner: str) -> None:
        async with self._write_lock:
            if self._writer == owner:
                self._writer = None
                _LOGGER.debug("Write lock released by %s", owner)
            else:
                _LOGGER.warning(
                    "Attempted to release write lock by %s who doesn't own it",
                    owner,
                )


@asynccontextmanager
async def managed_lock(
    lock_manager: LockManager,
    lock_id: str,
    owner: str,
    timeout: Optional[float] = None,
):
    async with lock_manager.acquire_lock(lock_id, owner, timeout):
        yield


async def synchronize_access(
    lock_manager: LockManager,
    lock_id: str,
    owner: str,
    operation: Callable[..., Awaitable[Any]],
    *args,
    **kwargs,
) -> Any:
    async with lock_manager.acquire_lock(lock_id, owner):
        return await operation(*args, **kwargs)
