import os
import json
from pathlib import Path

from sqlalchemy import orm

from traktor import timestamp as ts
from traktor.output import json_dumps
from traktor.models import Project, Task, Tag, Entry
from traktor.db.sync_db import sync_db as db
from traktor.engine.sync_engine.tag_mixin import TagMixin
from traktor.engine.sync_engine.timer_mixin import TimerMixin
from traktor.engine.sync_engine.db_mixin import DBMixin
from traktor.engine.sync_engine.config_mixin import ConfigMixin


class SyncEngine(TagMixin, TimerMixin, DBMixin, ConfigMixin):
    @classmethod
    def export(cls, session: orm.Session, path: Path):
        export = {
            "projects": [
                project.column_dict()
                for project in cls.project_list(session=session)
            ],
            "tags": [
                tag.column_dict() for tag in cls.tag_list(session=session)
            ],
            "tasks": [
                task.column_dict()
                for task in cls.task_list(session=session, project_id=None)
            ],
            "entries": [
                entry.column_dict()
                for entry in db.all(session=session, model=Entry)
            ],
        }
        os.makedirs(path.parent, exist_ok=True)
        path.write_text(json_dumps(export, indent=4), encoding="utf-8")

    @classmethod
    def load(cls, session: orm.Session, path: Path):
        data = json.loads(path.read_text(encoding="utf-8"))

        for d in data["projects"]:
            project = Project(
                id=d["id"],
                name=d["name"],
                slug=d["slug"],
                color=d["color"],
                created_on=ts.str_to_dt(d["created_on"]),
                updated_on=ts.str_to_dt(d["updated_on"]),
            )
            db.save(session=session, obj=project)

        for d in data["tags"]:
            tag = Tag(
                id=d["id"],
                name=d["name"],
                slug=d["slug"],
                color=d["color"],
                created_on=ts.str_to_dt(d["created_on"]),
                updated_on=ts.str_to_dt(d["updated_on"]),
            )
            db.save(session=session, obj=tag)

        for d in data["tasks"]:
            task = Task(
                id=d["id"],
                project_id=d["project_id"],
                name=d["name"],
                slug=d["slug"],
                color=d["color"],
                default=d["default"],
                created_on=ts.str_to_dt(d["created_on"]),
                updated_on=ts.str_to_dt(d["updated_on"]),
            )
            db.save(session=session, obj=task)

        for d in data["entries"]:
            entry = Entry(
                id=d["id"],
                project_id=d["project_id"],
                task_id=d["task_id"],
                description=d["description"],
                notes=d["notes"],
                start_time=ts.str_to_dt(d["start_time"]),
                end_time=ts.str_to_dt(d["end_time"]),
                duration=d["duration"],
                created_on=ts.str_to_dt(d["created_on"]),
                updated_on=ts.str_to_dt(d["updated_on"]),
            )
            db.save(session=session, obj=entry)


sync_engine = SyncEngine()
