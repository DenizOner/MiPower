"""Lock Types for Lock Management

This module contains common lock-related types and classes.
"""

import asyncio
import logging
from datetime import datetime
from typing import Optional

_LOGGER = logging.getLogger(__name__)


class HierarchicalLock:
    """A lock with hierarchical ordering to prevent deadlocks.

    This lock implementation supports hierarchical levels to ensure
    locks are acquired in a consistent order, reducing deadlock risk.
    """

    def __init__(self, lock_id: str, level: int):
        """Initialize a hierarchical lock.

        Args:
            lock_id: Unique identifier for this lock.
            level: Hierarchical level (higher numbers have higher priority).
        """
        self.lock_id = lock_id
        self.level = level
        self._lock = asyncio.Lock()
        self._owner: Optional[str] = None
        self._acquired_at: Optional[datetime] = None

    async def acquire(self, owner: str, timeout: Optional[float] = None) -> bool:
        """Acquire the lock with optional timeout.

        Args:
            owner: Identifier of the lock owner.
            timeout: Maximum time to wait for acquisition.

        Returns:
            bool: True if acquired, False if timed out.
        """
        try:
            acquired = False
            if timeout:
                acquired = await asyncio.wait_for(self._lock.acquire(), timeout=timeout)
            else:
                acquired = await self._lock.acquire()
            if acquired:
                self._owner = owner
                self._acquired_at = datetime.now()
                _LOGGER.debug("Lock %s acquired by %s", self.lock_id, owner)
            return acquired
        except asyncio.TimeoutError:
            _LOGGER.warning("Lock %s acquisition timed out for %s", self.lock_id, owner)
            return False

    def release(self, owner: str) -> None:
        """Release the lock if owned by the specified owner.

        Args:
            owner: The owner attempting to release the lock.
        """
        if self._owner == owner:
            self._lock.release()
            self._owner = None
            self._acquired_at = None
            _LOGGER.debug("Lock %s released by %s", self.lock_id, owner)

    def is_owned_by(self, owner: str) -> bool:
        """Check if the lock is owned by the specified owner.

        Args:
            owner: Owner to check.

        Returns:
            bool: True if owned by the owner.
        """
        return self._owner == owner

    def get_hold_time(self) -> Optional[float]:
        """Get how long the lock has been held.

        Returns:
            Optional[float]: Seconds held, or None if not acquired.
        """
        if self._acquired_at:
            return (datetime.now() - self._acquired_at).total_seconds()
        return None
