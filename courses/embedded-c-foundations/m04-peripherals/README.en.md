# Module 4 · Timers, interrupts, watchdogs, DMA and clocks

**Module goal:** use a microcontroller's main peripherals according to the rules of ISR context and RTOS.

Status: **alpha** (experimental) · Approximate time: 280 minutes

Every lesson has content, examples you can run on your computer, practice with a solution, a check for understanding, and a lab. The course code runs and has been checked on a computer; the on-board labs are still waiting for a teaching trial.

| Lesson | Topic | Time |
|---|---|---|
| [c-found.m04.l01](l01-gpio-and-interrupts/README.md) | GPIO and interrupts | 70 min |
| [c-found.m04.l02](l02-timers-and-clocks/README.md) | Timers and clocks | 70 min |
| [c-found.m04.l03](l03-watchdog/README.md) | The watchdog | 70 min |
| [c-found.m04.l04](l04-dma/README.md) | DMA | 70 min |

## End-of-module checkpoint

- [ ] Read a button with an interrupt and debounce it without blocking, with the ISR doing the least possible work and handing off to a task.
- [ ] Calculate a timer's frequency correctly from a BSP setting (a divider of N divides by N+1), and explain what the clock does to accuracy.
- [ ] Explain the correct place to feed the watchdog in an example program, and read a real board's reset cause.
- [ ] Point to where in the SDK's camera driver the cache must be cleaned before DMA can read, and explain why some buffers are placed in memory that bypasses the cache.
