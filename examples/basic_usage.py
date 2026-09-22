"""Example: use job_execution_analyser as a library, without the CLI.

Run with: uv run python examples/basic_usage.py
"""

from job_execution_analyser.cli import run

summary = run("data/sample_jobs.json", verbose=False)

print(f"total jobs: {summary.total_jobs}")
print(f"successful: {summary.successful_jobs}")
print(f"failed: {summary.failed_jobs}")
print(f"average success duration (s): {summary.average_success_duration_seconds}")
print(f"retried job ids: {summary.retried_job_ids}")
