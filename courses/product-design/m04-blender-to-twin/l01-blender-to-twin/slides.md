---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 4.1 — ส่งออก GLB และนำเข้า Twin host"
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
<!-- _backgroundColor: #0d1117 -->

# บทเรียน 4.1 — ส่งออก GLB และนำเข้า Twin host

## ความหมายของ Twin-ready การเตรียมไฟล์ก่อน export ขั้นตอน glTF Binary การตรวจหลังนำเข้า และจุดเซ็นเซอร์/โต้ตอบ

**โมดูล 4 — จาก Blender สู่ Digital Twin**

หลักสูตร **การออกแบบผลิตภัณฑ์เชิงอุตสาหกรรม (Blender และ Digital Twin)** · ดัดแปลงจากงานของ ผศ.ดร.สันติ นุราช (KMUTT)

---

## เป้าหมาย

เมื่อเรียนจบบทเรียนนี้ คุณควรทำได้:

1. ส่งออกโมเดลในรูปแบบ **glTF/GLB** ให้พร้อมใช้กับ Twin
2. นำโมเดลเข้าสู่ TESA Digital Twin ผ่าน **Bitstream Studio** (โฮสต์หลักของคอร์ส)
3. กำหนดจุดโต้ตอบ (**interaction points**) จุดเซ็นเซอร์ และตำแหน่งประกอบ
4. ทดสอบโมเดลร่วมกับข้อมูล telemetry / การเคลื่อนไหว / ค่าเซ็นเซอร์

> **คาถาประจำบทเรียน**
> GLB ที่ดี = *ขนาดถูก · แกนถูก · ชื่อคลิปชัด · วัสดุส่งออกได้* — นำเข้า Twin แล้วค่อยแต่งฉาก ไม่ใช่แก้สเกลทีหลังทีละร้อยเท่า

---

## "Twin-ready" หมายถึงอะไรในหลักสูตรนี้

โฮสต์ Digital Twin หลักคือ **Bitstream Studio** (VS Code extension) รับไฟล์ **glTF Binary (`.glb`)** สำหรับ preview / Sensor Studio / Animation Lab

```text
[Blender .blend] → export glTF 2.0 → enclosure_twin.glb
    → [Bitstream Studio / Twin host]: place model · mark sensor/interaction · play clip
        → (ทางเลือก) live telemetry (Simulator หรือ Board)
```

| รูปแบบ | ใช้เมื่อ |
|---|---|
| **`.glb`** | เป้าหมายหลัก — ไฟล์เดียวรวม mesh + materials + animations |
| `.gltf` + bins/textures | เมื่อต้องการแยก texture แก้ไขภายนอก |
| STL | เก็บไว้พิมพ์ในโมดูล 6 — ไม่แทน GLB สำหรับ Twin |

---

## เตรียมไฟล์ก่อน export ทุกครั้ง

| ขั้น | ทำ | ทำไม |
|---|---|---|
| 1 | ตรวจหน่วยทีมยังตรงบทเรียน 1.1 | กันสเกลเพี้ยนใน Twin |
| 2 | `Ctrl+A` → Scale (และ Rotation ถ้าจำเป็น) | จำเป็นก่อน export |
| 3 | Origin ของฝาอยู่ที่บานพับ (จากโมดูล 3) | คลิปหมุนถูกจุด |
| 4 | ลบ/ซ่อน cutter, ไฟทดสอบ, กล้องที่ไม่ต้องการส่ง | ไฟล์เบาและไม่รก |
| 5 | ชื่อ object เป็นภาษาอังกฤษสั้น | อ้างใน Twin / checklist |

ใช้ **Principled BSDF** ตามที่ฝึกในโมดูล 2 — glTF รองรับพารามิเตอร์หลักได้ดี ถ้ามีหลายคลิป (`lid_open`, `lid_close`) ให้ Stash ลง NLA ให้ครบก่อน export โดยใช้ชื่อเดียวกับ clip list ในโมดูล 3

---

## ตัวอย่างสมบูรณ์ (1) — ส่งออก glTF Binary

**ท่าที่ 1** เลือกเฉพาะชิ้นที่จะส่ง (หรือทั้ง scene ตามที่ทีมตกลง)

**ท่าที่ 2** `File → Export → glTF 2.0` → Format: **glTF Binary (.glb)** → เปิดอย่างน้อย: Selected Objects · Apply Modifiers · Materials · Animations (ถ้ามีคลิป)

