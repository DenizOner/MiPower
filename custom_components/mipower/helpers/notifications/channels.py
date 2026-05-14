"""Smartify notification channels module.

This module provides comprehensive notification channel management for the Smartify
integration, supporting various notification methods including persistent notifications,
mobile apps, Telegram, Pushover, and email. It includes channel status monitoring,
error handling, and statistics tracking.
"""

import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from homeassistant.core import HomeAssistant  # type: ignore[import]

from .notification_interface import NotificationChannelsInterface

_LOGGER = logging.getLogger(__name__)


@dataclass
class ChannelStatus:
    """Status information for a notification channel.

    Attributes:
        channel_name (str): Name of the notification channel.
        is_available (bool): Whether the channel is currently available.
        last_check (datetime): When the channel was last checked.
        last_success (Optional[datetime]): When the last successful send occurred.
        last_error (Optional[datetime]): When the last error occurred.
        error_count (int): Total number of errors.
        success_count (int): Total number of successes.
        average_response_time (float): Average response time in seconds.
    """

    channel_name: str
    is_available: bool = True
    last_check: datetime = field(default_factory=datetime.now)
    last_success: Optional[datetime] = None
    last_error: Optional[datetime] = None
    error_count: int = 0
    success_count: int = 0
    average_response_time: float = 0.0

    def record_success(self, response_time: float) -> None:
        """Record a successful notification send.

        Args:
            response_time (float): The response time in seconds.
        """
        self.is_available = True
        self.last_success = datetime.now()
        self.success_count += 1
        if self.average_response_time == 0:
            self.average_response_time = response_time
        else:
            self.average_response_time = (
                (self.average_response_time * (self.success_count - 1)) + response_time
            ) / self.success_count

    def record_error(self, error: str) -> None:
        """Record an error in notification sending.

        Args:
            error (str): The error message.
        """
        self.is_available = False
        self.last_error = datetime.now()
        self.error_count += 1

    def get_success_rate(self) -> float:
        """Calculate the success rate as a percentage.

        Returns:
            float: Success rate percentage (0-100).
        """
        total = self.success_count + self.error_count
        if total == 0:
            return 100.0
        return (self.success_count / total) * 100.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert the status to a dictionary representation.

        Returns:
            Dict[str, Any]: Dictionary containing status information.
        """
        return {
            "channel_name": self.channel_name,
            "is_available": self.is_available,
            "last_check": self.last_check.isoformat(),
            "last_success": (
                self.last_success.isoformat() if self.last_success else None
            ),
            "last_error": (self.last_error.isoformat() if self.last_error else None),
            "error_count": self.error_count,
            "success_count": self.success_count,
            "success_rate": round(self.get_success_rate(), 2),
            "average_response_time": round(self.average_response_time, 3),
        }


class NotificationChannel(ABC):
    """Abstract base class for notification channels."""

    def __init__(self, channel_name: str):
        """Initialize the notification channel.

        Args:
            channel_name (str): Name of the channel.
        """
        self.channel_name = channel_name
        self.status = ChannelStatus(channel_name)

    @abstractmethod
    async def send_notification(self, title: str, message: str, **kwargs) -> bool:
        """Send a notification through this channel.

        Args:
            title (str): The notification title.
            message (str): The notification message.
            **kwargs: Additional keyword arguments for the channel.

        Returns:
            bool: True if the notification was sent successfully, False otherwise.
        """
        pass

    @abstractmethod
    async def check_availability(self) -> bool:
        """Check if the notification channel is available.

        Returns:
            bool: True if the channel is available, False otherwise.
        """
        pass

    async def format_message(self, title: str, message: str) -> Dict[str, str]:
        """Format the title and message for sending.

        Args:
            title (str): The notification title.
            message (str): The notification message.

        Returns:
            Dict[str, str]: Formatted message dictionary.
        """
        return {"title": title, "message": message}


class PersistentNotificationChannel(NotificationChannel):
    """Channel for Home Assistant persistent notifications."""

    def __init__(self, hass: HomeAssistant):
        """Initialize the persistent notification channel.

        Args:
            hass (HomeAssistant): The Home Assistant instance.
        """
        super().__init__("persistent")
        self._hass = hass

    async def send_notification(self, title: str, message: str, **kwargs) -> bool:
        """Send a persistent notification.

        Args:
            title (str): The notification title.
            message (str): The notification message.
            **kwargs: Additional keyword arguments, supports notification_id.

        Returns:
            bool: True if the notification was sent successfully.
        """
        try:
            await self._hass.services.async_call(
                "persistent_notification",
                "create",
                {
                    "title": title,
                    "message": message,
                    "notification_id": kwargs.get("notification_id"),
                },
            )
            return True
        except Exception as e:
            _LOGGER.error(
                "Error sending persistent notification: %s",
                e,
                exc_info=True,
            )
            return False

    async def check_availability(self) -> bool:
        """Check if persistent notifications are available.

        Returns:
            bool: Always True as persistent notifications are always available.
        """
        try:
            return True
        except Exception:
            return False


class MobileNotificationChannel(NotificationChannel):
    """Channel for Home Assistant mobile app notifications."""

    def __init__(self, hass: HomeAssistant):
        """Initialize the mobile notification channel.

        Args:
            hass (HomeAssistant): The Home Assistant instance.
        """
        super().__init__("mobile")
        self._hass = hass

    async def send_notification(self, title: str, message: str, **kwargs) -> bool:
        """Send a notification to mobile app.

        Args:
            title (str): The notification title.
            message (str): The notification message.
            **kwargs: Additional keyword arguments (unused).

        Returns:
            bool: True if the notification was sent successfully.
        """
        try:
            await self._hass.services.async_call(
                "mobile_app",
                "send_message",
                {"title": title, "message": message},
            )
            return True
        except Exception:
            try:
                await self._hass.services.async_call(
                    "notify",
                    "mobile_app_smartphone",
                    {"title": title, "message": message},
                )
                return True
            except Exception as e:
                _LOGGER.error(
                    "Error sending mobile notification: %s",
                    e,
                    exc_info=True,
                )
                return False

    async def check_availability(self) -> bool:
        """Check if mobile app notifications are available.

        Returns:
            bool: True if mobile app service is available.
        """
        try:
            await self._hass.services.async_get("mobile_app")
            return True
        except Exception:
            return False


class TelegramNotificationChannel(NotificationChannel):
    """Channel for Telegram bot notifications."""

    def __init__(self, hass: HomeAssistant):
        """Initialize the Telegram notification channel.

        Args:
            hass (HomeAssistant): The Home Assistant instance.
        """
        super().__init__("telegram")
        self._hass = hass

    async def send_notification(self, title: str, message: str, **kwargs) -> bool:
        """Send a notification via Telegram bot.

        Args:
            title (str): The notification title.
            message (str): The notification message.
            **kwargs: Additional keyword arguments (unused).

        Returns:
            bool: True if the notification was sent successfully.
        """
        try:
            await self._hass.services.async_call(
                "telegram_bot",
                "send_message",
                {"title": title, "message": message},
            )
            return True
        except Exception as e:
            _LOGGER.debug("Telegram notification failed (service not available): %s", e)
            return False

    async def check_availability(self) -> bool:
        """Check if Telegram bot notifications are available.

        Returns:
            bool: True if telegram_bot service is available.
        """
        try:
            await self._hass.services.async_get("telegram_bot")
            return True
        except Exception:
            return False


class PushoverNotificationChannel(NotificationChannel):
    """Channel for Pushover notifications."""

    def __init__(self, hass: HomeAssistant):
        """Initialize the Pushover notification channel.

        Args:
            hass (HomeAssistant): The Home Assistant instance.
        """
        super().__init__("pushover")
        self._hass = hass

    async def send_notification(self, title: str, message: str, **kwargs) -> bool:
        """Send a notification via Pushover.

        Args:
            title (str): The notification title.
            message (str): The notification message.
            **kwargs: Additional keyword arguments, supports priority.

        Returns:
            bool: True if the notification was sent successfully.
        """
        try:
            service_data = {"title": title, "message": message}
            if "priority" in kwargs:
                service_data["data"] = json.dumps({"priority": kwargs["priority"]})
            await self._hass.services.async_call("notify", "pushover", service_data)
            return True
        except Exception as e:
            _LOGGER.debug("Pushover notification failed (service not available): %s", e)
            return False

    async def check_availability(self) -> bool:
        """Check if Pushover notifications are available.

        Returns:
            bool: True if notify service is available.
        """
        try:
            await self._hass.services.async_get("notify")
            return True
        except Exception:
            return False


class EmailNotificationChannel(NotificationChannel):
    """Channel for email notifications."""

    def __init__(self, hass: HomeAssistant):
        """Initialize the email notification channel.

        Args:
            hass (HomeAssistant): The Home Assistant instance.
        """
        super().__init__("email")
        self._hass = hass

    async def send_notification(self, title: str, message: str, **kwargs) -> bool:
        """Send a notification via email.

        Args:
            title (str): The notification title.
            message (str): The notification message.
            **kwargs: Additional keyword arguments (unused).

        Returns:
            bool: True if the notification was sent successfully.
        """
        try:
            await self._hass.services.async_call(
                "notify", "email", {"title": title, "message": message}
            )
            return True
        except Exception as e:
            _LOGGER.debug("Email notification failed (service not available): %s", e)
            return False

    async def check_availability(self) -> bool:
        """Check if email notifications are available.

        Returns:
            bool: True if notify service is available.
        """
        try:
            await self._hass.services.async_get("notify")
            return True
        except Exception:
            return False


class NotificationChannels(NotificationChannelsInterface):
    """Manager for multiple notification channels."""

    def __init__(self, hass: HomeAssistant):
        """Initialize the notification channels manager.

        Args:
            hass (HomeAssistant): The Home Assistant instance.
        """
        self._hass = hass
        self._channels: Dict[str, NotificationChannel] = {}
        self._initialize_channels()

    def _initialize_channels(self) -> None:
        """Initialize all notification channels."""
        self._channels = {
            "persistent": PersistentNotificationChannel(self._hass),
            "mobile": MobileNotificationChannel(self._hass),
            "telegram": TelegramNotificationChannel(self._hass),
            "pushover": PushoverNotificationChannel(self._hass),
            "email": EmailNotificationChannel(self._hass),
        }

    async def send_to_channel(
        self, channel_name: str, title: str, message: str, **kwargs
    ) -> bool:
        """Send a notification to a specific channel.

        Args:
            channel_name (str): Name of the channel to send to.
            title (str): The notification title.
            message (str): The notification message.
            **kwargs: Additional keyword arguments for the channel.

        Returns:
            bool: True if the notification was sent successfully.
        """
        channel = self._channels.get(channel_name)
        if not channel:
            _LOGGER.warning("Unknown notification channel: %s", channel_name)
            return False
        try:
            success = await channel.send_notification(title, message, **kwargs)
            if success:
                channel.status.record_success(0.1)
            else:
                channel.status.record_error("Send failed")
            return success
        except Exception as e:
            _LOGGER.error(
                "Error sending to channel %s: %s",
                channel_name,
                e,
                exc_info=True,
            )
            channel.status.record_error(str(e))
            return False

    async def send_to_multiple_channels(
        self, channel_names: List[str], title: str, message: str, **kwargs
    ) -> Dict[str, bool]:
        """Send a notification to multiple channels.

        Args:
            channel_names (List[str]): List of channel names to send to.
            title (str): The notification title.
            message (str): The notification message.
            **kwargs: Additional keyword arguments for the channels.

        Returns:
            Dict[str, bool]: Dictionary mapping channel names to send results.
        """
        results = {}
        for channel_name in channel_names:
            success = await self.send_to_channel(channel_name, title, message, **kwargs)
            results[channel_name] = success
        return results

    async def check_all_channels(self) -> Dict[str, bool]:
        """Check the availability of all notification channels.

        Returns:
            Dict[str, bool]: Dictionary mapping channel names to availability status.
        """
        results = {}
        for channel_name, channel in self._channels.items():
            try:
                is_available = await channel.check_availability()
                channel.status.is_available = is_available
                channel.status.last_check = datetime.now()
                results[channel_name] = is_available
            except Exception as e:
                _LOGGER.error(
                    "Error checking channel %s: %s",
                    channel_name,
                    e,
                    exc_info=True,
                )
                results[channel_name] = False
        return results

    def get_available_channels(self) -> List[str]:
        """Get a list of currently available notification channels.

        Returns:
            List[str]: List of available channel names.
        """
        available = []
        for channel_name, channel in self._channels.items():
            if channel.status.is_available:
                available.append(channel_name)
        return available

    def get_channel_status(self, channel_name: str) -> Optional[ChannelStatus]:
        """Get the status of a specific notification channel.

        Args:
            channel_name (str): Name of the channel.

        Returns:
            Optional[ChannelStatus]: Channel status if channel exists, None otherwise.
        """
        channel = self._channels.get(channel_name)
        return channel.status if channel else None

    def get_all_channel_status(self) -> Dict[str, ChannelStatus]:
        """Get the status of all notification channels.

        Returns:
            Dict[str, ChannelStatus]: Dictionary mapping channel names to status objects.
        """
        return {
            channel_name: channel.status
            for channel_name, channel in self._channels.items()
        }

    def get_channel_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics for all notification channels.

        Returns:
            Dict[str, Any]: Dictionary containing channel statistics, available channels, and totals.
        """
        stats = {}
        for channel_name, channel in self._channels.items():
            stats[channel_name] = channel.status.to_dict()
        return {
            "channels": stats,
            "available_channels": self.get_available_channels(),
            "total_channels": len(self._channels),
        }


