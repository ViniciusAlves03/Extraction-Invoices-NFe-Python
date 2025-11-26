from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator
from src.application.domain.validator.date_validator import DateValidator
from src.application.domain.validator.amount_validator import AmountValidator


class ExtractedExpense(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    amount: Decimal = Field(...)
    date: Optional[str] = None
    categoryId: Optional[str] = None

    @field_validator('title', 'description', mode='before')
    @classmethod
    def clean_strings(cls, v):
        return str(v).strip() if v else None

    @field_validator('amount', mode='before')
    @classmethod
    def parse_amount(cls, v):
        return AmountValidator.validate(v)

    @field_validator('date', mode='before')
    @classmethod
    def parse_date(cls, v):
        return DateValidator.validate_and_format(v)

class ExtractionTask(BaseModel):
    id: Optional[str] = None
    filename: str
    status: str
    file_type: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    result_data: List[ExtractedExpense] = []
