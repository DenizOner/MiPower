"""Notification interfaces for Smartify integration.

This module defines the interfaces for notification management components,
following SOLID principles with dependency injection support.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from .channels import ChannelStatus
from .manager import NotificationPreferences, SmartNotification


class NotificationManagerInterface(ABC):
    """Interface for notification management operations."""

    @abstractmethod
    async def send_notification(self, notification: SmartNotification) -> bool:
        """Send a smart notification through configured channels.

        Args:
            notification (SmartNotification): The notification to send.

        Returns:
            bool: True if notification was sent successfully, False otherwise.
        """
        pass

    @abstractmethod
    def _should_notify_based_on_preferences(
        self, notification: SmartNotification
    ) -> bool:
        """Check if notification should be sent based on user preferences.

        Args:
            notification (SmartNotification): The notification to check.

        Returns:
            bool: True if should notify, False otherwise.
        """
        pass

    @abstractmethod
    async def update_user_preferences(
        self, preferences: NotificationPreferences
    ) -> None:
        """Update user notification preferences.

        Args:
            preferences (NotificationPreferences): New preferences to apply.
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def get_notification_stats(self) -> Dict[str, Any]:
        """Get comprehensive notification statistics.

        Returns:
            Dict[str, Any]: Dictionary containing notification statistics.
        """
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """Clean up notification manager state and reset statistics."""
        pass


class NotificationTemplatesInterface(ABC):
    """Interface for notification template management."""

    @abstractmethod
    def get_template(self, template_id: str) -> Optional[Any]:
        """Get a template by its ID.

        Args:
            template_id (str): The template identifier.

        Returns:
            Optional[Any]: The template if found, None otherwise.
        """
        pass

    @abstractmethod
    def render_notification(
        self,
        template_id: str,
        context: Dict[str, Any],
        priority: Optional[str] = None,
    ) -> Dict[str, str]:
        """Render a notification using a template and context.

        Args:
            template_id (str): The template identifier to use.
            context (Dict[str, Any]): Context variables for template rendering.
            priority (Optional[str]): Override the default priority.

        Returns:
            Dict[str, str]: Rendered notification with title, message, and priority.
        """
        pass

    @abstractmethod
    def add_custom_template(self, template: Any) -> None:
        """Add a custom notification template.

        Args:
            template (Any): The custom template to add.
        """
        pass

    @abstractmethod
    def list_templates(self) -> List[str]:
        """Get a list of all available template IDs.

        Returns:
            List[str]: List of template identifiers.
        """
        pass


class NotificationChannelsInterface(ABC):
    """Interface for notification channel management."""

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    async def check_all_channels(self) -> Dict[str, bool]:
        """Check the availability of all notification channels.

        Returns:
            Dict[str, bool]: Dictionary mapping channel names to availability status.
        """
        pass

    @abstractmethod
    def get_available_channels(self) -> List[str]:
        """Get a list of currently available notification channels.

        Returns:
            List[str]: List of available channel names.
        """
        pass

    @abstractmethod
    def get_channel_status(self, channel_name: str) -> Optional[ChannelStatus]:
        """Get the status of a specific notification channel.

        Args:
            channel_name (str): Name of the channel.

        Returns:
            Optional[ChannelStatus]: Channel status if channel exists, None otherwise.
        """
        pass

    @abstractmethod
    def get_all_channel_status(self) -> Dict[str, ChannelStatus]:
        """Get the status of all notification channels.

        Returns:
            Dict[str, ChannelStatus]: Dictionary mapping channel names to status objects.
        """
        pass

    @abstractmethod
    def get_channel_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics for all notification channels.

        Returns:
            Dict[str, Any]: Dictionary containing channel statistics, available channels, and totals.
        """
        pass
