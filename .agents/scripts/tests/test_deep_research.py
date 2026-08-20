"""Tests for the deep-research evidence-ledger validator."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_PATH = ROOT / "skills/deep-research/scripts/validate_report.py"
SPEC = importlib.util.spec_from_file_location("deep_research_validator", VALIDATOR_PATH)
assert SPEC is not None and SPEC.loader is not None
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def valid_report() -> dict[str, object]:
    return {
        "question": "Which claim is supported?",
        "searched_at": "2026-08-20",
        "providers": ["runtime_web_search", "runtime_page_reader"],
        "unavailable_providers": [],
        "sources": [
            {
                "id": "s1",
                "url": "https://example.org/source",
                "publisher": "Example Institute",
                "source_type": "primary",
            }
        ],
        "claims": [
            {
                "id": "c1",
                "text": "A bounded claim.",
                "kind": "sourced",
                "confidence": "low",
                "source_ids": ["s1"],
                "independent_source_count": 1,
                "conflict": False,
            }
        ],
        "gaps": [],
    }


class DeepResearchValidatorTests(unittest.TestCase):
    def test_accepts_internally_consistent_report(self) -> None:
        self.assertEqual(validator.validate(valid_report()), [])

    def test_rejects_overstated_confidence_and_unknown_source(self) -> None:
        report = valid_report()
        claim = report["claims"][0]
        claim["confidence"] = "high"
        claim["source_ids"] = ["missing"]

        errors = validator.validate(report)

        self.assertTrue(any("unknown source id" in error for error in errors))
        self.assertTrue(any("requires at least 3" in error for error in errors))
        self.assertTrue(any("not referenced" in error for error in errors))

    def test_rejects_duplicate_providers_and_conflicting_high_confidence(self) -> None:
        report = valid_report()
        report["providers"] = ["runtime_web_search", "runtime_web_search"]
        claim = report["claims"][0]
        claim["confidence"] = "high"
        claim["independent_source_count"] = 3
        claim["conflict"] = True

        errors = validator.validate(report)

        self.assertIn("providers must contain at least two unique capabilities", errors)
        self.assertIn("providers must not contain duplicates", errors)
        self.assertTrue(any("exceeds its source references" in error for error in errors))
        self.assertTrue(any("cannot be high confidence" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
