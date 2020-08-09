from traktor.engine.tag_mixin import TagMixin
from traktor.engine.timer_mixin import TimerMixin
from traktor.engine.db_mixin import DBMixin
from traktor.engine.config_mixin import ConfigMixin


class Engine(TagMixin, TimerMixin, DBMixin, ConfigMixin):
    pass


engine = Engine()
