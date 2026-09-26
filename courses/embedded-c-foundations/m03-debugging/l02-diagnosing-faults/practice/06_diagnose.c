// SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
// SPDX-License-Identifier: Apache-2.0
//
// practice/06_diagnose.c — ฝึกเติม: ตัววินิจฉัยที่อ่านตัวนับแล้วบอกว่าสายงานพังที่ขั้นไหน
//
// ตรรกะเดียวกับตัวอย่าง 07_engine_health.c และ 10_model_load_diagnosis.c ของ SDK
// แต่เขียนใหม่ให้รันบนคอมพิวเตอร์ได้ มีช่องให้เติม 5 จุด (มองหา TODO)
//     gcc -std=c11 -Wall -Wextra -o diagnose 06_diagnose.c && ./diagnose
// ก่อนเติม test จะล้มหลายข้อ ลองเองก่อนอย่างน้อย 15 นาที แล้วค่อยเปิด solution/06_diagnose.c
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
    (void)now;
    (void)was;
    /* TODO 1 */
    return 0u;
}

// อ่านส่วนต่างแล้วตัดสิน โดยตรวจสาเหตุที่แคบที่สุดก่อน (ขั้นต้นของสายงานก่อนขั้นปลาย)
static stage_t diagnose(sample_t before, sample_t after)
{
    /* TODO 2: ถ้า model ของสองครั้งไม่เท่ากัน คืน STAGE_MEASUREMENT_INVALID ก่อนคำนวณอะไรทั้งนั้น */

    /* TODO 3: คำนวณส่วนต่างของ feeds passes verdicts ด้วย delta32()
     *         แล้วคืน STAGE_NO_FEED / STAGE_NO_PASS / STAGE_NO_VERDICT ตามลำดับ
     *         ถ้าทุกตัวขยับ คืน STAGE_HEALTHY */
    (void)before;
    (void)after;
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
    /* TODO 4: ตรวจตามลำดับนี้ แต่ละข้อมีความหมายเมื่อข้อก่อนหน้าถูกตัดทิ้งแล้วเท่านั้น
     *   calls == 0            -> LOAD_NEVER_RAN
     *   returns < calls       -> LOAD_STUCK
     *   last_rc == RC_NEVER_CALLED -> LOAD_NO_RC
     *   last_rc != 0          -> LOAD_REFUSED
     *   inits == 0            -> LOAD_ABANDONED
     *   นอกนั้น               -> LOAD_OK */
    (void)calls;
    (void)returns;
    (void)inits;
    (void)last_rc;
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
    (void)c;
    /* TODO 5 */
    *out = 0;            // โค้ดตั้งต้นนี้โกหก: คืนศูนย์แล้วบอกว่าสำเร็จ
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
