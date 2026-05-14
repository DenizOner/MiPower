"""Script helpers module for Smartify integration.

This module provides script execution utilities for the Smartify Home Assistant
integration following SOLID principles and pure dependency injection. It exports
the core script execution interface and implementation.
"""

from .executor import ScriptExecutor
from .executor_interface import ScriptExecutorInterface

__all__ = ["ScriptExecutor", "ScriptExecutorInterface"]
