from pydantic import ValidationError

from job_execution_analyser.exceptions import InvalidRecordError
from job_execution_analyser.models.records import JobRecord


def validate_record(raw: dict, index: int) -> JobRecord:
    """Parse and validate a single raw record, or raise InvalidRecordError."""
    if not isinstance(raw, dict):
        raise InvalidRecordError(index, raw, "record is not a JSON object")

    try:
        return JobRecord.model_validate(raw)
    except ValidationError as exc:
        # pydantic's default message is multi-line and verbose; collapse it
        # to one line per field so malformed-record logging stays readable.
        reason = "; ".join(
            f"{'.'.join(str(loc) for loc in err['loc'])}: {err['msg']}"
            for err in exc.errors()
        )
        raise InvalidRecordError(index, raw, reason) from exc
