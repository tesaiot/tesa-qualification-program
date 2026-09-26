# Co-sim checklist — Course 2 M04

**Course 2 · Module 4**

[Lesson](../README.md) · [Lab](../../l02-lab/README.md) · [TOC](../../../README.md)

---

## Setup

| Item | Your value |
|---|---|
| Path | Simulator / Board / Both |
| Bitstream Studio version | |
| HEX / firmware id (if board) | |
| Scene / profile used | |
| M03 script name | |

---

## Bring-up

| Check | OK? | Evidence |
|---|---|---|
| Firmware / sim heartbeat | | |
| Host Link stable ≥ 30 s | | |
| Stream visible | | |

---

## Input path (stimulus → firmware)

| Item | Your notes |
|---|---|
| Stimulus method | |
| What firmware showed | |
| Evidence file | |

---

## Output path (firmware → host)

| Item | Your notes |
|---|---|
| Firmware action | |
| What host / Twin showed | |
| Matches M03 WHEN/THEN? | Yes / No |
| Evidence file | |

---

## External consumer — `web-app/ex05` (recommended)

| Item | Your notes |
|---|---|
| `connected` + `route:` shown? | Yes / No |
| Orientation source (`euler` / `quaternion`) | |
| Mask hex (`0x…`) | |
| Horizon / ° moved after stimulus? | Yes / No |
| Evidence file (Studio + ex05 pair) | |

---

## Latency (recommended)

| Trial | Stimulus → log (approx ms) | Log → UI (approx ms) |
|---|---|---|
| 1 | | |
| 2 | | |
| 3 | | |

Suspected delay source:  

---

## Issues found

| Issue | Firmware or Host? | Fix / workaround |
|---|---|---|
| | | |

---

## Quick recall

```text
Bring-up → prove INPUT → prove OUTPUT → note latency → isolate layer
```

| Backend | Use alone |
|---|---|
| Simulator | COM closed |
| Bitstream | COM open |

---

## Portals

- [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)  
- [Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)  
- [Developer Hub](https://dev.tesaiot.dev/)  

[Lesson](../README.md) · [Lab](../../l02-lab/README.md) · [M05](../../../m05-telemetry-cloud/l01-telemetry-cloud-simulation/README.md)
