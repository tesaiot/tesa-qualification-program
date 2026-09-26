# Module 1 — Getting started: run the real thing, then take it apart

> Getting started: run the real thing, then take it apart · [Course page](../README.md)

Run a real edge AI model first, then take apart the sensor app and the edge AI app until you can see the shared four-beat structure, the model registry, and the path from a verdict to an action.

## Module goal

See where the whole course is headed from day one: query the model registry, select a model, read its answer, and wire it to an action on the board — while getting to know the shared structure every program in the course uses.

## Lessons

| Lesson | Topic | Time (min) | Slides |
|---|---|---|---|
| [1.1](l01-edge-ai-lifecycle/README.md) | What edge AI is: the five-stage data lifecycle and where a model can run | 55 | [slides.md](l01-edge-ai-lifecycle/slides.md) |
| [1.2](l02-edge-ai-module/README.md) | The edge_ai module: query the model registry, select, then read the answer | 60 | [slides.md](l02-edge-ai-module/slides.md) |
| [1.3](l03-first-inference-lab/README.md) | Hands-on: our first model menu | 70 | [slides.md](l03-first-inference-lab/slides.md) |
| [1.4](l04-sensor-app-anatomy/README.md) | Taking apart the sensor app: the shared four-beat structure of every program | 65 | [slides.md](l04-sensor-app-anatomy/slides.md) |
| [1.5](l05-sensor-remix-lab/README.md) | Hands-on: our own Tilt Monitor remix | 75 | [slides.md](l05-sensor-remix-lab/slides.md) |
| [1.6](l06-edge-ai-app-anatomy/README.md) | Taking apart the edge AI app: the model registry, verdicts and actions | 65 | [slides.md](l06-edge-ai-app-anatomy/slides.md) |
| [1.7](l07-verdict-action-lab/README.md) | Hands-on: from a verdict to an action on the board | 75 | [slides.md](l07-verdict-action-lab/slides.md) |

Lessons come in pairs: a concept lesson followed by a **hands-on** lesson with a practice file, a solution, and a lab.

## Module checkpoint

You pass this module once you can do all of the following (details are in the **Lab** section of each hands-on lesson):

- [ ] Run the `edge_ai` menu and read live results — both the winning class (`label`) and the confidence (`conf`) change with real gestures or sound (lesson 1.3).
- [ ] A remix that genuinely differs from the original, with every part explained by which beat it belongs to (lesson 1.5).
- [ ] Genuinely remix `s03_anatomy_edgeai.py`: swap the model (change `MODEL_KEYWORD` and `TARGET_CLASS`), and trigger an action when a matching verdict occurs (lesson 1.7).
