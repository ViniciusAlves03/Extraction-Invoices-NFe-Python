from typing import List, Optional
from datetime import datetime
from beanie import Document
from pydantic import BaseModel
from decimal import Decimal


class ExtractionErrorSchema(BaseModel):
    item_identifier: str
    error_message: str

class ExtractedExpenseSchema(BaseModel):
    title: str
    description: Optional[str] = None
    quantity: Decimal
    unit_price: Decimal
    total_amount: Decimal
    date: Optional[str] = None
    categoryId: Optional[str] = None

class ExtractionTaskSchema(Document):
    filename: str
    file_type: str
    file_hash: str
    status: str
    created_at: datetime
    updated_at: datetime
    result_data: List[ExtractedExpenseSchema] = []
    error_report: List[ExtractionErrorSchema] = []

    class Settings:
        name = "extraction_tasks"
