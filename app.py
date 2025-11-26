import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from src.application.domain.model.extraction_task import ExtractionTask
from src.ui.controller import extractions_controller
from src.di.di import Container

@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncIOMotorClient(os.getenv("MONGODB_URI", "mongodb://mongo:27017/extraction"))

    await init_beanie(database=client.ds_extraction, document_models=[ExtractionTask])

    yield

    client.close()

app = FastAPI(
    title="Extraction Service API",
    lifespan=lifespan
)

container = Container()

container.wire(modules=[extractions_controller])

app.container = container

app.include_router(extractions_controller.router)
