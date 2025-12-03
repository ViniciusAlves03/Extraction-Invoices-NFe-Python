from datetime import datetime
from src.utils import Strings


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
                    msg = Strings.ERROR_MESSAGE['DATE']['YEAR_NOT_ALLOWED'].format(dt.year)
                    raise ValueError(msg)
                return dt.strftime('%Y-%m-%d')
            except ValueError as e:
                if "year not allowed" in str(e):
                    raise e
                continue

        raise ValueError(Strings.ERROR_MESSAGE['DATE']['INVALID_DATE_FORMAT'].format(value))
