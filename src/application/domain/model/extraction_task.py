import re
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator
from src.application.domain.validator.date_validator import DateValidator
from src.application.domain.validator.amount_validator import AmountValidator
from src.application.domain.utils.status_types import Status


class ExtractedExpense(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    quantity: Decimal = Field(...)
    unit_price: Decimal = Field(...)
    total_amount: Decimal = Field(...)
    date: Optional[str] = None
    categoryId: Optional[str] = None
    access_key: Optional[str] = None
    is_duplicate: bool = False
    duplicate_of_id: Optional[str] = None

    @field_validator('title', 'description', mode='before')
    @classmethod
    def clean_strings(cls, v):
        return str(v).strip() if v else None

    @field_validator('quantity', 'unit_price', 'total_amount', mode='before')
    @classmethod
    def parse_amount(cls, v):
        return AmountValidator.validate(v)

    @field_validator('date', mode='before')
    @classmethod
    def parse_date(cls, v):
        return DateValidator.validate_and_format(v)

    @field_validator('access_key', mode='before')
    @classmethod
    def clean_access_key(cls, v):
        if not v: return None
        return re.sub(r'\D', '', str(v))

class ExtractionError(BaseModel):
    item_identifier: str
    error_message: str

class ExtractionTask(BaseModel):
    id: Optional[str] = None
    filename: str
    file_type: str
    file_hash: Optional[str] = None
    status: Status = Status.PENDING
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    result_data: List[ExtractedExpense] = []
    error_report: List[ExtractionError] = []

    class Config:
        use_enum_values = True
