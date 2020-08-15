from typing import List
from traktor.models import Entry, Report
from traktor.engine.async_engine.task_mixin import TaskMixin


class TimerMixin(TaskMixin):
    # Timer

    @classmethod
    def start(cls, project_id: str, task_id: str) -> Entry:
        # First see if there are running timers
        pass

    @staticmethod
    def stop() -> List[Entry]:
        pass

    @staticmethod
    def status() -> List[Entry]:
        pass

    @staticmethod
    def _make_report(entries: List[Entry]):
        pass

    @classmethod
    def today(cls):
        pass

    @classmethod
    def report(cls, days: int) -> List[Report]:
        pass
