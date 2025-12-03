from dependency_injector import containers, providers
from src.application.service import ExtractionService
from src.infrastructure.repository import ExtractionRepository
from src.infrastructure.adapter import (ExcelExtractor, GeminiExtractor)
from src.utils.custom_logger import CustomLogger


class Container(containers.DeclarativeContainer):
    logger = providers.Singleton(CustomLogger)

    extraction_repository = providers.Factory(ExtractionRepository)

    image_extractor = providers.Singleton(GeminiExtractor)
    excel_extractor = providers.Singleton(ExcelExtractor)

    extraction_service = providers.Factory(
        ExtractionService,
        repository=extraction_repository,
        image_extractor=image_extractor,
        excel_extractor=excel_extractor,
        logger=logger
    )
