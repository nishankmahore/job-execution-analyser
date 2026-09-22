class JobRecordError(Exception):
    """Base exception for job record processing errors."""


class InvalidRecordError(JobRecordError):
    """Raised when a single job record fails validation."""
