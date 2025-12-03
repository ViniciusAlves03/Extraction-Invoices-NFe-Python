from abc import ABC, abstractmethod
from src.application.domain.model import ExtractedExpense, ExtractionError


class IExcelExtractor(ABC):

    @abstractmethod
    def extract_products_from_excel(self, file_content: bytes) -> tuple[list[ExtractedExpense], list[ExtractionError]]:
        pass
