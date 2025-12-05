from typing import List, Optional, Annotated
from datetime import datetime
from beanie import Document, PydanticObjectId
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field
from pydantic.alias_generators import to_camel
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

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )

class ExtractedExpenseSchema(BaseModel):
    title: str
    description: Optional[str] = None
    quantity: PyDecimal
    unit_price: PyDecimal
    total_amount: PyDecimal
    date: Optional[str] = None
    category_id: Optional[str] = None
    access_key: Optional[str] = None
    is_duplicate: bool = False
    duplicate_of_id: Optional[str] = None

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )

class ExtractionTaskSchema(Document):
    id: Optional[PydanticObjectId] = Field(None, alias="_id")
    filename: str
    file_type: str
    file_hash: str
    status: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    result_data: List[ExtractedExpenseSchema] = []
    error_report: List[ExtractionErrorSchema] = []

    class Settings:
        name = "extraction_tasks"

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )
