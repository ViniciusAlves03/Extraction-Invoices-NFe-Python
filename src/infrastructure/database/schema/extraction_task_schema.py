from typing import List, Optional, Annotated
from datetime import datetime
from beanie import Document
from pydantic import BaseModel, BeforeValidator
from decimal import Decimal
from bson import Decimal128


def convert_decimal_128(v):
    if isinstance(v, Decimal128):
        return v.to_decimal()
    return v

PyDecimal = Annotated[Decimal, BeforeValidator(convert_decimal_128)]

class ExtractionErrorSchema(BaseModel):
    item_identifier: str
    error_message: str

class ExtractedExpenseSchema(BaseModel):
    title: str
    description: Optional[str] = None
    quantity: PyDecimal
    unit_price: PyDecimal
    total_amount: PyDecimal
    date: Optional[str] = None
    categoryId: Optional[str] = None
    access_key: Optional[str] = None
    is_duplicate: bool = False
    duplicate_of_id: Optional[str] = None

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
