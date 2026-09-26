// SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
// SPDX-License-Identifier: Apache-2.0
//
// examples/09_watchdog_sim.c — ป้อน watchdog ที่ไหนถึงจะจับการค้างได้จริง จำลองบนคอมพิวเตอร์
//
// ระบบจำลองมี 3 task และ watchdog ที่รีเซ็ตเมื่อไม่ถูกป้อนเกิน WDT_TIMEOUT_TICKS
// ที่ tick 40 task "sensor" ค้าง แล้วเราดูว่ากลยุทธ์การป้อนสองแบบตอบสนองอย่างไร
//   A: ป้อนใน ISR ของ timer ทุก tick (กับดัก)
//   B: ผู้ดูแล (supervisor) ป้อนเฉพาะเมื่อทุก task รายงานความคืบหน้าครบในรอบนั้น
//
//     gcc -std=c11 -Wall -Wextra -o watchdog_sim 09_watchdog_sim.c
//     ./watchdog_sim
//
// ทายก่อนรัน: กลยุทธ์ A จะรีเซ็ตระบบที่ tick ไหน
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

#define N_TASKS            (3u)
#define ALL_TASKS          ((1u << N_TASKS) - 1u)
#define WDT_TIMEOUT_TICKS  (10u)
#define HANG_AT_TICK       (40u)
#define SIM_TICKS          (100u)

static const char *const k_names[N_TASKS] = {"sensor", "comms", "ui"};

typedef enum { FEED_IN_TIMER_ISR, FEED_BY_SUPERVISOR } strategy_t;

static void run(strategy_t s)
{
    uint32_t checkin = 0u;          // บิตละหนึ่ง task: "รอบนี้ฉันทำงานคืบหน้าแล้ว"
    uint32_t since_feed = 0u;       // ตัวนับของ watchdog จำลอง

    for (uint32_t tick = 1u; tick <= SIM_TICKS; tick++) {
        // ท่าที่ 1: แต่ละ task ทำงานหนึ่งรอบ แล้ว check in (task sensor ค้างตั้งแต่ HANG_AT_TICK)
        for (uint32_t t = 0u; t < N_TASKS; t++) {
            const bool hung = (t == 0u) && (tick >= HANG_AT_TICK);
            if (!hung) {
                checkin |= (1u << t);
            }
        }

        // ท่าที่ 2: ใครเป็นคนป้อน
        if (s == FEED_IN_TIMER_ISR) {
            since_feed = 0u;        // ISR ของ timer ยังทำงานแม้ทุก task ตายหมด จึงป้อนเสมอ
        } else if (checkin == ALL_TASKS) {
            since_feed = 0u;        // ป้อนเมื่อพิสูจน์ได้ว่าทุก task คืบหน้า
            checkin = 0u;           // แล้วล้าง ให้แต่ละ task ต้องพิสูจน์ใหม่ในรอบหน้า
        }

        // ท่าที่ 3: watchdog นับต่อ ถ้าเกินเวลาคือรีเซ็ต
        if (++since_feed > WDT_TIMEOUT_TICKS) {
            printf("  tick %3u: WATCHDOG RESET (missing check-in from:", (unsigned)tick);
            for (uint32_t t = 0u; t < N_TASKS; t++) {
                if ((checkin & (1u << t)) == 0u) {
                    printf(" %s", k_names[t]);
                }
            }
            printf(")\n");
            return;
        }
    }
    printf("  ran %u ticks with no reset, although task 'sensor' hung at tick %u\n",
           (unsigned)SIM_TICKS, (unsigned)HANG_AT_TICK);
}

int main(void)
{
    printf("strategy A: feed from a timer ISR\n");
    run(FEED_IN_TIMER_ISR);
    printf("strategy B: supervisor feeds only when every task checked in\n");
    run(FEED_BY_SUPERVISOR);
    return 0;
}
