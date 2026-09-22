class JobRecordError(Exception):
    """Base exception for job record processing errors."""


class JobDataError(JobRecordError):
    """Raised for file-level problems: missing file, bad JSON, wrong shape."""


class InvalidRecordError(JobRecordError):
    """Raised when a single job record fails validation."""

    def __init__(self, index: int, raw: dict, reason: str) -> None:
        self.index = index
        self.raw = raw
        self.reason = reason
        super().__init__(f"record at index {index} is invalid: {reason}")
