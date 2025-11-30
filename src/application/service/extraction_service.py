import logging
from src.application.port.extraction_service_interface import IExtractionService
from src.application.port.extraction_repository_interface import IExtractionRepository
from src.application.port.image_extractor_interface import IImageExtractor
from src.application.port.excel_extractor_interface import IExcelExtractor
from src.application.domain.model.extraction_task import ExtractionTask
from src.utils.hashing import calculate_sha256

logger = logging.getLogger(__name__)

class ExtractionService(IExtractionService):

    def __init__(self, repository: IExtractionRepository, image_extractor: IImageExtractor, excel_extractor: IExcelExtractor):
        self.repository = repository
        self.image_extractor = image_extractor
        self.excel_extractor = excel_extractor

    async def process_file(self, file_content: bytes, filename: str) -> ExtractionTask:
        file_hash = calculate_sha256(file_content)

        existing_task = await self.repository.find_by_hash(file_hash)
        if existing_task:
            logger.info(f"Arquivo duplicado detectado (Hash: {file_hash}). Retornando existente.")
            return existing_task

        extension = filename.split('.')[-1].lower()

        extracted_data = []
        errors = []

        if extension in ['xlsx', 'xls']:
            extracted_data, errors = self.excel_extractor.extract_products_from_excel(file_content)

        elif extension in ['png', 'jpg', 'jpeg']:
            extracted_data, errors = self.image_extractor.extract_products_from_nfe(file_content)

        else:
            errors.append({"item_identifier": "Archive", "error_message": f"The {extension} format is not supported."})

        if extracted_data:
            checked_keys_cache = {}

            for item in extracted_data:
                if item.access_key and item.total_amount:
                    cache_key = f"{item.access_key}|{item.total_amount}"

                    if cache_key in checked_keys_cache:
                        result = checked_keys_cache[cache_key]
                    else:
                        result = await self.repository.find_duplicate_by_key(item.access_key, item.total_amount)
                        checked_keys_cache[cache_key] = result

                    if result:
                        original_task_id = result

                        item.is_duplicate = True
                        item.duplicate_of_id = original_task_id

                        logger.warning(f"Duplicata encontrada! Chave: {item.access_key} | Valor: {item.total_amount}")

        status = "COMPLETED"
        if errors and extracted_data:
            status = "PARTIAL_SUCCESS"
        elif errors and not extracted_data:
            status = "FAILED"

        task = ExtractionTask(
            filename=filename,
            status=status,
            file_type=extension,
            result_data=extracted_data,
            error_report=errors
        )

        return await self.repository.create(task)
