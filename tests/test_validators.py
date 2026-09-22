import pytest

from job_execution_analyser.exceptions import InvalidRecordError
from job_execution_analyser.io.validators import validate_record
from job_execution_analyser.models.enums import JobStatus


def test_validate_record_returns_job_record():
    """A well-formed record parses into a JobRecord with correct field types."""
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
    """A status outside the JobStatus enum is rejected."""
    raw = {
        "job_id": "job-1",
        "status": "bogus",
        "started_at": "2026-09-20T08:00:00",
        "attempt": 1,
    }
    with pytest.raises(InvalidRecordError):
        validate_record(raw, index=0)


def test_validate_record_rejects_missing_field():
    """A missing required field (status) is rejected."""
    raw = {"job_id": "job-1", "started_at": "2026-09-20T08:00:00", "attempt": 1}
    with pytest.raises(InvalidRecordError):
        validate_record(raw, index=0)


def test_validate_record_rejects_finished_before_started():
    """finished_at before started_at fails the model_validator check."""
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
    """A non-dict raw entry (e.g. a bare string in the array) is rejected."""
    with pytest.raises(InvalidRecordError):
        validate_record("not-a-dict", index=0)
