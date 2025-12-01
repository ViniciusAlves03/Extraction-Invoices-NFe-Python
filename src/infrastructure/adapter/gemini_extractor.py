import json
import io
import logging
from decimal import Decimal
from PIL import Image
import google.generativeai as genai
from pydantic import ValidationError

from src.application.port.image_extractor_interface import IImageExtractor
from src.application.domain.model.extraction_task import ExtractedExpense, ExtractionError
from src.utils.config import settings
from src.utils.strings import Strings

logger = logging.getLogger(__name__)

class GeminiExtractor(IImageExtractor):

    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def extract_products_from_nfe(self, file_content: bytes) -> tuple[list[ExtractedExpense], list[ExtractionError]]:
        try:
            image = Image.open(io.BytesIO(file_content))

            prompt = """
                Você é um assistente especializado em contabilidade e extração de dados de Notas Fiscais Brasileiras (DANFE/NFe).

                1. Localize a CHAVE DE ACESSO da nota fiscal (código numérico de 44 dígitos, geralmente no topo direito, abaixo do código de barras).
                2. Extraia os ITENS (produtos/serviços).

                Retorne APENAS um JSON com uma lista de objetos.
                IMPORTANTE: A chave de acesso encontrada deve ser repetida no campo 'access_key' de TODOS os itens.

                Estrutura do JSON:
                [
                    {
                        "title": "Descrição exata do produto",
                        "description": "Linha completa",
                        "quantity": 1.00,
                        "unit_price": 10.00,
                        "total_amount": 10.00,
                        "date": "YYYY-MM-DD",
                        "access_key": "352309..." (A chave de 44 dígitos da nota)
                    }
                ]

                Regras:
                1. Ignore linhas de Faturas/Impostos.
                2. Use ponto para decimais.
                3. Se a chave de acesso não estiver legível, deixe null.
            """

            response = self.model.generate_content([prompt, image])
            text = response.text.strip()

            if text.startswith("```"):
                text = text.replace("```json", "").replace("```", "")

            data = json.loads(text)

            valid_items = []
            errors = []

            for item in data:
                item_desc = item.get('title', 'Unnamed item')
                try:
                    expense = ExtractedExpense(
                        title=item.get('title'),
                        description=item.get('description'),
                        quantity=Decimal(str(item.get('quantity', 1))),
                        unit_price=Decimal(str(item.get('unit_price'))),
                        total_amount=Decimal(str(item.get('total_amount'))),
                        date=item.get('date'),
                        access_key=item.get('access_key')
                    )
                    valid_items.append(expense)
                except (ValidationError, ValueError) as e:
                    msg = str(e).split('[')[0]
                    errors.append(ExtractionError(
                        item_identifier=f"Item IA: {item_desc}",
                        error_message=Strings.ERROR_MESSAGE['EXTRACTOR']['GEMINI_INVALID_DATA'].format(msg)
                    ))

            return valid_items, errors

        except Exception as e:
            return [], [ExtractionError(
                item_identifier="AI Processing",
                error_message=Strings.ERROR_MESSAGE['EXTRACTOR']['GEMINI_ERROR'].format(str(e))
            )]
