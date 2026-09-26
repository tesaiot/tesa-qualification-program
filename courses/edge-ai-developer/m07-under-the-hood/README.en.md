# Module 7 — Under the hood and extending the firmware

> Under the hood and extending the firmware · [Course page](../README.md)

Take apart the stack from MicroPython across the IPC, to ai_engine and the NPU, then use that map to add your own model so it shows up in edge_ai.models().

## Module goal

Stop being just an API user, and start being someone who can read, fix, and extend the stack.

## Lessons

| Lesson | Topic | Time (min) | Slides |
|---|---|---|---|
| [7.1](l01-edge-ai-stack/README.md) | The Edge AI stack: tri-core, ai_engine, the IPC model link, and TFLite-Micro | 70 | [slides.md](l01-edge-ai-stack/slides.md) |
| [7.2](l02-trace-the-stack-lab/README.md) | Hands-on: tracing the stack from MicroPython | 75 | [slides.md](l02-trace-the-stack-lab/slides.md) |
| [7.3](l03-add-your-own-model/README.md) | Adding your own model: three edits, the four-function contract, and Vela | 70 | [slides.md](l03-add-your-own-model/slides.md) |
| [7.4](l04-extend-model-lab/README.md) | Hands-on: making a new model show up in edge_ai.models() | 75 | [slides.md](l04-extend-model-lab/slides.md) |

Lessons come in pairs: a concept lesson followed by a **hands-on** lesson with a practice file, a solution, and a lab.

## Module checkpoint

You pass this module once you can do all of the following (details are in the **Lab** section of each hands-on lesson):

- [ ] Explain the stack, and point to the source function or field for at least one point in each of the three layers (transport, control, result) (lesson 7.2).
- [ ] A newly added model raises `edge_ai.count()`, its name shows up in `edge_ai.models()`, and selecting and running it gets a real verdict on the board (lesson 7.4).
