import click
from loguru import logger

from job_execution_analyser.exceptions import JobDataError
from job_execution_analyser.io.loader import load_records


def run(input_file: str, verbose: bool = False) -> None:
    """Load and report on a job records file.

    Plain function, no click machinery — importable directly via
    ``from job_execution_analyser.cli import run`` for callers that don't
    want the CLI wrapper.

    Args:
        input_file: Path to a JSON file containing job execution records.
        verbose: If True, log a warning for each malformed record skipped.

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

    # TODO: wire up core.analyzer here once it's implemented.
    logger.info(
        "Loaded {} valid record(s), skipped {}.",
        len(result.records),
        len(result.errors),
    )


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
def main(input_file: str, verbose: bool) -> None:
    run(input_file, verbose)


if __name__ == "__main__":
    # Lets `python -m job_execution_analyser.cli` work during local dev,
    # on top of the installed `job_execution_analyser` console script.
    main()
