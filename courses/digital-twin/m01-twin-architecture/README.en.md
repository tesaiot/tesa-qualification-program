
# Module 1 — Digital Twin Architecture

*Digital Twin Architecture* · [Firmware Development with the VS Code-based TESA Digital Twin](../README.md) course

## Objectives

Set the mental map for Course 2: separate the Virtual Device, the Digital Twin Platform, the firmware logic, and the host from each other, and know which kind of test the Twin can handle, and which needs a real board.

## Lessons

| # | Lesson | Content |
|---|---|---|
| 1 | [Virtual Device, Digital Twin, and the world of real firmware](l01-twin-architecture/README.md) | The meaning of Virtual Device and Digital Twin, the layered architecture, the two live paths (Bitstream and Simulator), and the decision criteria for when a real board is needed |
| 2 | [Lab: mapping the Twin architecture](l02-lab/README.md) | Defining the terms in your own words, drawing the data flow, and filling in a decision table for which tests the Twin can handle, and which need a board |

Approximate time per the original: about 2 hours (lessons) + a 30–45 minute lab.

Accompanying sheets and templates (in the `resources/` folder of lesson 1):

- [twin-architecture-map.md](l01-twin-architecture/resources/twin-architecture-map.md)

## Checkpoint

Before moving to the next module, check that you can do the following:

- [ ] Define the three terms in Part A in your own words
- [ ] A data-flow diagram for one example system
- [ ] A decision table of at least 4 rows, with both "the Twin is enough" and "needs a board" rows

[Course page](../README.md) · [Module 2 →](../m02-vscode-twin/README.md)
