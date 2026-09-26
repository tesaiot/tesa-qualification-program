#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: Apache-2.0
"""Shared helpers for the TESA Open Knowledge site scripts (sync_content.py, slides.py).

Nothing here knows a site origin, base path or repo URL: every such value comes from
site.config.yaml at the repo root (BUILD_SPEC §7).
"""
from __future__ import annotations

import os
import posixpath
import re
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import quote, unquote

import yaml

IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".avif"}
THAI_RE = re.compile(r"[฀-๿]")


# --------------------------------------------------------------------------- problems
@dataclass
class Problem:
    level: str  # "error" | "warning"
    where: str
    message: str


@dataclass
class Problems:
    items: list[Problem] = field(default_factory=list)

    def error(self, where: str, message: str) -> None:
        self.items.append(Problem("error", where, message))

    def warn(self, where: str, message: str) -> None:
        self.items.append(Problem("warning", where, message))

    @property
    def errors(self) -> list[Problem]:
        return [p for p in self.items if p.level == "error"]

    @property
    def warnings(self) -> list[Problem]:
        return [p for p in self.items if p.level == "warning"]

    def report(self, stream=sys.stderr) -> None:
        # GitHub Actions turns "::error file=...::msg" into annotations; plain text elsewhere.
        gha = os.environ.get("GITHUB_ACTIONS") == "true"
        for p in self.items:
            if gha:
                kind = "error" if p.level == "error" else "warning"
                print(f"::{kind} file={p.where}::{p.message}", file=stream)
            else:
                print(f"  {p.level.upper():7} {p.where}: {p.message}", file=stream)


# --------------------------------------------------------------------------- config
@dataclass
class SiteConfig:
    origin: str
    base: str  # "" or "/something" (no trailing slash)
    title: str
    description: dict
    repo_url: str
    branch: str
    ide_origin: str
    credit: dict
    raw: dict

    def url(self, route: str, lang: str = "th") -> str:
        """Site-absolute URL path (with base) for a page route. route has no leading/trailing slash."""
        parts = [self.base]
        if lang == "en":
            parts.append("/en")
        if route:
            parts.append("/" + route)
        return "".join(parts) + "/"

    def absolute(self, route: str, lang: str = "th") -> str:
        return self.origin + self.url(route, lang)

    def asset_url(self, repo_path: str) -> str:
        return f"{self.base}/content-assets/{quote(repo_path)}"

    def gh_blob(self, repo_path: str, ref: str) -> str:
        return f"{self.repo_url}/blob/{ref}/{quote(repo_path)}"

    def gh_tree(self, repo_path: str, ref: str) -> str:
        return f"{self.repo_url}/tree/{ref}/{quote(repo_path)}"

    def gh_edit(self, repo_path: str) -> str:
        return f"{self.repo_url}/edit/{self.branch}/{quote(repo_path)}"


def load_site_config(repo: Path) -> SiteConfig:
    path = repo / "site.config.yaml"
    if not path.is_file():
        sys.exit(f"[site] {path} not found: the site cannot know its origin/base without it (BUILD_SPEC §7).")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}

    def need(*keys):
        cur = data
        for k in keys:
            if not isinstance(cur, dict) or k not in cur or cur[k] in (None, ""):
                sys.exit(f"[site] site.config.yaml: missing required key {'.'.join(keys)}")
            cur = cur[k]
        return cur

    base = str(need("site", "base")).strip()
    base = "" if base in ("", "/") else "/" + base.strip("/")
    credit = need("credit")
    for k in ("line", "attribution"):
        if k not in credit:
            sys.exit(f"[site] site.config.yaml: missing required key credit.{k}")
    site = data.get("site", {})
    return SiteConfig(
        origin=str(need("site", "origin")).rstrip("/"),
        base=base,
        title=str(site.get("title") or "TESA Open Knowledge"),
        description=site.get("description") or {},
        repo_url=str(need("repo", "url")).rstrip("/"),
        branch=str(need("repo", "branch")),
        ide_origin=str(need("ide", "origin")).rstrip("/"),
        credit=credit,
        raw=data,
    )


