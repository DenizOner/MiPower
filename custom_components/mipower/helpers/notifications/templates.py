"""Smartify notification templates module.

This module provides pre-defined notification templates for common Smartify events,
including device state changes, errors, configuration updates, and calibration events.
Templates support variable substitution and can be customized for different use cases.
"""

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from .notification_interface import NotificationTemplatesInterface

_LOGGER = logging.getLogger(__name__)


@dataclass
class NotificationTemplate:
    """Represents a notification template with variable substitution.

    Attributes:
        template_id (str): Unique identifier for the template.
        title_template (str): Template string for the notification title.
        message_template (str): Template string for the notification message.
        default_priority (str): Default priority level for notifications using this template.
        supported_channels (List[str]): List of supported notification channels.
        variables (List[str]): List of variable names used in the templates.
    """

    template_id: str
    title_template: str
    message_template: str
    default_priority: str = "normal"
    supported_channels: List[str] = field(default_factory=lambda: ["persistent"])
    variables: List[str] = field(default_factory=list)

    def render(self, context: Dict[str, Any]) -> Dict[str, str]:
        """Render the template with the provided context variables.

        Args:
            context (Dict[str, Any]): Dictionary containing variable values for substitution.

        Returns:
            Dict[str, str]: Dictionary with rendered title and message.
        """
        try:
            title = self._render_template(self.title_template, context)
            message = self._render_template(self.message_template, context)
            return {"title": title, "message": message}
        except Exception as e:
            _LOGGER.error(
                "Error rendering template %s: %s",
                self.template_id,
                e,
                exc_info=True,
            )
            return {
                "title": "Notification Error",
                "message": f"Failed to render template: {e}",
            }

    def _render_template(self, template: str, context: Dict[str, Any]) -> str:
        """Render a template string by substituting variables.

        Args:
            template (str): The template string to render.
            context (Dict[str, Any]): Dictionary containing variable values.

        Returns:
            str: The rendered template string.
        """
        result = template
        for var_name in self.variables:
            placeholder = f"{{{var_name}}}"
            value = context.get(var_name, f"{{{var_name}}}")
            result = result.replace(placeholder, str(value))
        return result


class NotificationTemplates(NotificationTemplatesInterface):
    """Manager for notification templates with built-in templates for common events."""

    def __init__(self):
        """Initialize the notification templates manager with default templates."""
        self.templates = self._create_default_templates()

    def _create_default_templates(self) -> Dict[str, NotificationTemplate]:
        """Create the default set of notification templates.

        Returns:
            Dict[str, NotificationTemplate]: Dictionary of default templates.
        """
        return {
            "device_state_change": NotificationTemplate(
                template_id="device_state_change",
                title_template="Device State Changed: {device_name}",
                message_template="Device '{device_name}' changed state: {old_state} → {new_state}",
                default_priority="normal",
                supported_channels=["persistent", "mobile"],
                variables=["device_name", "old_state", "new_state"],
            ),
            "power_sensor_error": NotificationTemplate(
                template_id="power_sensor_error",
                title_template="Power Sensor Error: {entity_id}",
                message_template="Power sensor '{entity_id}' is unavailable or returning invalid data.",
                default_priority="high",
                supported_channels=["persistent", "mobile"],
                variables=["entity_id"],
            ),
            "script_execution_error": NotificationTemplate(
                template_id="script_execution_error",
                title_template="Script Execution Failed: {script_name}",
                message_template="Failed to execute script '{script_name}': {error_message}",
                default_priority="high",
                supported_channels=["persistent", "mobile"],
                variables=["script_name", "error_message"],
            ),
            "configuration_updated": NotificationTemplate(
                template_id="configuration_updated",
                title_template="Smartify Configuration Updated",
                message_template="Configuration updated: {change_description}",
                default_priority="normal",
                supported_channels=["persistent"],
                variables=["change_description"],
            ),
            "calibration_started": NotificationTemplate(
                template_id="calibration_started",
                title_template="Calibration Started: {device_name}",
                message_template="Power calibration started for '{device_name}'. Follow the calibration wizard in Settings.",
                default_priority="normal",
                supported_channels=["persistent"],
                variables=["device_name"],
            ),
            "device_discovery": NotificationTemplate(
                template_id="device_discovery",
                title_template="New Device Discovered: {device_name}",
                message_template="Found new power device: {device_name} ({manufacturer} {model})",
                default_priority="low",
                supported_channels=["persistent"],
                variables=["device_name", "manufacturer", "model"],
            ),
            "performance_warning": NotificationTemplate(
                template_id="performance_warning",
                title_template="Performance Warning: {metric}",
                message_template="Performance issue detected: {metric} is {value} (threshold: {threshold})",
                default_priority="normal",
                supported_channels=["persistent"],
                variables=["metric", "value", "threshold"],
            ),
        }

    def get_template(self, template_id: str) -> Optional[NotificationTemplate]:
        """Get a template by its ID.

        Args:
            template_id (str): The template identifier.

        Returns:
            Optional[NotificationTemplate]: The template if found, None otherwise.
        """
        return self.templates.get(template_id)

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
        template = self.get_template(template_id)
        if not template:
            _LOGGER.warning("Template not found: %s", template_id)
            return {
                "title": "Unknown Notification",
                "message": f"Template '{template_id}' not found",
            }
        rendered = template.render(context)
        if priority:
            rendered["priority"] = priority
        return rendered

    def add_custom_template(self, template: NotificationTemplate) -> None:
        """Add a custom notification template.

        Args:
            template (NotificationTemplate): The custom template to add.
        """
        self.templates[template.template_id] = template
        _LOGGER.debug("Added custom template: %s", template.template_id)

    def list_templates(self) -> List[str]:
        """Get a list of all available template IDs.

        Returns:
            List[str]: List of template identifiers.
        """
        return list(self.templates.keys())


