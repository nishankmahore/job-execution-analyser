from job_execution_analyser.models.enums import JobStatus
from job_execution_analyser.models.records import JobRecord
from job_execution_analyser.models.summary import Summary


def summarize(records: list[JobRecord]) -> Summary:
    """Aggregate valid job records into a Summary.

    Args:
        records: Validated job records, e.g. from io.loader.load_records.

    Returns:
        Summary with total/successful/failed counts, average duration of
        successful jobs, and the ids of jobs that needed a retry.
    """
    successful = [r for r in records if r.status is JobStatus.SUCCESS]
    failed = [r for r in records if r.status is JobStatus.FAILED]

    # Only successful jobs with a finished_at contribute to the average —
    # a still-running or failed job has no meaningful "duration" here.
    durations = [
        (r.finished_at - r.started_at).total_seconds()
        for r in successful
        if r.finished_at is not None
    ]
    average_duration = sum(durations) / len(durations) if durations else None

    retried_job_ids = [r.job_id for r in records if r.attempt > 1]

    return Summary(
        total_jobs=len(records),
        successful_jobs=len(successful),
        failed_jobs=len(failed),
        average_success_duration_seconds=average_duration,
        retried_job_ids=retried_job_ids,
    )
