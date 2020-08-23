from pathlib import Path

from django_tea.config import ConfigField, Config as TeaConfig


class Config(TeaConfig):
    ENTRIES = {
        **TeaConfig.ENTRIES,
        "db_engine": ConfigField(section="database", option="engine"),
        "db_name": ConfigField(section="database", option="name"),
        "db_user": ConfigField(section="database", option="user"),
        "db_password": ConfigField(section="database", option="password"),
        "db_host": ConfigField(section="database", option="host"),
        "db_port": ConfigField(section="database", option="port", type=int),
    }

    def __init__(self):
        # Path to the configuration file
        self.config_dir = (Path("~").expanduser() / ".traktor").absolute()
        # Directory structure
        self.module_dir = Path(__file__).parent.absolute()

        # Database
        self.db_engine = "sqlite3"
        self.db_name = f"{self.config_dir}/traktor.db"
        self.db_user = None
        self.db_password = None
        self.db_host = None
        self.db_port = None

        super().__init__(config_file=self.config_dir / "traktor.ini")


config = Config()
