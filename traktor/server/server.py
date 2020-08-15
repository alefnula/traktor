from fastapi import FastAPI

from traktor.server import api
from traktor.db.async_db import async_db as db


server = FastAPI()

server.mount("/api/v0", api.app)


@server.on_event("startup")
async def startup():
    await db.connect()


@server.on_event("shutdown")
async def shutdown():
    await db.disconnect()
