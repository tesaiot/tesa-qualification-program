---
id: c-found.m06.l02
lang: en
title: {th: CI สำหรับเฟิร์มแวร์, en: CI for firmware}
summary: {th: ให้ GitHub Actions build ตรวจรูปแบบโค้ด วิเคราะห์แบบสถิต และรัน test ทุกการเปลี่ยนแปลง, en: 'Have GitHub Actions build, format-check, statically analyse and test every change.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m06.l01]
objectives:
- {th: เขียน workflow ของ GitHub Actions ที่รัน unit test บนเครื่องโฮสต์ทุก pull request, en: Write a GitHub Actions workflow that runs the host unit tests on every pull request.}
- {th: เพิ่มขั้นตรวจรูปแบบโค้ดด้วย clang-format และวิเคราะห์แบบสถิตด้วย cppcheck, en: Add a clang-format check and cppcheck static analysis.}
- {th: อธิบายว่าอะไรที่ CI บน runner สาธารณะตรวจได้ และอะไรที่ต้องทดสอบบนบอร์ดจริง, en: Explain what CI on public runners can check and what still needs a real board.}
develops:
- {skill: test.cicd, to: 3}
- {skill: vcs.git, to: 2}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
source_sha256: 1c11c4f6c2115f7baba6f2dd4f7015a2a9fd6eeddb4f9143c990f679f50b2ebe
---

## Objectives

By the end of this lesson, you will be able to

1. Write a GitHub Actions workflow that runs the host unit tests on every pull request.
2. Add a clang-format check and cppcheck static analysis step.
3. Explain what CI on public runners can check, and what still needs a real board.

Takes about 70 minutes (concepts 15 · practice 25 · lab 25 · check 5). You need everything from lesson 6.1, plus python3. If you want to run every step locally, you also need cppcheck and gcc-arm-none-eabi (on Ubuntu: `sudo apt-get install cppcheck gcc-arm-none-eabi`). The lab needs a GitHub account.

## Before you start

Two review questions.

1. The `pre-commit` hook from lesson 2.3 checks every commit on your own machine. Why still isn't that enough for a team (hint: `git commit --no-verify`)?
2. Lesson 6.1 said what a passing test can prove — and how did you prove it can genuinely fail?

## See it work first

The SDK repository this course uses has exactly one GitHub Actions workflow at commit ef72c1b. Below is its header and first step.

```yaml
on:
  release:
    types: [published]
  workflow_dispatch:

permissions:
  contents: read
# ... (concurrency and env omitted)
jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Ask the relay to re-read GitHub
        run: |
          set -euo pipefail
          echo "POST $RELAY/api/firmware/github/refresh"
          code=$(curl -s -o /tmp/refresh.json -w '%{http_code}' -X POST --max-time 120 \
                   "$RELAY/api/firmware/github/refresh")
          echo "HTTP $code"; cat /tmp/refresh.json; echo
          test "$code" = "200"
```

Source: [.github/workflows/notify-flash-relay.yml lines 20-46](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/.github/workflows/notify-flash-relay.yml#L20-L46) (Apache-2.0, tesaiot-pse84-devkit-sdk)

**Predict before reading on**, three questions: when does this workflow run? Does it build firmware? And if `curl` gets an HTTP 500, does this step turn green or red?

The answers: it runs when a release is published (or triggered manually). It does **not** build firmware — it just tells the Remote Flash relay to fetch the new release. A later step in the same file then verifies with sha256 that the `.hex` file actually arrived ("Firing the refresh is not the same as the file arriving"). If it gets a 500, the last line, `test "$code" = "200"`, returns non-zero, so the step turns red. That line is what makes this step able to fail — without it, the `echo` above would print 500 and still finish with 0. This lesson applies the same principle to every check.

## Concepts

### 1. Workflow, job, step, and "a thin workflow, a thick script"

GitHub Actions reads YAML files from a repo's `.github/workflows/`. Three terms worth telling apart:

| Term | What it is | In the file |
|---|---|---|
| workflow | One file, woken by an event such as `pull_request` or `push` | `on:` |
| job | One unit of work on its own fresh virtual machine; different jobs can run in parallel and don't see each other's files | `jobs.<name>.runs-on` |
| step | One command inside a job; a step that returns non-zero fails the job | `steps:` entries with `uses:` (a packaged action) or `run:` (a shell command) |

Three conventions used throughout this lesson.

- **A thin workflow, a thick script.** Put the real checking commands into [ci.sh](examples/ci.sh) in the repo, and have the workflow just install tools and call `bash ci.sh <stage>`. You can run the exact same commands locally before pushing, without waiting on CI to find out the result.
- **Least privilege.** GitHub's documentation recommends "It's good security practice to set the default permission for the `GITHUB_TOKEN` to read access only for repository contents" — that's `permissions: contents: read`, the same as the SDK's workflow above — and once any permission is stated explicitly, every unstated one becomes `none`.
- **Pin everything that can move on its own.** A tag like `v7` on an action can be moved to point at a different commit. GitHub's documentation states "Pinning an action to a full-length commit SHA is currently the only way to use an action as an immutable release." A runner label like `ubuntu-latest` can move too ([runner-images](https://github.com/actions/runner-images) says it "point[s] towards the newest stable OS version available"), which changes the version of cppcheck and the compiler that apt provides. This lesson therefore uses `ubuntu-24.04`, and sets `timeout-minutes`, because without it, a hung job can run for up to 360 minutes.

### 2. Four checking stages, and making every one able to fail

| Stage | Tool | Catches |
|---|---|---|
| `tests` | Unity + `prove_red.sh` from lesson 6.1 | Wrong logic, and tests that don't actually test anything |
| `format` | clang-format 18.1.3 with [.clang-format](examples/.clang-format) | Code formatted differently than the team agreed, keeping pull request diffs readable |
| `static` | cppcheck | Bugs visible without running the code, such as writing past an array's bounds |
| `cross` | arm-none-eabi-gcc for Cortex-M33 and Cortex-M55 | Logic that compiles on a computer but not on the microcontroller |

The most common CI trap is **a stage that reports a problem but still stays green.** We tested this with both tools this lesson uses, and got the same result both times.

- `clang-format --dry-run` finds badly formatted code, prints a warning, and returns 0. You must add `--Werror` to get 1.
- `cppcheck` finds an `arrayIndexOutOfBounds`, prints `error:`, and returns 0. You must add `--error-exitcode=1`.
- A command ending in `|| true`, or a step with `continue-on-error: true`, is always green no matter what happens inside.
- In bash, `( steps ) || rc=$?` turns off `set -e` for every command inside the subshell — a command that fails partway through gets skipped, and the whole thing ends with 0. ([ci.sh](examples/ci.sh) notes this inside its `run_stage` function.)

The `cross` stage uses Cortex-M33's flags, following the SDK template's own library Makefile.

```make
# Toolchain (same as project)
GCC_PATH := /Applications/mtb-gcc-arm-eabi/14.2.1/gcc/bin
CC := $(GCC_PATH)/arm-none-eabi-gcc
AR := $(GCC_PATH)/arm-none-eabi-ar

# Compiler flags for PSoC Edge Cortex-M33 (MUST match project: softfp)
CFLAGS := -mcpu=cortex-m33 -mthumb -mfloat-abi=softfp -mfpu=fpv5-sp-d16
```

Source: [bento_libs/claw/kit-pse84-ai/tesaiot/Makefile lines 25-31](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/tesaiot/Makefile#L25-L31) (Apache-2.0, tesaiot-pse84-devkit-sdk)

Notice `GCC_PATH` points at a folder on one particular macOS machine — this line doesn't work as-is on a CI runner. This is exactly the kind of hidden assumption about a machine that CI helps surface. And the compiler that line names is ModusToolbox's GCC 14.2.1, while `gcc-arm-none-eabi` from Ubuntu 24.04's apt is 13.2.1 — so the `cross` stage checks that the logic **compiles** for the board's CPU, not that it produces the exact same binary as a real build.

### 3. What CI on a public runner can check, and what needs a board

| CI on a public runner can check | Needs a real board |
|---|---|
| Logic that lives behind a seam (lesson 6.1) | Interrupt and timer timing (lessons 4.1, 4.2) |
| Code formatting, and bugs statically analysable | Cache and DMA ordering with barriers (lesson 4.4) — that lesson's host tests can simulate it, but can't prove it |
| Logic that compiles for Cortex-M33 and Cortex-M55 | Real signals on the UART, I2C, SPI wires (module 5) |
| Files that shouldn't be in the repo, such as what lesson 2.3's hook checks | A real watchdog reset, and a board booting after an unplug-replug (lessons 4.3, 2.1) |

Why not build the whole firmware image in CI? The same Makefile states one reason plainly: "Source files (tesaiot_*.c) are proprietary", distributing a prebuilt `libtesaiot.a` instead ([lines 10-11](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/tesaiot/Makefile#L10-L11)). And the SDK's own git repository has no `.a` files at all, since `.gitignore` excludes them — lesson 2.1 has you build from the release zip instead. A full build therefore needs ModusToolbox fully installed, along with the release's package, which you did on your own machine following [lesson 2.1](../../m02-build-and-version/l01-toolchain-first-build/README.md) and [the TESAIoT firmware course's build and flash steps](../../../tesaiot-firmware-stack/m01-getting-started/l01-toolchain-and-master-template/README.md).

The way to connect a board to CI is a self-hosted runner with a board plugged in (hardware-in-the-loop), but GitHub's documentation warns: "Self-hosted runners should almost never be used for public repositories on GitHub, because any user can open pull requests against the repository and compromise the environment." A public repository should therefore keep board testing in a private repository, or do it by hand, and record the evidence.

## Worked example

The [examples/](examples/) folder has five files.

- [host-tests.yml](examples/host-tests.yml): the smallest usable workflow — one job, running lesson 6.1's tests. Comments in the file explain workflow, job and step.
- [ci.sh](examples/ci.sh): the four checking stages. Every stage ends with `PASS`, `FAIL`, or `NOT CHECKED` (the tool is missing, or there's no file to check), and `NOT CHECKED` returns non-zero, just like `FAIL`.
- [.clang-format](examples/.clang-format): this course's code style. Lesson 6.1's C files are already formatted with this file.
- [check_workflow.py](examples/check_workflow.py): checks a workflow's structure against this lesson's four-job rule, locally (it does not run a real workflow).
- [.gitignore](examples/.gitignore): excludes the `.venv/` created during practice.

Run all four stages against lesson 6.1's code locally (you must have cloned Unity into lesson 6.1's `examples/unity` first):

```sh
cd examples
python3 -m venv .venv
.venv/bin/pip install clang-format==18.1.3 pyyaml==6.0.3
SRC_DIR=../../l01-unit-tests-on-host/examples TEST=../solution/test_level_alarm.c \
  CLANG_FORMAT=.venv/bin/clang-format bash ci.sh all
```

The result we got: `tests`, `format`, `static` and `cross` all show `PASS`. If your machine has no cppcheck, `static` will show `NOT CHECKED`, and the command ends with a non-zero status — which is correct.

**Try making each stage turn red, predicting the result first.** Do this in a copy of lesson 6.1's example folder, not the real files.

1. `format`: remove the spaces around `=` in one line, `a->count = 0u;`.
2. `static`: add a function with a loop `for (int i = 0; i <= 4; i++)` writing into `int history[4]`.
3. `cross`: add `_Static_assert(sizeof(long) == 8, "assumes a 64-bit long");` right after the `#include`s. The `tests` stage still passes, because `long` on a 64-bit computer is 8 bytes — but `cross` turns red, because on Cortex-M it's 4 bytes. A data type's size depends on the architecture (lesson 1.1).
4. `tests`: with `TEST=test_level_alarm_first.c`, both tests pass, yet this stage turns red, because `prove_red.sh` finds a bug that survives.

## Practice

Open [practice/firmware-ci.yml](practice/firmware-ci.yml). The `tests` job is already given; there are 6 gaps to fill in — more than in earlier lessons, matching this module's pace.

1. Run on every pull request.
2. Restrict `GITHUB_TOKEN`'s permission to read-only.
3. Pin every action with a full commit SHA.
4. The `format` job: install the pinned version of clang-format, then run `bash ci.sh format`.
5. The `static-analysis` job: install cppcheck, then run `bash ci.sh static`.
6. The `cross-compile` job: install gcc-arm-none-eabi, then run `bash ci.sh cross`.

Check it locally before pushing:

```sh
cd examples
.venv/bin/python check_workflow.py ../practice/firmware-ci.yml
```

Before you fill anything in, the checker shows `10 failed`. The work is done once it shows `0 failed`. This checker also catches `|| true` and `continue-on-error` — try adding one and watch it turn red.

## Solution

Try it yourself for at least 15 minutes first, then open [solution/firmware-ci.yml](solution/firmware-ci.yml). We checked the solution: the checker shows `21 passed, 0 failed`. Worth comparing:

- The `format` job installs clang-format via pip at version 18.1.3, instead of whatever ships with the runner, because the `ubuntu-24.04` image carries three clang-format versions (16.0.6, 17.0.6, 18.1.3, per the [image's list](https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Readme.md), 20260920 revision), and different versions can format differently. pip gives the same version on Linux, Windows and macOS runners alike.
- `concurrency` with `cancel-in-progress: true` cancels an older run when a new push lands on the same pull request, while the SDK's workflow sets it to `false`, letting a run that's already started finish. Which is right depends on the job: checking old code is pointless once new code exists, but a notification cancelled partway through might never reach its destination.

## Check your understanding

Answer the 5 questions in [quiz.yaml](quiz.yaml) (shown at the bottom of this page on the website), covering all three objectives. Getting 4 or more right counts as finishing the lesson.

## Lab

**Task:** have GitHub check your work on every pull request, and prove it can turn red.

1. Create your own repository (private or public), laid out like this: `ci.sh` and `.clang-format` from this lesson at the root; a `host-tests/` folder holding the files from lesson 6.1's `examples/` (except `unity/` and `build/`), with your fully-completed `test_level_alarm.c`; and the workflow you wrote, at `.github/workflows/firmware-ci.yml`. (If you did lesson 6.1's lab with your own logic instead, you can use that — just adjust the filenames in `prove_red.sh` to match.)
2. Push, then open the Actions tab. All four jobs must be green.
3. Open a pull request that plants one bug from the worked example section. Check that the job that should turn red actually does, then close that pull request without merging.
4. Move one check from lesson 2.3's `pre-commit` hook into a stage inside `ci.sh`, and prove with a pull request that `--no-verify` can no longer skip it.
5. If you have a board, write a short note on what kind of change in this repository could leave CI green while you'd still need to flash a board to check it — and what exactly you'd be checking.

**Evidence to keep in your portfolio:** the repository's link, a picture or link of a fully green run, the link to the red pull request with a note on what the bug was and which job caught it, and your answer to question 5.

## Going further

- Read the SDK's [notify-flash-relay.yml](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/.github/workflows/notify-flash-relay.yml) workflow in full. What does its second step check, and why did the author separate it from another workflow that also runs on a release? (The header comment refers to `firmware-index.yml`, which doesn't exist at this commit, but the reasoning is fully there in the comments.)
- Try turning on cppcheck's `--enable=style` against your own code. Which messages are useful, and which should be suppressed with `// cppcheck-suppress` and a reason?

Module 6, and this course, are now finished. Go back and look at the [end-of-module checkpoint](../README.md) and the [course page](../../README.md). The next course that builds on everything here is the [TESAIoT Firmware course](../../../tesaiot-firmware-stack/m01-getting-started/l01-toolchain-and-master-template/README.md).

## Reflect

- If CI has been green every time for six months, how would you know it's still checking anything?
- Which part of your work still relies on "it passes on my machine," and what would it take to move it into CI?

## References

- [GitHub Actions documentation](https://docs.github.com/en/actions)
- [ClangFormat](https://clang.llvm.org/docs/ClangFormat.html)
- [Cppcheck](https://cppcheck.sourceforge.io/)
- [GitHub Docs: Security hardening for GitHub Actions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions)
- [GitHub Docs: Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [actions/runner-images](https://github.com/actions/runner-images)
