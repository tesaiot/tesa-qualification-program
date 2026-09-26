// SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
// SPDX-License-Identifier: Apache-2.0
//
// practice/08_timer_math.c — ฝึกเติม: คำนวณค่าตั้ง timer และความคลาดเคลื่อนของ baud rate ด้วยเลขจำนวนเต็ม
//
// เขียนด้วยเลขจำนวนเต็มล้วนแบบที่เฟิร์มแวร์มักทำ (printf ของ CM33 ใน SDK ไม่มี float)
// กติกาของฮาร์ดแวร์ที่ใช้ในแบบฝึกนี้
//   - ตัวหาร 16 บิตรับค่า 0..65535 และหารด้วย (ค่า + 1) ตามเอกสารของ Cy_SysClk_PeriPclkSetDivider()
//   - timer นับขึ้นจาก 0 ถึง period รวม period + 1 จังหวะ และสมมติว่า period กว้าง 16 บิต (0..65535)
// มีช่องให้เติม 4 จุด (มองหา TODO)
//     gcc -std=c11 -Wall -Wextra -o timer_math 08_timer_math.c && ./timer_math
// ก่อนเติม test จะล้ม ลองเองก่อนอย่างน้อย 15 นาที แล้วค่อยเปิด solution/08_timer_math.c
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

#define SRC_HZ (100000000u)   // CLK_HF10 ของบอร์ดนี้ = 100 MHz

// ความถี่หลังตัวหาร (ปัดเศษทิ้ง)
static uint32_t divided_hz(uint32_t src_hz, uint32_t div_value)
{
    (void)src_hz;
    (void)div_value;
    /* TODO 1 */
    return 0u;
}

// เวลาต่อหนึ่งรอบของ timer เป็นไมโครวินาที: (period + 1) / clk
// ระวัง: (period + 1) * 1000000 ล้น 32 บิตได้ ใช้ตัวกลาง 64 บิต (บทเรียน 1.1)
static uint32_t overflow_us(uint32_t clk_hz, uint32_t period)
{
    (void)clk_hz;
    (void)period;
    /* TODO 2 */
    return 0u;
}

// หา divider ที่เล็กที่สุด (ความละเอียดสูงสุด) ที่ทำให้ได้ช่วงเวลา interval_us พอดีเป๊ะ
// เงื่อนไข: src หารด้วย (div + 1) ลงตัว, จำนวนจังหวะ = clk * interval_us / 1000000 เป็นจำนวนเต็ม
//           และอยู่ระหว่าง 1 ถึง 65536 จากนั้น period = จำนวนจังหวะ - 1
// หาไม่ได้ให้คืน false และไม่แตะ *div_value, *period
static bool pick_timer(uint32_t src_hz, uint32_t interval_us, uint32_t *div_value, uint32_t *period)
{
    (void)src_hz;
    (void)interval_us;
    (void)div_value;
    (void)period;
    /* TODO 3: วน div ตั้งแต่ 0 ถึง 65535 แล้วคืนตัวแรกที่ผ่านเงื่อนไข */
    return false;
}

// ความคลาดเคลื่อนของ baud rate เป็นส่วนในล้าน (ppm): (จริง - เป้า) * 1000000 / เป้า
// baud จริง = src / (div + 1) / oversample (ปัดเศษทิ้งทุกขั้นตามลำดับนี้)
static int32_t baud_error_ppm(uint32_t src_hz, uint32_t div_value, uint32_t oversample, uint32_t target)
{
    (void)src_hz;
    (void)div_value;
    (void)oversample;
    (void)target;
    /* TODO 4 */
    return 0;
}

static int failures = 0;
#define CHECK_EQ(expected, actual)                                                        \
    do {                                                                                  \
        long long e_ = (long long)(expected), a_ = (long long)(actual);                   \
        if (e_ != a_) {                                                                   \
            printf("FAIL line %d: %s expected %lld got %lld\n", __LINE__, #actual, e_, a_); \
            failures++;                                                                   \
        }                                                                                 \
    } while (0)

int main(void)
{
    // ค่าจริงจาก BSP ของ SDK
    CHECK_EQ(10000, divided_hz(SRC_HZ, 9999u));             // GENERAL_PURPOSE_TIMER
    CHECK_EQ(2000, divided_hz(SRC_HZ, 49999u));             // PWM_LED_CTRL
    CHECK_EQ(1000000, overflow_us(10000u, 9999u));          // 1 วินาทีพอดี
    CHECK_EQ(1000500, overflow_us(2000u, 2000u));           // period0 = 2000 ที่ 2 kHz

    // เลือกค่าเอง
    uint32_t div = 0u, per = 0u;
    CHECK_EQ(1, pick_timer(SRC_HZ, 1000u, &div, &per));     // 1 ms
    CHECK_EQ(1, div);
    CHECK_EQ(49999, per);
    CHECK_EQ(1, pick_timer(SRC_HZ, 1000000u, &div, &per));  // 1 s
    CHECK_EQ(1599, div);
    CHECK_EQ(62499, per);
    div = 7u;
    per = 7u;
    CHECK_EQ(0, pick_timer(SRC_HZ, 100000000u, &div, &per)); // 100 s: เป็นไปไม่ได้ด้วยตัวหารและ period 16 บิต
    CHECK_EQ(7, div);
    CHECK_EQ(7, per);

    // DEBUG_UART ของ BSP: divider 86, oversample 10, เป้า 115200
    CHECK_EQ(-2239, baud_error_ppm(SRC_HZ, 86u, 10u, 115200u));

    printf("%s: %d failure(s)\n", failures ? "FAIL" : "PASS", failures);
    return failures ? 1 : 0;
}
