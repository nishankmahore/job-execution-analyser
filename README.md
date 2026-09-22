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
or

```bash
job_execution_analyser -f path/to/records.json
```

Options:

- `-f, --file` (required) — path to a JSON file containing job execution records.
- `-v, --verbose` — log a warning for each malformed record that gets skipped.

A sample input file is provided at `data/sample_jobs.json` (includes a couple
of intentionally malformed records to show graceful handling).

## Use as a library

```python
from job_execution_analyser.cli import run

summary = run("data/sample_jobs.json", verbose=True)
print(summary.total_jobs)
```

See `examples/basic_usage.py` (run with `uv run python examples/basic_usage.py`).

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

## Possible improvements

- `load_records` reads the whole file into memory via `json.loads`; a
  streaming parser (e.g. `ijson`) would scale better for very large inputs.
- `retried_job_ids` treats any record with `attempt > 1` as retried. If a
  job's retries appear as separate records sharing one `job_id` rather
  than one record with the final `attempt`, this should instead group by
  `job_id` and check for `attempt` counts/values across the group.
- No timezone normalization — `started_at`/`finished_at` are parsed as-is,
  so mixed naive/aware timestamps in the same file would compare
  inconsistently.
- Only JSON output is supported; a `--format table|csv` option would help
  for human-facing use.
- No CI workflow (e.g. GitHub Actions) wired up to run tests/lint on push.
- Record validation runs sequentially; for very large files this could be
  parallelized (e.g. a thread pool) since each record validates
  independently — validation is mostly I/O-light CPU work, so gains would
  depend on record count vs. per-record overhead.
- Logging goes to stderr by default via loguru; no `--log-level` or file
  sink is configurable from the CLI.
