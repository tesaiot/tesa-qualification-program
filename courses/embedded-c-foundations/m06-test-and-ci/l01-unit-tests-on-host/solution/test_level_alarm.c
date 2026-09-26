// SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
// SPDX-License-Identifier: Apache-2.0
//
// solution/test_level_alarm.c — เฉลยของ practice/test_level_alarm.c
//
// รันจากโฟลเดอร์ examples:
//     make test TEST=../solution/test_level_alarm.c        -> 6 Tests 0 Failures 0 Ignored
// แล้วพิสูจน์ว่า test ล้มเป็น:
//     bash prove_red.sh ../solution/test_level_alarm.c <โฟลเดอร์ src ของ Unity>
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

static fake_sensor_t s_fake;

// ตัวช่วย: ป้อนค่าหนึ่งค่าแล้วก้าวหนึ่งครั้ง (ตัวปลอมอ่านจากตาราง one ที่มีค่าเดียว)
static alarm_state_t  step_with(level_alarm_t *a, int32_t mv);
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
    // ใช้ค่าเท่ากับเกณฑ์พอดี เพราะบั๊ก >= กลายเป็น > ซ่อนอยู่ตรงนี้เสมอ
    TEST_ASSERT_EQUAL_INT(ALARM_NORMAL, step_with(&s_alarm, 2000));
    TEST_ASSERT_EQUAL_INT(ALARM_NORMAL, step_with(&s_alarm, 2000));
    TEST_ASSERT_EQUAL_INT(ALARM_ACTIVE, step_with(&s_alarm, 2000));
}

// กรณีขอบ: ค่าสูงต้องติดกัน ถ้าขาดหนึ่งครั้งต้องนับใหม่
static void test_needs_consecutive_readings(void)
{
    static const int32_t v[] = {2000, 2000, 1999, 2000, 2000};
    for (unsigned i = 0u; i < 5u; i++) {
        TEST_ASSERT_EQUAL_INT(ALARM_NORMAL, step_with(&s_alarm, v[i]));
    }
    TEST_ASSERT_EQUAL_INT(ALARM_ACTIVE, step_with(&s_alarm, 2000));
}

// hysteresis: เมื่อ ACTIVE แล้ว ค่าระหว่าง off_mv (1500) กับ on_mv ต้องยังคง ACTIVE
static void test_hysteresis_holds_active(void)
{
    for (unsigned i = 0u; i < 3u; i++) {
        (void)step_with(&s_alarm, 2500);
    }
    // ตรวจเงื่อนไขตั้งต้นก่อน ไม่อย่างนั้นส่วนที่เหลือพิสูจน์อะไรไม่ได้
    TEST_ASSERT_EQUAL_INT(ALARM_ACTIVE, s_alarm.state);
    for (unsigned i = 0u; i < 3u; i++) {
        TEST_ASSERT_EQUAL_INT(ALARM_ACTIVE, step_with(&s_alarm, 1600));
    }
    TEST_ASSERT_EQUAL_INT(ALARM_ACTIVE, step_with(&s_alarm, 1400));
    TEST_ASSERT_EQUAL_INT(ALARM_ACTIVE, step_with(&s_alarm, 1400));
    TEST_ASSERT_EQUAL_INT(ALARM_NORMAL, step_with(&s_alarm, 1400));
}

// กรณีผิดพลาดแล้วฟื้น: อ่านล้มได้ FAULT พออ่านได้อีกครั้งต้องกลับมาประเมินจาก NORMAL
static void test_recovers_after_fault(void)
{
    s_fake.fail = 1;
    TEST_ASSERT_EQUAL_INT(ALARM_FAULT, level_alarm_step(&s_alarm));
    s_fake.fail = 0;
    TEST_ASSERT_EQUAL_INT(ALARM_NORMAL, step_with(&s_alarm, 100));
}

static alarm_state_t step_with(level_alarm_t *a, int32_t mv)
{
    static int32_t one;
    one = mv;
    s_fake.values = &one;
    s_fake.n = 1u;
    s_fake.next = 0u;
    return level_alarm_step(a);
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
