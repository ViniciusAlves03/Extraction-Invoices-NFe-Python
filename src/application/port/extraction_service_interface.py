from abc import ABC, abstractmethod
from typing import List, Optional
from src.application.domain.model.extraction_task import ExtractionTask
from src.application.domain.model.task_filter import TaskFilter


class IExtractionService(ABC):

    @abstractmethod
    async def process_file(self, file_content: bytes, filename: str) -> ExtractionTask:
        pass

    @abstractmethod
    async def get_all_tasks(self, filters: TaskFilter) -> List[ExtractionTask]:
        pass

    @abstractmethod
    async def get_task_by_id(self, task_id: str) -> ExtractionTask:
        pass
