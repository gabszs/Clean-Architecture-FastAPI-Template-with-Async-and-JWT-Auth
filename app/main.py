from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import sessionmanager
from app.core.settings import settings
from app.routes.v1 import routers
from app.models import User
from app.models.models_enums import UserRoles
from app.core.security import get_password_hash


def init_app(init_db=True):
    lifespan = None

    if init_db:
        sessionmanager.init(settings.DATABASE_URL)

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            yield
            if sessionmanager._engine is not None:
                await sessionmanager.close()

    app = FastAPI(
        title="CV-Api",
        description="CV Management Web API with basic auth CRUD built by @GabrielCarvalho for my girlfriend",
        contact={
            "name": "Gabriel Carvalho",
            "url": "https://www.linkedin.com/in/gabzsz/",
            "email": "gabriel.carvalho@huawei.com",
        },
        summary="WebAPI built on best market practices such as TDD, Clean Architecture, Data Validation with Pydantic V2",
        lifespan=lifespan,
    )
    app.include_router(routers)

    return app


app = init_app()
