from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Query
from typing import List, Optional
from src.application.domain.model.extraction_task import ExtractionTask
from src.application.domain.model.task_filter import TaskFilter
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
    content = await file.read()
    result = await service.process_file(content, file.filename)
    return result

@router.get("/", response_model=List[ExtractionTask])
@inject
async def get_extractions(
    filters: TaskFilter = Depends(),
    service: IExtractionService = Depends(Provide[Container.extraction_service])
):
    return await service.get_all_tasks(filters)

@router.get("/{task_id}", response_model=ExtractionTask)
@inject
async def get_extraction_by_id(
    task_id: str,
    service: IExtractionService = Depends(Provide[Container.extraction_service])
):
    return await service.get_task_by_id(task_id)
