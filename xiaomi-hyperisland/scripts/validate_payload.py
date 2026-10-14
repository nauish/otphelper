#!/usr/bin/env python3
"""Preflight a Xiaomi HyperIsland param_v2 JSON file (standard-library only).

This script checks documented envelope fields, core types, timeouts and the
Xiaomi FAQ's 3072 UTF-8 byte budget. It DOES NOT validate every template variant,
confirm an approved business scene, attach Android Bundles, or emulate SystemUI.

Usage:
  python scripts/validate_payload.py examples/package-delivery.json
  python scripts/validate_payload.py examples/package-delivery.json \
      --big-template 2 --small-template 1 --expanded-template 10 \
      --picture miui.focus.pic_box --action miui.focus.action_track
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

MAX_PARAM_BYTES = 3072
PIC_KEY = re.compile(r"^miui\.focus\.pic_[A-Za-z0-9_]+$")
ACTION_KEY = re.compile(r"^miui\.focus\.action_[A-Za-z0-9_]+$")


# Names identify Xiaomi's fixed approved *compositions*. These checks are
# best-effort shape preflight, not an exhaustive grammar or render guarantee.
BIG_COMPONENTS = {
    1: {"imageTextInfoLeft"},
    2: {"imageTextInfoLeft", "textInfo"},
    3: {"imageTextInfoLeft", "imageTextInfoRight"},
    4: {"imageTextInfoLeft", "imageTextInfoRight"},
    5: {"imageTextInfoLeft", "progressTextInfo"},
    6: {"imageTextInfoLeft", "sameWidthDigitInfo"},
    7: {"imageTextInfoLeft", "fixedWidthDigitInfo"},
    8: {"imageTextInfoLeft", "picInfo"},
    9: {"imageTextInfoLeft", "imageTextInfoRight"},
}
SMALL_COMPONENTS = {1: "picInfo", 2: "combinePicInfo", 3: "imageTextInfoRight"}
EXPANDED_COMPONENTS = {
    **{str(i): {"baseInfo", "picInfo"} for i in (1, 2)},
    "3": {"chatInfo", "picInfo"},
    "4": {"baseInfo", "picInfo", "progressInfo"},
    "5": {"baseInfo", "picInfo", "progressInfo"},
    "6": {"baseInfo", "picInfo", "progressInfo"},
    "7": {"chatInfo", "picInfo", "progressInfo"},
    "8": {"chatInfo", "picInfo", "hintInfo"},
    "9": {"baseInfo", "picInfo", "hintInfo"},
    "10": {"baseInfo", "picInfo", "hintInfo"},
    "11": {"highlightInfo", "picInfo", "hintInfo"},
    "12": {"chatInfo", "actions"},
    "13": {"highlightInfo", "actions"},
    "14-1": {"iconTextInfo"},
    "14-2": {"iconTextInfo", "picInfo"},
    "16": {"iconTextInfo", "actions"},
    "17": {"iconTextInfo", "picInfo", "highlightInfoV3"},
    "18": {"iconTextInfo", "picInfo", "textButton"},
    "19": {"coverInfo", "picInfo", "highlightInfoV3"},
    "20": {"baseInfo", "picInfo", "multiProgressInfo"},
    "21": {"chatInfo", "progressInfo"},
    "22": {"iconTextInfo", "picInfo", "multiProgressInfo"},
}


def lint_selected_templates(payload: dict, big: int | None, small: int | None, expanded: str | None) -> list[str]:
    errors = []
    island = payload.get("param_island", {})
    if not isinstance(island, dict):
        return errors
    big_area = island.get("bigIslandArea")
    small_area = island.get("smallIslandArea")
    if big is not None:
        if big not in BIG_COMPONENTS:
            errors.append("big template must be an official ID from 1 through 9")
        elif isinstance(big_area, dict):
            missing = BIG_COMPONENTS[big] - big_area.keys()
            if missing:
                errors.append(f"big template {big} missing components: {sorted(missing)}")
    if small is not None:
        if small not in SMALL_COMPONENTS:
            errors.append("small template must be 1, 2 or 3")
        elif isinstance(small_area, dict):
            field = SMALL_COMPONENTS[small]
            if field not in small_area:
                errors.append(f"small template {small} requires {field}")
            elif small == 3 and small_area[field].get("type") != 6:
                errors.append("small template 3 requires imageTextInfoRight.type=6")
    if expanded is not None:
        if expanded not in EXPANDED_COMPONENTS:
            errors.append("expanded template must be an official HyperOS 3 ID; 15 is not published")
        else:
            missing = EXPANDED_COMPONENTS[expanded] - payload.keys()
            if missing:
                errors.append(f"expanded template {expanded} missing components: {sorted(missing)}")
    return errors


def _walk_refs(node: Any, path: str = "$" ) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    if isinstance(node, dict):
        for key, value in node.items():
            result.extend(_walk_refs(value, f"{path}.{key}"))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            result.extend(_walk_refs(value, f"{path}[{index}]"))
    elif isinstance(node, str) and (
        node.startswith("miui.focus.pic_") or node.startswith("miui.focus.action_")
    ):
        result.append((path, node))
    return result


def lint_payload(
    obj: Any,
    *,
    picture_keys: set[str] | None = None,
    action_keys: set[str] | None = None,
    max_bytes: int = MAX_PARAM_BYTES,
    strict: bool = False,
    transport: str = "local",
    big_template: int | None = None,
    small_template: int | None = None,
    expanded_template: str | None = None,
) -> tuple[list[str], list[str], int]:
    """Return errors, warnings, and compact JSON UTF-8 bytes."""
    errors: list[str] = []
    warnings: list[str] = []
    picture_keys = picture_keys or set()
    action_keys = action_keys or set()
    try:
        compact = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
        size = len(compact.encode("utf-8"))
    except (ValueError, TypeError) as exc:
        return [f"JSON serialization error: {exc}"], [], 0

    if size > max_bytes:
        errors.append(f"miui.focus.param is {size} UTF-8 bytes; limit is {max_bytes}")
    if not isinstance(obj, dict):
        return errors + ["Top-level JSON must be an object"], warnings, size
    payload = obj.get("param_v2")
    if not isinstance(payload, dict):
        return errors + ["Required object param_v2 is missing"], warnings, size

    business = payload.get("business")
    if not isinstance(business, str) or not business.strip():
        errors.append("param_v2.business must be a nonempty string")
    elif "APPROVED" in business.upper() or "PLACEHOLDER" in business.upper():
        msg = "business contains a placeholder; replace with Xiaomi-approved scene code"
        (errors if strict else warnings).append(msg)

    island = payload.get("param_island")
    if not isinstance(island, dict):
        errors.append("param_v2.param_island must be an object")
    else:
        for area in ("bigIslandArea", "smallIslandArea"):
            value = island.get(area)
            if not isinstance(value, dict) or not value:
                errors.append(f"param_v2.param_island.{area} needs a populated template object")
        if "islandProperty" in island and (
            type(island["islandProperty"]) is not int or island["islandProperty"] not in (1, 2)
        ):
            errors.append("param_island.islandProperty must be 1 or 2")
        if "islandTimeout" in island and (
            type(island["islandTimeout"]) is not int or island["islandTimeout"] < 0
        ):
            errors.append("param_island.islandTimeout must be nonnegative integer seconds")
        if "shareData" in island:
            share = island["shareData"]
            if not isinstance(share, dict):
                errors.append("param_island.shareData must be an object")
            else:
                missing = sorted(set(("pic", "title", "content", "shareContent")) - share.keys())
                if missing:
                    warnings.append(f"shareData may be incomplete for drag-sharing: missing {missing}")

    for field in ("islandFirstFloat", "enableFloat", "updatable", "cancel", "filterWhenNoPermission"):
        if field in payload and type(payload[field]) is not bool:
            errors.append(f"param_v2.{field} must be boolean")
    if "timeout" in payload and (
        type(payload["timeout"]) is not int or payload["timeout"] < -1
    ):
        errors.append("param_v2.timeout must be integer minutes (>= -1)")
    if "sequence" in payload and (
        type(payload["sequence"]) is not int or payload["sequence"] < 0
    ):
        errors.append("param_v2.sequence must be a nonnegative integer")
    if transport == "mipush" and payload.get("updatable") and not payload.get("orderId"):
        warnings.append("For a MiPush real-time activity, supply orderId and monotonic sequence")
    if transport == "mipush" and payload.get("updatable") and "sequence" not in payload:
        warnings.append("MiPush real-time updates require sequence")
    if payload.get("islandFirstFloat") is True and payload.get("enableFloat") is True:
        warnings.append("Initial and update auto-expansion both enabled; check interruption policy")

    errors.extend(lint_selected_templates(payload, big_template, small_template, expanded_template))
    for path, ref in _walk_refs(obj):
        if ref.startswith("miui.focus.pic_"):
            if not PIC_KEY.fullmatch(ref):
                errors.append(f"Invalid picture reference format at {path}: {ref}")
            elif ref not in picture_keys:
                warnings.append(f"Picture {ref} at {path}: verify Android/remote bundle attachment")
        elif ref.startswith("miui.focus.action_"):
            if not ACTION_KEY.fullmatch(ref):
                errors.append(f"Invalid action reference format at {path}: {ref}")
            elif ref not in action_keys:
                warnings.append(f"Action {ref} at {path}: verify Notification.Action attachment")

    # Avoid repeating warnings for repeated icon references.
    warnings = list(dict.fromkeys(warnings))
    return errors, warnings, size


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="JSON file containing the param_v2 envelope")
    parser.add_argument("--picture", action="append", default=[], help="A known attached picture key")
    parser.add_argument("--action", action="append", default=[], help="A known attached action key")
    parser.add_argument("--strict", action="store_true", help="Reject placeholder business codes")
    parser.add_argument("--transport", choices=["local", "mipush"], default="local")
    parser.add_argument("--big-template", type=int, help="Verify selected big-island shape (1..9)")
    parser.add_argument("--small-template", type=int, help="Verify selected small-island shape (1..3)")
    parser.add_argument("--expanded-template", type=str, help="Verify expanded template component presence")
    args = parser.parse_args(argv)
    try:
        raw = args.path.read_bytes()
        obj = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"FAIL: could not read valid UTF-8 JSON: {exc}", file=sys.stderr)
        return 2

    errors, warnings, size = lint_payload(
        obj, picture_keys=set(args.picture), action_keys=set(args.action), strict=args.strict,
        transport=args.transport, big_template=args.big_template,
        small_template=args.small_template, expanded_template=args.expanded_template
    )
    print(f"HyperIsland structural preflight: {args.path} ({size} compact UTF-8 bytes)")
    for error in errors:
        print(f"ERROR: {error}")
    for warning in warnings:
        print(f"WARN: {warning}")
    if errors:
        print("FAILED: fix errors before real-device integration")
        return 1
    print("PASSED structural checks; renderability, business approval and permissions NOT verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
