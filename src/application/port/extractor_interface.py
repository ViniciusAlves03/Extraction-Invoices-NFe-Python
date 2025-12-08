from abc import ABC, abstractmethod
from src.application.domain.model import ExtractedExpense, ExtractionError


class IExtractor(ABC):

    @abstractmethod
    def extract(self, file_content: bytes) -> tuple[list[ExtractedExpense], list[ExtractionError]]:
        pass

    @abstractmethod
    def supports(self, filename: str) -> bool:
        pass
