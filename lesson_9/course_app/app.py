from contextlib import asynccontextmanager
from fastapi import FastAPI
from course_app.routers.router import api
from .tools import load_cve_repo, cve_pull_scheduler


@asynccontextmanager
async def lifespan(_app: FastAPI):
    from .deps import get_settings
    from .db import Base, get_engine

    engine = get_engine(get_settings())

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    load_cve_repo()

    yield

    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)



app = FastAPI(lifespan=lifespan)
app.include_router(api)
