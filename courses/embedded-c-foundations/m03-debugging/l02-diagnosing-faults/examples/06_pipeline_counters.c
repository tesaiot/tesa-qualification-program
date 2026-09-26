// SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
// SPDX-License-Identifier: Apache-2.0
//
// examples/06_pipeline_counters.c — อาการเดียวกัน สาเหตุต่างกัน แยกด้วยส่วนต่างของตัวนับ
//
// จำลองสายงานสามขั้นแบบเดียวกับ Edge AI ของ SDK: ข้อมูลเข้า (feeds) -> รอบประมวลผล (passes)
// -> ผลที่ได้ (verdicts) ทุกขั้นมีตัวนับสะสม แล้วจำลองความผิดพลาดสามแบบที่ "หน้าจอดูเหมือนกัน"
//
//     gcc -std=c11 -Wall -Wextra -o pipeline 06_pipeline_counters.c
//     ./pipeline
//
// ทายก่อนรัน: ในกรณี "no verdict" ส่วนต่างของตัวนับตัวไหนจะเป็นศูนย์ และคอลัมน์ result จะบอกอะไร
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

typedef struct {
    uint32_t feeds;     // ข้อมูลที่ไปถึงขั้นประมวลผล
    uint32_t passes;    // รอบประมวลผลที่ทำจบ
    uint32_t verdicts;  // รอบที่ได้ผลลัพธ์จริง
} counters_t;

// ผลลัพธ์ที่บอกความจริง: แยก "ไม่มีข้อมูล" "ยังไม่พร้อม" ออกจาก "สำเร็จ" (แบบเดียวกับ SDK_EX_* ของ SDK)
typedef enum { RESULT_OK, RESULT_NO_DATA, RESULT_UNAVAILABLE } result_t;

typedef enum { FAULT_NONE, FAULT_NO_SOURCE, FAULT_TASK_STUCK, FAULT_NO_VERDICT } fault_t;

static counters_t g_counters;   // สะสมตั้งแต่เริ่ม เหมือนตัวนับของ SDK
static bool g_have_result;

// ท่าที่ 1: สายงานหนึ่งจังหวะ ความผิดพลาดแต่ละแบบหยุดสายงานคนละขั้น
static void pipeline_tick(fault_t fault)
{
    if (fault == FAULT_NO_SOURCE) {
        return;                         // เซนเซอร์ไม่ส่งอะไรมา
    }
    g_counters.feeds++;
    if (fault == FAULT_TASK_STUCK) {
        return;                         // ข้อมูลมาถึง แต่ task ประมวลผลไม่ได้ทำงาน
    }
    g_counters.passes++;
    if (fault == FAULT_NO_VERDICT) {
        return;                         // ประมวลผลครบรอบ แต่ไม่มีผล (เช่น หน้าต่างข้อมูลยังไม่เต็ม หรือตัวเร่งค้าง)
    }
    g_counters.verdicts++;
    g_have_result = true;
}

// ท่าที่ 2: ฟังก์ชันที่ UI เรียก ถ้ายังไม่เคยมีผล ต้องบอกว่า "ไม่มีข้อมูล" ไม่ใช่คืนศูนย์แล้วบอกว่าสำเร็จ
static result_t get_confidence(int *out_percent)
{
    if (!g_have_result) {
        return RESULT_NO_DATA;
    }
    *out_percent = 87;                  // ค่าตัวอย่าง
    return RESULT_OK;
}

static uint32_t delta32(uint32_t now, uint32_t was)
{
    return (now >= was) ? (now - was) : 0u;   // ตัวนับถูกล้างระหว่างวัด -> ไม่คืนเลขมหาศาล
}

static void run_case(const char *name, fault_t fault)
{
    g_counters = (counters_t){0};
    g_have_result = false;

    // ท่าที่ 3: อ่านสองครั้งห่างกันหนึ่ง "ช่วงวัด" แล้วดูส่วนต่าง ตัวเลขสะสมตัวเดียวตอบไม่ได้ว่าตอนนี้ยังทำงานอยู่ไหม
    for (int i = 0; i < 50; i++) {
        pipeline_tick(FAULT_NONE);      // ช่วงแรกทำงานปกติ ตัวนับสะสมจึงไม่เป็นศูนย์
    }
    const counters_t a = g_counters;
    for (int i = 0; i < 20; i++) {
        pipeline_tick(fault);           // ช่วงที่วัด
    }
    const counters_t b = g_counters;

    int pct = 0;
    const result_t r = get_confidence(&pct);
    printf("%-14s totals f=%-3u p=%-3u v=%-3u | deltas f=+%-2u p=+%-2u v=+%-2u | result=%s\n",
           name, (unsigned)b.feeds, (unsigned)b.passes, (unsigned)b.verdicts,
           (unsigned)delta32(b.feeds, a.feeds), (unsigned)delta32(b.passes, a.passes),
           (unsigned)delta32(b.verdicts, a.verdicts),
           r == RESULT_OK ? "OK" : (r == RESULT_NO_DATA ? "NO_DATA" : "UNAVAILABLE"));
}

int main(void)
{
    run_case("healthy", FAULT_NONE);
    run_case("no source", FAULT_NO_SOURCE);
    run_case("task stuck", FAULT_TASK_STUCK);
    run_case("no verdict", FAULT_NO_VERDICT);
    return 0;
}
