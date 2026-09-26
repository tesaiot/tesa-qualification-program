// SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
// SPDX-License-Identifier: Apache-2.0
//
// examples/07_debounce_trace.c — กันเด้งปุ่มแบบไม่บล็อก ด้วยการนับการอ่านที่ตรงกันต่อเนื่อง
//
// ตรรกะเดียวกับ 04_gpio_led_button.c ของ SDK (อ่านทุก 10 ms เชื่อเมื่อค่าตรงกัน 3 ครั้งติด = 30 ms)
// แต่ป้อนค่าจากตารางที่จำลองการเด้งของหน้าสัมผัส แทนการอ่านขาจริง จึงรันบนคอมพิวเตอร์ได้
//
//     gcc -std=c11 -Wall -Wextra -o debounce_trace 07_debounce_trace.c
//     ./debounce_trace
//
// ทายก่อนรัน: ถ้านับทุกครั้งที่ค่าดิบเปลี่ยนจากปล่อยเป็นกด จะได้กี่ครั้ง และแบบกันเด้งได้กี่ครั้ง
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

#define POLL_MS         (10u)
#define DEBOUNCE_POLLS  (3u)

typedef enum { EV_NONE, EV_PRESS, EV_RELEASE } event_t;

typedef struct {
    bool     stable;   // สถานะที่เชื่อแล้ว (true = กด)
    bool     cand;     // สถานะที่กำลังนับอยู่
    unsigned agree;    // อ่านได้ cand ต่อเนื่องกี่ครั้งแล้ว
} debounce_t;

// ท่าที่ 2: หนึ่งการอ่าน หนึ่งการเรียก ไม่มีการรอ ไม่มี delay ข้างใน
// เรียกจาก task ทุก POLL_MS (หรือจาก timer) แล้วคืนเหตุการณ์ถ้าสถานะที่เชื่อเปลี่ยน
static event_t debounce_step(debounce_t *d, bool pressed_now)
{
    if (pressed_now == d->cand) {
        if (d->agree < DEBOUNCE_POLLS) {
            d->agree++;
        }
    } else {
        d->cand = pressed_now;      // ค่าเปลี่ยน: เริ่มนับใหม่
        d->agree = 1u;
    }
    if (d->agree >= DEBOUNCE_POLLS && d->cand != d->stable) {
        d->stable = d->cand;
        return d->stable ? EV_PRESS : EV_RELEASE;
    }
    return EV_NONE;
}

int main(void)
{
    // ท่าที่ 1: ค่าดิบที่อ่านทุก 10 ms (1 = กด) กดหนึ่งครั้ง มีการเด้งตอนกดลงและตอนปล่อย และมีสัญญาณรบกวนสั้น ๆ หนึ่งครั้ง
    static const uint8_t raw[] = {
        0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1,   // กดลงแบบเด้ง
        1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,   // ปล่อยแบบเด้ง
        0, 0, 1, 0, 0, 0, 0, 0,                           // สัญญาณรบกวนหนึ่งการอ่าน
    };
    const unsigned n = (unsigned)(sizeof(raw) / sizeof(raw[0]));

    debounce_t d = {false, false, 0u};
    unsigned raw_edges = 0u, presses = 0u;
    bool prev_raw = false;

    // ท่าที่ 3: เทียบ "นับค่าดิบ" กับ "นับแบบกันเด้ง" บนข้อมูลชุดเดียวกัน
    for (unsigned t = 0u; t < n; t++) {
        const bool now = (raw[t] != 0u);
        if (now && !prev_raw) {
            raw_edges++;
        }
        prev_raw = now;

        const event_t ev = debounce_step(&d, now);
        if (ev == EV_PRESS) {
            presses++;
            printf("t=%3u ms  PRESS\n", t * POLL_MS);
        } else if (ev == EV_RELEASE) {
            printf("t=%3u ms  RELEASE\n", t * POLL_MS);
        }
    }
    printf("raw rising edges = %u, debounced presses = %u\n", raw_edges, presses);
    return 0;
}
