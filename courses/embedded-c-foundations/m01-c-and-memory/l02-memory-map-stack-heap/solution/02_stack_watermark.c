// SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
// SPDX-License-Identifier: Apache-2.0
//
// solution/02_stack_watermark.c — เฉลยของ practice/02_stack_watermark.c
//
// FreeRTOS ระบาย stack ของทุก task ด้วยไบต์ 0xA5 ตอนสร้าง task (tskSTACK_FILL_BYTE ใน tasks.c)
// แล้ว uxTaskGetStackHighWaterMark() นับว่ายังเหลือไบต์ 0xA5 ที่ไม่เคยถูกเขียนทับกี่ตัว
// นับจากปลายที่ stack ยังไปไม่ถึง ค่านี้จึง "ลดได้อย่างเดียว" เป็นค่าต่ำสุดตลอดอายุของ task
// ไฟล์นี้จำลองกลไกเดียวกันบนคอมพิวเตอร์ ด้วยอาร์เรย์หนึ่งก้อนแทน stack ที่โตลง (จากท้ายอาร์เรย์มาหาต้น)
//
//     gcc -std=c11 -Wall -Wextra -o watermark 02_stack_watermark.c && ./watermark   -> PASS: 0 failure(s)
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>

#define FILL_BYTE   (0xA5u)
#define STACK_BYTES (256u)
#define WORD_BYTES  (4u)

static int failures = 0;
#define CHECK_EQ(expected, actual)                                                    \
    do {                                                                              \
        unsigned long e_ = (unsigned long)(expected), a_ = (unsigned long)(actual);   \
        if (e_ != a_) {                                                               \
            printf("FAIL line %d: expected %lu got %lu\n", __LINE__, e_, a_);         \
            failures++;                                                               \
        }                                                                             \
    } while (0)

// ระบายทุกไบต์ของ stack ด้วย FILL_BYTE (ทำครั้งเดียวตอนสร้าง task)
static void stack_paint(uint8_t *mem, size_t n)
{
    // memset(mem, FILL_BYTE, n) ก็ได้ผลเดียวกัน FreeRTOS เองใช้ memset
    for (size_t i = 0; i < n; i++) {
        mem[i] = (uint8_t)FILL_BYTE;
    }
}

// ให้มาแล้ว: จำลองว่า task ใช้ stack ลึก used ไบต์ stack โตลง จึงเขียนจากท้ายอาร์เรย์เข้ามา
static void simulate_use(uint8_t *mem, size_t n, size_t used)
{
    for (size_t i = 0; i < used && i < n; i++) {
        mem[n - 1u - i] = (uint8_t)i;   // ค่าอะไรก็ได้ที่ไม่ใช่ 0xA5 ส่วนใหญ่
        if (mem[n - 1u - i] == FILL_BYTE) {
            mem[n - 1u - i] = 0x00u;    // กันกรณีบังเอิญเขียนค่าเท่า FILL_BYTE
        }
    }
}

// นับไบต์ที่ยังเป็น FILL_BYTE ต่อเนื่องกันจาก mem[0] ขึ้นไป (ปลายที่ stack ยังไปไม่ถึง)
static size_t high_water_bytes(const uint8_t *mem, size_t n)
{
    // เริ่มจากปลายที่ stack ยังไปไม่ถึง (ที่อยู่ต่ำสุด เพราะ stack โตลง) แล้วนับจนเจอรอยแรกที่ถูกเขียน
    // ไบต์ที่ถูกเขียนแล้วไม่มีวันกลับเป็น FILL_BYTE ค่านี้จึงลดได้อย่างเดียว คือค่าต่ำสุดตลอดอายุ task
    size_t count = 0u;
    while (count < n && mem[count] == FILL_BYTE) {
        count++;
    }
    return count;
}

// เปอร์เซ็นต์ที่ใช้ไปแล้ว คิดแบบเดียวกับตัวอย่าง 07_engine_health ของ SDK
// total_words == 0 หมายถึง task ไม่เคยถูกสร้าง ให้คืน 0 (ห้ามหารด้วยศูนย์)
static unsigned percent_used(uint32_t total_words, uint32_t free_words)
{
    // ตัวอย่าง 07_engine_health ของ SDK ตรวจ total == 0 ก่อนหารเหมือนกัน (task ไม่เคยถูกสร้าง)
    // ถ้า free > total แปลว่าข้อมูลเสีย คืน 0 ดีกว่าคืนเลขที่ลบแล้ววนกลับเป็นค่ามหาศาล
    if (total_words == 0u || free_words > total_words) {
        return 0u;
    }
    return (unsigned)(((total_words - free_words) * 100u) / total_words);
}

// ให้มาแล้ว: เกณฑ์ตัดสินของหลักสูตรนี้ (ไม่ใช่ตัวเลขจาก SDK หรือ FreeRTOS)
//   เหลือน้อยกว่า 32 words (128 ไบต์) = CRITICAL, เหลือน้อยกว่าหนึ่งในสี่ = LOW, นอกนั้น OK
static const char *verdict(uint32_t total_words, uint32_t free_words)
{
    if (total_words == 0u) {
        return "NO TASK";
    }
    if (free_words < 32u) {
        return "CRITICAL";
    }
    if (free_words * 4u < total_words) {
        return "LOW";
    }
    return "OK";
}

int main(void)
{
    static uint8_t stack_mem[STACK_BYTES];   // static ไม่ใช่ local: ไม่อยากให้มันไปกิน stack ของ main เอง

    stack_paint(stack_mem, STACK_BYTES);
    CHECK_EQ(STACK_BYTES, high_water_bytes(stack_mem, STACK_BYTES));   // ยังไม่ถูกใช้เลย

    simulate_use(stack_mem, STACK_BYTES, 100u);
    CHECK_EQ(156u, high_water_bytes(stack_mem, STACK_BYTES));

    simulate_use(stack_mem, STACK_BYTES, 200u);                      // ลึกขึ้น
    CHECK_EQ(56u, high_water_bytes(stack_mem, STACK_BYTES));

    simulate_use(stack_mem, STACK_BYTES, 20u);                       // ตื้นลง ค่าต่ำสุดต้องไม่ขยับขึ้น
    CHECK_EQ(56u, high_water_bytes(stack_mem, STACK_BYTES));

    CHECK_EQ(75u, percent_used(1024u, 256u));
    CHECK_EQ(0u, percent_used(0u, 0u));
    CHECK_EQ(100u, percent_used(512u, 0u));

    const uint32_t total_words = STACK_BYTES / WORD_BYTES;
    const uint32_t free_words = (uint32_t)(high_water_bytes(stack_mem, STACK_BYTES) / WORD_BYTES);
    printf("stack: %lu words, %lu never used, %u%% used -> %s\n",
           (unsigned long)total_words, (unsigned long)free_words,
           percent_used(total_words, free_words), verdict(total_words, free_words));

    printf("%s: %d failure(s)\n", failures ? "FAIL" : "PASS", failures);
    return failures ? 1 : 0;
}
