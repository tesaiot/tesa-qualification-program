#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: Apache-2.0
"""Flag class-period wording in learner-facing text (BUILD_SPEC §1.2).

    python3 tools/check_terms.py                 # every *.md / *.mdx in the repo
    python3 tools/check_terms.py courses/foo     # a folder or files (md, mdx, yaml)

Exit 1 when anything is flagged. tools/validate.py imports this module and reports a finding as
an ERROR under courses/** and a WARNING elsewhere.

Forbidden (learner-facing prose):
  Thai    คาบเรียน · คาบ + a number (คาบ 3, คาบที่ 3, คาบที่สาม) · คาบนี้/คาบหน้า/คาบก่อน/คาบถัดไป/
          คาบที่แล้ว/คาบแรก/คาบสุดท้าย · ทุกคาบ · ต่อคาบ
  English "session N", "Session N", "session-NN", "sessions N-M"
Allowed:
  คาบเวลา · คาบของสัญญาณ · คาบ (period) · คาบ + a number with a time unit (มีคาบ 20 ms) ·
  คาบเกี่ยว · anything in fenced code, inline code, <pre>/<code>, URLs and link targets ·
  code files (clean_session is code) · the `source:` provenance block and path-valued YAML keys.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (REPO_ROOT, iter_files, mask_code, split_front_matter,  # noqa: E402
                     FIXTURES_REL)

_DIGITS = "0-9๐-๙"
_TIME_UNIT = r"(?:(?:ms|us|µs|μs|ns|s|sec)\b|วินาที|มิลลิวินาที|ไมโครวินาที|นาโนวินาที)"
_SPELLED = "หนึ่ง|สอง|สาม|สี่|ห้า|หก|เจ็ด|แปด|เก้า|สิบ"


@dataclass(frozen=True)
class Rule:
    id: str
    pattern: re.Pattern
    hint: str


RULES: tuple[Rule, ...] = (
    Rule("th-class-period", re.compile("คาบเรียน"),
         'ใช้ "บทเรียน" (lesson) หรือ "โมดูล" (module)'),
    Rule("th-period-number",
         re.compile(rf"คาบ[ \t]*(?:ที่[ \t]*)?(?:[{_DIGITS}]+(?:[.,][{_DIGITS}]+)?(?![{_DIGITS}.,])"
                    rf"(?![ \t]*{_TIME_UNIT})|ที่[ \t]*(?:{_SPELLED}))"),
         'ใช้ "บทเรียนที่ N" / "โมดูล N"; ถ้าหมายถึงคาบของสัญญาณ เขียน "คาบเวลา"'),
    Rule("th-period-deictic", re.compile(r"คาบ(?:นี้|หน้า|ก่อน|ถัดไป|ที่แล้ว|แรก|สุดท้าย)(?!ของ)"),
         'ใช้ "บทเรียนนี้" / "บทเรียนถัดไป" / "บทเรียนก่อนหน้า"'),
    Rule("th-period-each", re.compile(r"(?:ทุก|ต่อ)[ \t]?คาบ(?!เวลา|ของ|เกี่ยว|[ \t]*\([ \t]*period)"),
         'ใช้ "ทุกบทเรียน" / "ต่อบทเรียน"; ถ้าหมายถึงสัญญาณ เขียน "ทุกคาบเวลา" / "ต่อคาบเวลา"'),
    Rule("en-session-number", re.compile(r"\bsessions?[ \t]*[-–#]?[ \t]*[0-9]+", re.I),
         'use "lesson N" / "module N"'),
)

# URLs and link/image targets are addresses, not prose.
_URL = re.compile(r"(?:https?|ftp)://[^\s<>\"')\]]+|www\.[^\s<>\"')\]]+")
_LINK_TARGET = re.compile(r"\]\((?:<[^>\n]*>|[^)\s]*)(?:\s+\"[^\"\n]*\")?\)")
_HTML_ATTR = re.compile(r"\b(?:src|href|srcset)\s*=\s*(?:\"[^\"]*\"|'[^']*')", re.I)
_REF_DEF = re.compile(r"^( {0,3}\[[^\]]+\]:)\s*\S+.*$", re.M)

# YAML keys whose value is a path/address/provenance, not prose.
_YAML_SKIP_BLOCK = {"source"}
_YAML_SKIP_LINE = {"path", "evidence", "slides", "url", "repo", "ref", "site", "id", "prerequisites",
                   "short", "course", "modules", "paginate", "theme", "class", "marp", "size"}
_YAML_KEY = re.compile(r"^(\s*)(?:-\s+)?([A-Za-z_][\w-]*)\s*:(.*)$")


@dataclass(frozen=True)
class Finding:
    line: int
    col: int
    rule: str
    text: str
    hint: str


def _blank_span(s: str, start: int, end: int) -> str:
    return s[:start] + " " * (end - start) + s[end:]


def _mask_addresses(text: str) -> str:
    for rx in (_LINK_TARGET, _HTML_ATTR, _URL):
        text = rx.sub(lambda m: " " * len(m.group(0)) if "\n" not in m.group(0)
                      else re.sub(r"[^\n]", " ", m.group(0)), text)
    text = _REF_DEF.sub(lambda m: m.group(1) + " " * (len(m.group(0)) - len(m.group(1))), text)
    return text


def _mask_yaml(text: str) -> str:
    """Blank comments, provenance blocks and path-valued keys; keep prose values."""
    out = []
    skip_indent = None
    for line in text.split("\n"):
        stripped = line.lstrip(" ")
        indent = len(line) - len(stripped)
        if skip_indent is not None:
            if not stripped.strip() or indent > skip_indent:
                out.append(" " * len(line))
                continue
            skip_indent = None
        if stripped.startswith("#"):
            out.append(" " * len(line))
            continue
        m = _YAML_KEY.match(line)
        if m and m.group(2) in _YAML_SKIP_BLOCK:
            skip_indent = len(m.group(1))
            out.append(" " * len(line))
            continue
        if m and m.group(2) in _YAML_SKIP_LINE:
            out.append(" " * len(line))
            continue
        out.append(line)
    return _mask_addresses("\n".join(out))


def _scan_masked(masked: str, first_line: int = 1) -> list[Finding]:
    found = []
    for n, line in enumerate(masked.split("\n"), start=first_line):
        if "คาบ" not in line and "session" not in line.lower():
            continue
        for rule in RULES:
            for m in rule.pattern.finditer(line):
                found.append(Finding(n, m.start() + 1, rule.id, m.group(0).strip(), rule.hint))
    return found


def scan_text(text: str, kind: str = "md") -> list[Finding]:
    """Findings in a Markdown ('md') or YAML ('yaml') text. Line numbers are 1-based."""
    text = text.replace("\r\n", "\n")
    if text.startswith("\ufeff"):
        text = text[1:]
    if kind == "yaml":
        return _scan_masked(_mask_yaml(text))
    fm = split_front_matter(text)
    found: list[Finding] = []
    if fm.text is not None:
        found += _scan_masked(_mask_yaml(fm.text), fm.first_line)
        head_lines = fm.body_line - 1
        body = fm.body
    else:
        head_lines = 0
        body = text
    masked = _mask_addresses(mask_code(body))
    found += _scan_masked(masked, head_lines + 1)
    return sorted(found, key=lambda f: (f.line, f.col, f.rule))


def kind_of(path: str) -> str | None:
    p = path.lower()
    if p.endswith((".md", ".mdx", ".markdown")):
        return "md"
    if p.endswith((".yaml", ".yml")):
        return "yaml"
    return None


def scan_file(path: Path) -> list[Finding]:
    kind = kind_of(str(path))
    if kind is None:
        return []
    try:
        text = Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []
    return scan_text(text, kind)


def _targets(args: list[str], root: Path) -> list[Path]:
    if not args:
        return [root / r for r in iter_files(root, (FIXTURES_REL,)) if kind_of(r) == "md"]
    out: list[Path] = []
    for a in args:
        p = Path(a)
        if p.is_dir():
            out += [p / r for r in iter_files(p, ()) if kind_of(r)]
        elif p.is_file():
            out.append(p)
        else:
            print(f"check_terms: no such file or folder: {a}", file=sys.stderr)
            raise SystemExit(2)
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("paths", nargs="*", help="files or folders (default: every *.md/*.mdx in the repo)")
    ap.add_argument("--root", default=str(REPO_ROOT), help="repo root when no paths are given")
    ns = ap.parse_args(argv)
    total = 0
    for path in _targets(ns.paths, Path(ns.root)):
        for f in scan_file(path):
            total += 1
            shown = os.path.relpath(path) if os.path.isabs(path) else str(path)
            print(f"{shown}:{f.line}:{f.col}: [{f.rule}] \"{f.text}\" — {f.hint}")
    if total:
        print(f"\ncheck_terms: {total} finding(s). Learner-facing text says บทเรียน/โมดูล/หลักสูตร, "
              "not คาบ or session N.")
        return 1
    print("check_terms: clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
