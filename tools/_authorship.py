# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: Apache-2.0
"""The authorship rule, shared by tools/validate.py (files) and tools/check_authorship.py (commits).

Standard library only, so a git hook can run it with a plain python3.
"""
from __future__ import annotations

import re

# Authorship (owner's rule, 2026-09-26): authors and co-authors are people. An AI coding assistant is never
# credited as an author, a co-author or the generator of the work — not in a commit, not in a file.
# The patterns are written so that this source does not match itself (escaped dots and brackets).
AUTHORSHIP_PATTERNS = (
    (re.compile(r"^[ \t]*co-authored-by:.*\bclaude\b", re.I | re.M), "co-author trailer credits an AI assistant"),
    (re.compile(r"noreply@anthropic\.com", re.I), "AI assistant address"),
    (re.compile(r"generated\s+(?:with|by)\s+\[?claude(?:\s+code)?\]?", re.I), "\"generated with\" AI credit"),
)


def authorship_findings(text: str) -> list[tuple[int, str, str]]:
    """(line, what, matched text) for every AI-assistant credit in `text`."""
    out = []
    for rx, what in AUTHORSHIP_PATTERNS:
        for m in rx.finditer(text):
            out.append((text.count("\n", 0, m.start()) + 1, what, m.group(0).strip()))
    return sorted(out)
