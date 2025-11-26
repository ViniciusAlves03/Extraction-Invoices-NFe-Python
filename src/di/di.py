from dependency_injector import containers, providers
from src.application.service.extraction_service import ExtractionService
from src.application.service.extraction_service import ExtractionService
from src.infrastructure.repository.extraction_repository import ExtractionRepository


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=["src.ui.controller.extractions_controller"])

    extraction_repository = providers.Factory(ExtractionRepository)

    extraction_service = providers.Factory(
        ExtractionService,
        repository=extraction_repository
    )
