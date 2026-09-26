# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: Apache-2.0
"""Authors are people: no commit may credit an AI assistant as author, committer, co-author or generator.

  python tools/check_authorship.py                  every commit reachable from HEAD (CI: fetch-depth 0)
  python tools/check_authorship.py --range A..B     only the commits in a range (pre-push hook)
  python tools/check_authorship.py --message-file F one commit message (commit-msg hook)

Exit 0: clean · 1: an AI credit was found · 2: could not check (git missing, bad range, shallow clone).
The rule itself lives in tools/_authorship.py (AUTHORSHIP_PATTERNS); tools/validate.py applies it to files.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _authorship import authorship_findings  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent

SEP_COMMIT, SEP_FIELD = "\x1e", "\x1f"


def git(root: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True,
                          text=True, encoding="utf-8").stdout


def scan_commits(root: Path, rev: str) -> list[str]:
    fmt = SEP_FIELD.join(("%H", "%an <%ae>", "%cn <%ce>", "%B")) + SEP_COMMIT
    out = []
    for rec in git(root, "log", f"--format={fmt}", rev, "--").split(SEP_COMMIT):
        rec = rec.strip("\n")
        if not rec:
            continue
        sha, author, committer, body = rec.split(SEP_FIELD, 3)
        for who, value in (("author", author), ("committer", committer)):
            for _, what, hit in authorship_findings(value + "\n" + "co-authored-by: " + value):
                out.append(f"{sha[:12]} {who} {value!r}: {what}")
                break
        for line, what, hit in authorship_findings(body):
            out.append(f"{sha[:12]} message line {line}: {what}: {hit!r}")
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--root", default=str(REPO_ROOT))
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--range", help="revision range, e.g. origin/main..HEAD (default: all of HEAD)")
    g.add_argument("--message-file", help="check one commit message file (commit-msg hook)")
    ns = ap.parse_args(argv)
    root = Path(ns.root)
    try:
        if ns.message_file:
            text = Path(ns.message_file).read_text(encoding="utf-8", errors="replace")
            text = "\n".join(line for line in text.split("\n") if not line.startswith("#"))
            found = [f"message line {n}: {what}: {hit!r}" for n, what, hit in authorship_findings(text)]
            what_ran = "the commit message"
        else:
            if not ns.range and git(root, "rev-parse", "--is-shallow-repository").strip() == "true":
                print("check_authorship: shallow clone — could not check the whole history "
                      "(check out with fetch-depth: 0)", file=sys.stderr)
                return 2
            rev = ns.range or "HEAD"
            found = scan_commits(root, rev)
            n = len(git(root, "rev-list", rev, "--").split())
            what_ran = f"{n} commit(s) in {rev}"
    except (OSError, subprocess.CalledProcessError) as exc:
        detail = getattr(exc, "stderr", "") or str(exc)
        print(f"check_authorship: could not check ({detail.strip()})", file=sys.stderr)
        return 2
    if found:
        print(f"check_authorship: {len(found)} AI-assistant credit(s) in {what_ran}. Authors are people "
              "(CONTRIBUTING.md); reword the commit message(s) and push again.")
        for f in found:
            print("  " + f)
        return 1
    print(f"check_authorship: OK — {what_ran}, no AI-assistant credit")
    return 0


if __name__ == "__main__":
    sys.exit(main())
