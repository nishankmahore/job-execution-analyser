import json

from click.testing import CliRunner

from job_execution_analyser.cli import cli


def test_main_reports_summary(tmp_path):
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
    result = CliRunner().invoke(cli, ["-f", "does-not-exist.json"])

    assert result.exit_code != 0
