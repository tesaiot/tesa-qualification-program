# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: Apache-2.0
"""Helpers shared by the TESA Open Knowledge tools.

Only the standard library and PyYAML are used here, so every tool can import this module.
"""
from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator

import yaml

TOOLS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOLS_DIR.parent
SCHEMA_DIR = REPO_ROOT / "schemas"
POLICY_FILE = TOOLS_DIR / "policy.yaml"

# Directories that are never content: VCS, dependencies, build output, caches.
SKIP_DIR_NAMES = frozenset({
    ".git", "node_modules", "__pycache__", ".pytest_cache", ".venv", "venv", ".astro", "dist",
    ".cache", ".mypy_cache", ".ruff_cache", "lychee",
})
# The tools' own test fixtures deliberately break every rule; never scan them as repo content.
FIXTURES_REL = "tools/tests/fixtures"

TEXT_EXTS = frozenset({
    ".md", ".mdx", ".markdown", ".yaml", ".yml", ".json", ".toml", ".txt", ".cff", ".py", ".c",
    ".h", ".cpp", ".hpp", ".cc", ".ino", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".astro", ".html",
    ".htm", ".css", ".scss", ".sh", ".ini", ".cfg", ".svg", ".xml", ".csv",
})
TEXT_NAMES = frozenset({"NOTICE", "CODEOWNERS", "Makefile", "Dockerfile", ".gitignore",
                        ".gitattributes", ".editorconfig"})


# --------------------------------------------------------------------------- YAML
_BASE_LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)   # libyaml when present: same result, faster


class UniqueKeyLoader(_BASE_LOADER):
    """SafeLoader that rejects duplicate mapping keys and keeps dates as strings.

    Duplicate keys are silently merged by PyYAML (the last one wins) — a lesson with two
    `develops:` keys would lose one without a word. Dates stay strings so that the data is
    JSON-compatible and a schema can check it.
    """


UniqueKeyLoader.yaml_implicit_resolvers = {
    first: [(tag, rx) for tag, rx in resolvers if tag != "tag:yaml.org,2002:timestamp"]
    for first, resolvers in _BASE_LOADER.yaml_implicit_resolvers.items()
}


def _construct_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False):
    seen: dict[Any, int] = {}
    for key_node, _value in node.value:
        if key_node.tag == "tag:yaml.org,2002:merge":
            continue
        key = loader.construct_object(key_node, deep=deep)
        try:
            if key in seen:
                raise yaml.constructor.ConstructorError(
                    None, None,
                    f"duplicate key {key!r} (first defined on line {seen[key]})",
                    key_node.start_mark)
            seen[key] = key_node.start_mark.line + 1
        except TypeError:  # unhashable key; let PyYAML report it
            pass
    return _BASE_LOADER.construct_mapping(loader, node, deep)


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping)


@dataclass
class YamlDoc:
    data: Any = None
    error: str | None = None
    error_line: int = 0
    lines: dict[tuple, int] = field(default_factory=dict)
    line_offset: int = 0            # added to every line (front matter starts below line 1)

    def line_of(self, path) -> int:
        """Best line for a JSON path (tuple/list of keys and indices); 0 if unknown."""
        parts = tuple(str(p) for p in path)
        while parts not in self.lines and parts:
            parts = parts[:-1]
        line = self.lines.get(parts, 0)
        return line + self.line_offset if line else (self.line_offset + 1 if self.line_offset else 0)


def _line_map(text: str) -> dict[tuple, int]:
    try:
        node = yaml.compose(text, Loader=UniqueKeyLoader)
    except yaml.YAMLError:
        return {}
    out: dict[tuple, int] = {}

    def walk(n, path):
        if n is None:
            return
        out.setdefault(path, n.start_mark.line + 1)
        if isinstance(n, yaml.MappingNode):
            for k, v in n.value:
                p = path + (str(k.value),)
                out[p] = k.start_mark.line + 1
                walk(v, p)
        elif isinstance(n, yaml.SequenceNode):
            for i, v in enumerate(n.value):
                walk(v, path + (str(i),))

    walk(node, ())
    return out