async def send_persistent_notification(
    hass: HomeAssistant,
    title: str,
    message: str,
    notification_id: Optional[str] = None,
) -> bool:
    """Send a persistent notification to Home Assistant.

    Args:
        hass (HomeAssistant): The Home Assistant instance.
        title (str): The notification title.
        message (str): The notification message.
        notification_id (Optional[str]): Optional notification ID for updating existing notifications.

    Returns:
        bool: True if the notification was sent successfully.
    """
    channels = NotificationChannels(hass)
    return await channels.send_to_channel(
        "persistent", title, message, notification_id=notification_id
    )


async def send_mobile_notification(
    hass: HomeAssistant, title: str, message: str
) -> bool:
    """Send a notification to mobile app.

    Args:
        hass (HomeAssistant): The Home Assistant instance.
        title (str): The notification title.
        message (str): The notification message.

    Returns:
        bool: True if the notification was sent successfully.
    """
    channels = NotificationChannels(hass)
    return await channels.send_to_channel("mobile", title, message)


async def send_telegram_notification(
    hass: HomeAssistant, title: str, message: str
) -> bool:
    """Send a notification via Telegram bot.

    Args:
        hass (HomeAssistant): The Home Assistant instance.
        title (str): The notification title.
        message (str): The notification message.

    Returns:
        bool: True if the notification was sent successfully.
    """
    channels = NotificationChannels(hass)
    return await channels.send_to_channel("telegram", title, message)


async def send_pushover_notification(
    hass: HomeAssistant, title: str, message: str, priority: int = 0
) -> bool:
    """Send a notification via Pushover.

    Args:
        hass (HomeAssistant): The Home Assistant instance.
        title (str): The notification title.
        message (str): The notification message.
        priority (int): Priority level for the notification (default: 0).

    Returns:
        bool: True if the notification was sent successfully.
    """
    channels = NotificationChannels(hass)
    return await channels.send_to_channel("pushover", title, message, priority=priority)


async def check_notification_services(hass: HomeAssistant) -> Dict[str, bool]:
    """Check the availability of all notification services.

    Args:
        hass (HomeAssistant): The Home Assistant instance.

    Returns:
        Dict[str, bool]: Dictionary mapping service names to availability status.
    """
    channels = NotificationChannels(hass)
    return await channels.check_all_channels()
