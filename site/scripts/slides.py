#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: Apache-2.0
"""Prepare and verify the Marp decks for the site (called by render_slides.sh; testable without Node).

    slides.py prepare --stage DIR --out site/public/slides --manifest M.json
    slides.py verify  --manifest M.json

prepare, for every courses/**/slides.md (and slides.en.md):
  * makes sure the deck carries the TESA credit footer (BUILD_SPEC §1.9): injects `footer:` when the
    deck has none, appends the credit line when an existing footer lacks it (and warns);
  * makes sure the deck declares `lang:` (th, or en for slides.en.md) so <html lang> is right;
  * rewrites links the way lesson pages do (code -> GitHub at this commit, READMEs -> site pages);
  * copies every local image the deck uses (Markdown, <img src>, CSS url()) to
    site/public/content-assets/<repo path> and points the deck at it by absolute URL;
  * writes the prepared deck to STAGE/<course>/<module>/<lesson>/index.md (en.md for English);
    Marp is then run once with --input-dir STAGE --output OUT.
verify checks every expected HTML exists, has the right <html lang>, and shows the credit line.
"""
from __future__ import annotations

import argparse
import html
import json
import os
import posixpath
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tok_site import (  # noqa: E402
    COMMENT_RE,
    Problems,
    RewriteContext,
    _protect,
    _restore,
    classify,
    copy_file,
    credential_allowlist,
    load_site_config,
    rewrite_markdown,
    scan_secrets,
    slides_route,
    split_front_matter,
)

DEFAULT_REPO = Path(__file__).resolve().parent.parent.parent
CSS_URL_RE = re.compile(r"url\(\s*(['\"]?)([^'\")]+)\1\s*\)")
DIRECTIVE_FOOTER_RE = re.compile(r"<!--\s*footer\s*:(.*?)-->", re.S)


def page_sources(repo: Path) -> dict:
    """Repo Markdown files that are site pages, so a deck's links to them go to the site."""
    import sync_content  # local module

    problems = Problems()
    b = sync_content.Builder(repo, repo / "site", "", problems)
    b.load_skills()
    b.load_catalog()
    b.discover_courses()
    b.discover_root_docs()
    return b.page_sources


def credit_segments(credit: str) -> list[str]:
    """'TESA Open Knowledge · © 2026 ... (TESA) · CC BY 4.0' -> its ' · '-separated parts."""
    return [part.strip() for part in credit.split("·") if part.strip()]


def credit_ok(text: str, segments: list[str]) -> bool:
    """A course may merge its own credit into the footer (BUILD_SPEC §1.9: "merge with an existing
    footer"), so the rule is: every part of the TESA credit line is there, in order."""
    pos = 0
    for part in segments:
        i = text.find(part, pos)
        if i < 0:
            return False
        pos = i + len(part)
    return True


def drop_key(lines: list[str], key: str) -> list[str]:
    """Remove a top-level YAML key and its indented continuation lines (block scalars)."""
    out, skipping = [], False
    for ln in lines:
        if re.match(rf"^{re.escape(key)}\s*:", ln):
            skipping = True
            continue
        if skipping and (ln.startswith((" ", "\t")) or not ln.strip()):
            continue
        skipping = False
        out.append(ln)
    return out


