// SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
// SPDX-License-Identifier: Apache-2.0
//
// solution/06_diagnose.c — เฉลยของ practice/06_diagnose.c
//
// ตรรกะเดียวกับตัวอย่าง 07_engine_health.c และ 10_model_load_diagnosis.c ของ SDK
// แต่เขียนใหม่ให้รันบนคอมพิวเตอร์ได้
//     gcc -std=c11 -Wall -Wextra -o diagnose 06_diagnose.c && ./diagnose   -> PASS: 0 failure(s)
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

typedef struct {
    int      model;      // โมเดลที่ทำงานอยู่ตอนอ่าน (-1 = ไม่มี)
    uint32_t feeds;      // ข้อมูลที่ไปถึงโมเดล (สะสม)
    uint32_t passes;     // รอบประมวลผลที่จบ (สะสม)
    uint32_t verdicts;   // รอบที่ได้ผล (สะสม)
} sample_t;

typedef enum {
    STAGE_HEALTHY,
    STAGE_NO_FEED,              // ไม่มีข้อมูลไปถึงโมเดลเลยในช่วงวัด
    STAGE_NO_PASS,              // ข้อมูลมา แต่ task ประมวลผลไม่จบสักรอบ
    STAGE_NO_VERDICT,           // ประมวลผลจบ แต่ไม่มีผล
    STAGE_MEASUREMENT_INVALID,  // โมเดลเปลี่ยนระหว่างวัด ตัวนับถูกล้าง ส่วนต่างไม่มีความหมาย
} stage_t;

// ส่วนต่างแบบอิ่มตัว: ถ้าตัวนับถูกล้างระหว่างสองครั้งที่อ่าน (now < was) ให้คืน 0 ไม่ใช่เลขเกือบ 2^32
static uint32_t delta32(uint32_t now, uint32_t was)
{
    // SDK ใช้บรรทัดเดียวกันใน 07_engine_health.c เพราะ "a counter is cleared on a model switch"
    return (now >= was) ? (now - was) : 0u;
}

// อ่านส่วนต่างแล้วตัดสิน โดยตรวจสาเหตุที่แคบที่สุดก่อน (ขั้นต้นของสายงานก่อนขั้นปลาย)
static stage_t diagnose(sample_t before, sample_t after)
{
    // ตรวจความถูกต้องของการวัดก่อน: ถ้าโมเดลเปลี่ยน ตัวนับถูกล้าง ส่วนต่างทุกตัวจึงไม่มีความหมาย
    // การบอกว่า "วัดไม่ได้" ซื่อสัตย์กว่าการตีความตัวเลขที่ผิดตั้งแต่ต้น
    if (before.model != after.model) {
        return STAGE_MEASUREMENT_INVALID;
    }
    const uint32_t d_feeds = delta32(after.feeds, before.feeds);
    const uint32_t d_passes = delta32(after.passes, before.passes);
    const uint32_t d_verdicts = delta32(after.verdicts, before.verdicts);

    // ขั้นต้นก่อนขั้นปลาย: ถ้าไม่มีข้อมูลเข้า การที่ไม่มีรอบประมวลผลก็ไม่ใช่ข่าว
    if (d_feeds == 0u) {
        return STAGE_NO_FEED;
    }
    if (d_passes == 0u) {
        return STAGE_NO_PASS;
    }
    if (d_verdicts == 0u) {
        return STAGE_NO_VERDICT;
    }
    return STAGE_HEALTHY;
}

// ---------------------------------------------------------------------------
// ขั้นที่มาก่อน: โมเดลเคยโหลดสำเร็จไหม (อ่านครั้งเดียว ไม่ใช่ส่วนต่าง)
#define RC_NEVER_CALLED (0x7FFFFFFF)   // ค่าเดียวกับที่ ai_engine.h ของ SDK ใช้บอกว่า init() ไม่เคยถูกเรียก

typedef enum {
    LOAD_OK,
    LOAD_NEVER_RAN,     // ไม่มีใครเรียก init() ของโมเดลเลย
    LOAD_STUCK,         // เข้า init() มากกว่าที่ออกมา มีครั้งหนึ่งค้างอยู่ข้างใน
    LOAD_NO_RC,         // นับว่าเรียกแล้ว แต่ไม่มีรหัสผลลัพธ์ บัญชีไม่ตรงกัน ต้องรายงาน ไม่ใช่ถือว่าสำเร็จ
    LOAD_REFUSED,       // init() ของโมเดลคืนรหัสผิดพลาด
    LOAD_ABANDONED,     // init() สำเร็จ แต่การโหลดไม่จบ
} load_t;

