---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 2.1 — รายละเอียดกล่อง วัสดุ PBR และภาพนำเสนอ"
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

# บทเรียน 2.1 — รายละเอียดกล่อง วัสดุ PBR และภาพนำเสนอ

## Apply Scale, Solidify, Boolean, Bevel และการแยกฝา/ฐาน วัสดุ Principled BSDF แสงสามจุด กล้อง และการเรนเดอร์

**โมดูล 2 — การขึ้นรูป วัสดุ และการเรนเดอร์**

หลักสูตร **การออกแบบผลิตภัณฑ์เชิงอุตสาหกรรม (Blender และ Digital Twin)** · ดัดแปลงจากงานของ ผศ.ดร.สันติ นุราช (KMUTT)

---

## เป้าหมาย

เมื่อเรียนจบบทเรียนนี้ คุณควรทำได้:

1. พัฒนารูปทรงที่ซับซ้อนขึ้นจาก block model (hard-surface / ช่องพอร์ต / ความหนาผนัง)
2. กำหนดวัสดุ พื้นผิว และรายละเอียดผิวในแนว **PBR**
3. จัดแสงและเรนเดอร์ภาพคุณภาพสูงสำหรับนำเสนอ

> **คาถาประจำบทเรียน**
> เพิ่มรายละเอียดโดย **ไม่ทำลายขนาดที่ล็อกไว้ในบทเรียน 1.1** — ช่องพอร์ตสวยแต่บอร์ดใส่ไม่ได้ = ยังไม่ผ่าน

---

## จาก Block สู่รายละเอียดผลิตภัณฑ์ (คงสเกลไว้)

จากบทเรียนที่แล้ว คุณมี `PCB_placeholder` ตามขนาดจริง และ `Enclosure_block` ที่หุ้มได้ ในบทเรียนนี้คุณจะ

1. ทำให้กล่องมี **ผนังหนา** (ไม่ใช่ก้อนตันอย่างเดียว)
2. **เจาะช่อง** พอร์ต / LED / เซ็นเซอร์ อย่างน้อย 2 จุด
3. **มนขอบ** ที่ผู้ใช้จับ
4. **แยกฝาบน–ฐาน** เป็น object คนละชิ้น
5. ใส่วัสดุ + แสง + เรนเดอร์ภาพนำเสนอ

```text
Block (ขนาดล็อกแล้ว) → Solidify → Boolean cutouts → Bevel edges
    → Split lid/base → Materials (Principled BSDF) → Lights + camera → Render PNG
```

อย่าเปลี่ยน Dimensions ของ PCB โดยไม่จดเหตุผล — ถ้าต้องขยายกล่อง ให้แก้ตามสูตร clearance ในบทเรียน 1.1 แล้วอัปเดต checklist

---

## ตัวอย่างสมบูรณ์ (1) — Solidify และ Boolean

**ท่าที่ 1 — Apply Scale ก่อนเสมอ** `Ctrl+A` → Scale บนวัตถุก่อน Boolean / Bevel / Solidify ทุกครั้ง ไม่งั้นขอบมนและรูเจาะมักเพี้ยน

**ท่าที่ 2 — Solidify (ความหนาผนัง)** ใส่ Solidify Modifier · Thickness ≈ **2.0 mm** · เปิด Even Thickness ถ้าผลดูสม่ำเสมอ · ตรวจว่า PCB ยังอยู่ภายในและไม่ชนผนัง

**ท่าที่ 3 — Boolean Difference (เจาะช่อง)** สร้าง Cube/Cylinder เป็น `Cutter_USB` ตามขนาดช่อง → วางทับผนังตรงตำแหน่งพอร์ต → Add Modifier → Boolean → Operation Difference → Object = cutter → Apply แล้วซ่อน/ลบ cutter ทำอย่างน้อย **2 ช่อง** (เช่น USB + เซ็นเซอร์หรือ LED)

---

## ตัวอย่างสมบูรณ์ (2) — Bevel และแยกฝา/ฐาน

**ท่าที่ 4 — Bevel ขอบมน** Edit Mode เลือกขอบ → `Ctrl+B` ลากเมาส์ (หรือ Bevel Modifier ทั้งชิ้น ระวังอย่ามนจนช่องพอร์ตเสียรูป) รัศมีเริ่มต้นในแล็บ ≈ **0.5–1.5 mm** ที่ขอบนอกที่มือจับ

**ท่าที่ 5 — แยกฝาและฐาน** ตั้งแต่บทเรียนนี้ให้แยกอย่างน้อย `Enclosure_base` (ฐาน/ตัวล่าง) และ `Enclosure_lid` (ฝาบน) วิธีง่าย: Edit Mode เลือกหน้าด้านบน → `P` → Selection เป็น object ใหม่ เหตุผล: บทเรียนโมดูล 3 จะหมุนฝา และโมดูล 6 จะพิมพ์แยกชิ้น

