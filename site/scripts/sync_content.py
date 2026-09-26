#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: Apache-2.0
"""Turn the repository into Starlight content for the TESA Open Knowledge site.

    python3 site/scripts/sync_content.py            # writes into site/ (what CI runs, with --strict)
    python3 site/scripts/sync_content.py --site-dir /tmp/preview-site --strict

The site's Markdown is GENERATED, never committed. Sources of truth are the repo files:
  skills/skills.yaml, skills/roles/*.yaml, catalog/courses.yaml, catalog/tracks.yaml,
  courses/<id>/course.yaml + README(.en).md + every lesson README(.en).md, ATTRIBUTION.md, ...

Writes (all git-ignored):
  <site>/src/content/docs/**          Starlight pages (TH at the root, EN under en/)
  <site>/src/generated/site-config.json   site.config.yaml + build ref, read by astro.config.mjs
  <site>/src/generated/sidebar.json       the Starlight sidebar
  <site>/src/generated/site-data.json     skills x lessons view model for /roadmap/ and /coverage/
  <site>/public/content-assets/**      images referenced from raw HTML or plain links

Routes (URL = site.base [+ /en] + route + /):
  courses/<course>/<module>/<lesson>/   lesson (lesson folder README.md)
  skills/<skill-id>/                    one page per skill (ids keep their dots)
  catalog/  pathways/  skills/  attribution/  about/<doc>/   generated pages
"""
from __future__ import annotations

import argparse
import datetime as _dt
import html
import json
import os
import posixpath
import re
import shutil
import sys
import uuid
from dataclasses import dataclass, field
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tok_site import (  # noqa: E402
    Problems,
    RewriteContext,
    SiteConfig,
    both,
    credential_allowlist,
    first_h1,
    has_thai,
    load_site_config,
    load_yaml_file,
    one_line,
    pick,
    rewrite_markdown,
    safe_rmtree,
    scan_secrets,
    slides_url,
    slug_segment,
    split_front_matter,
)

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_REPO = SCRIPT_DIR.parent.parent
LANGS = ("th", "en")
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".github", "site"}
MODULE_RE = re.compile(r"^m\d{2}-")
LESSON_RE = re.compile(r"^l\d{2}-")

# Learner-facing vocabulary for values found in YAML (UI labels for the page chrome live in
# site/src/lib/strings.ts). Unknown codes are shown as written.
VOCAB = {
    "status": {
        "pre-alpha": {"th": "ร่างแรก (pre-alpha)", "en": "Pre-alpha"},
        "alpha": {"th": "ทดลองใช้ (alpha)", "en": "Alpha"},
        "beta": {"th": "ทดสอบใช้งาน (beta)", "en": "Beta"},
        "stable": {"th": "พร้อมใช้ (stable)", "en": "Stable"},
    },
    "board": {
        "eva-kit": {"th": "Eva Kit", "en": "Eva Kit"},
        "devkit": {"th": "Dev Kit", "en": "Dev Kit"},
        "none": {"th": "ไม่ต้องใช้บอร์ด", "en": "No board needed"},
    },
    "time": {
        "concept": {"th": "แนวคิด", "en": "concept"},
        "practise": {"th": "ฝึก", "en": "practice"},
        "practice": {"th": "ฝึก", "en": "practice"},
        "lab": {"th": "แล็บ", "en": "lab"},
        "check": {"th": "เช็กความเข้าใจ", "en": "check"},
    },
    "audience": {
        "public": {"th": "บุคคลทั่วไป", "en": "General public"},
        "student": {"th": "นักเรียนนักศึกษา", "en": "Students"},
        "developer": {"th": "นักพัฒนา", "en": "Developers"},
        "entrepreneur": {"th": "ผู้ประกอบการ", "en": "Entrepreneurs"},
        "educator": {"th": "ผู้สอน", "en": "Educators"},
    },
    "origin": {
        "eer": {"th": "โหนดบนแผนภาพ Roadmap v1.2.3", "en": "Node on the roadmap diagram v1.2.3"},
        "eer-readme": {"th": "หัวข้อใน README ของ Roadmap", "en": "Topic in the roadmap README"},
        "tesa": {"th": "TESA เพิ่ม", "en": "Added by TESA"},
    },
    "page": {
        "lab": {"th": "แล็บ", "en": "Lab"},
        "instructor-notes": {"th": "บันทึกสำหรับผู้สอน", "en": "Instructor notes"},
    },
    "badge_variant": {"pre-alpha": "caution", "alpha": "caution", "beta": "note"},
}

# Root documents published under /about/ when present (TH file, optional EN file).
ABOUT_DOCS = [
    ("tqp/levels.md", "tqp/levels.en.md", "tqp-levels"),
    ("tqp/certification.md", "tqp/certification.en.md", "tqp-certification"),
    ("CONTRIBUTING.md", "CONTRIBUTING.en.md", "contributing"),
    ("CODE_OF_CONDUCT.md", "CODE_OF_CONDUCT.en.md", "code-of-conduct"),
    ("GOVERNANCE.md", "GOVERNANCE.en.md", "governance"),
    ("TRADEMARKS.md", "TRADEMARKS.en.md", "trademarks"),
    ("NOTICE.md", None, "notice"),
    ("templates/AUTHORING.md", "templates/AUTHORING.en.md", "authoring"),
]


def esc(text) -> str:
    return html.escape(str(text if text is not None else ""), quote=True)


def md_cell(text) -> str:
    return str(text if text is not None else "").replace("|", "\\|").replace("\n", " ")


