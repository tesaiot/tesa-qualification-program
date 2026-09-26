
# Module 5 — Telemetry and Cloud Simulation

*Telemetry and Cloud Simulation* · [Firmware Development with the VS Code-based TESA Digital Twin](../README.md) course

## Objectives

Expand the data pipe outside Studio: classify telemetry/state/event, check the stream's quality, set up a broker in the Twin host, do pub/sub, and experiment with a controlled unstable network.

## Lessons

| # | Lesson | Content |
|---|---|---|
| 1 | [The telemetry pipe, MQTT on the Twin, and fault injection](l01-telemetry-cloud-simulation/README.md) | Separating Telemetry/State/Event, telling apart the Live Data pipe from MQTT, using the web-app ex08/ex09 to check the stream, and designing a broken-network experiment |
| 2 | [Lab: the telemetry pipe and MQTT on the Twin](l02-lab/README.md) | Designing topics, checking Live Data quality with ex08, setting up a broker then subscribing with ex09, and experimenting with lossy/reconnect |

Approximate time per the original: about 4 hours (lessons) + a 3.5–4 hour lab.

Accompanying sheets and templates (in the `resources/` folder of lesson 1):

- [telemetry-mqtt-lab-notes.md](l01-telemetry-cloud-simulation/resources/telemetry-mqtt-lab-notes.md)

## Checkpoint

Before moving to the next module, check that you can do the following:

- [ ] A topic table separating Telemetry / State / Event
- [ ] At least one pub/sub pair through the broker in Studio
- [ ] At least one fault-injection case with a recorded result
- [ ] telemetry-mqtt-lab-notes.md filled in completely

[← Module 4](../m04-cosimulation/README.md) · [Course page](../README.md) · [Module 6 →](../m06-integration/README.md)