def parse_yaml(text: str, line_offset: int = 0) -> YamlDoc:
    doc = YamlDoc(line_offset=line_offset)
    try:
        doc.data = yaml.load(text, Loader=UniqueKeyLoader)  # noqa: S506 - SafeLoader subclass
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None) or getattr(exc, "context_mark", None)
        doc.error = " ".join(str(exc).split())
        doc.error_line = (mark.line + 1 + line_offset) if mark else (line_offset + 1)
        return doc
    doc.lines = _line_map(text)
    return doc


def load_yaml(path: Path) -> YamlDoc:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return YamlDoc(error=f"cannot read: {exc}", error_line=0)
    return parse_yaml(text)


# --------------------------------------------------------------------------- front matter
@dataclass
class FrontMatter:
    text: str | None          # YAML text between the fences, None when the file has none
    body: str                 # everything after the closing fence
    first_line: int           # 1-based line of the first YAML line (2) — 0 when absent
    body_line: int            # 1-based line where the body starts


def split_front_matter(text: str) -> FrontMatter:
    """Split a `---` fenced YAML block at the very top of a Markdown file."""
    if text.startswith("\ufeff"):
        text = text[1:]
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].rstrip("\r\n").rstrip() != "---":
        return FrontMatter(None, text, 0, 1)
    for j in range(1, len(lines)):
        if lines[j].rstrip("\r\n").rstrip() in ("---", "..."):
            return FrontMatter("".join(lines[1:j]), "".join(lines[j + 1:]), 2, j + 2)
    return FrontMatter(None, text, 0, 1)   # unterminated: treat as no front matter


def body_of(text: str) -> str:
    """The Markdown body after the front matter, line endings normalised to \\n."""
    return split_front_matter(text.replace("\r\n", "\n")).body


# --------------------------------------------------------------------------- Markdown masking
_FENCE = re.compile(r"^( {0,3})(`{3,}|~{3,})(.*)$")
_BLOCK_HTML_CODE = re.compile(r"<(pre|code)\b[^>]*>.*?</\1\s*>", re.S | re.I)


def _blank(s: str) -> str:
    return re.sub(r"[^\n]", " ", s)


def mask_inline_code(line: str) -> str:
    """Replace `code spans` (any backtick run length) with spaces, keeping columns."""
    runs = [(m.start(), m.end()) for m in re.finditer(r"`+", line)]
    if len(runs) < 2:
        return line
    chars = list(line)
    k = 0
    while k < len(runs):
        s, e = runs[k]
        n = e - s
        for j in range(k + 1, len(runs)):
            if runs[j][1] - runs[j][0] == n:
                for x in range(s, runs[j][1]):
                    chars[x] = " "
                k = j + 1
                break
        else:
            k += 1
    return "".join(chars)


def mask_code(text: str) -> str:
    """Return `text` with fenced code blocks, inline code and <pre>/<code> blanked out.

    The result has the same lines and columns as the input, so a match in it can be reported
    at the right place in the original file.
    """
    text = _BLOCK_HTML_CODE.sub(lambda m: _blank(m.group(0)), text)
    out = []
    fence = None
    for line in text.split("\n"):
        m = _FENCE.match(line)
        if fence:
            if m and m.group(2)[0] == fence[0] and len(m.group(2)) >= fence[1] and not m.group(3).strip():
                fence = None
            out.append(_blank(line))
            continue
        if m and not (m.group(2)[0] == "`" and "`" in m.group(3)):
            fence = (m.group(2)[0], len(m.group(2)))
            out.append(_blank(line))
            continue
        out.append(mask_inline_code(line))
    return "\n".join(out)


def mask_front_matter(text: str) -> str:
    """Blank the front matter block (keeps line numbers)."""
    fm = split_front_matter(text)
    if fm.text is None:
        return text
    head_len = len(text) - len(fm.body)
    return _blank(text[:head_len]) + fm.body


