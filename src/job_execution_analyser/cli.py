from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="job_execution_analyser",
        description="Analyse job execution records from a JSON file.",
    )
    parser.add_argument(
        "-f",
        "--file",
        required=True,
        type=str,
        help="Path to JSON file containing job execution records.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    print(f"Would process file: {args.file}")


if __name__ == "__main__":
    main()
