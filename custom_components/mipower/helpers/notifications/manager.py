"""Smartify notification management module.

This module provides comprehensive notification management capabilities for the Smartify
integration, including priority-based notifications, channel management, rate limiting,
user preferences, filtering, and comprehensive statistics tracking.
"""

import asyncio
import logging
import time
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set

from homeassistant.core import HomeAssistant  # type: ignore[import]

from ..batch import BatchProcessor

from .notification_interface import NotificationManagerInterface

_LOGGER = logging.getLogger(__name__)


class NotificationPriority(Enum):
    """Enumeration of notification priority levels."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class NotificationChannel(Enum):
    """Enumeration of available notification channels."""

    PERSISTENT = "persistent"
    MOBILE = "mobile"
    TELEGRAM = "telegram"
    PUSHOVER = "pushover"
    EMAIL = "email"


@dataclass
class NotificationPreferences:
    """User preferences for notification behavior.

    Attributes:
        enabled_channels (Set[NotificationChannel]): Set of enabled notification channels.
        min_priority (NotificationPriority): Minimum priority level for notifications.
        quiet_hours_start (Optional[str]): Start time for quiet hours (HH:MM format).
        quiet_hours_end (Optional[str]): End time for quiet hours (HH:MM format).
        max_notifications_per_hour (int): Maximum notifications allowed per hour.
        group_similar_notifications (bool): Whether to group similar notifications.
        notification_history_days (int): Number of days to keep notification history.
    """

    enabled_channels: Set[NotificationChannel] = field(
        default_factory=lambda: {NotificationChannel.PERSISTENT}
    )
    min_priority: NotificationPriority = NotificationPriority.NORMAL
    quiet_hours_start: Optional[str] = None
    quiet_hours_end: Optional[str] = None
    max_notifications_per_hour: int = 10
    group_similar_notifications: bool = True
    notification_history_days: int = 7

    def is_in_quiet_hours(self) -> bool:
        """Check if current time is within quiet hours.

        Returns:
            bool: True if currently in quiet hours, False otherwise.
        """
        if not self.quiet_hours_start or not self.quiet_hours_end:
            return False
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        if self.quiet_hours_start > self.quiet_hours_end:
            return (
                current_time >= self.quiet_hours_start
                or current_time <= self.quiet_hours_end
            )
        else:
            return self.quiet_hours_start <= current_time <= self.quiet_hours_end

    def should_notify(
        self, priority: NotificationPriority, channel: NotificationChannel
    ) -> bool:
        """Determine if a notification should be sent based on preferences.

        Args:
            priority (NotificationPriority): Priority of the notification.
            channel (NotificationChannel): Channel for the notification.

        Returns:
            bool: True if notification should be sent, False otherwise.
        """
        if channel not in self.enabled_channels:
            return False
        priority_levels = {
            NotificationPriority.LOW: 0,
            NotificationPriority.NORMAL: 1,
            NotificationPriority.HIGH: 2,
            NotificationPriority.CRITICAL: 3,
        }
        if priority_levels.get(priority, 0) < priority_levels.get(self.min_priority, 1):
            return False
        if self.is_in_quiet_hours() and priority != NotificationPriority.CRITICAL:
            return False
        return True


@dataclass
class SmartNotification:
    """Represents a smart notification with metadata and delivery options.

    Attributes:
        title (str): The notification title.
        message (str): The notification message.
        priority (NotificationPriority): Priority level of the notification.
        channels (List[NotificationChannel]): List of channels to send the notification to.
        context (Dict[str, Any]): Additional context data for the notification.
        timestamp (datetime): When the notification was created.
        notification_id (Optional[str]): Unique identifier for the notification.
        expires_at (Optional[datetime]): When the notification expires.
        requires_acknowledgment (bool): Whether the notification requires acknowledgment.
        metadata (Dict[str, Any]): Additional metadata for the notification.
    """

    title: str
    message: str
    priority: NotificationPriority = NotificationPriority.NORMAL
    channels: List[NotificationChannel] = field(
        default_factory=lambda: [NotificationChannel.PERSISTENT]
    )
    context: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    notification_id: Optional[str] = None
    expires_at: Optional[datetime] = None
    requires_acknowledgment: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_expired(self) -> bool:
        """Check if the notification has expired.

        Returns:
            bool: True if the notification has expired, False otherwise.
        """
        if not self.expires_at:
            return False
        return datetime.now() > self.expires_at

    def to_dict(self) -> Dict[str, Any]:
        """Convert the notification to a dictionary representation.

        Returns:
            Dict[str, Any]: Dictionary containing notification data.
        """
        return {
            "title": self.title,
            "message": self.message,
            "priority": self.priority.value,
            "channels": [channel.value for channel in self.channels],
            "context": self.context.copy(),
            "timestamp": self.timestamp.isoformat(),
            "notification_id": self.notification_id,
            "expires_at": (self.expires_at.isoformat() if self.expires_at else None),
            "requires_acknowledgment": self.requires_acknowledgment,
            "metadata": self.metadata.copy(),
        }


class NotificationFilter:
    """Handles filtering and grouping of notifications."""

    def __init__(self):
        """Initialize the notification filter."""
        self._filter_rules: List[Callable[[SmartNotification], bool]] = []
        self._grouping_cache: Dict[str, List[SmartNotification]] = {}

    def add_filter_rule(self, rule: Callable[[SmartNotification], bool]) -> None:
        """Add a filter rule to the filter.

        Args:
            rule (Callable[[SmartNotification], bool]): Function that returns True if notification should be filtered.
        """
        self._filter_rules.append(rule)

    def should_filter(self, notification: SmartNotification) -> bool:
        """Check if a notification should be filtered out.

        Args:
            notification (SmartNotification): The notification to check.

        Returns:
            bool: True if the notification should be filtered, False otherwise.
        """
        return any(rule(notification) for rule in self._filter_rules)

    def add_grouping_rule(self, key_func: Callable[[SmartNotification], str]) -> None:
        """Add a grouping rule for similar notifications.

        Args:
            key_func (Callable[[SmartNotification], str]): Function to generate grouping key.
        """
        pass

    def get_grouped_notifications(
        self, notification: SmartNotification
    ) -> List[SmartNotification]:
        """Get notifications grouped with the given notification.

        Args:
            notification (SmartNotification): The notification to find groups for.

        Returns:
            List[SmartNotification]: List of grouped notifications.
        """
        return []


class NotificationManager(NotificationManagerInterface):
    """Manages smart notifications with filtering, rate limiting, and statistics."""

    def __init__(
        self,
        hass: HomeAssistant,
        default_preferences: Optional[NotificationPreferences] = None,
        max_history_size: int = 200,
    ):
        """Initialize the notification manager.

        Args:
            hass (HomeAssistant): The Home Assistant instance.
            default_preferences (Optional[NotificationPreferences]): Default notification preferences.
            max_history_size (int): Maximum number of notifications to keep in history.
        """
        self._hass = hass
        self.preferences = default_preferences or NotificationPreferences()
        self.max_history_size = max_history_size
        self.filter = NotificationFilter()
        self._notification_history: deque[SmartNotification] = deque(
            maxlen=max_history_size
        )
        self._channel_handlers: Dict[NotificationChannel, Callable] = {}
        self._notification_count: Dict[str, int] = {}
        self._last_notification: Dict[str, datetime] = {}
        self._stats_lock = asyncio.Lock()
        self._batch_processor = BatchProcessor(
            hass, max_concurrency=5, max_batch_size=20
        )
        self._notification_stats = {
            "total_sent": 0,
            "total_filtered": 0,
            "total_grouped": 0,
            "by_channel": {},
            "by_priority": {},
            "errors": 0,
        }
        self._initialize_channel_handlers()
        _LOGGER.debug(
            "NotificationManager initialized: channels=%d, max_history=%d",
            len(self.preferences.enabled_channels),
            max_history_size,
        )

    def _initialize_channel_handlers(self) -> None:
        """Initialize the channel handler mappings."""
        self._channel_handlers = {
            NotificationChannel.PERSISTENT: self._send_persistent_notification,
            NotificationChannel.MOBILE: self._send_mobile_notification,
            NotificationChannel.TELEGRAM: self._send_telegram_notification,
            NotificationChannel.PUSHOVER: self._send_pushover_notification,
            NotificationChannel.EMAIL: self._send_email_notification,
        }

    async def send_notification(self, notification: SmartNotification) -> bool:
        """Send a smart notification through configured channels.

        Args:
            notification (SmartNotification): The notification to send.

        Returns:
            bool: True if notification was sent successfully, False otherwise.
        """
        try:
            if self.filter.should_filter(notification):
                _LOGGER.debug("Notification filtered: %s", notification.title)
                await self._update_stats("filtered")
                return False
            if not self._should_notify_based_on_preferences(notification):
                _LOGGER.debug(
                    "Notification blocked by preferences: %s",
                    notification.title,
                )
                await self._update_stats("filtered")
                return False
            if not self._check_rate_limits(notification):
                _LOGGER.debug("Notification rate limited: %s", notification.title)
                await self._update_stats("filtered")
                return False
            success = await self._deliver_notification(notification)
            if success:
                self._notification_history.append(notification)
                self._last_notification[
                    notification.notification_id or notification.title
                ] = datetime.now()
                await self._update_stats("sent")
                await self._update_stats(f"by_priority.{notification.priority.value}")
                _LOGGER.info("Notification sent successfully: %s", notification.title)
            else:
                await self._update_stats("errors")
                _LOGGER.error(
                    "Failed to send notification: %s",
                    notification.title,
                    exc_info=True,
                )
            return success
        except Exception as e:
            _LOGGER.error(
                "Error sending notification %s: %s",
                notification.title,
                e,
                exc_info=True,
            )
            await self._update_stats("errors")
            return False

    def _should_notify_based_on_preferences(
        self, notification: SmartNotification
    ) -> bool:
        """Check if notification should be sent based on user preferences.

        Args:
            notification (SmartNotification): The notification to check.

        Returns:
            bool: True if should notify, False otherwise.
        """
        for channel in notification.channels:
            if self.preferences.should_notify(notification.priority, channel):
                return True
        return False

    def _check_rate_limits(self, notification: SmartNotification) -> bool:
        """Check if notification exceeds rate limits.

        Args:
            notification (SmartNotification): The notification to check.

        Returns:
            bool: True if within limits, False if rate limited.
        """
        current_hour = datetime.now().strftime("%Y%m%d%H")
        current_count = self._notification_count.get(current_hour, 0)
        if current_count >= self.preferences.max_notifications_per_hour:
            return False
        context_key = notification.notification_id or notification.title
        last_sent = self._last_notification.get(context_key)
        if last_sent:
            time_since_last = datetime.now() - last_sent
            min_interval = timedelta(minutes=5)
            if time_since_last < min_interval:
                return False
        return True

    async def _deliver_notification(self, notification: SmartNotification) -> bool:
        """Deliver notification to all configured channels using batch processing.

        Args:
            notification (SmartNotification): The notification to deliver.

        Returns:
            bool: True if delivered to at least one channel, False otherwise.
        """
        # Filter channels that should receive the notification
        eligible_channels = [
            channel
            for channel in notification.channels
            if self.preferences.should_notify(notification.priority, channel)
        ]

        if not eligible_channels:
            _LOGGER.debug(
                "No eligible channels for notification: %s", notification.title
            )
            return False

        # Create batch for channel delivery
        batch_id = f"notification_{notification.notification_id or id(notification)}_{time.time()}"
        await self._batch_processor.create_batch(batch_id)

        # Add channel delivery operations to batch
        for i, channel in enumerate(eligible_channels):
            await self._batch_processor.add_operation(
                batch_id,
                f"channel_{i}_{channel.value}",
                self._deliver_to_channel,
                priority=self._get_channel_priority(channel),
                dependencies=[],
                notification=notification,
                channel=channel,
            )

        # Execute batch
        batch_result = await self._batch_processor.execute_batch(batch_id)

        if batch_result.status != "completed":
            _LOGGER.error(
                "Batch notification delivery failed: %s",
                batch_result.status,
                exc_info=True,
            )

        # Check results
        delivered_channels = []
        success = False

        for operation_id, result in batch_result.results.items():
            if result:  # result is True if delivery succeeded
                channel_name = operation_id.split("_")[
                    2
                ]  # Extract channel name from operation_id
                delivered_channels.append(channel_name)
                success = True
            else:
                _LOGGER.warning(
                    "Failed to deliver to channel in operation: %s",
                    operation_id,
                )

        if delivered_channels:
            _LOGGER.debug(
                "Notification delivered to channels: %s",
                ", ".join(delivered_channels),
            )
        else:
            _LOGGER.warning(
                "Notification failed to deliver to any channel: %s",
                notification.title,
            )

        return success

    async def _send_persistent_notification(
        self, notification: SmartNotification
    ) -> None:
        """Send notification via Home Assistant persistent notifications.

        Args:
            notification (SmartNotification): The notification to send.
        """
        await self._hass.services.async_call(
            "persistent_notification",
            "create",
            {
                "title": notification.title,
                "message": notification.message,
                "notification_id": notification.notification_id,
            },
        )

    async def _send_mobile_notification(self, notification: SmartNotification) -> None:
        """Send notification via mobile app.

        Args:
            notification (SmartNotification): The notification to send.
        """
        try:
            await self._hass.services.async_call(
                "mobile_app",
                "send_message",
                {"title": notification.title, "message": notification.message},
            )
        except Exception:
            await self._hass.services.async_call(
                "notify",
                "mobile_app_smartphone",
                {"title": notification.title, "message": notification.message},
            )

    async def _send_telegram_notification(
        self, notification: SmartNotification
    ) -> None:
        """Send notification via Telegram bot.

        Args:
            notification (SmartNotification): The notification to send.
        """
        try:
            await self._hass.services.async_call(
                "telegram_bot",
                "send_message",
                {"title": notification.title, "message": notification.message},
            )
        except Exception as e:
            _LOGGER.debug("Telegram notification failed (service not available): %s", e)

    async def _send_pushover_notification(
        self, notification: SmartNotification
    ) -> None:
        """Send notification via Pushover.

        Args:
            notification (SmartNotification): The notification to send.
        """
        try:
            await self._hass.services.async_call(
                "notify",
                "pushover",
                {
                    "title": notification.title,
                    "message": notification.message,
                    "data": {
                        "priority": self._get_pushover_priority(notification.priority)
                    },
                },
            )
        except Exception as e:
            _LOGGER.debug("Pushover notification failed (service not available): %s", e)

    async def _send_email_notification(self, notification: SmartNotification) -> None:
        """Send notification via email.

        Args:
            notification (SmartNotification): The notification to send.
        """
        try:
            await self._hass.services.async_call(
                "notify",
                "email",
                {"title": notification.title, "message": notification.message},
            )
        except Exception as e:
            _LOGGER.debug("Email notification failed (service not available): %s", e)

    def _get_pushover_priority(self, priority: NotificationPriority) -> int:
        """Convert notification priority to Pushover priority level.

        Args:
            priority (NotificationPriority): The notification priority.

        Returns:
            int: Pushover priority level (-1 to 2).
        """
        priority_map = {
            NotificationPriority.LOW: -1,
            NotificationPriority.NORMAL: 0,
            NotificationPriority.HIGH: 1,
            NotificationPriority.CRITICAL: 2,
        }
        return priority_map.get(priority, 0)

    async def _deliver_to_channel(
        self, notification: SmartNotification, channel: NotificationChannel
    ) -> bool:
        """Deliver notification to a specific channel for batch processing.

        Args:
            notification (SmartNotification): The notification to deliver.
            channel (NotificationChannel): The channel to deliver to.

        Returns:
            bool: True if delivery succeeded, False otherwise.
        """
        try:
            handler = self._channel_handlers.get(channel)
            if handler:
                await handler(notification)
                # Update stats for successful delivery
                await self._update_stats(f"by_channel.{channel.value}")
                return True
            else:
                _LOGGER.warning("No handler for channel: %s", channel.value)
                return False
        except Exception as e:
            _LOGGER.error(
                "Error delivering to channel %s: %s",
                channel.value,
                e,
                exc_info=True,
            )
            return False

    def _get_channel_priority(self, channel: NotificationChannel) -> int:
        """Get priority level for a notification channel.

        Args:
            channel (NotificationChannel): The notification channel.

        Returns:
            int: Priority level (higher number = higher priority).
        """
        # Define channel priorities (higher = more important)
        channel_priorities = {
            NotificationChannel.PERSISTENT: 4,
            NotificationChannel.MOBILE: 3,
            NotificationChannel.TELEGRAM: 2,
            NotificationChannel.PUSHOVER: 2,
            NotificationChannel.EMAIL: 1,
        }
        return channel_priorities.get(channel, 1)

    async def update_user_preferences(
        self, preferences: NotificationPreferences
    ) -> None:
        """Update user notification preferences.

        Args:
            preferences (NotificationPreferences): New preferences to apply.
        """
        old_channels = self.preferences.enabled_channels
        self.preferences = preferences
        _LOGGER.info(
            "Notification preferences updated: channels %s -> %s, priority %s",
            [ch.value for ch in old_channels],
            [ch.value for ch in preferences.enabled_channels],
            preferences.min_priority.value,
        )

    def get_notification_history(
        self,
        limit: Optional[int] = None,
        priority: Optional[str] = None,
    ) -> List[SmartNotification]:
        """Get notification history with optional filtering.

        Args:
            limit (Optional[int]): Maximum number of notifications to return.
            priority (Optional[str]): Filter by priority level.

        Returns:
            List[SmartNotification]: List of notifications from history.
        """
        history = list(self._notification_history)
        if priority:
            history = [n for n in history if n.priority.value == priority]
        if limit:
            history = history[-limit:]
        return history

    async def _update_stats(self, stat_key: str) -> None:
        """Update notification statistics.

        Args:
            stat_key (str): Dot-separated key for the statistic to update.
        """
        async with self._stats_lock:
            keys = stat_key.split(".")
            current_dict = self._notification_stats
            for key in keys[:-1]:
                if key not in current_dict:
                    current_dict[key] = {}
                current_dict = current_dict[key]
            final_key = keys[-1]
            current_dict[final_key] = current_dict.get(final_key, 0) + 1

    def get_notification_stats(self) -> Dict[str, Any]:
        """Get comprehensive notification statistics.

        Returns:
            Dict[str, Any]: Dictionary containing notification statistics.
        """
        return self._notification_stats.copy()

    def get_notification_summary(self) -> Dict[str, Any]:
        """Get a comprehensive summary of notification system state.

        Returns:
            Dict[str, Any]: Dictionary containing preferences, statistics, and system info.
        """
        return {
            "preferences": {
                "enabled_channels": [
                    ch.value for ch in self.preferences.enabled_channels
                ],
                "min_priority": self.preferences.min_priority.value,
                "quiet_hours": f"{self.preferences.quiet_hours_start or 'None'} - {
                    self.preferences.quiet_hours_end or 'None'
                }",
                "max_per_hour": self.preferences.max_notifications_per_hour,
                "group_similar": self.preferences.group_similar_notifications,
            },
            "statistics": self.get_notification_stats(),
            "history_size": len(self._notification_history),
            "available_channels": [ch.value for ch in NotificationChannel],
            "is_in_quiet_hours": self.preferences.is_in_quiet_hours(),
        }

    async def cleanup(self) -> None:
        """Clean up notification manager state and reset statistics."""
        self._notification_history.clear()
        self._notification_count.clear()
        self._last_notification.clear()
        async with self._stats_lock:
            self._notification_stats = {
                "total_sent": 0,
                "total_filtered": 0,
                "total_grouped": 0,
                "by_channel": {},
                "by_priority": {},
                "errors": 0,
            }
        _LOGGER.info("NotificationManager cleanup completed")


async def send_device_state_notification(
    notification_manager: NotificationManager,
    device_name: str,
    old_state: str,
    new_state: str,
    priority: NotificationPriority = NotificationPriority.NORMAL,
) -> None:
    """Send a notification for device state changes.

    Args:
        notification_manager (NotificationManager): The notification manager instance.
        device_name (str): Name of the device that changed state.
        old_state (str): Previous state of the device.
        new_state (str): New state of the device.
        priority (NotificationPriority): Priority level for the notification.
    """
    title = f"Device State Changed: {device_name}"
    message = f"Device '{device_name}' changed state: {old_state} → {new_state}"
    notification = SmartNotification(
        title=title,
        message=message,
        priority=priority,
        channels=[NotificationChannel.PERSISTENT],
        context={
            "device_name": device_name,
            "old_state": old_state,
            "new_state": new_state,
            "notification_type": "device_state_change",
        },
    )
    await notification_manager.send_notification(notification)


async def send_error_notification(
    notification_manager: NotificationManager,
    error_message: str,
    error_code: str,
    entity_id: Optional[str] = None,
    priority: NotificationPriority = NotificationPriority.HIGH,
) -> None:
    """Send an error notification.

    Args:
        notification_manager (NotificationManager): The notification manager instance.
        error_message (str): The error message to send.
        error_code (str): The error code identifier.
        entity_id (Optional[str]): Optional entity ID related to the error.
        priority (NotificationPriority): Priority level for the notification.
    """
    title = f"Smartify Error: {error_code}"
    message = f"An error occurred: {error_message}"
    if entity_id:
        message += f"\n\nAffected Entity: {entity_id}"
    notification = SmartNotification(
        title=title,
        message=message,
        priority=priority,
        channels=[NotificationChannel.PERSISTENT, NotificationChannel.MOBILE],
        context={
            "error_code": error_code,
            "error_message": error_message,
            "entity_id": entity_id,
            "notification_type": "error",
        },
    )
    await notification_manager.send_notification(notification)


async def send_configuration_notification(
    notification_manager: NotificationManager,
    config_change: str,
    priority: NotificationPriority = NotificationPriority.NORMAL,
) -> None:
    """Send a configuration change notification.

    Args:
        notification_manager (NotificationManager): The notification manager instance.
        config_change (str): Description of the configuration change.
        priority (NotificationPriority): Priority level for the notification.
    """
    title = "Smartify Configuration Updated"
    message = f"Configuration change: {config_change}"
    notification = SmartNotification(
        title=title,
        message=message,
        priority=priority,
        channels=[NotificationChannel.PERSISTENT],
        context={
            "config_change": config_change,
            "notification_type": "configuration_change",
        },
    )
    await notification_manager.send_notification(notification)
