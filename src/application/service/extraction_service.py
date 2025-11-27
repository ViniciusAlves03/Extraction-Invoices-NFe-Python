import logging

from src.application.port.extraction_service_interface import IExtractionService
from src.application.port.extraction_repository_interface import IExtractionRepository
from src.application.port.image_extractor_interface import IImageExtractor
from src.application.port.excel_extractor_interface import IExcelExtractor
from src.application.domain.model.extraction_task import ExtractionTask

logger = logging.getLogger(__name__)

class ExtractionService(IExtractionService):

    def __init__(
        self,
        repository: IExtractionRepository,
        image_extractor: IImageExtractor,
        excel_extractor: IExcelExtractor
    ):
        self.repository = repository
        self.image_extractor = image_extractor
        self.excel_extractor = excel_extractor

    async def process_file(self, file_content: bytes, filename: str) -> ExtractionTask:
        extension = filename.split('.')[-1].lower()

        extracted_data = []

        if extension in ['xlsx', 'xls']:
            extracted_data = self.excel_extractor.extract_products_from_excel(file_content)

        elif extension in ['png', 'jpg', 'jpeg']:
            extracted_data = self.image_extractor.extract_products_from_nfe(file_content)

        task = ExtractionTask(
            filename=filename,
            status="COMPLETED",
            file_type=extension,
            result_data=extracted_data
        )
        created_task = await self.repository.create(task)
        return created_task
