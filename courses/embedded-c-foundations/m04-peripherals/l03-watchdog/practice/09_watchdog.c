// SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
// SPDX-License-Identifier: Apache-2.0
//
// practice/09_watchdog.c — ฝึกเติม: ผู้ดูแล watchdog แบบ check-in และบันทึกสาเหตุการรีเซ็ตที่รอดข้ามการรีเซ็ต
//
// บนบอร์ดจริง
//   - supervisor_poll() รันใน task ที่ความสำคัญต่ำ ถ้าคืน true ให้เรียก Cy_WDT_ClearWatchdog() ของ PDL
//   - boot_record_t วางไว้ใน section .noinit (linker script ของ SDK มี section นี้ และ startup ไม่ล้างมัน)
//     เช่น  static boot_record_t s_rec __attribute__((section(".noinit")));
//   - reset_reason มาจาก Cy_SysLib_GetResetReason() ค่าคงที่ข้างล่างเท่ากับ CY_SYSLIB_RESET_* ของ PDL
// ไฟล์นี้จำลองทั้งหมดบนคอมพิวเตอร์ มีช่องให้เติม 5 จุด (มองหา TODO)
//     gcc -std=c11 -Wall -Wextra -o watchdog 09_watchdog.c && ./watchdog
// ก่อนเติม test จะล้ม ลองเองก่อนอย่างน้อย 15 นาที แล้วค่อยเปิด solution/09_watchdog.c
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

#define SIM_RESET_POWER_ON (0x0000u)   // BSP ของ SDK ถือว่า 0 คือ POR, XRES หรือ BOD
#define SIM_RESET_HWWDT    (0x0001u)   // = CY_SYSLIB_RESET_HWWDT
#define SIM_RESET_SOFT     (0x0010u)   // = CY_SYSLIB_RESET_SOFT
#define RECORD_MAGIC       (0x5A17D06Eu)

typedef struct {
    uint32_t expected;   // บิตของ task ที่ต้อง check in ทุกรอบ
    uint32_t checkin;    // บิตที่ check in แล้วในรอบนี้
} supervisor_t;

typedef struct {
    uint32_t magic;          // ใช้แยก "ข้อมูลที่เราเขียน" ออกจากขยะใน RAM หลังเปิดไฟครั้งแรก
    uint32_t boots;          // บูตกี่ครั้งตั้งแต่เริ่มบันทึก
    uint32_t wdt_resets;     // กี่ครั้งที่สาเหตุคือ watchdog
    uint32_t missing;        // task ที่ขาด check in ครั้งล่าสุดที่ supervisor ดู (breadcrumb)
    uint32_t last_missing;   // missing ที่เหลือค้างตอน watchdog รีเซ็ตครั้งล่าสุด
} boot_record_t;

// task แต่ละตัวเรียกเมื่อทำงานคืบหน้าจริง (ไม่ใช่แค่ตื่นขึ้นมา)
static void wd_checkin(supervisor_t *s, uint32_t task_id)
{
    (void)s;
    (void)task_id;
    /* TODO 1: ตั้งบิตของ task นี้ใน checkin */
}

// เรียกเป็นระยะจาก task ที่ความสำคัญต่ำ คืน true เมื่อควรป้อน watchdog
static bool supervisor_poll(supervisor_t *s, boot_record_t *rec)
{
    rec->missing = s->expected & ~s->checkin;   // ให้มาแล้ว: ทิ้งร่องรอยไว้เผื่อรอบนี้คือรอบสุดท้ายก่อนรีเซ็ต

    /* TODO 2: ถ้ามี task ใดยังไม่ check in ให้คืน false (ไม่ป้อน) */

    /* TODO 3: ทุก task check in ครบแล้ว ล้าง checkin ให้ทุก task ต้องพิสูจน์ใหม่ในรอบหน้า แล้วคืน true */
    return true;
}

// เรียกครั้งเดียวตอนบูต ก่อนเริ่ม task
static void boot_record_update(boot_record_t *rec, uint32_t reset_reason)
{
    /* TODO 4: ถ้า magic ไม่ตรง (เปิดไฟครั้งแรก หรือ RAM ถูกลบ) ให้ตั้ง magic และล้างตัวนับทุกตัวเป็น 0 */

    rec->boots++;

    /* TODO 5: ถ้า reset_reason มีบิต SIM_RESET_HWWDT ให้เพิ่ม wdt_resets และคัดลอก missing ไปเก็บใน last_missing */
    (void)reset_reason;
}

static int failures = 0;
#define CHECK_EQ(expected, actual)                                                           \
    do {                                                                                     \
        unsigned long e_ = (unsigned long)(expected), a_ = (unsigned long)(actual);          \
        if (e_ != a_) {                                                                      \
            printf("FAIL line %d: %s expected %lu got %lu\n", __LINE__, #actual, e_, a_);    \
            failures++;                                                                      \
        }                                                                                    \
    } while (0)

int main(void)
{
    // RAM ตอนเปิดไฟครั้งแรกเป็นค่าอะไรก็ได้ จำลองด้วยขยะ
    boot_record_t rec = {0xDEADBEEFu, 77u, 99u, 5u, 5u};

    boot_record_update(&rec, SIM_RESET_POWER_ON);
    CHECK_EQ(RECORD_MAGIC, rec.magic);
    CHECK_EQ(1u, rec.boots);
    CHECK_EQ(0u, rec.wdt_resets);

    supervisor_t s = {0x7u, 0u};     // task 0, 1, 2
    wd_checkin(&s, 0u);
    wd_checkin(&s, 2u);
    CHECK_EQ(0, supervisor_poll(&s, &rec));    // task 1 ยังไม่มา: ห้ามป้อน
    CHECK_EQ(0x2u, rec.missing);
    wd_checkin(&s, 1u);
    CHECK_EQ(1, supervisor_poll(&s, &rec));    // ครบแล้ว: ป้อน
    CHECK_EQ(0u, s.checkin);                   // และล้างสำหรับรอบหน้า
    CHECK_EQ(0, supervisor_poll(&s, &rec));    // รอบใหม่ยังไม่มีใคร check in: ห้ามป้อน

    // task 0 ค้าง: 1 และ 2 ยังทำงาน แต่ supervisor ไม่ป้อน watchdog จึงรีเซ็ต
    wd_checkin(&s, 1u);
    wd_checkin(&s, 2u);
    CHECK_EQ(0, supervisor_poll(&s, &rec));
    boot_record_update(&rec, SIM_RESET_HWWDT);  // บูตใหม่หลัง watchdog รีเซ็ต (rec รอดเพราะอยู่ใน .noinit)
    CHECK_EQ(2u, rec.boots);
    CHECK_EQ(1u, rec.wdt_resets);
    CHECK_EQ(0x1u, rec.last_missing);          // รู้ว่า task 0 คือตัวที่ค้าง

    boot_record_update(&rec, SIM_RESET_SOFT);   // รีเซ็ตแบบซอฟต์แวร์ ไม่ใช่ watchdog
    CHECK_EQ(3u, rec.boots);
    CHECK_EQ(1u, rec.wdt_resets);

    printf("%s: %d failure(s)\n", failures ? "FAIL" : "PASS", failures);
    return failures ? 1 : 0;
}
