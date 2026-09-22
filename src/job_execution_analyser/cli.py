import click
from loguru import logger

from job_execution_analyser.core.analyzer import summarize
from job_execution_analyser.exceptions import JobDataError
from job_execution_analyser.io.loader import load_records
from job_execution_analyser.models.summary import Summary


def run(input_file: str, verbose: bool = False) -> Summary:
    """Load and summarize a job records file.

    Plain function, no click machinery — importable directly via
    ``from job_execution_analyser.cli import run`` for callers that don't
    want the CLI wrapper. Does not print anything; the caller decides
    what to do with the result.

    Args:
        input_file: Path to a JSON file containing job execution records.
        verbose: If True, log a warning for each malformed record skipped.

    Returns:
        Summary of the valid records.

    Raises:
        SystemExit: If the input file is missing, not valid JSON, or not
            a JSON array of records.
    """
    try:
        result = load_records(input_file)
    except JobDataError:
        logger.exception("Failed to load {}", input_file)
        raise SystemExit(1) from None

    if verbose:
        for error in result.errors:
            logger.warning(str(error))

    logger.info(
        "Loaded {} valid record(s), skipped {}.",
        len(result.records),
        len(result.errors),
    )
    return summarize(result.records)


@click.command()
@click.option(
    "-f",
    "--file",
    "input_file",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
    help="Path to JSON file containing job execution records.",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Show warnings for skipped malformed records.",
)
def cli(input_file: str, verbose: bool) -> None:
    summary = run(input_file, verbose)
    click.echo(summary.model_dump_json(indent=2))


if __name__ == "__main__":
    cli()
