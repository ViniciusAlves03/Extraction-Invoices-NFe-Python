import logging
from logging import config

from flask_restx import Namespace

from server import server
# from src.background import BackgroundService
from src.infrastructure.database.utils import db, ma
from src.ui.controller import (
    ExtractionController
    )
from src.utils.logger import create_default_logger_config

api = server.api
app = server.app

# Logger config
# config.dictConfig(create_default_logger_config("INFO"))

# Namespaces
ns_extractions = Namespace("Extractions", description="Extractions management")

ns_extractions.add_resource(ExtractionController, "databases")

api.add_namespace(ns_extractions, path="/")

# Instantiates the BackgroundService and its dependencies.
# background_service = BackgroundService()
# try:
#     background_service.start_services()
#     logging.info("Background services successfully initialized...")
# except Exception as error:
#     logging.error("{} {}".format(error.message, error.description), flush=True)

if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    server.run()
