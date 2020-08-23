import os
import json
from pathlib import Path

from tea import serde
from django.core.management import execute_from_command_line

from traktor.config import config
from traktor.models import Project, Task, Entry


class DBEngine:
    @staticmethod
    def ensure():
        if config.db_engine == "sqlite3":
            os.makedirs(os.path.dirname(config.db_name), exist_ok=True)
        execute_from_command_line(["traktor", "migrate", "-v", "0"])

    @staticmethod
    def export(path: Path):
        export = {
            "projects": [
                project.column_dict() for project in Project.objects.all()
            ],
            "tasks": [task.column_dict() for task in Task.objects.all()],
            "entries": [entry.column_dict() for entry in Entry.objects.all()],
        }
        os.makedirs(path.parent, exist_ok=True)
        path.write_text(serde.json_dumps(export, indent=4), encoding="utf-8")

    @staticmethod
    def load(path: Path):
        data = json.loads(path.read_text(encoding="utf-8"))

        for d in data["projects"]:
            project = Project.from_dict(d)
            project.save()

        for d in data["tasks"]:
            task = Task.from_dict(d)
            task.save()

        for d in data["entries"]:
            entry = Entry.from_dict(d)
            entry.save()
