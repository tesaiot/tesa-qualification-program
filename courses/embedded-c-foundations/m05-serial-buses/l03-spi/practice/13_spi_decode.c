// SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
// SPDX-License-Identifier: Apache-2.0
//
// practice/13_spi_decode.c — ฝึกเติม: ตัวถอดรหัส SPI สี่สาย (SCLK, MOSI, MISO, CS) แบบที่ logic analyzer ทำ
//
// สัญญาณถูกสุ่มเป็นลำดับของ sample_t CS ทำงานที่ระดับต่ำ ข้อมูล MSB ก่อน
// ตัวถอดรหัสต้องรู้โหมด (CPOL, CPHA) จึงอ่านถูกขอบ ถ้าตั้งโหมดผิด จะได้ไบต์ที่เลื่อนหรือกลับข้าง
// นี่คือบทสุดท้ายของโมดูล 5 จึงเว้นว่างมากที่สุด: 6 จุด (มองหา TODO)
//     gcc -std=c11 -Wall -Wextra -o spi_decode 13_spi_decode.c && ./spi_decode
// ก่อนเติม test จะล้ม ลองเองก่อนอย่างน้อย 15 นาที แล้วค่อยเปิด solution/13_spi_decode.c
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

typedef struct {
    uint8_t cs, sclk, mosi, miso;
} sample_t;

// ถอดรหัสทุกไบต์ที่ครบ 8 บิตขณะ CS ต่ำ เก็บลง mosi_out และ miso_out คืนจำนวนไบต์
// ไบต์ที่ไม่ครบ 8 บิตตอน CS ขึ้นสูงให้ทิ้ง (เหมือนธุรกรรมที่ถูกตัดกลางคัน)
static unsigned spi_decode(const sample_t *s, unsigned n, unsigned mode,
                           uint8_t *mosi_out, uint8_t *miso_out, unsigned max)
{
    /* TODO 1: แยก cpol และ cpha จาก mode (mode = CPOL * 2 + CPHA) */
    const unsigned cpol = 0u;
    const unsigned cpha = 0u;
    (void)cpol;
    (void)cpha;
    (void)mode;

    unsigned count = 0u, bits = 0u;
    uint8_t mo = 0u, mi = 0u;

    for (unsigned i = 1u; i < n; i++) {
        /* TODO 2: ถ้า CS ไม่ได้ทำงาน (สูง) ให้ล้างตัวนับบิตและไบต์ที่กำลังประกอบ แล้วข้ามไปตัวอย่างถัดไป */

        const bool edge = (s[i].sclk != s[i - 1u].sclk);
        (void)edge;
        /* TODO 3: ขอบ "leading" คือขอบที่ SCLK ออกจากระดับว่าง (ค่าใหม่ != cpol)
         *         ขอบ "trailing" คือขอบที่กลับสู่ระดับว่าง */

        /* TODO 4: ผู้รับอ่านที่ leading ถ้า CPHA = 0 และที่ trailing ถ้า CPHA = 1
         *         ถ้าตัวอย่างนี้ไม่ใช่ขอบที่ต้องอ่าน ให้ข้ามไป */

        /* TODO 5: เลื่อนบิตของ MOSI และ MISO เข้าท้ายไบต์ (MSB ก่อน) แล้วนับบิต
         *         อ่านค่าจากตัวอย่าง "ก่อนขอบ" คือ s[i - 1] ซึ่งเป็นค่าที่นิ่งอยู่ก่อนขอบ แบบที่ flip-flop ของผู้รับจับได้จริง */

        /* TODO 6: ครบ 8 บิต เก็บทั้งสองไบต์ (ถ้ายังมีที่) นับไบต์ แล้วเริ่มไบต์ใหม่ */
    }
    (void)bits;
    (void)mo;
    (void)mi;
    (void)mosi_out;
    (void)miso_out;
    (void)max;
    return count;
}