# --------------------------------------------------------------------------- small utils
def pick(value, lang: str, fallback: str = "") -> str:
    """Return the `lang` text of a {th:..., en:...} value (falls back to the other language)."""
    if value is None:
        return fallback
    if isinstance(value, dict):
        for key in (lang, "th", "en"):
            v = value.get(key)
            if isinstance(v, str) and v.strip():
                return v.strip()
        for v in value.values():
            if isinstance(v, str) and v.strip():
                return v.strip()
        return fallback
    return str(value).strip()


def both(value) -> dict:
    return {"th": pick(value, "th"), "en": pick(value, "en")}


def one_line(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def has_thai(text: str) -> bool:
    return bool(THAI_RE.search(text or ""))


def slug_segment(seg: str) -> str:
    s = seg.lower()
    s = re.sub(r"[^a-z0-9._-]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s or "page"


FM_RE = re.compile(r"\A﻿?---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", re.S)


def split_front_matter(text: str, where: str, problems: Problems | None = None):
    """Return (front_matter_dict_or_None, body, raw_front_matter_text_or_None)."""
    text = text.replace("\r\n", "\n")
    m = FM_RE.match(text)
    if not m:
        return None, text.lstrip("﻿"), None
    raw = m.group(1)
    try:
        data = yaml.safe_load(raw) or {}
    except yaml.YAMLError as exc:
        if problems is not None:
            problems.error(where, f"front matter is not valid YAML: {exc}")
        data = {}
    if not isinstance(data, dict):
        if problems is not None:
            problems.error(where, "front matter is not a YAML mapping")
        data = {}
    return data, text[m.end():], raw


def first_h1(body: str):
    """Return (title, body_without_that_h1) when the first content line is an ATX H1."""
    lines = body.split("\n")
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        m = re.match(r"^#\s+(.+?)\s*#*\s*$", line)
        if m:
            return m.group(1).strip(), "\n".join(lines[:i] + lines[i + 1:])
        return None, body
    return None, body


def load_yaml_file(path: Path, problems: Problems, where: str):
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        problems.error(where, f"cannot read YAML: {exc}")
        return None


def safe_rmtree(path: Path, must_end_with: tuple[str, ...]) -> None:
    """Delete a generated directory, refusing anything that is not one of ours."""
    p = path.resolve()
    if not any(str(p).endswith(sfx) for sfx in must_end_with):
        sys.exit(f"[site] refusing to delete {p}: not a generated directory")
    if p.exists():
        shutil.rmtree(p)


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() and dst.stat().st_size == src.stat().st_size and dst.stat().st_mtime >= src.stat().st_mtime:
        return
    shutil.copy2(src, dst)


# --------------------------------------------------------------------------- link rewriting
SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
FENCE_RE = re.compile(r"^( {0,3})(`{3,}|~{3,})")
CODESPAN_RE = re.compile(r"(?<!`)(`+)(?!`)(.+?)(?<!`)\1(?!`)", re.S)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
# [text](dest "title") and ![alt](dest); text may hold one level of nested brackets.
INLINE_LINK_RE = re.compile(
    r"(!?)\[((?:[^\[\]\n]|\[[^\[\]\n]*\])*)\]\(\s*(<[^>\n]*>|(?:[^\s()]|\([^\s()]*\))*)((?:\s+(?:\"[^\"\n]*\"|'[^'\n]*'|\([^)\n]*\)))?)\s*\)"
)
REFDEF_RE = re.compile(r"^( {0,3}\[[^\]\n]+\]:[ \t]*)(<[^>\n]*>|\S+)", re.M)
HTML_TAG_RE = re.compile(r"<[a-zA-Z][a-zA-Z0-9-]*\b[^<>]*>")
HTML_ATTR_RE = re.compile(r"(\s(?:src|href|poster|data-src)\s*=\s*)(\"[^\"]*\"|'[^']*')", re.I)


@dataclass
class Target:
    kind: str  # "keep" | "page" | "slides" | "image" | "file" | "dir" | "missing" | "outside"
    repo_path: str = ""
    suffix: str = ""  # "#frag" / "?q"
    lang: str | None = None  # language of the linked page file ("en" for *.en.md)


def classify(dest: str, src_dir: str, repo: Path, page_sources: dict) -> Target:
    """Resolve a link destination written in a file living in repo dir `src_dir`."""
    d = dest.strip()
    if d.startswith("<") and d.endswith(">"):
        d = d[1:-1].strip()
    if not d or d.startswith("#") or d.startswith("//") or SCHEME_RE.match(d) or d.startswith("/"):
        return Target("keep")
    m = re.match(r"^([^#?]*)(.*)$", d)
    path_part, suffix = m.group(1), m.group(2)
    if not path_part:
        return Target("keep")
    rel = unquote(path_part)
    joined = posixpath.normpath(posixpath.join(src_dir, rel)) if src_dir else posixpath.normpath(rel)
    if joined.startswith("../") or joined == "..":
        return Target("outside", joined, suffix)
    full = repo / joined
    if full.is_dir():
        for readme in ("README.md",):
            cand = posixpath.join(joined, readme) if joined != "." else readme
            if cand in page_sources:
                return Target("page", cand, suffix)
        return Target("dir", joined, suffix)
    if not full.is_file():
        return Target("missing", joined, suffix)
    name = posixpath.basename(joined)
    ext = posixpath.splitext(name)[1].lower()
    if name in ("slides.md", "slides.en.md"):
        return Target("slides", joined, suffix, "en" if name == "slides.en.md" else None)
    if joined in page_sources:
        return Target("page", joined, suffix, "en" if name.endswith(".en.md") else None)
    if ext in IMAGE_EXT:
        return Target("image", joined, suffix)
    return Target("file", joined, suffix)


def slides_route(repo_path_of_deck: str) -> str:
    """courses/<c>/<m>/<l>/slides.md -> slides/<c>/<m>/<l>"""
    d = posixpath.dirname(repo_path_of_deck)
    if d.startswith("courses/"):
        d = d[len("courses/"):]
    return "slides/" + "/".join(slug_segment(s) for s in d.split("/") if s)


def slides_url(cfg: SiteConfig, repo_path_of_deck: str) -> str:
    route = slides_route(repo_path_of_deck)
    if repo_path_of_deck.endswith("slides.en.md"):
        return f"{cfg.base}/{route}/en.html"
    return f"{cfg.base}/{route}/"


@dataclass
class RewriteContext:
    cfg: SiteConfig
    repo: Path
    ref: str  # commit sha or branch for GitHub links
    page_sources: dict  # repo path -> route (every Markdown file that becomes a page)
    problems: Problems
    # Where Markdown-syntax images are copied for Astro to optimise (None = use public assets).
    docs_dir: Path | None = None
    public_assets_dir: Path | None = None
    copied: set = field(default_factory=set)
    # Lesson folders whose quiz.yaml is rendered on the lesson page (a link to it becomes #tok-quiz).
    quiz_dirs: set = field(default_factory=set)
    stats: dict = field(default_factory=lambda: {"links": 0, "images": 0, "github": 0, "missing": 0})


def _copy_public(ctx: RewriteContext, repo_path: str) -> str:
    if ctx.public_assets_dir is not None:
        key = ("public", repo_path)
        if key not in ctx.copied:
            copy_file(ctx.repo / repo_path, ctx.public_assets_dir / repo_path)
            ctx.copied.add(key)
    return ctx.cfg.asset_url(repo_path)


def _copy_docs(ctx: RewriteContext, repo_path: str, out_md: Path) -> str:
    """Copy an image next to the generated pages (mirror of the repo layout) for Astro to optimise."""
    assert ctx.docs_dir is not None
    dst = ctx.docs_dir / repo_path
    key = ("docs", repo_path)
    if key not in ctx.copied:
        copy_file(ctx.repo / repo_path, dst)
        ctx.copied.add(key)
    rel = os.path.relpath(dst, out_md.parent).replace(os.sep, "/")
    if not rel.startswith("../"):
        rel = "./" + rel
    if re.search(r"[\s()<>]", rel):
        rel = "<" + rel + ">"
    return rel


def rewrite_dest(ctx: RewriteContext, dest: str, src_file: str, page_lang: str, *,
                 syntax: str, out_md: Path | None) -> str | None:
    """Return the new destination, or None to signal a missing image (caller replaces it)."""
    src_dir = posixpath.dirname(src_file)
    t = classify(dest, src_dir, ctx.repo, ctx.page_sources)
    if t.kind == "keep":
        return dest
    ctx.stats["links"] += 1
    if t.kind == "outside":
        ctx.problems.error(src_file, f"link leaves the repository: {dest}")
        ctx.stats["missing"] += 1
        return None if syntax == "md-image" else dest
    if t.kind == "missing":
        ctx.problems.error(src_file, f"link target does not exist: {dest} (resolved to {t.repo_path})")
        ctx.stats["missing"] += 1
        if syntax == "md-image":
            return None
        return ctx.cfg.gh_blob(t.repo_path, ctx.ref) + t.suffix
    if t.kind == "page":
        lang = "en" if t.lang == "en" else page_lang
        return ctx.cfg.url(ctx.page_sources[t.repo_path], lang) + t.suffix
    if t.kind == "slides":
        return slides_url(ctx.cfg, t.repo_path) + t.suffix
    if t.kind == "image":
        ctx.stats["images"] += 1
        if syntax == "md-image" and ctx.docs_dir is not None and out_md is not None:
            return _copy_docs(ctx, t.repo_path, out_md) + t.suffix
        return _copy_public(ctx, t.repo_path) + t.suffix
    if (t.kind == "file" and posixpath.basename(t.repo_path) == "quiz.yaml"
            and posixpath.dirname(t.repo_path) == src_dir and src_dir in ctx.quiz_dirs
            and posixpath.basename(src_file).startswith("README")):
        return "#tok-quiz"
    if t.kind == "dir":
        ctx.stats["github"] += 1
        return ctx.cfg.gh_tree(t.repo_path, ctx.ref) + t.suffix
    ctx.stats["github"] += 1
    return ctx.cfg.gh_blob(t.repo_path, ctx.ref) + t.suffix


def _protect(pattern: re.Pattern, text: str, store: list[str]) -> str:
    def sub(m):
        store.append(m.group(0))
        return f"\u0000{len(store) - 1}\u0000"
    return pattern.sub(sub, text)


def _restore(text: str, store: list[str]) -> str:
    # Placeholders may nest (a comment stored before a code span); loop until stable.
    for _ in range(3):
        new = re.sub(r"\u0000(\d+)\u0000", lambda m: store[int(m.group(1))], text)
        if new == text:
            break
        text = new
    return text


def _rewrite_prose(ctx: RewriteContext, text: str, src_file: str, page_lang: str, out_md: Path | None) -> str:
    store: list[str] = []
    text = _protect(COMMENT_RE, text, store)
    text = _protect(CODESPAN_RE, text, store)

    def inline(m: re.Match) -> str:
        bang, label, dest, title = m.group(1), m.group(2), m.group(3), m.group(4) or ""
        label = INLINE_LINK_RE.sub(inline, label)  # nested image inside a link
        syntax = "md-image" if bang else "md-link"
        new = rewrite_dest(ctx, dest, src_file, page_lang, syntax=syntax, out_md=out_md)
        if new is None:
            shown = label or dest
            return f"<mark class=\"tok-missing\">[missing image: {shown}]</mark>"
        return f"{bang}[{label}]({new}{title})"

    text = INLINE_LINK_RE.sub(inline, text)

    def refdef(m: re.Match) -> str:
        new = rewrite_dest(ctx, m.group(2), src_file, page_lang, syntax="ref", out_md=out_md)
        return m.group(1) + (new if new is not None else m.group(2))

    text = REFDEF_RE.sub(refdef, text)

    def tag(m: re.Match) -> str:
        def attr(a: re.Match) -> str:
            q = a.group(2)[0]
            val = a.group(2)[1:-1]
            new = rewrite_dest(ctx, val, src_file, page_lang, syntax="html", out_md=out_md)
            return f"{a.group(1)}{q}{new if new is not None else val}{q}"
        return HTML_ATTR_RE.sub(attr, m.group(0))

    text = HTML_TAG_RE.sub(tag, text)
    return _restore(text, store)


def rewrite_markdown(ctx: RewriteContext, body: str, src_file: str, page_lang: str, out_md: Path | None) -> str:
    """Rewrite every relative link/image in a Markdown body; fenced code is left untouched."""
    out: list[str] = []
    prose: list[str] = []
    fence: str | None = None

    def flush():
        if prose:
            out.append(_rewrite_prose(ctx, "\n".join(prose), src_file, page_lang, out_md))
            prose.clear()

    for line in body.split("\n"):
        m = FENCE_RE.match(line)
        if fence is None:
            if m:
                flush()
                fence = m.group(2)
                out.append(line)
            else:
                prose.append(line)
        else:
            out.append(line)
            if m and m.group(2)[0] == fence[0] and len(m.group(2)) >= len(fence) and not line.strip()[len(m.group(2)):].strip():
                fence = None
    flush()
    return "\n".join(out)


# --------------------------------------------------------------------------- credentials
# Same rule as AIoT_Cirriculum/tools/check_credentials.py (NAME = "literal" for a secret-shaped
# name; a <placeholder> or an empty string is what published material must carry), applied to
# the Markdown the site publishes. Code files are linked to GitHub, not copied; [tools] scans them.
SECRET_ASSIGN_RE = re.compile(
    r"(?im)^\s*[A-Z_]*(?:PASS|PASSWORD|SECRET|TOKEN|API_KEY)[A-Z_]*\s*[=:]\s*[\"']([^\"']*)[\"']"
)
SECRET_LITERAL_PATTERNS = [
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
]
# Same list as tools/validate.py LEAK_PATTERNS (internal paths, retired domain). The pragma keeps the
# validator from reporting this detector's own pattern as a leak.
INTERNAL_PATH_RE = re.compile(  # validate:ignore-leak
    r"/mnt/tesaiot|/home/wiroon\b|/tmp/claude-|TESAIoT_PLAN|Bento_Engine|IMPLEMENT_PLAN|TESA_Rules|\btesaiot\.com\b",  # validate:ignore-leak
    re.I,
)
# A literal that is obviously a placeholder (same rule as tools/validate.py PLACEHOLDER).
PLACEHOLDER_RE = re.compile(r"^(?:<.*>|\$\{.*\}|x+|X+|\*+|\.\.\.|YOUR_[A-Z_]+|your[-_ ].*)$")


_ALLOW_CACHE: dict = {}


def credential_allowlist(repo: Path) -> set:
    """Values tools/credentials_allow.txt accepts (`VALUE | reason`; a line without a reason is ignored)."""
    key = str(repo)
    if key not in _ALLOW_CACHE:
        allow = set()
        path = repo / "tools" / "credentials_allow.txt"
        if path.is_file():
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "|" in line:
                    value, reason = line.split("|", 1)
                    if value.strip() and reason.strip():
                        allow.add(value.strip())
        _ALLOW_CACHE[key] = allow
    return _ALLOW_CACHE[key]


def scan_secrets(text: str, where: str, problems: Problems, allow: set | None = None) -> None:
    allow = allow or set()
    for m in SECRET_ASSIGN_RE.finditer(text):
        value = m.group(1)
        if not value or PLACEHOLDER_RE.match(value) or value in allow:
            continue
        problems.error(where, f"secret-shaped literal (use a <placeholder>): {m.group(0).strip()[:70]}")
    for pat in SECRET_LITERAL_PATTERNS:
        for m in pat.finditer(text):
            problems.error(where, f"credential material in published text: {m.group(0)[:40]}")
    for m in INTERNAL_PATH_RE.finditer(text):
        problems.error(where, f"internal path or retired domain in published text: {m.group(0)}")
