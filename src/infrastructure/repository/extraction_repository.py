from src.application.port.extraction_repository_interface import IExtractionRepository
from src.application.domain.model.extraction_task import ExtractionTask
from src.infrastructure.database.schema.extraction_task_schema import ExtractionTaskSchema
from src.infrastructure.entity.mapper.extraction_mapper import ExtractionMapper


class ExtractionRepository(IExtractionRepository):

    async def create(self, task: ExtractionTask) -> ExtractionTask:
        schema = ExtractionMapper.to_schema(task)
        await schema.create()
        return ExtractionMapper.to_domain(schema)
