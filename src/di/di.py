from dependency_injector import containers, providers
from src.application.service import ExtractionService
from src.application.factory import ExtractorFactory
from src.infrastructure.repository import ExtractionRepository
from src.infrastructure.adapter import (ExcelExtractor, GeminiExtractor)
from src.utils.custom_logger import CustomLogger


class Container(containers.DeclarativeContainer):
    logger = providers.Singleton(CustomLogger)

    extraction_repository = providers.Factory(ExtractionRepository)

    excel_extractor = providers.Singleton(ExcelExtractor)
    gemini_extractor = providers.Singleton(GeminiExtractor)

    extractor_factory = providers.Factory(
        ExtractorFactory,
        extractors=providers.List(
            excel_extractor,
            gemini_extractor
        )
    )

    extraction_service = providers.Factory(
        ExtractionService,
        repository=extraction_repository,
        extractor_factory=extractor_factory,
        logger=logger
    )
