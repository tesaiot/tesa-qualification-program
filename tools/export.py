#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: Apache-2.0
"""Export the skill map, courses and coverage as JSON for the site (BUILD_SPEC §8).

    python3 tools/export.py --out site/src/data

Writes:
  skills.json    framework, levels, importance, areas, groups, skills (+ uuid, url), roles
  courses.json   catalog + every in-tree course.yaml + modules + lessons (front matter, path), tracks
  coverage.json  per skill: [{lesson, course, mode, level (+ to)}]; per course totals; overall totals
  case.json      a CASE 1.1-shaped CFPackage: CFDocument, CFItems (Group, Skill), CFAssociations
                 (isChildOf: skill -> group, group -> document)

A skill's uuid is uuid5(NAMESPACE_URL, f"{origin}{base}/skills/{id}/") with origin/base read from
site.config.yaml (a warning is printed if the file is missing and the policy fallback is used).
Output is deterministic: the same tree gives the same bytes. Timestamps come from
SOURCE_DATE_EPOCH if set, otherwise the last git commit touching skills/skills.yaml, otherwise
the file's modification time.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import uuid
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (REPO_ROOT, eprint, iter_files, load_policy, load_site_config,  # noqa: E402
                     load_yaml, parse_yaml, split_front_matter, read_text)

MOD_DIR = re.compile(r"^m([0-9]{2})-[a-z0-9]+(?:-[a-z0-9]+)*$")
LESSON_DIR = re.compile(r"^l([0-9]{2})-[a-z0-9]+(?:-[a-z0-9]+)*$")
CODE_DIRS = ("examples", "practice", "solution")


def _load(path: Path, what: str, required: bool = True) -> Any:
    if not path.is_file():
        if required:
            raise SystemExit(f"export: {what} is missing ({path})")
        return None
    doc = load_yaml(path)
    if doc.error:
        raise SystemExit(f"export: {path}: {doc.error} (run tools/validate.py)")
    return doc.data


def skill_url(site, sid: str) -> str:
    return f"{site.site_url}/skills/{sid}/"


def skill_uuid(site, sid: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, skill_url(site, sid)))


def _timestamp(root: Path) -> str:
    sde = os.environ.get("SOURCE_DATE_EPOCH")
    if sde and sde.isdigit():
        t = dt.datetime.fromtimestamp(int(sde), dt.timezone.utc)
    else:
        t = None
        try:
            out = subprocess.run(["git", "-C", str(root), "log", "-1", "--format=%ct", "--",
                                  "skills/skills.yaml"], capture_output=True, text=True, timeout=10)
            if out.returncode == 0 and out.stdout.strip().isdigit():
                t = dt.datetime.fromtimestamp(int(out.stdout.strip()), dt.timezone.utc)
        except (OSError, subprocess.SubprocessError):
            pass
        if t is None:
            t = dt.datetime.fromtimestamp(int((root / "skills" / "skills.yaml").stat().st_mtime),
                                          dt.timezone.utc)
    return t.strftime("%Y-%m-%dT%H:%M:%S+00:00")


# --------------------------------------------------------------------------- builders
def build_skills(root: Path, site, skills_doc: dict) -> dict:
    roles = []
    rdir = root / "skills" / "roles"
    if rdir.is_dir():
        for p in sorted(rdir.glob("*.y*ml")):
            data = _load(p, str(p), required=False)
            if isinstance(data, dict):
                roles.append(dict(data, path=p.relative_to(root).as_posix()))
    skills = []
    for s in skills_doc.get("skills") or []:
        if isinstance(s, dict) and isinstance(s.get("id"), str):
            skills.append(dict(s, uuid=skill_uuid(site, s["id"]), url=skill_url(site, s["id"])))
    return {
        "generated_by": "tools/export.py",
        "site": {"origin": site.origin, "base": site.base},
        "framework": skills_doc.get("framework"),
        "levels": skills_doc.get("levels") or [],
        "importance": skills_doc.get("importance") or {},
        "areas": skills_doc.get("areas") or [],
        "groups": skills_doc.get("groups") or [],
        "skills": skills,
        "roles": roles,
    }


def _files_under(root: Path, ldir: Path, sub: str) -> list[str]:
    d = ldir / sub
    if not d.is_dir():
        return []
    return [f"{sub}/{r}" for r in iter_files(d, ())]


def _front_matter(path: Path) -> dict | None:
    text = read_text(path)
    if text is None:
        return None
    fm = split_front_matter(text)
    if fm.text is None:
        return None
    doc = parse_yaml(fm.text)
    if doc.error or not isinstance(doc.data, dict):
        eprint(f"export: warning: {path}: unreadable front matter ({doc.error}); lesson skipped")
        return None
    return doc.data


def build_courses(root: Path, site, catalog: dict, tracks: Any) -> dict:
    courses = []
    for entry in catalog.get("courses") or []:
        if not isinstance(entry, dict) or not entry.get("in_tree"):
            continue
        cid = entry.get("id")
        cdir = root / "courses" / str(cid)
        cyaml = cdir / "course.yaml"
        if not cyaml.is_file():
            eprint(f"export: warning: courses/{cid}/course.yaml is missing; course skipped")
            continue
        course = _load(cyaml, str(cyaml))
        if not isinstance(course, dict):
            continue
        modules = []
        for m in course.get("modules") or []:
            if not isinstance(m, dict) or not isinstance(m.get("id"), str):
                continue
            mdir = cdir / m["id"]
            mm = MOD_DIR.match(m["id"])
            lessons = []
            if mdir.is_dir():
                for ld in sorted(p for p in mdir.iterdir() if p.is_dir() and LESSON_DIR.match(p.name)):
                    fm = _front_matter(ld / "README.md")
                    if fm is None:
                        continue
                    en = ld / "README.en.md"
                    fm_en = _front_matter(en) if en.is_file() else None
                    lrel = ld.relative_to(root).as_posix()
                    files = {k: _files_under(root, ld, k) for k in CODE_DIRS}
                    for name in ("slides.md", "lab.md", "quiz.yaml", "instructor-notes.md"):
                        files[name.split(".")[0].replace("-", "_")] = name if (ld / name).is_file() else None
                    files["resources"] = _files_under(root, ld, "resources")
                    lessons.append(dict(fm,
                                        course=cid, module=m["id"],
                                        number=int(LESSON_DIR.match(ld.name).group(1)),
                                        folder=ld.name, path=lrel, readme=f"{lrel}/README.md",
                                        readme_en=f"{lrel}/README.en.md" if en.is_file() else None,
                                        en=fm_en, files=files))
            else:
                eprint(f"export: warning: courses/{cid}/{m['id']}/ is missing")
            modules.append(dict(m, number=int(mm.group(1)) if mm else None,
                                path=mdir.relative_to(root).as_posix(),
                                readme=(mdir / "README.md").relative_to(root).as_posix()
                                if (mdir / "README.md").is_file() else None,
                                lessons=lessons))
        credits = _load(cdir / "credits.yaml", "credits", required=False)
        courses.append(dict(course, path=f"courses/{cid}", catalog=entry,
                            readme=f"courses/{cid}/README.md",
                            readme_en=f"courses/{cid}/README.en.md",
                            credits=(credits or {}).get("images", []) if isinstance(credits, dict) else [],
                            modules=modules))
    return {
        "generated_by": "tools/export.py",
        "site": {"origin": site.origin, "base": site.base},
        "repo": {"url": site.repo_url, "branch": site.branch},
        "catalog": catalog.get("courses") or [],
        "courses": courses,
        "tracks": (tracks or {}).get("tracks", []) if isinstance(tracks, dict) else [],
    }


def build_coverage(skills_json: dict, courses_json: dict) -> dict:
    per_skill: dict[str, list] = {s["id"]: [] for s in skills_json["skills"]}
    per_course: dict[str, dict] = {}
    lessons_total = 0
    for c in courses_json["courses"]:
        dev_ids, ass_ids = set(), set()
        n_dev = n_ass = n_lessons = 0
        for m in c["modules"]:
            for les in m["lessons"]:
                n_lessons += 1
                for d in les.get("develops") or []:
                    if isinstance(d, dict) and d.get("skill") in per_skill:
                        per_skill[d["skill"]].append({"lesson": les.get("id"), "course": c["id"],
                                                      "mode": "develops", "level": d.get("to"),
                                                      "to": d.get("to")})
                        dev_ids.add(d["skill"])
                        n_dev += 1
                for a in les.get("assesses") or []:
                    if isinstance(a, dict) and a.get("skill") in per_skill:
                        per_skill[a["skill"]].append({"lesson": les.get("id"), "course": c["id"],
                                                      "mode": "assesses", "level": a.get("level"),
                                                      "evidence": a.get("evidence")})
                        ass_ids.add(a["skill"])
                        n_ass += 1
        lessons_total += n_lessons
        per_course[c["id"]] = {"lessons": n_lessons, "develops": n_dev, "assesses": n_ass,
                               "skills_developed": sorted(dev_ids), "skills_assessed": sorted(ass_ids)}
    covered = sorted(k for k, v in per_skill.items() if v)
    assessed = sorted(k for k, v in per_skill.items() if any(e["mode"] == "assesses" for e in v))
    return {
        "generated_by": "tools/export.py",
        "skills": per_skill,
        "courses": per_course,
        "totals": {"skills": len(per_skill), "lessons": lessons_total, "covered": len(covered),
                   "assessed": len(assessed),
                   "uncovered": sorted(k for k, v in per_skill.items() if not v)},
    }


def build_case(site, skills_doc: dict, stamp: str) -> dict:
    """CASE 1.1-shaped CFPackage. Identifiers are uuid5 of the item's URI (stable)."""
    fw = skills_doc.get("framework") or {}
    title = fw.get("title") or {}
    doc_uri = f"{site.site_url}/skills/"
    doc_id = str(uuid.uuid5(uuid.NAMESPACE_URL, doc_uri))
    pkg_uri = f"{site.site_url}/case.json"

    def link(title_: str, ident: str, uri: str) -> dict:
        return {"title": title_, "identifier": ident, "uri": uri}

    doc_link = link(title.get("en", fw.get("id", "")), doc_id, doc_uri)
    types = {}
    for t in ("Group", "Skill"):
        turi = f"{site.site_url}/skills/#item-type-{t.lower()}"
        types[t] = {"identifier": str(uuid.uuid5(uuid.NAMESPACE_URL, turi)), "uri": turi, "title": t,
                    "description": f"TESA skill map {t.lower()}", "hierarchyCode": t,
                    "lastChangeDateTime": stamp}
    derived = fw.get("derived_from") or {}
    cf_doc = {
        "identifier": doc_id,
        "uri": doc_uri,
        "creator": site.org_en or "TESA",
        "title": title.get("en", ""),
        "lastChangeDateTime": stamp,
        "officialSourceURL": doc_uri,
        "publisher": site.org_en or "TESA",
        "description": title.get("th", ""),
        "language": "en",
        "version": str(fw.get("version", "")),
        "adoptionStatus": "Draft",
        "caseVersion": "1.1",
        "frameworkType": "Competency",
        "notes": (f"Adapted from \"{derived.get('title')}\" by {derived.get('author')} "
                  f"({derived.get('url')}), {derived.get('license')}.") if derived else "",
        "licenseURI": link(str(fw.get("license", "")), str(uuid.uuid5(uuid.NAMESPACE_URL,
                           f"https://spdx.org/licenses/{fw.get('license')}.html")),
                           f"https://spdx.org/licenses/{fw.get('license')}.html"),
        "CFPackageURI": link(title.get("en", ""), str(uuid.uuid5(uuid.NAMESPACE_URL, pkg_uri)), pkg_uri),
    }
    importance = skills_doc.get("importance") or {}
    items, assocs = [], []

    def assoc(origin: dict, dest: dict) -> dict:
        auri = f"{site.site_url}/case/associations/{origin['identifier']}/isChildOf/{dest['identifier']}"
        return {"identifier": str(uuid.uuid5(uuid.NAMESPACE_URL, auri)), "uri": auri,
                "associationType": "isChildOf",
                "originNodeURI": link(origin["title"], origin["identifier"], origin["uri"]),
                "destinationNodeURI": link(dest["title"], dest["identifier"], dest["uri"]),
                "CFDocumentURI": doc_link, "lastChangeDateTime": stamp}

    group_nodes = {}
    for gi, g in enumerate(skills_doc.get("groups") or []):
        if not isinstance(g, dict):
            continue
        guri = f"{site.site_url}/skills/#group-{g['id']}"
        gid = str(uuid.uuid5(uuid.NAMESPACE_URL, guri))
        items.append({"identifier": gid, "uri": guri, "fullStatement": g.get("en", g["id"]),
                      "alternativeLabel": g.get("th", ""), "humanCodingScheme": g["id"],
                      "listEnumeration": str(gi + 1), "CFItemType": "Group",
                      "CFItemTypeURI": link("Group", types["Group"]["identifier"], types["Group"]["uri"]),
                      "language": "en", "notes": f"area: {g.get('area')}",
                      "CFDocumentURI": doc_link, "lastChangeDateTime": stamp})
        node = {"title": g.get("en", g["id"]), "identifier": gid, "uri": guri}
        group_nodes[g["id"]] = node
        assocs.append(assoc(node, {"title": doc_link["title"], "identifier": doc_id, "uri": doc_uri}))
    for si, s in enumerate(skills_doc.get("skills") or []):
        if not isinstance(s, dict) or not isinstance(s.get("id"), str):
            continue
        suri = skill_url(site, s["id"])
        sid = skill_uuid(site, s["id"])
        imp = s.get("importance")
        notes = [f"roadmap importance: {importance.get(imp, {}).get('en', imp)}" if imp else
                 "added by TESA (not on the roadmap diagram)" if s.get("origin") == "tesa" else
                 "roadmap README topic"]
        if s.get("eer_node"):
            notes.append(f"roadmap node: {s['eer_node']}")
        if s.get("deprecated"):
            notes.append(f"deprecated; replaced by {s.get('replaced_by')}")
        items.append({"identifier": sid, "uri": suri, "fullStatement": s.get("en", s["id"]),
                      "alternativeLabel": s.get("th", ""), "humanCodingScheme": s["id"],
                      "listEnumeration": str(si + 1), "CFItemType": "Skill",
                      "CFItemTypeURI": link("Skill", types["Skill"]["identifier"], types["Skill"]["uri"]),
                      "language": "en", "notes": "; ".join(notes),
                      "CFDocumentURI": doc_link, "lastChangeDateTime": stamp})
        g = group_nodes.get(s.get("group"))
        if g:
            assocs.append(assoc({"title": s.get("en", s["id"]), "identifier": sid, "uri": suri}, g))
    return {"CFDocument": cf_doc, "CFItems": items, "CFAssociations": assocs,
            "CFDefinitions": {"CFItemTypes": list(types.values())}}


