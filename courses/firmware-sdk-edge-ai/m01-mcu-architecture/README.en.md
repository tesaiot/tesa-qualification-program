
# Module 1 — MCU Architecture and Firmware SDK Structure

*MCU Architecture and Firmware SDK Structure* · [TESA Firmware SDK for Edge AI](../README.md) course

## Objectives

Set the mental map for the whole course: know which domain of the PSOC™ Edge E84 each kind of work belongs in, and which software layer each piece of code belongs in, before installing any tools in the next module. This module does not yet flash a board.

## Lessons

| # | Lesson | Content |
|---|---|---|
| 1 | [Multi-domain MCU architecture and Firmware SDK layers](l01-architecture-and-sdk-layers/README.md) | Reading the PSOC™ Edge E84's multi-domain map, and the HAL/BSP · Driver API · Utility · Application software layers, before writing any real code |
| 2 | [Lab: matching MCU domains to SDK layers](l02-lab/README.md) | A conceptual lab (no board flashing needed): filling in a domain-to-task matching table, labelling software layers, and answering two combined scenario questions |

Approximate time per the original: about 2.5–3 hours (lessons) + a 30–45 minute lab.

Accompanying sheets and templates (in the `resources/` folder of lesson 1):

- [sdk-layer-cheatsheet.md](l01-architecture-and-sdk-layers/resources/sdk-layer-cheatsheet.md)

## Checkpoint

Before moving to the next module, check that you can do the following:

- [ ] Match 4 kinds of work to the M55 / M33 + NNLite / Ethos-U55 domains, with reasons
- [ ] Split the steps of an example task into HAL/BSP · Driver API · Utility · Application
- [ ] Score at least 8 of 10 on the true/false checklist in the lab
- [ ] Explain how an SDK differs from an IDE

[Course page](../README.md) · [Module 2 →](../m02-toolchain/README.md)
