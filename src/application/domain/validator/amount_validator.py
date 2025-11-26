from decimal import Decimal, InvalidOperation
import re


class AmountValidator:

    @staticmethod
    def validate(value: any) -> Decimal:
        if value is None:
            return None

        if isinstance(value, (int, float)):
            return Decimal(str(value))

        if isinstance(value, Decimal):
            return value

        val_str = str(value).strip()

        val_str = re.sub(r'[^\d.,-]', '', val_str)

        try:
            if ',' in val_str and '.' in val_str:
                if val_str.find('.') < val_str.find(','):
                    val_str = val_str.replace('.', '').replace(',', '.')
                else:
                    val_str = val_str.replace(',', '')

            elif ',' in val_str:
                val_str = val_str.replace(',', '.')

            return Decimal(val_str)
        except InvalidOperation:
            raise ValueError(f"Valor monetário inválido: {value}")
