from dataclasses import dataclass
from typing import Optional
from fastapi import Query

@dataclass
class TaskFilter:
    status: Optional[str] = None
    title: Optional[str] = None
    date: Optional[str] = None
    category_id: Optional[str] = None
    is_duplicate: Optional[bool] = None