def check_case(case: dict) -> list[str]:
    """Problems in a CFPackage: invalid JSON round trip, dangling association or item-type targets."""
    problems = []
    try:
        case = json.loads(json.dumps(case, ensure_ascii=False))
    except (TypeError, ValueError) as exc:
        return [f"not valid JSON: {exc}"]
    doc = case.get("CFDocument") or {}
    known = {doc.get("identifier")} | {i.get("identifier") for i in case.get("CFItems") or []}
    if None in known:
        problems.append("an item or the document has no identifier")
    ids = [i.get("identifier") for i in case.get("CFItems") or []]
    if len(ids) != len(set(ids)):
        problems.append("duplicate CFItem identifiers")
    types = {t.get("identifier") for t in (case.get("CFDefinitions") or {}).get("CFItemTypes") or []}
    for it in case.get("CFItems") or []:
        t = (it.get("CFItemTypeURI") or {}).get("identifier")
        if t and t not in types:
            problems.append(f"item {it.get('humanCodingScheme')}: CFItemTypeURI {t} is not defined")
        if (it.get("CFDocumentURI") or {}).get("identifier") != doc.get("identifier"):
            problems.append(f"item {it.get('humanCodingScheme')}: CFDocumentURI is not the document")
    for a in case.get("CFAssociations") or []:
        for end in ("originNodeURI", "destinationNodeURI"):
            t = (a.get(end) or {}).get("identifier")
            if t not in known:
                problems.append(f"association {a.get('identifier')}: {end} {t} does not exist")
    return problems


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out", required=True, help="output folder (created if missing)")
    ap.add_argument("--root", default=str(REPO_ROOT), help="repository root (default: this repo)")
    ns = ap.parse_args(argv)
    root = Path(ns.root).resolve()
    policy = load_policy()
    site = load_site_config(root, policy)
    for w in site.warnings:
        eprint(f"export: warning: {w}")
    skills_doc = _load(root / "skills" / "skills.yaml", "skills/skills.yaml")
    catalog = _load(root / "catalog" / "courses.yaml", "catalog/courses.yaml")
    tracks = _load(root / "catalog" / "tracks.yaml", "catalog/tracks.yaml", required=False)
    if not isinstance(skills_doc, dict) or not isinstance(catalog, dict):
        raise SystemExit("export: skills.yaml or courses.yaml is not a mapping (run tools/validate.py)")
    out = Path(ns.out)
    out.mkdir(parents=True, exist_ok=True)
    skills_json = build_skills(root, site, skills_doc)
    courses_json = build_courses(root, site, catalog, tracks)
    coverage_json = build_coverage(skills_json, courses_json)
    case_json = build_case(site, skills_doc, _timestamp(root))
    problems = check_case(case_json)
    if problems:
        for p in problems:
            eprint(f"export: case.json: {p}")
        return 1
    write_json(out / "skills.json", skills_json)
    write_json(out / "courses.json", courses_json)
    write_json(out / "coverage.json", coverage_json)
    write_json(out / "case.json", case_json)
    t = coverage_json["totals"]
    print(f"export: {len(skills_json['skills'])} skills, {len(courses_json['courses'])} in-tree courses, "
          f"{t['lessons']} lessons, {t['covered']} skills covered ({t['assessed']} assessed), "
          f"{len(case_json['CFItems'])} CFItems, {len(case_json['CFAssociations'])} CFAssociations -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
