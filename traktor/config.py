import io
import os
import enum
from pathlib import Path
from configparser import ConfigParser

import pytz
import tzlocal


class Format(str, enum.Enum):
    text = "text"
    json = "json"


class Config:
    Format = Format

    def __init__(self):
        # Path to the configuration file
        self.config_dir = (Path("~").expanduser() / ".traktor").absolute()
        self.config_path = self.config_dir / "traktor.ini"
        self.db_path = f"{self.config_dir}/traktor.db"

        # Directory structure
        self.module_dir = Path(__file__).parent.absolute()

        self.format: Format = Format.text
        self.timezone = tzlocal.get_localzone()

        # Load the values from configuration
        self.load()

    def load(self):
        """Load configuration."""
        if not os.path.isfile(self.config_path):
            return

        cp = ConfigParser()
        cp.read(self.config_path)

        if cp.has_option("traktor", "format"):
            try:
                self.format = Format(cp.get("traktor", "format"))
            except Exception:
                pass

        if cp.has_option("traktor", "db_path"):
            self.db_path = cp.get("traktor", "db_path")

        if cp.has_option("traktor", "timezone"):
            try:
                self.timezone = pytz.timezone(cp.get("traktor", "timezone"))
            except Exception:
                pass

    def save(self):
        # Create if it doesn't exist
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        cp = ConfigParser()
        # If it already exists read the values
        if os.path.isfile(self.config_path):
            cp.read(self.config_path)

        if not cp.has_section("traktor"):
            cp.add_section("traktor")

        # Set the values from configuration
        cp.set("traktor", "format", self.format.value)
        cp.set("traktor", "db_path", self.db_path)
        cp.set("traktor", "timezone", self.timezone.zone)

        with io.open(self.config_path, "w") as f:
            cp.write(f)

    @property
    def db_url(self):
        return f"sqlite:///{self.db_path}"


config = Config()
