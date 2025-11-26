from abc import ABC, abstractmethod
from src.application.domain.model.extraction_task import ExtractionTask

class IExtractionService(ABC):

    @abstractmethod
    async def process_file(self, file_content: bytes, filename: str) -> ExtractionTask:
        pass
