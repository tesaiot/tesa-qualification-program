---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 3.2 — แล็บ: สร้าง Virtual Device และ event script"
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

# บทเรียน 3.2 — แล็บ: สร้าง Virtual Device และ event script

## สร้างโมเดลอุปกรณ์ กำหนด behavior เขียนสคริปต์เหตุการณ์ที่รันซ้ำได้ และ (แนะนำ) ฝึก Blender สั้น ๆ แล้วส่งออก GLB

**พัฒนาเฟิร์มแวร์ร่วมกับ TESA Digital Twin บน VS Code — โมดูล 3 · แล็บ**

---

## เป้าหมาย

เมื่อทำครบ คุณจะ

1. สร้างโมเดลอุปกรณ์ (device-model.json หรือเทียบเท่า) ที่มีเซ็นเซอร์ ≥ 2 ชนิดและ behavior ≥ 1 เส้นทาง
2. รัน event script ซ้ำและเก็บหลักฐานผลบน visualization

---

## ก่อนเริ่ม

- [ ] Lab โมดูล 2 ผ่าน (เปิด Bitstream Studio ได้)
- [ ] เลือกเส้นทาง: Simulator และ/หรือบอร์ดที่สตรีมได้
- [ ] มีโฟลเดอร์ `lab-notes/` สำหรับไฟล์โมเดล + หลักฐาน
- [ ] (Lab E) ติดตั้ง Blender ถ้าจะทำส่วน 3D

**เวลาที่แนะนำ:** ~3–3.5 ชม. (Virtual Device) + ~1–1.5 ชม. (Lab E Blender ถ้าทำ)

---

## ดูของจริงก่อน — เกณฑ์ผ่านของแต่ละบล็อก

| บล็อก | เกณฑ์ผ่าน |
|---|---|
| Lab A — Create the model (required) | ไฟล์โมเดลอ่านรู้เรื่อง และโฮสต์แสดงค่าที่เกี่ยวข้องอย่างน้อยหนึ่งช่อง |
| Lab B — Behavior (required) | เพื่อนในทีมกระตุ้นอินพุตแล้วชี้ผลบนจอได้โดยไม่เดา |
| Lab C — Event script (required) | รันสคริปต์ซ้ำแล้วได้ลำดับผลเดียวกันโดยประมาณ |
| Lab E — Blender (แนะนำ) | มีไฟล์ `.glb` และหลักฐานว่าเปิดในโฮสต์ได้ |

---

## ฝึกเติม/แล็บ (1) — Lab A: Create the model

1. คัดลอก template เป็นไฟล์ของคุณ เช่น `lab-notes/device-model.json`
2. ตั้ง `deviceId` / `displayName` ให้ทีมจำได้
3. เปิดใช้เซ็นเซอร์อย่างน้อย 2 ชนิดจากชุด: switch, temperature/pressure, IMU
4. กำหนด `default` และช่วง `min`/`max` ให้สมเหตุสมผล
5. ระบุ actuator อย่างน้อย 1 ตัว (LED / flag / log sink)

บนโฮสต์: เปิด Simulator หรือบอร์ด แล้วเลือก scene ที่สอดคล้องโมเดล

---

## ฝึกเติม/แล็บ (2) — Lab B: Behavior

กำหนดและสาธิตอย่างน้อยหนึ่งกฎ เช่น:

- คำสั่ง/ปุ่ม → LED หรือสถานะบน UI
- อุณหภูมิเกินเกณฑ์ → event / ข้อความ log / การเปลี่ยนโหมด

เขียนเป็นประโยค `WHEN … THEN …` ใน checklist

---

## ฝึกเติม/แล็บ (3) — Lab C: Event script

เขียนไทม์ไลน์อย่างน้อย 4 จังหวะ แล้วรันจริง:

1. เริ่มจากค่า default / Lab Quiet
2. กระตุ้นสเกลาร์หรือสวิตช์ตามเวลา
3. กระตุ้น IMU หรือสลับไป Motion (ถ้าโมเดลมี IMU)
4. บันทึกผลที่เห็นเป็นสกรีนช็อตก่อน/หลังของคุณเอง (หรือคลิปสั้น)

อนุญาตให้รันแบบนาฬิกาจับเวลา + มือ — แต่ต้องทำซ้ำได้ในรอบที่ 2

---

## ฝึกเติม/แล็บ (4) — Lab D: Optional polish

- เพิ่ม behavior ที่สอง (threshold + command)
- เปรียบเทียบ scene Lab Quiet vs Motion บนเซ็นเซอร์ชุดเดียวกัน
- เปิด Hackathon `web-app/` เป็นจอ Visualization ชั้นนอก

---

## ฝึกเติม/แล็บ (5) — Lab E: Blender for Twin (แนะนำ)

เลือกอย่างน้อย **หนึ่ง** track ให้จบ:

- **E1 Modeling** — สร้างชิ้นส่วนง่าย (เคสกล่อง/บอร์ดแบน) จาก mesh primitive แล้ว Extrude/Bevel/Mirror ตั้ง origin + Apply Scale
- **E2 Texturing** — Unwrap UV ใส่ Principled BSDF + Base Color
- **E3 Animation** — Keyframe หมุนหรือเปิดฝา 2–3 วินาที
- **E4 Export & view** — Export → glTF 2.0 → `.glb` แล้วโหลดใน Bitstream Studio บันทึกสกรีนช็อตของคุณเองพร้อมชื่อไฟล์

---

## เช็กความเข้าใจ — ไล่อาการก่อนขอความช่วยเหลือ

ถ้าติดปัญหา ให้ตอบตัวเองก่อนว่าน่าจะตรงแถวไหน:

1. โมเดลเขียนแล้วแต่จอไม่เปลี่ยน — ควรตรวจอะไรก่อน
2. IMU ไม่ขยับ — สาเหตุที่พบบ่อยคืออะไร
3. ทำซ้ำสคริปต์ไม่ได้ — ควรแก้อย่างไร
4. GLB ไม่มี texture หรือ animation — มักลืมทำอะไร

---

## ไปต่อ

ก่อนส่งงาน ตรวจกับตัวเองว่ามีครบ:

- [ ] `device-model.json` (หรือเทียบเท่า)
- [ ] Lab A–C ผ่าน
- [ ] device-model-checklist.md กรอกครบ
- [ ] หลักฐานสคริปต์รัน (รูป/คลิปของคุณเอง)
- [ ] (แนะนำ) Lab D และ Lab E + `.glb`

พร้อมแล้ว ไปต่อ **โมดูล 4 — Co-simulation ระหว่างเฟิร์มแวร์กับ Twin**

[บทเรียนโมดูล 4 →](../../m04-cosimulation/l01-firmware-twin-cosim/README.md)

---

## แหล่งที่มา

"บทเรียน 3.2 — แล็บ: สร้าง Virtual Device และ event script" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)
นำเข้าจาก drsanti/TESAIoT-Courses — C2 (commit `287c218`) ภายใต้สัญญาอนุญาต CC BY 4.0

ไม่มีภาพจากบุคคลที่สามในสไลด์ชุดนี้
