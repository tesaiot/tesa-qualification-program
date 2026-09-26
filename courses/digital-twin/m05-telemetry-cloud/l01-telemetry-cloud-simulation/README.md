---
id: twin.m05.l01
lang: th
title:
  th: ท่อ telemetry, MQTT บน Twin และ fault injection
  en: Telemetry Pipelines, MQTT on the Twin and Fault Injection
summary:
  th: แยก Telemetry/State/Event แยกท่อ Live Data กับ MQTT ใช้ web-app ex08/ex09 ตรวจสตรีม และออกแบบการทดลองเครือข่ายเสีย
  en: Separate Telemetry, State and Event, tell the Live Data pipe from the MQTT pipe, check streams with web-app ex08/ex09 and design network-fault experiments.
level: L3
time_min:
  concept: 45
  practise: 20
  check: 10
hardware:
  emulator: true
  boards:
  - devkit
prerequisites:
- twin.m04.l02
objectives:
- th: จำแนกข้อมูลอุปกรณ์เป็น Telemetry, State และ Event และเลือก topic กับ retain ให้เหมาะแต่ละชนิด
  en: Classify device data as Telemetry, State or Event and choose a topic and retain setting for each.
- th: แยกท่อ Live Data กับ MQTT และใช้อาการที่เห็นระบุว่าท่อไหนมีปัญหา
  en: Tell the Live Data pipe from the MQTT pipe and use symptoms to say which one is failing.
- th: ออกแบบการทดลอง fault injection ที่เปลี่ยนตัวแปรครั้งละหนึ่งตัว และบันทึกผลทั้งสองฝั่ง
  en: Design a fault-injection experiment that changes one variable at a time and logs both sides.
develops:
- skill: proto.mqtt
  to: 2
- skill: iot.cloud-platform
  to: 2
- skill: test.sil-hil
  to: 1
context:
  platform: psoc-edge-e84
  host: bitstream-studio
  ide: vscode
  simulator: Bitstream Simulator (not the BENTO Emulator)
status: alpha
translation: done
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C2/M05/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M05 — Telemetry and Cloud Simulation

**Course 2 · Module 5**  
**Suggested time:** ประมาณ 4 ชั่วโมง (classify data · pipeline · MQTT broker · dashboard · fault injection)  
**Format:** บทเรียนเชิงปฏิบัติ — จัดรูปข้อมูลจาก Twin/เฟิร์มแวร์ แล้วส่งต่อไป broker / dashboard ภายใต้เงื่อนไขที่ควบคุมได้

[Lab](../l02-lab/README.md) · [Lab notes](resources/telemetry-mqtt-lab-notes.md) · [← Table of Contents](../../README.md) · [← M04](../../m04-cosimulation/l01-firmware-twin-cosim/README.md) · [M06 →](../../m06-integration/l01-system-integration-testing/README.md)

---

## เป้าหมาย (Learning Outcomes)

เมื่อเรียนจบ คุณควรทำได้ดังนี้:

1. อธิบายชุดข้อมูลจากอุปกรณ์: **Telemetry, State, Event**  
2. จำลอง **Data Pipeline** เพื่อทดสอบการจัดรูปแบบข้อมูล  
3. ส่งข้อมูลจำลองไปยัง **Cloud / ระบบภายนอก** และตรวจด้วย **Dashboard**  
4. ตั้งค่า **MQTT Broker** ในสภาพแวดล้อม Twin / Studio  
5. **Publish / Subscribe** ระหว่าง Twin (หรืออุปกรณ์) กับ Cloud services  
6. จำลองสถานการณ์ **Lossy Network / Error Injection** และทดสอบภายใต้เงื่อนไขที่ควบคุมได้  

