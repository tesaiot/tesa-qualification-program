# Module 3 · Debugging with SWD and GDB

**Module goal:** halt a program, inspect values, and find the cause of a fault from evidence.

Status: **alpha** (experimental) · Approximate time: 140 minutes

Every lesson has content, examples you can run on your computer, practice with a solution, a check for understanding, and a lab. The course code runs and has been checked on a computer; the on-board labs are still waiting for a teaching trial.

| Lesson | Topic | Time |
|---|---|---|
| [c-found.m03.l01](l01-swd-and-gdb/README.md) | SWD and GDB basics | 70 min |
| [c-found.m03.l02](l02-diagnosing-faults/README.md) | Diagnosing faults from evidence | 70 min |

## End-of-module checkpoint

- [ ] Set a breakpoint, inspect variables, and view a backtrace on a real board, and know how to start a debug session without leaving CM33 stuck in the boot ROM.
- [ ] Write up one diagnosis that separates at least three hypotheses with evidence.
- [ ] Pass every test in the `06_diagnose.c` exercise, including the one requiring you to answer "cannot be measured" when the counter is cleared mid-measurement.
