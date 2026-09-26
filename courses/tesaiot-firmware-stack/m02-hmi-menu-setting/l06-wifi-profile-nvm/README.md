---
id: fw-stack.m02.l06
lang: th
title:
  th: "เก็บโปรไฟล์ Wi-Fi ลงหน่วยความจำถาวร"
  en: "Store the Wi-Fi profile in non-volatile memory"
summary:
  th: "เก็บ SSID + password ลง non-volatile memory — form กรอก profile ผ่าน lv_textarea (password mode) และ save/load ผ่าน profile store"
  en: "Store the Wi-Fi profile in non-volatile memory"
level: L3
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m02.l05]
objectives:
  - th: "สร้างฟอร์มกรอก SSID และรหัสผ่าน โดยช่องรหัสผ่านอยู่ใน password mode"
    en: "Build an SSID and password form with the password field in password mode"
  - th: "บันทึก โหลด และล้างโปรไฟล์ผ่าน profile store ใน NVM ได้ และค่ายังอยู่หลังรีเซ็ตบอร์ด"
    en: "Save, load and clear the profile through the NVM profile store, and keep it across a board reset"
  - th: "อธิบายความเสี่ยงของการเก็บรหัสผ่านใน flash และแนวทางลดความเสี่ยง"
    en: "Explain the risk of keeping a password in flash and ways to reduce it"
develops:
  - {skill: sys.memory-fs, to: 2}
  - {skill: gui.hmi, to: 2}
  - {skill: sec.fundamentals, to: 1}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "hmi_ep06_wifi_profile_nvm"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
---

# เก็บโปรไฟล์ Wi-Fi ลงหน่วยความจำถาวร

## เป้าหมาย

1. สร้างฟอร์มกรอก SSID และรหัสผ่าน โดยช่องรหัสผ่านอยู่ใน password mode
2. บันทึก โหลด และล้างโปรไฟล์ผ่าน profile store ใน NVM ได้ และค่ายังอยู่หลังรีเซ็ตบอร์ด
3. อธิบายความเสี่ยงของการเก็บรหัสผ่านใน flash และแนวทางลดความเสี่ยง

## แนวคิด

### หน่วยเก็บที่ใช้จริงคือ RRAM ของ PSoC Edge ไม่ใช่ flash ทั่วไป

README ของ episode พูดกว้าง ๆ ว่า implementation "จะใช้ API ของ PSoC flash เช่น `cyhal_flash_*` หรือ `cy_em_eeprom`
หรือ MCUboot NVS แล้วแต่บอร์ด" แต่โค้ดจริงที่ commit `9a8e3ed` เรียก **`Cy_RRAM_TSReadByteArray()`** และ
**`Cy_RRAM_NvmWriteByteArray()`** ตรง ๆ กับ `RRAMC0` — RRAM (Resistive RAM) คือหน่วยความจำไม่ลบเลือนบนชิปของ PSoC
Edge E84 เอง ที่อยู่เขียนคือ `CYMEM_CM55_0_user_nvm_C_START` (พื้นที่ user NVM ของ CM55) ไม่ใช่ EEPROM emulation
หรือ MCUboot NVS แยกต่างหาก

### บันทึกเป็น record ขนาดคงที่ 256 ไบต์ พร้อม magic + CRC32

`wifi_profile_record_t` ที่เขียนลง RRAM จริงมี `magic` (`0x57465031` = "WFP1" ไม่ใช่ "WIFI" ตามที่ README ต้นทาง
บอก), `version`, `payload_len`, `crc32`, `valid` และข้อมูล ssid/password/security/auto_connect รวมกันพอดีใน
`WIFI_PROFILE_SLOT_SIZE = 256` ไบต์ (ตรวจด้วย compile-time assertion `wifi_profile_record_size_check`) CRC32
คำนวณจาก payload เท่านั้น ไม่รวม header ของ record ใช้ตรวจว่าอ่านค่ากลับมาไม่เพี้ยน ส่วน struct สาธารณะ
`wifi_profile_data_t` ที่ UI เห็นมีแค่ `ssid`, `password`, `security`, `auto_connect` — ไม่มีฟิลด์ `magic` (magic
อยู่ใน record ภายในเท่านั้น ไม่ใช่ struct ที่ UI ส่งเข้าออก ตามที่ README ต้นทางเขียนไว้)

### เขียนแล้วอ่านกลับมาตรวจ (verify-after-write) และข้ามการเขียนถ้าค่าไม่เปลี่ยน

