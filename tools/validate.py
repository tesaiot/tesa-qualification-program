#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: Apache-2.0
"""Validate the TESA Open Knowledge repository: content model, links, words, credits, secrets.

    python3 tools/validate.py              # errors -> exit 1, warnings printed separately
    python3 tools/validate.py --strict     # warnings count as errors
    python3 tools/validate.py --list-checks

When GITHUB_ACTIONS is set, every finding is also printed as a workflow annotation
(::error file=...,line=...::message) so it shows on the pull request diff.

A check that crashes is reported under `internal` as an ERROR ("could not check"), never as a pass.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import traceback
import urllib.parse
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_terms  # noqa: E402
from _authorship import authorship_findings  # noqa: E402
from _common import (FIXTURES_REL, REPO_ROOT, SCHEMA_DIR, YamlDoc, is_text_file,  # noqa: E402
                     iter_files, load_policy, load_site_config, load_yaml, mask_code,
                     parse_yaml, read_text, split_front_matter)

try:
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import best_match
except ImportError:  # pragma: no cover - reported as an internal error at run time
    Draft202012Validator = None

CHECKS: dict[str, str] = {
    "yaml": "YAML parses; no duplicate keys",
    "schema": "files match schemas/*.schema.json",
    "skills": "skill map integrity; every skill id used exists, is not deprecated, level 1-5",
    "catalog": "catalog/courses.yaml <-> courses/<id>/ folders and course.yaml id/short/level",
    "structure": "required files; mNN-/lNN- folders <-> course.yaml modules; lesson ids",
    "cover": "course.yaml cover: the image exists, is .webp/.jpg/.png under 600 KB, and a third-party cover is credited",
    "prereq": "lesson and course prerequisites exist",
    "tracks": "catalog/tracks.yaml references existing courses and modules",
    "videos": "catalog/videos.yaml: known channels and playlists, existing lesson ids, no duplicate video",
    "roles": "skills/roles/*.yaml reference existing skills",
    "links": "relative Markdown/HTML links and images resolve to files",
    "alt": "images have non-empty alt text (warning)",
    "evidence": "assesses[].evidence files exist",
    "pairs": "practice/X <-> solution/X",
    "slides": "front matter `slides:` path exists",
    "quiz": "quiz objective index and answer indices are in range",
    "translation": "translation: done => README.en.md exists; EN front matter matches TH",
    "credits": "credits.yaml paths exist; third-party-looking images are credited",
    "terms": "no class-period wording (ERROR in courses/**, WARNING elsewhere)",
    "size": "no file over the size limit under courses/",
    "secrets": "no literal passwords/tokens/private keys under courses/",
    "leaks": "no internal paths or retired domain in published files",
    "authorship": "no AI assistant credited as author, co-author or generator in any file",
    "tesa-footer": "every courses/**/slides.md footer credits TESA",
    "tesa-cite": "every course README.md / README.en.md has the TESA citation block",
    "tesa-notice": "root NOTICE and ATTRIBUTION.md exist and name TESA",
    "time": "lesson time_min total: ERROR outside 10-240 min, WARNING above 75 unless a lab",
    "config": "site.config.yaml present and complete (warning)",
    "internal": "a check crashed: could not check (ERROR)",
}

MOD_DIR = re.compile(r"^m([0-9]{2})-[a-z0-9]+(?:-[a-z0-9]+)*$")
LESSON_DIR = re.compile(r"^l([0-9]{2})-[a-z0-9]+(?:-[a-z0-9]+)*$")
SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
MD_EXTS = (".md", ".mdx", ".markdown")

# Third-party image name markers used by the AIC course (tools/gen_credits.py THIRD_PARTY there).
THIRD_PARTY_MARKERS = ("commons", "wikimedia", "pmc", "nasa", "esa", "flickr", "noaa", "darpa", "nhtsa")

# Internal paths and the retired domain (BUILD_SPEC §1.4, §1.5).
# REUSE-IgnoreStart
LEAK_PATTERNS = (
    (re.compile(r"/mnt/tesaiot"), "internal volume path"),
    (re.compile(r"/home/wiroon\b"), "internal home path"),
    (re.compile(r"/tmp/[^/\s]+/-(?:mnt|home)-"), "internal scratch path"),
    (re.compile(r"TESAIoT_PLAN|Bento_Engine|IMPLEMENT_PLAN|TESA_Rules"), "internal plan folder"),
    (re.compile(r"\btesaiot\.com\b", re.I), "retired domain tesaiot.com (use tesaiot.dev)"),
)
# REUSE-IgnoreEnd

# Secrets — the Python rule is the AIoT course's check_credentials.py rule, unchanged.
SECRET_PY = re.compile(r"^\s*[A-Z_]*(PASS|PASSWORD|SECRET|TOKEN|API_KEY)[A-Z_]*\s*=\s*['\"]([^'\"]*)['\"]")
SECRET_C = re.compile(r"^\s*(?:#\s*define\s+|(?:static\s+)?(?:const\s+)?(?:char|auto|String|std::string)"
                      r"\s*\*?\s*(?:const\s+)?)[A-Za-z_]*(?:PASS|PASSWORD|SECRET|TOKEN|API_KEY|pass|password|"
                      r"secret|token|api_key)[A-Za-z_]*\s*(?:\[\s*\])?\s*=?\s*\"([^\"]*)\"")
SECRET_ANY = (
    (re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |ENCRYPTED )?PRIVATE KEY-----"), "private key"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b"), "GitHub token"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS access key id"),
)
C_EXTS = (".c", ".h", ".cpp", ".hpp", ".cc", ".ino")
PLACEHOLDER = re.compile(r"^(?:<.*>|\$\{.*\}|x+|X+|\*+|\.\.\.|YOUR_[A-Z_]+|your[-_ ].*)$")
ALLOW_FILE = Path(__file__).resolve().parent / "credentials_allow.txt"

MARP_ALT_TOKEN = re.compile(
    r"^(?:bg|left|right|contain|cover|fit|auto|vertical|\d+(?:\.\d+)?%|"
    r"(?:w|h|width|height|left|right|x|y|blur|brightness|contrast|drop-shadow|grayscale|hue-rotate|"
    r"invert|opacity|saturate|sepia)(?::\S+)?)$", re.I)


# =========================================================================== reporting
@dataclass(order=True, frozen=True)
class Finding:
    path: str
    line: int
    check: str
    message: str


class Reporter:
    def __init__(self, strict: bool = False):
        self.strict = strict
        self.errors: list[Finding] = []
        self.warnings: list[Finding] = []

        self._seen: set[tuple] = set()

    def _add(self, bucket: list, sev: str, check: str, path: str, line: int, msg: str) -> None:
        assert check in CHECKS, check
        f = Finding(path or ".", int(line or 0), check, msg)
        if (sev, f) not in self._seen:
            self._seen.add((sev, f))
            bucket.append(f)

    def error(self, check: str, path: str, line: int, msg: str) -> None:
        self._add(self.errors, "e", check, path, line, msg)

    def warn(self, check: str, path: str, line: int, msg: str) -> None:
        self._add(self.warnings, "w", check, path, line, msg)

    def by_check(self) -> dict[str, tuple[int, int]]:
        e = Counter(f.check for f in self.errors)
        w = Counter(f.check for f in self.warnings)
        return {c: (e.get(c, 0), w.get(c, 0)) for c in CHECKS}

    @property
    def failed(self) -> bool:
        return bool(self.errors) or (self.strict and bool(self.warnings))


def _gha_escape(s: str, prop: bool = False) -> str:
    s = s.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
    if prop:
        s = s.replace(":", "%3A").replace(",", "%2C")
    return s


def print_report(rep: Reporter, gha: bool, max_warn: int, max_annot_warn: int = 50,
                 out=sys.stdout) -> None:
    errors = sorted(set(rep.errors))
    warnings = sorted(set(rep.warnings))
    wsev = "error" if rep.strict else "warning"
    print(f"== ERRORS ({len(errors)}) ==", file=out)
    for f in errors:
        loc = f"{f.path}:{f.line}" if f.line else f.path
        print(f"  [{f.check}] {loc}: {f.message}", file=out)
    print(f"\n== WARNINGS ({len(warnings)}){' — --strict: counted as errors' if rep.strict else ''} ==",
          file=out)
    shown = Counter()
    hidden = Counter()
    for f in warnings:
        if max_warn and shown[f.check] >= max_warn:
            hidden[f.check] += 1
            continue
        shown[f.check] += 1
        loc = f"{f.path}:{f.line}" if f.line else f.path
        print(f"  [{f.check}] {loc}: {f.message}", file=out)
    for c, n in sorted(hidden.items()):
        print(f"  [{c}] ... and {n} more (use --all-warnings)", file=out)
    if gha:
        for f in errors:
            props = f"file={_gha_escape(f.path, True)}" + (f",line={f.line}" if f.line else "")
            print(f"::error {props},title={_gha_escape(f.check, True)}::{_gha_escape(f.message)}", file=out)
        for i, f in enumerate(warnings):
            if i >= max_annot_warn and not rep.strict:
                print(f"::notice title=validate::{len(warnings) - i} more warnings in the log", file=out)
                break
            props = f"file={_gha_escape(f.path, True)}" + (f",line={f.line}" if f.line else "")
            print(f"::{wsev} {props},title={_gha_escape(f.check, True)}::{_gha_escape(f.message)}",
                  file=out)
    print("\n== SUMMARY ==", file=out)
    print(f"  {'check':<13} {'errors':>6} {'warnings':>8}", file=out)
    for c, (e, w) in rep.by_check().items():
        if e or w:
            print(f"  {c:<13} {e:>6} {w:>8}", file=out)
    status = "FAIL" if rep.failed else "OK"
    print(f"\nvalidate: {status} — {len(errors)} error(s), {len(warnings)} warning(s)", file=out)


# =========================================================================== context
@dataclass
class Lesson:
    id: str
    course: str
    module: str
    dir: Path
    rel: str
    fm: dict
    readme_rel: str
    doc: YamlDoc


@dataclass
class Ctx:
    root: Path
    rep: Reporter
    policy: dict
    files: list[str] = field(default_factory=list)
    site: Any = None
    skills: dict[str, dict] = field(default_factory=dict)
    level_ids: set[int] = field(default_factory=lambda: {1, 2, 3, 4, 5})
    catalog: dict[str, dict] = field(default_factory=dict)
    courses: dict[str, dict] = field(default_factory=dict)          # id -> course.yaml data
    modules: dict[str, list[str]] = field(default_factory=dict)     # course id -> module ids
    lessons: dict[str, Lesson] = field(default_factory=dict)
    lesson_prereqs: list[tuple[str, str, int, str]] = field(default_factory=list)
    validators: dict[str, Any] = field(default_factory=dict)

    def rel(self, p: Path) -> str:
        try:
            return p.relative_to(self.root).as_posix()
        except ValueError:
            return p.as_posix()


def _validator(ctx: Ctx, name: str):
    if name not in ctx.validators:
        schema = json.loads((SCHEMA_DIR / f"{name}.schema.json").read_text(encoding="utf-8"))
        ctx.validators[name] = Draft202012Validator(schema)
    return ctx.validators[name]


def schema_check(ctx: Ctx, doc: YamlDoc, name: str, relpath: str) -> bool:
    """Report schema errors; True when the data is valid."""
    errs = sorted(_validator(ctx, name).iter_errors(doc.data), key=lambda e: list(map(str, e.absolute_path)))
    for e in errs:
        if e.context:
            e = best_match(e.context) or e
        path = "/".join(str(p) for p in e.absolute_path) or "(top)"
        ctx.rep.error("schema", relpath, doc.line_of(e.absolute_path),
                      f"{path}: {e.message} [{name}.schema.json]")
    return not errs


def load_checked(ctx: Ctx, path: Path, schema: str | None) -> YamlDoc | None:
    """Load a YAML file, report parse/schema errors. Returns the doc (data may be invalid)."""
    relpath = ctx.rel(path)
    doc = load_yaml(path)
    if doc.error:
        ctx.rep.error("yaml", relpath, doc.error_line, doc.error)
        return None
    if schema:
        schema_check(ctx, doc, schema, relpath)
    return doc


def _skill_ref(ctx: Ctx, skill: Any, level: Any, relpath: str, line: int, what: str) -> None:
    if not isinstance(skill, str):
        return
    s = ctx.skills.get(skill)
    if s is None:
        if ctx.skills:
            ctx.rep.error("skills", relpath, line, f"{what}: unknown skill id {skill!r} "
                          "(ids live in skills/skills.yaml; ask the lead, never invent one)")
    elif s.get("deprecated"):
        repl = s.get("replaced_by")
        ctx.rep.error("skills", relpath, line, f"{what}: skill {skill!r} is deprecated"
                      + (f"; use {repl!r}" if repl else ""))
    if level is not None and (not isinstance(level, int) or isinstance(level, bool) or level not in ctx.level_ids):
        ctx.rep.error("skills", relpath, line, f"{what}: level {level!r} for {skill!r} is not one of "
                      f"{sorted(ctx.level_ids)}")


# =========================================================================== skills
def check_skills(ctx: Ctx) -> None:
    path = ctx.root / "skills" / "skills.yaml"
    if not path.is_file():
        ctx.rep.error("skills", "skills/skills.yaml", 0, "missing: the skill map is the source of truth")
        return
    doc = load_checked(ctx, path, "skills")
    if doc is None or not isinstance(doc.data, dict):
        return
    d = doc.data
    rp = "skills/skills.yaml"
    levels = d.get("levels") or []
    ids = [lv.get("id") for lv in levels if isinstance(lv, dict)]
    if ids:
        ctx.level_ids = {i for i in ids if isinstance(i, int)}
        if sorted(ctx.level_ids) != list(range(1, len(ctx.level_ids) + 1)):
            ctx.rep.error("skills", rp, doc.line_of(("levels",)), f"level ids must be 1..N, got {ids}")
        for i, lv in enumerate(levels):
            if isinstance(lv, dict) and lv.get("code") != f"L{lv.get('id')}":
                ctx.rep.error("skills", rp, doc.line_of(("levels", i)), f"level code {lv.get('code')!r} "
                              f"does not match id {lv.get('id')!r}")

    def unique(key):
        seen = {}
        for i, it in enumerate(d.get(key) or []):
            if not isinstance(it, dict):
                continue
            iid = it.get("id")
            if iid in seen:
                ctx.rep.error("skills", rp, doc.line_of((key, i)), f"duplicate {key[:-1]} id {iid!r}")
            seen[iid] = it
        return seen

    areas = unique("areas")
    groups = unique("groups")
    skills = unique("skills")
    importance = d.get("importance") or {}
    for i, g in enumerate(d.get("groups") or []):
        if isinstance(g, dict) and g.get("area") not in areas:
            ctx.rep.error("skills", rp, doc.line_of(("groups", i)), f"group {g.get('id')!r}: unknown area "
                          f"{g.get('area')!r}")
    for i, s in enumerate(d.get("skills") or []):
        if not isinstance(s, dict):
            continue
        sid, grp = s.get("id"), s.get("group")
        line = doc.line_of(("skills", i))
        if grp not in groups:
            ctx.rep.error("skills", rp, line, f"skill {sid!r}: unknown group {grp!r}")
        if isinstance(sid, str) and sid.split(".", 1)[0] != grp:
            ctx.rep.error("skills", rp, line, f"skill {sid!r}: id prefix must equal its group {grp!r}")
        imp = s.get("importance")
        if imp is not None and imp not in importance:
            ctx.rep.error("skills", rp, line, f"skill {sid!r}: importance {imp!r} is not one of "
                          f"{sorted(importance)} or null")
        if s.get("deprecated") and not s.get("replaced_by"):
            ctx.rep.warn("skills", rp, line, f"skill {sid!r} is deprecated without replaced_by")
        rb = s.get("replaced_by")
        if rb is not None and (rb not in skills or rb == sid):
            ctx.rep.error("skills", rp, line, f"skill {sid!r}: replaced_by {rb!r} is not another skill id")
        for req in s.get("requires") or []:
            if req not in skills:
                ctx.rep.error("skills", rp, line, f"skill {sid!r}: requires unknown skill {req!r}")
    ctx.skills = {k: v for k, v in skills.items() if isinstance(k, str)}


# =========================================================================== catalog + courses
def check_catalog(ctx: Ctx) -> None:
    path = ctx.root / "catalog" / "courses.yaml"
    rp = "catalog/courses.yaml"
    if not path.is_file():
        ctx.rep.error("catalog", rp, 0, "missing")
        return
    doc = load_checked(ctx, path, "catalog")
    if doc is None or not isinstance(doc.data, dict):
        return
    shorts: dict[str, str] = {}
    for i, c in enumerate(doc.data.get("courses") or []):
        if not isinstance(c, dict):
            continue
        cid, short = c.get("id"), c.get("short")
        line = doc.line_of(("courses", i))
        if cid in ctx.catalog:
            ctx.rep.error("catalog", rp, line, f"duplicate course id {cid!r}")
        if short in shorts:
            ctx.rep.error("catalog", rp, line, f"short {short!r} used by {shorts[short]!r} and {cid!r}")
        shorts[short] = cid
        ctx.catalog[cid] = dict(c, _line=line)
        folder = ctx.root / "courses" / str(cid)
        if c.get("in_tree") is True:
            if not folder.is_dir():
                ctx.rep.error("catalog", rp, line, f"in_tree course {cid!r} has no folder courses/{cid}/")
            elif not (folder / "course.yaml").is_file():
                ctx.rep.error("catalog", f"courses/{cid}", 0, f"in_tree course {cid!r} has no course.yaml")
        elif folder.exists():
            ctx.rep.warn("catalog", f"courses/{cid}", 0, f"course {cid!r} is in_tree: false but has a folder")
    cdir = ctx.root / "courses"
    if cdir.is_dir():
        for d in sorted(cdir.iterdir()):
            if d.is_dir() and not d.name.startswith(".") and d.name not in ctx.catalog:
                ctx.rep.error("catalog", f"courses/{d.name}", 0,
                              f"folder courses/{d.name}/ is not registered in catalog/courses.yaml")


def check_course(ctx: Ctx, cid: str) -> None:
    entry = ctx.catalog[cid]
    cdir = ctx.root / "courses" / cid
    crel = f"courses/{cid}"
    if not cdir.is_dir():
        return
    for req in ("course.yaml", "README.md", "README.en.md", "credits.yaml"):
        if not (cdir / req).is_file():
            ctx.rep.error("structure", f"{crel}/{req}", 0, "required course file is missing (BUILD_SPEC §3)")
    course: dict = {}
    doc = load_checked(ctx, cdir / "course.yaml", "course") if (cdir / "course.yaml").is_file() else None
    if doc is not None and isinstance(doc.data, dict):
        course = doc.data
        rp = f"{crel}/course.yaml"
        if course.get("id") != cid:
            ctx.rep.error("catalog", rp, doc.line_of(("id",)), f"id {course.get('id')!r} must equal the "
                          f"folder name and catalog id {cid!r}")
        for key in ("short", "level"):
            if key in course and course.get(key) != entry.get(key):
                ctx.rep.error("catalog", rp, doc.line_of((key,)), f"{key} {course.get(key)!r} does not "
                              f"match catalog/courses.yaml ({entry.get(key)!r})")
        if "status" in course and course.get("status") != entry.get("status"):
            ctx.rep.warn("catalog", rp, doc.line_of(("status",)), f"status {course.get('status')!r} differs "
                         f"from catalog/courses.yaml ({entry.get('status')!r})")
        pre = course.get("prerequisites") or {}
        if isinstance(pre, dict):
            for i, pc in enumerate(pre.get("courses") or []):
                if pc not in ctx.catalog:
                    ctx.rep.error("prereq", rp, doc.line_of(("prerequisites", "courses", i)),
                                  f"prerequisite course {pc!r} is not in the catalog")
            for i, ps in enumerate(pre.get("skills") or []):
                if isinstance(ps, dict):
                    _skill_ref(ctx, ps.get("skill"), ps.get("level"), rp,
                               doc.line_of(("prerequisites", "skills", i)), "prerequisites.skills")
        cov = course.get("cover")
        if isinstance(cov, dict) and isinstance(cov.get("image"), str):
            check_cover(ctx, cid, cdir, rp, doc.line_of(("cover", "image")), cov)
    ctx.courses[cid] = course
    # The catalog (lead-owned) is the source of truth for the lesson-id prefix; a course.yaml that
    # disagrees is reported once above instead of once per lesson.
    short = entry.get("short") or course.get("short")

    # ---- modules <-> folders
    listed: dict[str, int] = {}
    for i, m in enumerate(course.get("modules") or []):
        if isinstance(m, dict) and isinstance(m.get("id"), str):
            mid = m["id"]
            line = doc.line_of(("modules", i)) if doc else 0
            if mid in listed:
                ctx.rep.error("structure", f"{crel}/course.yaml", line, f"module {mid!r} listed twice")
            listed[mid] = line
            if not (cdir / mid).is_dir():
                ctx.rep.error("structure", f"{crel}/course.yaml", line,
                              f"module {mid!r} has no folder {crel}/{mid}/")
    if course:   # unknown when course.yaml is missing/unreadable: other checks must not guess
        ctx.modules[cid] = list(listed)
    numbers: dict[str, str] = {}
    for d in sorted(p for p in cdir.iterdir() if p.is_dir()):
        m = MOD_DIR.match(d.name)
        if not m:
            if re.match(r"^m[0-9]", d.name):
                ctx.rep.error("structure", f"{crel}/{d.name}", 0, "module folder must be mNN-<slug> "
                              "(lowercase ascii, hyphens)")
            continue
        if m.group(1) in numbers:
            ctx.rep.error("structure", f"{crel}/{d.name}", 0, f"module number m{m.group(1)} is also used by "
                          f"{numbers[m.group(1)]}")
        numbers[m.group(1)] = d.name
        if doc is not None and d.name not in listed:
            ctx.rep.error("structure", f"{crel}/{d.name}", 0, "module folder is not listed in course.yaml "
                          "modules")
        if not (d / "README.md").is_file():
            ctx.rep.error("structure", f"{crel}/{d.name}/README.md", 0, "module README.md is missing")
        for ld in sorted(p for p in d.iterdir() if p.is_dir()):
            lm = LESSON_DIR.match(ld.name)
            if not lm:
                if re.match(r"^l[0-9]", ld.name):
                    ctx.rep.error("structure", ctx.rel(ld), 0, "lesson folder must be lNN-<slug>")
                continue
            check_lesson(ctx, cid, short, d.name, m.group(1), lm.group(1), ld, course)

    check_credits(ctx, cid, cdir)
    check_cite(ctx, cid, cdir, course)


def check_lesson(ctx: Ctx, cid: str, short: str | None, mod: str, mnum: str, lnum: str, ldir: Path,
                 course: dict) -> None:
    lrel = ctx.rel(ldir)
    readme = ldir / "README.md"
    rp = f"{lrel}/README.md"
    if not readme.is_file():
        ctx.rep.error("structure", rp, 0, "lesson README.md is missing")
        return
    text = read_text(readme)
    if text is None:
        ctx.rep.error("structure", rp, 0, "not UTF-8 text")
        return
    fm = split_front_matter(text)
    if fm.text is None:
        ctx.rep.error("structure", rp, 1, "lesson README.md has no front matter (--- YAML --- at the top)")
        return
    doc = parse_yaml(fm.text, fm.first_line - 1)
    if doc.error:
        ctx.rep.error("yaml", rp, doc.error_line, doc.error)
        return
    if not isinstance(doc.data, dict):
        ctx.rep.error("schema", rp, 1, "front matter is not a mapping")
        return
    schema_check(ctx, doc, "lesson", rp)
    d = doc.data
    lid = d.get("id")
    expected = f"{short}.m{mnum}.l{lnum}" if short else None
    if expected and lid != expected:
        ctx.rep.error("structure", rp, doc.line_of(("id",)), f"id {lid!r} must be {expected!r} "
                      f"(<short>.mNN.lNN from the folder numbers)")
    if isinstance(lid, str):
        if lid in ctx.lessons:
            ctx.rep.error("structure", rp, doc.line_of(("id",)), f"lesson id {lid!r} is also used by "
                          f"{ctx.lessons[lid].readme_rel}")
        else:
            ctx.lessons[lid] = Lesson(lid, cid, mod, ldir, lrel, d, rp, doc)
    if d.get("lang") != "th":
        ctx.rep.error("translation", rp, doc.line_of(("lang",)), "README.md is the Thai page: lang must be th")
    for i, dev in enumerate(d.get("develops") or []):
        if isinstance(dev, dict):
            _skill_ref(ctx, dev.get("skill"), dev.get("to"), rp, doc.line_of(("develops", i)), "develops")
    for i, a in enumerate(d.get("assesses") or []):
        if isinstance(a, dict):
            _skill_ref(ctx, a.get("skill"), a.get("level"), rp, doc.line_of(("assesses", i)), "assesses")
            ev = a.get("evidence")
            if isinstance(ev, str):
                # A single path-like token is a file reference that must exist; free text
                # ("Deliverables: model.blend + checklist.md") describes learner output instead.
                target = ev.split("#", 1)[0].strip()
                if target and not re.search(r"\s", target) and (
                        "/" in target or re.search(r"\.[A-Za-z0-9]{1,5}$", target)):
                    if SCHEME.match(target) or target.startswith("/"):
                        ctx.rep.error("evidence", rp, doc.line_of(("assesses", i, "evidence")),
                                      f"evidence {ev!r} must be a path relative to the lesson")
                    elif not (ldir / target).exists():
                        ctx.rep.error("evidence", rp, doc.line_of(("assesses", i, "evidence")),
                                      f"evidence file {target!r} does not exist in {lrel}/")
    for i, p in enumerate(d.get("prerequisites") or []):
        if isinstance(p, str):
            ctx.lesson_prereqs.append((p, rp, doc.line_of(("prerequisites", i)), lid or "?"))
    tm = d.get("time_min")
    if isinstance(tm, dict) and tm and all(isinstance(v, int) and not isinstance(v, bool) for v in tm.values()):
        lim = (ctx.policy.get("limits") or {}).get("lesson_minutes") or {}
        lo, soft, hi = lim.get("min", 10), lim.get("soft_max", 75), lim.get("max", 240)
        marker = lim.get("lab_marker", "lab")
        total = sum(tm.values())
        line = doc.line_of(("time_min",))
        if not lo <= total <= hi:
            ctx.rep.error("time", rp, line, f"time_min totals {total} min; a lesson is {lo}–{hi} min "
                          "(split it or merge it)")
        elif total > soft and marker not in ldir.name:
            ctx.rep.warn("time", rp, line, f"time_min totals {total} min; a lesson over {soft} min should "
                         f"be split (only a lab — folder name containing {marker!r} — may run to {hi})")
    # slides
    sl = d.get("slides")
    if isinstance(sl, str) and not (ldir / sl).is_file():
        ctx.rep.error("slides", rp, doc.line_of(("slides",)), f"slides file {sl!r} does not exist in {lrel}/")
    # translation
    en = ldir / "README.en.md"
    tr = d.get("translation")
    if tr == "done" and not en.is_file():
        ctx.rep.error("translation", rp, doc.line_of(("translation",)),
                      "translation: done but README.en.md does not exist")
    if en.is_file():
        check_lesson_en(ctx, en, d)
    # quiz
    quiz = ldir / "quiz.yaml"
    if quiz.is_file():
        check_quiz(ctx, quiz, d)


def check_lesson_en(ctx: Ctx, en: Path, th: dict) -> None:
    rp = ctx.rel(en)
    text = read_text(en) or ""
    fm = split_front_matter(text)
    if fm.text is None:
        ctx.rep.error("translation", rp, 1, "README.en.md must repeat the front matter with lang: en")
        return
    doc = parse_yaml(fm.text, fm.first_line - 1)
    if doc.error:
        ctx.rep.error("yaml", rp, doc.error_line, doc.error)
        return
    if not isinstance(doc.data, dict):
        ctx.rep.error("schema", rp, 1, "front matter is not a mapping")
        return
    schema_check(ctx, doc, "lesson", rp)
    d = doc.data
    if d.get("lang") != "en":
        ctx.rep.error("translation", rp, doc.line_of(("lang",)), "README.en.md front matter needs lang: en")
    if d.get("id") != th.get("id"):
        ctx.rep.error("translation", rp, doc.line_of(("id",)), f"id {d.get('id')!r} differs from the Thai "
                      f"README.md ({th.get('id')!r})")
    for key in ("develops", "assesses", "prerequisites", "level", "slides"):
        if d.get(key) != th.get(key):
            ctx.rep.warn("translation", rp, doc.line_of((key,)), f"{key} differs from the Thai README.md "
                         "front matter (the EN file repeats it)")


def check_quiz(ctx: Ctx, quiz: Path, fm: dict) -> None:
    rp = ctx.rel(quiz)
    doc = load_checked(ctx, quiz, "quiz")
    if doc is None or not isinstance(doc.data, dict):
        return
    n_obj = len(fm.get("objectives") or [])
    seen = set()
    for i, it in enumerate(doc.data.get("items") or []):
        if not isinstance(it, dict):
            continue
        line = doc.line_of(("items", i))
        qid = it.get("id")
        if qid in seen:
            ctx.rep.error("quiz", rp, line, f"duplicate item id {qid!r}")
        seen.add(qid)
        obj = it.get("objective")
        if isinstance(obj, int) and not 1 <= obj <= n_obj:
            ctx.rep.error("quiz", rp, doc.line_of(("items", i, "objective")),
                          f"item {qid!r}: objective {obj} is out of range — the lesson has {n_obj} objective(s)")
        typ = it.get("type")
        choices = it.get("choices") or []
        ans = it.get("answer") or []
        if typ in ("single", "multi", "order"):
            nums = [a for a in ans if isinstance(a, int) and not isinstance(a, bool)]
            aline = doc.line_of(("items", i, "answer"))
            if len(nums) != len(ans):
                ctx.rep.error("quiz", rp, aline, f"item {qid!r}: answers of a {typ} item are choice indices")
            bad = [a for a in nums if not 0 <= a < len(choices)]
            if bad:
                ctx.rep.error("quiz", rp, aline, f"item {qid!r}: answer index {bad} out of range "
                              f"(0..{len(choices) - 1})")
            if typ == "single" and len(ans) != 1:
                ctx.rep.error("quiz", rp, aline, f"item {qid!r}: a single item has exactly one answer")
            if typ == "multi" and len(set(nums)) != len(nums):
                ctx.rep.error("quiz", rp, aline, f"item {qid!r}: repeated answer index")
            if typ == "order" and sorted(nums) != list(range(len(choices))):
                ctx.rep.error("quiz", rp, aline, f"item {qid!r}: an order answer lists every choice index "
                              "exactly once")


def check_prereqs(ctx: Ctx) -> None:
    for pid, rp, line, lid in ctx.lesson_prereqs:
        if pid not in ctx.lessons:
            ctx.rep.error("prereq", rp, line, f"prerequisite lesson {pid!r} does not exist")
        elif pid == lid:
            ctx.rep.error("prereq", rp, line, "a lesson cannot be its own prerequisite")


COVER_MAX_KB = 600


def check_cover(ctx: Ctx, cid: str, cdir: Path, rp: str, line: int, cov: dict) -> None:
    img = cdir / cov["image"]
    if not img.is_file():
        ctx.rep.error("cover", rp, line, f"cover image {cov['image']!r} does not exist in courses/{cid}/")
        return
    kb = img.stat().st_size // 1024
    if kb > COVER_MAX_KB:
        ctx.rep.error("cover", rp, line, f"cover image is {kb} KB; keep it under {COVER_MAX_KB} KB (a 1280x720 WebP is enough)")
    if cov.get("own") is not True:
        credits = cdir / "credits.yaml"
        listed = set()
        if credits.is_file():
            data = load_yaml(credits).data   # a broken credits.yaml is reported by the credits check
            if isinstance(data, dict):
                listed = {im.get("path") for im in data.get("images") or [] if isinstance(im, dict)}
        if cov["image"] not in listed:
            ctx.rep.error("cover", rp, line, f"cover image {cov['image']!r} is not in courses/{cid}/credits.yaml "
                          "(or set own: true for TESA's own image)")


def check_credits(ctx: Ctx, cid: str, cdir: Path) -> None:
    path = cdir / "credits.yaml"
    credited: set[str] = set()
    if path.is_file():
        doc = load_checked(ctx, path, "credits")
        if doc is not None and isinstance(doc.data, dict):
            rp = ctx.rel(path)
            spdx = _spdx_ids()
            for i, im in enumerate(doc.data.get("images") or []):
                if not isinstance(im, dict) or not isinstance(im.get("path"), str):
                    continue
                p = im["path"]
                line = doc.line_of(("images", i))
                if p in credited:
                    ctx.rep.warn("credits", rp, line, f"{p!r} is listed twice")
                credited.add(p)
                if not (cdir / p).is_file():
                    ctx.rep.error("credits", rp, line, f"credited file {p!r} does not exist in courses/{cid}/")
                src = im.get("source")
                if isinstance(src, str) and src.count("(") != src.count(")"):
                    # A URL cut at "(" or ")" when it was copied from a Markdown link: the credit then points nowhere.
                    ctx.rep.error("credits", rp, doc.line_of(("images", i, "source")),
                                  f"source URL looks cut off (unbalanced parentheses): {src!r}")
                lic = im.get("license")
                if spdx and isinstance(lic, str) and lic not in ("own", "Infineon-permission"):
                    for tok in re.split(r"\s+(?:AND|OR|WITH)\s+", lic):
                        if tok not in spdx and not tok.startswith("LicenseRef-"):
                            ctx.rep.warn("credits", rp, doc.line_of(("images", i, "license")),
                                         f"licence {tok!r} is not an SPDX id (see https://spdx.org/licenses/)")
    # Third-party-looking images that nobody credited.
    prefix = f"courses/{cid}/"
    for f in ctx.files:
        if not f.startswith(prefix) or not re.search(r"\.(png|jpe?g|gif|svg|webp)$", f, re.I):
            continue
        name = PurePosixPath(f).name.lower()
        if any(m in re.split(r"[_\-.]", name) for m in THIRD_PARTY_MARKERS) and f[len(prefix):] not in credited:
            ctx.rep.warn("credits", f, 0, "looks like a third-party image (name marker) but is not in "
                         f"courses/{cid}/credits.yaml")


_SPDX_CACHE: set[str] | None = None


def _spdx_ids() -> set[str]:
    global _SPDX_CACHE
    if _SPDX_CACHE is None:
        try:
            from reuse._licenses import ALL_MAP  # type: ignore
            _SPDX_CACHE = set(ALL_MAP)
        except Exception:  # reuse not installed: skip the SPDX-id warning, the schema still runs
            _SPDX_CACHE = set()
    return _SPDX_CACHE


def _section_after(text: str, heading_rx: re.Pattern) -> tuple[str, int] | None:
    """(section text, heading line) for the first Markdown heading matching heading_rx.

    Headings are looked up in code-masked text (a heading inside a code block does not count);
    the section is returned unmasked, because the attribution is often given in a code block
    for copying.
    """
    lines = text.split("\n")
    masked = mask_code(text).split("\n")
    for i, line in enumerate(masked):
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m and heading_rx.search(m.group(2)):
            level = len(m.group(1))
            out = []
            for j in range(i + 1, len(lines)):
                h = re.match(r"^(#{1,6})\s", masked[j])
                if h and len(h.group(1)) <= level:
                    break
                out.append(lines[j])
            return "\n".join(out), i + 1
    return None


def _template_fragments(template: str) -> list[str]:
    """The fixed wording of an attribution template (the text around {title} and {repo})."""
    edges = " \"'“”,"   # quotes around {title} and commas around {repo} belong to the slots
    return [f.strip(edges) for f in re.split(r"\{title\}|\{repo\}", template) if len(f.strip(edges)) >= 3]


def _squash(s: str) -> str:
    """Compare wording, not layout: drop blockquote markers, emphasis and all whitespace (Thai text
    has no spaces between words, so a line break may fall anywhere)."""
    s = re.sub(r"(?m)^\s*>\s?", "", s)
    return re.sub(r"[\s*_]+", "", s)


def check_cite(ctx: Ctx, cid: str, cdir: Path, course: dict) -> None:
    heads = (ctx.policy.get("attribution") or {}).get("cite_heading") or {}
    repo = ctx.site.repo_url
    title = course.get("title") or ctx.catalog.get(cid, {}).get("title") or {}
    for fname, lang in (("README.md", "th"), ("README.en.md", "en")):
        p = cdir / fname
        if not p.is_file():
            continue  # reported by structure
        rp = ctx.rel(p)
        text = (read_text(p) or "").replace("\r\n", "\n")
        heading = heads.get(lang)
        found = _section_after(text, re.compile(re.escape(heading), re.I)) if heading else None
        if found is None:
            ctx.rep.error("tesa-cite", rp, 0, f"missing the \"{heading}\" section (BUILD_SPEC §1.9: every "
                          "course README ends with the required TESA attribution)")
            continue
        sec, hline = found
        if repo not in sec:
            ctx.rep.error("tesa-cite", rp, hline, f"the \"{heading}\" section must contain {repo}")
        t = title.get(lang) if isinstance(title, dict) else None
        if t and _loose(t) not in _loose(sec):
            ctx.rep.warn("tesa-cite", rp, hline, f"the \"{heading}\" section does not quote the course "
                         f"title \"{t}\"")
        template = ctx.site.attribution.get(lang)
        if template:
            missing = [f for f in _template_fragments(template) if _squash(f) not in _squash(sec)]
            if missing:
                ctx.rep.warn("tesa-cite", rp, hline, "the attribution does not follow site.config.yaml "
                             f"credit.attribution.{lang}; missing: " + " | ".join(m.strip() for m in missing))


# =========================================================================== videos
def check_videos(ctx: Ctx) -> None:
    """catalog/videos.yaml is optional; when present every reference in it must resolve."""
    path = ctx.root / "catalog" / "videos.yaml"
    rp = "catalog/videos.yaml"
    if not path.is_file():
        return
    doc = load_checked(ctx, path, "videos")
    if doc is None or not isinstance(doc.data, dict):
        return
    channels = doc.data.get("channels") if isinstance(doc.data.get("channels"), dict) else {}
    playlists = {p.get("id") for p in doc.data.get("playlists") or [] if isinstance(p, dict)}
    for i, pl in enumerate(doc.data.get("playlists") or []):
        if isinstance(pl, dict) and pl.get("channel") not in channels:
            ctx.rep.error("videos", rp, doc.line_of(("playlists", i)), f"playlist {pl.get('id')!r}: unknown channel "
                          f"{pl.get('channel')!r}")
    seen: dict[str, int] = {}
    for i, v in enumerate(doc.data.get("videos") or []):
        if not isinstance(v, dict):
            continue
        line = doc.line_of(("videos", i))
        vid = v.get("id")
        if vid in seen:
            ctx.rep.error("videos", rp, line, f"video {vid!r} is listed twice (first on line {seen[vid]})")
        seen.setdefault(vid, line)
        if v.get("channel") not in channels:
            ctx.rep.error("videos", rp, line, f"video {vid!r}: unknown channel {v.get('channel')!r}")
        if v.get("playlist") is not None and v.get("playlist") not in playlists:
            ctx.rep.error("videos", rp, line, f"video {vid!r}: unknown playlist {v.get('playlist')!r}")
        for j, lid in enumerate(v.get("lessons") or []):
            if lid not in ctx.lessons:
                ctx.rep.error("videos", rp, doc.line_of(("videos", i, "lessons", j)) or line,
                              f"video {vid!r}: lesson {lid!r} does not exist")


# =========================================================================== tracks, roles
def check_tracks(ctx: Ctx) -> None:
    path = ctx.root / "catalog" / "tracks.yaml"
    rp = "catalog/tracks.yaml"
    if not path.is_file():
        ctx.rep.warn("tracks", rp, 0, "missing (BUILD_SPEC §2 lists 5 pathways here)")
        return
    doc = load_checked(ctx, path, "tracks")
    if doc is None or not isinstance(doc.data, dict):
        return
    seen = set()
    for i, t in enumerate(doc.data.get("tracks") or []):
        if not isinstance(t, dict):
            continue
        if t.get("id") in seen:
            ctx.rep.error("tracks", rp, doc.line_of(("tracks", i)), f"duplicate track id {t.get('id')!r}")
        seen.add(t.get("id"))
        for j, st in enumerate(t.get("steps") or []):
            if not isinstance(st, dict):
                continue
            c = st.get("course")
            line = doc.line_of(("tracks", i, "steps", j))
            if c not in ctx.catalog:
                ctx.rep.error("tracks", rp, line, f"track {t.get('id')!r}: course {c!r} is not in the catalog")
                continue
            mods = st.get("modules")
            if not mods:
                continue
            if not ctx.catalog[c].get("in_tree"):
                ctx.rep.error("tracks", rp, line, f"track {t.get('id')!r}: course {c!r} is external; "
                              "modules cannot be checked")
                continue
            known = ctx.modules.get(c)
            if known is None:
                continue  # course.yaml missing: reported by catalog/structure
            for m in mods:
                ok = (m in known if isinstance(m, str) and len(m) > 3 else
                      any(k.startswith(f"{m}-") for k in known) if isinstance(m, str) else
                      isinstance(m, int) and 1 <= m <= len(known))
                if not ok:
                    ctx.rep.error("tracks", rp, line, f"track {t.get('id')!r}: course {c!r} has no module {m!r}")


def check_roles(ctx: Ctx) -> None:
    rdir = ctx.root / "skills" / "roles"
    if not rdir.is_dir():
        return
    for p in sorted(rdir.glob("*.y*ml")):
        doc = load_checked(ctx, p, "roles")
        if doc is None or not isinstance(doc.data, dict):
            continue
        rp = ctx.rel(p)
        if doc.data.get("id") != p.stem:
            ctx.rep.warn("roles", rp, doc.line_of(("id",)), f"id {doc.data.get('id')!r} differs from the file "
                         f"name {p.stem!r}")
        for i, r in enumerate(doc.data.get("requires") or []):
            if not isinstance(r, dict):
                continue
            sid = r.get("skill")
            if ctx.skills and sid not in ctx.skills:
                ctx.rep.error("roles", rp, doc.line_of(("requires", i)), f"unknown skill id {sid!r}")
            elif ctx.skills.get(sid, {}).get("deprecated"):
                ctx.rep.error("roles", rp, doc.line_of(("requires", i)), f"skill {sid!r} is deprecated")
            lv = r.get("level")
            if isinstance(lv, int) and lv not in ctx.level_ids:
                ctx.rep.error("roles", rp, doc.line_of(("requires", i)), f"level {lv} is not a skill-map level")
            pf = r.get("promoted_from")
            imp = ctx.skills.get(sid, {}).get("importance") if sid in ctx.skills else None
            if "promoted_from" in r and sid in ctx.skills and pf != imp:
                ctx.rep.warn("roles", rp, doc.line_of(("requires", i, "promoted_from")),
                             f"promoted_from {pf!r} differs from the skill map importance {imp!r}")


# =========================================================================== file scans
@dataclass
class Link:
    line: int
    target: str
    image: bool
    alt: str | None
    html: bool = False


def _parse_dest(s: str, i: int) -> tuple[str, int] | None:
    """Parse a link destination starting at s[i] (just after '('). Returns (dest, index after ')')."""
    n = len(s)
    while i < n and s[i] in " \t":
        i += 1
    if i < n and s[i] == "<":
        j = s.find(">", i)
        if j < 0:
            return None
        dest = s[i + 1:j]
        i = j + 1
    else:
        depth, j = 0, i
        while j < n and not s[j].isspace():
            if s[j] == "\\":
                j += 2
                continue
            if s[j] == "(":
                depth += 1
            elif s[j] == ")":
                if depth == 0:
                    break
                depth -= 1
            j += 1
        dest = s[i:j]
        i = j
    # optional title
    while i < n and s[i] in " \t":
        i += 1
    if i < n and s[i] in "\"'(":
        close = {"\"": "\"", "'": "'", "(": ")"}[s[i]]
        j = s.find(close, i + 1)
        if j < 0:
            return None
        i = j + 1
        while i < n and s[i] in " \t":
            i += 1
    if i < n and s[i] == ")":
        return dest, i + 1
    return None


_HTML_TAG = re.compile(r"<(img|a|source)\b([^>]*)>", re.I | re.S)
_ATTR = re.compile(r"([a-zA-Z-]+)\s*=\s*(\"[^\"]*\"|'[^']*'|[^\s>]+)")
_REF_DEF = re.compile(r"^ {0,3}\[([^\]]+)\]:\s*<?([^\s>]+)>?", re.M)


def extract_links(masked: str) -> list[Link]:
    """Inline links/images, reference definitions and HTML img/a/source from code-masked Markdown."""
    out: list[Link] = []
    line_starts = [0] + [m.end() for m in re.finditer("\n", masked)]

    def line_at(pos: int) -> int:
        lo, hi = 0, len(line_starts) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if line_starts[mid] <= pos:
                lo = mid
            else:
                hi = mid - 1
        return lo + 1

    i, n = 0, len(masked)
    while i < n:
        j = masked.find("[", i)
        if j < 0:
            break
        if j > 0 and masked[j - 1] == "\\":
            i = j + 1
            continue
        image = j > 0 and masked[j - 1] == "!"
        depth, k = 0, j
        while k < n:
            ch = masked[k]
            if ch == "\\":
                k += 2
                continue
            if ch == "[":
                depth += 1
            elif ch == "]":
                depth -= 1
                if depth == 0:
                    break
            elif ch == "\n" and k + 1 < n and masked[k + 1] == "\n":
                break   # links do not span paragraphs
            k += 1
        if k >= n or masked[k] != "]":
            i = j + 1
            continue
        if k + 1 < n and masked[k + 1] == "(":
            parsed = _parse_dest(masked, k + 2)
            if parsed:
                dest, end = parsed
                out.append(Link(line_at(j), dest, image, masked[j + 1:k] if image else None))
                i = end
                continue
        i = j + 1
    for m in _REF_DEF.finditer(masked):
        out.append(Link(line_at(m.start()), m.group(2), False, None))
    for m in _HTML_TAG.finditer(masked):
        tag = m.group(1).lower()
        attrs = {a.lower(): v.strip("\"'") for a, v in _ATTR.findall(m.group(2))}
        if tag == "img":
            out.append(Link(line_at(m.start()), attrs.get("src", ""), True, attrs.get("alt"), html=True))
        elif tag == "a" and "href" in attrs:
            out.append(Link(line_at(m.start()), attrs["href"], False, None, html=True))
        elif tag == "source" and "src" in attrs:
            out.append(Link(line_at(m.start()), attrs["src"], False, None, html=True))
    return out


def _marp_alt(alt: str) -> str:
    return " ".join(t for t in alt.split() if not MARP_ALT_TOKEN.match(t))


def check_markdown_links(ctx: Ctx, relpath: str, text: str, is_marp: bool) -> None:
    masked = mask_code(text)
    fm = split_front_matter(masked)
    if fm.text is not None:   # front matter is YAML, not Markdown
        head = len(masked) - len(fm.body)
        masked = re.sub(r"[^\n]", " ", masked[:head]) + fm.body
    base = (ctx.root / relpath).parent
    for ln in extract_links(masked):
        tgt = ln.target.strip()
        if ln.image:
            alt = ln.alt
            if alt is not None and is_marp and not ln.html:
                alt = _marp_alt(alt)
            if alt is None or not alt.strip():
                ctx.rep.warn("alt", relpath, ln.line, f"image {tgt!r} has no alt text")
        if not tgt or tgt.startswith("#") or SCHEME.match(tgt) or tgt.startswith("//"):
            continue
        if any(c in tgt for c in "<>{}…") or "..." in PurePosixPath(tgt).name:
            continue   # template placeholder
        path = urllib.parse.unquote(tgt.split("#", 1)[0].split("?", 1)[0])
        if not path:
            continue
        dest = (ctx.root / path.lstrip("/")) if path.startswith("/") else (base / path)
        try:
            resolved = dest.resolve()
            resolved.relative_to(ctx.root.resolve())
        except ValueError:
            ctx.rep.error("links", relpath, ln.line, f"link {tgt!r} points outside the repository")
            continue
        if not resolved.exists():
            kind = "image" if ln.image else "link"
            ctx.rep.error("links", relpath, ln.line, f"broken {kind}: {tgt!r} does not exist")
        elif path.startswith("/"):
            ctx.rep.warn("links", relpath, ln.line, f"use a relative path instead of {tgt!r}")


def check_slides_footer(ctx: Ctx, relpath: str, text: str) -> None:
    need = (ctx.policy.get("attribution") or {}).get("footer_must_contain", "TESA")
    fm = split_front_matter(text)
    footer = None
    if fm.text is not None:
        doc = parse_yaml(fm.text, 1)
        if doc.error:
            ctx.rep.error("yaml", relpath, doc.error_line, doc.error)
            return
        if isinstance(doc.data, dict):
            footer = doc.data.get("footer")
    if not isinstance(footer, str) or need not in footer:
        ctx.rep.error("tesa-footer", relpath, 1, f"Marp front matter needs `footer:` containing {need!r} "
                      f"(BUILD_SPEC §1.9 short credit line)")
    elif ctx.site.credit_line:
        # BUILD_SPEC §1.9: "merge with an existing footer" — every part of the credit line must be
        # there, other credits may sit between the parts.
        parts = [p.strip() for p in ctx.site.credit_line.split("·") if p.strip()]
        missing = [p for p in parts if _loose(p) not in _loose(footer)]
        if missing:
            ctx.rep.warn("tesa-footer", relpath, 1, "footer lacks part of the credit line in "
                         f"site.config.yaml: {' · '.join(missing)}")
    masked = mask_code(fm.body if fm.text is not None else text)
    first = fm.body_line if fm.text is not None else 1
    for n, line in enumerate(masked.split("\n"), start=first):
        for m in re.finditer(r"<!--\s*footer\s*:\s*(.*?)\s*-->", line):
            if need not in m.group(1):
                ctx.rep.error("tesa-footer", relpath, n, f"a `footer:` directive replaces the TESA credit "
                              f"for the rest of the deck; keep {need!r} in it")


def load_allowlist() -> set[str]:
    allow = set()
    if ALLOW_FILE.is_file():
        for line in ALLOW_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "|" not in line:
                continue
            value, reason = line.split("|", 1)
            if value.strip() and reason.strip():
                allow.add(value.strip())
    return allow


def _secret_value_ok(v: str, allow: set[str]) -> bool:
    return not v or v.startswith("<") or bool(PLACEHOLDER.match(v)) or v in allow


def check_secrets(ctx: Ctx, relpath: str, text: str, allow: set[str]) -> None:
    low = relpath.lower()
    for n, line in enumerate(text.split("\n"), 1):
        for rx, what in SECRET_ANY:
            if rx.search(line):
                ctx.rep.error("secrets", relpath, n, f"{what} in a published file")
        m = None
        if low.endswith(".py") or low.endswith(MD_EXTS):
            m = SECRET_PY.match(line)
            val = m.group(2) if m else None
        if m is None and low.endswith(C_EXTS + MD_EXTS):
            m = SECRET_C.match(line)
            val = m.group(1) if m else None
        if m is not None and not _secret_value_ok(val, allow):
            ctx.rep.error("secrets", relpath, n, "literal secret assigned to a secret-shaped name; use a "
                          "<placeholder> or add the value to tools/credentials_allow.txt with a reason")


LEAK_PRAGMA = "validate:ignore-leak"   # on the same line: a detector's own pattern, not a leak


def check_leaks(ctx: Ctx, relpath: str, text: str) -> None:
    for n, line in enumerate(text.split("\n"), 1):
        if LEAK_PRAGMA in line:
            continue
        for rx, what in LEAK_PATTERNS:
            if rx.search(line):
                ctx.rep.error("leaks", relpath, n, f"{what}: {rx.search(line).group(0)!r}")


def check_terms_file(ctx: Ctx, relpath: str, text: str, kind: str) -> None:
    in_courses = relpath.startswith("courses/")
    for f in check_terms.scan_text(text, kind):
        msg = f"[{f.rule}] \"{f.text}\" — {f.hint}"
        if in_courses:
            ctx.rep.error("terms", relpath, f.line, msg)
        else:
            ctx.rep.warn("terms", relpath, f.line, msg)


def check_pairs(ctx: Ctx) -> None:
    sides: dict[str, dict[tuple[str, str], str]] = {"practice": {}, "solution": {}}
    for f in ctx.files:
        if not f.startswith("courses/"):
            continue
        parts = f.split("/")
        for i, seg in enumerate(parts[:-1]):
            if seg in sides:
                rest = "/".join(parts[i + 1:])
                if PurePosixPath(rest).name.lower() in ("readme.md", "readme.en.md", ".gitkeep"):
                    break
                sides[seg][("/".join(parts[:i]), rest)] = f
                break
    for a, b in (("practice", "solution"), ("solution", "practice")):
        for key, f in sorted(sides[a].items()):
            if key not in sides[b]:
                ctx.rep.error("pairs", f, 0, f"{a}/{key[1]} has no {b}/{key[1]} next to it")


def scan_files(ctx: Ctx) -> None:
    limit = int((ctx.policy.get("limits") or {}).get("max_file_bytes", 5 * 1024 * 1024))
    allow = load_allowlist()
    for f in ctx.files:
        p = ctx.root / f
        low = f.lower()
        in_courses = f.startswith("courses/")
        if in_courses:
            try:
                size = p.stat().st_size
            except OSError:
                size = 0
            if size > limit:
                ctx.rep.error("size", f, 0, f"{size / 1048576:.1f} MB is over the {limit / 1048576:.0f} MB "
                              "limit (BUILD_SPEC §3)")
        if not is_text_file(f):
            continue
        text = read_text(p)
        if text is None:
            continue
        text = text.replace("\r\n", "\n")
        if not f.startswith("tools/"):
            check_leaks(ctx, f, text)
        if not f.startswith("tools/tests/"):
            for n, what, hit in authorship_findings(text):
                ctx.rep.error("authorship", f, n, f"{what}: {hit!r} — authors are people (CONTRIBUTING.md)")
        if in_courses:
            check_secrets(ctx, f, text, allow)
        kind = check_terms.kind_of(f)
        if kind == "md":
            check_terms_file(ctx, f, text, "md")
            if not f.startswith("site/"):
                head = split_front_matter(text).text
                is_marp = PurePosixPath(f).name.startswith("slides") or bool(
                    head and re.search(r"^marp\s*:\s*true\b", head, re.M))
                check_markdown_links(ctx, f, text, is_marp)
            if in_courses and re.match(r"^slides(\.[a-z]{2})?\.md$", PurePosixPath(f).name):
                check_slides_footer(ctx, f, text)
        elif kind == "yaml" and (in_courses or f == "catalog/tracks.yaml"):
            check_terms_file(ctx, f, text, "yaml")


def check_root_notice(ctx: Ctx) -> None:
    files = (ctx.policy.get("attribution") or {}).get("root_files") or ["NOTICE", "ATTRIBUTION.md"]
    abbr = (ctx.policy.get("attribution") or {}).get("footer_must_contain", "TESA")
    names = [n for n in (ctx.site.org_th, ctx.site.org_en) if n]
    for name in files:
        p = ctx.root / name
        if not p.is_file():
            ctx.rep.error("tesa-notice", name, 0, "missing (BUILD_SPEC §1.9: everyone must credit TESA)")
            continue
        text = read_text(p) or ""
        if abbr not in text:
            ctx.rep.error("tesa-notice", name, 0, f"does not name {abbr}")
        elif names and not any(_loose(n) in _loose(text) for n in names):
            ctx.rep.warn("tesa-notice", name, 0, "does not give the official name "
                         f"({' / '.join(names)})")


def _loose(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def check_config(ctx: Ctx) -> None:
    for w in ctx.site.warnings:
        ctx.rep.warn("config", "site.config.yaml", 0, w)


# =========================================================================== driver
def run(root: Path, strict: bool = False, excludes: tuple[str, ...] | None = None) -> Reporter:
    root = Path(root).resolve()
    rep = Reporter(strict)
    if Draft202012Validator is None:
        rep.error("internal", "tools/requirements.txt", 0, "jsonschema is not installed: could not check "
                  "(pip install -r tools/requirements.txt)")
        return rep
    policy = load_policy()
    ctx = Ctx(root=root, rep=rep, policy=policy)
    if excludes is None:
        excludes = (FIXTURES_REL,)
    ctx.files = iter_files(root, excludes)
    ctx.site = load_site_config(root, policy)

    def step(name: str, fn, *args) -> None:
        try:
            fn(*args)
        except Exception as exc:  # a crash is "could not check", never a pass
            tb = traceback.extract_tb(exc.__traceback__)[-1]
            rep.error("internal", "tools/validate.py", tb.lineno,
                      f"{name} crashed ({type(exc).__name__}: {exc}); its result is unknown")

    step("config", check_config, ctx)
    step("skills", check_skills, ctx)
    step("catalog", check_catalog, ctx)
    for cid, entry in list(ctx.catalog.items()):
        if entry.get("in_tree") and isinstance(cid, str):
            step(f"course {cid}", check_course, ctx, cid)
    step("prereq", check_prereqs, ctx)
    step("tracks", check_tracks, ctx)
    step("videos", check_videos, ctx)
    step("roles", check_roles, ctx)
    step("pairs", check_pairs, ctx)
    step("files", scan_files, ctx)
    step("notice", check_root_notice, ctx)
    return rep


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--root", default=str(REPO_ROOT), help="repository root (default: this repo)")
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    ap.add_argument("--all-warnings", action="store_true", help="print every warning (default: 25 per check)")
    ap.add_argument("--list-checks", action="store_true", help="list the checks and exit")
    ap.add_argument("--json", metavar="FILE", help="also write the findings as JSON")
    ns = ap.parse_args(argv)
    if ns.list_checks:
        for c, d in CHECKS.items():
            print(f"{c:<13} {d}")
        return 0
    rep = run(Path(ns.root), strict=ns.strict)
    gha = bool(os.environ.get("GITHUB_ACTIONS"))
    print_report(rep, gha, 0 if ns.all_warnings else 25)
    if ns.json:
        Path(ns.json).write_text(json.dumps({
            "errors": [f.__dict__ for f in sorted(set(rep.errors))],
            "warnings": [f.__dict__ for f in sorted(set(rep.warnings))],
            "summary": {c: {"errors": e, "warnings": w} for c, (e, w) in rep.by_check().items()},
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 1 if rep.failed else 0


if __name__ == "__main__":
    sys.exit(main())
