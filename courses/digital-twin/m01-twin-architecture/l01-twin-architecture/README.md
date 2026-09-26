---
id: twin.m01.l01
lang: th
title:
  th: Virtual Device, Digital Twin และโลกของเฟิร์มแวร์จริง
  en: Virtual Devices, Digital Twins and Real Firmware
summary:
  th: ความหมายของ Virtual Device และ Digital Twin สถาปัตยกรรมเป็นชั้น เส้นทาง live สองเส้น (Bitstream กับ Simulator) และเกณฑ์ตัดสินใจว่าเมื่อไรต้องใช้บอร์ดจริง
  en: What a Virtual Device and a Digital Twin are, the layered architecture, the two live paths (Bitstream and Simulator) and when the real board is required.
level: L3
time_min:
  concept: 45
  practise: 15
  check: 10
hardware:
  emulator: false
  boards:
  - none
prerequisites: []
objectives:
- th: แยกความหมายของ Physical Device, Virtual Device, Digital Twin Platform และ Host ด้วยคำพูดของตัวเอง
  en: Distinguish Physical Device, Virtual Device, Digital Twin Platform and Host in your own words.
- th: อธิบายว่า Bitstream (UART/บอร์ด) กับ Simulator เป็นเส้นทาง live ที่ใช้ทีละเส้น และบอกเหตุผลที่ไม่ผสมกัน
  en: Explain that Bitstream (UART/board) and Simulator are live paths used one at a time, and why they are not mixed.
- th: ตัดสินใจว่าสถานการณ์ทดสอบหนึ่งใช้ Twin/Simulator ได้พอ หรือต้องยืนยันบนบอร์ดจริง พร้อมเหตุผล
  en: Decide whether a test scenario can use the Twin/Simulator or needs the real board, with a reason.
develops:
- skill: iot.digital-twin
  to: 2
- skill: sys.simulation
  to: 1
- skill: test.sil-hil
  to: 1
context:
  platform: psoc-edge-e84
  host: bitstream-studio
  ide: vscode
  simulator: Bitstream Simulator (not the BENTO Emulator)
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C2/M01/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M01 — Digital Twin Architecture

**Course 2 · Module 1**  
**Suggested time:** ประมาณ 2 ชั่วโมง (แนวคิด + แผนภาพ + เปิดโฮสต์ดูท่อข้อมูล)  
**Format:** บทเรียนเชิงแนวคิด — ยังไม่บังคับสร้าง Virtual Device เต็มรูป (เริ่มลงมือใน [M02](../../m02-vscode-twin/l01-vscode-for-twin/README.md) / [M03](../../m03-virtual-device/l01-virtual-device-modeling/README.md))

[Lab](../l02-lab/README.md) · [Cheatsheet](resources/twin-architecture-map.md) · [← Table of Contents](../../README.md) · [M02 →](../../m02-vscode-twin/l01-vscode-for-twin/README.md)

---

## เป้าหมาย (Learning Outcomes)

เมื่อเรียนจบ คุณควรทำได้ดังนี้:

1. อธิบายแนวคิด **Virtual Device** และ **Digital Twin** ในงาน IoT / Firmware  
2. อธิบายสถาปัตยกรรม **TESA Digital Twin Platform** เป็นชั้น ๆ ที่นำไปแล็บได้  
3. อธิบายการจำลองสัญญาณ เซ็นเซอร์ พฤติกรรมอุปกรณ์ และ **Data Pipeline**  
4. ระบุความสัมพันธ์ระหว่าง **Firmware จริง** กับ **Twin Environment** — เมื่อไรใช้บอร์ด / เมื่อไรใช้ Simulator / เมื่อไรต้องยืนยันบนฮาร์ดแวร์  

โมดูลนี้คือ **แผนที่ความคิด** ของ Course 2 หากเข้าใจสถาปัตยกรรม Twin แล้ว การติดตั้ง VS Code host ([M02](../../m02-vscode-twin/l01-vscode-for-twin/README.md)) และการสร้าง Virtual Device ([M03](../../m03-virtual-device/l01-virtual-device-modeling/README.md)) จะมีโครงที่ชัด

> **แนวทาง “พูดแนวคิด แล้วชี้เครื่องมือจริง”**  
> เอกสารหลักสูตรพูดถึง *engines* ของแพลตฟอร์ม Twin ในระดับสถาปัตยกรรม  
> ในแล็บ โฮสต์หลักคือ **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** + แพ็ก **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** — บทนี้จับคู่แนวคิดกับสิ่งที่คุณเปิดจริงในแล็บ

