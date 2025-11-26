from dependency_injector import containers, providers
from src.application.service.extraction_service import ExtractionService

class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=["src.ui.controller.extractions_controller"])

    # repository = providers.Factory(ExtractionRepository)

    extraction_service = providers.Factory(
        ExtractionService,
        repository=None
    )
