import functools
from typing import Any

from fastapi import Response

from traktor.output import json_dumps


class JSONResponse(Response):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        return json_dumps(content, encoding="utf-8", indent=None)


def tjson(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> JSONResponse:
        return JSONResponse(await func(*args, **kwargs))

    return wrapper
