#!/usr/bin/env python3
"""HyperOS 3-only design preflight regression tests."""
import json
import unittest
from pathlib import Path
from validate_design_spec import check

EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "ride-eta-design.json"


class DesignPreflightTests(unittest.TestCase):
    def setUp(self):
        self.spec = json.loads(EXAMPLE.read_text(encoding="utf-8"))

    def test_valid_ride_spec(self):
        self.assertFalse(check(self.spec)[0])

    def test_wrong_target_is_rejected(self):
        self.spec["platform"] = "Unsupported OS"
        self.assertTrue(any("HyperOS 3" in x for x in check(self.spec)[0]))

    def test_unlisted_template_15_is_rejected(self):
        self.spec["expandedTemplate"] = "15"
        self.assertTrue(any("template 15" in x for x in check(self.spec)[0]))

    def test_last_official_template_22_is_valid(self):
        self.spec["expandedTemplate"] = "22"
        self.assertFalse(check(self.spec)[0])

    def test_numeric_overflow_is_rejected(self):
        self.spec["states"][0]["bDigits"] = "1234"
        self.assertTrue(any("bDigits" in x for x in check(self.spec)[0]))

    def test_missing_stages_rejected(self):
        self.spec["states"] = self.spec["states"][:1]
        self.assertTrue(any("at least" in x for x in check(self.spec)[0]))


if __name__ == "__main__":
    unittest.main()
