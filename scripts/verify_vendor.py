#!/usr/bin/env python3
"""Verify pinned chart runtimes and bundled license files."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


EXPECTED = {
    "echarts-6.1.0/echarts.min.js": "b66b25aeb4df84e33199dc21694014d336d222cbd9deb0e5a7c14bd6aa0d0fd0",
    "d3-7.9.0/d3.min.js": "f2094bbf6141b359722c4fe454eb6c4b0f0e42cc10cc7af921fc158fceb86539",
}
LICENSES = [
    "echarts-6.1.0/LICENSE",
    "echarts-6.1.0/NOTICE",
    "d3-7.9.0/LICENSE",
    "NOTICE.md",
]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-output", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent / "assets/vendor"
    checks = []
    errors = []
    for relative, expected in EXPECTED.items():
        path = root / relative
        actual = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
        ok = actual == expected
        checks.append({"file": relative, "expected_sha256": expected, "actual_sha256": actual, "ok": ok})
        if not ok:
            errors.append(f"vendor hash mismatch: {relative}")
    for relative in LICENSES:
        if not (root / relative).is_file():
            errors.append(f"missing vendor license evidence: {relative}")
    result = {"ok": not errors, "errors": errors, "checks": checks, "license_files": LICENSES}
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if errors:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
