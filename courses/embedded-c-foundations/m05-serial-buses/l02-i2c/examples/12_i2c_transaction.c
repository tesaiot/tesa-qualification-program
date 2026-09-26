// SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
// SPDX-License-Identifier: Apache-2.0
//
// examples/12_i2c_transaction.c — ธุรกรรม I2C หน้าตาเป็นอย่างไรบนสาย พิมพ์แบบเดียวกับที่ decoder ของ logic analyzer แสดง
//
// จำลองบัสเซนเซอร์ของบอร์ด (SCB0) ที่มีอุปกรณ์ตามตารางในตัวอย่าง 01_i2c_bus_scan.c ของ SDK
// แล้วแสดงสองธุรกรรม: การ probe หนึ่ง address ระหว่างสแกน และการอ่านรีจิสเตอร์ chip id ของ BMI270
//
//     gcc -std=c11 -Wall -Wextra -o i2c_transaction 12_i2c_transaction.c
//     ./i2c_transaction
//
// ทายก่อนรัน: ไบต์แรกบนสายเมื่ออ่านจาก BMI270 (address 0x68) คืออะไร
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

// อุปกรณ์บนบัสเซนเซอร์ของ AI Kit / Dev Kit ตามตาราง bus_device_name() ใน 01_i2c_bus_scan.c ของ SDK
static const uint8_t k_present[] = {0x08u, 0x18u, 0x44u, 0x68u, 0x77u};

static bool device_acks(uint8_t addr7)
{
    for (unsigned i = 0u; i < sizeof(k_present); i++) {
        if (k_present[i] == addr7) {
            return true;
        }
    }
    return false;
}

// ท่าที่ 1: ไบต์ address = address 7 บิตเลื่อนซ้ายหนึ่งบิต แล้วใส่บิต R/W ไว้ท้าย (0 = write, 1 = read)
static uint8_t address_byte(uint8_t addr7, bool read)
{
    return (uint8_t)((addr7 << 1) | (read ? 1u : 0u));
}

// ท่าที่ 2: probe แบบที่การสแกนทำ ส่ง START แล้ว address+W ดูว่ามี ACK ไหม แล้ว STOP
static void probe(uint8_t addr7)
{
    printf("  probe 0x%02X:  S  %02X(0x%02X W)  %s  P\n", (unsigned)addr7,
           (unsigned)address_byte(addr7, false), (unsigned)addr7,
           device_acks(addr7) ? "ACK" : "NACK");
}

// ท่าที่ 3: อ่านรีจิสเตอร์: เขียนหมายเลขรีจิสเตอร์ "โดยไม่ STOP" แล้ว repeated START ไปอ่าน
// (ตัวอย่าง 06_raw_register_access.c ของ SDK อธิบายว่า sensor_i2c_read_reg() ทำแบบนี้)
static void read_register(uint8_t addr7, uint8_t reg, const uint8_t *reply, unsigned n)
{
    printf("  read  0x%02X reg 0x%02X:  S  %02X(W)  ACK  %02X(reg)  ACK  Sr  %02X(R)  ACK ",
           (unsigned)addr7, (unsigned)reg, (unsigned)address_byte(addr7, false), (unsigned)reg,
           (unsigned)address_byte(addr7, true));
    for (unsigned i = 0u; i < n; i++) {
        // master ตอบ ACK ทุกไบต์ ยกเว้นไบต์สุดท้ายตอบ NACK เพื่อบอกอุปกรณ์ว่าพอแล้ว
        printf(" %02X  %s ", (unsigned)reply[i], (i + 1u < n) ? "ACK" : "NACK");
    }
    printf(" P\n");
}

int main(void)
{
    printf("scan fragment (the SDK scan walks 0x08..0x77):\n");
    for (uint8_t a = 0x66u; a <= 0x69u; a++) {
        probe(a);
    }

    printf("register read:\n");
    const uint8_t chip_id = 0x24u;                  // BMI270 chip id ตามตัวอย่าง 02_read_imu.c ของ SDK
    read_register(0x68u, 0x00u, &chip_id, 1u);

    const uint8_t acc[6] = {0x10u, 0x00u, 0xF0u, 0xFFu, 0x00u, 0x40u};   // ค่าสมมติของความเร่งหกไบต์
    read_register(0x68u, 0x0Cu, acc, 6u);           // burst read: หกไบต์ในธุรกรรมเดียว
    return 0;
}
