"""Guard: no author email address may be committed under sources/raw.

The raw API exports carried 7,442 corresponding-author addresses, which were
replaced before the repository was made public (see
sources/raw/MANIFEST.emails-redacted.csv). A later search run writes fresh
exports from the same APIs and will bring the addresses straight back, so the
redaction has to be enforced rather than remembered.

Run after every search run, before every commit that touches sources/raw:

    python scripts/test_no_raw_emails.py
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PLACEHOLDER_DOMAIN = ".invalid"

EMAIL = re.compile(
    r"[A-Za-z0-9!#$%&'*+/=?^_`{|}~.-]+@[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)*\.[A-Za-z]{2,}"
)


def main() -> int:
    tracked = subprocess.run(
        ["git", "ls-files", "sources/raw"],
        cwd=REPO, capture_output=True, text=True, check=True,
    ).stdout.splitlines()

    offenders: list[tuple[str, int, str]] = []
    checked = 0
    for rel in tracked:
        if not rel.strip():
            continue
        path = REPO / rel
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, FileNotFoundError):
            continue
        checked += 1
        found = {a for a in EMAIL.findall(text) if not a.endswith(PLACEHOLDER_DOMAIN)}
        if found:
            # Report the count and one redacted sample, never the addresses.
            sample = sorted(found)[0]
            local, _, domain = sample.partition("@")
            offenders.append((rel, len(found), f"{local[:1]}***@{domain}"))

    print(f"tracked files checked: {checked}")
    if offenders:
        print(f"FAIL: {len(offenders)} file(s) contain unredacted addresses")
        for rel, count, sample in offenders[:20]:
            print(f"   ! {rel}: {count} distinct, e.g. {sample}")
        print("Fix: python scripts/redact_emails.py")
        return 1
    print("PASS: no unredacted author addresses under sources/raw")
    return 0


if __name__ == "__main__":
    sys.exit(main())
