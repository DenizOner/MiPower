"""Config validator interface for Smartify config flow."""

from abc import ABC, abstractmethod


class ConfigValidatorInterface(ABC):
    """Interface for configuration validators."""

    @abstractmethod
    async def validate_power_entity(self, entity_id: str) -> bool:
        """Validate that the selected entity is a valid power entity.

        Args:
            entity_id: The entity ID to validate.

        Returns:
            bool: True if the entity is a valid power sensor, False otherwise.
        """
        pass

    @abstractmethod
    def convert_remote_device_to_entity(self, remote_device_id: str) -> str:
        """Convert remote device ID to entity ID if needed.

        Args:
            remote_device_id: The remote device or entity ID.

        Returns:
            str: The entity ID for the remote device.
        """
        pass
