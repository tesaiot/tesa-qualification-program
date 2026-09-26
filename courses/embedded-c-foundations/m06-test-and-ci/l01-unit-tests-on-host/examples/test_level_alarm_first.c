// SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
// SPDX-License-Identifier: Apache-2.0
//
// test_level_alarm_first.c — unit test สองข้อแรกของ level_alarm ด้วย Unity (ThrowTheSwitch v2.7.0)
//
// ต้องมีซอร์สของ Unity ก่อน (ไม่ได้แนบมากับหลักสูตรนี้):
//     git clone --depth 1 --branch v2.7.0 https://github.com/ThrowTheSwitch/Unity.git unity
//     make test                                   (หรือดูคำสั่ง gcc ใน Makefile)
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

// ท่าที่ 3: รันทุก test แล้วสรุป UNITY_END() คืนจำนวนที่ล้ม ใช้เป็น exit code ให้ make หรือ CI รู้ผล
int main(void)
{
    UNITY_BEGIN();
    RUN_TEST(test_stays_normal_below_threshold);
    RUN_TEST(test_read_failure_reports_fault);
    return UNITY_END();
}