### Read alongside this chapter

| เอกสาร | ใช้เมื่อ |
|---|---|
| **[Bitstream Studio (Marketplace)](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | VS Code host — telemetry, Sensor Studio, Simulator, MQTT, 3D preview |
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | ตัวอย่างเฟิร์มแวร์ / API ที่จะไหลเข้า Twin |
| **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** | HEX, VSIX, Flasher, `web-app/` dashboards |
| **[ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)** | โมเดล 3D (GLB), texture, cubemap, รูปภาพสำหรับ Twin / Sensor Studio |
| [Course 1 TOC](../../../firmware-sdk-edge-ai/README.md) | พื้นฐาน SDK / sensors / MQTT / BLE |
| [Course 1 M05 — Sensor prep](../../../firmware-sdk-edge-ai/m05-sensor-data/l01-sensor-data-for-edge-ai/README.md) | แหล่งข้อมูลที่จะเข้า pipeline |
| [Course 1 M06 — MQTT](../../../firmware-sdk-edge-ai/m06-mqtt/l01-mqtt-and-mqtts/README.md) | ชั้น cloud ที่ Twin จะจำลอง/ทดสอบ |
| [Bluetooth / local path (C1 M07)](../../../firmware-sdk-edge-ai/m07-ble/l01-ble-connectivity/README.md) | ทางเลือก local เมื่อไม่ใช้ Wi‑Fi |
| [Digital Twin — Wikipedia overview](https://en.wikipedia.org/wiki/Digital_twin) | นิยามทั่วไปนอกคอร์ส (อ่านเสริม) |

---

## 1. Why Digital Twin for Firmware Development

การพัฒนาเฟิร์มแวร์ IoT / Edge AI วันนี้ไม่ใช่แค่ “กะพริบ LED” อีกต่อไป — ระบบมักมี:

- เซ็นเซอร์หลายตัว + กรอง/หน้าต่างข้อมูล  
- RTOS หลาย task  
- Connectivity (Wi‑Fi / MQTT / BLE)  
- โฮสต์ดูค่าแบบเรียลไทม์ และบางครั้งคลาวด์  

ถ้าทดสอบทุกเคสบนบอร์ดจริงอย่างเดียว จะเจอต้นทุนสูง เวลาช้า และความเสี่ยงต่อฮาร์ดแวร์

**Digital Twin** ในหลักสูตรนี้คือการสร้าง **ตัวแทนดิจิทัลของอุปกรณ์** ในสภาพแวดล้อมเสมือน เพื่อพัฒนา ทดสอบ วิเคราะห์ และสาธิตได้โดยไม่ต้องพึ่งบอร์ดจริงตลอดเวลา

### 1.1 What Twin Helps You Do

| ประโยชน์ | ความหมายในแล็บ |
|---|---|
| จำลองฮาร์ดแวร์ | อ่านค่าเซ็นเซอร์/สถานะโดยไม่ต้องต่อทุกพินจริง |
| ทดสอบ logic ซ้ำได้ | สคริปต์เขย่า IMU / กดสวิตช์ / ตัดเน็ต ได้ซ้ำ |
| ลดความเสี่ยงบอร์ด | เคสขอบทำบน Twin ก่อน flash จริง |
| เห็นผลทันที | กราฟ / แผง / 3D / dashboard โฮสต์ |
| เตรียมก่อนคลาวด์ | ตรวจรูปแบบ Telemetry / topic ก่อนขึ้น broker จริง |

> **Key phrase**  
> Twin ไม่ได้แทนที่บอร์ด 100% — มันเป็น **สะพาน** ระหว่างทฤษฎีเฟิร์มแวร์กับการทดสอบที่ทำซ้ำได้

### 1.2 Prerequisites from Course 1

Course 2 สมมติว่าคุณรู้จักแล้ว (หรือทบทวนได้):

| จาก Course 1 | ใช้ใน Course 2 อย่างไร |
|---|---|
| ชั้น SDK / โดเมนชิป | รู้ว่าโค้ดแอปอยู่ที่ไหน |
| Sensors + window | ข้อมูลที่จะเข้า Twin / dashboard |
| MQTT / BLE | ช่องทางที่ Twin และ cloud จะทดสอบ |
| Capstone patterns | โครง task + indication + connectivity |

---

## 2. Virtual Device vs Digital Twin

| คำ | ความหมายในหลักสูตรนี้ |
|---|---|
| **Physical Device** | บอร์ด + เซ็นเซอร์จริง (เช่น PSoC Edge kit) |
| **Virtual Device** | แบบจำลองซอฟต์แวร์ของ *อุปกรณ์หนึ่งตัว* — พิน, เซ็นเซอร์, สถานะ, พฤติกรรมตอบสนอง |
| **Digital Twin (Platform)** | สภาพแวดล้อมที่รวม Virtual Device + การสื่อสาร + visualization + สคริปต์เหตุการณ์ + (บ่อยครั้ง) MQTT/cloud จำลอง |
| **Firmware Logic** | โค้ดตรรกะผลิตภัณฑ์ที่ควรรันได้ทั้งกับ Twin และกับฮาร์ดแวร์ เมื่อแยกชั้น I/O ออกอย่างเหมาะสม |
| **Host / Twin UI** | VS Code extension และแอปโฮสต์ที่คุณใช้ดูผล — ในคอร์สนี้หลักคือ **Bitstream Studio** |

```text
Physical Device  ≈  “ของจริงบนโต๊ะ”
Virtual Device   ≈  “โมเดลอุปกรณ์หนึ่งเครื่องในซอฟต์แวร์”
Digital Twin     ≈  “โรงงานจำลองทั้งระบบ” (โมเดล + สื่อสาร + จอ + สคริปต์ + cloud sim)
```

เป้าหมายออกแบบโค้ดที่ดี:

- แยก **application logic** ออกจากรายละเอียดฮาร์ดแวร์โดยตรงให้มากพอ  
- สลับเป้าหมาย (Simulator / board / MQTT host) ได้โดยไม่เขียนแอปใหม่ทั้งก้อน  

---

## 3. TESA Digital Twin Platform Architecture

หลักสูตรอธิบายแพลตฟอร์มเป็นชุด **engine** ที่ทำงานรอบแกนกลาง — ผู้เรียนไม่ต้องท่องชื่อผลิตภัณฑ์ย่อยทุกตัว แต่ต้องชี้ได้ว่า *แต่ละบทบาท* อยู่ตรงไหนตอนแล็บ

### 3.1 Conceptual engines (curriculum map)

```text
                    ┌─────────────────────────────┐
                    │   Development Host (VS Code) │
                    │   Bitstream Studio / tools   │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
┌──────────────┐     ┌─────────────────────────┐     ┌────────────────┐
│ Firmware     │────►│  Digital Twin Engine     │────►│ Visualization  │
│ Logic        │     │  (state · time · events) │     │ Graphics / UI  │
└──────────────┘     └────────────┬────────────┘     └────────────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              ▼                   ▼                   ▼
      Communication         Scripting /           AI Connectivity
      (UART·MQTT·BLE)       Event / Behavior      (optional path)
              │
              ▼
         Cloud / Broker sim · external dashboards
```

| ชั้น (แนวคิด) | หน้าที่ | สิ่งที่มักเปิดในแล็บนี้ |
|---|---|---|
| **Digital Twin Engine** | จัดการ state ของ Virtual Device, เวลาจำลอง, ประสานเหตุการณ์ | สถานะเซ็นเซอร์/โหมดใน Studio · Simulator stream |
| **Communication Engine** | ช่องทางข้อมูลระหว่างเฟิร์มแวร์ ↔ โฮสต์ ↔ cloud | UART/bridge, MQTT broker ใน Studio, BLE host ตามรอบ |
| **Graphics / Visualization** | กราฟ, แผง, 3D, orientation | Sensor Telemetry · Sensor Studio · 3D rotation preview |
| **User Interaction** | อินพุตจากผู้เรียน (ปุ่ม, สคริปต์, โหมด toolbar) | เปลี่ยน Backend Bitstream/Simulator · สั่ง scene · publish คำสั่ง |
| **Scripting & Events** | จำลองเหตุการณ์ซ้ำได้ | event script / behavior (ลงลึกใน M03) · fault injection (M05) |
| **AI Connectivity (เสริม)** | ส่งข้อมูลไปวิเคราะห์ / รับผลกลับ | เส้นทางเตรียมใน Course 1 M05 — ไม่บังคับ M01 |
| **Physics (เสริม)** | จำลองการเคลื่อนไหว/แรงเมื่อโมเดลต้องการ | ใช้เมื่อโปรเจกต์มีกลไก — ไม่ใช่ทุกแล็บ |

> **Honest mapping**  
> UI ของแต่ละเวอร์ชัน extension อาจต่างกัน — **จำบทบาทของชั้น** ไม่ใช่จำพิกัดปุ่มทุกจอ

### 3.2 Concrete lab stack (what you install)

| ชิ้น | บทบาทใน Course 2 |
|---|---|
| **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | VS Code host หลัก — Twin / telemetry / MQTT / 3D |
| **Bitstream Simulator** (companion เมื่อใช้โหมด Simulator) | Virtual MCU ที่ฉีด telemetry โดยไม่ต้องเปิด COM |
| **บอร์ด + HEX** จาก [Hackathon](https://github.com/drsanti/TESAIoT_Hackathon) | Physical path — ยืนยันกับของจริง |
| **Hackathon `web-app/`** | Dashboard ภายนอกดูท่อ telemetry / MQTT |
| **[Developer Hub](https://dev.tesaiot.dev/)** | ตัวอย่างเฟิร์มแวร์ต้นทาง |
| **[ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)** | GLB / texture / รูป สำหรับ visualization 3D |

### 3.3 Two telemetry backends (critical mental model)

ใน Bitstream Studio มีแนวคิดสำคัญ: **Bitstream (UART/บอร์ด)** กับ **Simulator** เป็นเส้นทาง live ที่**ใช้ทีละเส้น** — ไม่ผสมใน UI

```text
Toolbar source = Bitstream  →  COM open  →  samples origin: uart
Toolbar source = Simulator →  COM closed →  samples origin: sim
```

| คำถาม | คำตอบสั้น |
|---|---|
| Twin ต้องมีบอร์ดไหม | ไม่เสมอ — Simulator = เส้นทางไม่มีบอร์ด |
| บอร์ดยังจำเป็นไหม | ใช่ — RF, analog, พลังงาน, ขาพินจริง |
| ทำไมห้ามผสม | กันข้อมูล uart/sim ปะปนในกราฟเดียวกัน |

รายละเอียด lifecycle จะฝึกใน M02/M04 — ใน M01 จำไว้ว่า **Twin Environment มีอย่างน้อยสองโหมดเข้าสู่โฮสต์**

---

## 4. Signals, Sensors, Behavior, and Data Pipeline

Twin จำลองได้หลาย *ระดับความละเอียด* — เลือกให้เหมาะกับคำถามที่ต้องการตอบ

### 4.1 Simulation levels

| ระดับ | ตัวอย่าง | ใช้ตอบคำถามอะไร |
|---|---|---|
| **I/O / pin logic** | สวิตช์เสมือน, LED เสมือน | ตรรกะควบคุมพื้นฐาน |
| **Sensor values** | IMU, temp, pressure | อ่านค่า → filter → ตัดสินใจ |
| **Behavior** | เมื่อกดปุ่มแล้วเปลี่ยนโหมด | ตอบสนองต่อเหตุการณ์ |
| **Connectivity** | MQTT pub/sub, lossy link | รูปแบบข้อความ + ความทนทาน |
| **Presentation** | กราฟ / 3D / dashboard | ผู้ใช้เห็นผลถูกต้องไหม |

### 4.2 Data pipeline (one page)

```text
[Source]
  board sensors  หรือ  virtual/sim sensors
        │
        ▼
[Firmware Logic]  — filter · window · decide · encode
        │
        ▼
[Communication]   — UART / MQTT / BLE
        │
        ▼
[Twin Host]       — decode · state · route
        │
        ├─► Visualization (Telemetry / Studio / 3D)
        ├─► External dashboard (Hackathon web-app)
        └─► Cloud / broker (M05)
```

ชุดข้อมูลที่ควรแยกในหัว (จะลงลึก M05):

| ชนิด | ความหมาย |
|---|---|
| **Telemetry** | ค่าวัดที่ไหลเป็นคาบ (อุณหภูมิ, accel, …) |
| **State** | สถานะระบบ (connected, mode, streaming) |
| **Event** | เหตุการณ์จุดเดียว (threshold crossed, button, alert) |

สิ่งที่ต้องชัดตอนออกแบบเทส:

1. อินพุตมาจาก **สคริปต์ / Simulator / ผู้ใช้ Twin** หรือจาก **โลกจริง**  
2. เฟิร์มแวร์ยัง “คิดว่า” กำลังอ่านฮาร์ดแวร์ผ่านชั้นที่ออกแบบไว้  
3. ผลลัพธ์ต้องสังเกตได้ใน **console + visualization** อย่างน้อยหนึ่งอย่าง  

---

## 5. Firmware Reality vs Twin Environment

| บนบอร์ดจริง | บน Twin / Simulator |
|---|---|
| Driver ↔ ซิลิคอน / วิทยุจริง | พอร์ตจำลอง ↔ Virtual Device / sim inject |
| Timing จากคริสตัล + RTOS จริง | Timing จำลอง — latency โฮสต์มีผล |
| ดีบักด้วย probe / UART | ดีบักผ่าน VS Code + log / panels ของโฮสต์ |
| RF / analog / พลังงานวัดได้ | มัก **จำลองไม่ได้ครบ** — ต้องยืนยันบนบอร์ด |

### 5.1 Decision guide (preview of lab table)

| สถานการณ์ | Twin/Sim พอไหม | ต้องบอร์ดจริงไหม |
|---|---|---|
| Logic สลับโหมดจากปุ่ม | มักพอ | ไม่จำเป็นระยะแรก |
| รูปแบบ JSON / MQTT topic | พอ (ดีมาก) | ยืนยันรอบสุดท้ายถ้าใช้ Wi‑Fi จริง |
| อ่าน IMU แล้วคำนวณบนโค้ด | พอสำหรับ logic | ยืนยัน noise/bias จริงบนบอร์ด |
| Wi‑Fi ระยะ / BLE ห้องจริง | ไม่แทน | **ต้อง** |
| ตรวจ pin map / บัดกรีผิด | ไม่แทน | **ต้อง** |

### 5.2 Recommended workflow

1. พัฒนาและเคสขอบบน **Twin / Simulator**  
2. ใช้ชุดเทส (topic, payload, scenario) ชุดเดียวกันให้มากที่สุด  
3. ยืนยันรอบสุดท้ายบน **ฮาร์ดแวร์จริง** โดยเฉพาะ analog, RF, พลังงาน  
4. เก็บหลักฐานทั้งสองโลกเมื่อส่ง Capstone (M06)

---

## 6. Course 2 Map — Where M01 Fits

| Module | คุณจะทำอะไรต่อจากแผนที่นี้ |
|---|---|
| **M01 (ตอนนี้)** | ชี้ชั้น Twin + ตัดสินใจเทส |
| [M02](../../m02-vscode-twin/l01-vscode-for-twin/README.md) | ติดตั้ง Bitstream Studio, ผูก workspace, Run/Debug ดูผล |
| [M03](../../m03-virtual-device/l01-virtual-device-modeling/README.md) | สร้าง Virtual Device + behavior + event script |
| [M04](../../m04-cosimulation/l01-firmware-twin-cosim/README.md) | Co-sim เฟิร์มแวร์ ↔ Twin วัด timing |
| [M05](../../m05-telemetry-cloud/l01-telemetry-cloud-simulation/README.md) | Telemetry pipeline + MQTT + lossy network |
| [M06](../../m06-integration/l01-system-integration-testing/README.md) | E2E mini-project + เอกสารส่งมอบ |

---

## Next Steps

1. ทำแล็บแผนที่: [แล็บ](../l02-lab/README.md)  
2. เก็บแผ่นสูตร: [twin-architecture-map.md](resources/twin-architecture-map.md)  
3. เมื่อพร้อม ไปต่อ **M02 — VS Code for Twin Development**

---

## References and Further Reading

1. **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)**  
2. **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)**  
3. **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)**  
4. **[ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)** — [`assets/`](https://github.com/drsanti/ternion-3d-assets-free/tree/main/assets)  
5. [Course 2 TOC](../../README.md) · [Course 1 TOC](../../../firmware-sdk-edge-ai/README.md)  
6. [Digital twin (overview)](https://en.wikipedia.org/wiki/Digital_twin)  
7. [MQTT Essentials](https://www.hivemq.com/mqtt-essentials/) — ทบทวนชั้น cloud ที่จะแตะใน M05  
8. [PSOC™ Edge E84](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm/psoc-edge-e84) — physical device อ้างอิง  

---

## เช็กความเข้าใจ

คำถามสั้นสามข้อใน [quiz.yaml](quiz.yaml) ผูกกับเป้าหมายของบทเรียนนี้ข้อละหนึ่งคำถาม ลองตอบเองก่อน แล้วค่อยเทียบกับเฉลยและคำอธิบายในไฟล์

## แล็บ

ลงมือต่อที่ [แล็บ: แผนที่สถาปัตยกรรม Twin](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Cheatsheet](resources/twin-architecture-map.md) · [← Table of Contents](../../README.md) · [M02 →](../../m02-vscode-twin/l01-vscode-for-twin/README.md)
