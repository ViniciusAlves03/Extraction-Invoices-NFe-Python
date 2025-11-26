import pandas as pd
import io
from pydantic import ValidationError
from src.application.port.extraction_service_interface import IExtractionService
from src.application.domain.model.extraction_task import ExtractionTask, ExtractedExpense

class ExtractionService(IExtractionService):

    def __init__(self, repository):
        self.repository = repository

    async def process_file(self, file_content: bytes, filename: str) -> ExtractionTask:
        extension = filename.split('.')[-1].lower()

        extracted_data = []

        if extension in ['xlsx', 'xls']:
            df = pd.read_excel(io.BytesIO(file_content))

            df.columns = df.columns.str.strip().str.lower()
            column_mapping = {
                'título': 'title', 'titulo': 'title', 'nome': 'title',
                'descrição': 'description', 'descricao': 'description',
                'value': 'amount', 'valor': 'amount', 'preço': 'amount', 'preço': 'amount', 'amount': 'amount',
                'data': 'date'
            }
            df.rename(columns=column_mapping, inplace=True)

            for _, row in df.iterrows():
                try:
                    expense = ExtractedExpense(
                        title=row.get('title'),
                        description=row.get('description'),
                        amount=row.get('amount'),
                        date=row.get('date')
                    )
                    extracted_data.append(expense)

                except ValidationError as e:
                    print(f"Linha ignorada por validação: {e.errors()}")
                    continue
                except Exception as e:
                    print(f"Erro genérico na linha: {e}")
                    continue

        task = ExtractionTask(
            filename=filename,
            status="COMPLETED",
            file_type=extension,
            result_data=extracted_data
        )
        await task.create()
        return task
