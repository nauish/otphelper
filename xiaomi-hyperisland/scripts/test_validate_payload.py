#!/usr/bin/env python3
"""Pure stdlib tests for structural preflight; run: python -m unittest discover -s scripts."""
import copy
import unittest

from validate_payload import lint_payload


class TestPayloadLint(unittest.TestCase):
    def setUp(self):
        self.good = {
            "param_v2": {
                "business": "taxi",
                "updatable": True,
                "param_island": {
                    "bigIslandArea": {"imageTextInfoLeft": {"type": 1}},
                    "smallIslandArea": {"picInfo": {"type": 1}},
                    "islandTimeout": 900,
                },
            }
        }

    def test_valid_envelope(self):
        errors, _, size = lint_payload(self.good)
        self.assertEqual(errors, [])
        self.assertGreater(size, 10)

    def test_missing_param_v2(self):
        errors, _, _ = lint_payload({"business": "taxi"})
        self.assertTrue(any("param_v2" in x for x in errors))

    def test_empty_area(self):
        obj = copy.deepcopy(self.good)
        obj["param_v2"]["param_island"]["smallIslandArea"] = {}
        errors, _, _ = lint_payload(obj)
        self.assertTrue(any("smallIslandArea" in x for x in errors))

    def test_utf8_byte_limit(self):
        obj = copy.deepcopy(self.good)
        obj["param_v2"]["baseInfo"] = {"title": "Package " + "A" * 3200}
        errors, _, _ = lint_payload(obj)
        self.assertTrue(any("3072" in x for x in errors))

    def test_invalid_timeout_type(self):
        obj = copy.deepcopy(self.good)
        obj["param_v2"]["timeout"] = "30"
        errors, _, _ = lint_payload(obj)
        self.assertTrue(any("timeout" in x for x in errors))

    def test_strict_placeholder(self):
        obj = copy.deepcopy(self.good)
        obj["param_v2"]["business"] = "APPROVED_BUSINESS_CODE"
        errors, _, _ = lint_payload(obj, strict=True)
        self.assertTrue(any("placeholder" in x for x in errors))


class SelectedHyperOS3TemplateTests(unittest.TestCase):
    def setUp(self):
        import json
        from pathlib import Path
        src = Path(__file__).resolve().parents[1] / 'examples' / 'package-delivery.json'
        self.obj = json.loads(src.read_text(encoding='utf-8'))

    def test_valid_selected_templates(self):
        errors, _, _ = lint_payload(
            self.obj, big_template=2, small_template=1, expanded_template='10'
        )
        self.assertEqual(errors, [])

    def test_wrong_big_template_requires_shape(self):
        errors, _, _ = lint_payload(self.obj, big_template=7)
        self.assertTrue(any('fixedWidthDigitInfo' in e for e in errors))

    def test_unlisted_expanded_template_rejected(self):
        errors, _, _ = lint_payload(self.obj, expanded_template='15')
        self.assertTrue(any('15' in e for e in errors))

    def test_small_ring_template_requires_combine(self):
        errors, _, _ = lint_payload(self.obj, small_template=2)
        self.assertTrue(any('combinePicInfo' in e for e in errors))


if __name__ == "__main__":
    unittest.main()
