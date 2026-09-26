---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 2.1 — ชุดเครื่องมือและการ build ครั้งแรก"
footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY 4.0"
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

# บทเรียน 2.1 — ชุดเครื่องมือและการ build ครั้งแรก

## ติดตั้ง ModusToolbox ตรวจความพร้อม ดึง dependency แล้ว build และแฟลชแม่แบบเฟิร์มแวร์ของ SDK

**โมดูล 2 — Build ด้วย ModusToolbox และ Make และ Git สำหรับเฟิร์มแวร์**

หลักสูตร **พื้นฐานเฟิร์มแวร์ภาษา C บน PSoC Edge**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. รันขั้นตอนตรวจความพร้อม ดึง dependency ของทุกโปรเจกต์ build และแฟลชแม่แบบเฟิร์มแวร์ได้สำเร็จ
2. อธิบายว่าคอร์ CM33_S, CM33_NS และ CM55 แต่ละคอร์รันอะไรในแม่แบบนี้
3. บันทึกเวอร์ชันของเครื่องมือและ commit ของ SDK ที่ใช้ build เพื่อให้ผู้อื่นทำซ้ำได้

ใช้เวลาประมาณ 70 นาที ไม่รวมดาวน์โหลด dependency ราว 1.9 GB — แนะนำให้เริ่มดาวน์โหลดตั้งแต่ต้นบทแล้วอ่านแนวคิดระหว่างรอ

---

## ก่อนเริ่ม

ทวนจากโมดูล 1 สองข้อ

1. ค่าเริ่มต้นของตัวแปร `.data` อยู่ที่ไหนตอนบอร์ดยังไม่เปิด และใครคัดลอกมันไปไว้ใน RAM
2. flash ภายนอกของบอร์ดแบ่งพื้นที่ให้ image ของ CM33 secure, CM33 non-secure และ CM55 แยกกัน คุณคิดว่าทำไมต้องแยกเป็นสาม image

**สิ่งที่ต้องมี:** ModusToolbox™ 3.6 พร้อม Arm GCC 14.2.1 · Git และ bash 4 ขึ้นไป · พื้นที่ว่างราว 4 GB · บอร์ด TESAIoT Dev Kit กับสาย USB-C เข้า KitProg3

---

## ดูของจริงก่อน

แม่แบบที่ build ได้มาเป็นไฟล์ **zip ใน release** ของ SDK ไม่ใช่ `git clone` เพราะ repository สาธารณะไม่ได้เก็บไลบรารี prebuilt (`.a`) หกตัวไว้ — ไลบรารีเหล่านั้นมากับ zip

ดาวน์โหลดสามไฟล์จาก [release fw-c-only-v1.10.0](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/releases/tag/fw-c-only-v1.10.0) แล้วรัน

```sh
shasum -a 256 -c SHA256SUMS.txt
unzip bento-firmware-template-mtb-only.zip
cd bento-firmware-template-mtb-only
./setup.sh --check
```

**ทายก่อนรัน**: บรรทัดไหนจะขึ้น `FAIL`/`warn` ในเครื่องใหม่ — ส่วนใหญ่จะเห็น `variant: mtb-only`, บรรทัดของ compiler และ `mtb_shared not found` ตามด้วยขนาดราว 1.9 GB

---

## แนวคิด (1) — แม่แบบนี้คือสามโปรเจกต์ บนสามคอร์

| โปรเจกต์ | คอร์ | รันอะไร (variant mtb-only) |
|---|---|---|
| `proj_cm33_s` | M33 secure | secure boot, TrustZone — "you will not touch this" |
| `proj_cm33_ns` | M33 non-secure | FreeRTOS, WiFi, เซนเซอร์ I2C, คลาวด์, **UART console ตัวเดียว** |
| `proj_cm55` | M55 (มี NPU) | จอ LVGL, ทุกหน้า UI, Edge AI, เรดาร์ |

ลำดับบูต: extended boot ปล่อย CM33 secure ก่อน → ตั้งค่าการป้องกันแล้วปล่อย CM33 non-secure → CM33 non-secure เปิด CM55 ทั้งสาม image รันจาก flash QSPI แบบ execute in place ผลของ build คือไฟล์ `app_combined.hex` ไฟล์เดียว

> ข้อควรจำ: **CM55 ไม่มี console** `printf` บน CM55 ไม่ออกไปไหน ข้อความทุกอย่างออกทาง CM33_NS

---

## แนวคิด (2) — dependency ต้องดึงแยกทีละโปรเจกต์ แล้วแพตช์

