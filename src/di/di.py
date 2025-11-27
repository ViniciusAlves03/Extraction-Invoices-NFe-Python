from dependency_injector import containers, providers
from src.application.service.extraction_service import ExtractionService
from src.application.service.extraction_service import ExtractionService
from src.infrastructure.repository.extraction_repository import ExtractionRepository
from src.infrastructure.adapter.gemini_extractor import GeminiExtractor


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=["src.ui.controller.extractions_controller"])

    extraction_repository = providers.Factory(ExtractionRepository)

    image_extractor = providers.Singleton(GeminiExtractor)
    excel_extractor = providers.Singleton(GeminiExtractor)

    extraction_service = providers.Factory(
        ExtractionService,
        repository=extraction_repository,
        image_extractor=image_extractor,
        excel_extractor=excel_extractor
    )
