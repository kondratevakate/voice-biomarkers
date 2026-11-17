#!/usr/bin/env python
"""Offline test: a redaction run must not erase earlier manifest rows.

    python scripts/test_redact_manifest_merge.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from redact_emails import merge_manifest  # noqa: E402


def main() -> int:
    existing = [
        {"file": "a.json", "sha256_original": "old-a"},
        {"file": "b.json", "sha256_original": "old-b"},
        {"file": "gone.json", "sha256_original": "old-gone"},
    ]
    new = [{"file": "b.json", "sha256_original": "new-b"}, {"file": "c.json", "sha256_original": "new-c"}]
    merged = merge_manifest(existing, new, lambda rel: rel != "gone.json")
    got = {r["file"]: r["sha256_original"] for r in merged}
    expected = {"a.json": "old-a", "b.json": "new-b", "c.json": "new-c"}
    ok = got == expected and [r["file"] for r in merged] == sorted(expected)
    print(f"{'PASS' if ok else 'FAIL'}  earlier rows kept, re-redacted file updated, deleted file dropped: {got}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
