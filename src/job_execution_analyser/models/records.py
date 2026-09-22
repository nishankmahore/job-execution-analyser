from datetime import datetime

from pydantic import BaseModel, Field, model_validator

from job_execution_analyser.models.enums import JobStatus


class JobRecord(BaseModel):
    job_id: str = Field(min_length=1)
    status: JobStatus
    started_at: datetime
    finished_at: datetime | None = None
    attempt: int = Field(ge=1)

    @model_validator(mode="after")
    def check_finished_after_started(self) -> "JobRecord":
        # A job can't finish before it started — catches clock skew /
        # swapped-field bugs in the source data early, at parse time.
        if self.finished_at is not None and self.finished_at < self.started_at:
            raise ValueError("finished_at cannot be before started_at")
        return self
