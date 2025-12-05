import re
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from src.application.domain.utils import Status
from src.application.domain.validator import DateValidator


class TaskFilter(BaseModel):
    status: Optional[str] = Field(
        None,
        description="Filter tasks by their processing status (e.g., PENDING, COMPLETED, FAILED).",
        examples=["COMPLETED"]
    )
    title: Optional[str] = Field(
        None,
        description="Filter by product title or description (partial match).",
        examples=["Gasoline"]
    )
    date: Optional[str] = Field(
        None,
        description="Filter by exact date in YYYY-MM-DD format.",
        examples=["2023-10-25"]
    )
    category_id: Optional[str] = Field(
        None,
        alias="categoryId",
        description="Filter by specific category identifier (24-char hex string).",
        examples=["507f1f77bcf86cd799439011"]
    )
    is_duplicate: Optional[bool] = Field(
        None,
        alias="isDuplicate",
        description="Filter to show only duplicates (true) or unique items (false)."
    )

    @field_validator('title', 'category_id', mode='before')
    @classmethod
    def clean_strings(cls, v):
        if v is None:
            return None
        v_str = str(v).strip()
        return v_str if v_str else None

    @field_validator('category_id')
    @classmethod
    def validate_mongo_id(cls, v):
        if v is None:
            return None
        if not re.match(r'^[0-9a-fA-F]{24}$', v):
            raise ValueError(f"Invalid categoryId format: '{v}'. Must be a 24-character hex string.")
        return v

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        if v is None:
            return None
        valid_statuses = [s.value for s in Status]
        if v not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")
        return v

    @field_validator('date')
    @classmethod
    def validate_date(cls, v):
        return DateValidator.validate_and_format(v)

    model_config = {
        "populate_by_name": True,
        "extra": "ignore"
    }
