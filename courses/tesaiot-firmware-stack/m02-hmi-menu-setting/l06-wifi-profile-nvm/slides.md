---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 2.6 — เก็บโปรไฟล์ Wi-Fi ลงหน่วยความจำถาวร"
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

# บทเรียน 2.6 — เก็บโปรไฟล์ Wi-Fi ลงหน่วยความจำถาวร

## เก็บ SSID + password ลง non-volatile memory — form กรอก profile ผ่าน lv_textarea (password mode) และ save/load ผ่าน profile store

**TESAIoT Dev Kit · PSoC Edge E84 · ภาษา C · ModusToolbox**

---

# เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. สร้างฟอร์มกรอก SSID และรหัสผ่าน โดยช่องรหัสผ่านอยู่ใน password mode
2. บันทึก โหลด และล้างโปรไฟล์ผ่าน profile store ใน NVM ได้ และค่ายังอยู่หลังรีเซ็ตบอร์ด
3. อธิบายความเสี่ยงของการเก็บรหัสผ่านใน flash และแนวทางลดความเสี่ยง

---

# ก่อนเริ่ม

- ผ่านบทเรียนก่อนหน้ามาแล้ว: `fw-stack.m02.l05`
- บอร์ด: TESAIoT Dev Kit
- แพลตฟอร์ม: PSoC Edge E84 · ModusToolbox
- เวลาโดยประมาณ: เนื้อหา 15 + ฝึกตาม 25 + แล็บ 20 + เช็กความเข้าใจ 5 = 65 นาที

---

# ดูของจริงก่อน

![หน้าจอของ EP06 — WiFi Profile NVM บน TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm/hmi_ep06_wifi_profile_nvm.png)

ก่อนอ่านโค้ด ให้ทายว่าหน้าจอนี้มี object อะไรบ้าง และอะไรเปลี่ยนเมื่อผู้ใช้แตะหรือเมื่อค่าเซนเซอร์เปลี่ยน

---

# แนวคิด — หน่วยเก็บจริงคือ RRAM

README ต้นทางพูดกว้าง ๆ ว่าใช้ `cyhal_flash_*`/`cy_em_eeprom`/MCUboot NVS

**โค้ดจริง** เรียก `Cy_RRAM_TSReadByteArray()` / `Cy_RRAM_NvmWriteByteArray()` ตรง ๆ กับ `RRAMC0`

RRAM = Resistive RAM บนชิป PSoC Edge E84 เอง เขียนที่ `CYMEM_CM55_0_user_nvm_C_START`

---

# แนวคิด — record 256 ไบต์ พร้อม magic + CRC32

`wifi_profile_record_t`: `magic` (`0x57465031` = "WFP1" ไม่ใช่ "WIFI"), `version`, `crc32`, `valid` + payload

พอดีใน `WIFI_PROFILE_SLOT_SIZE = 256` ไบต์ (ตรวจด้วย compile-time assertion)

struct สาธารณะ `wifi_profile_data_t` มีแค่ ssid/password/security/auto_connect — **ไม่มี magic**

---

# แนวคิด — เขียนแล้วต้องอ่านกลับมาตรวจ

- เทียบ block เดิมก่อน ถ้าเหมือนกันข้ามการเขียน (`SAVE_SKIP_SAME`, ลด wear)
- เขียนแล้วอ่านกลับมาเทียบไบต์ต่อไบต์ (`SAVE_VERIFY_FAIL` ถ้าไม่ตรง)
- slot ที่ไม่เคยเขียนคือ `0xFF` ทั้งก้อน — เช็คก่อนเสมอ ไม่งั้นตีความขยะเป็นโปรไฟล์

---

# แนวคิด — auto-fill ต้องกดปุ่ม ไม่ใช่แค่แตะแถว

README ต้นทาง: แตะแถวใน scan list → auto-jump ไปหน้า profile ทันที

**โค้ดจริง**: แตะแถวก่อน (เลือก) → ต้องกดปุ่ม **"Use this AP"** แยกอีกขั้น

หน้า scan กับ profile เชื่อมกันผ่าน callback ที่ registered ไว้ ไม่ใช่ global state `pending_ssid`

---

# แนวคิด — ทักษะที่ฝึกในบทเรียนนี้

บทเรียนนี้พัฒนาทักษะต่อไปนี้ (ตามระดับ 1–5 ของหลักสูตร)

