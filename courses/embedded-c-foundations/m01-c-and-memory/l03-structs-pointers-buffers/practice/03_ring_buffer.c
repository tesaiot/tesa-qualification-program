// SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
// SPDX-License-Identifier: Apache-2.0
//
// practice/03_ring_buffer.c — ฝึกเติม: บัฟเฟอร์วงแหวนขนาดคงที่ ผู้เขียนหนึ่ง ผู้อ่านหนึ่ง (SPSC)
//
// กติกาของบัฟเฟอร์นี้
//   - ขนาด RB_CAPACITY เป็นกำลังของสอง จึงหาตำแหน่งด้วย (ตัวนับ & RB_MASK) แทนการหารเอาเศษ
//   - head กับ tail เป็นตัวนับที่เดินไปเรื่อย ๆ (ไม่รีเซ็ต) จำนวนข้อมูลคือ head - tail
//     ซึ่งถูกเสมอแม้ตัวนับจะวนกลับ เพราะการลบของ unsigned เป็น modulo (บทเรียน 1.1)
//   - ผู้เขียน (เช่น ISR) แก้ได้แค่ head ผู้อ่าน (เช่น task) แก้ได้แค่ tail
//   - เต็มแล้วต้อง "ปฏิเสธ" ไม่ใช่เขียนทับข้อมูลที่ยังไม่มีใครอ่าน
//
// มีช่องให้เติม 5 จุด (มองหา TODO) คอมไพล์และรัน:
//     gcc -std=c11 -Wall -Wextra -o ring 03_ring_buffer.c && ./ring
// ก่อนเติม test จะล้ม ลองเองก่อนอย่างน้อย 15 นาที แล้วค่อยเปิด solution/03_ring_buffer.c
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
    (void)rb;
    /* TODO 1: จำนวนไบต์ที่ยังไม่ถูกอ่าน (หนึ่งบรรทัด) */
    return 0u;
}

static bool rb_is_empty(const ring_t *rb)
{
    (void)rb;
    /* TODO 2 */
    return false;
}

static bool rb_is_full(const ring_t *rb)
{
    (void)rb;
    /* TODO 3 */
    return false;
}

// ผู้เขียน: เต็มแล้วคืน false และห้ามแตะ data หรือ head
static bool rb_push(ring_t *rb, uint8_t byte)
{
    (void)rb;
    (void)byte;
    /* TODO 4: ตรวจว่าเต็ม -> เขียนข้อมูลลงช่อง (head & RB_MASK) -> แล้วจึงเลื่อน head
     *         ลำดับสำคัญ: ถ้าเลื่อน head ก่อนเขียนข้อมูล ผู้อ่านอาจอ่านช่องที่ยังว่าง */
    return false;
}

// ผู้อ่าน: ว่างแล้วคืน false
static bool rb_pop(ring_t *rb, uint8_t *out)
{
    (void)rb;
    (void)out;
    /* TODO 5: ตรวจว่าว่าง -> อ่านจากช่อง (tail & RB_MASK) -> แล้วจึงเลื่อน tail */
    return false;
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
