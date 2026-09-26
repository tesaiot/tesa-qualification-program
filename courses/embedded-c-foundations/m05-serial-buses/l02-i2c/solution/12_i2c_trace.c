// SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
// SPDX-License-Identifier: Apache-2.0
//
// solution/12_i2c_trace.c — เฉลยของ practice/12_i2c_trace.c
//
//     gcc -std=c11 -Wall -Wextra -o i2c_trace 12_i2c_trace.c && ./i2c_trace   -> PASS: 0 failure(s)
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

#define I2C_FIRST_ADDR (0x08u)   // ช่วงที่ sensor_i2c_scan() ของ SDK เดิน: 0x08..0x77
#define I2C_LAST_ADDR  (0x77u)   // address นอกช่วงนี้สงวนไว้ตามข้อกำหนดของ I2C

typedef enum { EV_START, EV_RESTART, EV_STOP, EV_BYTE, EV_ACK, EV_NACK } ev_kind_t;
typedef struct {
    ev_kind_t kind;
    uint8_t   value;   // ใช้เฉพาะ EV_BYTE
} event_t;

// ไบต์ address ที่ master ส่งหลัง START: address 7 บิตเลื่อนซ้ายหนึ่ง แล้วบิตท้ายคือ R/W (1 = read)
static uint8_t addr_byte(uint8_t addr7, bool read)
{
    // address 0x68 ของ BMI270 จึงกลายเป็น 0xD0 ตอนเขียน และ 0xD1 ตอนอ่านบน decoder
    return (uint8_t)(((unsigned)addr7 << 1) | (read ? 1u : 0u));
}

// แยกไบต์ address กลับเป็น address 7 บิตกับทิศทาง คืน false ถ้า address อยู่นอกช่วง 0x08..0x77
static bool parse_addr_byte(uint8_t b, uint8_t *addr7, bool *read)
{
    const uint8_t a = (uint8_t)(b >> 1);
    if (a < I2C_FIRST_ADDR || a > I2C_LAST_ADDR) {
        return false;                   // นอกช่วงที่อุปกรณ์ทั่วไปใช้ ไม่เขียนค่าลงผลลัพธ์
    }
    *addr7 = a;
    *read = (b & 1u) != 0u;
    return true;
}

// ---- ให้มาแล้ว: ต่อเหตุการณ์หนึ่งตัวลงรายการ ----
static unsigned push(event_t *ev, unsigned n, unsigned max, ev_kind_t k, uint8_t v)
{
    if (n < max) {
        ev[n].kind = k;
        ev[n].value = v;
    }
    return n + 1u;
}

// ลำดับเหตุการณ์ของการอ่าน count ไบต์จากรีจิสเตอร์ reg (อุปกรณ์ตอบ ACK ทุกไบต์ที่ master ส่ง)
//   START, addr+W, ACK, reg, ACK, RESTART, addr+R, ACK, แล้วข้อมูล count ไบต์ (ใส่ค่า 0x00 แทนข้อมูล)
//   master ตอบ ACK ทุกไบต์ข้อมูลยกเว้นไบต์สุดท้ายตอบ NACK แล้วปิดด้วย STOP
// คืนจำนวนเหตุการณ์ทั้งหมด
static unsigned encode_read_reg(uint8_t addr7, uint8_t reg, unsigned count, event_t *ev, unsigned max)
{
    unsigned n = 0u;
    n = push(ev, n, max, EV_START, 0u);
    n = push(ev, n, max, EV_BYTE, addr_byte(addr7, false));
    n = push(ev, n, max, EV_ACK, 0u);
    n = push(ev, n, max, EV_BYTE, reg);
    n = push(ev, n, max, EV_ACK, 0u);
    // ไม่มี STOP ตรงนี้: repeated START ทำให้ไม่มี master อื่นแทรกระหว่างเลือกรีจิสเตอร์กับการอ่าน
    n = push(ev, n, max, EV_RESTART, 0u);
    n = push(ev, n, max, EV_BYTE, addr_byte(addr7, true));
    n = push(ev, n, max, EV_ACK, 0u);
    for (unsigned i = 0u; i < count; i++) {
        n = push(ev, n, max, EV_BYTE, 0x00u);
        // NACK ที่ไบต์สุดท้ายบอกอุปกรณ์ให้หยุดส่ง ถ้าตอบ ACK อุปกรณ์จะเตรียมไบต์ถัดไปแล้วอาจค้างสาย SDA
        n = push(ev, n, max, (i + 1u < count) ? EV_ACK : EV_NACK, 0u);
    }
    n = push(ev, n, max, EV_STOP, 0u);
    return n;
}

// สแกนเหมือน sensor_i2c_scan(): เดิน 0x08..0x77 เก็บ address ที่ตอบ ACK เรียงจากน้อยไปมาก
// เก็บได้ไม่เกิน max ตัว (ตัดที่เกิน) และคืนจำนวนที่เก็บ
static unsigned scan(bool (*acks)(uint8_t addr7), uint8_t *found, unsigned max)
{
    unsigned n = 0u;
    for (unsigned a = I2C_FIRST_ADDR; a <= I2C_LAST_ADDR && n < max; a++) {
        if (acks((uint8_t)a)) {
            found[n++] = (uint8_t)a;    // เดินจากน้อยไปมาก ผลจึงเรียงอยู่แล้ว
        }
    }
    return n;
}

// ---- test ----
static bool board_acks(uint8_t a)   // อุปกรณ์บนบัสเซนเซอร์ตามตัวอย่าง 01_i2c_bus_scan.c ของ SDK
{
    return a == 0x08u || a == 0x18u || a == 0x44u || a == 0x68u || a == 0x77u;
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
    CHECK_EQ(0xD0, addr_byte(0x68u, false));
    CHECK_EQ(0xD1, addr_byte(0x68u, true));
    CHECK_EQ(0x20, addr_byte(0x10u, false));    // DFR0522 RGB matrix บน header

    uint8_t a = 0u;
    bool rd = false;
    CHECK_EQ(1, parse_addr_byte(0xEFu, &a, &rd));
    CHECK_EQ(0x77, a);
    CHECK_EQ(1, rd);
    CHECK_EQ(0, parse_addr_byte(0x0Au, &a, &rd));   // 0x05: อยู่ในช่วงที่สงวนไว้

    event_t ev[32];
    const unsigned n = encode_read_reg(0x68u, 0x00u, 2u, ev, 32u);
    CHECK_EQ(13, n);
    if (n == 13u) {
        CHECK_EQ(EV_START, ev[0].kind);
        CHECK_EQ(0xD0, ev[1].value);
        CHECK_EQ(EV_RESTART, ev[5].kind);
        CHECK_EQ(0xD1, ev[6].value);
        CHECK_EQ(EV_ACK, ev[9].kind);                // ไบต์ข้อมูลแรก: master ตอบ ACK
        CHECK_EQ(EV_NACK, ev[11].kind);              // ไบต์สุดท้าย: master ตอบ NACK
        CHECK_EQ(EV_STOP, ev[12].kind);
    }

    uint8_t found[16] = {0};
    CHECK_EQ(5, scan(board_acks, found, 16u));
    CHECK_EQ(0x08, found[0]);
    CHECK_EQ(0x77, found[4]);
    CHECK_EQ(2, scan(board_acks, found, 2u));     // ที่เก็บเล็ก: ตัดที่เกิน ไม่เขียนเลยขอบ

    printf("%s: %d failure(s)\n", failures ? "FAIL" : "PASS", failures);
    return failures ? 1 : 0;
}
