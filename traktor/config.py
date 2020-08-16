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


class ConfigKey(str, enum.Enum):
    format = "format"
    timezone = "timezone"
    prod_db_path = "prod_db_path"
    test_db_path = "test_db_path"
    use_test_db = "use_test_db"
    url = "url"


class Config:
    Key = ConfigKey
    Format = Format

    section = "traktor"

    def __init__(self):
        # Path to the configuration file
        self.config_dir = (Path("~").expanduser() / ".traktor").absolute()
        self.config_path = self.config_dir / "traktor.ini"
        # Directory structure
        self.module_dir = Path(__file__).parent.absolute()

        # Configuration
        self.format: Format = Format.text
        self.timezone = tzlocal.get_localzone()
        self.prod_db_path = f"{self.config_dir}/traktor.db"
        self.test_db_path = f"{self.config_dir}/traktor-test.db"
        self.use_test_db = False
        self.url = "http://127.0.0.1:5000"

        # Load the values from configuration file
        self.load()

    def load(self):
        """Load configuration."""
        if not os.path.isfile(self.config_path):
            return

        cp = ConfigParser()
        cp.read(self.config_path)

        if cp.has_option(self.section, self.Key.format):
            try:
                self.format = Format(cp.get(self.section, self.Key.format))
            except Exception:
                pass

        if cp.has_option(self.section, self.Key.timezone):
            try:
                self.timezone = pytz.timezone(
                    cp.get(self.section, self.Key.timezone)
                )
            except Exception:
                pass

        if cp.has_option(self.section, self.Key.prod_db_path):
            self.prod_db_path = cp.get(self.section, self.Key.prod_db_path)

        if cp.has_option(self.section, self.Key.test_db_path):
            self.test_db_path = cp.get(self.section, self.Key.test_db_path)

        if cp.has_option(self.section, self.Key.use_test_db):
            self.use_test_db = cp.getboolean(
                self.section, self.Key.use_test_db
            )

        if cp.has_option(self.section, self.Key.url):
            self.url = cp.get(self.section, self.Key.url)

    def save(self):
        # Create if it doesn't exist
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        cp = ConfigParser()
        # If it already exists read the values
        if os.path.isfile(self.config_path):
            cp.read(self.config_path)

        if not cp.has_section(self.section):
            cp.add_section(self.section)

        # Set the values from configuration
        cp.set(self.section, self.Key.format, self.format)
        cp.set(self.section, self.Key.timezone, self.timezone.zone)
        cp.set(self.section, self.Key.prod_db_path, self.prod_db_path)
        cp.set(self.section, self.Key.test_db_path, self.test_db_path)
        cp.set(self.section, self.Key.use_test_db, str(self.use_test_db))
        cp.set(self.section, self.Key.url, self.url)

        with io.open(self.config_path, "w") as f:
            cp.write(f)

    @property
    def db_path(self):
        return self.test_db_path if self.use_test_db else self.prod_db_path

    @property
    def db_url(self):
        return f"sqlite:///{self.db_path}"


config = Config()
