import os
import json
from pathlib import Path

from django_tea import serde
from django.core.management import execute_from_command_line

from traktor.config import config
from traktor.models import Project, Task, Entry


class DBEngine:
    @staticmethod
    def ensure():
        os.makedirs(os.path.dirname(config.db_path), exist_ok=True)
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
            project = serde.json_dict_to_model(model=Project, d=d)
            project.save()

        for d in data["tasks"]:
            task = serde.json_dict_to_model(model=Task, d=d)
            task.save()

        for d in data["entries"]:
            entry = serde.json_dict_to_model(model=Entry, d=d)
            entry.save()
