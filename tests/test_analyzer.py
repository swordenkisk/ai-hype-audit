import unittest

from aihype.analyzer import analyze


class AnalyzeTests(unittest.TestCase):
    def test_detects_phrase_case_insensitively(self) -> None:
        result = analyze("Some claim describes an EXISTENTIAL THREAT.")

        self.assertEqual(result.word_count, 6)
        self.assertEqual(result.findings[0].phrase, "existential threat")
        self.assertEqual(result.findings[0].count, 1)

    def test_returns_no_findings_for_neutral_text(self) -> None:
        result = analyze("The report describes three model evaluation methods.")

        self.assertEqual(result.score, 0)
        self.assertEqual(result.level, "low")
        self.assertEqual(result.findings, ())

    def test_counts_repeated_phrases(self) -> None:
        result = analyze("Act now. Act now.")

        urgency = next(
            finding for finding in result.findings
            if finding.phrase == "act now"
        )
        self.assertEqual(urgency.count, 2)

    def test_score_is_capped_at_one_hundred(self) -> None:
        result = analyze(
            " ".join(["existential threat"] * 100)
        )

        self.assertEqual(result.score, 100)
        self.assertEqual(result.level, "high")


if __name__ == "__main__":
    unittest.main()
