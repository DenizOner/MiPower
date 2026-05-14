"""
Lock Manager Interface - Dependency Inversion for Lock Management

This module defines the abstraction layer for lock management in Smartify,
implementing Dependency Inversion Principle (DIP) by decoupling lock operations
from the coordinator and other high-level components.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, AsyncContextManager, Awaitable, Callable, Dict, List, Optional

from .lock_types import HierarchicalLock


@dataclass
class LockInfo:
    """Information about an active lock instance.

    Contains details about a lock that is currently held, including
    ownership, timing, and metadata information.
    """

    lock_id: str
    owner: str
    acquired_at: datetime = field(default_factory=datetime.now)
    timeout: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def get_duration(self) -> float:
        return (datetime.now() - self.acquired_at).total_seconds()

    def is_expired(self, timeout: float) -> bool:
        return self.get_duration() > timeout


@dataclass
class LockStatistics:
    """Statistics for lock operations.

    Tracks performance metrics for lock usage including hold times,
    timeouts, deadlocks, and contention.
    """

    total_acquisitions: int = 0
    total_releases: int = 0
    total_timeouts: int = 0
    total_hold_time: float = 0.0
    max_hold_time: float = 0.0
    contention_count: int = 0
    deadlock_count: int = 0

    def update_hold_time(self, hold_time: float) -> None:
        """Update statistics with a new hold time.

        Args:
            hold_time: The hold time to record.
        """
        self.total_releases += 1
        self.total_hold_time += hold_time
        self.max_hold_time = max(self.max_hold_time, hold_time)

    def record_timeout(self) -> None:
        """Record a timeout event."""
        self.total_timeouts += 1

    def record_deadlock(self) -> None:
        """Record a deadlock event."""
        self.deadlock_count += 1

    def record_contention(self) -> None:
        """Record a contention event."""
        self.contention_count += 1

    @property
    def average_hold_time(self) -> float:
        """Get the average hold time."""
        if self.total_releases == 0:
            return 0.0
        return self.total_hold_time / self.total_releases


class LockAcquirerInterface(ABC):
    """Abstract interface for lock acquisition functionality."""

    @abstractmethod
    def acquire_lock(
        self,
        lock_id: str,
        owner: str,
        timeout: Optional[float] = None,
        hierarchy_level: int = 0,
    ) -> AsyncContextManager[bool]:
        """Acquire a lock with the specified parameters.

        Args:
            lock_id: Unique identifier for the lock.
            owner: Identifier of the lock owner.
            timeout: Maximum time to wait for lock acquisition.
            hierarchy_level: Hierarchical level for lock ordering.

        Returns:
            Async context manager for lock usage.
        """
        pass

    @abstractmethod
    async def execute_with_lock(
        self,
        lock_id: str,
        owner: str,
        operation: Callable[..., Awaitable[Any]],
        *args,
        **kwargs,
    ) -> Any:
        """Execute an operation while holding a lock.

        Args:
            lock_id: Unique identifier for the lock.
            owner: Identifier of the lock owner.
            operation: The async function to execute.
            *args: Positional arguments for the operation.
            **kwargs: Keyword arguments for the operation.

        Returns:
            Result of the operation execution.
        """


class LockQueryInterface(ABC):
    """Abstract interface for lock querying functionality."""

    @abstractmethod
    def get_lock_info(self, lock_id: str) -> Optional[LockInfo]:
        """Get information about a specific lock.

        Args:
            lock_id: Unique identifier for the lock.

        Returns:
            LockInfo object or None if lock not found.
        """

    @abstractmethod
    def get_locks_by_owner(self, owner: str) -> List[LockInfo]:
        """Get all locks held by a specific owner.

        Args:
            owner: Identifier of the lock owner.

        Returns:
            List of LockInfo objects for the owner.
        """


class LockStatisticsProviderInterface(ABC):
    """Abstract interface for lock statistics functionality."""

    @abstractmethod
    def get_lock_statistics(self) -> Dict[str, Any]:
        """Get comprehensive lock statistics.

        Returns:
            Dictionary containing lock statistics and metrics.
        """


class LockCleanupInterface(ABC):
    """Abstract interface for lock cleanup functionality."""

    @abstractmethod
    async def cleanup(self) -> None:
        """Clean up resources and reset the lock manager."""


class DeadlockDetectorInterface(ABC):
    """Abstract interface for deadlock detection functionality."""

    @abstractmethod
    def detect_deadlock(
        self, owner: str, lock_id: str, active_locks: Dict[str, LockInfo]
    ) -> bool:
        """Detect if acquiring a lock would cause a deadlock.

        Args:
            owner: The owner requesting the lock.
            lock_id: The lock being requested.
            active_locks: Dictionary of currently active locks.

        Returns:
            True if deadlock would occur, False otherwise.
        """


class LockStatisticsInterface(ABC):
    """Abstract interface for lock statistics tracking."""

    @abstractmethod
    def update_lock_statistics(self, lock_info: LockInfo) -> None:
        """Update statistics when a lock is released.

        Args:
            lock_info: Information about the released lock.
        """

    @abstractmethod
    def get_statistics(self) -> Dict[str, Any]:
        """Get current lock statistics.

        Returns:
            Dictionary containing statistics data.
        """


class LockFactoryInterface(ABC):
    """Abstract interface for lock creation and management."""

    @abstractmethod
    def create_lock(self, lock_id: str, hierarchy_level: int = 0) -> 'HierarchicalLock':
        """Create a new lock instance.

        Args:
            lock_id: Unique identifier for the lock.
            hierarchy_level: Hierarchical level for the lock.

        Returns:
            Lock instance.
        """

    @abstractmethod
    def get_lock(self, lock_id: str) -> Optional['HierarchicalLock']:
        """Get an existing lock instance.

        Args:
            lock_id: Unique identifier for the lock.

        Returns:
            Lock instance or None if not found.
        """

    @abstractmethod
    def validate_hierarchy(self, lock_id: str, new_level: int) -> bool:
        """Validate lock hierarchy constraints.

        Args:
            lock_id: Unique identifier for the lock.
            new_level: New hierarchical level to validate.

        Returns:
            True if hierarchy is valid, False otherwise.
        """


class LockManagerInterface(
    LockAcquirerInterface,
    LockQueryInterface,
    LockStatisticsProviderInterface,
    LockCleanupInterface,
):
    """Abstract interface for lock manager functionality.

    Combines all lock management interfaces into a single contract
    for dependency inversion and SOLID principles compliance.
    """

    pass
