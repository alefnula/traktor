from dataclasses import dataclass

from django_tea.table import Column
from django_tea import timestamp as ts
from django_tea.models import VanillaModel


@dataclass
class Report(VanillaModel):
    HEADERS = VanillaModel.HEADERS + [
        Column(title="Project", path="project"),
        Column(title="Task", path="task"),
        Column(title="Time", path="running_time", align=Column.Align.center),
    ]

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
            "project": self.project,
            "task": self.task,
            "duration": self.duration,
            "running_time": ts.humanize(self.duration),
        }
