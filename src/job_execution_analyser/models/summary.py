from pydantic import BaseModel


class Summary(BaseModel):
    total_jobs: int
    successful_jobs: int
    failed_jobs: int
    average_success_duration_seconds: float | None
    retried_job_ids: list[str]
