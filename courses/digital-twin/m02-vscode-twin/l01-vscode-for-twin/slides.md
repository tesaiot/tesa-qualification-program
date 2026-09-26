---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 2.1 — ตั้งโฮสต์ Twin ใน VS Code ด้วย Bitstream Studio"
footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · ดัดแปลงจากงานของ ผศ.ดร.สันติ นุราช (KMUTT) · CC BY 4.0"
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

# บทเรียน 2.1 — ตั้งโฮสต์ Twin ใน VS Code ด้วย Bitstream Studio

## ติดตั้ง Bitstream Studio (Marketplace หรือ VSIX) จัด workspace ผูกเฟิร์มแวร์ รู้จัก backend services และไล่ปัญหาเมื่อ UI ว่าง

**พัฒนาเฟิร์มแวร์ร่วมกับ TESA Digital Twin บน VS Code — โมดูล 2 · บทเรียน 1**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. ติดตั้ง Bitstream Studio ด้วยเส้นทาง Marketplace หรือ VSIX และเลือกเวอร์ชัน VSIX ให้ตรงกับ HEX
2. เปิดเซสชันแรกแบบ Simulator หรือ Bitstream (UART) จนเห็นค่าเซ็นเซอร์ขยับบนแผง telemetry
3. ไล่หาสาเหตุเมื่อ UI ว่างตามลำดับ extension → backend → link → source streaming → แผงที่ถูกต้อง

---

## ก่อนเริ่ม

- ผ่าน [บทเรียน 1.2 — แล็บ M01](../../m01-twin-architecture/l02-lab/README.md) มาแล้ว
- ต้องใช้ Visual Studio Code 1.75 ขึ้นไป (หรือ Cursor)
- ทำได้ด้วยโหมด Simulator (ไม่ต้องมีบอร์ด) หรือใช้บอร์ด TESAIoT PSoC Edge DevKit จริง

---

## ดูของจริงก่อน — ทำไม VS Code เป็นศูนย์กลาง

ใน Course 2 **Visual Studio Code** ไม่ใช่แค่ตัวพิมพ์โค้ด — เป็นศูนย์กลางที่เชื่อม:

| ชิ้น | บทบาท |
|---|---|
| โปรเจกต์เฟิร์มแวร์ | จาก Course 1 / ModusToolbox / โฟลเดอร์แล็บ |
| **Bitstream Studio** | Twin host — telemetry, Sensor Studio, MQTT, 3D |
| **Bitstream Simulator** (เสริม) | Virtual MCU เมื่อไม่มีบอร์ด |
| Backend services | Serial bridge, MQTT broker บน localhost |

```text
[VS Code]
   ├─ Firmware folder (edit / debug)
   ├─ Bitstream Studio webview  ← Twin UI
   ├─ Bridge :9998              ← Communication
   └─ (optional) Simulator VSIX ← Virtual device stream
```

> **Key phrase**: บทเรียนก่อนหน้า (Course 1 M02) สอน *สร้างและ flash เฟิร์มแวร์* — บทเรียนนี้สอน *เปิดโฮสต์ Twin ให้คุยกับเฟิร์มแวร์หรือ Simulator*

---

## แนวคิด — ติดตั้ง extension สองเส้นทาง

| เส้นทาง | ขั้นตอน |
|---|---|
| **A: Marketplace** | เปิด Extensions → ค้นหา Bitstream Studio → Install → Reload → Command Palette → Open Bitstream Studio |
| **B: Hackathon VSIX** | clone TESAIoT_Hackathon → เลือก `vsix/bitstream-studio-<version>.vsix` → Install from VSIX… → Reload |

```bash
code --install-extension vsix/bitstream-studio-0.1.8.vsix
code -r
```

> **Version matching**: VSIX กับ HEX ควรเป็นชุดเดียวกัน — ดู `latest` ใน firmware manifest ของ Hackathon เมื่อไม่แน่ใจ

อย่า commit รหัสผ่านหรือ token ลงไฟล์ผลงาน

---

## แนวคิด — จัด workspace และผูกเฟิร์มแวร์

```text
my-course2-workspace/
  firmware/          # โปรเจกต์ C จาก MTB / TESA (หรือลิงก์ไปโปรเจกต์ Course 1)
  lab-notes/         # โน้ต / สกรีนช็อต / setup sheet
  .vscode/           # tasks / settings ของทีม (ถ้ามี)
```

**"ผูกโปรเจกต์" หมายถึง:**

| ขั้น | ทำอะไร |
|---|---|
| 1 | เปิดโฟลเดอร์ workspace ที่มีเฟิร์มแวร์ |
| 2 | เปิด Bitstream Studio ในหน้าต่างเดียวกัน |
| 3 | เลือกแหล่งข้อมูล: Simulator หรือ Bitstream + COM ที่ถูกต้อง |
| 4 | (ถ้ามีบอร์ด) flash HEX ที่จับคู่ VSIX แล้วเปิดพอร์ต |
| 5 | กด Link / Connect จนเห็นสตรีม |

จำจากโมดูล 1: มีได้ทีละ backend เดียว — อย่าผสม uart+sim

---

