import json
from dataclasses import dataclass, field
from pathlib import Path

from job_execution_analyser.exceptions import InvalidRecordError, JobDataError
from job_execution_analyser.io.validators import validate_record
from job_execution_analyser.models.records import JobRecord


@dataclass
class LoadResult:
    """Split outcome so one bad record never blocks the good ones."""

    records: list[JobRecord] = field(default_factory=list)
    errors: list[InvalidRecordError] = field(default_factory=list)


def load_records(path: str | Path) -> LoadResult:
    """Read a JSON file and validate its contents into a LoadResult."""
    path = Path(path)

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise JobDataError(f"Input file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise JobDataError(f"Input file is not valid JSON: {path}") from exc

    if not isinstance(payload, list):
        raise JobDataError(f"{path} must contain a JSON array of records")

    result = LoadResult()
    for index, raw in enumerate(payload):
        try:
            result.records.append(validate_record(raw, index))
        except InvalidRecordError as exc:
            result.errors.append(exc)
    return result
