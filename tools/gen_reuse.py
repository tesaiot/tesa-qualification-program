#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: Apache-2.0
"""Generate REUSE.toml (REUSE Specification 3.3) from the policy and the courses' credits.

    python3 tools/gen_reuse.py           # (re)write REUSE.toml
    python3 tools/gen_reuse.py --check   # exit 1 if REUSE.toml is missing or stale

Sources, in the order they appear in REUSE.toml (the LAST matching annotation wins):
  1. tools/policy.yaml `reuse.base`      default CC-BY-NC-4.0 (TESA), code Apache-2.0, skills CC-BY-SA-4.0 ...
  2. every courses/<id>/                 content: licence from course.yaml `license.content`, TESA
                                         (+ per-course holders from the policy, e.g. AIC for aiot)
  3. every courses/<id>/ code folders    examples/ practice/ solution/ at any depth + shared/:
                                         licence from course.yaml `license.code` (or the policy)
  4. courses/<id>/credits.yaml images    precedence = "override": the owner's licence and author
LICENSES/ is never annotated. Licences that REUSE.toml uses but LICENSES/ lacks are listed at the
end (reuse lint fails on them; add them with `reuse download <id>`).
"""
from __future__ import annotations

import argparse
import difflib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import REPO_ROOT, iter_course_dirs, load_policy, load_yaml  # noqa: E402

OUT_NAME = "REUSE.toml"
# The TOML keys below are REUSE.toml keys, written without a colon, so the reuse tool does not
# read them as this file's own licence tags.
KEY_COPYRIGHT = "SPDX-FileCopyrightText"
KEY_LICENSE = "SPDX-License-Identifier"


def toml_str(s: str) -> str:
    out = []
    for ch in str(s):
        if ch == "\\":
            out.append("\\\\")
        elif ch == '"':
            out.append('\\"')
        elif ord(ch) < 0x20 or ord(ch) == 0x7F:
            out.append(f"\\u{ord(ch):04X}")
        else:
            out.append(ch)
    return '"' + "".join(out) + '"'


def toml_list(items: list[str]) -> str:
    if len(items) == 1:
        return toml_str(items[0])
    return "[\n" + "".join(f"    {toml_str(i)},\n" for i in items) + "]"


def glob_escape(path: str) -> str:
    """A literal file path as a REUSE.toml path: escape the glob characters \\ and *."""
    return path.replace("\\", "\\\\").replace("*", "\\*")


class Annotation:
    def __init__(self, paths: list[str], license_: str, holders: list[str], precedence: str,
                 comment: str | None = None):
        self.paths = paths
        self.license = license_
        self.holders = holders
        self.precedence = precedence
        self.comment = comment

    def render(self) -> str:
        lines = ["[[annotations]]"]
        if self.comment:
            lines += [f"# {c}" for c in self.comment.splitlines()]
        lines += [f"path = {toml_list(self.paths)}",
                  f"precedence = {toml_str(self.precedence)}",
                  f"{KEY_COPYRIGHT} = {toml_list(self.holders)}",
                  f"{KEY_LICENSE} = {toml_str(self.license)}"]
        return "\n".join(lines)


def _holders(policy_reuse: dict, keys: list[str]) -> list[str]:
    table = policy_reuse.get("holders") or {}
    out = []
    for k in keys:
        if k not in table:
            raise SystemExit(f"gen_reuse: tools/policy.yaml reuse.holders has no {k!r}")
        out.append(table[k])
    return out


