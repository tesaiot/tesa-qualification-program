// SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
// SPDX-License-Identifier: Apache-2.0
//
// examples/03_sensor_sample.c — struct ของข้อมูลเซนเซอร์หนึ่งชุด padding และการส่งด้วย pointer
//
//     gcc -std=c11 -Wall -Wextra -o sensor_sample 03_sensor_sample.c
//     ./sensor_sample
//
// ทายก่อนรัน: sizeof(imu_loose_t) เท่ากับเท่าไร (ลองบวกขนาดของสมาชิกทุกตัวดูก่อน)
#include <inttypes.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>

// ท่าที่ 1: struct เดียวกัน เรียงสมาชิกต่างกัน ขนาดไม่เท่ากัน
typedef struct {
    uint8_t  valid;      // 1 ไบต์ ตามด้วยช่องว่างเพื่อให้ t_ms อยู่ตรงขอบ 4 ไบต์
    uint32_t t_ms;
    int16_t  ax, ay, az; // ค่าดิบ มีเครื่องหมาย
    uint8_t  seq;
} imu_loose_t;

typedef struct {
    uint32_t t_ms;       // ตัวใหญ่ก่อน
    int16_t  ax, ay, az;
    uint8_t  valid;      // ตัวเล็กไว้ท้าย
    uint8_t  seq;
} imu_sample_t;

// ท่าที่ 2: อ่านอย่างเดียว -> const pointer; ต้องแก้ -> pointer ธรรมดา
static int32_t magnitude_sq(const imu_sample_t *s)
{
    // s->ax = 0;  // ถ้าเปิดบรรทัดนี้ คอมไพเลอร์จะไม่ยอม เพราะเราสัญญาว่าจะไม่แก้
    return (int32_t)s->ax * s->ax + (int32_t)s->ay * s->ay + (int32_t)s->az * s->az;
}

static void sample_fill(imu_sample_t *out, uint32_t now_ms, int16_t x, int16_t y, int16_t z)
{
    out->t_ms = now_ms;
    out->ax = x;
    out->ay = y;
    out->az = z;
    out->seq = (uint8_t)(out->seq + 1u);   // uint8_t วนกลับหลัง 255 ตั้งใจให้เป็นแบบนั้น
    out->valid = 1u;
}

// ส่งทั้ง struct แบบ by value: ได้สำเนา แก้สำเนาไม่กระทบตัวจริง และต้องคัดลอกทุกไบต์ลง stack
static void try_to_reset(imu_sample_t copy)
{
    copy.valid = 0u;
    printf("inside try_to_reset: copy.valid=%u\n", (unsigned)copy.valid);
}

int main(void)
{
    printf("sizeof(imu_loose_t)  = %zu (members add up to %zu)\n",
           sizeof(imu_loose_t), (size_t)(1 + 4 + 2 * 3 + 1));
    printf("  offsets: valid=%zu t_ms=%zu ax=%zu seq=%zu\n",
           offsetof(imu_loose_t, valid), offsetof(imu_loose_t, t_ms),
           offsetof(imu_loose_t, ax), offsetof(imu_loose_t, seq));
    printf("sizeof(imu_sample_t) = %zu\n", sizeof(imu_sample_t));

    imu_sample_t s = {0};                  // ท่าที่ 3: struct อยู่ใน stack ของ main ส่งที่อยู่ของมันต่อ
    sample_fill(&s, 1000u, 120, -35, 16384);
    printf("sample: t=%" PRIu32 " ms seq=%u |a|^2=%" PRId32 "\n",
           s.t_ms, (unsigned)s.seq, magnitude_sq(&s));

    try_to_reset(s);
    printf("after try_to_reset(copy): valid=%u (unchanged)\n", (unsigned)s.valid);
    return 0;
}
