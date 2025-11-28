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

logger = logging.getLogger(__name__)

class GeminiExtractor(IImageExtractor):

    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def extract_products_from_nfe(self, file_content: bytes) -> list[ExtractedExpense]:
        try:
            image = Image.open(io.BytesIO(file_content))

            prompt = """
                Você é um assistente especializado em contabilidade e extração de dados de Notas Fiscais Brasileiras (DANFE/NFe).
                Analise a imagem fornecida e extraia os ITENS (produtos/serviços) desta nota fiscal.

                Retorne APENAS um JSON (sem markdown, sem ```json) com uma lista de objetos seguindo estritamente esta estrutura:
                [
                    {
                        "title": "Descrição exata do produto (remova códigos iniciais como 'DH89' se houver)",
                        "description": "Linha completa original do item",
                        "quantity": 1.00 (número decimal),
                        "unit_price": 10.00 (número decimal),
                        "total_amount": 10.00 (número decimal),
                        "date": "YYYY-MM-DD" (Data de emissão da nota, se houver)
                    }
                ]

                Regras:
                1. Ignore linhas de 'Faturas', 'Transportadora' ou 'Impostos'. Foque apenas na tabela de 'DADOS DOS PRODUTOS/SERVIÇOS' ou semelhante.
                2. Se a quantidade não estiver explícita, tente deduzir matematicamente (Total / Unitário).
                3. Converta valores numéricos para formato americano (ponto decimal).
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
                        quantity=Decimal(str(item.get('quantity'))),
                        unit_price=Decimal(str(item.get('unit_price'))),
                        total_amount=Decimal(str(item.get('total_amount'))),
                        date=item.get('date')
                    )
                    valid_items.append(expense)
                except (ValidationError, ValueError) as e:
                    msg = str(e).split('[')[0]
                    errors.append(ExtractionError(
                        item_identifier=f"Item IA: {item_desc}",
                        error_message=f"Invalid data: {msg}"
                    ))

            return valid_items, errors

        except Exception as e:
            logger.error(f"Gemini fatal error: {e}")
            return [], [ExtractionError(item_identifier="Processamento IA", error_message=str(e))]