**ท่าที่ 3** เลือก Animation Mode: **Actions** (มี active action หรือ stash แล้ว) หรือ **NLA Tracks** (หลายแทร็กเป็นคลิปแยกชัด)

**ท่าที่ 4** ตั้งชื่อไฟล์ เช่น `enclosure_twin.glb` แล้ว Export ตรวจขนาดไฟล์และเปิดดูว่าคลิปยังเล่นได้ จดตัวเลือกที่ใช้จริงลง [export-twin-checklist.md](resources/export-twin-checklist.md)

---

## ตัวอย่างสมบูรณ์ (2) — นำเข้า Bitstream Studio

**ท่าที่ 5** เปิด [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) จาก VS Code แล้วนำเข้าไฟล์ `.glb` ตาม UI ของรอบนั้น เช่น แผง Assets / Model / Sensor Studio / Animation Lab

**ท่าที่ 6 — ตรวจหลังนำเข้า**

| ตรวจ | ผ่านเมื่อ |
|---|---|
| Model visible | เห็นกล่องใน viewport |
| Scale usable | ไม่จิ๋ว/ยักษ์ผิดปกติ |
| Up-axis / orientation | วางบน "พื้น" ได้โดยไม่ต้องหมุนแก้ยาว |
| Animation (ถ้ามี) | เล่น `lid_open` ได้ |

ถ้าสเกลผิด: **กลับไปแก้ใน Blender แล้ว export ใหม่** อย่าซูมแก้ใน Twin แล้วถือว่าจบ

---

## จุดเซ็นเซอร์และจุดโต้ตอบ

เป้าหมาย: ให้ทีมออกแบบกับทีมเฟิร์มแวร์พูดภาษาเดียวกัน

| ชนิดจุด | ตัวอย่างบนกล่อง | เชื่อมกับ |
|---|---|---|
| **Sensor node** | ช่องเหนือ IMU / อุณหภูมิ | ชื่อเซ็นเซอร์ เช่น `bmi270`, `sht40` |
| **Interaction point** | ฝา · ปุ่ม · LED window | คลิป `lid_open` · สถานะ LED |
| **Mount / placement** | ฐานวางโต๊ะ · รูสกรู | origin การวางในฉาก |

ชื่อที่ใช้ เช่น `sensor_bmi270_slot`, `interact_lid`, `led_status_window` — ระบุอย่างน้อย **1 จุด** ที่อธิบายได้ชัดพร้อมหลักฐาน (Empty ที่ export ไปด้วย หรือโน้ตตำแหน่ง + สกรีนช็อต)

---

## ทดสอบด้วย telemetry หรือ motion data

| การทดสอบ | วิธี | ผ่านเมื่อ |
|---|---|---|
| **A — วางนิ่ง** | โมเดลนิ่งใน Twin | ขนาด/แกนใช้ได้ |
| **B — เล่นคลิป** | เล่น `lid_open` ใน host | ฝาเปิดตามที่ออกแบบ |
| **C — ข้อมูลจริง/จำลอง** (แนะนำ) | Link Simulator หรือ Board | ค่าเซ็นเซอร์ไหลขณะโมเดลอยู่บนจอ |

ไม่ต้องครบทุกข้อในบทเรียนนี้ — เลือกอย่างน้อยหนึ่งเส้นทางที่มีหลักฐาน (สกรีนช็อตหรือคลิป)

---

## เช็กความเข้าใจ / ไปต่อ

ตอบคำถามใน [quiz.yaml](quiz.yaml) — สามข้อ ผูกกับเป้าหมายของบทเรียนนี้ข้อละหนึ่งคำถาม ลองตอบเองก่อนแล้วค่อยเทียบกับเฉลยในไฟล์

## ฝึกเติม/แล็บ

ลงมือต่อที่ [แล็บ: ส่งออก GLB และนำเข้า Twin](../l02-lab/README.md) (~2.5–3 ชั่วโมง)

- ได้ไฟล์ `.glb` จากโมเดลโมดูล 2/3 แล้วนำเข้า Bitstream Studio
- กำหนดจุด sensor หรือ interaction อย่างน้อย 1 จุดพร้อมชื่อ และทดสอบด้วยคลิปหรือ telemetry

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มา

"การออกแบบผลิตภัณฑ์เชิงอุตสาหกรรม (Blender และ Digital Twin)" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY-NC 4.0 (ดัดแปลง)

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)

เครื่องมือ Bitstream Studio (VS Code) และ Ternion ที่หลักสูตรนี้ใช้ เป็นผลงานของ ผศ.ดร.สันติ นุราช (KMUTT)
