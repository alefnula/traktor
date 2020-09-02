from dataclasses import dataclass

from tea import timestamp as ts
from tea_console.table import Column
from tea_django.models import VanillaModel


@dataclass
class Report(VanillaModel):
    HEADERS = VanillaModel.HEADERS + [
        Column(title="User", path="user"),
        Column(title="Project", path="project"),
        Column(title="Task", path="task"),
        Column(title="Time", path="running_time", align=Column.Align.center),
    ]

    user: str
    project: str
    task: str
    duration: int

    @property
    def key(self):
        return f"{self.project}-{self.task}"

    @property
    def running_time(self):
        return ts.humanize(self.duration)

    def to_dict(self) -> dict:
        return {
            "user": self.user,
            "project": self.project,
            "task": self.task,
            "duration": self.duration,
            "running_time": ts.humanize(self.duration),
        }