`wifi_profile_store_save()` เทียบ block ที่จะเขียนกับ block ปัจจุบันก่อน ถ้าเหมือนกันทุกไบต์จะข้ามการเขียนเลย
(`SAVE_SKIP_SAME`) เพื่อลดจำนวนรอบเขียนของหน่วยความจำ (wear) หลังเขียนจริงแล้วมันอ่านกลับมาเทียบกับ block ที่ตั้งใจ
เขียนอีกครั้ง (`verify_block`) ถ้าไม่ตรงจะถือว่าล้มเหลว (`SAVE_VERIFY_FAIL`) แม้ `Cy_RRAM_NvmWriteByteArray()` จะ
คืนค่า success ก็ตาม — เป็นการตรวจสองชั้นสำหรับข้อมูลที่สำคัญ

### แยก slot "erased" ออกจาก slot "ไม่มีข้อมูล" ด้วยรูปแบบ 0xFF

RRAM/flash ที่ยังไม่เคยเขียนจะมีค่าไบต์เป็น `0xFF` ทั้งบล็อก `wifi_profile_is_erased()` เช็ค pattern นี้ก่อนพยายาม
parse เป็น record เสมอ ถ้าไม่เช็คแล้วอ่าน `0xFF` ทั้งก้อนไปตีความเป็น struct ตรง ๆ อาจได้ `magic` ที่บังเอิญตรง
(แม้โอกาสน้อยก็ตาม) การ "clear" จึงหมายถึงเขียน `0xFF` ทับทั้ง slot ไม่ใช่มี erase API แยกต่างหาก

### auto-fill จาก Scan ไปหน้า Profile: ต้องกดปุ่ม "Use" ไม่ใช่แค่แตะแถว

README ต้นทางอธิบายว่าแค่แตะแถวใน scan list จะ auto-jump ไปหน้า Profile พร้อม pre-fill SSID ทันที แต่โค้ดจริงแบ่ง
เป็นสองขั้น: แตะแถวก่อนเพื่อ **เลือก** (`s_ctx.selected_idx`) แล้วต้องกดปุ่ม **"Use this AP"** แยกต่างหากเพื่อคัดลอก
AP ที่เลือกไปหน้า Profile จริง (`ui_wifi_use_selected_ap_cb()` เรียก callback ที่ถูกลงทะเบียนไว้ ซึ่งไปเรียก
`ui_wifi_profile_page_apply_ap()` ที่ copy SSID + security เข้า form) หน้า scan กับหน้า profile ไม่รู้จักกันโดยตรง
— เชื่อมกันผ่าน callback ที่ registered ไว้ตอนสร้าง shell เท่านั้น ไม่ใช่ผ่าน global state `pending_ssid` ใน
`menu_nav_state_t` ตามที่ README ต้นทางอธิบาย (state จริงของ `menu_nav_state_t` ใน episode นี้ไม่มีฟิลด์ SSID เลย)

## ตัวอย่างสมบูรณ์

โค้ดของ episode นี้อยู่ใน Developer Hub (อ้างอิงที่ commit `9a8e3ed`) — อ่าน Why ของ [README ต้นทาง](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm/README.md) เพื่อเข้าใจจุดประสงค์ แต่ **โค้ดตัวอย่างด้านล่างคัดลอกจากไฟล์จริง** (Apache-2.0, tesaiot/developer-hub, commit เดียวกัน) เพราะรายละเอียดของ storage และ cross-page flow ต่างจากที่ README ต้นทางอธิบายไว้

[`wifi_profile/wifi_profile_store.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm/wifi_profile/wifi_profile_store.c) — เขียนลง RRAM จริง พร้อม skip-if-same และ verify-after-write:

```c
/* Skip write if content is unchanged to reduce NVM wear. */
if(wifi_profile_read_slot(WIFI_PROFILE_PRIMARY_ADDR, current_block)) {
    if(0 == memcmp(current_block, block, sizeof(block))) {
        wifi_profile_log("SAVE_SKIP_SAME");
        return true;
    }
}

if(!wifi_profile_write_slot(WIFI_PROFILE_PRIMARY_ADDR, block)) {
    return false;
}

if(!wifi_profile_read_slot(WIFI_PROFILE_PRIMARY_ADDR, verify_block)) {
    return false;
}

if(0 != memcmp(verify_block, block, sizeof(block))) {
    wifi_profile_log("SAVE_VERIFY_FAIL");
    return false;
}
```

`wifi_profile_read_slot()`/`write_slot()` เรียก RRAM API ของ PSoC Edge ตรง ๆ:

```c
static bool wifi_profile_read_slot(uint32_t addr, uint8_t *out)
{
    cy_en_rram_status_t st = Cy_RRAM_TSReadByteArray(RRAMC0, addr, out, WIFI_PROFILE_SLOT_SIZE);
    return (st == CY_RRAM_SUCCESS);
}

static bool wifi_profile_write_slot(uint32_t addr, const uint8_t *in)
{
    cy_en_rram_status_t st = Cy_RRAM_NvmWriteByteArray(RRAMC0, addr, (uint8_t *)in, WIFI_PROFILE_SLOT_SIZE);
    return (st == CY_RRAM_SUCCESS);
}
```

[`wifi_list/ui_wifi_list_page.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm/wifi_list/ui_wifi_list_page.c) — ต้องเลือกแถวก่อน แล้วกดปุ่ม Use แยก:

