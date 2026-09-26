---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 3.1 — Virtual Device, behavior, event script และโมเดล 3D สำหรับ Twin"
footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · ดัดแปลงจากงานของ ผศ.ดร.สันติ นุราช (KMUTT) · CC BY-NC 4.0"
---
<style>
section { font-size: 24px; padding: 40px 52px; justify-content: flex-start; }
section h1 { font-size: 1.45em; line-height: 1.12; margin: 0 0 .22em; }
section h2 { font-size: 1.12em; margin: .15em 0; }
section h3 { font-size: 1.0em; margin: .12em 0; }
section p, section li { margin: .16em 0; line-height: 1.32; }
section img { max-width: 100%; height: auto; }
section svg { max-height: 250px; }
section table { font-size: .78em; }
section pre { font-size: .70em; line-height: 1.32; background:#0d1117; color:#e6edf3; border:1px solid #30363d; border-radius:8px; padding:12px 16px; box-shadow:0 2px 8px rgba(0,0,0,.25); }
section pre code { white-space: pre-wrap; background:transparent; color:inherit; } section pre .hljs-comment{color:#8b949e;font-style:italic} section pre .hljs-keyword,section pre .hljs-built_in,section pre .hljs-literal{color:#ff7b72} section pre .hljs-string{color:#a5d6ff} section pre .hljs-number{color:#79c0ff} section pre .hljs-title,section pre .hljs-title.function_,section pre .hljs-section{color:#d2a8ff} section pre .hljs-meta{color:#ffa657} section pre .hljs-attr,section pre .hljs-attribute,section pre .hljs-name{color:#7ee787}
section blockquote { margin: .25em 0; font-size: .92em; }
/* two images on a line (parity / 2x2 grids) stay side-by-side and small */
section p > img + img { margin-left: 10px; }
/* scroll-within-slide: dense slides scroll instead of clipping */
section { overflow-y: auto; overflow-x: hidden; }
section::-webkit-scrollbar { width: 11px; }
section::-webkit-scrollbar-thumb { background:#4a90d9; border-radius:6px; }
section::-webkit-scrollbar-track { background:rgba(0,0,0,.06); }
/* image drop-shadow + cover-slide readability (auto) */
section img{filter:drop-shadow(0 3px 12px rgba(0,0,0,.5))}
section.cover *{color:#fff !important}
section.cover h1,section.cover h2,section.cover h3,section.cover p,section.cover li,section.cover strong,section.cover em,section.cover blockquote,section.cover div{text-shadow:0 2px 9px rgba(0,0,0,.92),0 0 3px rgba(0,0,0,.8)}
section.cover div[style*="background:#"],section.cover div[style*="background: #"]{background:rgba(10,14,20,.66) !important;border-color:rgba(120,200,255,.45) !important;max-width:62%}
section.cover blockquote{border-left:4px solid rgba(120,200,255,.6) !important;background:rgba(13,17,23,.55) !important;border-radius:6px;padding:.3em .6em}
section.cover h1,section.cover h2,section.cover h3,section.cover p,section.cover blockquote{max-width:60%}
section.cover div:not(:has(img)){max-width:62%}
section.cover img{filter:none}
</style>

<!-- _class: cover -->

# บทเรียน 3.1 — Virtual Device, behavior, event script และโมเดล 3D สำหรับ Twin

## กำหนดโมเดลอุปกรณ์ เซ็นเซอร์ พฤติกรรม และสคริปต์เหตุการณ์ตามเวลา แล้วเตรียมโมเดล 3D ใน Blender ให้ส่งออกเป็น GLB สำหรับ Twin

**พัฒนาเฟิร์มแวร์ร่วมกับ TESA Digital Twin บน VS Code — โมดูล 3 · บทเรียน 1**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. กำหนด Virtual Device Model ที่มี identity เซ็นเซอร์อย่างน้อยสองชนิด (พร้อม unit, default, min/max) และเอาต์พุตที่สังเกตได้
2. เขียน behavior แบบ WHEN/THEN ที่ทดสอบได้ทั้งขาเข้าและขาออก และไทม์ไลน์ event script ที่รันซ้ำได้
3. ระบุเงื่อนไขของโมเดล 3D ที่พร้อมใช้กับ Twin (สเกลจริง origin ชัด UV พร้อม) และขั้นตอนส่งออกเป็น glTF Binary (.glb)

---

## ก่อนเริ่ม

- ผ่าน [บทเรียน 2.2 — แล็บ M02](../../m02-vscode-twin/l02-lab/README.md) มาแล้ว — โฮสต์ Twin (Bitstream Studio) พร้อมใช้
- ต้องมี **Blender 4.5** สำหรับส่วน 3D (ลิงก์คู่มือในบทเรียนตรึงไว้ที่เวอร์ชันนี้)
- ทำได้ด้วยโหมด Simulator ของ Bitstream Studio

> **หมายเหตุ:** บางเอกสารต้นฉบับอ้างปุ่ม scene ใน `ble-flet` แต่เครื่องมือนั้นยังไม่เผยแพร่ต่อสาธารณะ — ให้ใช้แผงใน Bitstream Studio แทน

---

## ดูของจริงก่อน — Virtual Device Model คืออะไร

**Virtual Device Model** คือคำอธิบายซอฟต์แวร์ของอุปกรณ์หนึ่งเครื่องในโลก Twin

| ส่วน | คำถามที่ต้องตอบได้ |
|---|---|
| Identity | ชื่อ / รหัสอุปกรณ์คงที่สำหรับอ้างในรายงาน |
| Sensors | มีตัวอะไร · หน่วย · ค่าเริ่มต้น · ช่วงที่ยอมรับ |
| Actuators / outputs | LED, flag, log — สิ่งที่สังเกตผลได้ |
| Behaviors | เมื่ออินพุต/คำสั่งเกิด แล้วสถานะเปลี่ยนอย่างไร |
| Events / scripts | สถานการณ์ตามเวลาที่รันซ้ำได้ |

> **Key phrase**: Virtual Device คือ *ข้อตกลง* ระหว่างสคริปต์เทสของคุณกับ Twin — ไม่ใช่ datasheet ทั้งเล่ม

---

## ตัวอย่างสมบูรณ์ — โครง JSON ของโมเดล (แนวคิด)

```json
{
  "deviceId": "tesa-edge-demo-01",
  "sensors": [
    { "id": "temp", "type": "temperature", "unit": "C", "default": 25.0, "min": -10.0, "max": 85.0 },
    { "id": "btn_user", "type": "switch", "default": 0 }
  ],
  "actuators": [
    { "id": "led_status", "type": "led", "default": 0 }
  ],
  "behaviors": [
    { "when": "command.led == on", "then": "actuators.led_status = 1" },
    { "when": "sensors.temp > 40", "then": "emit event threshold_exceeded" }
  ]
}
```

เป็น **template แนวคิดสำหรับเรียน** — ฟิลด์จริงของเครื่องมืออาจชื่อต่างกัน ดูฉบับเต็ม (รวมเซ็นเซอร์ IMU) ใน [README.md](README.md) หัวข้อ 1.1

---

## แนวคิด — เซ็นเซอร์และ scene presets

| ชนิด | ค่าที่มักจำลอง | เหมาะทดสอบ |
|---|---|---|
| IMU (เช่น BMI270) | accel / gyro | gesture, activity, orientation |
| Temperature / Humidity (SHT40) | สเกลาร์ต่อเนื่อง | threshold, calibration path |
| Switches / buttons | 0/1 หรือ edge | UI logic, debounce |

แนะนำลำดับเรียน: สวิตช์ + อุณหภูมิก่อน (สังเกตผลชัด) → เพิ่ม IMU เมื่อท่อข้อมูลพร้อม

| Scene (ตัวอย่างในแพ็กแล็บ) | ความหมายโดยประมาณ |
|---|---|
| Motion | IMU หนาแน่นขึ้น · env ช้า |
| Lab Quiet | ~1 Hz ทั้งชุด — ดีต่อการสาธิต |

---

## แนวคิด — default, range และความซื่อสัตย์ของโมเดล

| ฟิลด์ | ทำไมสำคัญ |
|---|---|
| `default` | ค่าตอนเริ่มสคริปต์ / ก่อนกระตุ้น |
| `min` / `max` | กันเทสที่อยู่นอกโลกจริงโดยไม่ตั้งใจ |
| unit | กันสับสน °C / Pa / g |
| "sim vs real" | ค่าจาก Simulator เป็น sine/สังเคราะห์ — ไม่ใช่ noise บอร์ดจริง |

โมเดล**ไม่ต้อง**จำลองทุกบล็อกในซิลิคอน — ต้อง**เพียงพอต่อการทดสอบ logic เฟิร์มแวร์**ตามโจทย์ของแล็บเท่านั้น

---

## ตัวอย่างสมบูรณ์ — เขียน Behavior แบบ WHEN/THEN

| แบบ | ตัวอย่าง | สังเกตผลที่ |
|---|---|---|
| Command → actuator | `led=on` → LED สถานะเปิด | UI / บอร์ด / log |
| Sensor → event | `temp > 40` → `threshold_exceeded` | event panel / MQTT / UART |
| Switch → mode | กดปุ่ม → เปลี่ยนโหมด publish | toolbar / stream rate |

```text
WHEN user_button rising edge
THEN led_status = ON for 1 s AND log "btn"
```

เขียน behavior ให้ **ทดสอบได้ทั้งขาเข้าและขาออก** — ถ้ามีแต่ "ค่าขยับ" โดยไม่มีข้อตกลงว่าควรเกิดอะไร จะวัดไม่ได้ว่า logic ถูก

---

## ตัวอย่างสมบูรณ์ — Event Simulation Script

```text
t = 0–2 s   : idle (defaults)
t = 2–5 s   : temperature ramp +0.5 °C / step
t = 5.0 s   : press virtual switch ~200 ms
t = 6.0 s   : short IMU shake pulse
t = 7–10 s  : observe outputs / events
t = 10 s    : stop or loop
```

สำคัญคือ **ลำดับเหตุการณ์ + ผลที่คาด + หลักฐาน** ไม่ใช่ภาษาสคริปต์เฉพาะ — เก็บไทม์ไลน์ไว้ในโฟลเดอร์แล็บ แล้วรันชุดเดิมซ้ำเมื่อแก้เฟิร์มแวร์ในโมดูล 4+ ถ้าผลเปลี่ยนโดยไม่ตั้งใจ คือสัญญาณ regression

---

## แนวคิด — บทบาทของ Blender สำหรับ Twin

Virtual Device อธิบาย **ข้อมูลและพฤติกรรม** — Blender เตรียม **ตัวแทนภาพ 3 มิติ** ที่ Twin/Sensor Studio แสดง

| ชั้นงาน | สิ่งที่คุณฝึก | ปลายทาง Twin |
|---|---|---|
| Modeling | สร้างรูปทรง mesh ของเคส/บอร์ด | รูปทรงในฉาก 3D |
| Texturing | UV + material / texture | พื้นผิวที่ดูสมจริงบนโฮสต์ |
| Animation | keyframe / action สั้น ๆ | แสดงกลไกเปิด-ปิด หรือ motion demo |
| Export | `.glb` | โหลดใน Studio |

> **Course 2 vs Course 3**: ที่นี่ให้พื้นฐานที่ใช้งานกับ Twin ได้ — หลักสูตร Product Industrial Design จะลงลึก casing/industrial workflow/prototype

---

## แนวคิด — แนวทางโมเดลอุปกรณ์ Edge/DevKit

1. ตั้งหน่วยเป็น **เมตร** (หรืออย่างน้อยสเกลสม่ำเสมอทั้งฉาก)
2. วาง **origin** ที่จุดที่มีความหมาย (มุมบอร์ด, แกนหมุนฝา, จุดวางบนโต๊ะ)
3. แยกชิ้นส่วนที่อาจขยับ (ฝา, ปุ่ม, LED) เป็น object คนละชิ้นถ้าจะ animate
4. คุมจำนวน polygon — webview Twin ไม่ต้องการ denseness ระดับฟิล์ม

> **Key phrase**: Modeling ที่ดีสำหรับ Twin = *อ่านรูปได้ + สเกลจริง + origin ชัด + พร้อม UV* — ไม่ใช่รายละเอียดที่ render ภาพโฆษณาเท่านั้น

---

## แนวคิด — Texturing และสิ่งที่ animation ส่งออกได้

Workflow ที่แนะนำ: Mesh ready → Unwrap UV → Principled BSDF → Base Color → ตรวจใน Material Preview → Export GLB

| glTF รองรับโดยทั่วไป | มักไม่ไป / ถูกมองข้าม |
|---|---|
| Keyframe ของ location / rotation / scale | Animation ของไฟ / material บางชนิด |
| Skinning (armature), Shape key animation | Logic เฉพาะใน Blender ที่ไม่ได้ export |

> **เชื่อมกับ Virtual Device**: Timeline event script = *เหตุการณ์ข้อมูล* · Timeline ใน Blender = *เหตุการณ์ภาพ* — ใน Capstone (โมดูล 6) พยายามให้สองเส้นนี้เล่าเรื่องเดียวกัน

---

## ตัวอย่างสมบูรณ์ — ส่งออกเป็น glTF Binary (.glb)

| ขั้น | การกระทำ |
|---|---|
| 1 | Apply transforms ที่จำเป็น, ตรวจ origin |
| 2 | UV + Principled BSDF พร้อม |
| 3 | Animation พร้อม (ถ้ามี) |
| 4 | File → Export → glTF 2.0 |
| 5 | เลือก glTF Binary (.glb) · เปิด Meshes / Materials / (Animations) |
| 6 | โหลดใน Bitstream Studio |

รูปแบบอื่น (FBX/OBJ/STL) มีที่ใช้ตอน prototype/พิมพ์ 3D — ในหลักสูตรนี้ให้โฟกัส **GLB สำหรับ Twin**

---

## แนวคิด — เช็กลิสต์ก่อนลงมือสร้างจริง

ก่อนลงมือ Lab ตอบให้ได้:

1. อุปกรณ์นี้ทดสอบ **logic ข้อไหน** ของเฟิร์มแวร์/ผลิตภัณฑ์
2. เซ็นเซอร์ขั้นต่ำที่ต้องมีมีอะไรบ้าง (อย่างน้อย 2 ชนิด)
3. Behavior หนึ่งเส้นสังเกตที่จอไหน
4. สคริปต์เหตุการณ์ใช้เวลากี่วินาที และใครรันซ้ำได้บ้างในทีม
5. (แนะนำ) จะใช้โมเดล 3D จาก Blender หรือจากแพ็กสำเร็จรูป

---

## ฝึกเติม/แล็บ

[แล็บ: สร้าง Virtual Device และ event script](../l02-lab/README.md)

- กำหนด Virtual Device Model ของคุณเอง (identity + เซ็นเซอร์ ≥ 2 ชนิด + actuator)
- เขียน behavior อย่างน้อยหนึ่งเส้นที่ทดสอบได้ทั้งขาเข้าขาออก
- สร้างไทม์ไลน์ event script แล้วรันซ้ำอย่างน้อยสองรอบ
- (แนะนำ) เตรียมโมเดล 3D ใน Blender แล้ว export เป็น .glb

---

## เช็กความเข้าใจ

1. ทำไมต้องใส่ `min` / `max` ให้เซ็นเซอร์ในโมเดล
2. ข้อใดเป็น behavior ที่ "ทดสอบได้" ตามแนวทางของบทเรียน
3. รูปแบบไฟล์ที่บทเรียนแนะนำสำหรับส่งโมเดลเข้า Bitstream Studio / Twin เว็บ

---

## ไปต่อ

- Virtual Device Model ต้องมี identity, เซ็นเซอร์ที่มี unit/default/range และ actuator ที่สังเกตได้
- Behavior เขียนแบบ WHEN/THEN ที่ทดสอบได้ทั้งสองทาง · Event script เก็บไว้รันซ้ำเพื่อ regression
- Blender เตรียมตัวแทนภาพ 3D — ส่งออกเป็น glTF Binary (.glb) สำหรับ Twin
- พร้อมแล้วสำหรับ **โมดูล 4 — Co-simulation ระหว่างเฟิร์มแวร์กับ Twin**

[บทเรียนโมดูล 4 →](../../m04-cosimulation/l01-firmware-twin-cosim/README.md)

---

## แหล่งที่มา

"บทเรียน 3.1 — Virtual Device, behavior, event script และโมเดล 3D สำหรับ Twin" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)
นำเข้าจาก drsanti/TESAIoT-Courses — C2 (commit `287c218`) ภายใต้สัญญาอนุญาต CC BY 4.0

ไม่มีภาพจากบุคคลที่สามในสไลด์ชุดนี้
