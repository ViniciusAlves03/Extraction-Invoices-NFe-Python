from typing import Optional, List, Any
from datetime import datetime
from beanie import Document
from pydantic import BaseModel

class ExtractedExpense(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    date: Optional[str] = None
    categoryId: Optional[str] = None

class ExtractionTask(Document):
    filename: str
    status: str  # PENDING, COMPLETED, ERROR
    file_type: str # PDF, EXCEL, IMAGE
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    result_data: List[ExtractedExpense] = []

    class Settings:
        name = "extraction_tasks"
