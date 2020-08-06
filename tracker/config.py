from pathlib import Path


class Config:
    def __init__(self):
        # Directory structure
        self.project_dir = Path(__file__).parent.parent.absolute()
        self.data_dir = self.project_dir / "data"
        self.app_dir = self.project_dir / "tracker"

    @property
    def db_path(self):
        return f"{self.data_dir}/tracker.db"

    @property
    def db_url(self):
        return f"sqlite:///{self.db_path}"


config = Config()
