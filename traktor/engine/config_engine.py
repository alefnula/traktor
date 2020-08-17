from typing import List

from django_tea.config import ConfigEntry

from traktor import errors
from traktor.config import config


class ConfigEngine:
    @staticmethod
    def list() -> List[ConfigEntry]:
        """List all configuration values."""
        return config.entries

    @classmethod
    def set(cls, key: str, value: str):
        try:
            config.set(field=key, value=value)
            config.save()
            return cls.list()
        except Exception as e:
            raise errors.InvalidConfiguration(key=key, value=value, error=e)