def create_device_state_notification(
    device_name: str, old_state: str, new_state: str
) -> Dict[str, str]:
    """Create a device state change notification.

    Args:
        device_name (str): Name of the device that changed state.
        old_state (str): Previous state of the device.
        new_state (str): New state of the device.

    Returns:
        Dict[str, str]: Rendered notification data.
    """
    templates = NotificationTemplates()
    return templates.render_notification(
        "device_state_change",
        {
            "device_name": device_name,
            "old_state": old_state,
            "new_state": new_state,
        },
    )


def create_error_notification(
    error_type: str, error_message: str, entity_id: Optional[str] = None
) -> Dict[str, str]:
    """Create an error notification based on error type.

    Args:
        error_type (str): Type of error (e.g., "script", "power", "sensor").
        error_message (str): The error message.
        entity_id (Optional[str]): Entity ID related to the error.

    Returns:
        Dict[str, str]: Rendered notification data.
    """
    templates = NotificationTemplates()
    if "script" in error_type.lower():
        return templates.render_notification(
            "script_execution_error",
            {
                "script_name": entity_id or "Unknown Script",
                "error_message": error_message,
            },
        )
    elif "power" in error_type.lower() or "sensor" in error_type.lower():
        return templates.render_notification(
            "power_sensor_error", {"entity_id": entity_id or "Unknown Sensor"}
        )
    else:
        return {
            "title": f"Smartify Error: {error_type}",
            "message": f"An error occurred: {error_message}",
        }


def create_configuration_notification(
    change_description: str,
) -> Dict[str, str]:
    """Create a configuration change notification.

    Args:
        change_description (str): Description of the configuration change.

    Returns:
        Dict[str, str]: Rendered notification data.
    """
    templates = NotificationTemplates()
    return templates.render_notification(
        "configuration_updated", {"change_description": change_description}
    )


def create_calibration_notification(device_name: str) -> Dict[str, str]:
    """Create a calibration started notification.

    Args:
        device_name (str): Name of the device being calibrated.

    Returns:
        Dict[str, str]: Rendered notification data.
    """
    templates = NotificationTemplates()
    return templates.render_notification(
        "calibration_started", {"device_name": device_name}
    )
