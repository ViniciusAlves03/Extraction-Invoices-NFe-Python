from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from src.infrastructure.database.schema.extraction_task_schema import ExtractionTaskSchema


class MongoConnection:
    _client: AsyncIOMotorClient = None

    @classmethod
    async def connect(cls, uri):
        cls._client = AsyncIOMotorClient(uri)

        await init_beanie(
            database=cls._client.get_default_database(),
            document_models=[ExtractionTaskSchema]
        )
        print(f"✅ Connected to MongoDB: {uri}")

    @classmethod
    async def disconnect(cls):
        if cls._client:
            cls._client.close()
            print("🛑 Connection to MongoDB closed.")
