import pytest

from job_execution_analyser.exceptions import InvalidRecordError
from job_execution_analyser.io.validators import validate_record
from job_execution_analyser.models.enums import JobStatus


def test_validate_record_returns_job_record():
    raw = {
        "job_id": "job-1",
        "status": "success",
        "started_at": "2026-09-20T08:00:00",
        "finished_at": "2026-09-20T08:05:00",
        "attempt": 1,
    }
    record = validate_record(raw, index=0)

    assert record.job_id == "job-1"
    assert record.status is JobStatus.SUCCESS


def test_validate_record_rejects_unknown_status():
    raw = {
        "job_id": "job-1",
        "status": "bogus",
        "started_at": "2026-09-20T08:00:00",
        "attempt": 1,
    }
    with pytest.raises(InvalidRecordError):
        validate_record(raw, index=0)


def test_validate_record_rejects_missing_field():
    raw = {"job_id": "job-1", "started_at": "2026-09-20T08:00:00", "attempt": 1}
    with pytest.raises(InvalidRecordError):
        validate_record(raw, index=0)


def test_validate_record_rejects_finished_before_started():
    raw = {
        "job_id": "job-1",
        "status": "success",
        "started_at": "2026-09-20T08:00:00",
        "finished_at": "2026-09-20T07:00:00",
        "attempt": 1,
    }
    with pytest.raises(InvalidRecordError):
        validate_record(raw, index=0)


def test_validate_record_rejects_non_object():
    with pytest.raises(InvalidRecordError):
        validate_record("not-a-dict", index=0)
