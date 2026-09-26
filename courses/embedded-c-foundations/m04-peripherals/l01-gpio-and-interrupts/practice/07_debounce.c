// SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
// SPDX-License-Identifier: Apache-2.0
//
// practice/07_debounce.c — ฝึกเติม: ตัวกันเด้งแบบไม่บล็อกที่ต้องผ่าน test สี่กรณี
//
// กติกา: เรียก debounce_step() หนึ่งครั้งต่อการอ่านขาหนึ่งครั้ง (เช่นทุก 10 ms) ห้ามมี delay หรือการรอข้างใน
// สถานะที่เชื่อ (stable) เปลี่ยนเมื่ออ่านได้ค่าใหม่ตรงกัน DEBOUNCE_POLLS ครั้งติดกันเท่านั้น
// มีช่องให้เติม 3 จุด (มองหา TODO)
//     gcc -std=c11 -Wall -Wextra -o debounce 07_debounce.c && ./debounce
// ก่อนเติม test จะล้ม ลองเองก่อนอย่างน้อย 15 นาที แล้วค่อยเปิด solution/07_debounce.c
#include <stdbool.h>
#include <stdio.h>

#define DEBOUNCE_POLLS (3u)

typedef enum { EV_NONE, EV_PRESS, EV_RELEASE } event_t;

typedef struct {
    bool     stable;   // สถานะที่เชื่อแล้ว (true = กด)
    bool     cand;     // สถานะที่กำลังนับ
    unsigned agree;    // อ่านได้ cand ต่อเนื่องกี่ครั้ง
} debounce_t;

static event_t debounce_step(debounce_t *d, bool pressed_now)
{
    if (pressed_now == d->cand) {
        /* TODO 1: ค่าเดิมซ้ำ เพิ่ม agree แต่ไม่ให้เกิน DEBOUNCE_POLLS (กันตัวเลขวนกลับเมื่อกดค้างนาน) */
    } else {
        /* TODO 2: ค่าเปลี่ยน เริ่มนับใหม่ที่ค่าใหม่ (การอ่านครั้งนี้นับเป็นครั้งที่ 1) */
    }
    /* TODO 3: ถ้าตรงกันครบ DEBOUNCE_POLLS ครั้ง และต่างจาก stable
     *         ให้ปรับ stable แล้วคืน EV_PRESS หรือ EV_RELEASE ตามสถานะใหม่ */
    return EV_NONE;
}

// ให้มาแล้ว: ป้อนลำดับค่าดิบเข้าไปทีละตัว แล้วนับเหตุการณ์ที่ได้
static void feed(debounce_t *d, const char *levels, unsigned *presses, unsigned *releases)
{
    for (const char *p = levels; *p != '\0'; p++) {
        const event_t ev = debounce_step(d, *p == '1');
        if (ev == EV_PRESS) {
            (*presses)++;
        } else if (ev == EV_RELEASE) {
            (*releases)++;
        }
    }
}

static int failures = 0;
#define CHECK_EQ(expected, actual)                                                       \
    do {                                                                                 \
        unsigned e_ = (expected), a_ = (actual);                                         \
        if (e_ != a_) {                                                                  \
            printf("FAIL line %d: %s expected %u got %u\n", __LINE__, #actual, e_, a_);  \
            failures++;                                                                  \
        }                                                                                \
    } while (0)

int main(void)
{
    unsigned pr, rl;
    debounce_t d;

    // กรณีปกติ: กดสะอาด ๆ แล้วปล่อย
    d = (debounce_t){false, false, 0u};
    pr = rl = 0u;
    feed(&d, "000111111000000", &pr, &rl);
    CHECK_EQ(1u, pr);
    CHECK_EQ(1u, rl);

    // กรณีเด้ง: กดครั้งเดียวที่เด้งหลายรอบ ต้องนับหนึ่ง
    d = (debounce_t){false, false, 0u};
    pr = rl = 0u;
    feed(&d, "0001011011111111110111101000000", &pr, &rl);
    CHECK_EQ(1u, pr);
    CHECK_EQ(1u, rl);

    // กรณีขอบ: สัญญาณรบกวนสั้นกว่า DEBOUNCE_POLLS ต้องไม่เป็นการกด
    d = (debounce_t){false, false, 0u};
    pr = rl = 0u;
    feed(&d, "000110000100000", &pr, &rl);
    CHECK_EQ(0u, pr);

    // กรณีขอบ: กดค้างนานมาก ต้องนับหนึ่ง และ agree ต้องไม่วิ่งเกิน DEBOUNCE_POLLS
    d = (debounce_t){false, false, 0u};
    pr = rl = 0u;
    for (unsigned i = 0u; i < 100000u; i++) {
        if (debounce_step(&d, true) == EV_PRESS) {
            pr++;
        }
    }
    CHECK_EQ(1u, pr);
    CHECK_EQ(DEBOUNCE_POLLS, d.agree);

    printf("%s: %d failure(s)\n", failures ? "FAIL" : "PASS", failures);
    return failures ? 1 : 0;
}
