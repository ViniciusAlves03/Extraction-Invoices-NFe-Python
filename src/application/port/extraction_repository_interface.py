from abc import ABC, abstractmethod
from src.application.domain.model.extraction_task import ExtractionTask


class IExtractionRepository(ABC):

    @abstractmethod
    async def create(self, task: ExtractionTask) -> ExtractionTask:
        pass
