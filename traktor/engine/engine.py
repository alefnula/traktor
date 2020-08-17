from traktor.engine.db_engine import DBEngine
from traktor.engine.config_engine import ConfigEngine
from traktor.engine.timer_mixin import TimerMixin


class Engine(TimerMixin):
    db = DBEngine()
    config = ConfigEngine()


engine = Engine()