def build(root: Path, policy: dict) -> tuple[list[Annotation], list[str]]:
    """(annotations in order, notes to print)."""
    pr = policy.get("reuse") or {}
    notes: list[str] = []
    anns: list[Annotation] = []
    for b in pr.get("base") or []:
        anns.append(Annotation(list(b["paths"]), b["license"], _holders(pr, b["holders"]),
                               b.get("precedence", "closest"), b.get("comment")))
    content = pr.get("course_content") or {}
    code = pr.get("course_code") or {}
    overrides = pr.get("courses") or {}
    lic_map = pr.get("credits_license_map") or {}
    credit_anns: list[Annotation] = []
    for cdir in iter_course_dirs(root):
        cid = cdir.name
        ov = overrides.get(cid) or {}
        cy = load_yaml(cdir / "course.yaml") if (cdir / "course.yaml").is_file() else None
        course = cy.data if cy is not None and not cy.error and isinstance(cy.data, dict) else {}
        if not course:
            notes.append(f"courses/{cid}: no readable course.yaml — content defaults to CC-BY-NC-4.0"
                         + ("" if ov.get("code_license") else "; code folders get no code licence yet"))
        lic = course.get("license") if isinstance(course.get("license"), dict) else {}
        c_lic = ov.get("content_license") or lic.get("content") or "CC-BY-NC-4.0"
        c_hold = _holders(pr, ov.get("content_holders") or content.get("default_holders") or ["tesa"])
        anns.append(Annotation([f"courses/{cid}/**"], c_lic, c_hold, content.get("precedence", "aggregate"),
                               f"Course {cid}: content"))
        res = pr.get("course_resources") or {}
        if res.get("license"):
            anns.append(Annotation([f"courses/{cid}/**/{d}/**" for d in res.get("dirs") or ["resources"]],
                                   res["license"], c_hold, res.get("precedence", "aggregate"),
                                   f"Course {cid}: templates in resources/"))
        k_lic = ov.get("code_license") or lic.get("code")
        if k_lic and k_lic != "none":
            dirs = code.get("dirs") or ["examples", "practice", "solution"]
            paths = [f"courses/{cid}/**/{d}/**" for d in dirs]
            if code.get("shared"):
                paths.append(f"courses/{cid}/{code['shared']}/**")
            k_hold = _holders(pr, ov.get("code_holders") or code.get("default_holders") or ["tesa"])
            anns.append(Annotation(paths, k_lic, k_hold, code.get("precedence", "closest"),
                                   f"Course {cid}: code"))
        cr = load_yaml(cdir / "credits.yaml") if (cdir / "credits.yaml").is_file() else None
        if cr is None:
            continue
        if cr.error or not isinstance(cr.data, dict):
            notes.append(f"courses/{cid}/credits.yaml is unreadable ({cr.error}); its images are not annotated")
            continue
        groups: dict[tuple[str, str], list[str]] = {}
        for im in cr.data.get("images") or []:
            if not isinstance(im, dict) or not im.get("path") or not im.get("license"):
                continue
            raw = str(im["license"]).strip()
            mapped = lic_map[raw] if raw in lic_map else raw
            if mapped is None:
                continue   # own work: the course content annotation applies
            author = str(im.get("author") or "").strip() or "unknown author"
            groups.setdefault((mapped, author), []).append(glob_escape(f"courses/{cid}/{im['path']}"))
        for (lic_id, author), paths in sorted(groups.items(), key=lambda kv: (sorted(kv[1])[0], kv[0])):
            credit_anns.append(Annotation(sorted(set(paths)), lic_id, [author], "override",
                                          f"Third-party ({cid}/credits.yaml)"))
    return anns + credit_anns, notes


def render(root: Path, policy: dict) -> tuple[str, list[str], set[str]]:
    anns, notes = build(root, policy)
    head = [
        "# GENERATED by tools/gen_reuse.py from tools/policy.yaml, courses/*/course.yaml and",
        "# courses/*/credits.yaml. Do not edit by hand: change the policy or a credits.yaml, then run",
        "# `python3 tools/gen_reuse.py`. CI runs `python3 tools/gen_reuse.py --check` and `reuse lint`.",
        "# REUSE Specification 3.3: the LAST annotation that matches a path wins.",
        "",
        "version = 1",
    ]
    body = "\n\n".join(a.render() for a in anns)
    used: set[str] = set()
    for a in anns:
        for tok in re.split(r"[\s()]+", a.license):
            if tok and tok not in ("AND", "OR", "WITH"):
                used.add(tok.rstrip("+"))
    return "\n".join(head) + "\n\n" + body + "\n", notes, used


def missing_licenses(root: Path, used: set[str]) -> list[str]:
    ldir = root / "LICENSES"
    have = {p.stem for p in ldir.iterdir() if p.is_file()} if ldir.is_dir() else set()
    return sorted(used - have)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--root", default=str(REPO_ROOT), help="repository root (default: this repo)")
    ap.add_argument("--check", action="store_true", help="exit 1 if REUSE.toml is missing or stale")
    ns = ap.parse_args(argv)
    root = Path(ns.root).resolve()
    text, notes, used = render(root, load_policy())
    for n in notes:
        print(f"gen_reuse: note: {n}", file=sys.stderr)
    for lic in missing_licenses(root, used):
        how = ("write the licence text by hand" if lic.startswith("LicenseRef-")
               else f"run `reuse download {lic}`")
        print(f"gen_reuse: warning: REUSE.toml uses {lic} but LICENSES/ has no {lic}.txt — {how} "
              "(reuse lint fails until then)", file=sys.stderr)
    out = root / OUT_NAME
    if ns.check:
        current = out.read_text(encoding="utf-8") if out.is_file() else ""
        if current != text:
            print(f"gen_reuse: {OUT_NAME} is {'stale' if current else 'missing'} — run "
                  "`python3 tools/gen_reuse.py` and commit the result", file=sys.stderr)
            sys.stderr.writelines(list(difflib.unified_diff(
                current.splitlines(keepends=True), text.splitlines(keepends=True),
                f"{OUT_NAME} (committed)", f"{OUT_NAME} (generated)", n=1))[:60])
            return 1
        print(f"gen_reuse: {OUT_NAME} is up to date")
        return 0
    if not out.is_file() or out.read_text(encoding="utf-8") != text:
        out.write_text(text, encoding="utf-8")
        print(f"gen_reuse: wrote {OUT_NAME} ({text.count('[[annotations]]')} annotations)")
    else:
        print(f"gen_reuse: {OUT_NAME} unchanged")
    return 0


if __name__ == "__main__":
    sys.exit(main())
