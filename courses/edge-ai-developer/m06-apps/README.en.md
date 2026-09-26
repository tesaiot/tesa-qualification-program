# Module 6 — Edge AI apps

> Edge AI apps · [Course page](../README.md)

Build an app focused on a single model, wire a verdict to an action through a pipeline that guards against false positives, fuse it with a raw sensor, and publish events over MQTT.

## Module goal

Turn a model's answer into a trustworthy action, and send it off the board with discipline.

## Lessons

| Lesson | Topic | Time (min) | Slides |
|---|---|---|---|
| [6.1](l01-focused-apps/README.md) | Six models and the edge_ai API: an app focused on one model | 70 | [slides.md](l01-focused-apps/slides.md) |
| [6.2](l02-focused-app-lab/README.md) | Hands-on: our own focused app | 75 | [slides.md](l02-focused-app-lab/slides.md) |
| [6.3](l03-action-pipeline/README.md) | An action pipeline: CONF_FLOOR, debounce, cooldown and on_result | 70 | [slides.md](l03-action-pipeline/slides.md) |
| [6.4](l04-action-pipeline-lab/README.md) | Hands-on: an action pipeline that guards against false positives | 75 | [slides.md](l04-action-pipeline-lab/slides.md) |
| [6.5](l05-sensor-fusion/README.md) | Sensor fusion: a model's verdict with a raw sensor | 70 | [slides.md](l05-sensor-fusion/slides.md) |
| [6.6](l06-fusion-iot-lab/README.md) | Hands-on: publishing a fused event to MQTT | 75 | [slides.md](l06-fusion-iot-lab/slides.md) |

Lessons come in pairs: a concept lesson followed by a **hands-on** lesson with a practice file, a solution, and a lab.

## Module checkpoint

You pass this module once you can do all of the following (details are in the **Lab** section of each hands-on lesson):

- [ ] A single-model focused app with a clean UI, targeting a model with `find_model()`, showing the verdict, every class's bar, and latency, with a counter that genuinely fires when the target class crosses `CONF_FLOOR`, retargetable to at least two models (lesson 6.2).
- [ ] A debounced action pipeline where the target class continuing triggers a real action, while a brief flicker of the signal is guarded against (lesson 6.4).
- [ ] A fused decision (verdict AND a raw gate) genuinely publishes to MQTT, once per event, while gentle motion is never sent (lesson 6.6).
