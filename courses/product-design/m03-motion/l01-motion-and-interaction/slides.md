---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 3.1 — แอนิเมชันเปิด–ปิดและการตรวจการชน"
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

# บทเรียน 3.1 — แอนิเมชันเปิด–ปิดและการตรวจการชน

## เตรียม pivot ของฝา keyframe เปิด–ปิด ตั้งชื่อ Action ตรวจการชนขณะเล่น และเตรียมคลิปสำหรับ Twin

**โมดูล 3 — การเคลื่อนไหวและการโต้ตอบ**

หลักสูตร **การออกแบบผลิตภัณฑ์เชิงอุตสาหกรรม (Blender และ Digital Twin)** · ดัดแปลงจากงานของ ผศ.ดร.สันติ นุราช (KMUTT)

---

## เป้าหมาย

เมื่อเรียนจบบทเรียนนี้ คุณควรทำได้:

1. สร้างภาพเคลื่อนไหวสำหรับเปิด–ปิดชิ้นส่วนหรือแสดงโครงสร้างภายใน
2. จำลองการเคลื่อนไหวเพื่อประเมินความเหมาะสมในการใช้งาน (ชิ้นส่วนไม่ทะลุกัน)
3. สร้างชุดลำดับการเคลื่อนไหว (**named clips / actions**) สำหรับ Twin หรือสื่อการสอน

> **คาถาประจำบทเรียน**
> Animation คือ **เครื่องมือตรวจกลไก** ไม่ใช่แค่ทำให้ดูสวย — ถ้าฝาเปิดแล้วทะลุฐาน แสดงว่าดีไซน์ยังไม่พร้อมพิมพ์

บทเรียนนี้ต่างจากโมดูล 3 ของหลักสูตรอื่นในชุด: ที่นี่คือ **animation ของผลิตภัณฑ์ใน Blender** (เปิดฝา / หมุนชิ้นส่วน / คลิปสั้น) ไม่ใช่ script ของอุปกรณ์เสมือน

---

## ทำไมต้องมีภาพเคลื่อนไหว

| คำถาม | สิ่งที่การเคลื่อนไหวช่วยตอบ |
|---|---|
| เปิดฝาแล้วมือหรือสายชนไหม | เส้นทางหมุนของฝา |
| ช่องภายในพอใส่ PCB / แบตเตอรี่ไหม | เปิดฝาแล้วเห็นช่องว่าง |
| ผู้ใช้เข้าใจวิธีเปิดอย่างไร | คลิปสั้นสำหรับสื่อการสอน |
| Twin จะเล่นสถานะอะไรได้บ้าง | ชื่อคลิป เช่น `lid_open` |

ในระยะแรกของคอร์สนี้ **ใช้คีย์เฟรมของ Location / Rotation เป็นหลัก** ส่วนใหญ่ฝากล่องหมุนรอบขอบด้านหลังก็พอ ยังไม่ต้องใช้ armature (กระดูก)

---

## เตรียม pivot ของฝาก่อนใส่คีย์เฟรม

จากบทเรียนก่อนหน้าคุณควรมี `Enclosure_lid` และ `Enclosure_base` แยกกันแล้ว

**วางจุดหมุน (origin) ที่บานพับ**

1. เลือก `Enclosure_lid` → Edit Mode → เลือกขอบหรือจุดที่จะเป็นบานพับ (มักเป็นขอบหลังด้านใน)
2. `Shift+S` → Cursor to Selected
3. Object Mode → `Object → Set Origin → Origin to 3D Cursor`
4. ทดสอบ: กด `R` แล้วหมุนรอบแกนที่ถูกต้อง (มักเป็น X หรือ Y) — ฝาควรเปิดเหมือนบานพับ ไม่ลอยไปทั้งก้อน

ก่อนใส่คีย์เฟรม: `Ctrl+A` → **Rotation & Scale** บนฝา (และฐานถ้าจำเป็น)

---

## ตัวอย่างสมบูรณ์ (1) — คีย์เฟรมเปิด/ปิด

**ท่าที่ 1 — ตั้ง fps และช่วงเวลา** เฟรมเรต 24 fps (หรือ 30 fps ทีมเดียวกัน) · ความยาวคลิป 1–3 วินาที เช่น `lid_open` ที่ 24 fps ยาว 1.5 วินาที ≈ เฟรม 1 → 36

**ท่าที่ 2 — ใส่คีย์เปิด/ปิด** ไปเฟรม 1 (ฝาปิด) → เลือก `Enclosure_lid` → กด `I` เลือก Rotation → ไปเฟรมปลายคลิป → หมุนฝาเปิดในมุมใช้งานจริง (เช่น 90–110°) → กด `I` → Rotation อีกครั้ง → กด Space เล่นตรวจ

