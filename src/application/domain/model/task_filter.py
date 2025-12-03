from dataclasses import dataclass
from typing import Optional
from fastapi import Query


@dataclass
class TaskFilter:
    status: Optional[str] = Query(
        None,
        description="Filter tasks by their processing status (e.g., PENDING, COMPLETED, FAILED).",
        examples=["COMPLETED"]
    )
    title: Optional[str] = Query(
        None,
        description="Filter by product title or description (partial match).",
        examples=["Gasoline"]
    )
    date: Optional[str] = Query(
        None,
        description="Filter by exact date in YYYY-MM-DD format.",
        examples=["2023-10-25"]
    )
    category_id: Optional[str] = Query(
        None,
        description="Filter by specific category identifier.",
        examples=["cat_5521"]
    )
    is_duplicate: Optional[bool] = Query(
        None,
        description="Filter to show only duplicates (true) or unique items (false)."
    )
