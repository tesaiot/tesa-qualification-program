// SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
// SPDX-License-Identifier: Apache-2.0
//
// practice/test_level_alarm.c — ฝึกเติม: เขียน unit test ให้ครบกรณีปกติ กรณีขอบ และกรณีผิดพลาด
//
// สองข้อแรกคัดมาจาก examples/test_level_alarm_first.c อีกสี่ข้อเป็นช่องให้เติม (มองหา TODO)
// ตอนนี้แต่ละข้อที่ยังไม่เขียนเรียก TEST_FAIL_MESSAGE จึงขึ้นสีแดง แทนที่ด้วย test จริงทีละข้อ
// รันจากโฟลเดอร์ examples:
//     make test TEST=../practice/test_level_alarm.c
// ลองเองก่อนอย่างน้อย 15 นาที แล้วค่อยเปิด solution/test_level_alarm.c
#include "level_alarm.h"
#include "unity.h"

// ---- ตัวปลอมของเซนเซอร์: คืนค่าจากตารางทีละค่า หรือจำลองการอ่านล้ม ----
typedef struct {
    const int32_t *values;
    unsigned       n;
    unsigned       next;
    int            fail; // ไม่ใช่ 0 = ทุกการอ่านล้ม
} fake_sensor_t;

static int fake_read(void *ctx, int32_t *out_mv)
{
    fake_sensor_t *f = (fake_sensor_t *)ctx;
    if (f->fail || f->next >= f->n) {
        return -1;
    }
    *out_mv = f->values[f->next++];
    return 0;
}

static fake_sensor_t  s_fake;
static level_sensor_t s_sensor = {fake_read, &s_fake};
static level_alarm_t  s_alarm;

// Unity ต้องการ setUp และ tearDown ในทุก test executable ที่ไม่ได้ใช้ test runner generator
void setUp(void)
{
    s_fake = (fake_sensor_t){0};
    level_alarm_init(&s_alarm, &s_sensor, 2000, 1500, 3u);
}

void tearDown(void)
{
}

// ท่าที่ 1: กรณีปกติ ค่าต่ำกว่าเกณฑ์ตลอด ต้องไม่แจ้งเตือน
static void test_stays_normal_below_threshold(void)
{
    static const int32_t v[] = {100, 900, 1999, 1200, 0};
    s_fake.values = v;
    s_fake.n = 5u;
    for (unsigned i = 0u; i < 5u; i++) {
        TEST_ASSERT_EQUAL_INT(ALARM_NORMAL, level_alarm_step(&s_alarm));
    }
}

// ท่าที่ 2: กรณีผิดพลาด อ่านเซนเซอร์ไม่ได้ ต้องได้ FAULT ไม่ใช่ NORMAL
static void test_read_failure_reports_fault(void)
{
    s_fake.fail = 1;
    TEST_ASSERT_EQUAL_INT(ALARM_FAULT, level_alarm_step(&s_alarm));
}

// กรณีขอบ: ค่าเท่ากับ on_mv พอดี (2000) ต้องนับว่าสูง และครบ confirm (3) ครั้งจึงเป็น ACTIVE
static void test_exact_threshold_counts(void)
{
    /* TODO 1: ป้อน 2000 สามครั้ง ตรวจว่าสองครั้งแรกยัง NORMAL และครั้งที่สามเป็น ACTIVE */
    TEST_FAIL_MESSAGE("TODO 1: write this test");
}

// กรณีขอบ: ค่าสูงต้องติดกัน ถ้าขาดหนึ่งครั้งต้องนับใหม่
static void test_needs_consecutive_readings(void)
{
    /* TODO 2: ป้อน 2000, 2000, 1999, 2000, 2000 แล้วตรวจว่ายัง NORMAL ทุกครั้ง
     *         จากนั้นป้อน 2000 อีกหนึ่งครั้ง (ครบสามครั้งติด) ต้องเป็น ACTIVE */
    TEST_FAIL_MESSAGE("TODO 2: write this test");
}

// hysteresis: เมื่อ ACTIVE แล้ว ค่าระหว่าง off_mv (1500) กับ on_mv ต้องยังคง ACTIVE
static void test_hysteresis_holds_active(void)
{
    /* TODO 3: ทำให้เป็น ACTIVE ก่อน แล้วป้อน 1600 สามครั้ง ต้องยัง ACTIVE
     *         จากนั้นป้อน 1400 สามครั้ง ครั้งที่สามต้องกลับเป็น NORMAL */
    TEST_FAIL_MESSAGE("TODO 3: write this test");
}

// กรณีผิดพลาดแล้วฟื้น: อ่านล้มได้ FAULT พออ่านได้อีกครั้งต้องกลับมาประเมินจาก NORMAL
static void test_recovers_after_fault(void)
{
    /* TODO 4: ตั้ง fail = 1 เรียกหนึ่งครั้ง (FAULT)
     *         แล้วตั้ง fail = 0 ใส่ค่า 100 หนึ่งค่า เรียกอีกครั้ง ต้องได้ NORMAL */
    TEST_FAIL_MESSAGE("TODO 4: write this test");
}

int main(void)
{
    UNITY_BEGIN();
    RUN_TEST(test_stays_normal_below_threshold);
    RUN_TEST(test_read_failure_reports_fault);
    RUN_TEST(test_exact_threshold_counts);
    RUN_TEST(test_needs_consecutive_readings);
    RUN_TEST(test_hysteresis_holds_active);
    RUN_TEST(test_recovers_after_fault);
    return UNITY_END();
}
