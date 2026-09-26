#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: Apache-2.0
#
# Render every courses/**/slides.md to site/public/slides/<course>/<module>/<lesson>/index.html
# (slides.en.md -> .../en.html) with Marp CLI. Runs in CI BEFORE `npm run build`, so Astro copies
# the decks into dist/. Needs Node (npx) and python3 with PyYAML.
#
#   bash site/scripts/render_slides.sh
#
# Every step fails loudly: a deck that is missing an image, that Marp cannot render, whose
# <html lang> is wrong or that does not show the TESA credit footer stops the build.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SITE="$(dirname "$HERE")"
REPO="$(dirname "$SITE")"
OUT="$SITE/public/slides"
ASSETS="$SITE/public/content-assets"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

# The Marp CLI version is pinned once, in site/package.json (devDependencies). Override with
# MARP_CLI_VERSION=x.y.z only to try another version.
MARP_VERSION="${MARP_CLI_VERSION:-$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["devDependencies"]["@marp-team/marp-cli"])' "$SITE/package.json")}"

echo "==> [slides] 1/3 prepare decks (credit footer, lang, links, images)"
rm -rf "$OUT"
mkdir -p "$OUT" "$ASSETS"
python3 "$HERE/slides.py" prepare --repo "$REPO" --stage "$WORK/decks" --out "$OUT" \
	--assets "$ASSETS" --manifest "$WORK/manifest.json"

COUNT="$(python3 -c 'import json,sys; print(len(json.load(open(sys.argv[1]))["decks"]))' "$WORK/manifest.json")"
if [ "$COUNT" -eq 0 ]; then
	echo "==> [slides] no slides.md in courses/ yet; nothing to render"
	exit 0
fi

echo "==> [slides] 2/3 marp-cli@${MARP_VERSION}: ${COUNT} deck(s) -> ${OUT#"$REPO"/}"
# Run from site/ so npx picks the copy `npm install` put in site/node_modules (same pinned version).
cd "$SITE"
npx --yes "@marp-team/marp-cli@${MARP_VERSION}" \
	--no-stdin \
	--config-file "$SITE/marp/marprc.yml" \
	--html \
	--input-dir "$WORK/decks" \
	--output "$OUT"

echo "==> [slides] 3/3 verify rendered decks"
python3 "$HERE/slides.py" verify --manifest "$WORK/manifest.json"
