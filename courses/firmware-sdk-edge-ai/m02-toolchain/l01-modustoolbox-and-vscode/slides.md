---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 2.1 — ModusToolbox™ และ VS Code: สร้าง build flash debug"
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

# บทเรียน 2.1 — ModusToolbox™ และ VS Code: สร้าง build flash debug

## แยกบทบาทของ ModusToolbox™, VS Code, KitProg3 และ SDK ตั้ง environment ให้ครบ เลือก BSP ให้ตรงคิต และรู้วิธีไล่อาการเสียที่พบบ่อย

**หลักสูตร TESA Firmware SDK สำหรับ Edge AI — โมดูล 2 · บทเรียน 1**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. ระบุว่างานที่กำหนดให้ (สร้างโปรเจกต์, แก้โค้ด, flash/debug, เรียก API) เป็นหน้าที่ของ ModusToolbox™, VS Code, KitProg3/OpenOCD หรือ SDK
2. ระบุองค์ประกอบ environment ที่ต้องมีก่อน build (tools, Arm GCC, VS Code, สิทธิ์ USB ของ KitProg) และเลือก BSP ให้ตรงกับคิตในมือ
3. ใช้ตาราง troubleshooting เชื่อมอาการเสียกับสาเหตุที่น่าจะเป็นได้ถูกต้อง

---

## ก่อนเริ่ม

- ผ่าน [บทเรียน 1.2 — แล็บ M01](../../m01-mcu-architecture/l02-lab/README.md) มาแล้ว
- **ต้องใช้บอร์ดจริง**: TESAIoT Dev Kit หรือ Eva Kit (KIT_PSE84_EVAL) พร้อมสาย USB
- บทเรียนเชิงปฏิบัติ ใช้เครื่องพัฒนา + บอร์ดจริง (ต่างจากโมดูล 1 ที่เป็นแนวคิดล้วน)

> **หมายเหตุเวอร์ชัน**: ให้ยึดเวอร์ชันที่ชุดแล็บของคุณกำหนดเป็นหลัก — คู่มือ Infineon มักแนะนำ ModusToolbox™ tools 3.6 หรือใหม่กว่า

---

## ดูของจริงก่อน — สามเครื่องมือ สามบทบาท

จากบทเรียนที่แล้วเรารู้ว่า TESA Firmware SDK คือชุดไลบรารี/API ที่แอปเรียกใช้ ส่วนเครื่องมือพัฒนาเป็นอีกชั้นหนึ่ง

| เครื่องมือ | บทบาทหลักในหลักสูตรนี้ |
|---|---|
| **ModusToolbox™** | ติดตั้ง toolchain, สร้างโปรเจกต์จาก BSP/template, จัดการ library, เปิด configurator |
| **Visual Studio Code** | เขียนโค้ด, IntelliSense, build/debug ผ่านเวิร์กโฟลว์ที่ ModusToolbox™ รองรับ |
| **KitProg3 / OpenOCD** (บนคิต) | Flash และ debug บนฮาร์ดแวร์จริง |

> **Key phrase**: ModusToolbox™ ใช้สร้างโปรเจกต์และจัดการ toolchain/library — VS Code ใช้เขียนโค้ดและ debug — SDK คือ API ที่แอปเรียกใช้

---

## แนวคิด (1) — ติดตั้งอะไรบ้างสำหรับ PSOC™ Edge

จาก PSOC™ Edge quick start guide ควรติดตั้งอย่างน้อย:

1. **ModusToolbox™ Setup** ตามคู่มือติดตั้งของ OS
2. **Arm® GNU Toolchain (GCC)**
3. **Base tools package** เวอร์ชันที่รองรับ Edge (**3.6+** ตาม quick start)
4. **IDE ตัวเลือก** — หลักสูตรนี้เลือก **VS Code**
5. **Programming tools package** ตามที่ Setup เสนอ

