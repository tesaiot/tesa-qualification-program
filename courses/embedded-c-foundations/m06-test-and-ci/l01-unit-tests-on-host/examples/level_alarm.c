// SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
// SPDX-License-Identifier: Apache-2.0
//
// level_alarm.c — ตรรกะล้วน คอมไพล์ได้ทั้งบนคอมพิวเตอร์และบนบอร์ด ไม่มี #include ของ PDL หรือ FreeRTOS
#include "level_alarm.h"

void level_alarm_init(level_alarm_t *a, const level_sensor_t *sensor, int32_t on_mv, int32_t off_mv,
                      unsigned confirm)
{
    a->sensor = sensor;
    a->on_mv = on_mv;
    a->off_mv = off_mv;
    a->confirm = (confirm == 0u) ? 1u : confirm;
    a->count = 0u;
    a->state = ALARM_NORMAL;
}

alarm_state_t level_alarm_step(level_alarm_t *a)
{
    int32_t mv = 0;
    if (a->sensor == 0 || a->sensor->read_mv(a->sensor->ctx, &mv) != 0) {
        a->state = ALARM_FAULT; // อ่านไม่ได้ต้องบอกว่าอ่านไม่ได้ ไม่ใช่ถือว่าปกติ
        a->count = 0u;
        return a->state;
    }
    if (a->state == ALARM_FAULT) {
        a->state = ALARM_NORMAL; // อ่านได้อีกครั้ง เริ่มประเมินใหม่จากปกติ
    }

    const int beyond = (a->state == ALARM_NORMAL) ? (mv >= a->on_mv) : (mv < a->off_mv);
    if (beyond) {
        a->count++;
        if (a->count >= a->confirm) {
            a->state = (a->state == ALARM_NORMAL) ? ALARM_ACTIVE : ALARM_NORMAL;
            a->count = 0u;
        }
    } else {
        a->count = 0u; // ต้องติดกัน ขาดหนึ่งครั้งเริ่มนับใหม่
    }
    return a->state;
}