def prepare(args) -> int:
    repo = args.repo.resolve()
    cfg = load_site_config(repo)
    ref = args.ref or os.environ.get("GITHUB_SHA") or cfg.branch
    credit = cfg.credit["line"]
    segments = credit_segments(credit)
    out = args.out.resolve()
    stage = args.stage.resolve()
    stage.mkdir(parents=True, exist_ok=True)
    problems = Problems()
    ctx = RewriteContext(cfg=cfg, repo=repo, ref=ref, page_sources=page_sources(repo), problems=problems,
                         docs_dir=None, public_assets_dir=args.assets.resolve())
    decks = sorted(p for p in (repo / "courses").rglob("slides*.md") if p.name in ("slides.md", "slides.en.md")) \
        if (repo / "courses").is_dir() else []
    manifest = []
    for deck in decks:
        rp = deck.resolve().relative_to(repo).as_posix()
        if any(part.startswith(".") or part == "node_modules" for part in Path(rp).parts):
            continue
        lang = "en" if deck.name == "slides.en.md" else "th"
        route = slides_route(rp)  # slides/<c>/<m>/<l>
        rel_dir = route[len("slides/"):]
        text = deck.read_text(encoding="utf-8")
        fm, body, raw = split_front_matter(text, rp, problems)
        notes = []
        fm = fm or {}
        lines = raw.split("\n") if raw is not None else ["marp: true"]
        footer = fm.get("footer")
        if footer is None or str(footer).strip() == "":
            lines = drop_key(lines, "footer")
            lines.append("footer: " + json.dumps(credit, ensure_ascii=False))
            notes.append("footer injected")
        elif not credit_ok(str(footer), segments):
            merged = f"{str(footer).strip()} · {credit}"
            lines = drop_key(lines, "footer")
            lines.append("footer: " + json.dumps(merged, ensure_ascii=False))
            notes.append("credit appended to existing footer")
            problems.warn(rp, "deck footer does not carry the TESA credit line; appended it (please merge it in the source)")
        if not fm.get("lang"):
            lines.append(f"lang: {lang}")
            notes.append(f"lang: {lang} added")
        elif str(fm.get("lang")).split("-")[0] != lang:
            problems.warn(rp, f"deck says lang: {fm.get('lang')} but is published as {lang}")
        for m in DIRECTIVE_FOOTER_RE.finditer(body):
            if not credit_ok(m.group(1), segments) and m.group(1).strip() not in ("", "''", '""'):
                problems.warn(rp, "an in-deck <!-- footer: --> directive replaces the credit line on later slides")
        try:
            yaml.safe_load("\n".join(lines))
        except yaml.YAMLError as exc:
            problems.error(rp, f"front matter no longer parses after adding footer/lang: {exc}")
            continue
        scan_secrets(body, rp, problems, credential_allowlist(repo))
        # Links and images the same way lesson pages do: code -> GitHub at this commit, READMEs ->
        # site pages, images -> copied to public/content-assets and referenced by absolute URL
        # (so the deck works wherever its HTML sits). CSS url() in <style> blocks is handled here.
        before_missing = ctx.stats["missing"]
        body2 = rewrite_markdown(ctx, body, rp, lang, None)
        store: list[str] = []
        body2 = _protect(COMMENT_RE, body2, store)

        def css_url(m: re.Match) -> str:
            t = classify(m.group(2), posixpath.dirname(rp), repo, ctx.page_sources)
            if t.kind == "image":
                copy_file(repo / t.repo_path, ctx.public_assets_dir / t.repo_path)
                return f"url({m.group(1)}{cfg.asset_url(t.repo_path)}{t.suffix}{m.group(1)})"
            if t.kind in ("missing", "outside"):
                problems.error(rp, f"deck CSS url() target does not exist: {m.group(2)}")
                ctx.stats["missing"] += 1
            return m.group(0)

        body2 = _restore(CSS_URL_RE.sub(css_url, body2), store)
        # The deck's `style:` directive lives in the front matter; its url() needs the same treatment.
        fm_text = CSS_URL_RE.sub(css_url, "\n".join(lines).strip("\n"))
        missing = ctx.stats["missing"] - before_missing
        out_name = "index.md" if lang == "th" else "en.md"
        staged = stage / rel_dir / out_name
        staged.parent.mkdir(parents=True, exist_ok=True)
        staged.write_text("---\n" + fm_text + "\n---\n" + body2, encoding="utf-8")
        html_out = out / rel_dir / ("index.html" if lang == "th" else "en.html")
        manifest.append({"src": rp, "lang": lang, "stage": str(staged), "html": str(html_out),
                         "url": cfg.base + "/" + route + ("/" if lang == "th" else "/en.html"),
                         "notes": notes, "missing_images": missing})
        print(f"  deck {rp} -> {html_out.relative_to(out.parent)} {('(' + ', '.join(notes) + ')') if notes else ''}")
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps({"out": str(out), "credit": credit, "segments": segments, "decks": manifest},
                                        ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"==> [slides] prepared {len(manifest)} deck(s); manifest {args.manifest}")
    if problems.items:
        problems.report(sys.stdout)
    if problems.errors and not args.lenient:
        print("==> [slides] FAILED: fix the deck errors above (missing images, secrets, broken front matter).")
        return 1
    return 0


def verify(args) -> int:
    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    segments = data["segments"]
    bad = 0
    for d in data["decks"]:
        path = Path(d["html"])
        if not path.is_file():
            print(f"::error file={d['src']}::Marp produced no HTML at {path}")
            bad += 1
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"<html[^>]*\blang=\"([^\"]*)\"", text)
        got = m.group(1) if m else None
        if not got or got.split("-")[0].lower() != d["lang"]:
            print(f"::error file={d['src']}::rendered deck has <html lang=\"{got}\">, expected {d['lang']}")
            bad += 1
        if not (credit_ok(text, segments) or credit_ok(text, [html.escape(x, quote=False) for x in segments])):
            print(f"::error file={d['src']}::rendered deck does not show the TESA credit line")
            bad += 1
        n_footers = len(re.findall(r"<footer\b", text))
        print(f"  ok? {d['src']}: lang={got} footers={n_footers} size={path.stat().st_size // 1024} KB")
    total = len(data["decks"])
    if bad:
        print(f"==> [slides] verify FAILED: {bad} problem(s) in {total} deck(s)")
        return 1
    print(f"==> [slides] verify passed: {total} deck(s) have lang and the TESA credit footer")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prepare")
    p.add_argument("--repo", type=Path, default=DEFAULT_REPO)
    p.add_argument("--stage", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True, help="where Marp writes HTML (site/public/slides)")
    p.add_argument("--assets", type=Path, default=None, help="content-assets dir (default: <out>/../content-assets)")
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--ref", default=None)
    p.add_argument("--lenient", action="store_true", help="do not fail on deck errors")
    v = sub.add_parser("verify")
    v.add_argument("--manifest", type=Path, required=True)
    args = ap.parse_args()
    if args.cmd == "prepare":
        if args.assets is None:
            args.assets = args.out.parent / "content-assets"
        return prepare(args)
    return verify(args)


if __name__ == "__main__":
    sys.exit(main())
