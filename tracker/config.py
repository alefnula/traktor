import io
import os
import enum
from pathlib import Path
from configparser import ConfigParser

import pytz
import tzlocal


class Format(enum.Enum):
    text = "text"
    json = "json"


class Config:
    Format = Format

    def __init__(self):
        # Path to the configuration file
        self.config_path = (
            Path("~").expanduser() / ".tracker" / "tracker.ini"
        ).absolute()
        self.profile = "default"

        # Directory structure
        self.project_dir = Path(__file__).parent.parent.absolute()
        self.data_dir = self.project_dir / "data"
        self.app_dir = self.project_dir / "tracker"

        self.format: Format = Format.text
        self.db_path = f"{self.data_dir}/tracker.db"
        self.timezone = tzlocal.get_localzone()
        # Load the values from configuration
        self.load()

    def load(self):
        """Load configuration."""
        if not os.path.isfile(self.config_path):
            return

        cp = ConfigParser()
        cp.read(self.config_path)

        if cp.has_option(self.profile, "format"):
            try:
                self.format = Format(cp.get(self.profile, "format"))
            except Exception:
                pass

        if cp.has_option(self.profile, "db_path"):
            self.db_path = cp.get(self.profile, "db_path")

        if cp.has_option(self.profile, "timezone"):
            try:
                self.timezone = pytz.timezone(cp.get(self.profile, "timezone"))
            except Exception:
                pass

    def save(self):
        # Create if it doesn't exist
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        cp = ConfigParser()
        # If it already exists read the values
        if os.path.isfile(self.config_path):
            cp.read(self.config_path)

        if not cp.has_section(self.profile):
            cp.add_section(self.profile)

        # Set the values from configuration
        cp.set(self.profile, "format", self.format.value)
        cp.set(self.profile, "db_path", self.db_path)
        cp.set(self.profile, "timezone", self.timezone.zone)

        with io.open(self.config_path, "w") as f:
            cp.write(f)

    @property
    def db_url(self):
        return f"sqlite:///{self.db_path}"


config = Config()
