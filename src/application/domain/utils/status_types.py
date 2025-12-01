from enum import Enum


class Status(Enum):
    COMPLETED = "COMPLETED"
    PENDING = "PENDING"
    PARTIAL_SUCCESS = "PARTIAL_SUCCESS"
    FAILED = "FAILED"
