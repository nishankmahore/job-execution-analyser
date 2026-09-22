# job-execution-analyser
Python-based job execution analysis with validation, duration metrics, retry tracking, and automated tests.

## Setup

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

## Run

```bash
uv run job_execution_analyser -f path/to/records.json
```

Options:

- `-f, --file` (required) — path to a JSON file containing job execution records.
- `-v, --verbose` — log a warning for each malformed record that gets skipped.

A sample input file is provided at `data/sample_jobs.json` (includes a couple
of intentionally malformed records to show graceful handling).

## Input format

A JSON array of objects, each with:

```json
{
  "job_id": "job-1",
  "status": "success",
  "started_at": "2026-09-20T08:00:00",
  "finished_at": "2026-09-20T08:05:00",
  "attempt": 1
}
```

- `status` must be one of `success`, `failed`, `running`.
- `finished_at` is optional (e.g. for still-`running` jobs) but, when
  present, cannot be before `started_at`.
- `attempt` must be `>= 1`.

Records that fail validation are skipped rather than aborting the whole run;
use `-v` to see why each one was skipped.

## Tests

```bash
uv run pytest
```

## Dev tooling

Lint, format, and type-check:

```bash
uv run ruff check .
uv run ruff format .
uv run mypy src
```

[pre-commit](https://pre-commit.com/) is configured to run ruff and mypy on
each commit (`uv run pre-commit install` to enable it locally).
