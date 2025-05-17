import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import sessionmanager
from app.core.settings import settings
from app.routes import app_routes


def init_app(init_db=True):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logging.getLogger("opentelemetry").propagate = False
    # logger.addHandler(logging.StreamHandler()) # use this to print the logs in the console

    lifespan = None

    if init_db:
        print(f"DATABASE_URL{settings.DATABASE_URL:}")
        sessionmanager.init(settings.DATABASE_URL)
        # sessionmanager.run_migrations()

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            logger.info(f"{settings.PROJECT_NAME} initialization started.")
            yield
            logger.info(f"{settings.PROJECT_NAME} shutdown completed.")
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
    app.include_router(app_routes)

    return app


app = init_app()
