from abc import ABC, abstractmethod
from src.application.domain.model.extraction_task import ExtractedExpense


class IExcelExtractor(ABC):

    @abstractmethod
    def extract_products_from_excel(self, file_content: bytes) -> list[ExtractedExpense]:
        pass
