// SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
// SPDX-License-Identifier: Apache-2.0
//
// solution/01_bitops.c — เฉลยของ practice/01_bitops.c
//
//     gcc -std=c11 -Wall -Wextra -o bitops 01_bitops.c && ./bitops    -> PASS: 0 failure(s)
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>

static int failures = 0;
#define CHECK_EQ(expected, actual)                                                  \
    do {                                                                            \
        uint32_t e_ = (expected), a_ = (actual);                                    \
        if (e_ != a_) {                                                             \
            printf("FAIL line %d: expected 0x%08" PRIX32 " got 0x%08" PRIX32 "\n",  \
                   __LINE__, e_, a_);                                               \
            failures++;                                                             \
        }                                                                           \
    } while (0)

// ตั้งบิตทุกบิตที่เป็น 1 ใน mask ให้เป็น 1 บิตอื่นต้องไม่เปลี่ยน
static void bits_set(volatile uint32_t *reg, uint32_t mask)
{
    // |= คือ read-modify-write ในบรรทัดเดียว: อ่าน *reg, OR กับ mask, เขียนกลับ
    // บิตที่เป็น 0 ใน mask ไม่เปลี่ยน เพราะ x | 0 == x
    *reg |= mask;
}

// ล้างบิตทุกบิตที่เป็น 1 ใน mask ให้เป็น 0 บิตอื่นต้องไม่เปลี่ยน
static void bits_clear(volatile uint32_t *reg, uint32_t mask)
{
    // ~mask มี 0 ตรงบิตที่จะล้าง และ 1 ตรงบิตอื่น เพราะ x & 1 == x บิตอื่นจึงไม่เปลี่ยน
    // เขียน *reg = mask หรือ *reg &= mask ตรง ๆ คือบั๊กที่พบบ่อย มันลบบิตของคนอื่นทิ้ง
    *reg &= ~mask;
}

// ให้มาแล้ว: สลับบิต
static void bits_toggle(volatile uint32_t *reg, uint32_t mask)
{
    *reg ^= mask;
}

// ให้มาแล้ว: เขียนฟิลด์หลายบิต (ล้างก่อน แล้วใส่ค่าใหม่) ด้วยการอ่านหนึ่งครั้งและเขียนหนึ่งครั้ง
static void field_write(volatile uint32_t *reg, uint32_t msk, uint32_t pos, uint32_t value)
{
    uint32_t v = *reg;
    v &= ~msk;
    v |= (value << pos) & msk;
    *reg = v;
}

int main(void)
{
    volatile uint32_t reg = 0x000000F0u;

    bits_set(&reg, 0x00000001u);
    CHECK_EQ(0x000000F1u, reg);            // bit 0 ติด บิตอื่นเหมือนเดิม

    bits_clear(&reg, 0x00000030u);
    CHECK_EQ(0x000000C1u, reg);            // bit 4 และ 5 ดับ

    bits_set(&reg, 0x00000001u);
    CHECK_EQ(0x000000C1u, reg);            // ตั้งบิตที่ตั้งอยู่แล้วต้องไม่เปลี่ยนอะไร

    bits_toggle(&reg, 0x80000000u);
    CHECK_EQ(0x800000C1u, reg);

    field_write(&reg, 0x00000700u, 8u, 5u);
    CHECK_EQ(0x800005C1u, reg);

    field_write(&reg, 0x00000700u, 8u, 9u); // 9 ไม่พอดีฟิลด์ 3 บิต mask ตัดเหลือ 1
    CHECK_EQ(0x800001C1u, reg);

    printf("%s: %d failure(s)\n", failures ? "FAIL" : "PASS", failures);
    return failures ? 1 : 0;
}