// ---- ให้มาแล้ว: สร้างสัญญาณทดสอบของหนึ่งธุรกรรมในโหมดที่กำหนด ----
static unsigned make_trace(sample_t *s, unsigned mode, const uint8_t *tx, const uint8_t *rx, unsigned len)
{
    const uint8_t cpol = (uint8_t)((mode >> 1) & 1u), cpha = (uint8_t)(mode & 1u);
    unsigned n = 0u;
    for (unsigned k = 0u; k < 3u; k++) s[n++] = (sample_t){1u, cpol, 0u, 0u};      // ว่าง CS สูง
    s[n++] = (sample_t){0u, cpol, 0u, 0u};                                          // CS ลง
    for (unsigned b = 0u; b < len; b++) {
        for (int bit = 7; bit >= 0; bit--) {
            const uint8_t mo = (uint8_t)((tx[b] >> bit) & 1u), mi = (uint8_t)((rx[b] >> bit) & 1u);
            if (cpha == 0u) {   // ข้อมูลตั้งก่อนขอบแรก อ่านที่ขอบแรก
                s[n++] = (sample_t){0u, cpol, mo, mi};
                s[n++] = (sample_t){0u, (uint8_t)!cpol, mo, mi};
            } else {            // ข้อมูลเปลี่ยนที่ขอบแรก อ่านที่ขอบที่สอง
                s[n++] = (sample_t){0u, (uint8_t)!cpol, mo, mi};
                s[n++] = (sample_t){0u, cpol, mo, mi};
            }
        }
    }
    s[n++] = (sample_t){0u, cpol, 0u, 0u};
    for (unsigned k = 0u; k < 3u; k++) s[n++] = (sample_t){1u, cpol, 0u, 0u};      // CS ขึ้น แล้วว่าง
    return n;
}

static int failures = 0;
#define CHECK_EQ(expected, actual)                                                        \
    do {                                                                                  \
        long e_ = (long)(expected), a_ = (long)(actual);                                  \
        if (e_ != a_) {                                                                   \
            printf("FAIL line %d: %s expected %ld got %ld\n", __LINE__, #actual, e_, a_); \
            failures++;                                                                   \
        }                                                                                 \
    } while (0)

int main(void)
{
    static sample_t s[1024];
    uint8_t mo[16] = {0}, mi[16] = {0};

    // เฟรมที่ตัวอย่าง Header I/O Test ส่งตอนกด SPI ครั้งแรก (โหมด 0): A5 31 00 5A 01 02 03 แล้ว XOR checksum
    const uint8_t tx[8] = {0xA5u, 0x31u, 0x00u, 0x5Au, 0x01u, 0x02u, 0x03u, 0xCEu};
    const uint8_t rx[8] = {0xFFu, 0xFFu, 0xFFu, 0xFFu, 0xFFu, 0xFFu, 0xFFu, 0xFFu};  // สมมติ MISO ลอยสูง
    unsigned n = make_trace(s, 0u, tx, rx, 8u);
    CHECK_EQ(8, spi_decode(s, n, 0u, mo, mi, 16u));
    CHECK_EQ(0xA5, mo[0]);
    CHECK_EQ(0xCE, mo[7]);
    CHECK_EQ(0xFF, mi[0]);

    // โหมด 3 ทั้งสองทิศ
    const uint8_t t3[2] = {0x3Cu, 0x81u}, r3[2] = {0x24u, 0x7Eu};
    n = make_trace(s, 3u, t3, r3, 2u);
    CHECK_EQ(2, spi_decode(s, n, 3u, mo, mi, 16u));
    CHECK_EQ(0x3C, mo[0]);
    CHECK_EQ(0x7E, mi[1]);

    // ตั้งโหมดผิด (ส่งโหมด 1 แต่ถอดเป็นโหมด 0): ไบต์ที่ได้ต้องไม่ตรงกับที่ส่ง
    const uint8_t t1[1] = {0xA5u}, r1[1] = {0x00u};
    n = make_trace(s, 1u, t1, r1, 1u);
    CHECK_EQ(1, spi_decode(s, n, 1u, mo, mi, 16u));
    CHECK_EQ(0xA5, mo[0]);
    spi_decode(s, n, 0u, mo, mi, 16u);
    CHECK_EQ(1, mo[0] != 0xA5u);

    // ที่เก็บเล็ก: เก็บได้หนึ่งไบต์ แต่นับครบ และไม่เขียนเลยขอบ
    uint8_t small_mo[1] = {0}, small_mi[1] = {0};
    n = make_trace(s, 0u, tx, rx, 8u);
    CHECK_EQ(8, spi_decode(s, n, 0u, small_mo, small_mi, 1u));
    CHECK_EQ(0xA5, small_mo[0]);

    printf("%s: %d failure(s)\n", failures ? "FAIL" : "PASS", failures);
    return failures ? 1 : 0;
}