`make getlibs` ดึงไลบรารีแต่ละโปรเจกต์ไว้ใน `mtb_shared` แม่แบบนี้ **ไม่มี getlibs ระดับบนสุด** ต้องรันในทั้งสามโปรเจกต์ — ถ้ารันแค่ `proj_cm33_ns` จะได้ 33 จาก 41 asset แล้ว build หยุดเพราะหาไฟล์ optiga-trust-m ไม่เจอ

หลังดึงเสร็จต้องใส่แพตช์ด้วย `patch -F0` แล้วตรวจด้วย SHA-256 — ทำไมต้อง `-F0`: ค่าเริ่มต้นของ GNU patch ยอมให้บริบทคลาดเคลื่อนได้แล้วยังคืนค่าสำเร็จ และแพตช์ 10 ใน 11 ตัว **"fail silently"** เมื่อหายไป (เช่น mTLS ถอยไปใช้กุญแจซอฟต์แวร์ แล้ว broker ปฏิเสธอุปกรณ์)

> exit status บอกว่าแพตช์ลงไปที่ไหนสักที่ ส่วน digest บอกว่ามันลงถูกที่

---

## แนวคิด (3) — build ที่ทำซ้ำได้ เริ่มจากรุ่นที่ตรึงไว้

README ของ SDK ตรึง ModusToolbox ไว้ที่ 3.6 — Configurator รุ่นใหม่กว่าจะสร้างการตั้งค่า BSP ใหม่จาก `design.modus` แล้วออก notice ที่กลายเป็น error ในไฟล์ที่ไม่เคยแตะ รุ่นใหม่กว่าจึงไม่ได้ดีกว่าเสมอไป

"ซอร์สที่อ่าน" (commit ใน git) กับ "แพ็กเกจที่ build" (zip ของ release) เป็นคนละชิ้น — บันทึกให้ครบทั้งสองชิ้นเสมอ

**build ที่ทำซ้ำได้ต้องตอบสามคำถาม:** ใช้เครื่องมือรุ่นอะไร · ใช้ซอร์สที่ commit ไหน · มีอะไรที่แก้แต่ยังไม่ commit — บวกหลักฐานผลลัพธ์ เช่นขนาดและ SHA-256 ของ `app_combined.hex`

---

## ตัวอย่างสมบูรณ์ — ท่าที่ 1/2 ตรวจเครื่อง แล้วดึงและแพตช์

```sh
# ท่าที่ 1: ตรวจสิ่งที่ได้รับ และตรวจเครื่อง
(cd lib && ./verify.sh)      # ลายเซ็นและ digest ของไลบรารี prebuilt
./bento.sh doctor            # toolchain และสิ่งที่แม่แบบไม่ได้แนบมา

# ท่าที่ 2: ดึง dependency ทีละโปรเจกต์ แล้วแพตช์
for p in proj_cm33_s proj_cm33_ns proj_cm55; do (cd $p && make getlibs); done
```

ถ้า `verify.sh` ไม่ผ่าน ให้หยุด — แพ็กเกจที่ได้มาไม่ใช่ตัวที่ถูกเซ็นไว้ หรือกำลังรันใน clone ของ git ที่ไม่มีไฟล์ `.a`

---

## ตัวอย่างสมบูรณ์ — ท่าที่ 3 build flash แล้วดูหลักฐาน

```sh
make build -j                # build ครั้งแรกของทั้งสามคอร์ใช้เวลาราวสิบนาที
make program                 # เขียนผ่าน KitProg3
```

แล้ว **ถอดสาย USB ให้สุด รอสักครู่ แล้วเสียบใหม่** เปิด serial console ที่ 115200 8N1 ไว้ก่อนเสียบ หลักฐานว่าบูตสำเร็จคือบรรทัด `[HB] t=...s tasks=...` ทุกสิบวินาที และป้ายรุ่นบนหน้าจอ Home ที่ลงท้ายด้วย `-mtb_only`

**กับดักที่พบในวันแรก:** #21 จอดำหลัง flash (ถอดสายเสียบใหม่ทุกครั้ง) · #22 บูตเย็นอาจต้องเสียบรอบที่สอง · #16 อย่า attach debugger กับบอร์ดที่กำลังทำงาน · อย่าเรียก `openocd` ตรง ๆ ใช้ `make program` เท่านั้น

---

## ฝึกเติม

บทนี้ฝึกกับเครื่องมือ ไม่ใช่กับโค้ด — ตอบคำถามโดยอ่านจากเครื่องของคุณและจากไฟล์ใน SDK ไม่ใช่จากความจำ

