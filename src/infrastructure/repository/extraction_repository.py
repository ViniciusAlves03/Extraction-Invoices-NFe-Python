from decimal import Decimal
from beanie import PydanticObjectId
from beanie.operators import In
from src.application.port import IExtractionRepository
from src.application.domain.model import (ExtractionTask, ExtractedExpense, TaskFilter)
from src.infrastructure.database.schema import ExtractionTaskSchema
from src.infrastructure.entity.mapper import ExtractionMapper


class ExtractionRepository(IExtractionRepository):

    async def create(self, task: ExtractionTask) -> ExtractionTask:
        schema = ExtractionMapper.to_schema(task)
        await schema.create()
        return ExtractionMapper.to_domain(schema)

    async def find_all(self, user_id: str, filters: TaskFilter) -> list[ExtractionTask]:
        query = {"userId": user_id}

        if filters.status:
            query["status"] = filters.status

        if filters.title:
            query["resultData.title"] = {"$regex": filters.title, "$options": "i"}

        if filters.date:
            query["resultData.date"] = filters.date

        if filters.category_id:
            query["resultData.category_id"] = filters.category_id

        if filters.is_duplicate is not None:
            query["resultData.isDuplicate"] = filters.is_duplicate

        schemas = await ExtractionTaskSchema.find(query).to_list()
        return [ExtractionMapper.to_domain(s) for s in schemas]

    async def find_by_id(self, id: str) -> ExtractionTask | None:
        try:
            oid = PydanticObjectId(id)
        except:
            return None

        schema = await ExtractionTaskSchema.get(oid)
        if schema:
            return ExtractionMapper.to_domain(schema)
        return None

    async def find_by_hash(self, user_id: str, file_hash: str) -> ExtractionTask | None:
        schema = await ExtractionTaskSchema.find_one(
            ExtractionTaskSchema.file_hash == file_hash,
            ExtractionTaskSchema.user_id == user_id,
            In(ExtractionTaskSchema.status, ["COMPLETED", "PENDING", "PARTIAL_SUCCESS"])
        ).project(ExtractionTaskSchema)
        if schema:
            return ExtractionMapper.to_domain(schema)
        return None

    async def find_duplicate_by_key(self, user_id: str, access_key: str, amount: Decimal) -> tuple[str, ExtractedExpense] | None:
        if not access_key: return None

        task_schema = await ExtractionTaskSchema.find_one(
            {
                "userId": user_id,
                "resultData": {
                    "$elemMatch": {
                        "accessKey": access_key,
                        "totalAmount": amount
                    }
                },
                "status": "COMPLETED"
            }
        )

        if not task_schema:
            return None

        found_item_schema = next(
            (item for item in task_schema.result_data
             if item.access_key == access_key and item.total_amount == amount),
            None
        )

        if found_item_schema:
            domain_item = ExtractedExpense(
                title=found_item_schema.title,
                description=found_item_schema.description,
                quantity=found_item_schema.quantity,
                unit_price=found_item_schema.unit_price,
                total_amount=found_item_schema.total_amount,
                date=found_item_schema.date,
                category_id=found_item_schema.category_id,
                access_key=found_item_schema.access_key
            )
            return str(task_schema.id), domain_item

        return None
