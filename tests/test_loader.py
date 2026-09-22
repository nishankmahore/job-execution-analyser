import json

import pytest

from job_execution_analyser.exceptions import JobDataError
from job_execution_analyser.io.loader import load_records


def _write(tmp_path, payload):
    path = tmp_path / "records.json"
    path.write_text(json.dumps(payload))
    return path


def test_load_records_splits_valid_and_invalid(tmp_path):
    payload = [
        {
            "job_id": "job-1",
            "status": "success",
            "started_at": "2026-09-20T08:00:00",
            "finished_at": "2026-09-20T08:05:00",
            "attempt": 1,
        },
        {
            "job_id": "job-2",
            "status": "bogus",
            "started_at": "2026-09-20T08:00:00",
            "attempt": 1,
        },
    ]
    result = load_records(_write(tmp_path, payload))

    assert len(result.records) == 1
    assert result.records[0].job_id == "job-1"
    assert len(result.errors) == 1
    assert result.errors[0].index == 1


def test_load_records_rejects_non_array(tmp_path):
    path = _write(tmp_path, {"not": "a list"})
    with pytest.raises(JobDataError):
        load_records(path)


def test_load_records_rejects_invalid_json(tmp_path):
    path = tmp_path / "records.json"
    path.write_text("{not json")
    with pytest.raises(JobDataError):
        load_records(path)


def test_load_records_rejects_missing_file(tmp_path):
    with pytest.raises(JobDataError):
        load_records(tmp_path / "missing.json")
