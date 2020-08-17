from pathlib import Path

import pytz
import tzlocal

from django_tea.enums import ConsoleFormat
from django_tea.config import ConfigField, Config as TeaConfig

from traktor import errors


class Config(TeaConfig):
    Format = ConsoleFormat

    ENTRIES = {
        "format": ConfigField(
            section="traktor",
            option="format",
            to_value=ConsoleFormat,
            to_string=lambda v: v.value,
        ),
        "timezone": ConfigField(
            section="traktor",
            option="timezone",
            to_value=pytz.timezone,
            to_string=lambda v: v.zone,
        ),
        "prod_db_path": ConfigField(section="database", option="prod_db_path"),
        "test_db_path": ConfigField(section="database", option="test_db_path"),
        "use_test_db": ConfigField(
            section="database", option="use_test_db", type=bool
        ),
        "url": ConfigField(section="server", option="url"),
    }

    def __init__(self):
        # Path to the configuration file
        self.config_dir = (Path("~").expanduser() / ".traktor").absolute()
        super().__init__(config_file=self.config_dir / "traktor.ini")
        # Directory structure
        self.module_dir = Path(__file__).parent.absolute()

        # Configuration
        self.format: ConsoleFormat = ConsoleFormat.text
        self.timezone = tzlocal.get_localzone()
        self.prod_db_path = f"{self.config_dir}/traktor.db"
        self.test_db_path = f"{self.config_dir}/traktor-test.db"
        self.use_test_db = False
        self.url = "http://127.0.0.1:5000"

        # Load the values from configuration file
        try:
            self.load()
        except ValueError as e:
            raise errors.TraktorError(str(e))

    @property
    def db_path(self):
        return self.test_db_path if self.use_test_db else self.prod_db_path


config = Config()
