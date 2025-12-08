from src.application.port import (IExtractionRepository, IExtractionService, ILogger)
from src.application.port import ILogger
from src.application.domain.model import (ExtractionTask, TaskFilter)
from src.application.domain.exception import (NotFoundException, ConflictException)
from src.application.domain.utils import Status
from src.application.factory import ExtractorFactory
from src.utils import (Strings, calculate_sha256)


class ExtractionService(IExtractionService):

    def __init__(self, repository: IExtractionRepository, extractor_factory: ExtractorFactory, logger: ILogger):
        self.repository = repository
        self.extractor_factory = extractor_factory
        self.logger = logger

    async def process_file(self, user_id: str, file_content: bytes, filename: str) -> ExtractionTask:
        extension = filename.split('.')[-1].lower() if '.' in filename else 'unknown'
        extractor = self.extractor_factory.get_extractor(filename)

        file_hash = calculate_sha256(file_content)
        existing_task = await self.repository.find_by_hash(user_id, file_hash)

        if existing_task:
            raise ConflictException(
                message=Strings.ERROR_MESSAGE['TASK']['TASK_REGISTERED'],
                description=Strings.ERROR_MESSAGE['TASK']['TASK_REGISTERED_DESCRIPTION'].format(existing_task.status)
            )

        extracted_data = []
        errors = []

        try:
            extracted_data, errors = extractor.extract(file_content)

            if extracted_data:
                checked_keys_cache = {}
                for item in extracted_data:
                    if item.access_key and item.total_amount:
                        cache_key = f"{item.access_key}|{item.total_amount}"

                        if cache_key in checked_keys_cache:
                            result = checked_keys_cache[cache_key]
                        else:
                            result = await self.repository.find_duplicate_by_key(user_id, item.access_key, item.total_amount)
                            checked_keys_cache[cache_key] = result

                        if result:
                            original_id, _ = result
                            item.is_duplicate = True
                            item.duplicate_of_id = original_id

            if not extracted_data and errors:
                status = Status.FAILED
            elif not extracted_data and not errors:
                status = Status.FAILED
                errors.append({"item_identifier": "General", "error_message": Strings.ERROR_MESSAGE['FILE']['EMPTY']})
            else:
                status = Status.PENDING

            task = ExtractionTask(
                filename=filename,
                file_hash=file_hash,
                file_type=extension,
                status=status,
                user_id=user_id,
                result_data=extracted_data,
                error_report=errors
            )

            saved_task = await self.repository.create(task)
            return saved_task

        except Exception as e:
            error_task = ExtractionTask(
                filename=filename,
                file_hash=file_hash,
                file_type=extension,
                status=Status.FAILED,
                user_id=user_id,
                error_report=[{"item_identifier": "System", "error_message": str(e)}]
            )
            return await self.repository.create(error_task)

    async def get_all_tasks(self, user_id: str, filters: TaskFilter) -> list[ExtractionTask]:
        return await self.repository.find_all(user_id, filters)

    async def get_task_by_id(self, user_id: str, task_id: str) -> ExtractionTask:
        task = await self.repository.find_by_id(task_id)
        if not task or task.user_id != user_id:
            raise NotFoundException(
                message=Strings.ERROR_MESSAGE['TASK']['NOT_FOUND'],
                description=Strings.ERROR_MESSAGE['TASK']['NOT_FOUND_DESC']
            )
        return task
