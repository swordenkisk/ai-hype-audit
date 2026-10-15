"""Command-line interface for AI Hype Audit."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from aihype.analyzer import Analysis, analyze


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ai-hype-audit",
        description="Identify selected rhetorical signals in AI-related text.",
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--text", help="Text to analyze.")
    source.add_argument("--file", type=Path, help="UTF-8 text file to analyze.")
    source.add_argument(
        "--stdin",
        action="store_true",
        help="Read text from standard input.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print the result as JSON.",
    )
    return parser


def _read_input(args: argparse.Namespace) -> str:
    if args.text is not None:
        return args.text
    if args.file is not None:
        return args.file.read_text(encoding="utf-8")
    return sys.stdin.read()


def _format_report(result: Analysis) -> str:
    lines = [
        f"Rhetorical-signal index: {result.score}/100 ({result.level})",
        f"Words analyzed: {result.word_count}",
        "",
        "This heuristic flags selected wording; it does not assess factual accuracy.",
    ]

    if not result.findings:
        lines.extend(["", "No phrases from the current signal list were detected."])
        return "\n".join(lines)

    lines.extend(["", "Detected phrases:"])
    for finding in result.findings:
        count_label = "occurrence" if finding.count == 1 else "occurrences"
        lines.append(
            f"- [{finding.category}] “{finding.phrase}” "
            f"— {finding.count} {count_label}"
        )

    return "\n".join(lines)


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    try:
        text = _read_input(args)
    except OSError as error:
        print(f"Error reading input: {error}", file=sys.stderr)
        return 2

    if not text.strip():
        print("Error: input text is empty.", file=sys.stderr)
        return 2

    result = analyze(text)

    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(_format_report(result))

    return 0
