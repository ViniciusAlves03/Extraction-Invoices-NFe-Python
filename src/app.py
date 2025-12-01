from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.ui.controller import extractions_controller
from src.di.di import Container
from src.infrastructure.database.mongo_connection import MongoConnection
from src.utils.config import Settings
from src.application.domain.exception import DomainException
from src.utils.strings import Strings
from src.ui.exception.exception_handler import global_exception_handler


def create_app(settings: Settings) -> FastAPI:

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await MongoConnection.connect(uri=settings.MONGODB_URI)

        yield

        await MongoConnection.disconnect()

    app = FastAPI(
        title=Strings.APP['TITLE'],
        lifespan=lifespan)

    app.add_exception_handler(DomainException, global_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)

    container = Container()

    container.wire(modules=[extractions_controller])
    app.container = container

    app.include_router(extractions_controller.router)

    return app
