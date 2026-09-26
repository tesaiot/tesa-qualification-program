#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: Apache-2.0
"""Report English pages whose Thai source changed after they were translated.

    python3 tools/i18n_stale.py                    # report; exit 0
    python3 tools/i18n_stale.py --strict           # exit 1 if any translation is stale
    python3 tools/i18n_stale.py --hash path/README.md   # print the hash to put in README.en.md

A README.en.md records what it translated with `source_sha256:` in its front matter: the sha256
of the Thai README.md BODY (everything after the front matter; CRLF normalised to LF; UTF-8).
Front-matter-only edits in the Thai file (status, level, ...) do not make the translation stale.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import REPO_ROOT, iter_files, parse_yaml, read_text, split_front_matter  # noqa: E402


def body_sha256(text: str) -> str:
    body = split_front_matter(text.replace("\r\n", "\n")).body
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def scan(root: Path) -> dict[str, list]:
    """{'stale': [(en, th, recorded, actual)], 'fresh': [...], 'untracked': [en], 'orphan': [en]}"""
    res: dict[str, list] = {"stale": [], "fresh": [], "untracked": [], "orphan": []}
    for rel in iter_files(root):
        if not rel.endswith("README.en.md"):
            continue
        en = root / rel
        th = en.with_name("README.md")
        text = read_text(en) or ""
        fm = split_front_matter(text)
        recorded = None
        if fm.text is not None:
            doc = parse_yaml(fm.text)
            if not doc.error and isinstance(doc.data, dict):
                recorded = doc.data.get("source_sha256")
        if not recorded:
            res["untracked"].append(rel)
            continue
        th_text = read_text(th)
        if th_text is None:
            res["orphan"].append(rel)
            continue
        actual = body_sha256(th_text)
        key = "fresh" if str(recorded).lower() == actual else "stale"
        res[key].append((rel, th.relative_to(root).as_posix(), str(recorded), actual))
    return res


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--root", default=str(REPO_ROOT), help="repository root (default: this repo)")
    ap.add_argument("--strict", action="store_true", help="exit 1 when any translation is stale")
    ap.add_argument("--hash", metavar="README_MD", help="print the source_sha256 of a Thai README.md")
    ns = ap.parse_args(argv)
    if ns.hash:
        text = read_text(Path(ns.hash))
        if text is None:
            print(f"i18n_stale: cannot read {ns.hash}", file=sys.stderr)
            return 2
        print(body_sha256(text))
        return 0
    root = Path(ns.root).resolve()
    res = scan(root)
    for en, th, rec, act in res["stale"]:
        print(f"STALE  {en}: {th} changed since translation (recorded {rec[:12]}…, now {act[:12]}…)")
    for en in res["orphan"]:
        print(f"ORPHAN {en}: records source_sha256 but has no README.md next to it")
    print(f"i18n_stale: {len(res['stale'])} stale, {len(res['fresh'])} fresh, "
          f"{len(res['untracked'])} without source_sha256, {len(res['orphan'])} orphan")
    if ns.strict and (res["stale"] or res["orphan"]):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
