# Contributing to TESA Open Knowledge

Thank you for helping. A one-word typo fix, a report that some code does not run, a translation or a whole new lesson are all
valuable. This page walks through the process from start to finish.

*Thai (source language): [CONTRIBUTING.md](CONTRIBUTING.md)*

## What you agree to when you contribute

By submitting work to this repository you confirm that:

1. you have the right to submit it, and it may be published under the licence of the path it lives in (see
   "Licences by path" below);
2. **your work is published as part of TESA Open Knowledge with the credit of the Thai Embedded Systems Association (TESA),
   สมาคมสมองกลฝังตัวไทย**, as set out in [ATTRIBUTION.md](ATTRIBUTION.md). Your name stays in the git history and, for
   substantive writing, in the `authors` list of the `course.yaml`;
3. you follow the [Code of Conduct](CODE_OF_CONDUCT.en.md).

## DCO sign-off on every commit

We use the [Developer Certificate of Origin 1.1](https://developercertificate.org/) instead of a CLA. Signing off certifies that you
have the right to submit the work under the project's licences. Add `-s` when you commit:

```bash
git commit -s -m "Fix the PWM explanation in lesson aiot-mpy.m02.l03"
```

git appends `Signed-off-by: Your Real Name <your@email>` to the message.

- Use a real name and a working e-mail (`git config user.name`, `git config user.email`).
- Forgot on the last commit? `git commit --amend -s --no-edit`. On several commits? `git rebase --signoff main`.
- Editing in the GitHub web editor? Type the `Signed-off-by:` line into the commit message yourself.

Pull requests with unsigned commits are not merged.

## Pick your route

| You want to | Start here |
|---|---|
| Report wrong content, a broken link, code that does not run | [Erratum](https://github.com/tesaiot/tesa-qualification-program/issues/new?template=erratum.yml) |
| Propose a new lesson or course | [Lesson proposal](https://github.com/tesaiot/tesa-qualification-program/issues/new?template=lesson-proposal.yml), before you write |
| Translate or review a translation | [Translation](https://github.com/tesaiot/tesa-qualification-program/issues/new?template=translation.yml) |
| Report that a new firmware or toolchain release broke a lesson | [Toolchain breakage](https://github.com/tesaiot/tesa-qualification-program/issues/new?template=toolchain-breakage.yml) |
| Report a vulnerability or a leaked secret | Not a public issue: see [SECURITY.md](SECURITY.md) |

Small fixes such as typos can go straight to a pull request.

## Writing or editing a lesson

1. **Open a lesson proposal** for anything large, to agree the goal, level and skill IDs with the course lead first.
2. **Fork and branch**, e.g. `lesson/aiot-mpy-m02-l04`.
3. **Copy a template** from [templates/](templates/): [templates/lesson/](templates/lesson/) into
   `courses/<course-id>/mNN-<slug>/lNN-<slug>/`, [templates/module/README.md](templates/module/README.md) for a module,
   [templates/course/](templates/course/) for a new course.
4. **Follow the authoring guide** [templates/AUTHORING.md](templates/AUTHORING.md) (Thai): front matter, heading order, quizzes,
   slides and the teaching rules.
5. **Run the validator** and make it pass:

   ```bash
   python3 tools/validate.py
   ```

   It checks the content model: YAML and front-matter schemas, skill IDs and referenced files. On a pull request, CI also checks
   banned words, image credits, links and per-file licensing.
6. **Run the code for real** on a board or in the BENTO Emulator, and note the board, firmware version and toolchain or
   emulator version in the pull request.
7. **Open the pull request** and complete the checklist in the template.

## The words rule

Learning units are **pathway → course (หลักสูตร) → module (โมดูล) → lesson (บทเรียน)**.

- Learner-facing text never uses `คาบ` or `คาบเรียน` to mean a class period, and never calls a unit of learning `session N`.
  Use lesson, module or course (บทเรียน, โมดูล, หลักสูตร). Inside the AIoT in Action course, "ตอน" may stand for a module.
- **Exception:** `คาบ` meaning the period of a signal is correct. For a PWM period, write **คาบเวลา**.
- Address the reader as "ผู้เรียน" (learner). Drop university-class framing: naming the learners' faculty or university,
  grading weights, senior/junior forms of address, or group sizes as requirements.
- Thai prose first, English technical terms welcome; common terms are in [glossary/terms.yaml](glossary/terms.yaml).
- Identifiers, function names and file names are English.

CI checks the banned words in lessons but cannot read context. If a correct "คาบเวลา" is flagged, say so in the PR.

## Licences by path

| Path | Licence |
|---|---|
| Markdown content, slides and your own images in `courses/` | CC BY 4.0 |
| New code (examples, practice, solutions, tools, site) | Apache-2.0 |
| Code imported from the AIC AIoT in Action course | MIT (keep the original copyright line) |
| `skills/` | CC BY-SA 4.0 |
| Third-party images or files | Their own licence, registered in `credits.yaml` |

Start new code files with an SPDX header:

```python
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: Apache-2.0
```

Infineon code examples are linked to by repository and tag by default. If a file must be copied, keep its original header and
licence file and cite the source in full (see [NOTICE.md](NOTICE.md)).

## Images and credits

- Every image you did not make yourself needs an entry in `courses/<course-id>/credits.yaml`: `path`, `title`, `author`,
  `source`, `license` (an SPDX ID, or `own` for your own image) and `modified` (true if you changed it, e.g. added Thai labels).
- A modified CC BY-SA image becomes CC BY-SA; record it correctly.
- No image without a clear licence.
- Every image needs alt text that says what it shows.
- `CREDITS.md` is generated from the `credits.yaml` files; do not edit it by hand.
- No file above 5 MB, and no video files.

## Translations

- Thai is the source (`README.md`); English sits next to it in the same folder (`README.en.md`).
- The Thai front matter's `translation` field is `done` when `README.en.md` matches the latest Thai, or `pending` when it is
  missing or behind.
- If you change the substance of the Thai text, update the English too or set `translation: pending`.
- Machine-translated drafts are fine if a person reviews them before merge and the PR says a machine helped.
- Code is shared by both languages; do not duplicate files per language.

## No secrets, no internal details

- No real Wi-Fi passwords, tokens, broker passwords or keys in code or screenshots. Use placeholders such as `"<your-password>"`.
- Before opening a PR, search your files for `PASSWORD`, `SECRET`, `TOKEN` and `API_KEY` and check every value is a placeholder.
- No internal machine or server paths, and no links to internal documents.
- Use the `tesaiot.dev` domain only: BENTO IDE at https://ide.tesaiot.dev/ and the Developer Hub at https://dev.tesaiot.dev/.

## Review and merge

- Every PR passes the validator, CI and the DCO check.
- A new lesson or a substantive change needs **two-key review**: a technical reviewer runs the code on a real board or the
  emulator, and a pedagogical reviewer checks objectives, time, prerequisites and skill IDs.
- An erratum that does not change substance needs one approval.
- Course leads listed in [.github/CODEOWNERS](.github/CODEOWNERS) merge.
- The lesson life cycle (pre-alpha → alpha → beta → stable) and its promotion criteria are in [GOVERNANCE.md](GOVERNANCE.md).

If you get stuck, ask in an issue. We will work it out together.
