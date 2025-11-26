from typing import Optional, List, Any
from datetime import datetime
from decimal import Decimal
from beanie import Document
from pydantic import BaseModel, Field, field_validator

from src.application.domain.validator.date_validator import DateValidator
from src.application.domain.validator.amount_validator import MoneyValidator

class ExtractedExpense(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Título da despesa")
    description: Optional[str] = Field(None, max_length=255)
    amount: Decimal = Field(...)
    date: Optional[str] = None
    categoryId: Optional[str] = None

    @field_validator('title', 'description', mode='before')
    @classmethod
    def clean_strings(cls, v):
        if v is None:
            return None
        return str(v).strip()

    @field_validator('amount', mode='before')
    @classmethod
    def parse_amount(cls, v):
        return MoneyValidator.validate(v)

    @field_validator('date', mode='before')
    @classmethod
    def parse_date(cls, v):
        return DateValidator.validate_and_format(v)

class ExtractionTask(Document):
    filename: str
    status: str
    file_type: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    result_data: List[ExtractedExpense] = []
    class Settings:
        name = "extraction_tasks"