(ถ้าฝาหรือปุ่มสมมาตรซ้าย–ขวา ใช้ Mirror Modifier ลดงานซ้ำได้)

---

## วัสดุแบบ PBR ด้วย Principled BSDF

**PBR** (Physically Based Rendering) คือวัสดุที่ตอบสนองแสงใกล้ความจริงเมื่อเปลี่ยนมุมไฟ ใน Blender ใช้โหนด **Principled BSDF** (เข้ากันดีกับ glTF ตอน export ในโมดูล 4)

| พารามิเตอร์ | ความหมาย | คำแนะนำในแล็บ |
|---|---|---|
| **Base Color** | สีพื้น | พลาสติกตัวเครื่อง: เทาอ่อน / ขาวหม่น |
| **Roughness** | ด้าน ↔ เงา (0 = เงามาก, 1 = ด้าน) | พลาสติกด้าน ≈ 0.45–0.7 |
| **Metallic** | 0 = ไม่ใช่โลหะ, 1 = โลหะ | พลาสติก = 0 · โลหะปุ่ม/พอร์ต = 1 |
| **Emission** (ทางเลือก) | แสงออกจากผิว | LED จำลอง — ความเข้มต่ำพอ |

ต้องมีวัสดุอย่างน้อย **2 ชนิด** เช่น พลาสติกด้าน (Base Color ≈ 0.75,0.75,0.78 · Roughness 0.55 · Metallic 0) และวัสดุตัดกัน เช่น ยางขาตั้งหรือโลหะพอร์ต — จดค่าจริงใน look-dev sheet

---

## แสงและกล้องสำหรับภาพนำเสนอ

| Engine | ใช้เมื่อ |
|---|---|
| **EEVEE** | ดูผลเร็ว · แล็บส่วนใหญ่ |
| **Cycles** | ภาพนำเสนอสุดท้ายถ้าเครื่องไหว |

**แสงสามจุดเริ่มต้น** Key (ไฟหลักด้านหน้า-ข้าง) · Fill (ลดเงามืด อ่อนกว่าฝั่งตรงข้าม) · Rim/back (แยกวัตถุจากพื้นหลัง) หรือใช้ World HDRI เป็นแสงแวดล้อมแล้วเติม Area หนึ่งดวงเน้นขอบ พื้นหลังสีเทาอ่อนเรียบ อย่าให้ลายรบกวนการอ่านรูปทรง

**กล้อง** มุมแนะนำ three-quarter หรือ isometric-ish ที่เห็นฝา + พอร์ตด้านข้าง ถ่ายอย่างน้อย 1 ภาพ beauty (แนะนำเพิ่ม 1 ภาพ technical ที่เห็นช่องพอร์ตหรือ PCB ชัด)

---

## Render Output และเกณฑ์ก่อนไปโมดูล 3

Output Properties → Resolution เช่น 1920×1080 · File Format = PNG · `F12` แล้ว Image → Save As จดค่า engine, samples/คุณภาพ, ชื่อไฟล์ลง [material-lighting-sheet.md](resources/material-lighting-sheet.md)

| ตรวจ | ผ่านเมื่อ |
|---|---|
| สเกลจากบทเรียน 1.1 ยังใช้ได้ | PCB ยังใส่ได้ใน Wireframe |
| ช่องเปิด ≥ 2 | พอร์ต/เซ็นเซอร์/LED ชัด |
| ฝาและฐานแยก object | พร้อม animate ในโมดูล 3 |
| วัสดุ ≥ 2 | Principled BSDF · ค่าจดใน sheet |
| มีการเรนเดอร์อย่างน้อย 1 ภาพ | PNG ในโฟลเดอร์ผลงาน |

---

## เช็กความเข้าใจ / ไปต่อ

ตอบคำถามใน [quiz.yaml](quiz.yaml) — สามข้อ ผูกกับเป้าหมายของบทเรียนนี้ข้อละหนึ่งคำถาม ลองตอบเองก่อนแล้วค่อยเทียบกับเฉลยในไฟล์

## ฝึกเติม/แล็บ

ลงมือต่อที่ [แล็บ: ขัดเกลาโมเดล วัสดุ PBR และเรนเดอร์](../l02-lab/README.md) (~3.5–4 ชั่วโมง)

- เจาะช่องเปิด ≥ 2 จุด และแยกฝา/ฐานเป็นคนละ object โดย PCB ยังใส่ได้
- ใส่วัสดุ PBR ≥ 2 ชนิด และเรนเดอร์ PNG ≥ 1 ภาพ พร้อมกรอก [material-lighting-sheet.md](resources/material-lighting-sheet.md)

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มา

"การออกแบบผลิตภัณฑ์เชิงอุตสาหกรรม (Blender และ Digital Twin)" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY-NC 4.0 (ดัดแปลง)

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)

เครื่องมือ Bitstream Studio (VS Code) และ Ternion ที่หลักสูตรนี้ใช้ เป็นผลงานของ ผศ.ดร.สันติ นุราช (KMUTT)
