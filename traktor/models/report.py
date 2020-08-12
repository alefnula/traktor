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
    duration: int

    @property
    def key(self):
        return f"{self.project}-{self.task}"

    @property
    def humanized_time(self):
        return humanize(self.duration)

    def to_dict(self) -> dict:
        return {
            "project": self.project,
            "task": self.task,
            "duration": self.duration,
            "running_time": humanize(self.duration),
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Report":
        return cls(
            project=d["project"], task=d["task"], duration=d["duration"]
        )