1. `./setup.sh --check` ตรวจอะไรบ้าง และตรวจอะไร **ไม่** ได้ (มันแตะแพตช์หรือไม่)
2. หลัง getlibs นับจำนวนโฟลเดอร์ระดับแรกใน `../mtb_shared` ได้เท่าไร
3. ใน `third_party_patches/series` มีแพตช์กี่ไฟล์ และตัวไหนที่ README บอกว่าเป็นตัวเดียวที่ทำให้ build หยุด
4. เปิด [resources/build-record.md](resources/build-record.md) แล้วเติมส่วน "เครื่องและเครื่องมือ" กับ "ซอร์สที่ build" ให้ครบ

ลองเองก่อนอย่างน้อย 15 นาทีก่อนเทียบกับคำตอบในบทเต็ม

---

## เช็กความเข้าใจ

ตอบคำถาม 5 ข้อใน [quiz.yaml](quiz.yaml) ครอบคลุมเป้าหมายทั้งสามข้อ (ตอบถูกตั้งแต่ 4 ข้อขึ้นไปถือว่าจบบทเรียน)

1. เรียงขั้นตอนตั้งแต่ clone จนเห็นว่าบอร์ดทำงาน สำหรับแม่แบบ mtb-only
2. ผู้เรียนรัน `make getlibs` เฉพาะใน `proj_cm33_ns` แล้ว build อาการที่ README ของแม่แบบบอกไว้คืออะไร
3. ในแม่แบบ mtb-only คอร์ใดเป็นเจ้าของ UART console ตัวเดียวของบอร์ด และคอร์ใดวาดหน้าจอ
4. ข้อใดอธิบายลำดับการเริ่มทำงานของสามคอร์ได้ถูกต้อง
5. เพื่อนต้อง build เฟิร์มแวร์ตัวเดียวกับคุณในเดือนหน้า ข้อมูลใดต้องอยู่ในบันทึกการ build (เลือกได้หลายข้อ)

---

## แล็บ

**งาน:** build และ flash แม่แบบ mtb-only ครั้งแรก แล้วเขียนบันทึกการ build ที่เพื่อนทำซ้ำได้

1. ทำตามสามท่าในหัวข้อตัวอย่างสมบูรณ์จนเห็นบรรทัด `[HB]` อย่างน้อยสองบรรทัด
2. ตรวจว่าตัวเลข `t=` เพิ่มทีละ 10 และจำนวน task คงที่หลังบูตเสร็จ
3. เติม [resources/build-record.md](resources/build-record.md) ให้ครบทุกช่อง รวม SHA-256 ของ `build/app_combined.hex`
4. ให้เพื่อนหนึ่งคน build จากบันทึกของคุณบนเครื่องของเขา แล้วเทียบ SHA-256 ถ้าไม่ตรงกัน ให้หาว่าต่างกันตรงไหนก่อนสรุปว่าอะไรผิด

**หลักฐานที่เก็บไว้ใน portfolio:** log ของ getlibs และการตรวจแพตช์ (บรรทัด `OK`) บรรทัด `[HB]` จาก console ภาพหน้าจอ Home และไฟล์ build record ที่เติมครบ

---

## ไปต่อ

- เปิด [A0 — What you can build, and where each piece lives](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__a0__orientation.html) หาว่าไลบรารี prebuilt ตัวไหนลิงก์เข้าคอร์ไหน ตรงกับตารางในแนวคิดข้อ 1 หรือไม่
- เทียบกับ [mtb-example-psoc-edge-hello-world @ release-v2.1.0](https://github.com/Infineon/mtb-example-psoc-edge-hello-world/tree/release-v2.1.0) ของ Infineon ซึ่งทดสอบกับ ModusToolbox 3.7 — ถ้าจะใช้ทั้งสองรุ่นในเครื่องเดียว ต้องจัดการเรื่องรุ่นอย่างไร

บทถัดไป: [บทเรียน 2.2 — Make และตัวแปรของการ build](../l02-make-and-build-flags/README.md)

---

## แหล่งที่มาและเครดิต

"พื้นฐานเฟิร์มแวร์ภาษา C บน PSoC Edge" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY 4.0

บทเรียนนี้อ้างอิง SDK ที่ commit `ef72c1b` และ release `fw-c-only-v1.10.0`
(Apache-2.0, tesaiot-pse84-devkit-sdk) — ไม่มีการคัดลอกไฟล์ของ SDK มาไว้ในหลักสูตรนี้
