from typing import List

import pytz

from traktor import errors
from traktor.config import config, Format
from traktor.models import ConfigEntry, ConfigKey


class ConfigMixin:
    @staticmethod
    def config_list() -> List[ConfigEntry]:
        """List all configuration values."""
        return [
            ConfigEntry(key=ConfigKey.format, value=config.format.value),
            ConfigEntry(key=ConfigKey.timezone, value=config.timezone.zone),
            ConfigEntry(key=ConfigKey.prod_db_path, value=config.prod_db_path),
            ConfigEntry(key=ConfigKey.test_db_path, value=config.test_db_path),
            ConfigEntry(key=ConfigKey.use_test_db, value=config.use_test_db),
        ]

    @classmethod
    def config_set(cls, key: ConfigKey, value: str):
        if key == ConfigKey.format:
            try:
                config.format = Format(value)
            except Exception:
                valid_values = ", ".join([f.value for f in Format])
                raise errors.InvalidConfiguration(
                    value=value, valid_values=valid_values
                )
        elif key == ConfigKey.timezone:
            try:
                config.timezone = pytz.timezone(value)
            except Exception:
                raise errors.InvalidConfiguration(value=value)
        elif key == ConfigKey.prod_db_path:
            config.prod_db_path = value
        elif key == ConfigKey.test_db_path:
            config.test_db_path = value
        elif key == ConfigKey.use_test_db:
            config.use_test_db = value.lower() in ("true", "on")

        config.save()

        return cls.config_list()
