from fastapi import APIRouter, UploadFile, File, Depends
from typing import List
from src.application.domain.model.extraction_task import ExtractionTask
from src.application.domain.model.task_filter import TaskFilter
from src.application.port.extraction_service_interface import IExtractionService
from src.di.di import Container
from dependency_injector.wiring import inject, Provide

router = APIRouter(prefix="/v1/users/{user_id}/extractions", tags=["Extractions"])

@router.post(
    "/",
    summary="process new invoice file",
    description="Upload an Excel spreadsheet (.xlsx) or image (png, jpg, or jpeg) for data extraction."
)
@inject
async def upload_file(
    user_id: str,
    file: UploadFile = File(...),
    service: IExtractionService = Depends(Provide[Container.extraction_service])
):
    content = await file.read()
    result = await service.process_file(user_id, content, file.filename)
    return result

@router.get(
    "/",
    response_model=List[ExtractionTask],
    summary="Retrieve all extraction tasks",
    description="Retrieves a list of all data extraction tasks for a specific user. You can filter the results by status, title, date, category ID, or duplicate status."
)
@inject
async def get_extractions(
    user_id: str,
    filters: TaskFilter = Depends(),
    service: IExtractionService = Depends(Provide[Container.extraction_service])
):
    return await service.get_all_tasks(user_id, filters)

@router.get(
    "/{task_id}",
    response_model=ExtractionTask,
    summary="Retrieve an extraction task by ID",
    description="Retrieves detailed information about a specific extraction task identified by its unique ID."
)
@inject
async def get_extraction_by_id(
    user_id: str,
    task_id: str,
    service: IExtractionService = Depends(Provide[Container.extraction_service])
):
    return await service.get_task_by_id(user_id, task_id)
