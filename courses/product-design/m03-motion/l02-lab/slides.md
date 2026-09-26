---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 3.2 — แล็บ: แอนิเมชันฝาและลำดับการเคลื่อนไหวสั้น"
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

# บทเรียน 3.2 — แล็บ: แอนิเมชันฝาและลำดับการเคลื่อนไหวสั้น

## ตั้งบานพับ keyframe คลิป `lid_open` สร้างคลิปปิด ตรวจการชน และบันทึกรายการคลิป

**โมดูล 3 — การเคลื่อนไหวและการโต้ตอบ** · Hands-on ~2.5–3 ชั่วโมง

หลักสูตร **การออกแบบผลิตภัณฑ์เชิงอุตสาหกรรม (Blender และ Digital Twin)** · ดัดแปลงจากงานของ ผศ.ดร.สันติ นุราช (KMUTT)

---

## เป้าหมายของแล็บ

- ตั้ง Origin ของฝาที่บานพับ
- สร้างแอนิเมชันเปิด/ปิดอย่างน้อย 1 ชุด
- ตรวจว่าชิ้นส่วนไม่ทะลุกันอย่างรุนแรงขณะเล่น
- ตั้งชื่อ Action/clip เป็นภาษาอังกฤษสั้น เช่น `lid_open`
- กรอก [animation-clip-list.md](../l01-motion-and-interaction/resources/animation-clip-list.md)

---

## ก่อนเริ่ม

- [ ] มีไฟล์จากบทเรียน 2.2 ที่แยก `Enclosure_lid` / `Enclosure_base` แล้ว
- [ ] คัดลอกเป็น `m03_enclosure_motion.blend` ก่อนแก้
- ถ้ายังไม่แยกฝา–ฐาน ให้กลับไปทำแล็บ C ในบทเรียน 2.2 ก่อน

---

## ฝึกเติม/แล็บ (1) — จุดหมุนของบานพับ

**ท่าที่ 1 — Hinge origin (บังคับ)**

1. เลือก `Enclosure_lid`
2. วาง 3D Cursor ที่ขอบบานพับ (Edit Mode → `Shift+S` → Cursor to Selected)
3. Object Mode → Origin to 3D Cursor
4. `Ctrl+A` → Rotation & Scale
5. ทดสอบหมุนด้วย `R` บนแกนที่ถูกต้อง — ต้องเปิดแบบบานพับ

**ผ่านเมื่อ:** เพื่อนในทีมหมุนฝาแล้วเข้าใจว่าบานพับอยู่ตรงไหนโดยไม่ต้องอธิบายยาว

---

## ฝึกเติม/แล็บ (2) — คีย์เฟรม `lid_open`

**ท่าที่ 2 — Keyframe `lid_open` (บังคับ)**

1. ตั้ง fps ของทีม (แนะนำ 24) และช่วงเฟรมประมาณ 1–3 วินาที
2. เฟรมต้น: ฝาปิด → `I` → Rotation
3. เฟรมปลาย: หมุนเปิด → `I` → Rotation
4. Play ใน Timeline ตรวจการเคลื่อนไหว
5. ตั้งชื่อ Action เป็น `lid_open` (หรือชื่อสื่อความหมายเทียบเท่า)

**ผ่านเมื่อ:** กด Play แล้วฝาเปิดจากปิดไปเปิดได้อย่างชัดเจน

---

## ฝึกเติม/แล็บ (3) — คลิปปิดและการตรวจการชน

**ท่าที่ 3 — Close clip (บังคับ)** เลือกอย่างใดอย่างหนึ่ง: Action แยกชื่อ `lid_close` หรือช่วงเฟรมต่อจากเปิดแล้วกลับไปท่าปิดในคลิปเดียวกัน (จดใน clip list ให้ชัด)

**ท่าที่ 4 — Interference check (บังคับ)**

1. เล่นแอนิเมชันช้า ๆ · สลับ Wireframe ตรวจจุดบานพับและชิ้นส่วนสูง
2. จดใน clip list: ผ่าน / มีชนเล็กน้อย / ต้องแก้รูปทรง
3. ถ้าชนรุนแรง: แก้ Origin มุมเปิด หรือกลับโมดูล 2

**ผ่านเมื่อ:** ไม่มีทะลุรุนแรง หรือมีบันทึกปัญหาพร้อมแผนแก้

---

## ฝึกเติม/แล็บ (4) — หลักฐานและ clip list

**ท่าที่ 5 — Evidence + clip list (บังคับ)**

1. กรอก [animation-clip-list.md](../l01-motion-and-interaction/resources/animation-clip-list.md) ครบทุกคลิป
2. บันทึกหลักฐาน: สกรีนช็อตเฟรมปิด+เปิด หรือ viewport playblast สั้น ๆ
3. Save `.blend`

(ทางเลือก) คลิป `battery_reveal` · ปรับ easing ด้วย Graph Editor · Parent ชิ้นส่วนเล็กติดกับฝา

---

## ผลงานที่ต้องส่ง

- [ ] `m03_enclosure_motion.blend`
- [ ] แอนิเมชันเปิด/ปิดที่ตั้งชื่อแล้ว
- [ ] บันทึกผลตรวจการชนแล้ว
- [ ] [animation-clip-list.md](../l01-motion-and-interaction/resources/animation-clip-list.md) กรอกครบ
- [ ] หลักฐานภาพหรือคลิปสั้น

---

## แก้ปัญหาที่พบบ่อย

| อาการ | ลองทำ |
|---|---|
| ฝาหมุนแล้วลอยทั้งก้อน | Origin ยังไม่อยู่ที่บานพับ — ทำท่าที่ 1 ใหม่ |
| หมุนผิดแกน | ใช้ `R` แล้ว `X`/`Y`/`Z` หรือหมุนใน Transform panel ทีละแกน |

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มา

"การออกแบบผลิตภัณฑ์เชิงอุตสาหกรรม (Blender และ Digital Twin)" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY 4.0 (ดัดแปลง)

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)

เครื่องมือ Bitstream Studio (VS Code) และ Ternion ที่หลักสูตรนี้ใช้ เป็นผลงานของ ผศ.ดร.สันติ นุราช (KMUTT)
