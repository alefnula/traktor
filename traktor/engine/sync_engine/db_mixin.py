import os
import subprocess

from alembic.config import Config
from alembic import command

from traktor.config import config
from traktor import filesystem as fs


class DBMixin:
    @staticmethod
    def __ensure_db_directory():
        os.makedirs(os.path.dirname(config.db_path), exist_ok=True)

    @classmethod
    def db_revision(cls, revision: str):
        """Create a new migration."""
        cls.__ensure_db_directory()

        alembic_cfg = Config(config.module_dir / "alembic.ini")

        with fs.goto(config.module_dir.parent):
            command.revision(
                config=alembic_cfg, message=revision, autogenerate=True
            )

    @classmethod
    def db_migrate(cls, revision: str = "head"):
        """Run migrations."""
        cls.__ensure_db_directory()

        if revision == "head":
            direction = "upgrade"
        else:
            destination = int(revision, 10)
            current = int(
                subprocess.check_output(["alembic", "current"])[:4], 10
            )
            if destination > current:
                direction = "upgrade"
            else:
                direction = "downgrade"

        alembic_cfg = Config(config.module_dir / "alembic.ini")

        with fs.goto(config.module_dir.parent):
            if direction == "upgrade":
                command.upgrade(config=alembic_cfg, revision=revision)
            else:
                command.downgrade(config=alembic_cfg, revision=revision)

    @classmethod
    def db_reset(cls):
        """Reset migrations - delete all tables."""
        cls.__ensure_db_directory()

        alembic_cfg = Config(config.module_dir / "alembic.ini")
        with fs.goto(config.module_dir.parent):
            command.downgrade(config=alembic_cfg, revision="0000")

    @classmethod
    def ensure_db(cls):
        """Ensure that the database exists and that it's migrated."""
        cls.db_migrate(revision="head")
