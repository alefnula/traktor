from dataclasses import dataclass

from traktor.config import ConfigKey
from traktor.models.model import VanillaModel, Column


@dataclass
class ConfigEntry(VanillaModel):

    Key = ConfigKey

    HEADERS = VanillaModel.HEADERS + [
        Column(title="Key", path="key.value"),
        Column(title="Value", path="value"),
    ]

    key: ConfigKey
    value: str

    def to_dict(self) -> dict:
        return {
            "key": self.key,
            "value": self.value,
        }