static load_t load_diagnosis(uint32_t calls, uint32_t returns, uint32_t inits, int32_t last_rc)
{
    // ลำดับเดียวกับ 10_model_load_diagnosis.c ของ SDK: "Each test is only meaningful once the one
    // above it has been ruled out."
    if (calls == 0u) {
        return LOAD_NEVER_RAN;          // ดูที่ task และคำสั่งเลือกโมเดล ไม่ใช่ที่ตัวโมเดล
    }
    if (returns < calls) {
        return LOAD_STUCK;              // กรณีเดียวที่ตัวนับชี้เข้าไปข้างในโมเดล
    }
    if (last_rc == RC_NEVER_CALLED) {
        return LOAD_NO_RC;              // บัญชีไม่ตรงกัน รายงานออกไป อย่าเงียบแล้วถือว่าสำเร็จ
    }
    if (last_rc != 0) {
        return LOAD_REFUSED;            // รหัสนี้เป็นของโมเดล ไปดูใน header ของโมเดลนั้น
    }
    if (inits == 0u) {
        return LOAD_ABANDONED;          // init ผ่านแต่การโหลดถูกทิ้งกลางทาง เช่น มีการเปลี่ยนโมเดล
    }
    return LOAD_OK;
}

// ---------------------------------------------------------------------------
// ผลลัพธ์ที่บอกความจริง
typedef enum { RESULT_OK = 0, RESULT_UNAVAILABLE = -1, RESULT_NO_DATA = -4 } result_t;

typedef struct {
    bool    sensor_present;
    bool    valid;        // เคยอ่านสำเร็จอย่างน้อยหนึ่งครั้งหรือยัง
    int32_t milli_g;
} cache_t;

// คืน RESULT_UNAVAILABLE ถ้าไม่มีเซนเซอร์, RESULT_NO_DATA ถ้ายังไม่เคยอ่านได้, RESULT_OK พร้อมค่าถ้ามีข้อมูล
// และห้ามเขียนลง *out เมื่อไม่ได้คืน RESULT_OK
static result_t read_latest(const cache_t *c, int32_t *out)
{
    // สามสถานะที่ผู้เรียกต้องแยกได้: ไม่มีฮาร์ดแวร์ / มีแต่ยังไม่มีข้อมูล / มีข้อมูล
    // คืน 0 พร้อม OK จะทำให้หน้าจอแสดง 0 mg อย่างมั่นใจทั้งที่ไม่เคยวัดได้เลย
    if (!c->sensor_present) {
        return RESULT_UNAVAILABLE;
    }
    if (!c->valid) {
        return RESULT_NO_DATA;
    }
    *out = c->milli_g;
    return RESULT_OK;
}

static int failures = 0;
#define CHECK(cond)                                                                \
    do {                                                                           \
        if (!(cond)) {                                                             \
            printf("FAIL line %d: %s\n", __LINE__, #cond);                         \
            failures++;                                                            \
        }                                                                          \
    } while (0)

int main(void)
{
    // delta32
    CHECK(delta32(15u, 10u) == 5u);
    CHECK(delta32(10u, 15u) == 0u);                  // ถูกล้างระหว่างวัด

    // diagnose: ตัวเลขสะสมใหญ่ไม่ได้แปลว่าตอนนี้ยังทำงาน
    const sample_t a = {2, 5000u, 4900u, 4800u};
    CHECK(diagnose(a, (sample_t){2, 5050u, 4950u, 4850u}) == STAGE_HEALTHY);
    CHECK(diagnose(a, (sample_t){2, 5000u, 4900u, 4800u}) == STAGE_NO_FEED);
    CHECK(diagnose(a, (sample_t){2, 5050u, 4900u, 4800u}) == STAGE_NO_PASS);
    CHECK(diagnose(a, (sample_t){2, 5050u, 4950u, 4800u}) == STAGE_NO_VERDICT);
    CHECK(diagnose(a, (sample_t){3, 10u, 9u, 8u}) == STAGE_MEASUREMENT_INVALID);

    // load_diagnosis: สี่สาเหตุของ "ไม่เคยมีผลเลย" บวกกรณีบัญชีไม่ตรง
    CHECK(load_diagnosis(0u, 0u, 0u, RC_NEVER_CALLED) == LOAD_NEVER_RAN);
    CHECK(load_diagnosis(2u, 1u, 0u, 0) == LOAD_STUCK);
    CHECK(load_diagnosis(1u, 1u, 0u, RC_NEVER_CALLED) == LOAD_NO_RC);
    CHECK(load_diagnosis(1u, 1u, 0u, -5) == LOAD_REFUSED);
    CHECK(load_diagnosis(1u, 1u, 0u, 0) == LOAD_ABANDONED);
    CHECK(load_diagnosis(3u, 3u, 3u, 0) == LOAD_OK);

    // read_latest: ไม่มีข้อมูลต้องพูดว่าไม่มี และไม่แตะค่าที่ผู้เรียกถืออยู่
    int32_t v = 1234;
    const cache_t absent = {false, false, 0};
    const cache_t empty = {true, false, 0};
    const cache_t ready = {true, true, 981};
    CHECK(read_latest(&absent, &v) == RESULT_UNAVAILABLE && v == 1234);
    CHECK(read_latest(&empty, &v) == RESULT_NO_DATA && v == 1234);
    CHECK(read_latest(&ready, &v) == RESULT_OK && v == 981);

    printf("%s: %d failure(s)\n", failures ? "FAIL" : "PASS", failures);
    return failures ? 1 : 0;
}
