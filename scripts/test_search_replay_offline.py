#!/usr/bin/env python
"""Offline tests for the completion-run controls in run_formal_search.py.

A completion run re-queries only the sources that failed on the date of
record and replays every other source from its saved raw responses, so the
snapshot of a source that already succeeded cannot move. These tests need no
network access:

    python scripts/test_search_replay_offline.py
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import run_formal_search as r  # noqa: E402


def check(name: str, ok: bool) -> bool:
    print(f"{'PASS' if ok else 'FAIL'}  {name}")
    return ok


def main() -> int:
    results = []

    r.LIVE_SOURCES.clear()
    results.append(check("no --live: nothing is replayed", not r._is_replayed(Path("pubmed_x_p00.json"))))

    r.LIVE_SOURCES.update({"OpenAlex"})
    results.append(check("--live OpenAlex: PubMed page is replayed", r._is_replayed(Path("pubmed_x_p00.json"))))
    results.append(check("--live OpenAlex: DBLP page is replayed", r._is_replayed(Path("dblp_x_p00.json"))))
    results.append(check("--live OpenAlex: OpenAlex page is live", not r._is_replayed(Path("openalex_x_p00.json"))))
    # europepmc_all_ and europepmc_preprints_ must not shadow each other.
    r.LIVE_SOURCES.clear()
    r.LIVE_SOURCES.update({"EuropePMC"})
    results.append(check("EuropePMC live does not make preprints live",
                         r._is_replayed(Path("europepmc_preprints_x_p00.json"))))
    r.LIVE_SOURCES.clear()

    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "pubmed_missing_p00.json"
        r.LIVE_SOURCES.update({"OpenAlex"})
        try:
            r.fetch_json("http://unused", out)
            missing_raises = False
        except FileNotFoundError:
            missing_raises = True
        results.append(check("replay of a missing raw page raises, not skips", missing_raises))
        r.LIVE_SOURCES.clear()

        # A response that echoes the API key must never be written to disk.
        r.OPENALEX_API_KEY = "test-key-not-real"
        original = r._fetch
        r._fetch = lambda url, errors: '{"echo": "test-key-not-real"}'
        out = Path(tmp) / "openalex_echo_p00.json"
        try:
            r.fetch_json("http://unused", out)
            raised = False
        except RuntimeError:
            raised = True
        finally:
            r._fetch = original
            r.OPENALEX_API_KEY = ""
        results.append(check("key echo raises and nothing is saved", raised and not out.exists()))

    for argv, valid in [([], True), (["--live", "OpenAlex"], True), (["--live", "Scopus"], False), (["--all"], False)]:
        r.LIVE_SOURCES.clear()
        try:
            r.parse_args(argv)
            accepted = True
        except SystemExit:
            accepted = False
        results.append(check(f"parse_args {argv} accepted={valid}", accepted == valid))
    r.LIVE_SOURCES.clear()

    # A live OpenAlex run without a key must stop, not degrade to anonymous.
    for live, key, should_exit in [({"OpenAlex"}, "", True), (set(), "", True),
                                   ({"OpenAlex"}, "k", False), ({"DBLP"}, "", False)]:
        r.LIVE_SOURCES.clear(); r.LIVE_SOURCES.update(live); r.OPENALEX_API_KEY = key
        try:
            r.require_openalex_key(); exited = False
        except SystemExit:
            exited = True
        results.append(check(f"require key live={sorted(live)} key={bool(key)} exits={should_exit}",
                             exited == should_exit))
    r.LIVE_SOURCES.clear(); r.OPENALEX_API_KEY = ""

    # A truncated JSON body is re-fetched and never written to disk.
    with tempfile.TemporaryDirectory() as tmp:
        bodies = iter(['{"results": [1, 2', '{"results": []}'])
        original, sleep = r._fetch, r.time.sleep
        r._fetch = lambda url, errors: next(bodies)
        r.time.sleep = lambda s: None
        out = Path(tmp) / "openalex_trunc_p00.json"
        try:
            data = r.fetch_json("http://unused", out)
        finally:
            r._fetch, r.time.sleep = original, sleep
        results.append(check("truncated JSON is retried, valid body saved",
                             data == {"results": []} and out.read_text() == '{"results": []}'))
        bodies = iter(['{"x', '{"x', '{"x', '{"x'])
        r._fetch = lambda url, errors: next(bodies); r.time.sleep = lambda s: None
        out = Path(tmp) / "openalex_trunc2_p00.json"
        try:
            r.fetch_json("http://unused", out); raised = False
        except ValueError:
            raised = True
        finally:
            r._fetch, r.time.sleep = original, sleep
        results.append(check("persistently truncated JSON raises and is not saved", raised and not out.exists()))

    # A source that fails mid-pagination must contribute no records.
    import io, contextlib
    saved = {n: getattr(r, n) for n in ("FAMILIES", "run_pubmed", "run_europe_pmc", "run_openalex",
                                         "run_arxiv", "run_dblp", "write_csv", "ROOT")}
    def partial_then_fail(family, acc, *a):
        r.add_candidate(acc, source="OpenAlex", query_family="f", id="x", title="Partial page")
        raise RuntimeError("HTTP 429 on page 2")
    ok_none = lambda family, acc, *a: (0, False)
    written = {}
    try:
        r.FAMILIES = saved["FAMILIES"][:1]
        r.run_pubmed = r.run_europe_pmc = r.run_arxiv = r.run_dblp = ok_none
        r.run_openalex = partial_then_fail
        r.write_csv = lambda rows, path: written.setdefault("rows", rows)
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "sources").mkdir()
            r.ROOT = Path(tmp)
            sys.argv = ["x", "--live", "DBLP"]
            with contextlib.redirect_stdout(io.StringIO()):
                r.main()
    finally:
        for n, v in saved.items():
            setattr(r, n, v)
    results.append(check("failed source leaves no partial records", written.get("rows") == []))

    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
