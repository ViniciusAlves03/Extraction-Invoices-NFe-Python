from typing import Optional, Any


class APIError:
    def __init__(self, code: int, message: str, description: Optional[str] = None):
        self.code = code
        self.message = message
        self.description = description

    def to_json(self) -> dict[str, Any]:
        result = {
            "code": self.code,
            "message": self.message
        }
        if self.description:
            result["description"] = self.description

        return result
