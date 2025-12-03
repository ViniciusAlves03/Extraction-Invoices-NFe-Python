from abc import ABC, abstractmethod
from typing import List
from src.application.domain.model.extraction_task import ExtractionTask
from src.application.domain.model.task_filter import TaskFilter


class IExtractionService(ABC):

    @abstractmethod
    async def process_file(self, user_id: str, file_content: bytes, filename: str) -> ExtractionTask:
        pass

    @abstractmethod
    async def get_all_tasks(self, user_id: str, filters: TaskFilter) -> List[ExtractionTask]:
        pass

    @abstractmethod
    async def get_task_by_id(self, user_id: str, task_id: str) -> ExtractionTask:
        pass