# --------------------------------------------------------------------------- files
def iter_files(root: Path, excludes: tuple[str, ...] = (FIXTURES_REL,)) -> list[str]:
    """Every regular file under root as a sorted list of POSIX paths relative to root.

    Skips VCS/dependency/build folders, symlinks, and the relative directories in `excludes`.
    """
    root = Path(root)
    excl = {e.strip("/") for e in excludes if e}
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root).replace(os.sep, "/")
        rel_dir = "" if rel_dir == "." else rel_dir
        keep = []
        for d in dirnames:
            rel = f"{rel_dir}/{d}" if rel_dir else d
            if d in SKIP_DIR_NAMES or rel in excl or os.path.islink(os.path.join(dirpath, d)):
                continue
            keep.append(d)
        dirnames[:] = sorted(keep)
        for f in filenames:
            full = os.path.join(dirpath, f)
            if os.path.islink(full) or not os.path.isfile(full):
                continue
            out.append(f"{rel_dir}/{f}" if rel_dir else f)
    return sorted(out)


def is_text_file(rel: str) -> bool:
    p = Path(rel)
    return p.suffix.lower() in TEXT_EXTS or p.name in TEXT_NAMES


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


# --------------------------------------------------------------------------- config
def load_policy() -> dict:
    doc = load_yaml(POLICY_FILE)
    if doc.error or not isinstance(doc.data, dict):
        raise SystemExit(f"tools/policy.yaml is unreadable: {doc.error}")
    return doc.data


@dataclass
class SiteConfig:
    origin: str
    base: str
    repo_url: str
    branch: str
    credit_line: str | None
    org_th: str
    org_en: str
    warnings: list[str]
    attribution: dict = field(default_factory=dict)   # {th, en} templates with {title} and {repo}

    @property
    def site_url(self) -> str:
        return f"{self.origin}{self.base}"


def _dig(d: Any, *keys):
    for k in keys:
        if not isinstance(d, dict) or k not in d:
            return None
        d = d[k]
    return d


def load_site_config(root: Path, policy: dict | None = None) -> SiteConfig:
    """Read site.config.yaml (owned by [site]); fall back to tools/policy.yaml with a warning."""
    policy = policy or load_policy()
    fb = policy.get("fallback", {})
    warnings: list[str] = []
    path = Path(root) / "site.config.yaml"
    data: dict = {}
    if not path.is_file():
        warnings.append("site.config.yaml is missing; using the fallback site/repo values from "
                        "tools/policy.yaml")
    else:
        doc = load_yaml(path)
        if doc.error or not isinstance(doc.data, dict):
            warnings.append(f"site.config.yaml is unreadable ({doc.error}); using fallbacks")
        else:
            data = doc.data

    def pick(keys, fb_keys, label):
        v = _dig(data, *keys)
        if isinstance(v, str) and v.strip():
            return v.strip()
        v = _dig(fb, *fb_keys)
        if data:  # the file exists but lacks the key
            warnings.append(f"site.config.yaml has no {label}; using fallback {v!r}")
        return v

    origin = pick(("site", "origin"), ("site", "origin"), "site.origin").rstrip("/")
    base = pick(("site", "base"), ("site", "base"), "site.base")
    base = "/" + base.strip("/") if base.strip("/") else ""
    repo_url = pick(("repo", "url"), ("repo", "url"), "repo.url").rstrip("/")
    branch = pick(("repo", "branch"), ("repo", "branch"), "repo.branch")
    credit_line = _dig(data, "credit", "line")
    org_th = _dig(data, "credit", "org", "th") or _dig(fb, "credit", "org", "th")
    org_en = _dig(data, "credit", "org", "en") or _dig(fb, "credit", "org", "en")
    attribution = _dig(data, "credit", "attribution")
    attribution = {k: v for k, v in attribution.items() if isinstance(v, str)} if isinstance(attribution, dict) else {}
    return SiteConfig(origin, base, repo_url, branch, credit_line, org_th, org_en, warnings, attribution)


def rel(path: Path, root: Path) -> str:
    try:
        return Path(path).resolve().relative_to(Path(root).resolve()).as_posix()
    except ValueError:
        return Path(path).as_posix()


def eprint(*args) -> None:
    print(*args, file=sys.stderr)


def iter_course_dirs(root: Path) -> Iterator[Path]:
    cdir = Path(root) / "courses"
    if cdir.is_dir():
        for d in sorted(cdir.iterdir()):
            if d.is_dir() and not d.name.startswith(".") and not d.is_symlink():
                yield d
