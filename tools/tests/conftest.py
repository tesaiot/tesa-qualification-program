# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: Apache-2.0
"""Shared pytest fixtures: every test works on a private copy of tests/fixtures/green."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pytest

TESTS = Path(__file__).resolve().parent
TOOLS = TESTS.parent
REPO = TOOLS.parent
FIXTURES = TESTS / "fixtures"
GREEN = FIXTURES / "green"

sys.path.insert(0, str(TOOLS))


@pytest.fixture
def green(tmp_path: Path) -> Path:
    """A writable copy of the green fixture repo (passes validate.py --strict)."""
    dst = tmp_path / "repo"
    shutil.copytree(GREEN, dst)
    return dst


@pytest.fixture
def lesson1(green: Path) -> Path:
    return green / "courses/demo-course/m01-first-steps/l01-blink"


def edit(path: Path, old: str, new: str, count: int = 1) -> None:
    """Replace text in a fixture file; fail loudly if the anchor text is not there."""
    text = path.read_text(encoding="utf-8")
    assert text.count(old) >= 1, f"anchor {old!r} not found in {path}"
    path.write_text(text.replace(old, new, count), encoding="utf-8")
