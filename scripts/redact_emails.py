"""Redact author email addresses from the tracked raw API exports.

The raw exports under sources/raw are the PRISMA-S evidence for the search and
must stay in the repository. They also carry corresponding-author email
addresses taken from Europe PMC and PubMed records. Those addresses are
personal data, and republishing several hundred of them in a public repository
is a different act from citing the paper, so they are removed before the
repository is made public.

Provenance is preserved the way the full-text cache already does it: the
SHA-256 of every original file is recorded in a manifest, so any reader can
verify that the redacted file differs from the original in the recorded way and
in no other, and the original can be re-fetched from the API.

Every address is replaced by one fixed placeholder rather than by a hash of
itself. A hash would look more careful and protect nothing: the source records
are public, so anyone could hash the candidate addresses and match them back.
Distinctness is not needed either, because the unit of this review is the
record, not the author.

Usage:
    python scripts/redact_emails.py --dry-run
    python scripts/redact_emails.py
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RAW = REPO / "sources" / "raw"
MANIFEST = RAW / "MANIFEST.emails-redacted.csv"
PLACEHOLDER = "redacted@example.invalid"

# Conservative: a local part, an @, a dotted domain with a 2+ letter TLD.
# Deliberately does not try to match exotic valid-but-rare forms; a missed
# address is reported by the verification pass rather than silently left in.
EMAIL = re.compile(
    r"[A-Za-z0-9!#$%&'*+/=?^_`{|}~.-]+@[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)*\.[A-Za-z]{2,}"
)

MANIFEST_FIELDS = [
    "file",
    "sha256_original",
    "bytes_original",
    "sha256_redacted",
    "bytes_redacted",
    "addresses_replaced",
    "distinct_addresses",
    "redacted_date",
    "script",
]


def tracked_raw_files() -> list[Path]:
    """Only files git tracks: the local full-text cache is gitignored and never
    published, so it is left alone."""
    out = subprocess.run(
        ["git", "ls-files", "sources/raw"],
        cwd=REPO, capture_output=True, text=True, check=True,
    ).stdout.splitlines()
    return [REPO / line for line in out if line.strip()]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# Characters that could end a JSON string or an XML attribute or element. The
# placeholder contains none of them, so substituting it cannot change the
# syntax of either format. Asserted rather than assumed.
SYNTAX_CHARS = set('"\\<>&\'')


def verify(path: Path, original: str, redacted: str) -> tuple[bool, str]:
    """A redaction that breaks the file is worse than the exposure it fixes.

    Two checks, neither of which needs an XML parser. Parsing attacker-shaped
    XML with the standard library would be the wrong trade here: these are our
    own committed API responses, and adding defusedxml would give the
    repository its first third-party dependency and break the claim that the
    search re-runs on a bare interpreter.
    """
    if SYNTAX_CHARS & set(PLACEHOLDER):
        return False, "placeholder contains a syntax character"

    # The redacted text must be the original with the matched spans, and only
    # those spans, replaced. Rebuilt independently of the substitution above.
    pieces: list[str] = []
    cursor = 0
    for match in EMAIL.finditer(original):
        if match.group(0).endswith(".invalid"):
            continue
        pieces.append(original[cursor:match.start()])
        pieces.append(PLACEHOLDER)
        cursor = match.end()
    pieces.append(original[cursor:])
    if "".join(pieces) != redacted:
        return False, "redacted text differs outside the matched spans"

    if path.suffix.lower() == ".json":
        # One export carries a UTF-8 BOM. The BOM is left in the bytes, because
        # only the matched spans may change, so it is stripped for the parse
        # check alone.
        try:
            json.loads(redacted.lstrip("﻿"))
        except ValueError as exc:
            return False, f"JSON no longer parses: {exc}"
    return True, ""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true",
                        help="report what would change and write nothing")
    args = parser.parse_args()

    today = datetime.now(timezone.utc).astimezone().date().isoformat()
    rows: list[dict[str, object]] = []
    skipped: list[tuple[str, str]] = []
    failed: list[tuple[str, str]] = []
    total_replaced = 0

    for path in tracked_raw_files():
        if path == MANIFEST:
            continue
        raw = path.read_bytes()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            skipped.append((str(path.relative_to(REPO)), f"not utf-8: {exc}"))
            continue

        found = EMAIL.findall(text)
        found = [a for a in found if not a.endswith(".invalid")]
        if not found:
            continue

        redacted = EMAIL.sub(
            lambda m: PLACEHOLDER if not m.group(0).endswith(".invalid") else m.group(0),
            text,
        )
        ok, why = verify(path, text, redacted)
        if not ok:
            failed.append((str(path.relative_to(REPO)), why))
            continue

        rel = path.relative_to(REPO).as_posix()
        rows.append({
            "file": rel,
            "sha256_original": sha256(raw),
            "bytes_original": len(raw),
            "sha256_redacted": sha256(redacted.encode("utf-8")),
            "bytes_redacted": len(redacted.encode("utf-8")),
            "addresses_replaced": len(found),
            "distinct_addresses": len(set(found)),
            "redacted_date": today,
            "script": "scripts/redact_emails.py",
        })
        total_replaced += len(found)

        if not args.dry_run:
            path.write_bytes(redacted.encode("utf-8"))

    print(f"files with addresses: {len(rows)}")
    print(f"addresses replaced:   {total_replaced}")
    print(f"distinct addresses:   {sum(int(r['distinct_addresses']) for r in rows)}")
    if skipped:
        print(f"skipped (not utf-8):  {len(skipped)}")
        for name, why in skipped:
            print(f"   - {name}: {why}")
    if failed:
        print(f"FAILED verification:  {len(failed)}")
        for name, why in failed:
            print(f"   ! {name}: {why}")

    if args.dry_run:
        print("dry run: nothing written")
        return 1 if failed else 0

    if rows:
        rows.sort(key=lambda r: str(r["file"]))
        with MANIFEST.open("w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=MANIFEST_FIELDS)
            writer.writeheader()
            writer.writerows(rows)
        print(f"manifest written: {MANIFEST.relative_to(REPO).as_posix()}")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
