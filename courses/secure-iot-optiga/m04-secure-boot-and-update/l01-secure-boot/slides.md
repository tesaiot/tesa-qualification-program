---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 4.1 — Secure boot และ chain of trust"
footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY-NC 4.0"
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

# บทเรียน 4.1 — Secure boot และ chain of trust

## ตามลำดับการบูตของบอร์ดและดูว่าแต่ละขั้นตรวจขั้นถัดไปอย่างไร

**โมดูล 4 — Secure boot และ Protected Update**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. อธิบายบทบาทของคอร์ CM33_S ในการบูตแบบปลอดภัยของแม่แบบเฟิร์มแวร์
2. วาดห่วงโซ่ความเชื่อใจตั้งแต่ ROM จนถึงแอปพลิเคชัน และระบุว่าลายเซ็นถูกตรวจที่ขั้นใด
3. อธิบายความต่างระหว่าง secure boot กับการเข้ารหัสเฟิร์มแวร์

---

## ก่อนเริ่ม

- เรียนมาก่อน: [บทเรียน 3.2](../../m03-mtls-to-platform/l02-mqtts-to-tesaiot/README.md), ลายเซ็น [บทเรียน 1.2](../../m01-threats-and-crypto/l02-crypto-basics/README.md)
- ซอฟต์แวร์: แม่แบบของ SDK ที่ `ef72c1b` build ได้แล้ว

**บทนี้จะไม่ให้ทำ** provision `secure_boot=true` หรือโอนความเป็นเจ้าของด้วยกุญแจ OEM — งานนี้เปลี่ยนอุปกรณ์ระดับชิป ต้องทำตาม AN237849 โดยคนที่ตัดสินใจแล้วและดูแลกุญแจ OEM ได้

---

## ดูของจริงก่อน

| Core | Runs | Typical work |
|---|---|---|
| **CM33_S** | secure boot | you will not touch this |

`proj_cm33_s/main.c` ยาวไม่ถึงห้าสิบบรรทัด — หัวไฟล์ "CM33 Secure boot - TrustZone setup and jump to CM33_NS" มีแค่ `cybsp_init()`, เปิด interrupt, อ่าน stack pointer/reset handler จากตาราง vector ของ CM33_NS แล้วกระโดดไปที่นั่น

**ทายก่อน** ก่อนกระโดด CM33_S ตรวจลายเซ็นของเฟิร์มแวร์ CM33_NS หรือไม่ ถ้าไม่ตรวจ ใครตรวจอะไร

---

## แนวคิด (1) — บทบาทของ CM33_S

PSoC™ Edge E84 มีสามคอร์ (`proj_cm33_s`, `proj_cm33_ns`, `proj_cm55`) — Extended Boot เปิด CM33 secure จากตำแหน่งคงที่ → CM33 secure เปิด CM33 non-secure → CM33 non-secure เปิด CM55

**CM33_S คือ image แรกของผู้ใช้ที่ Extended Boot เห็น และเป็นข้อต่อเดียวที่ Extended Boot ตรวจลายเซ็นได้**

สวิตช์ `SECURE_BOOT` ใน `common.mk`

- `SECURE_BOOT=0` (ค่าเริ่มต้น) — image CM33_S ได้แค่หัว MCUboot **ไม่ได้ลงนาม**
- `SECURE_BOOT=1` — CM33_S ถูกลงนามด้วยกุญแจ OEM root of trust

ค่าอื่นนอกจาก `0`/`1` (เช่น `true`, `yes`) ทำให้ build **หยุดด้วย error** — ค่าที่พิมพ์ผิดต้องไม่กลายเป็น build ที่ไม่ได้ลงนามแบบเงียบ ๆ

---

## แนวคิด (2) — ห่วงโซ่ความเชื่อใจของบอร์ดนี้

```text
 Boot ROM (Infineon) → Extended Boot (Infineon)
    │  ตรวจลายเซ็นของ image CM33_S ด้วยกุญแจ OEM
    │  ✔ เมื่อ provision secure_boot=true และ build SECURE_BOOT=1
    │  ✘ ในสภาพเริ่มต้นของแม่แบบ (SECURE_BOOT=0)
    ▼
 CM33_S   cybsp_init() แล้วกระโดดไป reset handler ของ CM33_NS
    │  ✘ ไม่ตรวจลายเซ็นของ CM33_NS
    ▼
 CM33_NS  FreeRTOS, PSA+OPTIGA driver, WiFi, MQTT แล้ว Cy_SysEnableCM55()
    │  ✘ ไม่ตรวจลายเซ็นของ CM55
    ▼
 CM55     จอ, Edge AI (โมเดลตรวจผ่าน hook ที่ยังเป็น weak function คืน "ตรวจไม่ได้")
```

**ข้อสรุปที่ต้องเขียนลง threat model** ต่อให้เปิด secure boot ครบ ห่วงโซ่ในแม่แบบนี้ก็**ขาดหลัง CM33_S** — ใครเขียน flash ของ CM33_NS หรือ CM55 ได้ จะรันโค้ดของตัวเองได้โดยไม่มีใครตรวจ

---

## แนวคิด (3) — secure boot ≠ การเข้ารหัสเฟิร์มแวร์

| | secure boot | การเข้ารหัสเฟิร์มแวร์ |
|---|---|---|
| ตอบคำถาม | โค้ดนี้มาจากเจ้าของกุญแจและไม่ถูกแก้ใช่ไหม | คนอื่นอ่านโค้ดนี้ได้ไหม |
| สมบัติ | ความถูกต้อง+ความแท้ | ความลับ |
| เครื่องมือ | ลายเซ็นดิจิทัล | การเข้ารหัสสมมาตร |
| ไม่ได้ป้องกัน | คนอ่านโค้ดใน flash, บั๊กในโค้ดที่ลงนามแล้ว | การรันโค้ดอื่นแทน (ถ้าไม่มีตรวจลายเซ็นด้วย) |

