# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: Apache-2.0
"""Screenshots of the BENTO emulator and TESAIoT web pages, taken on a CI runner (never on a server).

  survey  --glob 'courses/explorer/**/examples/*.py' --out DIR
          run every matching lesson program in the public BENTO simulator, photograph the emulated
          screen, and write DIR/<name>.png, DIR/report.json and DIR/contact-sheet-N.jpg for review.
  publish --manifest tools/screens/screens.yaml [--only ID ...]
          take the shots listed in the manifest and write them (WebP) to their `out` paths in the repo.

A shot that shows an error, a blank screen or a traceback is reported, never published: `publish`
exits 1 when any listed shot fails its gate. The simulator URL comes from site.config.yaml (ide.origin)
plus the manifest's `simulator_path`; nothing here names a host.
"""
from __future__ import annotations

import argparse
import asyncio
import io
import json
import math
import re
import sys
from pathlib import Path

import yaml
from PIL import Image, ImageDraw, ImageStat
from playwright.async_api import async_playwright

REPO = Path(__file__).resolve().parents[2]
MANIFEST = Path(__file__).with_name("screens.yaml")


def load_manifest(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    site = yaml.safe_load((REPO / "site.config.yaml").read_text(encoding="utf-8"))
    data["simulator"] = site["ide"]["origin"].rstrip("/") + data.get("simulator_path", "/simulator/index.html")
    return data


def gate(png: bytes, console: str) -> tuple[str, float]:
    """('ok' | 'traceback' | 'blank', ink): ink = share of pixels that differ from the background colour."""
    im = Image.open(io.BytesIO(png)).convert("RGB")
    small = im.resize((200, 120))
    colours = small.getcolors(200 * 120) or []
    bg = max(colours)[1] if colours else (0, 0, 0)
    ink = sum(n for n, c in colours if sum(abs(a - b) for a, b in zip(c, bg)) > 40) / (200 * 120)
    if "Traceback" in console or re.search(r"^\w*Error\b.*:", console, re.M):
        return "traceback", ink
    if ink < 0.01 or ImageStat.Stat(small).stddev[0] < 2:
        return "blank", ink
    return "ok", ink


async def shoot_emulator(browser, url: str, code: str, wait_ms: int, console_drawer: bool,
                         viewport: dict) -> tuple[bytes, str]:
    page = await browser.new_page(viewport=viewport)
    try:
        await page.goto(url, wait_until="load", timeout=60000)
        await page.wait_for_function("() => window.BentoEmulator && window.BentoEmulator.ready", timeout=60000)
        await page.evaluate("(c) => window.BentoEmulator.run(c)", code)
        await page.wait_for_timeout(wait_ms)
        canvas = page.locator("#emu-canvas")
        if console_drawer:   # the device's Console drawer button sits in the bottom-right corner
            box = await canvas.bounding_box()
            await canvas.click(position={"x": box["width"] - 50, "y": box["height"] - 34})
            await page.wait_for_timeout(600)
        png = await canvas.screenshot()
        console = await page.locator("#emu-console").inner_text()
        return png, console
    finally:
        await page.close()


async def shoot_page(browser, shot: dict, viewport: dict) -> tuple[bytes, str]:
    page = await browser.new_page(viewport=shot.get("viewport") or viewport)
    try:
        await page.goto(shot["url"], wait_until="networkidle", timeout=90000)
        if shot.get("wait_for"):
            await page.wait_for_selector(shot["wait_for"], state="visible", timeout=60000)
        for sel in shot.get("hide") or []:
            await page.add_style_tag(content=f"{sel}{{display:none !important}}")
        await page.wait_for_timeout(int(shot.get("wait_ms", 1500)))
        target = page.locator(shot["clip"]) if shot.get("clip") else page
        png = await target.screenshot()
        return png, ""
    finally:
        await page.close()


def contact_sheets(results: list[dict], out: Path, per_sheet: int = 24) -> None:
    ok = [r for r in results if r.get("png")]
    for n in range(math.ceil(len(ok) / per_sheet)):
        chunk = ok[n * per_sheet:(n + 1) * per_sheet]
        cols, tw, th = 4, 400, 262
        sheet = Image.new("RGB", (cols * tw, math.ceil(len(chunk) / cols) * th), "white")
        for i, r in enumerate(chunk):
            im = Image.open(out / r["png"]).convert("RGB")
            im.thumbnail((tw - 10, th - 32))
            x, y = (i % cols) * tw, (i // cols) * th
            sheet.paste(im, (x + 5, y + 5))
            ImageDraw.Draw(sheet).text((x + 6, y + th - 24), f"{i + n * per_sheet} {r['status']} {r['name'][:44]}",
                                       fill="red" if r["status"] != "ok" else "black")
        sheet.save(out / f"contact-sheet-{n + 1}.jpg", quality=82)


async def survey(pattern: str, out: Path, wait_ms: int, jobs: int) -> int:
    man = load_manifest(MANIFEST)
    files = sorted(p for p in REPO.glob(pattern) if p.is_file() and p.suffix == ".py")
    if not files:
        print(f"survey: no .py files match {pattern!r}", file=sys.stderr)
        return 2
    out.mkdir(parents=True, exist_ok=True)
    sem = asyncio.Semaphore(jobs)
    results: list[dict] = []
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()

        async def one(p: Path) -> None:
            rel = p.relative_to(REPO).as_posix()
            name = rel.replace("courses/", "").replace("/", "__")[:-3]
            async with sem:
                r = {"file": rel, "name": name}
                try:
                    png, console = await shoot_emulator(browser, man["simulator"], p.read_text(encoding="utf-8"),
                                                        wait_ms, False, man["viewport"])
                    status, ink = gate(png, console)
                    if status == "blank" and console.strip():   # a console-only program: show the drawer
                        png, console = await shoot_emulator(browser, man["simulator"], p.read_text(encoding="utf-8"),
                                                            wait_ms, True, man["viewport"])
                        status, ink = gate(png, console)
                        status = "console" if status == "ok" else status
                    (out / f"{name}.png").write_bytes(png)
                    r.update(status=status, ink=round(ink, 4), png=f"{name}.png", console=console[-600:])
                except Exception as exc:  # recorded, never silently dropped
                    r.update(status="error", error=f"{type(exc).__name__}: {exc}"[:300])
                results.append(r)
                print(f"{r['status']:9s} {rel}", flush=True)

        await asyncio.gather(*(one(p) for p in files))
        await browser.close()
    results.sort(key=lambda r: r["file"])
    (out / "report.json").write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    contact_sheets(results, out)
    counts = {s: sum(1 for r in results if r["status"] == s) for s in sorted({r["status"] for r in results})}
    print(f"survey: {len(results)} programs {counts}")
    return 0


async def publish(manifest: Path, only: list[str]) -> int:
    man = load_manifest(manifest)
    shots = [s for s in man.get("shots") or [] if not only or s["id"] in only]
    failed = []
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        for s in shots:
            try:
                if s["kind"] == "emulator":
                    code = (REPO / s["code"]).read_text(encoding="utf-8")
                    # `replace: [[old, new], ...]` fills what the learner must fill before the program runs
                    # (a team id, say) — for the photograph only; the lesson file is not changed.
                    for old_text, new_text in s.get("replace") or []:
                        if old_text not in code:
                            raise ValueError(f"replace: {old_text!r} is not in {s['code']}")
                        code = code.replace(old_text, new_text)
                    png, console = await shoot_emulator(browser, man["simulator"], code, int(s.get("wait_ms", 4000)),
                                                        bool(s.get("console")), man["viewport"])
                    status, _ = gate(png, console)
                else:
                    png, _ = await shoot_page(browser, s, man["viewport"])
                    status = "ok"
            except Exception as exc:
                status, png = f"error {type(exc).__name__}: {exc}"[:200], None
            if status != "ok" or png is None:
                failed.append((s["id"], status))
                print(f"FAIL {s['id']}: {status}")
                continue
            dest = REPO / s["out"]
            dest.parent.mkdir(parents=True, exist_ok=True)
            im = Image.open(io.BytesIO(png)).convert("RGB")
            if s.get("size"):   # centre-crop to the screen itself (the canvas element adds a CSS border)
                w, h = (int(v) for v in s["size"])
                if im.width >= w and im.height >= h:
                    x, y = (im.width - w) // 2, (im.height - h) // 2
                    im = im.crop((x, y, x + w, y + h))
            if s.get("width") and im.width > int(s["width"]):
                im = im.resize((int(s["width"]), round(im.height * int(s["width"]) / im.width)), Image.LANCZOS)
            if dest.suffix.lower() == ".png":   # replacing a picture a slide already uses: keep its format
                im.save(dest, "PNG", optimize=True)
            else:
                im.save(dest, "WEBP", quality=int(s.get("quality", 82)), method=6)
            print(f"ok   {s['id']} -> {s['out']} ({dest.stat().st_size // 1024} KB)")
        await browser.close()
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("survey")
    a.add_argument("--glob", required=True)
    a.add_argument("--out", type=Path, required=True)
    a.add_argument("--wait-ms", type=int, default=4000)
    a.add_argument("--jobs", type=int, default=3)
    b = sub.add_parser("publish")
    b.add_argument("--manifest", type=Path, default=MANIFEST)
    b.add_argument("--only", nargs="*", default=[])
    ns = ap.parse_args(argv)
    if ns.cmd == "survey":
        return asyncio.run(survey(ns.glob, ns.out, ns.wait_ms, ns.jobs))
    return asyncio.run(publish(ns.manifest, ns.only))


if __name__ == "__main__":
    sys.exit(main())
