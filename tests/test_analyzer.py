from job_execution_analyser.core.analyzer import summarize
from job_execution_analyser.models.records import JobRecord


def _record(**overrides):
    defaults = {
        "job_id": "job-1",
        "status": "success",
        "started_at": "2026-09-20T08:00:00",
        "finished_at": "2026-09-20T08:05:00",
        "attempt": 1,
    }
    return JobRecord.model_validate({**defaults, **overrides})


def test_summarize_counts_and_average_duration():
    records = [
        _record(job_id="job-1", status="success", finished_at="2026-09-20T08:05:00"),
        _record(job_id="job-2", status="success", finished_at="2026-09-20T08:10:00"),
        _record(job_id="job-3", status="failed", finished_at="2026-09-20T08:01:00"),
        _record(job_id="job-4", status="running", finished_at=None),
    ]

    summary = summarize(records)

    assert summary.total_jobs == 4
    assert summary.successful_jobs == 2
    assert summary.failed_jobs == 1
    # (300 + 600) / 2 = 450 seconds
    assert summary.average_success_duration_seconds == 450.0


def test_summarize_tracks_retried_jobs():
    records = [
        _record(job_id="job-1", attempt=1),
        _record(job_id="job-2", attempt=3),
    ]

    summary = summarize(records)

    assert summary.retried_job_ids == ["job-2"]


def test_summarize_empty_records():
    summary = summarize([])

    assert summary.total_jobs == 0
    assert summary.average_success_duration_seconds is None
    assert summary.retried_job_ids == []