```c
static void ui_wifi_use_selected_ap_cb(lv_event_t *e)
{
    uint16_t count;
    const wifi_scan_ap_t *aps = wifi_scan_service_get_list(&s_ctx.service, &count);

    if((aps == NULL) || (count == 0U) || (s_ctx.selected_idx >= count)) {
        lv_label_set_text(s_ctx.hint_label, "Select an AP row before using it in profile page.");
        return;
    }

    s_use_ap_cb(&aps[s_ctx.selected_idx], s_use_ap_user_data);
    lv_label_set_text(s_ctx.hint_label, "AP copied to profile page.");
}
```

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm/main_example.c) pre-init WiFi scan service แล้ว forward เข้า `ui_wifi_profile_nvm_create()` ตรงตามที่ README ต้นทางอธิบาย
- [`wifi_profile/wifi_profile_types.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm/wifi_profile/wifi_profile_types.h) — struct สาธารณะจริง (ไม่มี `magic`)
- ดูโฟลเดอร์เต็มที่ [`hmi_ep06_wifi_profile_nvm/`](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm)

## จุดที่มักพลาด

- **คิดว่าใช้ generic flash API** — README ต้นทางพูดกว้าง ๆ ถึง `cyhal_flash_*`/`cy_em_eeprom`/MCUboot NVS แต่โค้ด
  จริงเรียก RRAM API (`Cy_RRAM_TSReadByteArray`, `Cy_RRAM_NvmWriteByteArray`) ตรง ๆ กับพื้นที่ user NVM ของ CM55
- **ไม่เช็คว่า slot ถูก erase หรือมีข้อมูลจริง** — ต้องเช็ค pattern `0xFF` ทั้งบล็อกก่อนเสมอ ไม่งั้นอาจตีความขยะจาก
  หน่วยความจำที่ยังไม่เคยเขียนเป็นโปรไฟล์ที่ใช้ได้
- **เขียนแล้วไม่ตรวจกลับ (verify-after-write)** — โค้ดต้นทางทำสองชั้นคือเช็ค return code ของการเขียน และอ่าน
  กลับมาเทียบไบต์ต่อไบต์อีกที ถ้าข้ามขั้นตอนนี้จะไม่รู้ว่าการเขียนเพี้ยนจริงหรือไม่
- **คิดว่าแตะแถวใน scan list จะ auto-jump ไปหน้า profile ทันที** — โค้ดจริงต้องกดปุ่ม "Use this AP" แยกอีกขั้น
  หลังเลือกแถว ไม่ใช่ auto-jump แบบที่ README ต้นทางอธิบาย

### build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

หรือเปิด [ตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep06_wifi_profile_nvm&q=hmi_ep06_wifi_profile_nvm) แล้ว flash เฟิร์มแวร์สำเร็จรูป

## ดูของจริงก่อน

![หน้าจอของ EP06 — WiFi Profile NVM บน TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm/hmi_ep06_wifi_profile_nvm.png)

ก่อนอ่านโค้ด ให้ทายว่าหน้าจอนี้มี object อะไรบ้าง และอะไรเปลี่ยนเมื่อผู้ใช้แตะหรือเมื่อค่าเซนเซอร์เปลี่ยน

## ลองแก้

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

## เช็กความเข้าใจ

- ข้อมูลใน NVM ต่างจากตัวแปรใน RAM อย่างไรเมื่อบอร์ดรีเซ็ต
- ทำไมช่องรหัสผ่านต้องซ่อนตัวอักษร
- ถ้าต้องการลบโปรไฟล์ทั้งหมด ต้องเรียกฟังก์ชันใดของ profile store

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [README ของ episode](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm/README.md) · [โฟลเดอร์โค้ด](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm) · commit `9a8e3ed`
- [เปิดตัวอย่างนี้บน Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep06_wifi_profile_nvm&q=hmi_ep06_wifi_profile_nvm)
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้
