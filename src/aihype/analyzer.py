"""Heuristic analysis of rhetorical signals in text.

This module identifies selected phrases and does not determine whether
a statement is accurate, misleading, or supported by evidence.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class PhraseSignal:
    """A phrase that may indicate a rhetorical framing pattern."""

    category: str
    phrase: str
    weight: int


@dataclass(frozen=True)
class Finding:
    """A detected phrase and its occurrence count."""

    category: str
    phrase: str
    count: int
    weight: int


@dataclass(frozen=True)
class Analysis:
    """Summary of detected signals in the supplied text."""

    word_count: int
    score: int
    level: str
    findings: tuple[Finding, ...]

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-compatible representation."""
        return asdict(self)


SIGNALS: tuple[PhraseSignal, ...] = (
    PhraseSignal("catastrophe", "existential threat", 3),
    PhraseSignal("catastrophe", "human extinction", 3),
    PhraseSignal("catastrophe", "wipe out humanity", 3),
    PhraseSignal("catastrophe", "end of humanity", 3),
    PhraseSignal("catastrophe", "out of control", 2),
    PhraseSignal("catastrophe", "catastrophic", 2),
    PhraseSignal("certainty", "inevitable", 2),
    PhraseSignal("certainty", "guaranteed", 2),
    PhraseSignal("certainty", "no doubt", 2),
    PhraseSignal("certainty", "certain to", 2),
    PhraseSignal("urgency", "before it is too late", 2),
    PhraseSignal("urgency", "before it's too late", 2),
    PhraseSignal("urgency", "act now", 2),
    PhraseSignal("urgency", "time is running out", 2),
    PhraseSignal("urgency", "immediately", 1),
    PhraseSignal("scale", "all jobs", 1),
    PhraseSignal("scale", "every job", 1),
    PhraseSignal("scale", "everyone", 1),
    PhraseSignal("scale", "humanity", 1),
)


def _count_phrase(text: str, phrase: str) -> int:
    """Count whole-phrase matches, allowing flexible whitespace."""
    parts = phrase.split()
    expression = r"\s+".join(re.escape(part) for part in parts)
    pattern = re.compile(rf"(?<!\w){expression}(?!\w)", re.IGNORECASE)
    return len(pattern.findall(text))


def analyze(text: str) -> Analysis:
    """Identify selected rhetorical signals and calculate a heuristic score."""
    words = re.findall(r"\b[\w'-]+\b", text)
    word_count = len(words)

    findings: list[Finding] = []
    weighted_points = 0

    for signal in SIGNALS:
        count = _count_phrase(text, signal.phrase)
        if count:
            findings.append(
                Finding(
                    category=signal.category,
                    phrase=signal.phrase,
                    count=count,
                    weight=signal.weight,
                )
            )
            weighted_points += count * signal.weight

    # Normalize against text length. This is a heuristic index, not a
    # probability, factuality score, or measurement of author intent.
    score = min(100, round(weighted_points / max(1, word_count / 12) * 10))

    if score >= 45:
        level = "high"
    elif score >= 20:
        level = "moderate"
    else:
        level = "low"

    return Analysis(
        word_count=word_count,
        score=score,
        level=level,
        findings=tuple(findings),
    )
