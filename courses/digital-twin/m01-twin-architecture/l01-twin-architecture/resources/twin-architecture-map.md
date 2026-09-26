# Twin architecture map — Course 2 M01

**Course 2 · Module 1**

[Lesson](../README.md) · [Lab](../../l02-lab/README.md) · [TOC](../../../README.md)

---

## Terms (one line each)

| Term | One-liner |
|---|---|
| Physical Device | บอร์ด + เซ็นเซอร์จริงบนโต๊ะ |
| Virtual Device | โมเดลซอฟต์แวร์ของอุปกรณ์หนึ่งเครื่อง |
| Digital Twin | Virtual Device + สื่อสาร + จอ + สคริปต์ + cloud sim |
| Firmware Logic | ตรรกะแอปที่ควรพกไปได้ทั้ง Twin และบอร์ด |
| Host | VS Code + Bitstream Studio (หลักในคอร์สนี้) |

---

## Layers you must point to

| Layer | What you often see in the lab |
|---|---|
| VS Code / Host | extension, workspace, toolbar Bitstream/Simulator |
| Firmware Logic | `main`, tasks, encode/publish policy |
| Communication | UART bridge, MQTT broker, BLE host |
| Twin Engine / Virtual Device | state, sim sensors, inject stream |
| Visualization | Telemetry panels, Sensor Studio, 3D |
| Scripts / Events | shake / press / cut-network scenarios (M03+) |
| Cloud / Dashboard | broker topics, Hackathon `web-app/` |

---

## Data pipeline sketch

```text
sensors (real or virtual)
  → firmware (filter / decide / encode)
  → UART | MQTT | BLE
  → host twin state
  → UI / dashboard / cloud
```

| Kind | Meaning |
|---|---|
| Telemetry | ค่าเป็นคาบ |
| State | สถานะระบบ |
| Event | จุดเหตุการณ์ / alert |

---

## Bitstream vs Simulator (remember)

| Source | Need COM? | Typical origin tag |
|---|---|---|
| Bitstream | Yes (open) | uart |
| Simulator | No (closed) | sim |

Only **one** live backend at a time.

---

## Twin enough? / Board required?

| Usually Twin/Sim OK | Usually need real board |
|---|---|
| Mode / logic / JSON format | RF range, pin wiring |
| Repeatable scripted events | Analog noise, power |
| Dashboard wiring | Final sign-off before ship |

---

## Review questions

1. Twin แทนที่บอร์ดจริงได้ 100% หรือไม่ — เพราะอะไร  
2. Data pipeline ช่วยทดสอบอะไร *ก่อน* ส่งขึ้นคลาวด์  
3. จุดที่เฟิร์มแวร์ “คิดว่า” คุยกับฮาร์ดแวร์ อยู่ชั้นไหนในแผนภาพ  

---

## Portals

- [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)  
- [Developer Hub](https://dev.tesaiot.dev/)  
- [Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)  
- [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)  

[Lesson](../README.md) · [Lab](../../l02-lab/README.md) · [M02](../../../m02-vscode-twin/l01-vscode-for-twin/README.md)
