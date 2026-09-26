# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: Apache-2.0
"""tools/validate.py: the green fixture passes --strict, and EVERY check goes red on a one-change
mutation of it. test_every_check_has_a_red_case fails if a check is added without one."""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

import validate
from conftest import GREEN, TOOLS, edit

L1 = "courses/demo-course/m01-first-steps/l01-blink"
L2 = "courses/demo-course/m01-first-steps/l02-pwm-period"
C = "courses/demo-course"


def test_green_fixture_is_clean_even_strict() -> None:
    rep = validate.run(GREEN, strict=True)
    assert rep.errors == [] and rep.warnings == [], [*rep.errors, *rep.warnings]
    assert not rep.failed


# ------------------------------------------------------------------ mutations
def m_yaml_syntax(r: Path):
    edit(r / C / "course.yaml", "hours: 2", "hours: [2")


def m_yaml_duplicate_key(r: Path):
    edit(r / C / "course.yaml", "hours: 2", "hours: 2\nhours: 3")


def m_schema_extra_key(r: Path):
    edit(r / C / "course.yaml", "hours: 2", "hours: 2\nduration: 2")


def m_schema_lesson_objectives(r: Path):
    edit(r / L2 / "README.md", "  - {th: ตั้งค่า duty cycle ให้ได้ความสว่างที่ต้องการ, en: Set a duty cycle for a target brightness}\n", "")


def m_skills_unknown(r: Path):
    edit(r / L2 / "README.md", "develops: [{skill: mcu.pwm, to: 1}]", "develops: [{skill: mcu.pwmx, to: 1}]")


def m_skills_deprecated(r: Path):
    edit(r / L2 / "README.md", "develops: [{skill: mcu.pwm, to: 1}]", "develops: [{skill: mcu.old-io, to: 1}]")


def m_skills_map_prefix(r: Path):
    edit(r / "skills/skills.yaml", "{id: mcu.pwm, group: mcu,", "{id: mcu.pwm, group: lang,")


def m_cover_missing(r: Path):
    edit(r / C / "course.yaml", "hours: 2", "hours: 2\ncover: {image: no-such-cover.webp, own: true}")


def m_cover_uncredited(r: Path):
    (r / C / "cover.webp").write_bytes(b"RIFF0000WEBPVP8 ")
    edit(r / C / "course.yaml", "hours: 2", "hours: 2\ncover: {image: cover.webp}")


def m_catalog_short(r: Path):
    edit(r / C / "course.yaml", "short: demo", "short: dem")


def m_catalog_unregistered(r: Path):
    (r / "courses/stray-course").mkdir()


def m_catalog_missing_folder(r: Path):
    shutil.rmtree(r / C)


def m_structure_module_readme(r: Path):
    (r / C / "m01-first-steps/README.md").unlink()


def m_structure_lesson_id(r: Path):
    edit(r / L2 / "README.md", "id: demo.m01.l02", "id: demo.m01.l03")


def m_structure_unlisted_module(r: Path):
    (r / C / "m02-extra").mkdir()
    (r / C / "m02-extra/README.md").write_text("# m02\n", encoding="utf-8")


def m_structure_bad_lesson_folder(r: Path):
    (r / C / "m01-first-steps/l3-Bad").mkdir()


def m_prereq(r: Path):
    edit(r / L2 / "README.md", "prerequisites: [demo.m01.l01]", "prerequisites: [demo.m09.l09]")


def m_tracks_course(r: Path):
    edit(r / "catalog/tracks.yaml", "{course: outside-course}", "{course: nowhere-course}")


def m_tracks_module(r: Path):
    edit(r / "catalog/tracks.yaml", "modules: [m01-first-steps]", "modules: [m07-missing]")


def m_roles(r: Path):
    edit(r / "skills/roles/embedded-developer.yaml", "{skill: mcu.gpio, level: 3", "{skill: mcu.gpiox, level: 3")


def m_links(r: Path):
    edit(r / L1 / "README.md", "[practice/blink.py](practice/blink.py)", "[practice/blink.py](practice/blinky.py)")


