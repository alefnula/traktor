from pathlib import Path

from django_tea.config import ConfigField, Config as TeaConfig


class Config(TeaConfig):
    ENTRIES = {
        **TeaConfig.ENTRIES,
        "prod_db_path": ConfigField(section="database", option="prod_db_path"),
        "test_db_path": ConfigField(section="database", option="test_db_path"),
        "use_test_db": ConfigField(
            section="database", option="use_test_db", type=bool
        ),
        "server_url": ConfigField(section="server", option="url"),
    }

    def __init__(self):
        # Path to the configuration file
        self.config_dir = (Path("~").expanduser() / ".traktor").absolute()
        super().__init__(config_file=self.config_dir / "traktor.ini")

        # Directory structure
        self.module_dir = Path(__file__).parent.absolute()

        # Database
        self.prod_db_path = f"{self.config_dir}/traktor.db"
        self.test_db_path = f"{self.config_dir}/traktor-test.db"
        self.use_test_db = False

        # Server
        self.server_url = "127.0.0.1:5000"

        # Load the values from configuration file
        self.load()

    @property
    def db_path(self):
        return self.test_db_path if self.use_test_db else self.prod_db_path


config = Config()
