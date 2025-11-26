from typing import List
from datetime import datetime
from beanie import Document
from pydantic import BaseModel
from decimal import Decimal


class ExtractedExpenseSchema(BaseModel):
    title: str
    description: str | None
    amount: Decimal
    date: str | None
    categoryId: str | None

class ExtractionTaskSchema(Document):
    filename: str
    status: str
    file_type: str
    created_at: datetime
    updated_at: datetime
    result_data: List[ExtractedExpenseSchema] = []

    class Settings:
        name = "extraction_tasks"
