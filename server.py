import os

from dotenv import load_dotenv
from flask import Blueprint, Flask
from flask_cors import CORS
from flask_restx import Api

load_dotenv(override=True)


class Server():
    def __init__(self):
        self.app = Flask(__name__)

        CORS(self.app)
        self.bluePrint = Blueprint("api", __name__, url_prefix="/v1")
        self.api = Api(self.bluePrint,
                       doc="/doc",
                       title="Extraction Python",
                       security="Bearer Auth",
                       authorizations={
                           "Bearer Auth": {
                               "type": "apiKey",
                               "in": "header",
                               "name": "Authorization",
                               "description": "Add JWT token in format: Bearer <token>"
                           }
                       }
                       )
        self.app.register_blueprint(self.bluePrint)

        self.app.config["PORT_HTTP"] = os.environ.get("PORT_HTTP")

        super().__init__()

    def run(self, ):
        self.app.run(
            port=int(self.app.config["PORT_HTTP"]),
            debug=True,
            host="0.0.0.0"
        )


server = Server()
