from decimal import Decimal
from src.application.port.extraction_repository_interface import IExtractionRepository
from src.application.domain.model.extraction_task import ExtractionTask, ExtractedExpense
from src.infrastructure.database.schema.extraction_task_schema import ExtractionTaskSchema
from src.infrastructure.entity.mapper.extraction_mapper import ExtractionMapper


class ExtractionRepository(IExtractionRepository):

    async def create(self, task: ExtractionTask) -> ExtractionTask:
        schema = ExtractionMapper.to_schema(task)
        await schema.create()
        return ExtractionMapper.to_domain(schema)

    async def find_by_hash(self, file_hash: str) -> ExtractionTask | None:
        schema = await ExtractionTaskSchema.find_one(
            ExtractionTaskSchema.file_hash == file_hash,
            ExtractionTaskSchema.status == "COMPLETED"
        )
        if schema:
            return ExtractionMapper.to_domain(schema)
        return None

    async def find_duplicate_by_key(self, access_key: str, amount: Decimal) -> tuple[str, ExtractedExpense] | None:
        if not access_key: return None

        task_schema = await ExtractionTaskSchema.find_one(
            {
                "result_data": {
                    "$elemMatch": {
                        "access_key": access_key,
                        "total_amount": amount
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
                categoryId=found_item_schema.categoryId,
                access_key=found_item_schema.access_key
            )
            return str(task_schema.id), domain_item

        return None
