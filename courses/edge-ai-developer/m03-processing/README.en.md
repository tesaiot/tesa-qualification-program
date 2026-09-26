# Module 3 — Processing with maths and physics

> Processing with maths and physics · [Course page](../README.md)

Turn raw numbers into physical quantities (tilt angle, energy, altitude, dBFS), derived values like dew point and heat index, and classify with rules before reaching for ML.

## Module goal

Use maths and physics to give numbers meaning, and know when a plain rule is enough.

## Lessons

| Lesson | Topic | Time (min) | Slides |
|---|---|---|---|
| [3.1](l01-physics-quantities/README.md) | From raw numbers to physical quantities: tilt angle, energy, altitude and dBFS | 65 | [slides.md](l01-physics-quantities/slides.md) |
| [3.2](l02-physics-gauges-lab/README.md) | Hands-on: four physics gauges on screen | 75 | [slides.md](l02-physics-gauges-lab/slides.md) |
| [3.3](l03-rules-before-ml/README.md) | Derived values and rule-based classification: dew point, heat index and a rule ladder | 60 | [slides.md](l03-rules-before-ml/slides.md) |
| [3.4](l04-rule-classifier-lab/README.md) | Hands-on: a rule-based comfort classifier | 75 | [slides.md](l04-rule-classifier-lab/slides.md) |

Lessons come in pairs: a concept lesson followed by a **hands-on** lesson with a practice file, a solution, and a lab.

## Module checkpoint

You pass this module once you can do all of the following (details are in the **Lab** section of each hands-on lesson):

- [ ] A raw signal → a computed quantity → shown on screen, the full loop working for at least one quantity (lesson 3.2).
- [ ] Write your own `classify()` with a rule ladder, and have the board or emulator show a class that genuinely changes as temperature or humidity changes (lesson 3.4).
