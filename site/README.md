<!--
SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
SPDX-License-Identifier: CC-BY-4.0
-->

# TESA Open Knowledge website

This folder builds the public site at `https://tesaiot.github.io/tesa-qualification-program/`
(origin and base path come from [`../site.config.yaml`](../site.config.yaml); nothing here hardcodes them).

- **Astro Starlight** for the site: Thai at the root, English under `/en/`. Starlight's Thai UI and its
  "this page is not translated yet" notice are used as they are.
- **Pagefind** search (built into Starlight). Pagefind segments Thai when the page has `lang="th"`.
- **Marp CLI** renders each lesson's `slides.md` to `/slides/<course>/<module>/<lesson>/`.
- **IBM Plex Sans Thai** and **IBM Plex Mono** are self-hosted from `@fontsource` (OFL-1.1).

## Nothing under `src/content/docs/` is written by hand

The repository files are the source. `scripts/sync_content.py` turns them into Starlight pages each
time the site is built:

| Repository | Site |
|---|---|
| `courses/<c>/README.md` (+ `README.en.md`) | `/courses/<c>/` (and `/en/courses/<c>/`) |
| `courses/<c>/<mNN-…>/README.md` | `/courses/<c>/<m>/` |
| `courses/<c>/<m>/<lNN-…>/README.md` (front matter, BUILD_SPEC §4) | `/courses/<c>/<m>/<l>/`, with a lesson header box, review questions from `quiz.yaml`, and a “cite this lesson” box |
| any other `.md` in a course (`lab.md`, `resources/*.md`, …) | a page next to it, e.g. `/courses/<c>/<m>/<l>/lab/` |
| `courses/**/slides.md` | `/slides/<c>/<m>/<l>/` (Marp HTML) |
| `skills/skills.yaml` + every lesson's `develops` / `assesses` | `/skills/<id>/` (127 pages × 2 languages), `/skills/`, `/roadmap/`, `/coverage/` |
| `catalog/courses.yaml`, `catalog/tracks.yaml` | `/catalog/`, `/pathways/` |
| `ATTRIBUTION.md` | `/attribution/` ("วิธีอ้างอิง TESA / How to cite TESA"), linked from every page footer |
| `tqp/*.md`, `CONTRIBUTING*.md`, `GOVERNANCE.md`, … | `/about/<doc>/` |

Links inside the Markdown are rewritten on the way:

- to code or any other repo file (`examples/`, `practice/`, `solution/`, `shared/`, `*.py`, `*.c`, …) → GitHub,
  **pinned to the commit being built** (`GITHUB_SHA`; `repo.branch` when run locally);
- to another README or `.md` page → that page on the site (same language as the page linking);
- to `slides.md` → the rendered deck; to the lesson's own `quiz.yaml` → the review questions on the page;
- Markdown images (`![alt](img/x.png)`) are copied next to the generated page so Astro optimises them;
  images in raw HTML (`<img src>`) or linked with `[text](img/x.png)` are copied to `public/content-assets/`.

A link to a file that does not exist, an unknown skill id, a secret-shaped literal (same rule and allowlist as
`tools/validate.py`: `tools/credentials_allow.txt`) or an internal path is an **error**; with `--strict`
(what CI uses) the build stops and the log names the file.

Our own metadata rides in one namespaced front-matter field, `tqp`, declared in `src/content.config.ts`.
The components that render it are small overrides: `src/components/MarkdownContent.astro` (lesson header,
review questions, cite box) and `src/components/Footer.astro` (the TESA credit line, BUILD_SPEC §1.9, on every
page). `/roadmap/` and `/coverage/` are Astro pages in `src/pages/` that read `src/generated/site-data.json`.

## How CI builds it (`.github/workflows/site.yml`)

1. `pip install -r tools/requirements.txt`
2. `python tools/export.py --out site/src/data` (the [tools] export; `sync_content.py` cross-checks its skill
   uuids and coverage against its own reading of the YAML and warns if they disagree)
3. `python site/scripts/sync_content.py --strict`
4. `npm install` in `site/` (Node 22). **There is no lockfile yet**: versions in `package.json` are exact, but
   their dependencies are resolved fresh. Commit `site/package-lock.json` once it exists and switch to `npm ci`.
5. `bash site/scripts/render_slides.sh` — before the Astro build, so Astro copies `public/slides/` into `dist/`.
   It injects the credit footer into any deck that lacks it, adds `lang:` where missing, renders with Marp,
   then checks every deck has the right `<html lang>` and shows the credit line.
6. `npm run build` (Astro + Pagefind)
7. `python site/scripts/check_dist.py` — every page has the right `lang` and the credit line, every lesson has
   its cite box, all 127 × 2 skill pages exist, Pagefind has a `th` and an `en` index, size under 1 GB.
8. Upload `site/dist` and deploy to GitHub Pages (Settings → Pages → Source: GitHub Actions).

## Preview on your own computer

Needs Python 3.11+ with PyYAML and Node 22.12+. From the repository root:

```sh
pip install -r tools/requirements.txt
python3 tools/export.py --out site/src/data        # optional; the site works without it
python3 site/scripts/sync_content.py               # add --strict to fail on content errors
cd site
npm install
npm run dev                                        # http://localhost:4321/tesa-qualification-program/
```

Slides (optional, needs `npx`): `bash site/scripts/render_slides.sh` before `npm run dev` or `npm run build`.
Search works only in a production build: `npm run build && npm run preview`.

Re-run `sync_content.py` after editing course files; the dev server picks up the regenerated pages.

## Files

```
site/
  astro.config.mjs          Starlight config; reads src/generated/site-config.json + sidebar.json
  package.json              exact versions (see the build report for why each)
  marp/marprc.yml           Marp CLI config (lang: th, html: true)
  scripts/sync_content.py   repo -> src/content/docs + src/generated (Python, no Node)
  scripts/tok_site.py       shared helpers: site.config.yaml, link rewriting, secret scan
  scripts/slides.py         prepare/verify decks for render_slides.sh
  scripts/render_slides.sh  Marp render step (CI)
  scripts/check_dist.py     checks on the built site (CI)
  src/content.config.ts     docs collection = Starlight schema + `tqp`
  src/components/           Footer, MarkdownContent (overrides), LessonMeta, LessonEnd, RoadmapView, CoverageMatrix, CovIcon
  src/pages/                roadmap.astro, coverage.astro (+ en/)
  src/lib/                  strings.ts (UI words, TH/EN), data.ts (site-data.json types)
  src/styles/custom.css     fonts, Thai line height, roadmap colours (light and dark)
```

Generated and git-ignored: `src/content/docs/`, `src/generated/`, `src/data/`, `public/content-assets/`,
`public/slides/`, `dist/`, `node_modules/`.