แม่แบบนี้**ไม่มีขั้นเข้ารหัส image** — เปิด secure boot แล้วใครอ่าน flash ได้ก็ยังอ่านโค้ดได้

> **ยังไม่นับเป็นมาตรการกันย้อนรุ่น** config แบบลงนามใส่ `security-counter=1` (รูปแบบ MCUboot สำหรับกันย้อนรุ่น) แต่เอกสารที่หลักสูตรนี้ตรวจไม่ได้ยืนยันว่า Extended Boot บังคับใช้เลขนี้อย่างไร — บทเรียน 4.2 มีการกันย้อนรุ่นที่ยืนยันได้ในชิป OPTIGA™

---

## ตัวอย่างสมบูรณ์ — ความต่างของสอง config

```text
// Identical to boot_with_extended_boot.json except the CM33_S sign stage
// additionally carries "signing-key" + "security-counter", which turn the
// MCUboot metadata into a real OEM signature that Extended Boot verifies
// once the device is provisioned secure_boot=true.
```

**อ่านแล้วตอบได้สามข้อ**

1. ต่างจากแบบไม่ลงนามแค่สองฟิลด์: `"signing-key"` กับ `"security-counter"`
2. **ลายเซ็นมีความหมายเมื่ออุปกรณ์ provision แล้วเท่านั้น** — บอร์ดที่ยังไม่ provision `secure_boot=true` ไม่ได้ตรวจลายเซ็นนี้
3. ผู้เขียนออกแบบให้ **"ล้มแบบมีเสียง"** — ไม่ส่งกุญแจ = build error ไม่ใช่ image ไม่ได้ลงนามเงียบ ๆ

---

## ฝึกเติม / แล็บ

**ฝึกเติม** จัดข้อความว่าเป็นจริงกับ **secure boot** / **การเข้ารหัส** / **ทั้งสอง** / **ไม่ใช่ทั้งสอง**: กันบั๊ก buffer overflow ในโค้ดที่ลงนามถูกต้อง → **ไม่ใช่ทั้งสอง** (ลายเซ็นบอกแค่ว่ามาจากใคร) · กันการเปลี่ยนเฟิร์มแวร์ CM55 แม้เปิด `SECURE_BOOT=1` แล้ว → **ไม่ใช่ทั้งสอง** (ลายเซ็นครอบแค่ CM33_S)

**แล็บ** `diff` สอง config ไฟล์ นับฟิลด์ที่ต่าง · สั่ง `make build SECURE_BOOT=yes` ดู error (ทำไม "ล้ม" จึงเป็นเรื่องดี) · วาดห่วงโซ่สองแบบ (บอร์ดตอนนี้ vs ผลิตภัณฑ์ที่เปิด secure boot ครบ) · อัปเดต threat model บทเรียน 1.1

---

## เช็กความเข้าใจ

1. ใน `proj_cm33_s/main.c` ของแม่แบบ CM33_S ทำอะไรก่อนเปิด CM33_NS
   - ก) ตรวจลายเซ็นของ CM33_NS ด้วย OPTIGA™ Trust M · ข) `cybsp_init()` แล้วอ่าน stack pointer และ reset handler จากตาราง vector แล้วกระโดดไป · ค) ถอดรหัส image ของ CM33_NS · ง) เชื่อมต่อ WiFi

2. build ด้วย `SECURE_BOOT=1` แล้ว flash ลงบอร์ดที่ **ยังไม่** provision `secure_boot=true` ผลคืออะไร
   - ก) บอร์ดไม่บูต · ข) Extended Boot ยังไม่ได้บังคับตรวจลายเซ็น การมีลายเซ็นจึงยังไม่ได้เพิ่มการป้องกัน · ค) ชิป OPTIGA ถูกล็อก · ง) LcsO เปลี่ยนเป็น operational

3. ข้อใดอธิบายความต่างของ secure boot กับการเข้ารหัสเฟิร์มแวร์ได้ถูก
   - ก) secure boot ซ่อนโค้ด การเข้ารหัสยืนยันว่าใครเขียน · ข) secure boot ยืนยันว่าโค้ดมาจากเจ้าของกุญแจและไม่ถูกแก้ การเข้ารหัสทำให้คนอื่นอ่านโค้ดไม่ได้ · ค) ทั้งสองอย่างเหมือนกัน · ง) secure boot ต้องใช้กุญแจลับบนอุปกรณ์

---

## ไปต่อ

secure boot ตอบเรื่องเฟิร์มแวร์ตอนเปิดเครื่อง แต่ข้อมูลบางอย่างในชิป เช่นใบรับรองของอุปกรณ์ ต้องเปลี่ยนได้ตลอดอายุการใช้งาน บทต่อไปดูว่า OPTIGA™ Trust M รับการเปลี่ยนแปลงนั้นอย่างไรโดยไม่เชื่อ host

บทเรียนถัดไป: [บทเรียน 4.2: Protected Update](../l02-protected-update/README.md)

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มาและเครดิต

"Secure IoT กับ OPTIGA™ Trust M" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

โค้ดและ config ที่ยกในสไลด์นี้จาก TESAIoT PSE84 Dev Kit SDK (Apache-2.0) — ลิงก์และสัญญาอนุญาตอยู่ใน README ของบทเรียน

TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY-NC 4.0
