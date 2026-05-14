"""
Script Types - Data classes for script execution

This module defines data classes used by the script execution subsystem.
"""

from typing import Any, Dict, Optional


class ExecutionResult:
    """Result data class for script execution outcomes.

    Encapsulates the outcome of a script execution operation, including success
    status, timing information, and any error details. Provides serialization
    to dictionary format for integration with Home Assistant APIs.

    Attributes:
        success (bool): Whether the script execution was successful.
        script_entity_id (str): The entity ID of the executed script.
        execution_time (float): Time taken to execute the script in seconds.
        error_message (Optional[str]): Error message if execution failed.
    """

    def __init__(
        self,
        success: bool,
        script_entity_id: str,
        execution_time: float,
        error_message: Optional[str] = None,
    ):
        self.success = success
        self.script_entity_id = script_entity_id
        self.execution_time = execution_time
        self.error_message = error_message

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "script_entity_id": self.script_entity_id,
            "execution_time": round(self.execution_time, 2),
            "error_message": self.error_message,
        }
