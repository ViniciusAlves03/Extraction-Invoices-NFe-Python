from http import HTTPStatus
from src.application.domain.exception import (
    DomainException,
    ValidationException,
    ConflictException,
    RepositoryException,
    NotFoundException
)
from src.utils.strings import Strings
from .api_error import APIError

class APIExceptionManager:
    @staticmethod
    def build(exc: Exception) -> APIError:
        if isinstance(exc, ValidationException):
            return APIError(HTTPStatus.UNPROCESSABLE_ENTITY, exc.message, exc.description)

        elif isinstance(exc, NotFoundException):
            return APIError(HTTPStatus.NOT_FOUND, exc.message, exc.description)

        elif isinstance(exc, ConflictException):
            return APIError(HTTPStatus.CONFLICT, exc.message, exc.description)

        elif isinstance(exc, RepositoryException):
            return APIError(HTTPStatus.INTERNAL_SERVER_ERROR, exc.message, exc.description)

        elif isinstance(exc, DomainException):
            return APIError(HTTPStatus.BAD_REQUEST, exc.message, exc.description)

        return APIError(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            Strings.ERROR_MESSAGE["UNEXPECTED"],
            str(exc)
        )
