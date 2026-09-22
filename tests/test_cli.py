import json

import pytest
from click.testing import CliRunner
from loguru import logger

from job_execution_analyser.cli import cli, run


def test_main_reports_summary(tmp_path):
    """CLI runs end-to-end and prints the summary as JSON on success."""
    payload = [
        {
            "job_id": "job-1",
            "status": "success",
            "started_at": "2026-09-20T08:00:00",
            "finished_at": "2026-09-20T08:05:00",
            "attempt": 1,
        }
    ]
    path = tmp_path / "records.json"
    path.write_text(json.dumps(payload))

    result = CliRunner().invoke(cli, ["-f", str(path)])

    assert result.exit_code == 0
    assert '"total_jobs": 1' in result.output


def test_main_exits_nonzero_for_missing_file():
    """click's --file validation rejects a nonexistent path before the CLI runs."""
    result = CliRunner().invoke(cli, ["-f", "does-not-exist.json"])

    assert result.exit_code != 0


def test_main_verbose_logs_malformed_records(tmp_path):
    """-v logs a warning for each skipped malformed record."""
    # Attach a throwaway loguru sink rather than fighting pytest's stream
    # capture for loguru's own stderr handler.
    messages: list[str] = []
    sink_id = logger.add(messages.append, level="WARNING")

    payload = [{"job_id": "job-1", "started_at": "2026-09-20T08:00:00", "attempt": 1}]
    path = tmp_path / "records.json"
    path.write_text(json.dumps(payload))

    try:
        result = CliRunner().invoke(cli, ["-f", str(path), "-v"])
    finally:
        logger.remove(sink_id)

    assert result.exit_code == 0
    assert any("record at index 0 is invalid" in m for m in messages)


def test_run_raises_systemexit_for_bad_input(tmp_path):
    """run() itself (not just the CLI) exits non-zero on a missing file."""
    # Bypasses click's Path(exists=True) check to exercise run()'s own
    # JobDataError -> SystemExit handling directly.
    with pytest.raises(SystemExit):
        run(str(tmp_path / "does-not-exist.json"))
