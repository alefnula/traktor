from traktor.engine.async_engine.tag_mixin import TagMixin
from traktor.engine.async_engine.timer_mixin import TimerMixin


class AsyncEngine(TagMixin, TimerMixin):
    pass


async_engine = AsyncEngine()