def m_links_image(r: Path):
    edit(r / L1 / "README.md", "(img/led.png)", "(img/missing.png)")


def m_alt(r: Path):
    edit(r / L1 / "README.md", "![LED บนบอร์ด](img/led.png)", "![](img/led.png)")


def m_alt_marp(r: Path):
    edit(r / L1 / "slides.md", "![bg right:40% LED สีแดงบนบอร์ด]", "![bg right:40%]")


def m_evidence(r: Path):
    for f in ("README.md", "README.en.md"):
        edit(r / L1 / f, "evidence: practice/blink.py", "evidence: practice/blink2.py")


def m_pairs(r: Path):
    (r / L1 / "practice/extra.py").write_text("____\n", encoding="utf-8")


def m_pairs_solution_only(r: Path):
    (r / L1 / "solution/bonus.py").write_text("print(1)\n", encoding="utf-8")


def m_slides(r: Path):
    for f in ("README.md", "README.en.md"):
        edit(r / L1 / f, "slides: slides.md", "slides: deck.md")


def m_quiz_objective(r: Path):
    edit(r / L1 / "quiz.yaml", "objective: 2", "objective: 3")


def m_quiz_answer(r: Path):
    edit(r / L1 / "quiz.yaml", "answer: [1]", "answer: [2]")


def m_translation_done(r: Path):
    (r / L1 / "README.en.md").unlink()


def m_translation_lang(r: Path):
    edit(r / L1 / "README.en.md", "lang: en", "lang: th")


def m_credits_path(r: Path):
    edit(r / C / "credits.yaml", "img/led_commons.png", "img/led_commons2.png")


def m_credits_source_cut(r: Path):
    edit(r / C / "credits.yaml", "File:Example.png", "File:Example_(2019")


def m_credits_uncredited(r: Path):
    shutil.copy(r / L1 / "img/led.png", r / L1 / "img/chip_wikimedia.png")
    edit(r / L1 / "README.md", "## ฝึกเติม", "![ชิปจาก Wikimedia](img/chip_wikimedia.png)\n\n## ฝึกเติม")


def m_terms_course(r: Path):
    edit(r / L2 / "README.md", "## แนวคิด\n", "## แนวคิด\n\nในคาบ 3 เราจะอ่านเซนเซอร์\n")


def m_terms_root(r: Path):
    edit(r / "README.md", "# ชุดทดสอบ", "# ชุดทดสอบ\n\nเจอกันคาบหน้า")


def m_size(r: Path):
    with open(r / L1 / "img/huge.bin", "wb") as fh:
        fh.truncate(6 * 1024 * 1024)   # sparse: 6 MB by size, no disk used


def m_secrets(r: Path):
    edit(r / L1 / "examples/01_blink.py", 'WIFI_PASS = "<รหัสผ่านของคุณ>"', 'WIFI_PASS = "hunter22"')


def m_secrets_c(r: Path):
    (r / L1 / "examples/wifi.h").write_text('#define WIFI_PASSWORD "hunter22"\n', encoding="utf-8")


def m_secrets_key(r: Path):
    (r / L1 / "examples/device.key").write_text("-----BEGIN PRIVATE KEY-----\nMIIB\n", encoding="utf-8")
    (r / L1 / "examples/device.key").rename(r / L1 / "examples/device_key.txt")


def m_leaks(r: Path):
    edit(r / "README.md", "# ชุดทดสอบ", "# ชุดทดสอบ\n\nเปิด https://ide.tesaiot.com/ ได้เลย")


def m_leaks_path(r: Path):
    edit(r / L2 / "README.md", "## แนวคิด\n", "## แนวคิด\n\nไฟล์อยู่ที่ /mnt/tesaiot_volume/x\n")


def m_leaks_scratch(r: Path):
    edit(r / L2 / "README.md", "## แนวคิด\n", "## แนวคิด\n\nร่างอยู่ที่ /tmp/agent-1000/-mnt-volume-x/scratchpad/a.md\n")


