from typing import List
from src.application.port.extractor_interface import IExtractor
from src.application.domain.exception import ValidationException
from src.utils import Strings


class ExtractorFactory:
    def __init__(self, extractors: List[IExtractor]):
        self.extractors = extractors

    def get_extractor(self, filename: str) -> IExtractor:
        for extractor in self.extractors:
            if extractor.supports(filename):
                return extractor

        extension = filename.split('.')[-1].lower() if '.' in filename else ''
        msg = Strings.ERROR_MESSAGE['FILE']['NOT_SUPPORTED'].format(extension)
        raise ValidationException(message=msg)
