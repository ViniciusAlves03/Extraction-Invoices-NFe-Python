from abc import ABC, abstractmethod

class ILogger(ABC):
    @abstractmethod
    def info(self, message: str, **kwargs):
        pass

    @abstractmethod
    def warning(self, message: str, **kwargs):
        pass

    @abstractmethod
    def error(self, message: str, **kwargs):
        pass

    @abstractmethod
    def debug(self, message: str, **kwargs):
        pass

    @abstractmethod
    def critical(self, message: str, **kwargs):
        pass
