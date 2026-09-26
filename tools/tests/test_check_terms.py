# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: Apache-2.0
"""Positive controls for tools/check_terms.py: it must go RED on class-period wording and stay
GREEN on signal-period wording, code and addresses. A check that cannot go red is not a check."""
from __future__ import annotations

import pytest

import check_terms
from conftest import FIXTURES

TERMS = FIXTURES / "terms"
FLAG_LINES = [ln for ln in (TERMS / "must_flag.md").read_text(encoding="utf-8").splitlines() if ln.strip()]


@pytest.mark.parametrize("line", FLAG_LINES)
def test_every_forbidden_line_is_flagged(line: str) -> None:
    found = check_terms.scan_text(line)
    assert found, f"NOT flagged (the check cannot go red here): {line!r}"
    assert all(f.line == 1 for f in found)


def test_must_flag_file_has_one_finding_per_line_at_least() -> None:
    found = check_terms.scan_file(TERMS / "must_flag.md")
    assert {f.line for f in found} == set(range(1, len(FLAG_LINES) + 1))


def test_every_rule_fires_at_least_once() -> None:
    found = check_terms.scan_file(TERMS / "must_flag.md")
    assert {f.rule for f in found} == {r.id for r in check_terms.RULES}


def test_signal_period_code_and_addresses_pass() -> None:
    found = check_terms.scan_file(TERMS / "must_pass.md")
    assert found == [], "false positives: " + "; ".join(f"{f.line}:{f.text}" for f in found)


def test_structured_markdown_front_matter_footer_notes_and_link_text() -> None:
    found = check_terms.scan_file(TERMS / "must_flag_structured.md")
    # 3 = front matter title, 4 = Marp footer, 10 = speaker note, 12 = link text (inline code on
    # the same line is not counted; the source: block on line 5 is provenance, not prose).
    assert sorted({f.line for f in found}) == [3, 4, 10, 12]
    assert len([f for f in found if f.line == 12]) == 1


def test_yaml_prose_is_scanned_but_comments_paths_and_provenance_are_not() -> None:
    found = check_terms.scan_file(TERMS / "must_flag.yaml")
    assert sorted({f.line for f in found}) == [3, 6, 9]


@pytest.mark.parametrize("text", [
    "สัญญาณมีคาบ 20 ms", "คาบเวลา 3 วินาที", "คาบของสัญญาณ", "คาบ (period)", "ทุกคาบเวลา",
    "ต่อคาบเวลา", "คาบเกี่ยว", "`คาบ 3`", "clean_session=1",
])
def test_allowed_phrases(text: str) -> None:
    assert check_terms.scan_text(text) == []


def test_code_files_are_not_scanned(tmp_path) -> None:
    p = tmp_path / "mqtt.py"
    p.write_text("# คาบ 3\nclient = MQTTClient(clean_session=True)  # session 3\n", encoding="utf-8")
    assert check_terms.scan_file(p) == []


def test_cli_exit_codes(tmp_path, capsys) -> None:
    bad = tmp_path / "bad.md"
    bad.write_text("เจอกันคาบหน้า\n", encoding="utf-8")
    good = tmp_path / "good.md"
    good.write_text("คาบเวลา 1 ms\n", encoding="utf-8")
    assert check_terms.main([str(bad)]) == 1
    assert "th-period-deictic" in capsys.readouterr().out
    assert check_terms.main([str(good)]) == 0
