from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from src.application.port.extraction_service_interface import IExtractionService
from src.di.di import Container
from dependency_injector.wiring import inject, Provide

router = APIRouter(prefix="/v1/extractions")

@router.post("/")
@inject
async def upload_file(
    file: UploadFile = File(...),
    service: IExtractionService = Depends(Provide[Container.extraction_service])
):
    try:
        content = await file.read()
        result = await service.process_file(content, file.filename)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