# Built from parts so this test file never carries the credit it tests for.
AI_NAME, AI_ADDR = "Cl" + "aude", "noreply@" + "anthropic.com"


def m_authorship_trailer(r: Path):
    edit(r / L2 / "README.md", "## แนวคิด\n", f"## แนวคิด\n\nCo-Authored-By: {AI_NAME} <{AI_ADDR}>\n")


def m_authorship_generated(r: Path):
    edit(r / "README.md", "# ชุดทดสอบ", f"# ชุดทดสอบ\n\n🤖 Generated with {AI_NAME} Code")


def m_footer(r: Path):
    edit(r / L1 / "slides.md", 'footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY 4.0"',
         'footer: "AIoT in Action"')


def m_footer_directive(r: Path):
    edit(r / L1 / "slides.md", "## ลูปกะพริบ", "<!-- footer: หน้าที่สอง -->\n\n## ลูปกะพริบ")


def m_footer_partial(r: Path):
    edit(r / L1 / "slides.md", " · CC BY 4.0\"", "\"")


def m_cite_heading(r: Path):
    edit(r / C / "README.md", "## อ้างอิง TESA", "## เครดิต")


def m_cite_url(r: Path):
    edit(r / C / "README.en.md", "https://github.com/example/fixture-repo", "https://example.org/")


def m_cite_wording(r: Path):
    edit(r / C / "README.md", "สัญญาอนุญาต CC BY 4.0", "สงวนลิขสิทธิ์")


def m_notice(r: Path):
    (r / "NOTICE").unlink()


def m_notice_name(r: Path):
    (r / "ATTRIBUTION.md").write_text("# Attribution\n\nCredit the association.\n", encoding="utf-8")


def m_time(r: Path):
    edit(r / L2 / "README.md", "time_min: {concept: 15, practise: 10, check: 5}",
         "time_min: {concept: 150, practise: 10, check: 5}")


def m_time_hard_limit(r: Path):
    edit(r / L2 / "README.md", "time_min: {concept: 15, practise: 10, check: 5}",
         "time_min: {concept: 3, check: 2}")


def m_config(r: Path):
    edit(r / "site.config.yaml", "  branch: main\n", "")


# (mutation, check that must go red, "error" | "warning")
CASES = [
    (m_cover_missing, "cover", "error"),
    (m_cover_uncredited, "cover", "error"),
    (m_yaml_syntax, "yaml", "error"),
    (m_yaml_duplicate_key, "yaml", "error"),
    (m_schema_extra_key, "schema", "error"),
    (m_schema_lesson_objectives, "schema", "error"),
    (m_skills_unknown, "skills", "error"),
    (m_skills_deprecated, "skills", "error"),
    (m_skills_map_prefix, "skills", "error"),
    (m_catalog_short, "catalog", "error"),
    (m_catalog_unregistered, "catalog", "error"),
    (m_catalog_missing_folder, "catalog", "error"),
    (m_structure_module_readme, "structure", "error"),
    (m_structure_lesson_id, "structure", "error"),
    (m_structure_unlisted_module, "structure", "error"),
    (m_structure_bad_lesson_folder, "structure", "error"),
    (m_prereq, "prereq", "error"),
    (m_tracks_course, "tracks", "error"),
    (m_tracks_module, "tracks", "error"),
    (m_roles, "roles", "error"),
    (m_links, "links", "error"),
    (m_links_image, "links", "error"),
    (m_alt, "alt", "warning"),
    (m_alt_marp, "alt", "warning"),
    (m_evidence, "evidence", "error"),
    (m_pairs, "pairs", "error"),
    (m_pairs_solution_only, "pairs", "error"),
    (m_slides, "slides", "error"),
    (m_quiz_objective, "quiz", "error"),
    (m_quiz_answer, "quiz", "error"),
    (m_translation_done, "translation", "error"),
    (m_translation_lang, "translation", "error"),
    (m_credits_path, "credits", "error"),
    (m_credits_source_cut, "credits", "error"),
    (m_credits_uncredited, "credits", "warning"),
    (m_terms_course, "terms", "error"),
    (m_terms_root, "terms", "warning"),
    (m_size, "size", "error"),
    (m_secrets, "secrets", "error"),
    (m_secrets_c, "secrets", "error"),
    (m_secrets_key, "secrets", "error"),
    (m_leaks, "leaks", "error"),
    (m_leaks_path, "leaks", "error"),
    (m_leaks_scratch, "leaks", "error"),
    (m_authorship_trailer, "authorship", "error"),
    (m_authorship_generated, "authorship", "error"),
    (m_footer, "tesa-footer", "error"),
    (m_footer_directive, "tesa-footer", "error"),
    (m_footer_partial, "tesa-footer", "warning"),
    (m_cite_heading, "tesa-cite", "error"),
    (m_cite_url, "tesa-cite", "error"),
    (m_cite_wording, "tesa-cite", "warning"),
    (m_notice, "tesa-notice", "error"),
    (m_notice_name, "tesa-notice", "error"),
    (m_time, "time", "warning"),
    (m_time_hard_limit, "time", "error"),
    (m_config, "config", "warning"),
]
# Mutations that legitimately trip a second check as well (everything else must be isolated).
ALSO = {
    "m_catalog_missing_folder": {"links"},       # the root README links into the deleted course
    "m_structure_module_readme": {"links"},      # the course READMEs link to the deleted file
    "m_schema_lesson_objectives": {"quiz"},      # q2 now points at objective 2 of 1
}


