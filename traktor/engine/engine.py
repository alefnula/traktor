from traktor.engine.db_engine import DBEngine
from traktor.engine.timer_mixin import TimerMixin


class Engine(TimerMixin):
    db = DBEngine()


engine = Engine()
