from dataclasses import dataclass

from traktor.timestamp import humanize
from traktor.models.model import VanillaModel, Column


@dataclass
class Report(VanillaModel):
    HEADERS = VanillaModel.HEADERS + [
        Column(title="Project", path="project"),
        Column(title="Task", path="task"),
        Column(title="Time", path="humanized_time", align=Column.Align.center),
    ]

    project: str
    task: str
    time: int

    @property
    def key(self):
        return f"{self.project}-{self.task}"

    @property
    def humanized_time(self):
        return humanize(self.time)

    def to_dict(self) -> dict:
        return {
            "project": self.project,
            "task": self.task,
            "time": self.time,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Report":
        return cls(project=d["project"], task=d["task"], time=d["time"])
