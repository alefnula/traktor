import os
import json
from pathlib import Path

from sqlalchemy import orm

from traktor.models import DB, Entry
from traktor.engine.tag_mixin import TagMixin
from traktor.engine.timer_mixin import TimerMixin
from traktor.engine.db_mixin import DBMixin
from traktor.engine.config_mixin import ConfigMixin


class Engine(TagMixin, TimerMixin, DBMixin, ConfigMixin):
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


engine = Engine()
