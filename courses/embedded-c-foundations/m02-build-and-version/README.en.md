# Module 2 · Building with ModusToolbox, Make and Git for firmware

**Module goal:** build and flash firmware reproducibly every time, and keep a history of changes with Git.

Status: **alpha** (experimental) · Approximate time: 210 minutes

Every lesson has content, examples you can run on your computer, practice with a solution, a check for understanding, and a lab. The course code runs and has been checked on a computer; the on-board labs are still waiting for a teaching trial.

| Lesson | Topic | Time |
|---|---|---|
| [c-found.m02.l01](l01-toolchain-first-build/README.md) | The toolchain and a first build | 70 min |
| [c-found.m02.l02](l02-make-and-build-flags/README.md) | Make and build flags | 70 min |
| [c-found.m02.l03](l03-git-for-firmware/README.md) | Git for firmware work | 70 min |

## End-of-module checkpoint

- [ ] Build the firmware template from the release zip successfully, flash it to the board, see the `[HB]` line on the console, and record the tool versions used.
- [ ] Enable one example with a Make variable, see its effect on the board, and measure how much the firmware size changed.
- [ ] Have a repository with no build files and no secrets, with a `pre-commit` hook that passes lesson 2.3's test suite.
