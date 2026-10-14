#!/usr/bin/env python3
"""Preflight a HyperOS 3-only Xiaomi HyperIsland UX scene spec.

Checks official template IDs, lifecycle completeness, icon dimensions and
conservative compact digit limits. This DOES NOT prove runtime rendering,
Xiaomi service approval, Figma accuracy, or full component JSON correctness.

Usage: python scripts/validate_design_spec.py examples/ride-eta-design.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

EXPANDED = {str(i) for i in range(1, 14)} | {"14-1", "14-2"} | {str(i) for i in range(16, 23)}
ASCII_DIGITS = re.compile(r"^[0-9]{1,3}$")


def check(spec: object) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(spec, dict):
        return ["Root must be a JSON object"], warnings

    if spec.get("platform") != "HyperOS 3":
        errors.append('platform must be exactly "HyperOS 3"')
    if "osTargets" in spec or "expandedTemplates" in spec:
        errors.append("Use a single HyperOS 3 'expandedTemplate', not multi-version templates")
    if not isinstance(spec.get("scenario"), str) or not spec["scenario"].strip():
        errors.append("scenario must describe an active task")

    expanded = spec.get("expandedTemplate")
    if not isinstance(expanded, str) or expanded not in EXPANDED:
        errors.append("expandedTemplate must be one of the live official IDs (no template 15)")

    summary = spec.get("summary")
    if not isinstance(summary, dict):
        errors.append("summary must include official big and small template IDs")
        summary = {}
    big = summary.get("bigTemplate")
    small = summary.get("smallTemplate")
    if type(big) is not int or big not in range(1, 10):
        errors.append("summary.bigTemplate must be an integer 1..9")
    if type(small) is not int or small not in range(1, 4):
        errors.append("summary.smallTemplate must be an integer 1..3")
    pixels = summary.get("iconPixels")
    if pixels is not None and (
        not isinstance(pixels, list)
        or len(pixels) != 2
        or any(type(n) is not int or n < 88 for n in pixels)
        or pixels[0] != pixels[1]
    ):
        errors.append("summary.iconPixels must be a square icon >= 88x88 px")
    if pixels is None:
        warnings.append("Provide a square >=88x88 px summary icon in the design handoff")

    states = spec.get("states")
    if not isinstance(states, list) or len(states) < 2:
        errors.append("states must contain at least create/update and termination stages")
        states = []
    seen_ids: set[str] = set()
    for i, state in enumerate(states):
        path = f"states[{i}]"
        if not isinstance(state, dict):
            errors.append(f"{path} must be an object")
            continue
        node_id = state.get("id")
        if not isinstance(node_id, str) or not node_id.strip():
            errors.append(f"{path}.id must name a lifecycle stage")
        elif node_id in seen_ids:
            errors.append(f"{path}.id duplicated: {node_id}")
        else:
            seen_ids.add(node_id)
        for field in ("trigger", "aText", "expandedHeadline", "fallbackTitle", "fallbackBody"):
            val = state.get(field)
            if not isinstance(val, str) or not val.strip():
                errors.append(f"{path}.{field} must be a nonempty string")
        if type(state.get("autoExpand")) is not bool:
            errors.append(f"{path}.autoExpand must be boolean")
        if big == 7:
            if not isinstance(state.get("bDigits"), str) or not ASCII_DIGITS.fullmatch(state["bDigits"]):
                errors.append(f"{path}.bDigits must contain 1..3 ASCII digits for big template 7")
            unit = state.get("bUnit", "")
            if not isinstance(unit, str) or len(unit) > 2:
                warnings.append(f"{path}.bUnit might overflow; measure font widths on the device")
        if small == 3:
            digits = state.get("smallDigits")
            if not isinstance(digits, str) or not ASCII_DIGITS.fullmatch(digits):
                errors.append(f"{path}.smallDigits must contain 1..3 digits")
        for field in ("islandTimeoutSeconds", "dismissAfterSeconds"):
            if field in state and (type(state[field]) is not int or state[field] < 0):
                errors.append(f"{path}.{field} must be nonnegative integer seconds")
        if isinstance(state.get("aText"), str) and len(state["aText"]) > 5:
            warnings.append(f"{path}.aText may overflow; inspect actual glyph width")

    if states and not any(
        isinstance(s, dict) and ("dismissAfterSeconds" in s or "cancel" in str(s.get("id", "")).lower())
        for s in states
    ):
        warnings.append("No explicit termination/dismiss stage found")
    if spec.get("approvalStatus") != "approved":
        warnings.append("Xiaomi scene approval is not confirmed")
    warnings.append("Design preflight only; verify Figma reference and authorized device rendering")
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    try:
        spec = json.loads(args.path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError) as exc:
        print(f"ERROR: could not read JSON: {exc}", file=sys.stderr)
        return 2
    errors, warnings = check(spec)
    for item in errors:
        print("ERROR:", item)
    for item in warnings:
        print("WARN:", item)
    print("PASS: HyperOS 3 design preflight only" if not errors else "FAIL: Design preflight")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