> LLVM Embedded Toolchain for Arm ไม่รวมใน Setup มาตรฐาน — ติดตั้งเพิ่มเมื่อคู่มือของชุดที่ใช้ระบุ

---

## แนวคิด (2) — สร้างโปรเจกต์ด้วย Project Creator

ลำดับมาตรฐาน:

1. เปิด **ModusToolbox™ Dashboard** หรือเปิด **Project Creator** โดยตรง
2. เลือก **Kit / BSP** ที่ตรงกับบอร์ดในมือ (เช่นตระกูล KIT_PSE84_EVAL)
3. เลือก **code example** — แนะนำเปิดตัวอย่างจาก **TESAIoT Developer Hub** (กรอง Board/Domain ตามคิตในมือ)
4. ใน Target IDE เลือก **Visual Studio Code**
5. ระบุโฟลเดอร์ปลายทาง แล้วให้เครื่องมือ clone BSP/template และดึงไลบรารีจาก manifest

ผลลัพธ์ที่คาดหวัง: โครงสร้างโปรเจกต์พร้อม `make` · ไลบรารี/BSP ที่ดึงมาแล้ว · ไฟล์ `*.code-workspace`

---

## แนวคิด (3) — เปิดโปรเจกต์ให้ถูกวิธีใน VS Code

1. สร้างโปรเจกต์ด้วย Project Creator โดยเลือก target เป็น VS Code
2. เปิด **VS Code ด้วยมือ**
3. เปิดไฟล์ **`{project-name}.code-workspace`** ในโฟลเดอร์โปรเจกต์

> อย่าเปิดแค่โฟลเดอร์ย่อยแบบสุ่มจน task/launch configuration หาย — ให้เปิดไฟล์ workspace ที่เครื่องมือสร้างให้

Build = เรียก **ระบบ make ของโปรเจกต์** ที่ ModusToolbox™ สร้างไว้ (ไม่ว่าจะกดปุ่มใน VS Code หรือใช้เทอร์มินัล)

---

## แนวคิด (4) — BSP ต้องตรงคิตเสมอ

**BSP (Board Support Package)** บอกโปรเจกต์ว่าใช้ชิป/บอร์ดใด ขาและอุปกรณ์บนบอร์ดแมปอย่างไร และต้องดึงไลบรารีใดเป็นอย่างน้อย

> การเลือก BSP ผิดตอนสร้างโปรเจกต์ = โค้ดอาจ build ได้แต่ **ขา LED/UART ไม่ตรงของจริง**

กฎง่าย ๆ: **เลือก BSP ให้ตรงกับคิตที่เสียบอยู่**

**Program vs Debug**

| การกระทำ | ความหมาย |
|---|---|
| Program / Flash | เขียนเฟิร์มแวร์ลงหน่วยความจำของอุปกรณ์ |
| Debug | มักรวมการ program แล้วหยุดที่ breakpoint / step โค้ดผ่าน GDB + OpenOCD หรือ probe อื่น |

---

## แนวคิด (5) — สแต็กเดียวกับที่เรียนในโมดูล 1

```text
VS Code (edit / build / debug)
        │
ModusToolbox™ tools (create, libraries, configurators, OpenOCD)
        │
Application  →  Utility / Driver API (TESA Firmware SDK ในหลักสูตร)
        │
BSP / PDL / HAL (Device Support)
        │
PSOC™ Edge hardware
```

โมดูล 2 ทำให้คุณพร้อมสร้างและรันโปรเจกต์บนเครื่องมือจริง — โมดูล 3 จะให้คุณเรียก Driver API บนโปรเจกต์นี้อย่างตั้งใจ

---

## ตัวอย่างสมบูรณ์ — เกณฑ์ผ่านขั้นต่ำของโมดูลนี้

เป้าหมายขั้นต่ำ (Hello World path):

