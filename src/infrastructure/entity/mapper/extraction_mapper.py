from src.application.domain.model.extraction_task import ExtractionTask, ExtractedExpense, ExtractionError
from src.infrastructure.database.schema.extraction_task_schema import ExtractionTaskSchema, ExtractedExpenseSchema, ExtractionErrorSchema

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
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    total_amount=item.total_amount,
                    date=item.date,
                    categoryId=item.categoryId
                ) for item in schema.result_data
            ],
            error_report=[
                ExtractionError(
                    item_identifier=err.item_identifier,
                    error_message=err.error_message
                ) for err in schema.error_report
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
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    total_amount=item.total_amount,
                    date=item.date,
                    categoryId=item.categoryId
                ) for item in domain.result_data
            ],
            error_report=[
                ExtractionErrorSchema(
                    item_identifier=err.item_identifier,
                    error_message=err.error_message
                ) for err in domain.error_report
            ]
        )
