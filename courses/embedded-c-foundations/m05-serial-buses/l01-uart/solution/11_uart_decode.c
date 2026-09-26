// SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
// SPDX-License-Identifier: Apache-2.0
//
// solution/11_uart_decode.c — เฉลยของ practice/11_uart_decode.c
//
// สัญญาณถูกสุ่มที่ SPB ตัวอย่างต่อบิต (samples per bit) หา start bit จากขอบขาลงแรก
// แล้วอ่านค่า "กลางบิต" ของแต่ละบิต กลางบิตคือจุดที่ไกลจากขอบที่สุด จึงทนความคลาดของ baud ได้มากที่สุด
//     gcc -std=c11 -Wall -Wextra -o uart_decode 11_uart_decode.c && ./uart_decode   -> PASS: 0 failure(s)
#include <stdint.h>
#include <stdio.h>
#include <string.h>

typedef enum { PARITY_NONE, PARITY_EVEN, PARITY_ODD } parity_t;
enum { UART_OK = 0, UART_NO_START = -1, UART_PARITY_ERROR = -2, UART_FRAMING_ERROR = -3 };

#define SPB (8u)   // samples per bit

// ถอดรหัสหนึ่งเฟรมแบบ 8 data bit, 1 stop bit คืน UART_OK และเขียน *out หรือคืนรหัสผิดพลาด
static int uart_decode(const uint8_t *s, unsigned n, parity_t parity, uint8_t *out)
{
    // หาขอบขาลงแรก (สายว่างเป็น 1 start bit เป็น 0) ให้มาแล้ว
    unsigned k = 1u;
    while (k < n && !(s[k - 1u] == 1u && s[k] == 0u)) {
        k++;
    }
    if (k >= n) {
        return UART_NO_START;
    }
    const unsigned mid0 = k + SPB / 2u;            // กลางของ start bit
    if (mid0 >= n || s[mid0] != 0u) {
        return UART_NO_START;                      // แค่สัญญาณรบกวนสั้น ๆ ไม่ใช่ start bit
    }

    uint8_t byte = 0u;
    unsigned ones = 0u;
    for (unsigned i = 0u; i < 8u; i++) {
        const unsigned at = mid0 + (i + 1u) * SPB;
        if (at >= n) {
            return UART_FRAMING_ERROR;             // สัญญาณขาดก่อนครบเฟรม
        }
        if (s[at] != 0u) {
            byte |= (uint8_t)(1u << i);            // บิตแรกบนสายคือ LSB
            ones++;
        }
    }

    unsigned next = 9u;                            // บิตถัดไปหลัง data คือบิตที่ 9 ของเฟรม
    if (parity != PARITY_NONE) {
        const unsigned at = mid0 + 9u * SPB;
        if (at >= n) {
            return UART_FRAMING_ERROR;
        }
        const unsigned total = ones + (s[at] != 0u ? 1u : 0u);
        const unsigned want_odd = (parity == PARITY_ODD) ? 1u : 0u;
        if ((total & 1u) != want_odd) {
            return UART_PARITY_ERROR;              // parity จับบิตผิดได้เป็นจำนวนคี่เท่านั้น ผิดสองบิตจะหลุด
        }
        next = 10u;
    }

    // stop bit ที่ไม่ใช่ 1 คืออาการคลาสสิกของ baud ไม่ตรงกันระหว่างสองฝั่ง (framing error)
    const unsigned stop_at = mid0 + next * SPB;
    if (stop_at >= n || s[stop_at] != 1u) {
        return UART_FRAMING_ERROR;
    }

    *out = byte;
    return UART_OK;
}

// ---- ให้มาแล้ว: สร้างสัญญาณทดสอบ ----
static unsigned make_trace(uint8_t *s, uint8_t byte, parity_t parity, uint8_t stop_level)
{
    unsigned n = 0u, ones = 0u;
    for (unsigned i = 0u; i < 2u * SPB; i++) s[n++] = 1u;                 // idle
    for (unsigned i = 0u; i < SPB; i++) s[n++] = 0u;                      // start
    for (unsigned b = 0u; b < 8u; b++) {
        const uint8_t bit = (uint8_t)((byte >> b) & 1u);
        ones += bit;
        for (unsigned i = 0u; i < SPB; i++) s[n++] = bit;
    }
    if (parity != PARITY_NONE) {
        const uint8_t p = (uint8_t)((parity == PARITY_EVEN) ? (ones & 1u) : ((ones & 1u) ^ 1u));
        for (unsigned i = 0u; i < SPB; i++) s[n++] = p;
    }
    for (unsigned i = 0u; i < SPB; i++) s[n++] = stop_level;              // stop
    for (unsigned i = 0u; i < 2u * SPB; i++) s[n++] = 1u;                 // idle
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
    uint8_t s[16u * SPB];
    uint8_t v = 0u;
    unsigned n;

    n = make_trace(s, 0xA5u, PARITY_NONE, 1u);          // ไบต์แรกของ UART Echo ใน Header I/O Test
    CHECK_EQ(UART_OK, uart_decode(s, n, PARITY_NONE, &v));
    CHECK_EQ(0xA5, v);

    n = make_trace(s, 0x11u, PARITY_EVEN, 1u);
    CHECK_EQ(UART_OK, uart_decode(s, n, PARITY_EVEN, &v));
    CHECK_EQ(0x11, v);

    n = make_trace(s, 0xFFu, PARITY_NONE, 1u);          // 0xFF เป็นข้อมูลจริง ไม่ใช่ "ไม่มีข้อมูล"
    CHECK_EQ(UART_OK, uart_decode(s, n, PARITY_NONE, &v));
    CHECK_EQ(0xFF, v);

    n = make_trace(s, 0x11u, PARITY_ODD, 1u);           // ส่งแบบ odd แต่ถอดแบบ even
    CHECK_EQ(UART_PARITY_ERROR, uart_decode(s, n, PARITY_EVEN, &v));

    n = make_trace(s, 0x3Cu, PARITY_NONE, 0u);          // stop bit เป็น 0: baud ไม่ตรงหรือสายมีปัญหา
    CHECK_EQ(UART_FRAMING_ERROR, uart_decode(s, n, PARITY_NONE, &v));

    memset(s, 1, sizeof(s));                            // สายว่างทั้งเส้น
    CHECK_EQ(UART_NO_START, uart_decode(s, 40u, PARITY_NONE, &v));

    printf("%s: %d failure(s)\n", failures ? "FAIL" : "PASS", failures);
    return failures ? 1 : 0;
}
