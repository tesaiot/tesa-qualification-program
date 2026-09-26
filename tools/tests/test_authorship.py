# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: Apache-2.0
"""tools/check_authorship.py: a commit that credits an AI assistant goes red; people stay green;
a check that cannot run says so (exit 2) instead of passing."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

import check_authorship

# Built from parts so this file never carries the credit it tests for.
AI_NAME, AI_ADDR = "Cl" + "aude", "noreply@" + "anthropic.com"
TRAILER = f"Co-Authored-By: {AI_NAME} Opus <{AI_ADDR}>"
FOOTER = f"🤖 Generated with [{AI_NAME} Code](https://example.org)"
HUMAN = "Co-authored-by: Somchai Jaidee <12345+somchai@users.noreply.github.com>"

pytestmark = pytest.mark.skipif(shutil.which("git") is None, reason="git is not installed")


def _git(repo: Path, *args: str, name: str = "Test Person", email: str = "test@example.org") -> None:
    env = {"GIT_AUTHOR_NAME": name, "GIT_AUTHOR_EMAIL": email, "GIT_COMMITTER_NAME": name,
           "GIT_COMMITTER_EMAIL": email, "HOME": str(repo), "PATH": "/usr/bin:/bin:/usr/local/bin"}
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, env=env)


def _commit(repo: Path, msg: str, **who) -> None:
    (repo / "f.txt").write_text(msg, encoding="utf-8")
    _git(repo, "add", "f.txt", **who)
    _git(repo, "commit", "-q", "-m", msg, **who)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    r = tmp_path / "r"
    r.mkdir()
    _git(r, "init", "-q", "-b", "main")
    _commit(r, f"First lesson\n\n{HUMAN}\nSigned-off-by: Test Person <test@example.org>")
    return r


def test_people_only_history_is_green(repo: Path) -> None:
    assert check_authorship.main(["--root", str(repo)]) == 0


@pytest.mark.parametrize("msg", [f"Fix a typo\n\n{TRAILER}", f"Add a lesson\n\n{FOOTER}",
                                 f"Tidy\n\nco-authored-by: {AI_NAME.lower()} <bot@example.org>"])
def test_ai_credit_in_any_commit_goes_red(repo: Path, msg: str, capsys) -> None:
    _commit(repo, msg)
    _commit(repo, "A later clean commit does not hide the earlier one")
    assert check_authorship.main(["--root", str(repo)]) == 1
    assert "AI-assistant credit" in capsys.readouterr().out


def test_ai_author_identity_goes_red(repo: Path) -> None:
    _commit(repo, "Looks clean", name=AI_NAME, email=AI_ADDR)
    assert check_authorship.main(["--root", str(repo)]) == 1


def test_range_checks_only_that_range(repo: Path) -> None:
    _commit(repo, f"Bad\n\n{TRAILER}")
    _git(repo, "tag", "bad")
    _commit(repo, "Good")
    assert check_authorship.main(["--root", str(repo), "--range", "bad..HEAD"]) == 0
    assert check_authorship.main(["--root", str(repo), "--range", "bad~1..HEAD"]) == 1


def test_message_file_hook(tmp_path: Path) -> None:
    msg = tmp_path / "COMMIT_EDITMSG"
    msg.write_text(f"Add quiz\n\n{TRAILER}\n", encoding="utf-8")
    assert check_authorship.main(["--message-file", str(msg)]) == 1
    msg.write_text(f"Add quiz\n\n# {TRAILER}\n{HUMAN}\n", encoding="utf-8")   # git strips # lines
    assert check_authorship.main(["--message-file", str(msg)]) == 0


def test_cannot_check_is_not_a_pass(tmp_path: Path) -> None:
    assert check_authorship.main(["--root", str(tmp_path / "not-a-repo")]) == 2


def test_shallow_clone_is_not_a_pass(repo: Path, tmp_path: Path) -> None:
    _commit(repo, "Second")
    shallow = tmp_path / "shallow"
    subprocess.run(["git", "clone", "-q", "--depth", "1", f"file://{repo}", str(shallow)], check=True,
                   capture_output=True)
    assert check_authorship.main(["--root", str(shallow)]) == 2
