from abc import ABC, abstractmethod
from src.application.domain.model.extraction_task import ExtractedExpense, ExtractionError


class IImageExtractor(ABC):

    @abstractmethod
    def extract_products_from_nfe(self, file_content: bytes) -> tuple[list[ExtractedExpense], list[ExtractionError]]:
        pass
