
# Module 5 — Sensor Data and Edge AI Preparation

*Sensor Data and Edge AI Preparation* · [TESA Firmware SDK for Edge AI](../README.md) course

## Objectives

Get sensor data ready for Edge AI: read at a fixed period, filter, normalise, arrange it into data windows, and pass it on to a host or a Digital Twin.

## Lessons

| # | Lesson | Content |
|---|---|---|
| 1 | [A sensor stream ready for Edge AI](l01-sensor-data-for-edge-ai/README.md) | From a sensor pin to a stream ready for a model: a fixed period, filters, normalising, data windows, and passing data on to a host |
| 2 | [Lab: a sensor stream and a data window ready for AI](l02-lab/README.md) | Reading two kinds of sensor with a fixed-period task, filtering or normalising, building a data window, then choosing an extension (fusion, host telemetry, or an event) |

Approximate time per the original: about 3.5–4 hours (lessons) + a 2.5–3.5 hour lab.

Accompanying sheets and templates (in the `resources/` folder of lesson 1):

- [sensor-ai-prep.md](l01-sensor-data-for-edge-ai/resources/sensor-ai-prep.md)

> The C code in this module uses the API of the TESAIoT Bitstream firmware, which is not yet open source. Read the note at the top of the [lesson](l01-sensor-data-for-edge-ai/README.md) before you start.

## Checkpoint

Before moving to the next module, check that you can do the following:

- [ ] Read at least two kinds of sensor in a fixed-period task
- [ ] Have at least one filter or normalisation step in the lab code
- [ ] A data window produces a summary vector at least once per second
- [ ] The table in sensor-ai-prep.md and a short report are both filled in completely

[← Module 4](../m04-rtos/README.md) · [Course page](../README.md) · [Module 6 →](../m06-mqtt/README.md)