def as_int(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


# --------------------------------------------------------------------------- model
@dataclass
class Lesson:
    id: str
    course: str
    module: str
    dir: str  # repo path of the lesson folder
    route: str
    fm: dict
    fm_en: dict | None
    title: dict
    summary: dict
    has_en: bool
    deck: str | None = None
    deck_en: str | None = None
    quiz: list = field(default_factory=list)


@dataclass
class Module:
    id: str
    course: str
    dir: str
    route: str
    title: dict
    has_page: bool
    lessons: list = field(default_factory=list)


@dataclass
class Course:
    id: str
    dir: str
    route: str
    cat: dict
    meta: dict  # course.yaml
    title: dict
    summary: dict
    has_page: bool
    has_en: bool
    modules: list = field(default_factory=list)


@dataclass
class Page:
    route: str
    lang: str
    out: Path
    title: str
    body: str
    front: dict = field(default_factory=dict)
    src: str | None = None


class Builder:
    def __init__(self, repo: Path, site_dir: Path, ref: str, problems: Problems):
        self.repo = repo
        self.site_dir = site_dir
        self.docs = site_dir / "src" / "content" / "docs"
        self.gen = site_dir / "src" / "generated"
        self.public_assets = site_dir / "public" / "content-assets"
        self.ref = ref
        self.p = problems
        self.cfg: SiteConfig = load_site_config(repo)
        self.pages: list[Page] = []
        self.page_sources: dict[str, str] = {}  # repo md path -> route
        self.courses: list[Course] = []
        self.lessons: dict[str, Lesson] = {}
        self.skills: dict[str, dict] = {}
        self.skill_order: list[str] = []
        self.coverage: dict[str, list] = {}
        self.roles: dict[str, list] = {}
        self.about: list[tuple[str, dict]] = []  # (route, title both)
        self.ctx = RewriteContext(cfg=self.cfg, repo=repo, ref=ref, page_sources=self.page_sources,
                                  problems=problems, docs_dir=self.docs, public_assets_dir=self.public_assets)

    # ------------------------------------------------------------------ helpers
    def rel(self, path: Path) -> str:
        return path.resolve().relative_to(self.repo.resolve()).as_posix()

    def url(self, route: str, lang: str) -> str:
        return self.cfg.url(route, lang)

    def out_path(self, route: str, lang: str, src_name: str | None = None) -> Path:
        """Output .md path. Pages built from a repo file mirror its folder so relative images resolve."""
        base = self.docs / "en" if lang == "en" else self.docs
        if not route:
            return base / "index.md"
        return base / (route + ".md") if src_name is None else base / src_name

    def attribution(self, title: str, lang: str) -> str:
        tpl = pick(self.cfg.credit.get("attribution"), lang)
        return tpl.replace("{title}", title).replace("{repo}", self.cfg.repo_url)

    def add_page(self, page: Page) -> None:
        self.pages.append(page)

    # ------------------------------------------------------------------ load
    def load_skills(self) -> None:
        data = load_yaml_file(self.repo / "skills" / "skills.yaml", self.p, "skills/skills.yaml")
        if not isinstance(data, dict):
            sys.exit("[site] skills/skills.yaml is missing or unreadable; the site cannot be built without it.")
        self.skillmap = data
        self.levels = {int(lv["id"]): lv for lv in data.get("levels", []) if isinstance(lv, dict) and "id" in lv}
        self.level_by_code = {str(lv.get("code")): lv for lv in self.levels.values()}
        self.areas = [a for a in data.get("areas", []) if isinstance(a, dict)]
        self.groups = {g["id"]: g for g in data.get("groups", []) if isinstance(g, dict) and "id" in g}
        for s in data.get("skills", []):
            if not isinstance(s, dict) or "id" not in s:
                continue
            if s["id"] in self.skills:
                self.p.error("skills/skills.yaml", f"duplicate skill id {s['id']}")
            self.skills[s["id"]] = s
            self.skill_order.append(s["id"])
            self.coverage[s["id"]] = []
            self.roles[s["id"]] = []

    def skill_uuid(self, sid: str) -> str:
        return str(uuid.uuid5(uuid.NAMESPACE_URL, self.cfg.origin + self.cfg.url(f"skills/{sid}", "th")))

    def skill_name(self, sid: str) -> dict:
        s = self.skills.get(sid)
        return {"th": s.get("th") or sid, "en": s.get("en") or sid} if s else {"th": sid, "en": sid}

    def level_name(self, code_or_int) -> dict:
        lv = None
        if isinstance(code_or_int, int):
            lv = self.levels.get(code_or_int)
        else:
            lv = self.level_by_code.get(str(code_or_int))
        if not lv:
            return {"th": str(code_or_int), "en": str(code_or_int)}
        return {"th": f"{lv.get('code')} {lv.get('th', '')}".strip(), "en": f"{lv.get('code')} {lv.get('en', '')}".strip()}

    def load_roles(self) -> None:
        roles_dir = self.repo / "skills" / "roles"
        files = sorted(list(roles_dir.glob("*.yaml")) + list(roles_dir.glob("*.yml"))) if roles_dir.is_dir() else []
        if not files:
            self.p.warn("skills/roles/", "no role profiles yet; skill pages list no roles")
            return
        by_group: dict[str, list] = {}
        for sid, s in self.skills.items():
            by_group.setdefault(s.get("group"), []).append(sid)
        for path in files:
            where = self.rel(path)
            data = load_yaml_file(path, self.p, where)
            if not isinstance(data, dict):
                continue
            rid = str(data.get("id") or path.stem)
            title = both(data.get("title") or data.get("name") or rid)
            found: dict[str, dict] = {}

            def record(sid, level=None, importance=None):
                targets = by_group.get(sid[:-2], []) if isinstance(sid, str) and sid.endswith(".*") else [sid]
                for t in targets:
                    if t in self.skills:
                        cur = found.setdefault(t, {"level": None, "importance": None})
                        if level is not None:
                            cur["level"] = level
                        if importance:
                            cur["importance"] = importance

            def walk(node, top=False):
                if isinstance(node, dict):
                    sk = node.get("skill")
                    if isinstance(sk, str):
                        imp = node.get("importance") or node.get("promoted_from")
                        if imp is None and node.get("to") in ("R", "Rec", "P"):
                            imp = node.get("to")
                        lvl = as_int(node.get("level") if node.get("level") is not None else node.get("to"))
                        record(sk, lvl, imp)
                    for k, v in node.items():
                        if top and k in ("id", "title", "name", "summary", "target_level"):
                            continue
                        if isinstance(k, str) and (k in self.skills or k.endswith(".*")) and not isinstance(v, (dict, list)):
                            record(k, as_int(v), v if v in ("R", "Rec", "P") else None)
                        else:
                            walk(v)
                elif isinstance(node, list):
                    for v in node:
                        if isinstance(v, str) and (v in self.skills or v.endswith(".*")):
                            record(v)
                        else:
                            walk(v)

            walk(data, top=True)
            for sid, info in found.items():
                self.roles[sid].append({"id": rid, "title": title, **info})
            if not found:
                self.p.warn(where, "role profile names no known skill id (format not recognised?)")

    def load_catalog(self) -> None:
        data = load_yaml_file(self.repo / "catalog" / "courses.yaml", self.p, "catalog/courses.yaml") or {}
        self.catalog = [c for c in (data.get("courses") or []) if isinstance(c, dict) and c.get("id")]
        tracks_path = self.repo / "catalog" / "tracks.yaml"
        self.tracks = load_yaml_file(tracks_path, self.p, "catalog/tracks.yaml") if tracks_path.is_file() else None
        if self.tracks is None:
            self.p.warn("catalog/tracks.yaml", "not present yet; the pathways page says so")
        self.load_videos()

    def load_videos(self) -> None:
        """catalog/videos.yaml -> self.videos_by_lesson: lesson id -> [video view model] (file order).
        References are checked by tools/validate.py; anything unresolvable here is reported and skipped."""
        self.videos_by_lesson: dict[str, list] = {}
        self.video_channels: dict[str, dict] = {}
        path = self.repo / "catalog" / "videos.yaml"
        if not path.is_file():
            return
        data = load_yaml_file(path, self.p, "catalog/videos.yaml") or {}
        prov = data.get("provider") or {}
        channels = data.get("channels") or {}
        playlists = {pl.get("id"): pl for pl in data.get("playlists") or [] if isinstance(pl, dict)}
        for key, ch in channels.items():
            self.video_channels[key] = {"key": key, "name": ch.get("name"), "credit": ch.get("credit"), "url": ch.get("url")}
        for v in data.get("videos") or []:
            if not isinstance(v, dict) or v.get("channel") not in channels:
                self.p.error("catalog/videos.yaml", f"video {v!r}: unknown channel")
                continue
            vid = str(v["id"])
            pl = playlists.get(v.get("playlist"))
            model = {
                "id": vid,
                "title": str(v.get("title") or vid),
                "url": str(prov.get("watch", "")).replace("{id}", vid),
                "thumb": str(prov.get("thumb", "")).replace("{id}", vid),
                "channel": v["channel"],
                "playlist": ({"title": pl.get("title"), "url": str(prov.get("playlist", "")).replace("{id}", str(pl["id"]))}
                             if pl else None),
            }
            for lid in v.get("lessons") or []:
                self.videos_by_lesson.setdefault(str(lid), []).append(model)

    def notice_tqp(self, cat: dict) -> dict | None:
        """catalog/courses.yaml `notice` (e.g. content that follows firmware still in development) for every lesson
        page of the course (the course README carries the same notice itself); the box links to the repository's
        issues so a reader can report a mismatch."""
        n = cat.get("notice") if isinstance(cat.get("notice"), dict) else None
        if not n:
            return None
        return {"label": n.get("label"), "text": n.get("text"), "issues": f"{self.cfg.repo_url.rstrip('/')}/issues"}

    def videos_tqp(self, lesson_ids) -> dict | None:
        """The companion-video box for a page: the videos of these lessons (first mention wins the order),
        the channels to credit and the playlists they come from."""
        seen, items = set(), []
        for lid in lesson_ids:
            for v in self.videos_by_lesson.get(lid, []):
                if v["id"] not in seen:
                    seen.add(v["id"])
                    items.append(v)
        if not items:
            return None
        used = list(dict.fromkeys(v["channel"] for v in items))
        playlists = list({v["playlist"]["url"]: v["playlist"] for v in items if v.get("playlist")}.values())
        return {"items": items, "channels": [self.video_channels[k] for k in used], "playlists": playlists}

    # ------------------------------------------------------------------ discover pages
    def md_route(self, repo_path: str) -> str:
        parts = repo_path.split("/")
        dirs, name = parts[:-1], parts[-1]
        dir_route = "/".join(slug_segment(d) for d in dirs)
        if name in ("README.md", "README.en.md"):
            return dir_route
        stem = name[:-6] if name.endswith(".en.md") else name[:-3]
        return (dir_route + "/" if dir_route else "") + slug_segment(stem)

    def discover_courses(self) -> None:
        courses_dir = self.repo / "courses"
        in_tree = [c for c in self.catalog if c.get("in_tree")]
        ids = [c["id"] for c in in_tree]
        extra = []
        if courses_dir.is_dir():
            for d in sorted(courses_dir.iterdir()):
                if d.is_dir() and (d / "course.yaml").is_file() and d.name not in ids:
                    self.p.warn(f"courses/{d.name}", "course folder is not listed in catalog/courses.yaml")
                    extra.append({"id": d.name, "in_tree": True})
        seen_routes: dict[str, str] = {}
        for cat in in_tree + extra:
            cid = cat["id"]
            cdir = courses_dir / cid
            if not cdir.is_dir():
                self.p.warn("catalog/courses.yaml", f"in_tree course {cid} has no courses/{cid}/ folder yet")
                continue
            # Every Markdown file in the course becomes a page, except decks.
            for path in sorted(cdir.rglob("*.md")):
                relparts = path.relative_to(cdir).parts
                if any(part in SKIP_DIRS or part.startswith(".") for part in relparts[:-1]):
                    continue
                name = path.name
                rp = self.rel(path)
                if name in ("slides.md", "slides.en.md"):
                    continue
                if name.startswith("_"):
                    self.p.warn(rp, "file name starts with '_' (Starlight ignores it); not published")
                    continue
                route = self.md_route(rp)
                key = ("en" if name.endswith(".en.md") else "th") + ":" + route
                if key in seen_routes:
                    self.p.error(rp, f"two files map to the same page {route}: {seen_routes[key]}")
                    continue
                seen_routes[key] = rp
                self.page_sources[rp] = route
            self.courses.append(self.load_course(cat, cdir))

    def load_course(self, cat: dict, cdir: Path) -> Course:
        cid = cat["id"]
        crel = f"courses/{cid}"
        meta = load_yaml_file(cdir / "course.yaml", self.p, f"{crel}/course.yaml") if (cdir / "course.yaml").is_file() else None
        if meta is None:
            self.p.error(f"{crel}/course.yaml", "missing course.yaml")
            meta = {}
        title = both(meta.get("title") or cat.get("title") or cid)
        course = Course(
            id=cid, dir=crel, route=self.md_route(f"{crel}/README.md"), cat=cat, meta=meta,
            title=title, summary=both(meta.get("summary") or ""),
            has_page=(cdir / "README.md").is_file(), has_en=(cdir / "README.en.md").is_file(),
        )
        listed = [m for m in (meta.get("modules") or []) if isinstance(m, dict) and m.get("id")]
        listed_ids = [m["id"] for m in listed]
        folders = sorted(d.name for d in cdir.iterdir() if d.is_dir() and MODULE_RE.match(d.name))
        for mid in folders:
            if mid not in listed_ids:
                self.p.warn(f"{crel}/{mid}", "module folder is not listed in course.yaml modules")
        for mid in listed_ids + [f for f in folders if f not in listed_ids]:
            mdir = cdir / mid
            if not mdir.is_dir():
                self.p.warn(f"{crel}/course.yaml", f"module {mid} is listed but has no folder yet")
                continue
            mmeta = next((m for m in listed if m["id"] == mid), {})
            mtitle = mmeta.get("title")
            if not mtitle and (mdir / "README.md").is_file():
                _, body, _ = split_front_matter((mdir / "README.md").read_text(encoding="utf-8"), f"{crel}/{mid}/README.md")
                h1, _ = first_h1(body)
                mtitle = h1
            module = Module(id=mid, course=cid, dir=f"{crel}/{mid}", route=self.md_route(f"{crel}/{mid}/README.md"),
                            title=both(mtitle or mid), has_page=(mdir / "README.md").is_file())
            for ldir in sorted(d for d in mdir.iterdir() if d.is_dir() and LESSON_RE.match(d.name)):
                lesson = self.load_lesson(course, module, ldir)
                if lesson:
                    module.lessons.append(lesson)
            course.modules.append(module)
        return course

    PAGE_ONLY_FILES = {"README.md", "README.en.md", "quiz.yaml"}

    def lesson_has_material(self, repo_dir: str) -> bool:
        """True when a lesson folder holds files beyond its own page (README/quiz), e.g. code or slides."""
        root = self.repo / repo_dir
        for f in root.rglob("*"):
            if f.is_file() and not (f.parent == root and f.name in self.PAGE_ONLY_FILES):
                return True
        return False

    def load_lesson(self, course: Course, module: Module, ldir: Path):
        lrel = self.rel(ldir)
        readme = ldir / "README.md"
        if not readme.is_file():
            self.p.error(lrel, "lesson folder has no README.md")
            return None
        fm, _, _ = split_front_matter(readme.read_text(encoding="utf-8"), f"{lrel}/README.md", self.p)
        if not fm:
            self.p.error(f"{lrel}/README.md", "lesson README has no front matter (BUILD_SPEC §4)")
            fm = {}
        fm_en = None
        if (ldir / "README.en.md").is_file():
            fm_en, _, _ = split_front_matter((ldir / "README.en.md").read_text(encoding="utf-8"), f"{lrel}/README.en.md", self.p)
        lid = str(fm.get("id") or "")
        if not lid:
            self.p.error(f"{lrel}/README.md", "lesson front matter has no id")
            lid = lrel
        short = course.cat.get("short") or course.meta.get("short")
        if short and not re.match(rf"^{re.escape(str(short))}\.m\d{{2}}\.l\d{{2}}$", lid):
            self.p.warn(f"{lrel}/README.md", f"lesson id {lid} does not look like {short}.mNN.lNN")
        if lid in self.lessons:
            self.p.error(f"{lrel}/README.md", f"lesson id {lid} is also used by {self.lessons[lid].dir}")
        title = both(fm.get("title") or (fm_en or {}).get("title") or ldir.name)
        if fm_en and fm_en.get("title"):
            title["en"] = pick(fm_en.get("title"), "en", title["en"])
        summary = both(fm.get("summary") or "")
        if fm_en and fm_en.get("summary"):
            summary["en"] = pick(fm_en.get("summary"), "en", summary["en"])
        lesson = Lesson(id=lid, course=course.id, module=module.id, dir=lrel, route=self.md_route(f"{lrel}/README.md"),
                        fm=fm, fm_en=fm_en, title=title, summary=summary, has_en=fm_en is not None)
        if (ldir / "slides.md").is_file():
            lesson.deck = f"{lrel}/slides.md"
        if (ldir / "slides.en.md").is_file():
            lesson.deck_en = f"{lrel}/slides.en.md"
        declared = fm.get("slides")
        if declared and not (ldir / str(declared)).is_file():
            self.p.error(f"{lrel}/README.md", f"front matter slides: {declared} does not exist")
        if (ldir / "quiz.yaml").is_file():
            lesson.quiz = self.load_quiz(ldir / "quiz.yaml", f"{lrel}/quiz.yaml")
            if lesson.quiz:
                self.ctx.quiz_dirs.add(lrel)
        # coverage
        for d in fm.get("develops") or []:
            if not isinstance(d, dict):
                continue
            sid = d.get("skill")
            if sid not in self.skills:
                self.p.error(f"{lrel}/README.md", f"develops unknown skill id {sid!r} (skills/skills.yaml)")
                continue
            self.coverage[sid].append({"lesson": lid, "mode": "develops", "level": as_int(d.get("to"))})
        for a in fm.get("assesses") or []:
            if not isinstance(a, dict):
                continue
            sid = a.get("skill")
            if sid not in self.skills:
                self.p.error(f"{lrel}/README.md", f"assesses unknown skill id {sid!r} (skills/skills.yaml)")
                continue
            self.coverage[sid].append({"lesson": lid, "mode": "assesses", "level": as_int(a.get("level")),
                                       "evidence": a.get("evidence")})
        if not fm.get("develops"):
            self.p.warn(f"{lrel}/README.md", "lesson develops no skill (BUILD_SPEC §4 asks for at least one)")
        self.lessons[lid] = lesson
        return lesson

    def load_quiz(self, path: Path, where: str) -> list:
        data = load_yaml_file(path, self.p, where)
        items = data.get("items") if isinstance(data, dict) else data
        out = []
        for it in items or []:
            if not isinstance(it, dict):
                continue
            choices = [both(c) for c in (it.get("choices") or [])]
            ans = it.get("answer")
            answers = []
            for a in (ans if isinstance(ans, list) else ([] if ans is None else [ans])):
                if isinstance(a, int) and not isinstance(a, bool) and 0 <= a < len(choices):
                    answers.append({"index": a, "text": choices[a]})
                elif isinstance(a, int) and not isinstance(a, bool):
                    self.p.error(where, f"item {it.get('id')}: answer index {a} has no choice")
                else:
                    answers.append({"index": None, "text": both(a)})
            out.append({
                "id": str(it.get("id", "")), "type": str(it.get("type", "single")),
                "objective": as_int(it.get("objective")), "prompt": both(it.get("prompt")),
                "choices": choices, "answer": answers,
                "explain": both(it.get("explain")) if it.get("explain") else None,
            })
        return out

    def discover_root_docs(self) -> None:
        src = self.cfg.credit.get("page_source") or "ATTRIBUTION.md"
        self.attribution_src = src if (self.repo / src).is_file() else None
        if self.attribution_src:
            self.page_sources[self.attribution_src] = "attribution"
            en = src[:-3] + ".en.md"
            if (self.repo / en).is_file():
                self.page_sources[en] = "attribution"
        else:
            self.p.warn(src, "not present yet; /attribution/ is built from site.config.yaml credit wording")
        self.about_docs = []
        for th, en, slug in ABOUT_DOCS:
            if (self.repo / th).is_file():
                self.page_sources[th] = f"about/{slug}"
                if en and (self.repo / en).is_file():
                    self.page_sources[en] = f"about/{slug}"
                self.about_docs.append((th, en if en and (self.repo / en).is_file() else None, slug))

    # ------------------------------------------------------------------ build pages
    def body_from(self, repo_path: str, lang: str, out: Path, strip_title: bool = True):
        text = (self.repo / repo_path).read_text(encoding="utf-8")
        fm, body, _ = split_front_matter(text, repo_path, self.p)
        h1 = None
        if strip_title:
            h1, body = first_h1(body)
        scan_secrets(body, repo_path, self.p, credential_allowlist(self.repo))
        body = rewrite_markdown(self.ctx, body, repo_path, lang, out)
        return fm or {}, h1, body.strip() + "\n"

    def build_course_pages(self) -> None:
        for course in self.courses:
            for rp, route in list(self.page_sources.items()):
                if not rp.startswith(course.dir + "/"):
                    continue
                lang = "en" if rp.endswith(".en.md") else "th"
                name = posixpath.basename(rp)
                d = posixpath.dirname(rp)
                out_name = posixpath.join(d, "index.md" if name.startswith("README") else (name[:-6] + ".md" if lang == "en" else name))
                out = (self.docs / "en" / out_name) if lang == "en" else (self.docs / out_name)
                fm, h1, body = self.body_from(rp, lang, out)
                front: dict = {"editUrl": self.cfg.gh_edit(rp)}
                kind, title, desc = "page", None, ""
                lesson = next((l for l in self.lessons.values() if f"{l.dir}/README.md" == rp or f"{l.dir}/README.en.md" == rp), None)
                module = next((m for c in [course] for m in c.modules if f"{m.dir}/README.md" == rp or f"{m.dir}/README.en.md" == rp), None)
                if rp in (f"{course.dir}/README.md", f"{course.dir}/README.en.md"):
                    kind, title, desc = "course", course.title[lang], course.summary[lang]
                    front["tqp"] = self.course_tqp(course)
                elif module is not None:
                    kind, title = "module", module.title[lang]
                    desc = f"{course.title[lang]}"
                elif lesson is not None:
                    kind, title, desc = "lesson", lesson.title[lang], lesson.summary[lang]
                    front["tqp"] = self.lesson_tqp(lesson)
                else:
                    t = fm.get("title")
                    title = pick(t, lang) if t else h1
                    if not title:
                        stem = slug_segment(name[:-6] if lang == "en" else name[:-3])
                        label = VOCAB["page"].get(stem)
                        owner = next((l for l in self.lessons.values() if rp.startswith(l.dir + "/")), None)
                        title = (pick(label, lang) if label else stem.replace("-", " ").capitalize())
                        if owner:
                            title = f"{title}: {owner.title[lang]}"
                    if fm.get("summary") or fm.get("description"):
                        desc = pick(fm.get("summary") or fm.get("description"), lang)
                    front["sidebar"] = {"hidden": True}
                if desc:
                    front["description"] = one_line(desc)
                self.add_page(Page(route=route, lang=lang, out=out, title=one_line(title or route), body=body, front=front, src=rp))

    def course_tqp(self, course: Course) -> dict:
        m = course.meta
        hw = m.get("hardware") or {}
        return {
            "kind": "course",
            "id": course.id,
            "level": {"code": str(m.get("level") or course.cat.get("level") or ""),
                      "name": self.level_name(str(m.get("level") or course.cat.get("level") or ""))},
            "status": self.status(m.get("status") or course.cat.get("status")),
            "hours": m.get("hours"),
            "audience": [VOCAB["audience"].get(a, {"th": str(a), "en": str(a)}) for a in (m.get("audience") or [])],
            "hardware": self.hardware(hw),
            "license": {k: str(v) for k, v in (m.get("license") or {}).items()},
            "lessons": sum(len(mod.lessons) for mod in course.modules),
            "modules": len(course.modules),
            "source_url": self.cfg.gh_tree(course.dir, self.ref),
            "videos": self.videos_tqp(l.id for mod in course.modules for l in mod.lessons),
        }

    def status(self, code) -> dict:
        code = str(code or "")
        return {"code": code, "label": VOCAB["status"].get(code, {"th": code, "en": code})}

    def hardware(self, hw) -> dict:
        hw = hw if isinstance(hw, dict) else {}
        return {"emulator": bool(hw.get("emulator")),
                "boards": [{"id": str(b), "label": VOCAB["board"].get(str(b), {"th": str(b), "en": str(b)})}
                           for b in (hw.get("boards") or [])]}

    def lesson_tqp(self, lesson: Lesson) -> dict:
        fm = lesson.fm
        course = next(c for c in self.courses if c.id == lesson.course)
        module = next(m for m in course.modules if m.id == lesson.module)
        tm = fm.get("time_min") or {}
        parts = []
        if isinstance(tm, dict):
            for k, v in tm.items():
                n = as_int(v)
                if n is not None:
                    parts.append({"key": str(k), "min": n, "label": VOCAB["time"].get(str(k), {"th": str(k), "en": str(k)})})
        prereq = []
        for pid in fm.get("prerequisites") or []:
            pl = self.lessons_by_id_lazy(str(pid))
            if pl:
                prereq.append({"id": pl.id, "title": pl.title, "route": pl.route})
            else:
                prereq.append({"id": str(pid), "title": {"th": str(pid), "en": str(pid)}, "route": None})
                self.p.warn(f"{lesson.dir}/README.md", f"prerequisite {pid} is not a known lesson id")
        develops = [{"skill": d.get("skill"), "name": self.skill_name(d.get("skill")), "to": as_int(d.get("to")),
                     "importance": (self.skills.get(d.get("skill")) or {}).get("importance")}
                    for d in (fm.get("develops") or []) if isinstance(d, dict) and d.get("skill") in self.skills]
        assesses = []
        for a in fm.get("assesses") or []:
            if not isinstance(a, dict) or a.get("skill") not in self.skills:
                continue
            ev = a.get("evidence")
            ev_urls = {lang: self.evidence_url(lesson, ev, lang, report=(lang == "th")) for lang in LANGS}
            assesses.append({"skill": a["skill"], "name": self.skill_name(a["skill"]), "level": as_int(a.get("level")),
                             "evidence": str(ev or ""), "evidence_url": ev_urls})
        ctx = fm.get("context") if isinstance(fm.get("context"), dict) else {}
        # "Open BENTO IDE" only for MicroPython/BENTO lessons that have real material; C lessons build with
        # ModusToolbox and an outline (pre-alpha) lesson has nothing to open yet.
        status = str(fm.get("status") or "").lower()
        has_material = self.lesson_has_material(lesson.dir)
        ide = None
        is_bento = "bento" in str(ctx.get("ide", "")).lower() or str(ctx.get("lang", "")).lower() == "micropython"
        if is_bento and status != "pre-alpha" and has_material:
            ide = self.cfg.ide_origin + "/"
        # Material TESA itself adapted keeps its upstream credit (BUILD_SPEC §1.9).
        upstream = None
        src = fm.get("source") if isinstance(fm.get("source"), dict) else None
        csrc = course.meta.get("source") if isinstance(course.meta.get("source"), dict) else None
        for s in (src, csrc):
            if s and s.get("repo"):
                repo_url, ref, path = str(s["repo"]).rstrip("/"), s.get("ref"), s.get("path")
                if ref and path and "github.com/" in repo_url:
                    url = f"{repo_url}/blob/{ref}/{str(path).lstrip('/')}"
                elif ref and "github.com/" in repo_url:
                    url = f"{repo_url}/tree/{ref}"
                else:
                    url = repo_url
                upstream = {"url": url, "note": one_line(str(s.get("note") or (csrc or {}).get("note") or ""))}
                break
        return {
            "kind": "lesson",
            "id": lesson.id,
            "course": {"id": course.id, "title": course.title, "route": course.route if course.has_page else None},
            "module": {"id": module.id, "title": module.title, "route": module.route if module.has_page else None},
            "level": {"code": str(fm.get("level") or ""), "name": self.level_name(str(fm.get("level") or ""))},
            "time": {"total": sum(p["min"] for p in parts), "parts": parts},
            "hardware": self.hardware(fm.get("hardware")),
            "prerequisites": prereq,
            "develops": develops,
            "assesses": assesses,
            "status": self.status(fm.get("status")),
            "translation": str(fm.get("translation") or ("done" if lesson.has_en else "pending")),
            "slides": {"th": slides_url(self.cfg, lesson.deck) if lesson.deck else None,
                       "en": slides_url(self.cfg, lesson.deck_en) if lesson.deck_en else None},
            "ide": ide,
            # The GitHub button only when the folder holds more than the page itself (code, slides, lab, ...).
            "source_url": self.cfg.gh_tree(lesson.dir, self.ref) if has_material else None,
            "quiz": lesson.quiz,
            "videos": self.videos_tqp([lesson.id]),
            "notice": self.notice_tqp(course.cat),
            "cite": {
                "th": self.attribution(lesson.title["th"], "th"),
                "en": self.attribution(lesson.title["en"], "en"),
                "url": {"th": self.cfg.absolute(lesson.route, "th"), "en": self.cfg.absolute(lesson.route, "en")},
                "upstream": upstream,
            },
        }

    def evidence_url(self, lesson: Lesson, ev, lang: str = "th", report: bool = False):
        """Evidence may be a file ('practice/x.py'), a section ('README.md#checklist'), or free text that
        describes what the learner hands in ('video of the board ...'). Same rule as tools/validate.py:
        only a single path-like token (no whitespace, has '/' or a file extension) must resolve."""
        if not ev:
            return None
        target = str(ev).split("#", 1)[0].strip()
        if target and (re.search(r"\s", target) or not ("/" in target or re.search(r"\.[A-Za-z0-9]{1,5}$", target))):
            return None  # free-text deliverable: shown as text, nothing to link
        m = re.match(r"^([^#?]*)(.*)$", str(ev))
        path, frag = m.group(1), m.group(2)
        evp = posixpath.normpath(posixpath.join(lesson.dir, path)) if path else f"{lesson.dir}/README.md"
        if not (self.repo / evp).exists():
            if report:
                self.p.error(f"{lesson.dir}/README.md", f"assesses evidence {ev} does not exist")
            return None
        if evp in self.page_sources:
            return self.url(self.page_sources[evp], lang) + frag
        return self.cfg.gh_blob(evp, self.ref) + frag

    def lessons_by_id_lazy(self, lid: str):
        return self.lessons.get(lid)

    # ------------------------------------------------------------------ root docs
    def build_root_docs(self) -> None:
        # /attribution/ — "วิธีอ้างอิง TESA / How to cite TESA"
        titles = {"th": "วิธีอ้างอิง TESA", "en": "How to cite TESA"}
        if self.attribution_src:
            en_src = self.attribution_src[:-3] + ".en.md"
            for lang in LANGS:
                src = en_src if lang == "en" and (self.repo / en_src).is_file() else self.attribution_src
                out = self.out_path("attribution", lang)
                _, h1, body = self.body_from(src, lang, out)
                self.add_page(Page("attribution", lang, out, titles[lang], body,
                                   {"editUrl": self.cfg.gh_edit(src), "description": self.cfg.credit["line"]}, src))
        else:
            for lang in LANGS:
                body = self.fallback_attribution(lang)
                self.add_page(Page("attribution", lang, self.out_path("attribution", lang), titles[lang], body,
                                   {"editUrl": False, "description": self.cfg.credit["line"]}))
        for th, en, slug in self.about_docs:
            route = f"about/{slug}"
            text_th = (self.repo / th).read_text(encoding="utf-8")
            for lang in LANGS:
                if lang == "en":
                    if en:
                        src = en
                    elif not has_thai(text_th):
                        src = th  # English-only document: publish it at both locales, no fallback notice
                    else:
                        continue  # Thai-only: Starlight shows the TH page with its "not translated" notice
                else:
                    src = th
                out = self.out_path(route, lang)
                fm, h1, body = self.body_from(src, lang, out)
                title = pick(fm.get("title"), lang) if fm.get("title") else (h1 or slug.replace("-", " ").title())
                self.add_page(Page(route, lang, out, one_line(title), body, {"editUrl": self.cfg.gh_edit(src)}, src))
                if lang == "th":
                    self.about.append((route, {"th": one_line(title), "en": one_line(title)}))
                else:
                    self.about[-1] = (route, {"th": self.about[-1][1]["th"], "en": one_line(title)})

    def fallback_attribution(self, lang: str) -> str:
        c = self.cfg.credit
        ex_title = "ชื่อบทเรียนหรือหลักสูตร" if lang == "th" else "Lesson or course title"
        if lang == "th":
            return (
                f"เนื้อหาใน TESA Open Knowledge เผยแพร่ภายใต้สัญญาอนุญาต {c['licence']} "
                "นำไปใช้ต่อในงานที่ไม่ใช่เพื่อการค้าได้ สถาบันการศึกษามีคำอนุญาตเพิ่ม ขอเพียงอ้างอิงสมาคมสมองกลฝังตัวไทย (TESA) ทุกครั้งตามรูปแบบนี้\n\n"
                f"> {self.attribution(ex_title, 'th')}\n\n"
                f"ถ้าดัดแปลงเนื้อหา ให้ต่อท้ายว่า{pick(c.get('adapted_suffix'), 'th')}\n\n"
                f"บรรทัดเครดิตแบบสั้น (ท้ายหน้า ท้ายสไลด์): `{c['line']}`\n"
            )
        return (
            f"TESA Open Knowledge is published under {c['licence']}. Anyone may reuse it non-commercially, and "
            "educational institutions have an additional permission; "
            "please credit the Thai Embedded Systems Association (TESA) every time, in this form:\n\n"
            f"> {self.attribution(ex_title, 'en')}\n\n"
            f"If you changed the material, add{pick(c.get('adapted_suffix'), 'en')} after the title.\n\n"
            f"Short credit line (page and slide footers): `{c['line']}`\n"
        )

    # ------------------------------------------------------------------ skills
    def coverage_state(self, sid: str) -> dict:
        entries = self.coverage.get(sid, [])
        dev = [e["level"] for e in entries if e["mode"] == "develops" and e["level"] is not None]
        ass = [e["level"] for e in entries if e["mode"] == "assesses" and e["level"] is not None]
        n_dev = sum(1 for e in entries if e["mode"] == "develops")
        n_ass = sum(1 for e in entries if e["mode"] == "assesses")
        state = "assessed" if n_ass else ("developed" if n_dev else "none")
        return {"state": state, "dev_max": max(dev) if dev else None, "ass_max": max(ass) if ass else None,
                "n_dev": n_dev, "n_ass": n_ass}

    def build_skill_pages(self) -> None:
        importance = self.skillmap.get("importance") or {}
        fw = self.skillmap.get("framework") or {}
        area_of_group = {gid: g.get("area") for gid, g in self.groups.items()}
        areas = {a["id"]: a for a in self.areas}
        S = {
            "th": {"id": "รหัสทักษะ", "group": "กลุ่ม", "area": "หมวด", "imp": "ความสำคัญตาม Roadmap",
                   "imp_none": "ไม่มีสีใน Roadmap (TESA เพิ่ม)", "origin": "ที่มา", "node": "โหนดใน Roadmap",
                   "cov": "สถานะในคลังบทเรียน", "dev": "บทเรียนที่พัฒนาทักษะนี้", "ass": "บทเรียนที่ประเมินทักษะนี้",
                   "roles": "บทบาทที่ใช้ทักษะนี้", "levels": "ระดับความสามารถ", "none_yet": "ยังไม่มีบทเรียน",
                   "no_roles": "ยังไม่มีโปรไฟล์บทบาทที่ระบุทักษะนี้",
                   "col_lesson": "บทเรียน", "col_course": "หลักสูตร", "col_to": "พัฒนาถึงระดับ", "col_level": "ระดับ",
                   "col_ev": "หลักฐาน", "col_role": "บทบาท", "col_rimp": "ในบทบาทนี้", "col_min": "ระดับขั้นต่ำ",
                   "req": "จำเป็น (R)", "promoted": "ยกจาก {x} ในแผนที่", "tesa_imp": "TESA เพิ่ม",
                   "align": "ใช้อ้างอิงใน Open Badges 3.0 และ CASE", "roadmap": "ดูในแผนที่ทักษะ",
                   "license": ("ข้อมูลแผนที่ทักษะเผยแพร่ภายใต้ CC BY-SA 4.0 ดัดแปลงจาก "
                               "[Embedded Systems Engineering Roadmap](https://github.com/m3y54m/Embedded-Engineering-Roadmap) "
                               "ของ Meysam Parvizi"),
                   "states": {"none": "ยังไม่มีบทเรียน", "developed": "มีบทเรียนพัฒนา", "assessed": "มีบทเรียนประเมิน"}},
            "en": {"id": "Skill id", "group": "Group", "area": "Area", "imp": "Roadmap importance",
                   "imp_none": "No roadmap colour (added by TESA)", "origin": "Origin", "node": "Roadmap node",
                   "cov": "Status in the lesson library", "dev": "Lessons that develop this skill",
                   "ass": "Lessons that assess this skill", "roles": "Roles that use this skill",
                   "levels": "Proficiency levels", "none_yet": "No lesson yet",
                   "no_roles": "No role profile names this skill yet",
                   "col_lesson": "Lesson", "col_course": "Course", "col_to": "Develops to", "col_level": "Level",
                   "col_ev": "Evidence", "col_role": "Role", "col_rimp": "In this role", "col_min": "Minimum level",
                   "req": "Required (R)", "promoted": "raised from {x} on the map", "tesa_imp": "added by TESA",
                   "align": "For Open Badges 3.0 and CASE alignment", "roadmap": "See it on the skill roadmap",
                   "license": ("Skill map data is licensed CC BY-SA 4.0, adapted from the "
                               "[Embedded Systems Engineering Roadmap](https://github.com/m3y54m/Embedded-Engineering-Roadmap) "
                               "by Meysam Parvizi"),
                   "states": {"none": "No lesson yet", "developed": "Developed by a lesson", "assessed": "Assessed by a lesson"}},
        }
        course_title = {c.id: c.title for c in self.courses}
        for sid in self.skill_order:
            s = self.skills[sid]
            cov = self.coverage_state(sid)
            gid = s.get("group")
            g = self.groups.get(gid, {})
            area = areas.get(area_of_group.get(gid), {})
            imp = s.get("importance")
            for lang in LANGS:
                t = S[lang]
                name = pick({"th": s.get("th"), "en": s.get("en")}, lang, sid)
                imp_text = f"{imp} · {pick(importance.get(imp), lang)}" if imp else t["imp_none"]
                rows = [
                    (t["id"], f"<code>{esc(sid)}</code>"),
                    (t["area"], esc(pick(area, lang, area_of_group.get(gid) or ""))),
                    (t["group"], esc(pick(g, lang, gid or ""))),
                    (t["imp"], f'<span class="tok-imp tok-imp-{esc(imp or "none")}">{esc(imp_text)}</span>'),
                    (t["origin"], esc(pick(VOCAB["origin"].get(s.get("origin"), {"th": s.get("origin"), "en": s.get("origin")}), lang))),
                ]
                if s.get("eer_node"):
                    rows.append((t["node"], esc(s["eer_node"])))
                rows.append((t["cov"], f'<span class="tok-cov tok-cov-{cov["state"]}">{esc(t["states"][cov["state"]])}</span>'))
                meta = "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in rows)
                roadmap_href = self.cfg.base + ("/en" if lang == "en" else "") + f"/roadmap/#group-{gid}"
                lines = [f'<dl class="tok-skill-meta not-content">{meta}</dl>', "",
                         f"[{t['roadmap']}]({roadmap_href})", ""]
                dev = [e for e in self.coverage[sid] if e["mode"] == "develops"]
                ass = [e for e in self.coverage[sid] if e["mode"] == "assesses"]
                lines += [f"## {t['dev']}", ""]
                if dev:
                    lines += [f"| {t['col_lesson']} | {t['col_course']} | {t['col_to']} |", "|---|---|---|"]
                    for e in dev:
                        les = self.lessons[e["lesson"]]
                        lines.append(f"| [{md_cell(les.title[lang])}]({self.url(les.route, lang)}) | "
                                     f"{md_cell(pick(course_title.get(les.course), lang))} | "
                                     f"{md_cell(pick(self.level_name(e['level']), lang) if e['level'] else '')} |")
                else:
                    lines.append(t["none_yet"])
                lines += ["", f"## {t['ass']}", ""]
                if ass:
                    lines += [f"| {t['col_lesson']} | {t['col_level']} | {t['col_ev']} |", "|---|---|---|"]
                    for e in ass:
                        les = self.lessons[e["lesson"]]
                        ev = e.get("evidence") or ""
                        ev_link = self.evidence_url(les, ev, lang)
                        ev_md = f"[{md_cell(ev)}]({ev_link})" if ev_link else md_cell(ev)
                        lines.append(f"| [{md_cell(les.title[lang])}]({self.url(les.route, lang)}) | "
                                     f"{md_cell(pick(self.level_name(e['level']), lang) if e['level'] else '')} | {ev_md} |")
                else:
                    lines.append(t["none_yet"])
                lines += ["", f"## {t['roles']}", ""]
                if self.roles[sid]:
                    lines += [f"| {t['col_role']} | {t['col_min']} | {t['col_rimp']} |", "|---|---|---|"]
                    for r in self.roles[sid]:
                        lv = pick(self.level_name(r["level"]), lang) if r.get("level") else ""
                        pf = r.get("importance")
                        note = t["req"] + (" · " + t["promoted"].format(x=pf) if pf in ("Rec", "P") else "")
                        lines.append(f"| {md_cell(pick(r['title'], lang))} | {md_cell(lv)} | {md_cell(note)} |")
                else:
                    lines.append(t["no_roles"])
                lines += ["", f"## {t['levels']}", ""]
                for lv in self.levels.values():
                    bloom = f" · Bloom: {md_cell(lv.get('bloom'))}" if lv.get("bloom") else ""
                    lines.append(f"- **{esc(lv.get('code'))}** {md_cell(pick(lv, lang))}{bloom}")
                target_url = self.cfg.absolute(f"skills/{sid}", "th")
                alignment = {
                    "type": ["Alignment"],
                    "targetName": pick({"th": s.get("th"), "en": s.get("en")}, "en", sid),
                    "targetUrl": target_url,
                    "targetCode": sid,
                    "targetFramework": f"{pick(fw.get('title'), 'en')} {fw.get('version', '')}".strip(),
                    "targetType": "CFItem",
                }
                lines += ["", f"## {t['align']}", "", f"UUID: `{self.skill_uuid(sid)}`", "",
                          "```json", json.dumps(alignment, ensure_ascii=False, indent=2), "```", "",
                          t["license"], ""]
                front = {"slug": ("en/" if lang == "en" else "") + f"skills/{sid}", "editUrl": False,
                         "description": one_line(f"{sid} · {name} · {pick(g, lang, gid or '')}"),
                         "tqp": {"kind": "skill", "id": sid}}
                self.add_page(Page(f"skills/{sid}", lang, self.docs / ("en" if lang == "en" else "") / "skills" / f"{sid}.md",
                                   name, "\n".join(lines), front))

    def build_skills_index(self) -> None:
        T = {"th": ("ทักษะทั้งหมด", "รายการทักษะทั้ง {n} ข้อในแผนที่ทักษะ TESA จัดตามหมวดและกลุ่ม "
                    "ดูแบบภาพได้ที่ [แผนที่ทักษะ]({roadmap}) และดูว่าหลักสูตรใดครอบคลุมทักษะใดได้ที่ [ตารางความครอบคลุม]({coverage})",
                    ("ทักษะ", "รหัส", "ความสำคัญ", "สถานะบทเรียน"), {"none": "ยังไม่มี", "developed": "พัฒนา", "assessed": "ประเมิน"}),
             "en": ("All skills", "All {n} skills in the TESA skill map, by area and group. "
                    "See the [skill roadmap]({roadmap}) for the visual map and the [coverage matrix]({coverage}) "
                    "for which course covers which skill.",
                    ("Skill", "Id", "Importance", "Lessons"), {"none": "none", "developed": "developed", "assessed": "assessed"})}
        for lang in LANGS:
            title, intro, cols, states = T[lang]
            pre = self.cfg.base + ("/en" if lang == "en" else "")
            lines = [intro.format(n=len(self.skills), roadmap=f"{pre}/roadmap/", coverage=f"{pre}/coverage/"), ""]
            for area in self.areas:
                gids = [gid for gid, g in self.groups.items() if g.get("area") == area.get("id")]
                if not any(self.skills[s].get("group") in gids for s in self.skill_order):
                    continue
                lines += [f"## {pick(area, lang)}", ""]
                for gid in gids:
                    sids = [s for s in self.skill_order if self.skills[s].get("group") == gid]
                    if not sids:
                        continue
                    lines += [f"### {pick(self.groups[gid], lang)}", "", f"| {' | '.join(cols)} |", "|---|---|---|---|"]
                    for sid in sids:
                        s = self.skills[sid]
                        cov = self.coverage_state(sid)["state"]
                        lines.append(f"| [{md_cell(pick({'th': s.get('th'), 'en': s.get('en')}, lang))}]({self.url('skills/' + sid, lang)}) "
                                     f"| `{sid}` | {md_cell(s.get('importance') or '—')} | {states[cov]} |")
                    lines.append("")
            desc = (f"รายการทักษะทั้ง {len(self.skills)} ข้อในแผนที่ทักษะ TESA" if lang == "th"
                    else f"All {len(self.skills)} skills in the TESA skill map")
            front = {"slug": ("en/" if lang == "en" else "") + "skills", "editUrl": False, "description": desc}
            self.add_page(Page("skills", lang, self.docs / ("en" if lang == "en" else "") / "skills" / "index.md",
                               title, "\n".join(lines), front))

    # ------------------------------------------------------------------ catalog / pathways / home
    def course_by_id(self, cid: str):
        return next((c for c in self.courses if c.id == cid), None)

    def course_href(self, cid: str, lang: str):
        c = self.course_by_id(cid)
        if c and c.has_page:
            return self.url(c.route, lang)
        cat = next((x for x in self.catalog if x.get("id") == cid), None)
        ext = (cat or {}).get("external") or {}
        return ext.get("site") or ext.get("repo")

    def course_meta_line(self, cat: dict, course, lang: str) -> str:
        m = course.meta if course else {}
        bits = []
        lvl = m.get("level") or cat.get("level")
        if lvl:
            bits.append(pick(self.level_name(str(lvl)), lang))
        st = m.get("status") or cat.get("status")
        if st:
            bits.append(pick(VOCAB["status"].get(st, {"th": st, "en": st}), lang))
        if m.get("hours"):
            bits.append(f"{m['hours']} {'ชั่วโมง' if lang == 'th' else 'hours'}")
        if course:
            n = sum(len(mod.lessons) for mod in course.modules)
            if n:
                bits.append(f"{n} {'บทเรียน' if lang == 'th' else 'lessons'}")
        hw = self.hardware(m.get("hardware"))
        hw_bits = (["BENTO Emulator"] if hw["emulator"] else []) + [pick(b["label"], lang) for b in hw["boards"]]
        if hw_bits:
            bits.append(", ".join(hw_bits))
        return " · ".join(bits)

    def course_card(self, cat: dict, c, lang: str) -> str:
        """A course card: cover image (16:9, decorative), title link stretched over the card (one tab stop),
        level/time/lessons/hardware chips, and a 3-line summary. Covers are copied to public/covers/."""
        m = c.meta or {}
        href = self.course_href(c.id, lang)
        img = ""
        cover = m.get("cover") if isinstance(m.get("cover"), dict) else None
        if cover and cover.get("image"):
            src = self.repo / "courses" / c.id / str(cover["image"])
            if src.is_file():
                ext = src.suffix.lower()
                dst = self.site_dir / "public" / "covers" / f"{c.id}{ext}"
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src, dst)
                pos = esc(str(cover.get("position") or "center"))
                img = (f'<img class="tok-card-img" src="{self.cfg.base}/covers/{c.id}{ext}" alt="" loading="lazy" '
                       f'decoding="async" width="960" height="540" style="object-position:{pos}">')
            else:
                self.p.warn(f"courses/{c.id}/course.yaml", f"cover image {cover['image']} not found")
        chips = []
        lvl = str(m.get("level") or cat.get("level") or "")
        if lvl:
            chips.append(f'<li class="tok-chip tok-lvl tok-lvl-{esc(lvl.lower())}">{esc(pick(self.level_name(lvl), lang))}</li>')
        if m.get("hours"):
            chips.append(f'<li class="tok-chip">{m["hours"]} {"ชม." if lang == "th" else "h"}</li>')
        n = sum(len(mod.lessons) for mod in c.modules)
        if n:
            chips.append(f'<li class="tok-chip">{n} {"บทเรียน" if lang == "th" else "lessons"}</li>')
        hw = self.hardware(m.get("hardware"))
        hw_bits = (["Emulator"] if hw["emulator"] else []) + [pick(b["label"], lang) for b in hw["boards"]]
        if hw_bits:
            chips.append(f'<li class="tok-chip tok-chip-hw">{esc(" · ".join(hw_bits))}</li>')
        flags = ""
        if cat.get("featured"):
            flags += f'<span class="tok-card-flag">{"หลักสูตรหลัก" if lang == "th" else "Core course"}</span>'
        if isinstance(cat.get("notice"), dict):
            flags += f'<span class="tok-card-notice">{esc(pick(cat["notice"].get("label"), lang))}</span>'
        st = str(m.get("status") or cat.get("status") or "")
        if st:
            flags += f'<span class="tok-card-status">{esc(pick(VOCAB["status"].get(st, {"th": st, "en": st}), lang))}</span>'
        summary = pick(c.summary, lang)
        title = esc(c.title[lang])
        link = f'<a href="{esc(href)}">{title}</a>' if href else title
        return (f'<article class="tok-card{" tok-card-featured" if cat.get("featured") else ""}">'
                f'<div class="tok-card-text"><p class="tok-card-title" role="heading" aria-level="3">{link}</p>'
                f'<ul class="tok-chips">{"".join(chips)}</ul>'
                + (f'<p class="tok-card-body">{esc(summary)}</p>' if summary else "")
                + f'</div>{img}{flags}</article>')

    def build_catalog(self) -> None:
        T = {"th": ("หลักสูตรทั้งหมด",
                    "ทุกหลักสูตรเรียนได้ฟรี เรียงจากพื้นฐานไปถึงงานเฉพาะทาง หลักสูตรที่ยังเป็นร่าง (pre-alpha, alpha) "
                    "เปิดให้ดูโครงก่อน เนื้อหาจะทยอยเติม ถ้ายังไม่แน่ใจว่าจะเริ่มตรงไหน ดู[เส้นทางการเรียนรู้]({pathways})",
                    "หลักสูตรภายนอกที่เชื่อมกับคลังนี้", "ยังไม่มีหน้าหลักสูตร", "ต้นฉบับ", "สัญญาอนุญาต"),
             "en": ("All courses",
                    "Every course is free. They run from the basics to specialist work. Draft courses (pre-alpha, alpha) "
                    "show their outline first and fill in over time. Not sure where to start? See the [learning pathways]({pathways}).",
                    "External courses linked to this library", "No course page yet", "Source", "Licence")}
        for lang in LANGS:
            title, intro, ext_h, no_page, src_l, lic_l = T[lang]
            pre = self.cfg.base + ("/en" if lang == "en" else "")
            lines = [intro.format(pathways=f"{pre}/pathways/"), ""]
            externals = []
            by_level: dict = {}
            for cat in self.catalog:
                if not cat.get("in_tree"):
                    externals.append(cat)
                    continue
                course = self.course_by_id(cat["id"])
                if not course:
                    continue
                lvl = str(course.meta.get("level") or cat.get("level") or "")
                by_level.setdefault(lvl, []).append(self.course_card(cat, course, lang))
            for lvl in sorted(by_level):
                lines += [f"## {pick(self.level_name(lvl), lang) if lvl else ('อื่น ๆ' if lang == 'th' else 'Other')}", "",
                          f'<div class="tok-cards not-content">{"".join(by_level[lvl])}</div>', ""]
            if externals:
                lines += [f"## {ext_h}", ""]
                for cat in externals:
                    ext = cat.get("external") or {}
                    ctitle = pick(cat.get("title"), lang, cat["id"])
                    link = ext.get("site") or ext.get("repo")
                    lines.append(f"### [{ctitle}]({link})" if link else f"### {ctitle}")
                    lines += ["", f'<p class="tok-meta">{esc(self.course_meta_line(cat, None, lang))}</p>', ""]
                    if ext.get("repo"):
                        ref = str(ext.get("ref") or "")
                        lines.append(f"{src_l}: [{ext['repo']}]({ext['repo']}{'/tree/' + ref if ref else ''})"
                                     + (f" @ `{ref[:12]}`" if ref else ""))
                    lic = ext.get("license") or {}
                    if lic:
                        lines += ["", f"{lic_l}: " + ", ".join(f"{k} {v}" for k, v in lic.items())]
                    lines.append("")
            self.add_page(Page("catalog", lang, self.out_path("catalog", lang), title, "\n".join(lines),
                               {"slug": ("en/" if lang == "en" else "") + "catalog", "editUrl": self.cfg.gh_edit("catalog/courses.yaml"),
                                "description": title + " · " + self.cfg.title}))

    def build_pathways(self) -> None:
        T = {"th": ("เส้นทางการเรียนรู้", "เลือกเส้นทางที่ตรงกับเป้าหมายของคุณ แต่ละเส้นทางบอกว่าเริ่มจากหลักสูตรใด ต่อด้วยอะไร และไปจบที่ไหน",
                    "กำลังจัดทำเส้นทางการเรียนรู้ ระหว่างนี้เริ่มจาก[หลักสูตรทั้งหมด]({catalog})ได้เลย",
                    {"audience": "เหมาะกับ", "hours": "เวลา (ส่วนบังคับ)", "hardware": "อุปกรณ์", "outcome": "เมื่อจบเส้นทาง", "badge": "Badge", "level": "ระดับ"}),
             "en": ("Learning pathways", "Pick the pathway that matches your goal. Each one says which course to start with, what comes next and where it leads.",
                    "The pathways are being written. Meanwhile, start from [all courses]({catalog}).",
                    {"audience": "For", "hours": "Time (required steps)", "hardware": "Hardware", "outcome": "At the end", "badge": "Badge", "level": "Level"})}
        data = self.tracks
        tracks = data.get("tracks") if isinstance(data, dict) else data
        known = {"id", "title", "name", "summary", "description", "audience", "hours", "size", "hardware", "outcome",
                 "destination", "next", "exit", "badge", "steps", "courses", "sequence", "path", "level", "note"}
        unknown_keys: set = set()
        for lang in LANGS:
            title, intro, pending, labels = T[lang]
            pre = self.cfg.base + ("/en" if lang == "en" else "")
            lines = [intro, ""]
            if not isinstance(tracks, list) or not tracks:
                lines.append(pending.format(catalog=f"{pre}/catalog/"))
            else:
                for tr in tracks:
                    if not isinstance(tr, dict):
                        continue
                    unknown_keys |= set(tr) - known
                    anchor = slug_segment(str(tr.get("id") or ""))
                    lines += [f"## {pick(tr.get('title') or tr.get('name') or tr.get('id'), lang)}", ""]
                    summ = tr.get("summary") or tr.get("description")
                    if summ:
                        lines += [one_line(pick(summ, lang)), ""]
                    facts = []
                    for key in ("audience", "level", "hours", "size", "hardware", "badge", "exit", "outcome", "destination", "next"):
                        v = tr.get(key)
                        if v in (None, "", []):
                            continue
                        lab = {"size": "hours", "level": "hours", "destination": "outcome", "next": "outcome", "exit": "outcome"}.get(key, key)
                        if key == "level":
                            text, lab = pick(self.level_name(str(v)), lang), "level"
                        elif key == "audience":
                            vals = v if isinstance(v, list) else [v]
                            text = ", ".join(pick(VOCAB["audience"].get(x, x), lang) if isinstance(x, str) else pick(x, lang) for x in vals)
                        elif key == "hours" and isinstance(v, (int, float)):
                            text = f"{v:g} {'ชั่วโมง' if lang == 'th' else 'hours'}"
                        elif key == "hardware" and isinstance(v, dict) and not ({"th", "en"} & set(v)):
                            hw = self.hardware(v)
                            text = ", ".join((["BENTO Emulator"] if hw["emulator"] else []) + [pick(b["label"], lang) for b in hw["boards"]])
                        elif isinstance(v, list):
                            text = ", ".join(pick(x, lang) for x in v)
                        else:
                            text = one_line(pick(v, lang))
                        facts.append(f"- **{labels.get(lab, lab)}:** {text}")
                    steps = tr.get("steps") or tr.get("courses") or tr.get("sequence") or tr.get("path") or []
                    step_lines = [f"{i}. {self.step_text(st, lang)}" for i, st in enumerate(steps if isinstance(steps, list) else [], 1)]
                    lines += step_lines + ([""] if step_lines else [])
                    lines += facts + ([""] if facts else [])
            self.add_page(Page("pathways", lang, self.out_path("pathways", lang), title, "\n".join(lines),
                               {"slug": ("en/" if lang == "en" else "") + "pathways",
                                "editUrl": self.cfg.gh_edit("catalog/tracks.yaml") if data is not None else False,
                                "description": intro}))
        if unknown_keys:
            self.p.warn("catalog/tracks.yaml", f"keys not shown on the pathways page: {sorted(unknown_keys)}")

    def step_text(self, st, lang: str) -> str:
        def course_ref(cid: str) -> str:
            c = self.course_by_id(cid)
            cat = next((c2 for c2 in self.catalog if c2.get("id") == cid), None)
            if not c and not cat:
                self.p.warn("catalog/tracks.yaml", f"step names unknown course {cid}")
                return cid
            name = pick(c.title if c else cat.get("title"), lang, cid)
            href = self.course_href(cid, lang)
            return f"[{name}]({href})" if href else name

        def module_ref(cid: str, mid: str) -> str:
            c = self.course_by_id(cid)
            m = next((m for m in (c.modules if c else []) if m.id == mid), None)
            if not m:
                return mid
            return f"[{m.title[lang]}]({self.url(m.route, lang)})" if m.has_page else m.title[lang]

        def lesson_ref(lid: str) -> str:
            les = self.lessons.get(lid)
            return f"[{les.title[lang]}]({self.url(les.route, lang)})" if les else lid

        if isinstance(st, str):
            return course_ref(st) if (self.course_by_id(st) or any(c.get("id") == st for c in self.catalog)) else lesson_ref(st)
        if not isinstance(st, dict):
            return str(st)
        cid = st.get("course")
        head = course_ref(str(cid)) if cid else pick(st.get("title"), lang)
        parts = []
        if cid and isinstance(st.get("modules"), list):
            parts.append(", ".join(module_ref(str(cid), str(m)) for m in st["modules"]))
        if isinstance(st.get("lessons"), list):
            parts.append(", ".join(lesson_ref(str(x)) for x in st["lessons"]))
        text = head + (f" ({'; '.join(parts)})" if parts else "")
        note = st.get("note") or st.get("summary")
        if note:
            text += f" — {one_line(pick(note, lang))}"
        return text

    def build_home(self) -> None:
        T = {
            "th": {
                "tagline": "คอร์สเปิดด้านระบบสมองกลฝังตัว AIoT และ Edge AI เรียนทีละบท มีสไลด์ ตัวอย่างโค้ด และแบบฝึกครบในที่เดียว",
                "a1": "ดูหลักสูตรทั้งหมด", "a2": "เลือกเส้นทางการเรียนรู้", "a3": "แผนที่ทักษะ",
                "who_h": "เรียนได้ทุกคน",
                "who": ("บุคคลทั่วไปเริ่มจากหลักสูตร Explorer ที่ลองได้ใน BENTO Emulator โดยไม่ต้องมีบอร์ด "
                        "นักศึกษาและนักพัฒนาเรียนต่อถึงเฟิร์มแวร์ภาษา C, Secure IoT และ Edge AI บน PSoC Edge "
                        "ผู้ประกอบการมีหลักสูตรที่ไม่ต้องเขียนโค้ด และผู้สอนมีชุดสำหรับนำไปสอนต่อ"),
                "courses_h": "หลักสูตรในคลังนี้",
                "tqp_h": "ทุกบทเรียนผูกกับแผนที่ทักษะ",
                "tqp": ("แต่ละบทเรียนบอกไว้ชัดว่าฝึกทักษะใดและไปถึงระดับไหน ตามแผนที่ทักษะ TESA ที่ต่อยอดจาก "
                        "Embedded Systems Engineering Roadmap ข้อมูลชุดนี้เป็นฐานของ TESA Qualification Program (TQP) "
                        "โครงการร่วมระหว่าง TESA และ Infineon"),
                "reuse_h": "นำไปใช้ต่อได้ ขอให้อ้างอิง TESA",
                "reuse": (f"เนื้อหาเผยแพร่ภายใต้ {self.cfg.credit['licence']} ใช้ต่อในงานที่ไม่ใช่เพื่อการค้าได้ "
                          "และมหาวิทยาลัยนำไปสอนได้ตามคำอนุญาตเพิ่ม ส่วนโค้ดภายใต้ Apache-2.0 หรือ MIT ตามที่ระบุในแต่ละหลักสูตร "
                          "อ้างอิงสมาคมสมองกลฝังตัวไทย (TESA) ทุกครั้ง ดูรูปแบบการอ้างอิงและคำอนุญาตเพิ่มได้ที่"),
                "reuse_link": "วิธีอ้างอิง TESA",
                "lessons": "บทเรียน",
            },
            "en": {
                "tagline": "Open courses on embedded systems, AIoT and Edge AI. Learn lesson by lesson, with slides, example code and practice in one place.",
                "a1": "Browse all courses", "a2": "Choose a pathway", "a3": "Skill roadmap",
                "who_h": "Open to everyone",
                "who": ("Newcomers start with the Explorer course in the BENTO Emulator, no board needed. "
                        "Students and developers continue to C firmware, Secure IoT and Edge AI on PSoC Edge. "
                        "Entrepreneurs have a no-code course, and educators have a kit for teaching."),
                "courses_h": "Courses in this library",
                "tqp_h": "Every lesson maps to the skill map",
                "tqp": ("Each lesson states which skills it trains and to what level, on the TESA skill map adapted from the "
                        "Embedded Systems Engineering Roadmap. The same data underpins the TESA Qualification Program (TQP), "
                        "a joint TESA and Infineon programme."),
                "reuse_h": "Reuse it, and credit TESA",
                "reuse": (f"Content is licensed {self.cfg.credit['licence']}: reuse it non-commercially, and universities may teach "
                          "with it under an additional permission. Code is Apache-2.0 or MIT as each course states. "
                          "Credit the Thai Embedded Systems Association (TESA) every time. The wording and the permissions are on"),
                "reuse_link": "How to cite TESA",
                "lessons": "lessons",
            },
        }
        for lang in LANGS:
            t = T[lang]
            pre = self.cfg.base + ("/en" if lang == "en" else "")
            cards = []
            for cat in self.catalog:
                if not cat.get("in_tree"):
                    continue
                c = self.course_by_id(cat["id"])
                if not c:
                    continue
                cards.append(self.course_card(cat, c, lang))
            lines = [
                f"## {t['who_h']}", "", t["who"], "",
                f"## {t['courses_h']}", "",
                f'<div class="tok-cards not-content">{"".join(cards)}</div>' if cards else f"[{t['a1']}]({pre}/catalog/)", "",
                f"## {t['tqp_h']}", "", t["tqp"], "",
                f"[{t['a3']}]({pre}/roadmap/)", "",
                f"## {t['reuse_h']}", "", f"{t['reuse']} [{t['reuse_link']}]({pre}/attribution/)", "",
            ]
            front = {
                "template": "splash",
                "editUrl": False,
                "description": pick(self.cfg.description, lang),
                "hero": {
                    "title": self.cfg.title,
                    "tagline": t["tagline"],
                    "actions": [
                        {"text": t["a1"], "link": f"{pre}/catalog/", "icon": "right-arrow"},
                        {"text": t["a2"], "link": f"{pre}/pathways/", "variant": "secondary"},
                        {"text": t["a3"], "link": f"{pre}/roadmap/", "variant": "minimal"},
                    ],
                },
            }
            self.add_page(Page("", lang, self.out_path("", lang), self.cfg.title, "\n".join(lines), front))

    # ------------------------------------------------------------------ generated JSON
    def site_data(self) -> dict:
        importance = self.skillmap.get("importance") or {}
        in_tree = [c for c in self.courses]
        lesson_course = {l.id: l.course for l in self.lessons.values()}
        skills = {}
        matrix = {}
        for sid in self.skill_order:
            s = self.skills[sid]
            cov = self.coverage_state(sid)
            row = {}
            for e in self.coverage[sid]:
                cid = lesson_course.get(e["lesson"])
                cell = row.setdefault(cid, {"dev": None, "ass": None, "n": 0})
                cell["n"] += 1
                key = "dev" if e["mode"] == "develops" else "ass"
                if e["level"] is not None and (cell[key] is None or e["level"] > cell[key]):
                    cell[key] = e["level"]
                if e["level"] is None and cell[key] is None:
                    cell[key] = 0
            matrix[sid] = row
            skills[sid] = {"id": sid, "th": s.get("th") or sid, "en": s.get("en") or sid, "group": s.get("group"),
                           "importance": s.get("importance"), "origin": s.get("origin"),
                           "coverage": cov["state"], "dev_max": cov["dev_max"], "ass_max": cov["ass_max"],
                           "n_dev": cov["n_dev"], "n_ass": cov["n_ass"], "courses": sorted(k for k in row if k),
                           "deprecated": bool(s.get("deprecated"))}
        areas = []
        for a in self.areas:
            groups = []
            for gid, g in self.groups.items():
                if g.get("area") != a.get("id"):
                    continue
                sids = [x for x in self.skill_order if self.skills[x].get("group") == gid]
                groups.append({"id": gid, "th": g.get("th") or gid, "en": g.get("en") or gid, "skills": sids})
            areas.append({"id": a.get("id"), "th": a.get("th"), "en": a.get("en"), "groups": groups})
        totals = {"skills": len(skills), "lessons": len(self.lessons), "courses_in_tree": len(in_tree),
                  "none": 0, "developed": 0, "assessed": 0, "by_importance": {}}
        for sk in skills.values():
            totals[sk["coverage"]] += 1
            key = sk["importance"] or "none"
            b = totals["by_importance"].setdefault(key, {"total": 0, "covered": 0})
            b["total"] += 1
            b["covered"] += 1 if sk["coverage"] != "none" else 0
        imp = {k: {"th": pick(v, "th"), "en": pick(v, "en")} for k, v in importance.items()}
        imp["none"] = {"th": "TESA เพิ่ม", "en": "Added by TESA"}
        return {
            "generated": {"ref": self.ref, "at": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")},
            "framework": self.skillmap.get("framework") or {},
            "levels": [{"id": k, "code": v.get("code"), "th": v.get("th"), "en": v.get("en")} for k, v in self.levels.items()],
            "importance": imp,
            "areas": areas,
            "skills": skills,
            "courses": [{"id": c.id, "short": c.cat.get("short") or c.meta.get("short") or c.id, "title": c.title,
                         "route": c.route if c.has_page else None,
                         "lessons": sum(len(m.lessons) for m in c.modules)} for c in in_tree],
            "matrix": matrix,
            "totals": totals,
        }

    def sidebar(self) -> list:
        th_routes = {p.route for p in self.pages if p.lang == "th"}

        def slug_item(route, label=None, en=None):
            item = {"slug": route if route else "index"}
            if label:
                item["label"] = label
                if en:
                    item["translations"] = {"en": en}
            return item

        start = [slug_item("", "หน้าแรก", "Home"), slug_item("catalog"), slug_item("pathways")]
        skills = [
            {"link": "/roadmap/", "label": "แผนที่ทักษะ (Roadmap)", "translations": {"en": "Skill roadmap"}},
            {"link": "/coverage/", "label": "ตารางความครอบคลุม", "translations": {"en": "Coverage matrix"}},
            slug_item("skills"),
        ]
        courses = []
        for c in self.courses:
            items = []
            if c.route in th_routes:
                items.append(slug_item(c.route, "ภาพรวมหลักสูตร", "Course overview"))
            for m in c.modules:
                sub = []
                if m.route in th_routes:
                    sub.append(slug_item(m.route, "ภาพรวมโมดูล", "Module overview"))
                # Label both languages from the front matter, so an untranslated lesson still has an
                # English label in the English sidebar (its page is Starlight's TH fallback).
                sub += [slug_item(l.route, l.title["th"], l.title["en"]) for l in m.lessons if l.route in th_routes]
                if sub:
                    items.append({"label": m.title["th"], "translations": {"en": m.title["en"]}, "collapsed": True, "items": sub})
            if not items:
                continue
            nav = c.cat.get("nav") if isinstance(c.cat.get("nav"), dict) else None
            label = {"th": pick(nav, "th", c.title["th"]), "en": pick(nav, "en", c.title["en"])} if nav else c.title
            group = {"label": label["th"], "translations": {"en": label["en"]}, "collapsed": True, "items": items}
            # Only drafts get a badge: a badge on every course was noise in a dense list.
            st = str(c.meta.get("status") or c.cat.get("status") or "")
            if st == "pre-alpha":
                group["badge"] = {"text": "ร่าง", "variant": "caution"}
            notice = c.cat.get("notice") if isinstance(c.cat.get("notice"), dict) else None
            if notice and isinstance(notice.get("label"), dict):
                # Starlight badges take per-language text keyed by the locale's lang (root = th).
                group["badge"] = {"text": {"th": notice["label"].get("th"), "en": notice["label"].get("en")},
                                  "variant": "caution"}
            courses.append(group)
        about = [slug_item("attribution")] + [slug_item(r) for r, _ in self.about if r in th_routes]
        bar = [
            {"label": "เริ่มต้น", "translations": {"en": "Start here"}, "items": start},
            {"label": "แผนที่ทักษะ", "translations": {"en": "Skill map"}, "items": skills},
        ]
        if courses:
            bar.append({"label": "หลักสูตร", "translations": {"en": "Courses"}, "items": courses})
        bar.append({"label": "เกี่ยวกับ", "translations": {"en": "About"}, "items": about})
        # Every slug must exist as a TH page or Starlight stops the build; check it here with a clear message.
        def check(items):
            for it in items:
                if "slug" in it and (it["slug"] if it["slug"] != "index" else "") not in th_routes:
                    self.p.error("site/src/generated/sidebar.json", f"sidebar slug {it['slug']} has no page")
                if "items" in it:
                    check(it["items"])
        check(bar)
        return bar

    # ------------------------------------------------------------------ write
    def write(self) -> dict:
        safe_rmtree(self.docs, ("site/src/content/docs", "src/content/docs"))
        safe_rmtree(self.gen, ("site/src/generated", "src/generated"))
        safe_rmtree(self.public_assets, ("site/public/content-assets", "public/content-assets"))
        # Build pages that copy images first (the rmtree above must not delete them afterwards).
        self.pages.clear()
        self.ctx.copied.clear()
        self.build_course_pages()
        self.build_root_docs()
        self.build_skill_pages()
        self.build_skills_index()
        self.build_catalog()
        self.build_pathways()
        self.build_home()
        seen = {}
        for pg in self.pages:
            key = (pg.lang, pg.route)
            if key in seen:
                self.p.error(pg.src or str(pg.out), f"duplicate page {pg.lang}:{pg.route} (also {seen[key]})")
            seen[key] = pg.src or str(pg.out)
            front = {"title": pg.title}
            if pg.route and "slug" not in pg.front:
                front["slug"] = ("en/" if pg.lang == "en" else "") + pg.route
            front.update(pg.front)
            fm_text = yaml.safe_dump(front, allow_unicode=True, sort_keys=False, width=4096, default_flow_style=False)
            pg.out.parent.mkdir(parents=True, exist_ok=True)
            pg.out.write_text(f"---\n{fm_text}---\n\n{pg.body}", encoding="utf-8")
        self.gen.mkdir(parents=True, exist_ok=True)
        site_cfg = {
            "site": {"origin": self.cfg.origin, "base": self.cfg.base or "/", "title": self.cfg.title,
                     "description": self.cfg.description},
            "repo": {"url": self.cfg.repo_url, "branch": self.cfg.branch, "ref": self.ref},
            "ide": {"origin": self.cfg.ide_origin},
            "credit": self.cfg.credit,
        }
        (self.gen / "site-config.json").write_text(json.dumps(site_cfg, ensure_ascii=False, indent=2), encoding="utf-8")
        sidebar = self.sidebar()
        (self.gen / "sidebar.json").write_text(json.dumps(sidebar, ensure_ascii=False, indent=2), encoding="utf-8")
        data = self.site_data()
        (self.gen / "site-data.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        return data

    def cross_check_exports(self, data: dict) -> None:
        """Compare with tools/export.py output (site/src/data/*.json) when it exists: two readings of one truth."""
        ddir = self.site_dir / "src" / "data"
        sk = ddir / "skills.json"
        if sk.is_file():
            try:
                exp = json.loads(sk.read_text(encoding="utf-8"))
                items = exp.get("skills") if isinstance(exp, dict) else exp
                ids = {x.get("id") for x in items or [] if isinstance(x, dict)}
                if ids and ids != set(self.skills):
                    self.p.warn("site/src/data/skills.json", f"export has {len(ids)} skills, skills.yaml has {len(self.skills)}")
                for x in items or []:
                    if isinstance(x, dict) and x.get("uuid") and x.get("id") in self.skills and x["uuid"] != self.skill_uuid(x["id"]):
                        self.p.warn("site/src/data/skills.json", f"uuid for {x['id']} differs from the site's ({x['uuid']})")
                        break
            except (ValueError, AttributeError) as exc:
                self.p.warn("site/src/data/skills.json", f"could not read: {exc}")
        cv = ddir / "coverage.json"
        if cv.is_file():
            try:
                exp = json.loads(cv.read_text(encoding="utf-8"))
                per = exp.get("skills") if isinstance(exp, dict) and isinstance(exp.get("skills"), dict) else exp
                if isinstance(per, dict):
                    diff = []
                    for sid, entries in per.items():
                        if sid not in self.coverage or not isinstance(entries, list):
                            continue
                        theirs = sorted({str(e.get("lesson") or e.get("lesson_id") or e.get("id")) for e in entries if isinstance(e, dict)})
                        ours = sorted({e["lesson"] for e in self.coverage[sid]})
                        if theirs != ours:
                            diff.append(sid)
                    if diff:
                        self.p.warn("site/src/data/coverage.json", f"lesson sets differ from the site's for {len(diff)} skills, e.g. {diff[:5]}")
            except (ValueError, AttributeError) as exc:
                self.p.warn("site/src/data/coverage.json", f"could not read: {exc}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", type=Path, default=DEFAULT_REPO, help="repository root (default: two levels above this script)")
    ap.add_argument("--site-dir", type=Path, default=None, help="Astro project dir to write into (default: <repo>/site)")
    ap.add_argument("--ref", default=None, help="commit for GitHub code links (default: $GITHUB_SHA, else repo.branch)")
    ap.add_argument("--strict", action="store_true", help="exit 1 on any error (CI uses this)")
    args = ap.parse_args()

    repo = args.repo.resolve()
    site_dir = (args.site_dir or (repo / "site")).resolve()
    problems = Problems()
    b = Builder(repo, site_dir, "", problems)
    b.ref = args.ref or os.environ.get("GITHUB_SHA") or b.cfg.branch
    b.ctx.ref = b.ref
    print(f"==> [sync] repo={repo}")
    print(f"==> [sync] site={site_dir}  base={b.cfg.base or '/'}  ref={b.ref}")
    b.load_skills()
    b.load_roles()
    b.load_catalog()
    b.discover_courses()
    b.discover_root_docs()
    data = b.write()
    b.cross_check_exports(data)
    by_lang = {lang: sum(1 for p in b.pages if p.lang == lang) for lang in LANGS}
    t = data["totals"]
    print(f"==> [sync] pages: th={by_lang['th']} en={by_lang['en']}  courses={len(b.courses)}  lessons={len(b.lessons)}")
    print(f"==> [sync] skills={t['skills']}  none={t['none']} developed={t['developed']} assessed={t['assessed']}")
    print(f"==> [sync] links rewritten={b.ctx.stats['links']} images={b.ctx.stats['images']} "
          f"to-github={b.ctx.stats['github']} missing={b.ctx.stats['missing']}")
    if problems.items:
        print(f"==> [sync] {len(problems.errors)} error(s), {len(problems.warnings)} warning(s):")
        problems.report(sys.stdout)
    if args.strict and problems.errors:
        print("==> [sync] FAILED (--strict): fix the errors above; they are content problems, not site bugs.")
        return 1
    print("==> [sync] done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
