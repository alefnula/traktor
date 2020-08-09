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
            ConfigEntry(key=ConfigEntry.Key.format, value=config.format.value),
            ConfigEntry(key=ConfigEntry.Key.db_path, value=config.db_path),
            ConfigEntry(
                key=ConfigEntry.Key.timezone, value=config.timezone.zone
            ),
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

        elif key == ConfigKey.db_path:
            config.db_path = value
        elif key == ConfigKey.timezone:
            try:
                config.timezone = pytz.timezone(value)
            except Exception:
                raise errors.InvalidConfiguration(value=value)

        config.save()

        return cls.config_list()
