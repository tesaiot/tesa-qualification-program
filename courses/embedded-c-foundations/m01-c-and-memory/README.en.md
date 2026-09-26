# Module 1 · C for microcontrollers and memory

**Module goal:** write C that works with bits, registers and memory safely on a microcontroller.

Status: **alpha** (experimental) · Approximate time: 210 minutes

Every lesson has content, examples you can run on your computer, practice with a solution, a check for understanding, and a lab. The course code runs and has been checked on a computer; the on-board labs are still waiting for a teaching trial.

| Lesson | Topic | Time |
|---|---|---|
| [c-found.m01.l01](l01-c-on-a-microcontroller/README.md) | C on a microcontroller | 70 min |
| [c-found.m01.l02](l02-memory-map-stack-heap/README.md) | The memory map, stack and heap | 70 min |
| [c-found.m01.l03](l03-structs-pointers-buffers/README.md) | Structs, pointers and a ring buffer | 70 min |

## End-of-module checkpoint

- [ ] Read the SDK's `06_raw_register_access.c` example and explain the read-modify-write step, line by line.
- [ ] Identify whether a variable in an example program lives in the stack, the heap, or static memory.
- [ ] Read a real task's stack counter on the board, and judge with a calculation whether it is still safe.
- [ ] Pass every test in the `03_ring_buffer.c` exercise, and explain who owns the data in the buffer at each point.