@pytest.mark.parametrize("mutate,check,severity", CASES, ids=[c[0].__name__ for c in CASES])
def test_check_goes_red(green: Path, mutate, check: str, severity: str) -> None:
    mutate(green)
    rep = validate.run(green)
    bucket = rep.errors if severity == "error" else rep.warnings
    hits = [f for f in bucket if f.check == check]
    assert hits, f"{check} did not go red ({severity}); got {[*rep.errors, *rep.warnings]}"
    others = {f.check for f in [*rep.errors, *rep.warnings]} - {check} - ALSO.get(mutate.__name__, set())
    assert not others, f"{mutate.__name__} also tripped {others}: {[*rep.errors, *rep.warnings]}"
    if severity == "warning":
        assert not rep.failed and validate.run(green, strict=True).failed, "--strict must fail on warnings"
    else:
        assert rep.failed


def test_internal_crash_is_an_error_not_a_pass(green: Path, monkeypatch) -> None:
    def boom(ctx):
        raise RuntimeError("simulated")
    monkeypatch.setattr(validate, "check_tracks", boom)
    rep = validate.run(green)
    assert [f for f in rep.errors if f.check == "internal" and "tracks crashed" in f.message]
    assert rep.failed


def test_every_check_has_a_red_case() -> None:
    covered = {c for _, c, _ in CASES} | {"internal"}
    assert covered == set(validate.CHECKS), f"checks without a red case: {set(validate.CHECKS) - covered}"


def test_github_annotations_and_exit_code(green: Path) -> None:
    m_links(green)
    env = dict(os.environ, GITHUB_ACTIONS="true")
    out = subprocess.run([sys.executable, str(TOOLS / "validate.py"), "--root", str(green)],
                         capture_output=True, text=True, env=env)
    assert out.returncode == 1
    assert f"::error file={L1}/README.md,line=" in out.stdout
    assert "title=links::broken link" in out.stdout
    clean = subprocess.run([sys.executable, str(TOOLS / "validate.py"), "--root", str(GREEN)],
                           capture_output=True, text=True, env=env)
    assert clean.returncode == 0 and "::error" not in clean.stdout


def test_line_numbers_point_at_the_offending_key(green: Path) -> None:
    m_skills_unknown(green)
    rep = validate.run(green)
    hit = next(f for f in rep.errors if f.check == "skills")
    lines = (green / L2 / "README.md").read_text(encoding="utf-8").splitlines()
    assert "mcu.pwmx" in lines[hit.line - 1]


def test_fixture_folder_is_excluded_from_the_real_repo_scan() -> None:
    files = validate.iter_files(TOOLS.parent)
    assert not [f for f in files if f.startswith("tools/tests/fixtures/")]


