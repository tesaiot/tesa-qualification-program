// SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
// SPDX-License-Identifier: Apache-2.0
//
// solution/03_ring_buffer.c — เฉลยของ practice/03_ring_buffer.c
//
// กติกาของบัฟเฟอร์นี้
//   - ขนาด RB_CAPACITY เป็นกำลังของสอง จึงหาตำแหน่งด้วย (ตัวนับ & RB_MASK) แทนการหารเอาเศษ
//   - head กับ tail เป็นตัวนับที่เดินไปเรื่อย ๆ (ไม่รีเซ็ต) จำนวนข้อมูลคือ head - tail
//     ซึ่งถูกเสมอแม้ตัวนับจะวนกลับ เพราะการลบของ unsigned เป็น modulo (บทเรียน 1.1)
//   - ผู้เขียน (เช่น ISR) แก้ได้แค่ head ผู้อ่าน (เช่น task) แก้ได้แค่ tail
//   - เต็มแล้วต้อง "ปฏิเสธ" ไม่ใช่เขียนทับข้อมูลที่ยังไม่มีใครอ่าน
//
//     gcc -std=c11 -Wall -Wextra -o ring 03_ring_buffer.c && ./ring   -> PASS: 0 failure(s)
//
// atomic_thread_fence() มาจาก C11 <stdatomic.h> ใช้กั้นไม่ให้คอมไพเลอร์และ CPU สลับลำดับ
// "เขียนข้อมูล" กับ "เลื่อน head" บน Cortex-M ใน SDK ใช้ __DMB() ของ CMSIS ทำหน้าที่เดียวกัน
// (ดู radar_dsp.c ที่เขียน snapshot แล้ว __DMB() ก่อนประกาศเลขลำดับใหม่)
#include <stdatomic.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

#define RB_CAPACITY (16u)                 // ต้องเป็นกำลังของสอง
#define RB_MASK     (RB_CAPACITY - 1u)

typedef struct {
    uint8_t           data[RB_CAPACITY];
    volatile uint32_t head;               // จำนวนไบต์ที่เคยเขียน (ผู้เขียนเป็นเจ้าของ)
    volatile uint32_t tail;               // จำนวนไบต์ที่เคยอ่าน (ผู้อ่านเป็นเจ้าของ)
} ring_t;

// ให้มาแล้ว: เริ่มตัวนับที่ค่าใดก็ได้ (test จะเริ่มใกล้ UINT32_MAX เพื่อบังคับให้วนกลับ)
static void rb_init(ring_t *rb, uint32_t start)
{
    rb->head = start;
    rb->tail = start;
}

static uint32_t rb_count(const ring_t *rb)
{
    // ถูกแม้ head วนกลับผ่าน 0 แล้วแต่ tail ยังไม่วน เช่น 2 - 0xFFFFFFFE = 4 ใน uint32_t
    return rb->head - rb->tail;
}

static bool rb_is_empty(const ring_t *rb)
{
    return rb_count(rb) == 0u;
}

static bool rb_is_full(const ring_t *rb)
{
    return rb_count(rb) >= RB_CAPACITY;
}

// ผู้เขียน: เต็มแล้วคืน false และห้ามแตะ data หรือ head
static bool rb_push(ring_t *rb, uint8_t byte)
{
    if (rb_is_full(rb)) {
        return false;                                  // ปฏิเสธ ไม่เขียนทับของที่ยังไม่ถูกอ่าน
    }
    const uint32_t h = rb->head;                       // อ่าน head ครั้งเดียว (เราเป็นเจ้าของ ไม่มีใครแก้)
    rb->data[h & RB_MASK] = byte;                      // 1) เขียนข้อมูลก่อน
    atomic_thread_fence(memory_order_release);         // 2) ให้ข้อมูลถึงหน่วยความจำก่อน
    rb->head = h + 1u;                                 // 3) แล้วจึงประกาศว่ามีข้อมูลใหม่
    return true;
}

// ผู้อ่าน: ว่างแล้วคืน false
static bool rb_pop(ring_t *rb, uint8_t *out)
{
    if (rb_is_empty(rb)) {
        return false;
    }
    atomic_thread_fence(memory_order_acquire);         // เห็น head ใหม่แล้ว ข้อมูลที่ head ประกาศต้องเห็นด้วย
    const uint32_t t = rb->tail;
    *out = rb->data[t & RB_MASK];                      // 1) อ่านข้อมูลออกก่อน
    atomic_thread_fence(memory_order_release);
    rb->tail = t + 1u;                                 // 2) แล้วจึงคืนช่องให้ผู้เขียน
    return true;
}

static int failures = 0;
#define CHECK(cond)                                                    \
    do {                                                               \
        if (!(cond)) {                                                 \
            printf("FAIL line %d: %s\n", __LINE__, #cond);             \
            failures++;                                                \
        }                                                              \
    } while (0)

int main(void)
{
    static ring_t rb;
    uint8_t v = 0u;

    // กรณีปกติ: เข้าก่อนออกก่อน
    rb_init(&rb, 0u);
    CHECK(rb_is_empty(&rb));
    CHECK(rb_push(&rb, 0x11u) && rb_push(&rb, 0x22u));
    CHECK(rb_count(&rb) == 2u);
    CHECK(rb_pop(&rb, &v) && v == 0x11u);
    CHECK(rb_pop(&rb, &v) && v == 0x22u);
    CHECK(!rb_pop(&rb, &v));                       // ว่างแล้วต้องบอกว่าว่าง

    // กรณีขอบ: เต็มแล้วต้องปฏิเสธ และข้อมูลเก่าต้องไม่ถูกทับ
    for (unsigned i = 0u; i < RB_CAPACITY; i++) {
        CHECK(rb_push(&rb, (uint8_t)i));
    }
    CHECK(rb_is_full(&rb));
    CHECK(!rb_push(&rb, 0xEEu));                   // ไบต์ที่ 17 ต้องถูกปฏิเสธ
    CHECK(rb_pop(&rb, &v) && v == 0u);             // ไบต์แรกยังเป็น 0 ไม่ใช่ 0xEE

    // กรณีขอบ: ตัวนับวนกลับผ่าน UINT32_MAX ระหว่างทาง
    rb_init(&rb, UINT32_MAX - 3u);
    unsigned ok = 0u;
    for (unsigned round = 0u; round < 1000u; round++) {
        uint8_t in = (uint8_t)round, got = 0u;
        if (rb_push(&rb, in) && rb_pop(&rb, &got) && got == in) {
            ok++;
        }
    }
    CHECK(ok == 1000u);
    CHECK(rb_is_empty(&rb));

    printf("%s: %d failure(s)\n", failures ? "FAIL" : "PASS", failures);
    return failures ? 1 : 0;
}
