# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: Apache-2.0
"""export.py, gen_credits.py, i18n_stale.py, gen_reuse.py: each proven in both directions."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tomllib
import uuid
from pathlib import Path

import pytest

import export
import gen_credits
import gen_reuse
import i18n_stale
from conftest import REPO, TOOLS, edit

L1 = "courses/demo-course/m01-first-steps/l01-blink"


# ------------------------------------------------------------------ export.py
def test_export_writes_the_four_files_with_config_driven_uuids(green: Path, tmp_path: Path) -> None:
    out = tmp_path / "out"
    assert export.main(["--root", str(green), "--out", str(out)]) == 0
    skills = json.loads((out / "skills.json").read_text(encoding="utf-8"))
    gpio = next(s for s in skills["skills"] if s["id"] == "mcu.gpio")
    # site.config.yaml of the fixture says https://fixture.example.org + /fixture-site
    assert gpio["url"] == "https://fixture.example.org/fixture-site/skills/mcu.gpio/"
    assert gpio["uuid"] == str(uuid.uuid5(uuid.NAMESPACE_URL, gpio["url"]))
    assert skills["roles"][0]["id"] == "embedded-developer"
    courses = json.loads((out / "courses.json").read_text(encoding="utf-8"))
    (course,) = courses["courses"]
    lessons = course["modules"][0]["lessons"]
    assert [le["id"] for le in lessons] == ["demo.m01.l01", "demo.m01.l02"]
    assert lessons[0]["path"] == L1 and lessons[0]["files"]["practice"] == ["practice/blink.py"]
    assert lessons[0]["en"]["lang"] == "en" and lessons[1]["en"] is None
    assert courses["tracks"][0]["id"] == "first-steps"
    cov = json.loads((out / "coverage.json").read_text(encoding="utf-8"))
    assert {"lesson": "demo.m01.l01", "course": "demo-course", "mode": "assesses", "level": 1,
            "evidence": "practice/blink.py"} in cov["skills"]["mcu.gpio"]
    assert cov["skills"]["lang.python"] == [] and "lang.python" in cov["totals"]["uncovered"]
    assert cov["courses"]["demo-course"]["lessons"] == 2
    case = json.loads((out / "case.json").read_text(encoding="utf-8"))
    assert export.check_case(case) == []
    types = {i["CFItemType"] for i in case["CFItems"]}
    assert types == {"Group", "Skill"}
    codes = {i["humanCodingScheme"] for i in case["CFItems"]}
    assert {"mcu", "lang", "mcu.gpio"} <= codes
    assert all(a["associationType"] == "isChildOf" for a in case["CFAssociations"])
    # 2 group->document + 5 skill->group
    assert len(case["CFAssociations"]) == 7


def test_export_is_deterministic(green: Path, tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SOURCE_DATE_EPOCH", "1790000000")
    a, b = tmp_path / "a", tmp_path / "b"
    export.main(["--root", str(green), "--out", str(a)])
    export.main(["--root", str(green), "--out", str(b)])
    for name in ("skills.json", "courses.json", "coverage.json", "case.json"):
        assert (a / name).read_bytes() == (b / name).read_bytes()


def test_export_falls_back_with_a_warning_when_site_config_is_missing(green, tmp_path, capsys):
    (green / "site.config.yaml").unlink()
    export.main(["--root", str(green), "--out", str(tmp_path / "o")])
    assert "site.config.yaml is missing" in capsys.readouterr().err
    skills = json.loads((tmp_path / "o/skills.json").read_text(encoding="utf-8"))
    url = next(s for s in skills["skills"] if s["id"] == "mcu.gpio")["url"]
    assert url == "https://tesaiot.github.io/tesa-qualification-program/skills/mcu.gpio/"


def test_case_check_catches_a_dangling_association(green: Path) -> None:
    site = export.load_site_config(green)
    skills_doc = export._load(green / "skills/skills.yaml", "skills")
    case = export.build_case(site, skills_doc, "2026-01-01T00:00:00+00:00")
    assert export.check_case(case) == []
    case["CFAssociations"][0]["destinationNodeURI"]["identifier"] = "00000000-dead-beef-0000-000000000000"
    case["CFItems"][0]["CFItemTypeURI"]["identifier"] = "not-a-type"
    problems = export.check_case(case)
    assert any("does not exist" in p for p in problems)
    assert any("is not defined" in p for p in problems)


# ------------------------------------------------------------------ gen_credits.py
def test_gen_credits_writes_checks_and_detects_staleness(green: Path, capsys) -> None:
    assert gen_credits.main(["--root", str(green), "--check"]) == 1           # missing
    assert gen_credits.main(["--root", str(green)]) == 0
    text = (green / "CREDITS.md").read_text(encoding="utf-8")
    assert "NOTICE.md" in text and "ATTRIBUTION.md" in text
    assert "| [`m01-first-steps/l01-blink/img/led_commons.png`](courses/demo-course/" in text
    assert "Fixture Author" in text and "CC-BY-SA-4.0" in text
    assert gen_credits.main(["--root", str(green), "--check"]) == 0           # fresh
    first = (green / "CREDITS.md").read_bytes()
    gen_credits.main(["--root", str(green)])
    assert (green / "CREDITS.md").read_bytes() == first                       # idempotent
    edit(green / "courses/demo-course/credits.yaml", "Fixture Author", "Another Author")
    assert gen_credits.main(["--root", str(green), "--check"]) == 1           # stale
    assert "stale" in capsys.readouterr().err


# ------------------------------------------------------------------ i18n_stale.py
def test_i18n_fresh_then_stale(green: Path, capsys) -> None:
    res = i18n_stale.scan(green)
    assert len(res["fresh"]) == 1 and res["stale"] == []
    assert i18n_stale.main(["--root", str(green), "--strict"]) == 0
    # A front-matter-only change in the Thai file does not make the translation stale ...
    edit(green / L1 / "README.md", "status: alpha", "status: beta")
    assert i18n_stale.scan(green)["stale"] == []
    # ... a body change does.
    edit(green / L1 / "README.md", "ทำให้ LED กะพริบ", "ทำให้ LED กะพริบเร็วขึ้น")
    assert len(i18n_stale.scan(green)["stale"]) == 1
    assert i18n_stale.main(["--root", str(green)]) == 0                        # report only
    assert i18n_stale.main(["--root", str(green), "--strict"]) == 1
    assert "STALE" in capsys.readouterr().out


def test_i18n_hash_helper_matches_scan(green: Path, capsys) -> None:
    i18n_stale.main(["--hash", str(green / L1 / "README.md")])
    h = capsys.readouterr().out.strip()
    assert f"source_sha256: {h}" in (green / L1 / "README.en.md").read_text(encoding="utf-8")


# ------------------------------------------------------------------ gen_reuse.py
def _reuse_toml(green: Path) -> dict:
    return tomllib.loads((green / "REUSE.toml").read_text(encoding="utf-8"))


def test_gen_reuse_policy_order_and_overrides(green: Path) -> None:
    assert gen_reuse.main(["--root", str(green), "--check"]) == 1             # missing
    assert gen_reuse.main(["--root", str(green)]) == 0
    data = _reuse_toml(green)
    assert data["version"] == 1
    anns = data["annotations"]
    first = anns[0]
    assert first["path"] == "**" and first["SPDX-License-Identifier"] == "CC-BY-NC-4.0"
    assert "2026 Thai Embedded Systems Association (TESA)" in [first["SPDX-FileCopyrightText"]]
    code = next(a for a in anns if a.get("path") and "courses/demo-course/**/practice/**" in a["path"])
    assert code["SPDX-License-Identifier"] == "Apache-2.0"                     # from course.yaml
    third = anns[-1]
    assert third["precedence"] == "override"
    assert third["path"] == f"courses/demo-course/{L1.split('demo-course/')[1]}/img/led_commons.png"
    assert third["SPDX-License-Identifier"] == "CC-BY-SA-4.0"
    assert third["SPDX-FileCopyrightText"] == "Fixture Author"
    assert gen_reuse.main(["--root", str(green), "--check"]) == 0             # fresh
    edit(green / "courses/demo-course/credits.yaml", "CC-BY-SA-4.0", "CC-BY-3.0")
    assert gen_reuse.main(["--root", str(green), "--check"]) == 1             # stale


def test_gen_reuse_aiot_policy_keeps_aic_on_code_and_adds_tesa_on_content(green: Path) -> None:
    aiot = green / "courses/aiot-micropython"
    aiot.mkdir()
    gen_reuse.main(["--root", str(green)])
    anns = _reuse_toml(green)["annotations"]
    content = next(a for a in anns if a["path"] == "courses/aiot-micropython/**")
    assert content["SPDX-FileCopyrightText"] == [
        "2026 Thai Embedded Systems Association (TESA)",
        "2026 Wiroon Sriborrirux, Advance Innovation Centre (AIC), Burapha University"]
    assert content["precedence"] == "aggregate" and content["SPDX-License-Identifier"] == "CC-BY-NC-4.0"
    res = next(a for a in anns if "courses/aiot-micropython/**/resources/**" in (a["path"] if isinstance(a["path"], list) else [a["path"]]))
    assert res["SPDX-License-Identifier"] == "CC-BY-4.0"                       # templates stay usable at work
    code = next(a for a in anns if isinstance(a["path"], list)
                and "courses/aiot-micropython/**/examples/**" in a["path"])
    assert code["SPDX-License-Identifier"] == "MIT"
    assert code["SPDX-FileCopyrightText"] == \
        "2026 Wiroon Sriborrirux, Advance Innovation Centre (AIC), Burapha University"
    assert "courses/aiot-micropython/shared/**" in code["path"]


def test_gen_reuse_reports_licences_missing_from_licenses_dir(green: Path, capsys) -> None:
    gen_reuse.main(["--root", str(green)])
    err = capsys.readouterr().err
    assert "CC-BY-SA-4.0" in err and "reuse download" in err                  # no LICENSES/ at all


@pytest.mark.skipif(shutil.which("reuse") is None and not (Path(sys.executable).parent / "reuse").exists(),
                    reason="reuse is not installed")
def test_reuse_lint_passes_on_the_green_fixture_and_fails_without_a_licence(green: Path) -> None:
    lic = REPO / "LICENSES"
    if not lic.is_dir():
        pytest.skip("repo LICENSES/ not present yet")
    (green / "LICENSES").mkdir()
    for name in ("Apache-2.0", "CC-BY-4.0", "CC-BY-NC-4.0", "CC-BY-SA-4.0"):   # exactly what the fixture uses
        if not (lic / f"{name}.txt").is_file():
            pytest.skip(f"repo LICENSES/{name}.txt not present yet")
        shutil.copy(lic / f"{name}.txt", green / "LICENSES" / f"{name}.txt")
    gen_reuse.main(["--root", str(green)])
    exe = shutil.which("reuse") or str(Path(sys.executable).parent / "reuse")
    ok = subprocess.run([exe, "--root", str(green), "lint"], capture_output=True, text=True)
    assert ok.returncode == 0, ok.stdout + ok.stderr
    (green / "LICENSES/CC-BY-SA-4.0.txt").unlink()
    bad = subprocess.run([exe, "--root", str(green), "lint"], capture_output=True, text=True)
    assert bad.returncode != 0 and "CC-BY-SA-4.0" in bad.stdout


def test_tools_have_no_hardcoded_site_origin() -> None:
    """Site origin/base must come from site.config.yaml; only policy.yaml may hold the fallback."""
    for p in TOOLS.glob("*.py"):
        text = p.read_text(encoding="utf-8")
        assert "tesaiot.github.io" not in text, p.name