def test_missing_site_config_falls_back_with_a_warning(green: Path) -> None:
    (green / "site.config.yaml").unlink()
    rep = validate.run(green)
    assert [f for f in rep.warnings if f.check == "config" and "missing" in f.message]
    # The fallback repo URL is TESA's real one, not the fixture's, so the citation check notices.
    assert [f for f in rep.errors if f.check == "tesa-cite"]


def test_merged_footer_is_accepted(green: Path) -> None:
    """BUILD_SPEC §1.9 says merge the credit line with an existing footer: other credits may sit
    between its parts."""
    edit(green / L1 / "slides.md", "(TESA) · CC BY 4.0", "(TESA) · ดัดแปลงจาก AIoT in Action (AIC) · CC BY 4.0")
    rep = validate.run(green, strict=True)
    assert not rep.failed, [*rep.errors, *rep.warnings]


def test_free_text_evidence_is_not_treated_as_a_path(green: Path) -> None:
    for f in ("README.md", "README.en.md"):
        edit(green / L1 / f, "evidence: practice/blink.py",
             "evidence: \"Deliverables: blink.mp4 + checklist.md\"")
    rep = validate.run(green, strict=True)
    assert not rep.failed, [*rep.errors, *rep.warnings]


def _set_minutes(readme: Path, total: int) -> None:
    tm = f"{{concept: {total}}}" if total <= 240 else f"{{concept: 240, check: {total - 240}}}"
    edit(readme, "time_min: {concept: 15, practise: 10, check: 5}", f"time_min: {tm}")


def _make_lab(repo: Path) -> Path:
    """Copy lesson 2 into a lab folder (name contains 'lab'), as lesson 3 of the module."""
    lab = repo / C / "m01-first-steps/l03-pwm-lab"
    shutil.copytree(repo / L2, lab)
    edit(lab / "README.md", "id: demo.m01.l02", "id: demo.m01.l03")
    return lab


# Lead decision 2026-09-25: total 10-240 min, else ERROR; above 75 is a WARNING unless a lab.
@pytest.mark.parametrize("kind,total,expected", [
    ("lesson", 9, "error"), ("lesson", 10, "clean"), ("lesson", 75, "clean"), ("lesson", 76, "warning"),
    ("lesson", 240, "warning"), ("lesson", 241, "error"),
    ("lab", 9, "error"), ("lab", 76, "clean"), ("lab", 240, "clean"), ("lab", 241, "error"),
])
def test_time_limits(green: Path, kind: str, total: int, expected: str) -> None:
    readme = (_make_lab(green) if kind == "lab" else green / L2) / "README.md"
    _set_minutes(readme, total)
    rep = validate.run(green)
    errs = [f for f in rep.errors if f.check == "time"]
    warns = [f for f in rep.warnings if f.check == "time"]
    others = [f for f in [*rep.errors, *rep.warnings] if f.check != "time"]
    assert not others, others
    assert (bool(errs), bool(warns)) == {"error": (True, False), "warning": (False, True),
                                         "clean": (False, False)}[expected], (errs, warns)


def test_schema_caps_a_single_time_field_at_240(green: Path) -> None:
    edit(green / L2 / "README.md", "time_min: {concept: 15, practise: 10, check: 5}", "time_min: {concept: 241}")
    rep = validate.run(green)
    assert [f for f in rep.errors if f.check == "schema" and "time_min/concept" in f.message]


def test_cite_wording_survives_line_wrapping_and_the_adapted_suffix(green: Path) -> None:
    edit(green / C / "README.md", "\"หลักสูตรตัวอย่าง: ไฟกะพริบ\" จาก TESA Open Knowledge โดยสมาคม",
         "\"หลักสูตรตัวอย่าง: ไฟกะพริบ\" (ดัดแปลง) จาก **TESA Open Knowledge** โดยสมา\n> คม")
    rep = validate.run(green, strict=True)
    assert not rep.failed, [*rep.errors, *rep.warnings]
