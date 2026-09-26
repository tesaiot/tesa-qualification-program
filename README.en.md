# TESA Open Knowledge

Open courses in embedded systems, AIoT and Edge AI from the **Thai Embedded Systems Association (TESA)**, สมาคมสมองกลฝังตัวไทย.
Free to learn, one lesson at a time, with slides, example code that really runs, practice files and solutions, for developers,
the general public, entrepreneurs, educators and students.

**Website:** https://tesaiot.github.io/tesa-qualification-program/ · *ภาษาไทย: [README.md](README.md)*

> **Anyone may use this material, and everyone must credit TESA every time.**
> The required wording, with examples for slides, course syllabi, printed handouts and code repositories, is in
> [ATTRIBUTION.md](ATTRIBUTION.md).

## What TESA Open Knowledge is

We want anyone curious about embedded systems to learn from real hardware: from the first LED on a board to a device that sends
data securely to an IoT platform and runs an AI model on itself. Lessons are written in Thai with English technical terms, and
are open to teach, adapt and build on.

Every lesson declares which skills it develops and to what level, using one shared [skill map](skills/README.md). That data is
the basis of the Skillset Mapping of the **TESA Qualification Program (TQP), a joint TESA × Infineon programme.**

TQP is a v0.1 design and is **not yet open for candidates**; no credential can be obtained today. The L1–L5 levels are in
[tqp/levels.en.md](tqp/levels.en.md) and the credential design in [tqp/certification.en.md](tqp/certification.en.md).

## Pathways

| Pathway | For |
|---|---|
| **Explorer (general public)** | No programming needed to start: a first line of MicroPython in the BENTO Emulator, no board required. |
| **Entrepreneur** | What Edge AI and IoT can do, how to judge cost and risk, and how to brief developers. No code. |
| **Developer** | Start at the level that matches your background, then move on to C firmware, Secure IoT and Edge AI on real boards. |
| **Student** | From AIoT in Action to C firmware and a capstone kept as a GitHub portfolio. |
| **Educator** | The Educator Kit for adopting these courses in your own teaching. |

Each pathway's courses, hours and exit point are in [catalog/tracks.yaml](catalog/tracks.yaml).

## Courses

| Course | Level | Status |
|---|---|---|
| [Explorer: Meet Embedded Systems](courses/explorer/README.en.md) | L1 Aware | alpha |
| [AIoT in Action: From Touch Screen to IoT Platform (MicroPython)](courses/aiot-micropython/README.en.md) | L2 Guided | alpha |
| [Edge AI & IoT for Product Decisions](courses/edge-ai-iot-for-business/README.en.md) | L1 Aware | alpha |
| [Product Industrial Design (Blender & Twin)](courses/product-design/README.en.md) | L2 Guided | alpha |
| [Electronics & Test Instruments for Embedded Developers](courses/electronics-and-instruments/README.en.md) | L2 Guided | pre-alpha |
| [Embedded C Foundations on PSoC Edge](courses/embedded-c-foundations/README.en.md) | L3 Independent | pre-alpha |
| [TESA Firmware SDK for Edge AI](courses/firmware-sdk-edge-ai/README.en.md) | L3 Independent | alpha |
| [Firmware Development with the VS Code-based TESA Digital Twin](courses/digital-twin/README.en.md) | L3 Independent | alpha |
| [Secure IoT with OPTIGA™ Trust M](courses/secure-iot-optiga/README.en.md) | L3 Independent | pre-alpha |
| [Edge AI Developer: From Sensor to On-Device Model](courses/edge-ai-developer/README.en.md) | L3 Independent | pre-alpha |
| [Educator Kit](courses/educator-kit/README.en.md) | L3 Independent | alpha |
| [Fundamental of Embedded Systems Developer I–II (Game Console)](https://advance-innovation-centre-aic.github.io/embedded-systems-for-game_console_developer/) · external course | L2 Guided | stable |

Status: **pre-alpha** outline, content incomplete · **alpha** complete draft tested by the author · **beta** two-key reviewed and
piloted by someone other than the author · **stable** ready to teach. See [GOVERNANCE.md](GOVERNANCE.md). External courses are
maintained by their owners and registered in [catalog/courses.yaml](catalog/courses.yaml), pinned to an exact commit.

## How to learn

All you need is a browser and [BENTO IDE](https://ide.tesaiot.dev/), which includes the BENTO Emulator, so no board is required.
With an Eva Kit or TESAIoT Dev Kit board you see the result on real hardware. A lesson takes 30–60 minutes and runs in this order:

1. **Objectives and warm-up**: what you will be able to do, and two questions reviewing earlier lessons.
2. **See it work first**: predict, then run the finished program on a board or the emulator.
3. **Concept and worked example**: short chunks, then a step-by-step example.
4. **Practice, then the solution**: more blanks as you progress; try for at least 15 minutes before looking.
5. **Check, lab and reflection**: 80% or more on the check completes the lesson; keep your lab evidence in a portfolio.

## Contributing

Anyone can report an error, translate a lesson or write a new one. Start with [CONTRIBUTING.en.md](CONTRIBUTING.en.md).
Authors use the [templates](templates/) and the [authoring guide](templates/AUTHORING.md) (Thai). Every commit needs a DCO
sign-off and every pull request must pass `python3 tools/validate.py`. The community follows the
[Code of Conduct](CODE_OF_CONDUCT.en.md); decisions and two-key review are described in [GOVERNANCE.md](GOVERNANCE.md).
Report vulnerabilities or leaked secrets privately, as described in [SECURITY.md](SECURITY.md).

## Licences

| Part | Licence |
|---|---|
| Lesson content, slides and TESA's own images | [CC BY 4.0](LICENSES/CC-BY-4.0.txt) |
| New code | [Apache-2.0](LICENSE) |
| Code imported from the AIC AIoT in Action course | [MIT](LICENSES/MIT.txt) |
| The skill map in `skills/` | [CC BY-SA 4.0](LICENSES/CC-BY-SA-4.0.txt) |
| Third-party images | Their own licence; see each course's `credits.yaml` |

The TESA, TQP, TESAIoT and BENTO names and logos and Infineon's trademarks are not covered by these licences; see
[TRADEMARKS.md](TRADEMARKS.md).

## Sources and credits

- Made and published by the Thai Embedded Systems Association (TESA), สมาคมสมองกลฝังตัวไทย.
- The AIoT in Action course is adapted from "AIoT in Action — Embedded Systems for AIoT Developer", © 2026 Assoc. Prof. Wiroon
  Sriborrirux, Advance Innovation Centre (AIC), Burapha University · BENTO & TESAIoT (CC BY 4.0 / MIT).
- The TESA Firmware SDK, Digital Twin and Product Design courses are based on original material by drsanti
  (https://github.com/drsanti), produced with funding from TESA.
- The skill map is adapted from the Embedded Systems Engineering Roadmap by Meysam Parvizi (CC BY-SA 4.0).
- Infineon®, PSOC™, ModusToolbox™ and OPTIGA™ are trademarks of Infineon Technologies AG. Infineon code examples are referenced
  by link.

Full details: [NOTICE.md](NOTICE.md) · academic citation: [CITATION.cff](CITATION.cff) · release history: [CHANGELOG.md](CHANGELOG.md)

## How to cite TESA

> "TESA Open Knowledge" by the Thai Embedded Systems Association (TESA),
> https://github.com/tesaiot/tesa-qualification-program, licensed under CC BY 4.0

When you use only some lessons or courses, name them as shown in [ATTRIBUTION.md](ATTRIBUTION.md).
