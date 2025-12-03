from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List
from src.application.domain.model import ExtractionTask, ExtractedExpense
from src.application.domain.model.task_filter import TaskFilter


class IExtractionRepository(ABC):

    @abstractmethod
    async def create(self, task: ExtractionTask) -> ExtractionTask:
        pass

    @abstractmethod
    async def find_all(self, user_id: str, filters: TaskFilter) -> List[ExtractionTask]:
        pass

    @abstractmethod
    async def find_by_id(self, id: str) -> ExtractionTask | None:
        pass

    @abstractmethod
    async def find_by_hash(self, user_id: str, file_hash: str) -> ExtractionTask | None:
        pass

    @abstractmethod
    async def find_duplicate_by_key(self, user_id: str, access_key: str, amount: Decimal) -> tuple[str, ExtractedExpense] | None:
        pass