1. Build โปรเจกต์ตัวอย่างผ่าน **หรือ** flash HEX จากแพ็กแล็บสำเร็จ
2. Program ลงบอร์ดสำเร็จ
3. เห็นพฤติกรรมที่ยืนยันได้ เช่น LED กระพริบ และ/หรือข้อความบน serial terminal / telemetry ใน Bitstream Studio
4. เปิด debug session ได้ อย่างน้อย halt ที่ `main` หรือ breakpoint ง่าย ๆ (เมื่อใช้เส้นทาง build จากซอร์ส)

เปิด Device Configurator จากโฟลเดอร์โปรเจกต์:

```bash
make device-configurator
```

---

## ตัวอย่างสมบูรณ์ — ไล่อาการเสียที่พบบ่อย

| อาการ | แนวทางตรวจ |
|---|---|
| บอร์ดไม่ปรากฏ / ไม่ program ได้ | สาย USB, พอร์ต, KitProg3, ไดรเวอร์, ลองพอร์ตอื่น |
| Build หา toolchain ไม่เจอ | ติดตั้ง GCC/tools ตาม Setup, เปิดเทอร์มินัลที่ถูกต้อง |
| Build ผ่านแต่ไม่มีอาการบนบอร์ด | BSP ผิดคิต, ยังไม่ได้ program, ดูคนละ LED/UART |
| Debug ต่อไม่ได้ | OpenOCD/KitProg, ปิดโปรแกรมที่ครองพอร์ต, ตรวจ launch config |
| Flash HEX แล้วไม่มี telemetry | VSIX กับ HEX คนละเวอร์ชัน, baud ไม่ใช่ 921600, ยังไม่ Link ใน Bitstream Studio |

ดูตารางเต็ม (6 แถว) ใน [README.md](README.md) หัวข้อ 6.5

---

## ฝึกเติม/แล็บ

[แล็บ: สร้าง build flash และ debug โปรเจกต์เฟิร์มแวร์](../l02-lab/README.md) — บทเรียนเชิงปฏิบัติ ~90–120 นาที รวมติดตั้ง

- ติดตั้ง environment ให้ครบตามเช็กลิสต์
- สร้างโปรเจกต์จาก BSP ที่ตรงกับคิตในมือ
- Build → Program → เห็นผลลัพธ์บนบอร์ดจริง
- เปิด debug session อย่างน้อยหนึ่งครั้ง

---

## เช็กความเข้าใจ

1. เครื่องมือใดทำหน้าที่ "สร้างโปรเจกต์จาก BSP/template และจัดการ toolchain / library"
2. ข้อใดเป็นเงื่อนไขที่บทเรียนย้ำว่า "ต้องตรง" ก่อนคาดหวังผลบนบอร์ด
3. Flash HEX แล้วแต่ไม่มี telemetry ใน Bitstream Studio ตารางในหัวข้อ 6.5 ชี้สาเหตุใด

---

## ไปต่อ

- **Environment** ที่ถูกต้อง = tools + GCC + VS Code + สิทธิ์เข้าถึง KitProg
- เปิดโปรเจกต์ผ่าน **`.code-workspace`** แล้ว build/debug ตามเวิร์กโฟลว์ Infineon
- **BSP ต้องตรงคิต**; ใช้ Device Configurator และ Library Manager เป็นทางหลัก
- **Flash + Debug บนบอร์ดจริง** คือเกณฑ์ผ่านของโมดูลนี้ — พร้อมแล้วสำหรับ **โมดูล 3 — GPIO และอุปกรณ์ต่อพ่วงพื้นฐาน**

[บทเรียนโมดูล 3 →](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md)

---

## แหล่งที่มา

"บทเรียน 2.1 — ModusToolbox™ และ VS Code: สร้าง build flash debug" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY 4.0

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)
นำเข้าจาก drsanti/TESAIoT-Courses — C1 (commit `287c218`) ภายใต้สัญญาอนุญาต CC BY 4.0

ไม่มีภาพจากบุคคลที่สามในสไลด์ชุดนี้
