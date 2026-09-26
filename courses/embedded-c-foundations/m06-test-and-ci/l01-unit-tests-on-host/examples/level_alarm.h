// SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
// SPDX-License-Identifier: Apache-2.0
//
// level_alarm.h — state machine แจ้งเตือนระดับ (เช่น แรงดันจากโพเทนชิโอมิเตอร์หรือเซนเซอร์ระดับน้ำ)
//
// ตรรกะทั้งหมดอยู่ใน level_alarm.c ซึ่งไม่แตะฮาร์ดแวร์เลย การอ่านค่าผ่าน "ตะเข็บ" (seam) คือ struct ของ
// function pointer แบบเดียวกับ arduino_ops_t ใน arduino_shield ของ SDK บนบอร์ดเราใส่ฟังก์ชันที่เรียก PDL
// บนคอมพิวเตอร์เราใส่ฟังก์ชันปลอมที่คืนค่าที่ test กำหนด
#ifndef LEVEL_ALARM_H
#define LEVEL_ALARM_H

#include <stdint.h>

typedef struct {
    // คืน 0 เมื่ออ่านสำเร็จ ค่าอื่นคืออ่านไม่ได้
    int (*read_mv)(void *ctx, int32_t *out_mv);
    void *ctx;
} level_sensor_t;

typedef enum { ALARM_NORMAL, ALARM_ACTIVE, ALARM_FAULT } alarm_state_t;

typedef struct {
    // on_mv: ค่าตั้งแต่นี้ขึ้นไปนับว่า "สูง"
    // off_mv: ต่ำกว่านี้นับว่า "กลับปกติ" (off_mv < on_mv คือ hysteresis)
    // confirm: ต้องเห็นติดกันกี่ครั้งจึงเปลี่ยนสถานะ
    const level_sensor_t *sensor;
    int32_t               on_mv;
    int32_t               off_mv;
    unsigned              confirm;
    unsigned              count;
    alarm_state_t         state;
} level_alarm_t;

void level_alarm_init(level_alarm_t *a, const level_sensor_t *sensor, int32_t on_mv, int32_t off_mv,
                      unsigned confirm);

// อ่านหนึ่งครั้ง ปรับสถานะ แล้วคืนสถานะใหม่
alarm_state_t level_alarm_step(level_alarm_t *a);

#endif
