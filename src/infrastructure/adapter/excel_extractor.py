import io
import pandas as pd
import logging
from pydantic import ValidationError

from src.application.port.excel_extractor_interface import IExcelExtractor
from src.application.domain.model.extraction_task import ExtractedExpense, ExtractionError

logger = logging.getLogger(__name__)

class ExcelExtractor(IExcelExtractor):

    def extract_products_from_excel(self, file_content: bytes) -> tuple[list[ExtractedExpense], list[ExtractionError]]:
        extracted_data = []
        errors = []

        try:
            df = pd.read_excel(io.BytesIO(file_content))
            df.columns = df.columns.str.strip().str.lower()
            col_map = {
                'título': 'title', 'titulo': 'title', 'produto': 'title', 'descrição': 'title',
                'obs': 'description', 'observação': 'description',
                'data': 'date', 'emissão': 'date',
                'qtd': 'quantity', 'quantidade': 'quantity', 'quant': 'quantity',
                'unitário': 'unit_price', 'unitario': 'unit_price', 'valor unit': 'unit_price', 'v.un': 'unit_price',
                'total': 'total_amount', 'valor total': 'total_amount',
                'chave': 'access_key', 'chave de acesso': 'access_key', 'chave nfe': 'access_key', 'key': 'access_key'
            }
            df.rename(columns=col_map, inplace=True)

            for index, row in df.iterrows():
                row_idx = index + 2
                try:
                    if pd.isna(row.get('title')) or pd.isna(row.get('total_amount')):
                         raise ValueError("Required fields (Title or Total) are empty.")

                    expense = ExtractedExpense(
                        title=row.get('title'),
                        description=row.get('description'),
                        quantity=row.get('quantity', 1),
                        unit_price=row.get('unit_price', row.get('total_amount')),
                        total_amount=row.get('total_amount'),
                        date=row.get('date'),
                        access_key=row.get('access_key')
                    )
                    extracted_data.append(expense)

                except (ValidationError, ValueError) as e:
                    msg = str(e).replace('\n', ' ')
                    errors.append(ExtractionError(
                        item_identifier=f"Excel Row {row_idx}",
                        error_message=msg
                    ))
                    logger.warning(f"Excel Row Error {row_idx}: {msg}")
                except Exception as e:
                    errors.append(ExtractionError(
                        item_identifier=f"Excel Row {row_idx}",
                        error_message=f"Unexpected error: {str(e)}"
                    ))

            return extracted_data, errors

        except Exception as e:
            logger.error(f"Excel fatal error: {e}")
            return [], [ExtractionError(item_identifier="General Archive", error_message=str(e))]
