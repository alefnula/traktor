import os
import json
from pathlib import Path

from sqlalchemy import orm

from traktor.models import Entry
from traktor.db.sync_db import SyncDB as DB
from traktor.engine.sync_engine.tag_mixin import TagMixin
from traktor.engine.sync_engine.timer_mixin import TimerMixin
from traktor.engine.sync_engine.db_mixin import DBMixin
from traktor.engine.sync_engine.config_mixin import ConfigMixin


class SyncEngine(TagMixin, TimerMixin, DBMixin, ConfigMixin):
    @classmethod
    def export(cls, session: orm.Session, path: Path):
        export = {
            "projects": [
                project.to_dict()
                for project in cls.project_list(session=session)
            ],
            "tasks": [
                task.to_dict()
                for task in cls.task_list(session=session, project=None)
            ],
            "entries": [
                entry.to_dict()
                for entry in DB.all(session=session, model=Entry)
            ],
        }
        os.makedirs(path.parent, exist_ok=True)
        path.write_text(json.dumps(export, indent=4), encoding="utf-8")


sync_engine = SyncEngine()