- `sys.memory-fs` (ระดับ 2)
- `gui.hmi` (ระดับ 2)
- `sec.fundamentals` (ระดับ 1)

---

# ตัวอย่างสมบูรณ์ — เขียน RRAM พร้อม verify

โค้ดจาก tesaiot/developer-hub (Apache-2.0) · commit `9a8e3ed` · [`wifi_profile_store.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm/wifi_profile/wifi_profile_store.c)

```c
/* Skip write if content is unchanged to reduce NVM wear. */
if(wifi_profile_read_slot(WIFI_PROFILE_PRIMARY_ADDR, current_block)) {
    if(0 == memcmp(current_block, block, sizeof(block))) {
        return true;   /* SAVE_SKIP_SAME */
    }
}

if(!wifi_profile_write_slot(WIFI_PROFILE_PRIMARY_ADDR, block)) {
    return false;
}
if(!wifi_profile_read_slot(WIFI_PROFILE_PRIMARY_ADDR, verify_block)) {
    return false;
}
if(0 != memcmp(verify_block, block, sizeof(block))) {
    return false;   /* SAVE_VERIFY_FAIL */
}
```

---

# ตัวอย่างสมบูรณ์ — ต้องเลือกแถวก่อนกด Use

[`ui_wifi_list_page.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm/wifi_list/ui_wifi_list_page.c)

```c
static void ui_wifi_use_selected_ap_cb(lv_event_t *e)
{
    uint16_t count;
    const wifi_scan_ap_t *aps =
        wifi_scan_service_get_list(&s_ctx.service, &count);

    if((aps == NULL) || (count == 0U) ||
       (s_ctx.selected_idx >= count)) {
        lv_label_set_text(s_ctx.hint_label,
            "Select an AP row before using it.");
        return;
    }

    s_use_ap_cb(&aps[s_ctx.selected_idx], s_use_ap_user_data);
}
```

---

# จุดที่มักพลาด

- คิดว่าใช้ generic flash API — โค้ดจริงใช้ RRAM API ตรง ๆ
- ไม่เช็คว่า slot เป็น `0xFF` (erased) ก่อน parse เป็น record
- เขียนแล้วไม่อ่านกลับมาตรวจ — ข้ามขั้น verify-after-write
- คิดว่าแตะแถวจะ auto-jump — จริงต้องกดปุ่ม Use แยกอีกขั้น

---

# ตัวอย่างสมบูรณ์ — build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

หรือเปิด [ตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep06_wifi_profile_nvm&q=hmi_ep06_wifi_profile_nvm) แล้ว flash เฟิร์มแวร์สำเร็จรูป

---

# ฝึกเติม / แล็บ

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

---

# เช็กความเข้าใจ

- ข้อมูลใน NVM ต่างจากตัวแปรใน RAM อย่างไรเมื่อบอร์ดรีเซ็ต
- ทำไมช่องรหัสผ่านต้องซ่อนตัวอักษร
- ถ้าต้องการลบโปรไฟล์ทั้งหมด ต้องเรียกฟังก์ชันใดของ profile store

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

---

# ไปต่อ

- ทบทวนเป้าหมายทั้ง 3 ข้อของบทเรียนนี้ก่อนไปต่อ
- ถ้าตอบคำถามหน้าที่แล้วไม่ได้ครบ กลับไปอ่าน README ของตัวอย่างส่วน Why / What / How อีกครั้ง
- พร้อมแล้วไปเปิดบทเรียนถัดไปในโมดูลเดียวกัน

---

# แหล่งอ้างอิง

- [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm) · commit `9a8e3ed`
- [เปิดตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep06_wifi_profile_nvm&q=hmi_ep06_wifi_profile_nvm)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้

---

# เครดิต

> "TESAIoT Firmware Stack: เฟิร์มแวร์ภาษา C บน TESAIoT Dev Kit" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย (Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY-NC 4.0

ตัวอย่างโค้ดเป็นผลงานของ TESAIoT Firmware Stack โดยสมาคมสมองกลฝังตัวไทย (TESA) ใน [tesaiot/developer-hub](https://github.com/tesaiot/developer-hub) รายละเอียดการให้เครดิตอยู่ที่ [ATTRIBUTION.md](../../../../ATTRIBUTION.md)

ภาพหน้าจอในสไลด์นี้มาจาก tesaiot/developer-hub (hmi_ep06_wifi_profile_nvm) ที่ commit `9a8e3ed`
