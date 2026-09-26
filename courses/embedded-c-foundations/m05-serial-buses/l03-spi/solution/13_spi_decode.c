// SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
// SPDX-License-Identifier: Apache-2.0
//
// solution/13_spi_decode.c — เฉลยของ practice/13_spi_decode.c
//
// สัญญาณถูกสุ่มเป็นลำดับของ sample_t CS ทำงานที่ระดับต่ำ ข้อมูล MSB ก่อน
// ตัวถอดรหัสต้องรู้โหมด (CPOL, CPHA) จึงอ่านถูกขอบ ถ้าตั้งโหมดผิด จะได้ไบต์ที่เลื่อนหรือกลับข้าง
//     gcc -std=c11 -Wall -Wextra -o spi_decode 13_spi_decode.c && ./spi_decode   -> PASS: 0 failure(s)
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
    const unsigned cpol = (mode >> 1) & 1u;   // โหมด 2 และ 3: SCLK ว่างที่ระดับสูง
    const unsigned cpha = mode & 1u;          // โหมด 1 และ 3: อ่านที่ขอบที่สอง

    unsigned count = 0u, bits = 0u;
    uint8_t mo = 0u, mi = 0u;

    for (unsigned i = 1u; i < n; i++) {
        if (s[i].cs != 0u) {
            // CS สูง = ไม่มีธุรกรรม และไบต์ที่ค้างครึ่งตัวถือว่าถูกตัด ห้ามนำไปต่อกับธุรกรรมถัดไป
            bits = 0u;
            mo = mi = 0u;
            continue;
        }
        if (s[i].sclk == s[i - 1u].sclk) {
            continue;                                   // ไม่ใช่ขอบ
        }
        const bool leading = (s[i].sclk != cpol);       // ออกจากระดับว่าง
        const bool sample_here = (cpha == 0u) ? leading : !leading;
        if (!sample_here) {
            continue;
        }
        // ค่าที่ผู้รับจับได้คือค่าที่นิ่งอยู่ก่อนขอบ ถ้าอีกฝั่งเปลี่ยนข้อมูลตรงขอบนี้พอดี (ตั้งโหมดผิด) จะได้บิตของรอบก่อน
        mo = (uint8_t)((mo << 1) | (s[i - 1u].mosi & 1u));
        mi = (uint8_t)((mi << 1) | (s[i - 1u].miso & 1u));
        if (++bits == 8u) {
            if (count < max) {
                mosi_out[count] = mo;
                miso_out[count] = mi;
            }
            count++;                                    // นับทุกไบต์ แม้ที่เก็บเต็ม ผู้เรียกจะรู้ว่าตกหล่นไปเท่าไร
            bits = 0u;
            mo = mi = 0u;
        }
    }
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
