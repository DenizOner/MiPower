"""Config validator implementation for Smartify config flow.

Provides validation functionality for configuration flow following SOLID principles.
"""

import logging
from homeassistant.core import HomeAssistant  # type: ignore[import]
from homeassistant.helpers import entity_registry as er  # type: ignore[import]

from .validator_interface import ConfigValidatorInterface
from ...di.container import DependencyContainer

_LOGGER = logging.getLogger(__name__)


class ConfigFlowValidator(ConfigValidatorInterface):
    """Validator for configuration flow inputs."""

    def __init__(self, hass: HomeAssistant, container: DependencyContainer):
        """Initialize validator with Home Assistant instance.

        Args:
            hass: Home Assistant instance
            container: Dependency injection container
        """
        self._container = container
        self.hass = hass

        # Safe logger initialization
        self.logger = container.get_instance("logger") or _LOGGER

        self.logger.info(
            "ConfigFlowValidator __init__ başlatıldı - kapsamlı loglama aktif"
        )
        self.logger.debug(f"Home Assistant instance: {hass}")
        self.logger.debug("Hass instance başarıyla atandı")
        self.logger.info("ConfigFlowValidator __init__ başarıyla tamamlandı")

    async def validate_power_entity(self, entity_id: str) -> bool:
        """Validate that the selected entity is a valid power entity.

        Args:
            entity_id: The entity ID to validate.

        Returns:
            bool: True if the entity is a valid power sensor, False otherwise.
        """
        try:
            self.logger.info(
                f"validate_power_entity başlatıldı - kapsamlı loglama aktif, entity_id: {entity_id}"
            )
            self.logger.debug(f"Validating power entity: {entity_id}")

            # Check if entity exists
            self.logger.debug("Entity varlığı kontrol ediliyor")
            state = self.hass.states.get(entity_id)
            if state is None:
                self.logger.warning(f"Entity {entity_id} does not exist")
                self.logger.debug("Entity bulunamadı, False döndürülüyor")
                return False

            self.logger.debug(f"Entity state bulundu: {state.state}")

            # Check if it's a sensor entity
            self.logger.debug("Sensor kontrolü yapılıyor")
            if not entity_id.startswith("sensor."):
                self.logger.warning(f"Entity {entity_id} is not a sensor")
                self.logger.debug("Sensor değil, False döndürülüyor")
                return False

            # Check if entity has appropriate device_class
            self.logger.debug("Entity registry kontrol ediliyor")
            entity_registry = er.async_get(self.hass)
            registry_entry = entity_registry.async_get(entity_id)
            self.logger.debug(f"Registry entry: {registry_entry}")

            if registry_entry and registry_entry.device_class == "power":
                self.logger.debug(f"Entity {entity_id} validated as power sensor")
                self.logger.info(
                    "validate_power_entity başarıyla tamamlandı - power sensor doğrulandı"
                )
                return True
            elif registry_entry and registry_entry.unit_of_measurement in [
                "W",
                "kW",
                "mW",
            ]:
                self.logger.debug(
                    f"Entity {entity_id} validated by unit of measurement"
                )
                self.logger.info(
                    "validate_power_entity başarıyla tamamlandı - unit of measurement ile doğrulandı"
                )
                return True
            else:
                self.logger.warning(
                    f"Entity {entity_id} is not a recognized power sensor"
                )
                self.logger.debug("Power sensor olarak tanınmadı, False döndürülüyor")
                return False

        except Exception as e:
            self.logger.error(
                f"Error validating power entity {entity_id}: {e}",
                exc_info=True,
            )
            self.logger.error(
                f"Hata bağlamı - entity_id: {entity_id}, hass mevcut: {self.hass is not None}"
            )
            return False
        finally:
            self.logger.debug("validate_power_entity finally bloğu çalıştırıldı")

    def convert_remote_device_to_entity(self, remote_device_id: str) -> str:
        """Convert remote device ID to entity ID if needed.

        Args:
            remote_device_id: The remote device or entity ID.

        Returns:
            str: The entity ID for the remote device.
        """
        try:
            self.logger.info(
                f"convert_remote_device_to_entity başlatıldı - kapsamlı loglama aktif, remote_device_id: {remote_device_id}"
            )
            # For now, assume it's already an entity ID
            # In a full implementation, this would map device IDs to entity IDs
            self.logger.debug(f"Converting remote device ID: {remote_device_id}")
            self.logger.debug("Şu anda doğrudan entity ID olarak kabul ediliyor")
            result = remote_device_id
            self.logger.info(
                f"convert_remote_device_to_entity başarıyla tamamlandı - sonuç: {result}"
            )
            return result
        except Exception as e:
            self.logger.error(
                f"Error converting remote device ID {remote_device_id}: {e}",
                exc_info=True,
            )
            self.logger.error(f"Hata bağlamı - remote_device_id: {remote_device_id}")
            return remote_device_id
        finally:
            self.logger.debug(
                "convert_remote_device_to_entity finally bloğu çalıştırıldı"
            )
