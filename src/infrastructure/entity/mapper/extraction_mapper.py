from src.application.domain.model import (ExtractionTask, ExtractedExpense, ExtractionError)
from src.infrastructure.database.schema import (ExtractionTaskSchema, ExtractedExpenseSchema, ExtractionErrorSchema)


class ExtractionMapper:

    @staticmethod
    def to_domain(schema: ExtractionTaskSchema) -> ExtractionTask:
        return ExtractionTask(
            id=str(schema.id),
            filename=schema.filename,
            file_type=schema.file_type,
            file_hash=schema.file_hash,
            status=schema.status,
            user_id=schema.user_id,
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
                    category_id=item.category_id,
                    access_key=item.access_key,
                    is_duplicate=item.is_duplicate,
                    duplicate_of_id=item.duplicate_of_id
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
            file_type=domain.file_type,
            file_hash=domain.file_hash,
            status=domain.status,
            user_id=domain.user_id,
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
                    category_id=item.category_id,
                    access_key=item.access_key,
                    is_duplicate=item.is_duplicate,
                    duplicate_of_id=item.duplicate_of_id
                ) for item in domain.result_data
            ],
            error_report=[
                ExtractionErrorSchema(
                    item_identifier=err.item_identifier,
                    error_message=err.error_message
                ) for err in domain.error_report
            ]
        )
