---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 1.2 — แล็บ: กล่องหุ้มแบบ block ตามสเกลฮาร์ดแวร์"
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
<!-- _backgroundColor: #0d1117 -->

# บทเรียน 1.2 — แล็บ: กล่องหุ้มแบบ block ตามสเกลฮาร์ดแวร์

## ตั้งฉากและหน่วย สร้าง PCB placeholder สร้าง enclosure block ที่มี clearance แล้วตั้งชื่อและบันทึกไฟล์

**โมดูล 1 — พื้นฐานการออกแบบเชิงอุตสาหกรรม** · Hands-on ~90–120 นาที

หลักสูตร **การออกแบบผลิตภัณฑ์เชิงอุตสาหกรรม (Blender และ Digital Twin)** · ดัดแปลงจากงานของ ผศ.ดร.สันติ นุราช (KMUTT)

---

## เป้าหมายของแล็บ

- ตั้งฉาก Blender เป็น **Metric + Millimeters** ตามสูตรทีม
- สร้าง **PCB placeholder** ตามขนาดที่วัดหรือขนาด Lab default
- สร้าง **enclosure block** ที่หุ้ม PCB ได้โดยมี clearance ตามบทเรียนที่แล้ว
- Apply Scale · ตั้งชื่อ object · บันทึก `.blend` + สกรีนช็อต
- กรอก [scale-and-block-checklist.md](../l01-industrial-design-fundamentals/resources/scale-and-block-checklist.md)

---

## ก่อนเริ่ม

- [ ] ติดตั้ง Blender (แนะนำสาย LTS)
- [ ] อ่านบทเรียน 1.1 ส่วน "ตัวอย่างสมบูรณ์" อย่างน้อยหนึ่งรอบ
- [ ] เตรียมโฟลเดอร์โปรเจกต์ เช่น `course3-m01-block/`
- [ ] (แนะนำ) เวอร์เนีย + บอร์ดจริงที่ใช้

---

## เลือกแหล่งที่มาของขนาด — สองแทร็ก

**แทร็ก A — วัดบอร์ดจริง (แนะนำ)** วัด กว้าง × ยาว × หนา ของ PCB และความสูงชิ้นส่วนสูงสุด แล้วจดแหล่งที่มาใน checklist

**แทร็ก B — Placeholder (ยังไม่มีบอร์ด)** ใช้ขนาดฝึกนี้แล้วเปลี่ยนเป็นของจริงภายหลังได้

| ชิ้นส่วน | X (mm) | Y (mm) | Z (mm) |
|---|---|---|---|
| `PCB_placeholder` | 80 | 55 | 1.6 |
| ช่องว่างเหนือชิ้นส่วนสูงสุด | — | — | 3.0 |
| Clearance (แต่ละด้าน) | 0.5 | 0.5 | — |
| ผนัง (แผนไว้) | 2.0 | 2.0 | 2.0 |

คำนวณ `Enclosure_block` outer ตามสูตรในบทเรียน 1.1 แล้วจดตัวเลขลง checklist **ก่อน** สร้างใน Blender

---

## ฝึกเติม/แล็บ (1) — ฉากใหม่และหน่วย

**ท่าที่ 1 — ตั้งฉากและหน่วย (บังคับ)**

1. `File → New → General`
2. Scene Properties → Units: Unit System = Metric · Length = Millimeters · Unit Scale = 0.001
3. บันทึกไฟล์ `m01_block_enclosure.blend`
4. จด Blender version ใน checklist (`Help → About` / splash)

**ผ่านเมื่อ:** เปลี่ยน Dimensions ของ Cube แล้วเห็นหน่วยเป็น mm บน UI

---

## ฝึกเติม/แล็บ (2) — PCB placeholder

**ท่าที่ 2 — สร้าง PCB placeholder (บังคับ)**

1. Add Cube → ตั้งชื่อ `PCB_placeholder`
2. ตั้ง Dimensions ตามแทร็ก A หรือ B
3. `Object → Set Origin → Origin to Geometry`
4. `Ctrl+A` → Scale (ต้องเป็น 1,1,1)
5. จัด Location ให้อยู่เหนือ World Origin พอมองเห็น
6. (แนะนำ) เปิด Overlay → Measurements ใน Edit Mode แล้วสุ่มวัดขอบหนึ่งด้านให้ตรงตาราง

**ผ่านเมื่อ:** Dimensions ตรงตาราง และ Scale = 1,1,1

---

## ฝึกเติม/แล็บ (3) — enclosure block และการตรวจชน

**ท่าที่ 3 — Enclosure block + fit check (บังคับ)**

1. คำนวณ outer size (จดใน checklist)
2. Add Cube → ตั้งชื่อ `Enclosure_block`
3. ตั้ง Dimensions · Origin to Geometry · Apply Scale
4. จัดตำแหน่งให้ PCB อยู่ภายใน
5. สลับ Wireframe ตรวจจากมุม Top / Front / Right
6. ยืนยัน: PCB ไม่โผล่ผนัง · มีช่องว่างคร่าว ๆ ตาม clearance

**ผ่านเมื่อ:** สกรีนช็อต isometric เห็นทั้งสองชิ้น และเพื่อนในทีมอ่าน Dimensions ได้จาก checklist

---

## ฝึกเติม/แล็บ (4) — ตั้งชื่อ สี บันทึกไฟล์

**ท่าที่ 4 — Naming, colors, save (บังคับ)**

1. ตั้ง viewport color หรือ material ชั่วคราวคนละสีระหว่าง PCB / Enclosure
2. `File → Save`
3. Export สกรีนช็อต (หรือ Render Viewport) ชื่อ `m01_block_iso.png`
4. กรอก checklist ให้ครบ

**ทางเลือกเพิ่มเติม (ไม่บังคับ):** เพิ่ม `Battery_block` หรือ `Display_block` ตาม datasheet · เขียนโน้ต concept 4 ข้อจากบทเรียน 1.1

---

## ผลงานที่ต้องส่ง

- [ ] `m01_block_enclosure.blend`
- [ ] สกรีนช็อต isometric
- [ ] [scale-and-block-checklist.md](../l01-industrial-design-fundamentals/resources/scale-and-block-checklist.md) กรอกครบ
- [ ] (ถ้ามีบอร์ด) แหล่งขนาด = วัดจริง และ/หรือเอกสาร kit

## แก้ปัญหาที่พบบ่อย

| อาการ | ลองทำ |
|---|---|
| กริดหาย / วัตถุเล็กจนมองไม่เห็น | ตรวจ Unit Scale = 0.001 · ซูม · ปรับ Grid overlay |
| พิมพ์ 80 แล้วได้ยักษ์หรือจิ๋ว | ทีมใช้สูตรหน่วยไม่ตรงกัน — รีเซ็ตตามท่าที่ 1 |
| Bevel / ปรับขนาดเพี้ยนภายหลัง | ลืม Apply Scale — ทำ `Ctrl+A` → Scale |

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มา

"การออกแบบผลิตภัณฑ์เชิงอุตสาหกรรม (Blender และ Digital Twin)" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY 4.0 (ดัดแปลง)

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)

เครื่องมือ Bitstream Studio (VS Code) และ Ternion ที่หลักสูตรนี้ใช้ เป็นผลงานของ ผศ.ดร.สันติ นุราช (KMUTT)
