"""Smartify yapılandırma akışı için şema oluşturucular.

Bu modül, SOLID prensiplerine uygun olarak şema oluşturma mantığını
ana yapılandırma akışından ayırarak şema oluşturma hizmetleri sunar.
"""

import logging

import voluptuous as vol  # type: ignore
from homeassistant.helpers import selector as sel  # type: ignore

from ...const import (
    CONF_NAME,
    CONF_OFF_SCRIPT,
    CONF_ON_SCRIPT,
    CONF_POWER_DEVICE_ID,
    CONF_REMOTE_DEVICE_ID,
)
from ...helpers.config_flow.schema_builder_interface import (
    ConfigSchemaBuilderInterface,
)
from ...helpers.logger.config_flow_logger import schema_builder_logging

_LOGGER = logging.getLogger(__name__)


class ConfigSchemaBuilder(ConfigSchemaBuilderInterface):
    """Yapılandırma formları için Tek Sorumluluk Prensibi'ne uygun şema
    oluşturucu.
    """

    @schema_builder_logging()
    def build_device_config_schema(
        self, power_devices: list, remote_devices: list
    ) -> vol.Schema:
        """Cihaz kurulumu için gelişmiş yapılandırma şemasını oluşturur.

        Args:
            power_devices: Mevcut güç sensörü cihazlarının listesi.
            remote_devices: Mevcut uzaktan kumanda cihazlarının listesi.

        Returns:
            vol.Schema: Cihaz seçimi alanlarına sahip yapılandırma şeması.
        """
        try:
            _LOGGER.info(
                "build_device_config_schema başlatıldı - kapsamlı loglama aktif"
            )
            _LOGGER.debug("Cihaz yapılandırma şeması oluşturuluyor.")
            _LOGGER.debug(
                f"Power devices sayısı: {len(power_devices)}, Remote devices sayısı: {len(remote_devices)}"
            )
            power_options = []
            for d in power_devices:
                device_id = str(d.get("id", "")).strip()
                device_name = str(d.get("name", "")).strip()
                label = (
                    device_name if device_name else device_id.replace("_", " ").title()
                )
                if device_id:
                    power_options.append({"value": device_id, "label": label})
                _LOGGER.debug(
                    "Eklendi güç cihazı seçeneği: {'value': '%s', 'label': '%s'}",
                    device_id,
                    label,
                )

            remote_options = []
            for d in remote_devices:
                device_id = str(d.get("id", "")).strip()
                device_name = str(d.get("name", "")).strip()
                label = (
                    device_name if device_name else device_id.replace("_", " ").title()
                )
                if device_id:
                    remote_options.append({"value": device_id, "label": label})
                _LOGGER.debug(
                    "Eklendi uzaktan kumanda cihazı seçeneği: {'value': '%s', 'label': '%s'}",
                    device_id,
                    label,
                )

            _LOGGER.debug("Schema dict oluşturuluyor")
            schema_dict = {
                vol.Required(CONF_NAME): sel.TextSelector(),
                vol.Required(CONF_POWER_DEVICE_ID): sel.SelectSelector(
                    {
                        "options": power_options,
                        "mode": "dropdown",
                        "multiple": False,
                    }
                ),
                vol.Required(CONF_REMOTE_DEVICE_ID): sel.SelectSelector(
                    {
                        "options": remote_options,
                        "mode": "dropdown",
                        "multiple": False,
                    }
                ),
            }
            schema = vol.Schema(schema_dict)
            _LOGGER.debug("Device configuration schema built successfully")
            _LOGGER.info("build_device_config_schema başarıyla tamamlandı")
            return schema
        except Exception as e:
            _LOGGER.error(
                "Error building device config schema: %s",
                e,
                exc_info=True,
            )
            _LOGGER.error(
                f"Hata bağlamı - power_devices: {len(power_devices) if power_devices else 0}, remote_devices: {len(remote_devices) if remote_devices else 0}"
            )
            return self._build_fallback_schema()
        finally:
            _LOGGER.debug("build_device_config_schema finally bloğu çalıştırıldı")

    @schema_builder_logging()
    def build_scripts_schema(self, device_scripts: list) -> vol.Schema:
        """Build the scripts selection schema.

        Args:
            device_scripts: List of available script dictionaries.

        Returns:
            vol.Schema: Scripts selection schema with dropdown selectors.
        """
        try:
            _LOGGER.debug(
                "Building scripts selection schema with %d scripts",
                len(device_scripts),
            )

            # Convert script dicts to SelectOptionDict format
            script_options = []
            for script in device_scripts:
                try:
                    script_alias = script.get("alias")
                    script_name = script.get("name", script["id"])

                    if (
                        script_alias
                        and isinstance(script_alias, str)
                        and script_alias.strip()
                    ):
                        label = script_alias.strip()
                    elif script_alias and isinstance(script_alias, dict):
                        friendly_name = script_alias.get("friendly_name")
                        if friendly_name:
                            label = str(friendly_name).strip()
                        else:
                            label = str(script_name).strip()
                    else:
                        label = str(script_name).strip()

                    if not label:
                        label = (
                            script["id"]
                            .replace("script.", "")
                            .replace("_", " ")
                            .title()
                        )

                    script_options.append(
                        {
                            "value": script["id"],
                            "label": label,
                        }
                    )
                except Exception as e:
                    _LOGGER.warning(
                        f"'{script['id']}' komut dosyası işlenirken hata: %s", e
                    )
                    fallback_label = script.get("name", script["id"]).strip()
                    if not fallback_label:
                        fallback_label = (
                            script["id"]
                            .replace("script.", "")
                            .replace("_", " ")
                            .title()
                        )

                    script_options.append(
                        {
                            "value": script["id"],
                            "label": fallback_label,
                        }
                    )

            schema_dict = {
                vol.Required(CONF_ON_SCRIPT): sel.SelectSelector(
                    {
                        "options": script_options,
                        "mode": "dropdown",
                        "multiple": False,
                    }
                ),
                vol.Required(CONF_OFF_SCRIPT): sel.SelectSelector(
                    {
                        "options": script_options,
                        "mode": "dropdown",
                        "multiple": False,
                    }
                ),
            }
            schema = vol.Schema(schema_dict)
            _LOGGER.debug("Komut dosyası şeması başarıyla oluşturuldu")
            return schema
        except Exception as e:
            _LOGGER.critical(
                "Komut dosyaları şeması oluşturulurken hata: %s. "
                "Dize girişlerine geri dönülüyor.",
                e,
                exc_info=True,
            )
            return vol.Schema(
                {
                    vol.Required(CONF_ON_SCRIPT): sel.TextSelector(),
                    vol.Required(CONF_OFF_SCRIPT): sel.TextSelector(),
                }
            )

    @schema_builder_logging()
    def _build_fallback_schema(self) -> vol.Schema:
        """Build a fallback schema for error recovery.

        Returns:
            vol.Schema: Basic input schema for fallback.
        """
        return vol.Schema(
            {
                vol.Required(CONF_NAME): sel.TextSelector(),
                vol.Required(CONF_POWER_DEVICE_ID): sel.TextSelector(),
                vol.Required(CONF_REMOTE_DEVICE_ID): sel.TextSelector(),
            }
        )