โมดูลนี้ต่อจาก [M04](../../m04-cosimulation/l01-firmware-twin-cosim/README.md) ที่คุณพิสูจน์แล้วว่าเฟิร์มแวร์ ↔ Twin มี I/O จริง — ตอนนี้ขยายชั้น **“ข้อมูลออกไปนอก Studio”** (Live Data consumer + MQTT) ก่อนรวมระบบใน [M06](../../m06-integration/l01-system-integration-testing/README.md)

> **Key phrase**  
> Twin เป็นสนามซ้อมของท่อข้อมูล — ฝึก topic, payload, dashboard และ reconnect **ก่อน** ขึ้นคลาวด์จริงทั้งวัน

### Read alongside this chapter

| เอกสาร | ใช้เมื่อ |
|---|---|
| [M04 — Co-simulation](../../m04-cosimulation/l01-firmware-twin-cosim/README.md) | ท่อ I/O ที่พิสูจน์แล้ว · `ex05` เป็น consumer ชั้นนอก |
| [Course 1 M06 — MQTT](../../../firmware-sdk-edge-ai/m06-mqtt/l01-mqtt-and-mqtts/README.md) | Broker / QoS / retain / เฟิร์มแวร์ CM55→CM33 |
| [Course 1 M05 — Sensors](../../../firmware-sdk-edge-ai/m05-sensor-data/l01-sensor-data-for-edge-ai/README.md) | ความหมายค่าที่จะใส่ใน telemetry |
| **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | Start broker · telemetry route · Twin MQTT tools |
| **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** | `web-app/` — **ex08** (route/stale) · **ex09–ex15** (MQTT) |
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | ตัวอย่าง encode / publish ฝั่งเฟิร์มแวร์ |
| [HiveMQ MQTT Essentials](https://www.hivemq.com/mqtt-essentials/) | อ่านเสริมแนวคิด topic / QoS |
| **[ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)** | visualization 3D ประกอบ dashboard (ถ้าใช้) |

---

## 1. Telemetry, State, and Event

การแยกชนิดข้อมูลช่วยออกแบบ **topic**, **อัตราการส่ง**, และ **แดชบอร์ด** ไม่ให้สตรีมหนาแน่นกลบเหตุการณ์สำคัญ

| ชนิด | ลักษณะ | ตัวอย่างในแล็บ Twin |
|---|---|---|
| **Telemetry** | สตรีมต่อเนื่องตามเวลา | อุณหภูมิทุก 1 s · BMI270 sample · DevKit Twin channels |
| **State** | สถานะปัจจุบันของระบบ | `mode=idle`, `led=on`, Link `connected`, `route=uart\|sim` |
| **Event** | เกิดเป็นครั้งคราวเมื่อเงื่อนไขเป็นจริง | `threshold_exceeded`, `stale`, `reconnect`, `fault_injected` |

### 1.1 Design habits

| นิสัย | เหตุผล |
|---|---|
| Telemetry ใช้ topic/อัตราคงที่ | แดชบอร์ดคาดหวังจังหวะ |
| State ส่งเมื่อเปลี่ยน (หรือ retain ล่าสุด) | ลด spam · subscriber ใหม่รู้สถานะทันที |
| Event เก็บ timestamp + เหตุผลสั้น ๆ | debug / M06 E2E ไล่ย้อนได้ |
| อย่าใส่ทุกอย่างใน topic เดียวแบบไม่แยกความหมาย | ทดสอบและ ACL ยาก |

ตัวอย่างโครง topic ในแล็บ (ปรับตามชุดที่คุณใช้ได้):

```text
device/<deviceId>/devkit-twin/telemetry     ← telemetry stream
device/<deviceId>/state                      ← current mode / flags
device/<deviceId>/event/<name>               ← sparse events
lab/qos-demo                                 ← สนามทดลอง QoS/retain (ex14)
```

ค่าเริ่มต้นที่ Hackathon `web-app` ใช้บ่อย:  
`device/devkit-twin-01/devkit-twin/telemetry` (ดู §5)

> **Key phrase**  
> Telemetry = *ลมหายใจ* · State = *ท่าทางปัจจุบัน* · Event = *เหตุการณ์ที่ควรบันทึก*

---

## 2. Data Pipeline (Twin Lab View)

ลำดับทั่วไป:

```text
[Source]
  Firmware / Simulator / Twin virtual device
        │
        ▼
[Shape]
  JSON fields · units · mask · channels
        │
        ▼
[Transport]
  A) Live Data provider (WS) → Studio panels / web-app ex05–ex08
  B) MQTT broker             → web-app ex09–ex15 / cloud / external tools
        │
        ▼
[Observe]
  Dashboard · subscriber log · gauges
```

### 2.1 Two pipes you must not confuse

| ท่อ | ใช้เมื่อ | ตัวอย่าง consumer |
|---|---|---|
| **Live Data** (telemetry provider) | ดู sample ที่ decode จาก bridge แล้ว · `route` / `origin` / `stale` | `ex05`, `ex06`, **`ex08`** |
| **MQTT** (broker pub/sub) | จำลองชั้น cloud / ระบบภายนอก | **`ex09`**, `ex12`, `ex15` |

ทั้งสองท่ออาจแสดง “อุณหภูมิก้อนเดียวกัน” แต่ **โปรโตคอลและจุดล้มต่างกัน**

| อาการ | น่าสงสัยท่อ |
|---|---|
| `TelemetryClient` disconnected | Live Data / bridge / Serve web-app |
| MQTT `disconnected` ที่ `ws://127.0.0.1:8883/mqtt` | ยังไม่ **Start broker** ใน Studio |
| Live Data ดี แต่ MQTT ว่าง | ยังไม่มี publisher บน topic นั้น |
| MQTT มีข้อความแต่ Live Data เงียบ | คนละท่อ — ไม่ได้แปลว่า “เซ็นเซอร์ตาย” |

### 2.2 Schema / format drills (pipeline test)

วิธีทดสอบท่อที่มีประโยชน์ก่อนขึ้นคลาวด์:

1. ส่ง payload ครบฟิลด์ → dashboard เขียว  
2. **ตัดฟิลด์** หรือเปลี่ยนชื่อ key → ดูว่า UI พังตรงไหน  
3. ส่งหน่วยผิด (เช่น °C ใส่เป็น milli) → ตัวเลขเพี้ยนแต่ยัง parse ได้  
4. ส่ง JSON เสีย → subscriber แสดง error ชัดหรือเงียบ  

บันทึกผลใน [telemetry-mqtt-lab-notes.md](resources/telemetry-mqtt-lab-notes.md)

---

## 3. Walkthrough — `ex08` Stale, Route, and Origin

ก่อนเปิด broker ให้คุ้น **คุณภาพของสตรีม Live Data** — ต่อจาก M04 ที่ใช้ `ex05` เป็น orientation consumer

ไฟล์: [Hackathon](https://github.com/drsanti/TESAIoT_Hackathon) → `web-app/ex08_stale_and_route.html`

### 3.1 What the page proves

| UI | ความหมาย |
|---|---|
| Connection **route** | backend ที่ provider ใช้ (สัมพันธ์ Simulator vs Bitstream) |
| **COM open** | มีพอร์ตอนุกรมเปิดหรือไม่ |
| Last sample **origin** | `uart` หรือ `sim` — ต้องสอดคล้องโหมดที่เลือกใน Studio |
| Sensor **pills** + stale | แต่ละเซ็นเซอร์เงียบเกิน `staleAfterMs` หรือยัง fresh |
| Event **log** | connection / sample / stale เป็นเหตุการณ์ไล่เวลาได้ |

### 3.2 Lab steps

1. Link Studio (Simulator *หรือ* Bitstream — ไม่ผสม)  
2. Serve โฟลเดอร์ `web-app/` แล้วเปิด **ex08**  
3. ยืนยัน `connected` · จด `route` และ `origin` ของ sample ล่าสุด  
4. หยุดสตรีมชั่วคราว (หยุด Simulator / ถอด COM สั้น ๆ ตามที่รอบอนุญาต) → pill ควรเข้า **stale** และมี event ใน log  
5. กลับมาสตรีม → pill **fresh** อีกครั้ง  

**ผ่านเมื่อ:** อธิบายได้ว่า `stale` คือ **Event** ด้านโฮสต์เมื่อ telemetry ขาดช่วง — ไม่ใช่ค่าเซ็นเซอร์

> ใช้ ex08 เป็นหลักฐาน **lossy / disconnect ชั้น Live Data** ก่อนไปชั้น MQTT (§6)

---

## 4. MQTT Broker in the Twin Host

ใน Course 2 โฮสต์หลักคือ Bitstream Studio — มักมีคำสั่งประมาณ:

**Toolbar / Server → Start broker**

จากนั้นหน้าเว็บ MQTT ใน Hackathon ต่อที่ค่าเริ่มต้น:

```text
ws://127.0.0.1:8883/mqtt
```

(ดู `DEFAULT_MQTT_WS_PATH` ใน `web-app/shared/ex-mqtt.js`)

| ตรวจ | คาดหวัง |
|---|---|
| Start broker แล้วยังไม่เปิดหน้าเว็บ | broker พร้อมรับ client |
| เปิด `ex09` โดยยังไม่ start broker | ค้าง connecting / error |
| Override URL | `?mqtt=ws://…` ถ้าพอร์ตเปลี่ยน |

### 4.1 Twin / cloud roles (honest mapping)

| บทบาทในเอกสารหลักสูตร | สิ่งที่ทำในแล็บ |
|---|---|
| MQTT ใน Twin | Studio **Start broker** + pub จาก Twin / Sensor Studio / เครื่องมือโฮสต์ |
| Cloud / ระบบภายนอก | `web-app` subscriber · หรือ broker สาธารณะ/LAN (ทบทวน [C1 M06](../../../firmware-sdk-edge-ai/m06-mqtt/l01-mqtt-and-mqtts/README.md)) |
| อุปกรณ์จริง publish | เฟิร์มแวร์บนบอร์ดหลัง Wi‑Fi (C1) — ใน M05 โฟกัสท่อโฮสต์ก่อนถ้าเวลาน้อย |

อย่าสมมติว่า “Start broker” = มี telemetry อัตโนมัติ — ยังต้องมี **publisher** บน topic ที่ subscribe

---

## 5. Walkthrough — `ex09` MQTT Subscriber (main cloud-sim example)

ตัวอย่างหลักของ M05 สำหรับชั้น MQTT: **`ex09_mqtt_subscriber.html`**

### 5.1 What it does

1. โหลด mqtt.js ผ่าน Serve Web App (`/@bitstream/mqtt-live-data.js`)  
2. เชื่อม `ws://127.0.0.1:8883/mqtt` (หรือ `?mqtt=`)  
3. Subscribe topic เริ่มต้น:

```text
device/devkit-twin-01/devkit-twin/telemetry
```

สร้างจาก `devkitTwinTopic(deviceId)` — เปลี่ยนด้วย `?device=` หรือ `?topic=`  

4. แสดง **last payload** (JSON) · นับข้อความ · นับ `channels` ถ้ามี  

### 5.2 How to run (evidence path)

```text
[Bitstream Studio] Start broker
        │
        ▼
[Publisher]
  DevKit Twin MQTT tab
  หรือ Sensor Studio connectivity nodes
  หรือเครื่องมือ publish อื่น
        │  topic: device/<id>/devkit-twin/telemetry
        ▼
[Broker ws://127.0.0.1:8883/mqtt]
        │
        ▼
[ex09 browser page]  →  Last payload + message count
```

ขั้นตอนสั้น:

1. **Start broker** ใน Studio  
2. Serve `web-app/` → เปิด **ex09**  
3. รอ badge `connected`  
4. Publish จาก Twin / โฮสต์ไป topic ที่หน้าเว็บ subscribe  
5. แคป `Last payload` คู่กับแหล่ง publish  

**ผ่านเมื่อ:** มีอย่างน้อยหนึ่ง JSON ที่ฟิลด์ตรงกับที่ตั้งใจส่ง (หน่วยและชื่อ key)

### 5.3 Teaching view of the page code

แนวคิดหลัก (ดูไฟล์จริงใน Hackathon):

```text
connectMqtt(mqtt, MQTT_URL)
  → onConnect → client.subscribe(TOPIC)
  → on("message") → JSON.parse → อัปเดต payload + chips
```

`wireMqttState` จัดการ `connected` / `reconnecting` / `error` / `disconnected` — ใช้เป็นหลักฐาน **reconnect** ในแล็บ lossy (§6)

### 5.4 Nearby examples (ladder)

| ไฟล์ | ใช้เมื่อ |
|---|---|
| **ex09** | Subscribe หนึ่ง topic — **ตัวอย่างหลัก §5** |
| ex10 | Publish จากเบราว์เซอร์ |
| ex11 | Wildcards (`+` / `#`) |
| ex12 | DevKit gauges |
| ex13 | Live data client ผสมแนว MQTT |
| **ex14** | QoS + retain ทดลองมือ |
| ex15 | Dashboard รวม WS + MQTT |

สำหรับ M05 ให้ทำ **ex08 + ex09** ให้ชัวร์ แล้วเลือกอย่างน้อยหนึ่งจาก ex10–ex15 ตามเวลา

---

## 6. Publish / Subscribe Patterns

ทบทวนสั้นจาก [Course 1 M06](../../../firmware-sdk-edge-ai/m06-mqtt/l01-mqtt-and-mqtts/README.md) แล้วยกมาใช้ใน Twin:

| แบบ | ใคร publish | ใคร subscribe | ใช้ในแล็บ |
|---|---|---|---|
| Device → Cloud | Twin / เฟิร์มแวร์ | ex09 / dashboard | telemetry |
| Cloud → Device | เครื่องมือโฮสต์ / ex10 | Twin หรือเฟิร์มแวร์ | คำสั่ง / state set |
| Lab mirror | ex14 | ex11 บน topic เดียวกัน | QoS / retain |

### 6.1 QoS and retain (quick lab with ex14)

| แนวคิด | สิ่งที่ลอง |
|---|---|
| QoS 0 | ส่งแล้วไปต่อ — เหมาะ telemetry หนาแน่น |
| QoS 1 / 2 | รับประกันมากขึ้น — ดูพฤติกรรมบน lab topic |
| **Retain** | publish พร้อม retain → เปิด subscriber ใหม่ (เช่น ex11) ควรได้ข้อความล่าสุดทันที |

อย่าเปิด retain บน topic telemetry ความถี่สูงโดยไม่คิด — broker จะเก็บ “ค่าล่าสุด” ที่อาจทำให้ผู้มาใหม่เข้าใจผิดว่าเป็นสตรีมสด

### 6.2 Mapping Telemetry / State / Event onto MQTT

| ชนิด | แนวทาง topic | Retain? |
|---|---|---|
| Telemetry | `…/telemetry` หรือ `…/sensors/<name>` | มัก **ไม่** |
| State | `…/state` | มัก **ใช่** (ค่าล่าสุด) |
| Event | `…/event/<name>` | มัก **ไม่** (เก็บที่ log/DB แทน) |

---

## 7. Lossy Network and Error Injection

เป้าหมายไม่ใช่ทำเครือข่ายพังเก่งที่สุด แต่คือ **ควบคุมตัวแปรหนึ่งตัว** แล้วบันทึกว่าคิว / UI / client รับมืออย่างไร

### 7.1 Experiments you can run in the lab

| การทดลอง | วิธีในแล็บ Twin | ดูอะไร |
|---|---|---|
| ข้อความขาดช่วง | หยุด publisher ชั่วคราว · หรือหยุด Simulator | ex08 stale · ช่องว่างบนกราฟ |
| ตัดการเชื่อมต่อสั้น ๆ | Stop broker แล้ว Start ใหม่ · หรือปิดแท็บแล้วเปิด | ex09 `reconnecting` → `connected` |
| Latency สูง | ลดอัตรา publish / scene Quiet | ช่วงเวลาระหว่าง message count |
| Payload ผิดรูป | ส่ง JSON ตัดฟิลด์ | dashboard error vs เงียบ |
| สลับ backend ผิดจังหวะ | (อย่าทำตอนจับหลักฐาน) ผสม sim+uart | origin สับสน — ใช้สอนว่าต้อง XOR |

### 7.2 What to write down

สำหรับแต่ละเคส:

1. สิ่งที่ฉีด / ตัด  
2. สิ่งที่เห็นบน subscriber / Studio (timestamp)  
3. พฤติกรรม: **drop** · **retry** · **reconnect** · **stale UI** · **backoff**  
4. ยอมรับได้สำหรับโปรเจกต์หรือต้องแก้ก่อน M06  

แบบฟอร์ม: [telemetry-mqtt-lab-notes.md](resources/telemetry-mqtt-lab-notes.md)

> **Key phrase**  
> Fault injection ที่ดี = *เปลี่ยนอย่างเดียวต่อรอบ* แล้วมี log ทั้งสองฝั่ง

---

## 8. How M05 Feeds M06

| หลัง M05 คุณมี | ใช้ต่อที่ M06 |
|---|---|
| Topic + ตัวอย่าง payload | E2E Smart Environmental Monitor |
| Dashboard / ex09–ex15 ที่ใช้ซ้ำได้ | เกณฑ์รับงานแบบมีหลักฐาน |
| โน้ต lossy / stale / reconnect | ส่วนวิเคราะห์ความเสี่ยงในรายงาน |
| แยก Live Data vs MQTT ได้ | ไม่ปนหลักฐานผิดท่อตอน demo |

---

## Next Steps

1. ทำแล็บ: [แล็บ](../l02-lab/README.md)  
2. กรอก [telemetry-mqtt-lab-notes.md](resources/telemetry-mqtt-lab-notes.md)  
3. เมื่อพร้อม ไปต่อ [M06 — System Integration and Testing](../../m06-integration/l01-system-integration-testing/README.md)

---

## References and Further Reading

1. [M04 Co-simulation](../../m04-cosimulation/l01-firmware-twin-cosim/README.md) · [Course 1 M06 MQTT](../../../firmware-sdk-edge-ai/m06-mqtt/l01-mqtt-and-mqtts/README.md)  
2. **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** — Start broker / Twin MQTT  
3. **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** — `web-app/ex08` … `ex15`  
4. **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)**  
5. [HiveMQ MQTT Essentials](https://www.hivemq.com/mqtt-essentials/) · [mqtt.org](https://mqtt.org/)  
6. **[ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)**  
7. [Course 2 TOC](../../README.md)  

---

## เช็กความเข้าใจ

คำถามสั้นสามข้อใน [quiz.yaml](quiz.yaml) ผูกกับเป้าหมายของบทเรียนนี้ข้อละหนึ่งคำถาม ลองตอบเองก่อน แล้วค่อยเทียบกับเฉลยและคำอธิบายในไฟล์

## แล็บ

ลงมือต่อที่ [แล็บ: ท่อ telemetry และ MQTT บน Twin](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Lab notes](resources/telemetry-mqtt-lab-notes.md) · [← Table of Contents](../../README.md) · [← M04](../../m04-cosimulation/l01-firmware-twin-cosim/README.md) · [M06 →](../../m06-integration/l01-system-integration-testing/README.md)
