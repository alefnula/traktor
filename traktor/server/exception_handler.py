from fastapi import Request
from fastapi.responses import JSONResponse

from traktor import errors


async def traktor_exception_handler(
    request: Request, exc: errors.TraktorError
):
    if isinstance(exc, (errors.ObjectNotFound, errors.MultipleObjectsFound)):
        return JSONResponse(status_code=404, content={"detail": exc.message})
    if isinstance(exc, errors.ObjectAlreadyExists):
        return JSONResponse(status_code=409, content={"detail": exc.message})
    else:
        return JSONResponse(status_code=500, content={"detail": exc.message})
