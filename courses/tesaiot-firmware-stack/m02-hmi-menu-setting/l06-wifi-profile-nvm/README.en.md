---
id: fw-stack.m02.l06
lang: en
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
source_sha256: c9c66fac0adbaaac9ed6014f726069c4baff1a102b692d21caf1a63c026c2f12
---

# Store the Wi-Fi profile in non-volatile memory

## Objectives

1. Build an SSID and password form with the password field in password mode
2. Save, load and clear the profile through the NVM profile store, and keep it across a board reset
3. Explain the risk of keeping a password in flash and ways to reduce it

## Concepts

### The real storage is the PSoC Edge's RRAM, not generic flash

The episode's README speaks broadly of an implementation that "uses a PSoC flash API such as `cyhal_flash_*`,
`cy_em_eeprom`, or MCUboot NVS, depending on the board." The actual code at commit `9a8e3ed` instead calls
**`Cy_RRAM_TSReadByteArray()`** and **`Cy_RRAM_NvmWriteByteArray()`** directly against `RRAMC0` — RRAM (Resistive
RAM) is the on-chip non-volatile memory of the PSoC Edge E84 itself. The write address is
`CYMEM_CM55_0_user_nvm_C_START` (CM55's user NVM region), not an EEPROM emulation layer or a separate MCUboot NVS.

### Saved as a fixed 256-byte record with a magic value and a CRC32

The `wifi_profile_record_t` written to RRAM actually has `magic` (`0x57465031`, "WFP1" — not "WIFI" as the
upstream README states), `version`, `payload_len`, `crc32`, `valid`, plus the ssid/password/security/auto_connect
data, all fitting exactly within `WIFI_PROFILE_SLOT_SIZE = 256` bytes (checked by the compile-time assertion
`wifi_profile_record_size_check`). The CRC32 covers only the payload, not the record header, and is used to
confirm the data read back has not been corrupted. The public struct `wifi_profile_data_t` that the UI sees only
has `ssid`, `password`, `security` and `auto_connect` — it has no `magic` field at all (magic lives only in the
internal record, not in the struct passed in and out by the UI, contrary to what the upstream README implies).

### Write, then read back to verify — and skip the write if nothing changed

`wifi_profile_store_save()` first compares the block it is about to write against the block currently stored; if
every byte matches, it skips the write entirely (`SAVE_SKIP_SAME`) to reduce the number of write cycles (wear).
After a real write, it reads the data back and compares it byte-for-byte against the intended block
(`verify_block`); a mismatch is treated as a failure (`SAVE_VERIFY_FAIL`) even though `Cy_RRAM_NvmWriteByteArray()`
itself reported success — a double check for data that matters.

### Telling an "erased" slot apart from "no data" using the 0xFF pattern

RRAM/flash that has never been written reads back as `0xFF` across the whole block. `wifi_profile_is_erased()`
always checks for this pattern before attempting to parse a record. Skip that check and read `0xFF` bytes straight
into the struct, and you risk (however unlikely) a `magic` value that happens to match. "Clearing" therefore means
writing `0xFF` over the whole slot — there is no separate erase API.

### Auto-fill from Scan to Profile needs a button press, not just a tap

The upstream README describes tapping a row in the scan list as auto-jumping to the Profile page with the SSID
pre-filled immediately. The real code splits this into two steps: tapping a row only **selects** it
(`s_ctx.selected_idx`); a separate **"Use this AP"** button must then be pressed to actually copy the selected AP
over to the Profile page (`ui_wifi_use_selected_ap_cb()` calls a registered callback, which in turn calls
`ui_wifi_profile_page_apply_ap()` to copy the SSID and security into the form). The scan page and the profile page
do not know about each other directly — they are wired together only through a callback registered when the shell
is built, not through a global `pending_ssid` field on `menu_nav_state_t` as the upstream README describes (the
real `menu_nav_state_t` in this episode has no SSID field at all).

## Worked example

This episode's code lives on the Developer Hub (pinned to commit `9a8e3ed`) — read the Why section of the
[upstream README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm/README.md)
to understand its purpose, but **the excerpts below are copied from the actual files** (Apache-2.0,
tesaiot/developer-hub, same commit), because the storage details and the cross-page flow differ from the upstream
README.

[`wifi_profile/wifi_profile_store.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm/wifi_profile/wifi_profile_store.c) — writes to real RRAM, with skip-if-same and verify-after-write:

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

`wifi_profile_read_slot()`/`write_slot()` call the PSoC Edge's RRAM API directly:

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

[`wifi_list/ui_wifi_list_page.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm/wifi_list/ui_wifi_list_page.c) — a row must be selected first, then a separate Use button:

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

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm/main_example.c) pre-inits the WiFi scan service then forwards into `ui_wifi_profile_nvm_create()`, exactly as the upstream README describes
- [`wifi_profile/wifi_profile_types.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm/wifi_profile/wifi_profile_types.h) — the real public struct (no `magic`)
- See the full folder at [`hmi_ep06_wifi_profile_nvm/`](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm)

## Common mistakes

- **Assuming a generic flash API is used** — the upstream README speaks broadly of
  `cyhal_flash_*`/`cy_em_eeprom`/MCUboot NVS, but the real code calls the RRAM API
  (`Cy_RRAM_TSReadByteArray`, `Cy_RRAM_NvmWriteByteArray`) directly against CM55's user NVM region.
- **Not checking whether a slot is erased versus holding real data** — you must always check for the `0xFF`
  pattern across the whole block first, or you risk misreading never-written memory as a usable profile.
- **Writing without verifying afterward** — the source code does this in two layers: checking the write's return
  code, and reading the data back to compare byte-for-byte. Skip this and you cannot know whether a write was
  actually corrupted.
- **Assuming tapping a scan row auto-jumps to the profile page** — the real code needs a separate "Use this AP"
  button press after selecting a row, not the auto-jump the upstream README describes.

### Build and flash

```sh
# In the master template folder (see lesson 1.1)
# 1) Delete the old episode's files in proj_cm55/apps/
# 2) Copy all of this episode's files into proj_cm55/apps/
make build
make program     # flash through KitProg3
```

Or open [this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep06_wifi_profile_nvm&q=hmi_ep06_wifi_profile_nvm) and flash the ready-made firmware.

## See it work first

![Screen of EP06 — WiFi Profile NVM on the TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm/hmi_ep06_wifi_profile_nvm.png)

Before reading the code, guess what objects this screen has, and what changes when the user taps it or when a sensor value changes.

## Try a change

1. **Guess** before you change anything: pick one value the example's README explains in the How section, and write down what you expect to change on the screen or in the log.
2. **Change and run**: build + flash, then compare against your guess. If it does not match, find which part you misunderstood.
3. **Extend**: add one thing the example does not yet have, and keep a photo or video in your portfolio.

## Check your understanding

- How does data in NVM differ from a variable in RAM when the board resets?
- Why must the password field hide its characters?
- If you need to erase every profile, which profile-store function must you call?

The answers are in the example's README and in the code. If you cannot answer one, go back and read the Why / What / How section again.

## References

- [Episode README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm/README.md) · [code folder](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep06_wifi_profile_nvm) · commit `9a8e3ed`
- [Open this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep06_wifi_profile_nvm&q=hmi_ep06_wifi_profile_nvm)
- The code belongs to the Developer Hub and is referenced by link, not copied into this repository
