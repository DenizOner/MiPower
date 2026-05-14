"""Error context for Smartify integration.

Provides structured context information for error handling.
"""

from typing import Any, Dict, Optional


class ErrorContext:
    """Context information for error handling operations.

    Provides structured information about the operation that caused an error,
    including component, operation type, and relevant identifiers.
    """

    def __init__(
        self,
        component: str,
        operation: str,
        entity_id: Optional[str] = None,
        additional_data: Optional[Dict[str, Any]] = None,
    ):
        """Initialize error context.

        Args:
            component: The component where the error occurred (e.g., "switch", "sensor")
            operation: The operation being performed (e.g., "script_execution", "power_measurement")
            entity_id: The entity ID related to the operation
            additional_data: Any additional context data
        """
        self.component = component
        self.operation = operation
        self.entity_id = entity_id
        self.additional_data = additional_data or {}
        self.timestamp = self._get_timestamp()

    def _get_timestamp(self) -> str:
        """Get current timestamp.

        Returns:
            Current timestamp string
        """
        from datetime import datetime

        return datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert context to dictionary representation.

        Returns:
            Dictionary containing context information
        """
        return {
            "component": self.component,
            "operation": self.operation,
            "entity_id": self.entity_id,
            "additional_data": self.additional_data,
            "timestamp": self.timestamp,
        }
