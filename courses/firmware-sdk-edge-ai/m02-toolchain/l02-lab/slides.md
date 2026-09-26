---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 2.2 — แล็บ: สร้าง build flash และ debug โปรเจกต์เฟิร์มแวร์"
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

# บทเรียน 2.2 — แล็บ: สร้าง build flash และ debug โปรเจกต์เฟิร์มแวร์

## ตรวจเครื่อง สร้างโปรเจกต์จาก BSP build ใน VS Code flash ลงบอร์ด และ debug อย่างน้อยหนึ่งครั้ง

**หลักสูตร TESA Firmware SDK สำหรับ Edge AI — โมดูล 2 · แล็บ**

---

## เป้าหมาย

เมื่อทำครบ คุณจะ

- ติดตั้ง/ตรวจสภาพแวดล้อม ModusToolbox™ + VS Code ให้พร้อม
- สร้างโปรเจกต์จาก BSP ของคิตในมือ
- Build สำเร็จใน VS Code หรือเทอร์มินัล
- Flash และยืนยันผลบนบอร์ดจริง
- เปิด debug session อย่างน้อยหนึ่งครั้ง

---

## ก่อนเริ่ม

- [ ] อ่านจบ [บทเรียน 2.1](../l01-modustoolbox-and-vscode/README.md)
- [ ] เครื่องติดตั้งตามรายการในบทเรียน (หรือตามคู่มือของชุดที่ใช้)
- [ ] บอร์ด PSOC™ Edge + สาย USB
- [ ] รู้รหัส/ชื่อคิตที่ใช้เลือก BSP

> **หลัง flash สำเร็จ — ดู telemetry บนโฮสต์**: ติดตั้ง Bitstream Studio จาก Marketplace (หรือจาก `vsix/` ในแพ็กแล็บ) แล้วใช้ Command Palette → Bitstream Studio: Open Bitstream Studio / Start Serial Bridge
> **แพ็ก HEX / Flasher / demos:** [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)

---

## ดูของจริงก่อน — Part 1: Environment Check

บันทึกผลลงโน้ตก่อนลงมือสร้างโปรเจกต์:

| รายการ | มีแล้ว? | หมายเหตุ |
|---|---|---|
| ModusToolbox™ tools (ระบุเวอร์ชัน) | | |
| Arm GNU Toolchain (GCC) | | |
| VS Code | | |
| ส่วนขยายที่ชุดแล็บกำหนด | | |
| Terminal emulator (ถ้าต้องดู UART) | | |

**ผ่านเมื่อ:** ตรวจรายการข้างบนครบว่าเครื่องพร้อม หรือสร้างโปรเจกต์ใหม่ได้ใน Part 2

---

## ฝึกเติม/แล็บ (1) — Part 2: Create a Project

1. เปิด **ModusToolbox™ Dashboard** หรือ **Project Creator**
2. เลือก **BSP/Kit** ให้ตรงบอร์ดในมือ
3. เลือกตัวอย่างเริ่มต้น — แนะนำเปิดจาก **TESAIoT Developer Hub** (Example Explorer → กรอง Board ตามคิต)
4. เลือกเป้าหมาย **VS Code**
5. สร้างโปรเจกต์ลงโฟลเดอร์ที่ตั้งชื่อเป็นระเบียบ

บันทึก: ชื่อโปรเจกต์ · BSP ที่เลือก · path โฟลเดอร์

**ผ่านเมื่อ:** มีไฟล์ `.code-workspace` ในโปรเจกต์

---

## ฝึกเติม/แล็บ (2) — Part 3: Open in VS Code and Build

1. เปิดไฟล์ **`*.code-workspace`** ด้วย VS Code
2. รัน **build** ตามเวิร์กโฟลว์ที่เลือกใช้ (ปุ่มใน IDE หรือ `make` ในเทอร์มินัลโปรเจกต์)
3. แก้ error เบื้องต้นถ้ามี (toolchain / path / library)

บันทึก: ผล build สำเร็จครั้งแรกใช้เวลาประมาณเท่าไร และ error ที่เจอ (ถ้ามี)

**ผ่านเมื่อ:** build สำเร็จโดยไม่มี error

---

## ฝึกเติม/แล็บ (3) — Part 4: Flash to the Board

1. เสียบ USB ให้ KitProg พร้อม
2. Program/Flash ตาม launch config หรือคำสั่งที่เอกสารกำหนด
3. สังเกตผลบนบอร์ด (LED / พฤติกรรมตามตัวอย่าง)
4. ถ้าตัวอย่างมี UART: เปิด terminal ที่ baud ตามคู่มือ แล้วบันทึกข้อความที่ได้

**ผ่านเมื่อ:** เห็นพฤติกรรมที่ยืนยันว่าเฟิร์มแวร์ใหม่รันบนบอร์ด

---

## ฝึกเติม/แล็บ (4) — Part 5: Debug Once

1. ตั้ง breakpoint ใน `main` หรือฟังก์ชันที่เห็นชัดในตัวอย่าง
2. เริ่ม debug session
3. ยืนยันว่า halt ที่ breakpoint ได้ แล้ว resume/step อย่างน้อยหนึ่งครั้ง

บันทึก: ชื่อ configuration ที่ใช้ และ halt ที่บรรทัด/ฟังก์ชันใด

**ผ่านเมื่อ:** debug ทำงานได้อย่างน้อยหนึ่งรอบ

---

## เช็กความเข้าใจ — Part 6: Configuration Awareness

เปิด **Device Configurator** (`make device-configurator` หรือจาก IDE) หา peripheral ที่ตัวอย่างใช้ (เช่น GPIO สำหรับ LED หรือ UART) แล้วเปิด **Library Manager** ดูรายการไลบรารีที่มีในโปรเจกต์ ตอบสั้น ๆ:

1. BSP ของคุณชื่ออะไร
2. ไลบรารีหนึ่งตัวที่เห็นใน Library Manager คืออะไร
3. ถ้าเลือก BSP ผิดคิต จะเสี่ยงปัญหาแบบใด

---

## ไปต่อ

ก่อนส่งงาน ตรวจกับตัวเองว่า:

- [ ] Part 1 ตรวจเครื่องแล้ว
- [ ] สร้างโปรเจกต์ BSP ตรงคิต
- [ ] Build สำเร็จ
- [ ] Flash แล้วเห็นผลบนบอร์ด
- [ ] Debug halt ได้อย่างน้อยหนึ่งครั้ง
- [ ] ตอบคำถาม Part 6 ครบ

พร้อมแล้ว ไปต่อ **โมดูล 3 — GPIO และอุปกรณ์ต่อพ่วงพื้นฐาน**

[บทเรียนโมดูล 3 →](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md)

---

## แหล่งที่มา

"บทเรียน 2.2 — แล็บ: สร้าง build flash และ debug โปรเจกต์เฟิร์มแวร์" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY 4.0

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)
นำเข้าจาก drsanti/TESAIoT-Courses — C1 (commit `287c218`) ภายใต้สัญญาอนุญาต CC BY 4.0

ไม่มีภาพจากบุคคลที่สามในสไลด์ชุดนี้
