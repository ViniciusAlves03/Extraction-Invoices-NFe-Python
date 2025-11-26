import re
from datetime import datetime

class DateValidator:
    @staticmethod
    def validate_and_format(value: any) -> str:
        if not value:
            return None

        if hasattr(value, 'strftime'):
            return value.strftime('%Y-%m-%d')

        date_str = str(value).strip()

        formats = [
            '%Y-%m-%d',       # ISO: 2023-12-25
            '%d/%m/%Y',       # BR:  25/12/2023
            '%m/%d/%Y',       # US:  12/25/2023
            '%d-%m-%Y',       # Dash BR
            '%Y/%m/%d'        # Slash ISO
        ]

        for fmt in formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                if dt.year < 1678 or dt.year > 2261:
                    raise ValueError(f"Ano fora do limite permitido: {dt.year}")
                return dt.strftime('%Y-%m-%d')
            except ValueError:
                continue

        raise ValueError(f"Formato de data desconhecido ou inválido: {value}")
