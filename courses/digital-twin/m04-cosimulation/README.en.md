
# Module 4 — Firmware–Twin Co-simulation

*Firmware–Twin Co-simulation* · [Firmware Development with the VS Code-based TESA Digital Twin](../README.md) course

## Objectives

Run real firmware alongside the Twin, prove the input–output path with evidence, measure latency, and tell apart problems on the firmware side from problems on the host side.

## Lessons

| # | Lesson | Content |
|---|---|---|
| 1 | [Co-simulation: proving I/O, measuring latency, and isolating problems](l01-firmware-twin-cosim/README.md) | Getting a stable bring-up first, proving the input/output path, using an external web-app as a second layer of evidence, measuring latency, and troubleshooting layer by layer |
| 2 | [Lab: full-cycle I/O with co-simulation](l02-lab/README.md) | Co-sim bring-up, proving the input and output paths, recording latency, and (recommended) using the web-app ex05 as a second mirror |

Approximate time per the original: about 3 hours (lessons) + a 2.5–3 hour lab.

Accompanying sheets and templates (in the `resources/` folder of lesson 1):

- [cosim-checklist.md](l01-firmware-twin-cosim/resources/cosim-checklist.md)

## Checkpoint

Before moving to the next module, check that you can do the following:

- [ ] A heartbeat on both the host side and the firmware side (sim or board)
- [ ] Evidence of the input and output paths
- [ ] A rough latency figure for at least one point
- [ ] cosim-checklist.md filled in completely

[← Module 3](../m03-virtual-device/README.md) · [Course page](../README.md) · [Module 5 →](../m05-telemetry-cloud/README.md)