**ท่าที่ 3 — คลิปปิด (ทางเลือก)** สร้างคลิปปิดแยก หรือช่วงเฟรมถัดไปที่กลับสู่ท่าปิด — สำหรับ Twin มักแยกชื่อชัดกว่า: `lid_open` และ `lid_close`

---

## ตัวอย่างสมบูรณ์ (2) — ตั้งชื่อ Action

Animation ถูกเก็บใน **Action** เปิด Dope Sheet → โหมด Action แล้วตั้งชื่อเป็นภาษาอังกฤษสั้น เช่น `lid_open`

| ชื่อที่ดี | เลี่ยง |
|---|---|
| `lid_open` | `Anim1`, `asdf`, `เปิดฝา` |
| `lid_close` | `final_final2` |
| `battery_reveal` | ชื่อยาวมีช่องว่างเยอะ |

หลีกเลี่ยงชื่อว่าง ชื่อซ้ำ หรือภาษาไทยในชื่อไฟล์คลิปที่จะส่ง Twin — จดทุกคลิปใน [animation-clip-list.md](resources/animation-clip-list.md)

---

## ตรวจการชนขณะเล่นแอนิเมชัน

เล่นแอนิเมชันช้า ๆ แล้วตรวจ

| ตรวจ | ผ่านเมื่อ |
|---|---|
| ฝากับฐาน | ไม่ทะลุกันรุนแรงตรงบานพับ |
| ฝากับชิ้นส่วนสูง | ไม่ชนหัว USB / เซ็นเซอร์ / จอ |
| ช่องมือ/สาย (แนวคิด) | มีช่องให้จินตนาการมือเปิดได้ |
| มุมสุดขั้ว | มุมเปิดไม่เกินที่กลไกจริงทำได้ |

ถ้าชน: เลื่อนบานพับ (Origin) · ลดมุมเปิด · หรือกลับไปแก้รูปทรงในโมดูล 2 ไม่จำเป็นต้องเปิด Physics simulation — ดูด้วยตา + Wireframe ก็พอสำหรับบทเรียนนี้

> **คาถาประจำบทเรียน** Motion ที่ชน = บั๊กดีไซน์ที่จับได้ถูกกว่าตอนพิมพ์แล้วค่อยรู้

---

## คลิปสั้นสำหรับ Twin และสื่อการสอน

| แนวทาง | ทำไม |
|---|---|
| 1–3 วินาทีต่อคลิป | จัดการง่าย · export เบา · ผู้ชมเข้าใจจุดเดียว |
| หนึ่งคลิป = หนึ่งเจตนา | `lid_open` ไม่ปนการหมุนกล้องยาว |
| ชื่อคงที่ทั้งทีม | โมดูล 4 / Bitstream Studio อ้างชื่อเดียวกัน |

แอนิเมชันที่ export ได้ดีคือ keyframe ของ transform ถ้ามีหลาย Action ที่จะส่งออก มักต้อง **Stash** ลง NLA ตามโหมด export (รายละเอียดปุ่ม export อยู่ในบทเรียน 4.1) บันทึกหลักฐานสั้น ๆ ได้ด้วย Viewport Render Animation หรือบันทึกหน้าจอขณะกด Play

---

## เช็กความเข้าใจ / ไปต่อ

ตอบคำถามใน [quiz.yaml](quiz.yaml) — สามข้อ ผูกกับเป้าหมายของบทเรียนนี้ข้อละหนึ่งคำถาม ลองตอบเองก่อนแล้วค่อยเทียบกับเฉลยในไฟล์

## ฝึกเติม/แล็บ

ลงมือต่อที่ [แล็บ: แอนิเมชันฝาและลำดับการเคลื่อนไหวสั้น](../l02-lab/README.md) (~2.5–3 ชั่วโมง)

- ตั้ง Origin ของฝาที่บานพับ และสร้างแอนิเมชันเปิด/ปิดอย่างน้อย 1 ชุด
- ตรวจว่าชิ้นส่วนไม่ทะลุกันอย่างรุนแรงขณะเล่น แล้วกรอก [animation-clip-list.md](resources/animation-clip-list.md)

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มา

"การออกแบบผลิตภัณฑ์เชิงอุตสาหกรรม (Blender และ Digital Twin)" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY-NC 4.0 (ดัดแปลง)

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)

เครื่องมือ Bitstream Studio (VS Code) และ Ternion ที่หลักสูตรนี้ใช้ เป็นผลงานของ ผศ.ดร.สันติ นุราช (KMUTT)
