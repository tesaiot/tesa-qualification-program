#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: Apache-2.0
"""Check the BUILT site (site/dist) before it is deployed. Run after `npm run build`.

    python3 site/scripts/check_dist.py [--dist site/dist]

Fails (exit 1) when:
  * the home pages (TH, EN) or the /roadmap/ and /coverage/ pages are missing;
  * a page's <html lang> is not th (root) / en (/en/);
  * any Starlight page lacks the TESA credit line in its footer (BUILD_SPEC §1.9);
  * a lesson page lacks the "cite this lesson" box;
  * a skill page /skills/<id>/ is missing for any skill in skills/skills.yaml;
  * Pagefind produced no index, or no Thai ("th") or English index;
  * the site is larger than the GitHub Pages limit (1 GB).
The inputs it compares against are the generated files (src/generated, src/content/docs), so each
check can go red: remove a skill page or the footer override and it fails.
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from pathlib import Path

import yaml

SITE = Path(__file__).resolve().parent.parent
PAGES_LIMIT = 1024 ** 3


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dist", type=Path, default=SITE / "dist")
    ap.add_argument("--site", type=Path, default=SITE)
    args = ap.parse_args()
    dist, site = args.dist.resolve(), args.site.resolve()
    cfg = json.loads((site / "src" / "generated" / "site-config.json").read_text(encoding="utf-8"))
    data = json.loads((site / "src" / "generated" / "site-data.json").read_text(encoding="utf-8"))
    credit = cfg["credit"]["line"]
    credit_forms = {credit, html.escape(credit, quote=False), html.escape(credit)}
    errors: list[str] = []

    def err(msg: str) -> None:
        errors.append(msg)
        print(f"::error::{msg}")

    if not dist.is_dir():
        print(f"::error::{dist} does not exist; run npm run build first")
        return 1

    # 1. key pages
    for rel in ("index.html", "en/index.html", "roadmap/index.html", "en/roadmap/index.html",
                "coverage/index.html", "en/coverage/index.html", "catalog/index.html", "attribution/index.html",
                "en/attribution/index.html", "skills/index.html"):
        if not (dist / rel).is_file():
            err(f"missing page dist/{rel}")

    # 2. every Starlight page: lang + credit footer
    pages = [p for p in dist.rglob("*.html")
             if not any(part in ("slides", "pagefind", "_astro", "content-assets") for part in p.relative_to(dist).parts)]
    no_credit, bad_lang = [], []
    for p in pages:
        text = p.read_text(encoding="utf-8", errors="replace")
        if "data-pagefind-body" not in text and "sl-markdown-content" not in text:
            continue  # not a Starlight page (e.g. a redirect stub)
        rel = p.relative_to(dist).as_posix()
        want = "en" if rel.startswith("en/") else "th"
        m = re.search(r"<html[^>]*\slang=\"([^\"]+)\"", text)
        if not m or m.group(1).split("-")[0] != want:
            bad_lang.append(f"{rel} (lang={m.group(1) if m else None})")
        if not any(f in text for f in credit_forms):
            no_credit.append(rel)
    if bad_lang:
        err(f"{len(bad_lang)} page(s) with the wrong <html lang>, e.g. {bad_lang[:3]}")
    if no_credit:
        err(f"{len(no_credit)} page(s) without the TESA credit line, e.g. {no_credit[:3]}")

    # 3. lesson pages carry the cite box; skill pages exist
    docs = site / "src" / "content" / "docs"
    lessons = 0
    for md in docs.rglob("*.md"):
        head = md.read_text(encoding="utf-8").split("\n---", 1)[0]
        if "kind: lesson" not in head:
            continue
        fm = yaml.safe_load(head.lstrip("-\n")) or {}
        slug = fm.get("slug")
        if not slug:
            continue
        lessons += 1
        page = dist / slug / "index.html"
        if not page.is_file():
            err(f"lesson page missing: dist/{slug}/index.html")
        elif "tok-cite" not in page.read_text(encoding="utf-8", errors="replace"):
            err(f"lesson page has no 'cite this lesson' box: dist/{slug}/index.html")
    missing_skills = [sid for sid in data["skills"] for pre in ("", "en/")
                      if not (dist / f"{pre}skills/{sid}" / "index.html").is_file()]
    if missing_skills:
        err(f"{len(missing_skills)} skill page(s) missing, e.g. {missing_skills[:3]} (expected dist/skills/<id>/index.html)")

    # 4. Pagefind index, per language
    entry = dist / "pagefind" / "pagefind-entry.json"
    langs = {}
    if not entry.is_file():
        err("no Pagefind index (dist/pagefind/pagefind-entry.json)")
    else:
        langs = json.loads(entry.read_text(encoding="utf-8")).get("languages", {})
        for lang in ("th", "en"):
            if not langs.get(lang, {}).get("page_count"):
                err(f"Pagefind has no '{lang}' index (languages: {sorted(langs)})")

    # 5. size
    total = sum(f.stat().st_size for f in dist.rglob("*") if f.is_file())
    if total > PAGES_LIMIT:
        err(f"site is {total / 1024 ** 2:.0f} MB, over the GitHub Pages 1 GB limit")
    slides = dist / "slides"
    n_decks = len(list(slides.rglob("*.html"))) if slides.is_dir() else 0

    print(f"==> [dist] {len(pages)} HTML files · {lessons} lesson pages · {len(data['skills'])} skills x 2 languages · "
          f"{n_decks} slide decks · {total / 1024 ** 2:.1f} MB")
    print(f"==> [dist] pagefind languages: " + ", ".join(f"{k}={v.get('page_count')}" for k, v in sorted(langs.items())))
    if errors:
        print(f"==> [dist] FAILED: {len(errors)} problem(s)")
        return 1
    print("==> [dist] all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
