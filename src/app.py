from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.ui.controller import extractions_controller
from src.di.di import Container
from src.infrastructure.database.mongo_connection import MongoConnection
from src.utils.config import Settings


def create_app(settings: Settings) -> FastAPI:

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await MongoConnection.connect(uri=settings.MONGODB_URI)

        yield

        await MongoConnection.disconnect()

    app = FastAPI(
        title="Extraction Service API",
        lifespan=lifespan
    )

    container = Container()

    container.wire(modules=[extractions_controller])
    app.container = container

    app.include_router(extractions_controller.router)

    return app