## แนวคิด — backend services ที่เริ่มอัตโนมัติ

| บริการ | พอร์ตที่พบบ่อย | บทบาท |
|---|---|---|
| Serial / WS bridge | **9998** | คุยระหว่าง webview ↔ UART / Simulator |
| MQTT broker (local) | **1883** / **8883** | ใช้ในแล็บ cloud ภายหลัง (โมดูล 5) |

| คำสั่งโดยประมาณ | เมื่อใช้ |
|---|---|
| Open Bitstream Studio | เปิด UI หลัก |
| Start / Stop Bitstream Simulator | โหมดไม่มีบอร์ด |
| Start All / Shutdown Backend Services | แก้พอร์ตชน หรือสลับไป terminal dev |

> **Multi-editor tip**: เปิด VS Code กับ Cursor พร้อมกันได้ แต่ bridge มี owner เดียว — ถ้าพอร์ตติด ให้ Shutdown จากหน้าต่างที่เป็นเจ้าของ แล้วค่อยเปิดใหม่

---

## ตัวอย่างสมบูรณ์ — เซสชันแรกแบบ Simulator (แนะนำก่อน)

ลำดับที่ลดความเสี่ยงฮาร์ดแวร์:

1. ติดตั้ง Bitstream Studio (+ Simulator ถ้าต้องการโหมดไม่มีบอร์ด)
2. **Open Bitstream Studio**
3. Toolbar → แหล่งข้อมูล **Simulator**
4. สตาร์ท Simulator / Streaming
5. กด **Link / Connect**
6. เปิด **Sensor Telemetry**

**ผ่านเมื่อ:** เห็นค่าเซ็นเซอร์จำลองขยับภายในไม่กี่วินาที และสถานะลิงก์ปกติ

---

## ตัวอย่างสมบูรณ์ — เซสชันแรกแบบ Bitstream (บอร์ดจริง)

1. Flash HEX จาก Hackathon (`hex/`) ด้วย Flasher หรือ ModusToolbox — เวอร์ชันจับคู่ VSIX
2. เสียบ USB / เลือก COM
3. Toolbar → **Bitstream**
4. **Link / Connect** จน handshake สำเร็จ
5. ดู Telemetry / Sensor Studio

**ผ่านเมื่อ:** มีสตรีมจากบอร์ด (origin ฝั่ง uart) และ UI ไม่ว่าง

---

## แนวคิด — ไล่ปัญหาเมื่อ UI ว่าง

แยกปัญหาเป็นชั้น (จากง่าย → ยาก):

1. Extension ยังไม่พร้อม / ไม่มีคำสั่ง
2. Backend พอร์ตชน
3. ยังไม่ Link หรือเลือกโหมดผิด
4. เฟิร์มแวร์/ Simulator ยังไม่สตรีม
5. Visualization คนละ workspace / ยังไม่เปิดแผง

> **Key phrase**: ถ้า UI ว่าง ให้ถามตามลำดับ: *extension? backend? link? source streaming? correct panel?*

---

## ฝึกเติม/แล็บ

[แล็บ: ติดตั้ง Twin บน VS Code และเซสชันแรก](../l02-lab/README.md)

- ติดตั้ง Bitstream Studio ด้วยเส้นทางใดเส้นทางหนึ่ง
- จัด workspace แยกชัดและเปิดซ้ำได้
- เปิดเซสชันแรก (Simulator หรือ Bitstream) จนเห็น telemetry ขยับ
- ฝึกไล่ปัญหาตามลำดับ 5 ชั้นถ้า UI ว่าง

---

## เช็กความเข้าใจ

1. ทำไมบทเรียนย้ำว่า VSIX กับ HEX ควรเป็นชุดเดียวกัน
2. โหมดใดที่บทเรียนแนะนำให้ลองเป็นอย่างแรกเพื่อลดความเสี่ยงฮาร์ดแวร์
3. เรียงลำดับคำถามที่ควรถามเมื่อ UI ว่าง จากรายการนี้: link? · extension? · correct panel? · backend? · source streaming?

---

## ไปต่อ

- ติดตั้ง Bitstream Studio ได้ทั้งจาก Marketplace หรือ VSIX ที่จับคู่เวอร์ชันกับ HEX
- จัด workspace แยกชัด แล้วผูกเฟิร์มแวร์เข้ากับ Twin host
- เซสชันแรก: Simulator ก่อนเพื่อลดความเสี่ยง แล้วค่อยลอง Bitstream บนบอร์ดจริง
- พร้อมแล้วสำหรับ **โมดูล 3 — การสร้างแบบจำลองอุปกรณ์เสมือน**

[บทเรียนโมดูล 3 →](../../m03-virtual-device/l01-virtual-device-modeling/README.md)

---

## แหล่งที่มา

"บทเรียน 2.1 — ตั้งโฮสต์ Twin ใน VS Code ด้วย Bitstream Studio" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY 4.0

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)
นำเข้าจาก drsanti/TESAIoT-Courses — C2 (commit `287c218`) ภายใต้สัญญาอนุญาต CC BY 4.0

ไม่มีภาพจากบุคคลที่สามในสไลด์ชุดนี้
