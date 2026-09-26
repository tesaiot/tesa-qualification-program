# Module 6 · Unit tests and CI

**Module goal:** test firmware logic on the host computer, and have CI check every change.

Status: **alpha** (experimental) · Approximate time: 140 minutes

Every lesson has content, examples you can run on your computer, practice with a solution, a check for understanding, and a lab. The course code runs and has been checked on a computer; the on-board labs are still waiting for a teaching trial.

| Lesson | Topic | Time |
|---|---|---|
| [c-found.m06.l01](l01-unit-tests-on-host/README.md) | Unit tests on the host | 70 min |
| [c-found.m06.l02](l02-ci-for-firmware/README.md) | CI for firmware | 70 min |

## End-of-module checkpoint

- [ ] Have at least five unit tests that run on the host, and prove that at least one of them can genuinely fail.
- [ ] Plant at least three kinds of bug in your logic, and have the tests catch every one (none survives).
- [ ] Have a CI workflow that runs tests, checks formatting, runs static analysis, and compiles for Cortex-M on every pull request.
- [ ] Have a pull request where CI turned red because of a deliberately planted bug, as proof the checks can actually fail.
