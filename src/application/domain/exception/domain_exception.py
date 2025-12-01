class DomainException(Exception):
    def __init__(self, message: str, description: str = None):
        self.message = message
        self.description = description
        super().__init__(self.message)
