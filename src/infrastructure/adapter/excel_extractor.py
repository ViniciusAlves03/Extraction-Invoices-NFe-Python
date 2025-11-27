import io
import pandas as pd
import logging
from pydantic import ValidationError

from src.application.port.excel_extractor_interface import IExcelExtractor
from src.application.domain.model.extraction_task import ExtractedExpense

logger = logging.getLogger(__name__)

class ExcelExtractor(IExcelExtractor):

    def extract_products_from_excel(self, file_content: bytes) -> list[ExtractedExpense]:
        extracted_data = []
        try:
            df = pd.read_excel(io.BytesIO(file_content))

            df.columns = df.columns.str.strip().str.lower()
            column_mapping = {
                'título': 'title', 'titulo': 'title', 'nome': 'title',
                'descrição': 'description', 'descricao': 'description',
                'value': 'amount', 'valor': 'amount', 'preço': 'amount', 'amount': 'amount',
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
                    logger.warning(f"Excel: Linha ignorada validação: {e.errors()}")
                    continue
                except Exception as e:
                    logger.warning(f"Excel: Erro linha: {e}")
                    continue

            return extracted_data

        except Exception as e:
            logger.error(f"Erro fatal no ExcelExtractor: {e}")
            return []
