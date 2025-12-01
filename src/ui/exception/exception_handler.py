from fastapi import Request
from fastapi.responses import JSONResponse
from .api_exception_manager import APIExceptionManager

async def global_exception_handler(request: Request, exc: Exception):
    api_error = APIExceptionManager.build(exc)

    return JSONResponse(
        status_code=api_error.code,
        content=api_error.to_json()
    )
