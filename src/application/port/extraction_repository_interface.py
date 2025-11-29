from abc import ABC, abstractmethod
from decimal import Decimal
from src.application.domain.model.extraction_task import ExtractionTask


class IExtractionRepository(ABC):

    @abstractmethod
    async def create(self, task: ExtractionTask) -> ExtractionTask:
        pass

    @abstractmethod
    async def find_by_hash(self, file_hash: str) -> ExtractionTask | None:
        pass
