from src.application.domain.model.extraction_task import ExtractionTask, ExtractedExpense
from src.infrastructure.database.schema.extraction_task_schema import ExtractionTaskSchema, ExtractedExpenseSchema


class ExtractionMapper:

    @staticmethod
    def to_domain(schema: ExtractionTaskSchema) -> ExtractionTask:
        return ExtractionTask(
            id=str(schema.id),
            filename=schema.filename,
            status=schema.status,
            file_type=schema.file_type,
            created_at=schema.created_at,
            updated_at=schema.updated_at,
            result_data=[
                ExtractedExpense(
                    title=item.title,
                    description=item.description,
                    amount=item.amount,
                    date=item.date,
                    categoryId=item.categoryId
                ) for item in schema.result_data
            ]
        )

    @staticmethod
    def to_schema(domain: ExtractionTask) -> ExtractionTaskSchema:
        return ExtractionTaskSchema(
            filename=domain.filename,
            status=domain.status,
            file_type=domain.file_type,
            created_at=domain.created_at,
            updated_at=domain.updated_at,
            result_data=[
                ExtractedExpenseSchema(
                    title=item.title,
                    description=item.description,
                    amount=item.amount,
                    date=item.date,
                    categoryId=item.categoryId
                ) for item in domain.result_data
            ]
        )
