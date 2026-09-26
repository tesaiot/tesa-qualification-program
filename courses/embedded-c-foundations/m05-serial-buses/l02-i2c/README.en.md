---
id: c-found.m05.l02
lang: en
title: {th: I2C, en: I2C}
summary: {th: สแกนบัส อ่านเขียนรีจิสเตอร์ของอุปกรณ์ และใช้ lock ของบัสร่วมกับงานอื่นอย่างถูกต้อง, en: 'Scan the bus, read and write device registers, and share the bus lock correctly with other tasks.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m05.l01]
objectives:
- {th: สแกนบัส I2C และระบุอุปกรณ์ที่พบจาก address ได้, en: Scan the I2C bus and identify devices by address.}
- {th: อ่านและเขียนรีจิสเตอร์ของอุปกรณ์ โดยถือ lock ของบัสตลอดหนึ่งธุรกรรมและคืนทุกครั้ง, en: Read and write device registers while holding the bus lock for one whole transaction and always releasing it.}
- {th: 'ถอดรหัสภาพสัญญาณ I2C ได้ครบ start, address, read/write, ACK/NACK และ stop', en: 'Decode an I2C trace: start, address, read/write, ACK/NACK and stop.'}
develops:
- {skill: proto.i2c, to: 3}
- {skill: meas.logic-analyzer, to: 3}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
slides: slides.md
source_sha256: 96bace876bd1d470d5b3610f117a8a47c9c1e53ed45cb5c7fcdf722140e6f6f4
---

## Objectives

By the end of this lesson, you will be able to

1. Scan the I2C bus and identify the devices found by their address.
2. Read and write a device's registers, holding the bus lock for one entire transaction and always releasing it.
3. Decode an I2C trace in full: start, address, read/write, ACK/NACK and stop.

Takes about 70 minutes (concepts 15 · practice 25 · lab 25 · check 5). The lab needs a two-channel logic analyzer that can accept 3.3 V.

## Before you start

Two review questions from earlier lessons.

1. UART has no clock wire — how does the receiver know each bit's timing? How does a bus with a separate clock wire, like I2C, differ from that?
2. The `06_raw_register_access.c` example you read in lesson 1.1 does a read-modify-write of `PWR_CTRL` inside what, and why must the whole step be wrapped in it?

## See it work first

Open [examples/12_i2c_transaction.c](examples/12_i2c_transaction.c). This program simulates the board's sensor bus and prints transactions the way a logic analyzer's decoder would show them. **Predict before you run it:** what is the first byte on the wire when reading from the BMI270 (address `0x68`)?

```sh
gcc -std=c11 -Wall -Wextra -o i2c_transaction examples/12_i2c_transaction.c
./i2c_transaction
```

The answer is `D0`, not `68`, because the 7-bit address is shifted left by one bit, with the R/W bit appended. The `probe` line shows what a scan does: send an address and see whether anyone ACKs. The `read` line shows that reading one register involves writing the register number, a repeated START, and then reading — all inside one single transaction.

## Concepts

### 1. One I2C transaction

I2C uses two wires: SCL (the clock, driven by the master) and SDA (data). Both are open-drain, with pull-up resistors. Several devices share the same wires, told apart by their address.

| Event | On the wire | Meaning |
|---|---|---|
| START | SDA goes low while SCL is high | Begins a transaction |
| address + R/W | 8 bits, MSB first: a 7-bit address then an R/W bit (0 write, 1 read) | Addresses one device |
| ACK / NACK | The ninth bit; the receiver pulls SDA low = ACK, leaves it high = NACK | "Received" or "no one there" / "that's enough" |
| data | 8 bits MSB first, followed by ACK/NACK for every byte | One byte at a time |
| repeated START | A new START without a STOP first | Switches from write to read without releasing the bus |
| STOP | SDA goes high while SCL is high | Ends the transaction |

Most devices on a bus behave as a "register file". The SDK's [06_raw_register_access.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/06_raw_register_access.c#L15-L32) example explains that `sensor_i2c_read_reg()` writes the register number "with NO stop", followed by a repeated START and the read, which "is what the parts expect and what you would get wrong writing it yourself." Some devices, such as the SHT40, have no registers at all — they use command-then-response instead, which is why the same file also has `sensor_i2c_write_raw()` and `sensor_i2c_read_raw()`.

### 2. Scan, then prove the wire before trusting the driver

Scanning means probing every address from 0x08 to 0x77 and noting which ones respond with ACK. The board's sensor bus is SCB0, on P8.0 (SCL) and P8.1 (SDA), running at 1.8 V and 400 kHz, and the addresses expected on this board are listed in the `bus_device_name()` table in [01_i2c_bus_scan.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/01_i2c_bus_scan.c#L98-L110).

| Address | Device |
|---|---|
| 0x08 | CapSense PSoC 4000T (base board) |
| 0x18 | TLV320DAC3100 audio codec |
| 0x44 | SHT40 humidity and temperature |
| 0x68 | BMI270 IMU |
| 0x77 | DPS368 pressure and temperature |

Two things the example warns about: the BMM350 (0x15) is on I3C, a different kind of device, "and never appears here", and finding an address not in the table "is not an error — it is a board you have added something to." Finding an address is still not proof that it's the chip you assumed. [02_read_imu.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/02_read_imu.c#L32-L38) teaches to "PROVE THE WIRE FIRST" — read register 0x00 first: getting `0x24` confirms it's a real BMI270; getting `0xFF` or a failed read means the bus or chip has a problem; getting anything else means it's a different chip sharing that same address.

### 3. The bus lock: one transaction, one lock, released on every path

SCB0 has several owners. The SDK documentation's chapter J1 states that OPTIGA Trust M's PAL is also a master on SCB0, alongside a background task that reads sensors every 100 ms. The SDK's read/write functions **do not hold the lock for you** — the caller must wrap it themselves with `sensor_i2c_lock()` and `sensor_i2c_unlock()`. A comment in 01_i2c_bus_scan.c explains what happens without it: "It works, it keeps working, and then one day a repeated START from this task lands between the address phase and the data phase of the auto task's read and both come back wrong."

```c
/* Step 2 — take the bus. Never scan without this. */
if (!sensor_i2c_lock(SCAN_LOCK_TIMEOUT_MS)) {
    /* Someone still holds it after a full second. The likeliest cause is
     * the hazard in the header block: the auto task was suspended between
     * its own lock and unlock. Resuming it lets it finish and release. */
    printf("  sensor_i2c_lock(%u ms) TIMED OUT — someone holds the bus\r\n",
           (unsigned)SCAN_LOCK_TIMEOUT_MS);
    if (auto_was_running) {
        printf("  resuming the auto task so it can release the mutex\r\n");
        sensor_auto_start();
    }
    return SDK_EX_BUSY;
}
```

Source: [01_i2c_bus_scan.c lines 143-155](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/01_i2c_bus_scan.c#L143-L155) (Apache-2.0, tesaiot-pse84-devkit-sdk)

Rules drawn from these examples:

- **A lock always has a timeout,** and when it times out, report busy — don't conclude the bus is broken.
- **One lock per set of readings, not per register.** 02_read_imu reads acceleration, gyro and temperature inside a single lock, so all three come from the same instant, and a command-then-response device must hold the lock across "the command, the wait AND the response" (06_raw_register_access).
- **Release the lock on every exit path.** The scan example has a comment: "There is no path out of here that skips this." And chapter J1 notes that even reporting an error must happen after unlocking.
- **Never hold the lock across a long delay** — it blocks every other job waiting on the bus.

## Worked example

[examples/12_i2c_transaction.c](examples/12_i2c_transaction.c) runs in three parts.

- **Part 1**: `address_byte()` shifts the 7-bit address and appends the R/W bit.
- **Part 2**: `probe()` simulates scanning four addresses around 0x68 — the one with a device answers ACK, the rest NACK.
- **Part 3**: `read_register()` prints reading a one-byte chip id, and reading six bytes of acceleration in a single transaction (a burst read).

Try changing things and predicting the result before you run it.

1. Switch to reading the DPS368 (0x77). What is the address byte on the write, and on the read?
2. If the six-byte read were split into six separate one-byte transactions, how many more bytes would appear on the wire, and why does the SDK's example say a burst read is "both faster and ATOMIC"?
3. Add `0x10` (the DFR0522 RGB matrix, connected to the header's 3.3 V bus) to the device list, and probe it.

## Practice

Open [practice/12_i2c_trace.c](practice/12_i2c_trace.c). There are 4 gaps to fill in.

1. `addr_byte()` assembles the address byte.
2. `parse_addr_byte()` takes it apart again, and rejects an address outside 0x08 to 0x77.
3. `encode_read_reg()` produces the event sequence for reading a register, including the NACK on the final byte.
4. `scan()` scans the same way `sensor_i2c_scan()` does, and stops adding results once storage is full.

```sh
gcc -std=c11 -Wall -Wextra -o i2c_trace practice/12_i2c_trace.c && ./i2c_trace
```

## Solution

Try it yourself for at least 15 minutes first, then open [solution/12_i2c_trace.c](solution/12_i2c_trace.c). The comments in the solution explain two things often overlooked: why there is no STOP between selecting the register and reading it, and why the master must respond with NACK on the last byte.

## Check your understanding

Answer the 5 questions in [quiz.yaml](quiz.yaml) (shown at the bottom of this page on the website), covering all three objectives. Getting 4 or more right counts as finishing the lesson.

## Lab

**Task:** scan the board's sensor bus with the SDK's example, then capture a real I2C transaction on the header's 3.3 V bus with a logic analyzer.

**Part 1: scanning with the SDK**

1. Build with `make build -j ENABLE_PAGE_EXAMPLES=1 SDK_EXAMPLE_CM33=cm33/sensors/01_i2c_bus_scan`, then flash and unplug/replug the cable.
2. From the serial console, note every address that responds and the name the example prints for it. Compare against the table in concept 2 — which ones are missing, and which are extra?
3. Build again with `SDK_EXAMPLE_CM33=cm33/sensors/02_read_imu`. Note the chip id line, and answer: what kind of evidence is this that a scan alone cannot give?

**Part 2: capturing signals** (the sensor bus runs at 1.8 V and isn't exposed at the header, so this part uses the header's 3.3 V I2C bus instead)

4. Flash the [QWA309 — Header I/O Test](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_header_hw_test&q=prac_qwa309_header_hw_test) example from the Developer Hub. Connect the logic analyzer, one channel to SCL and one to SDA of the Arduino header's I2C, plus ground. Set the decoder to I2C.
5. Capture while pressing the **Scan** button on the screen. This example scans 0x08 to 0x77 on the same bus as the touch screen. Find one address in the decoder that got a NACK and one that got an ACK, then decode by eye, bit by bit: START, the 7 address bits, the R/W bit, the ninth bit, STOP.
6. If you have a DFR0522 RGB matrix, connect it and scan again — you should see 0x10 respond with ACK (the [DFR0522 RGB Dot Matrix](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_rgb_matrix&q=prac_qwa309_rgb_matrix) example uses this address).
7. Measure SCL's frequency from the waveform.

**Evidence to keep in your portfolio:** the scan log and chip id from the serial console, one waveform picture of an ACK transaction and one of a NACK transaction, both labelled by hand, and the SCL frequency you measured (state which part of the waveform you measured it from, since I2C speeds differ by bus configuration).

## Going further

- Read the SDK documentation's chapter [J1 — The sensor bus and its lock](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__j1__sensor__bus.html), the section explaining why `sensor_i2c_init()` calls a bus recovery routine (freeing a device stuck holding SDA) before configuring the pins.
- Read [Understanding the I2C Bus (Texas Instruments SLVA704)](https://www.ti.com/lit/an/slva704/slva704.pdf) on pull-ups and clock stretching, then connect it to Appendix X #13 of the SDK documentation, which recounts a clock-stretching device stuck on the display's bus starving other CM55 tasks.

Next lesson: [lesson 5.3, SPI](../l03-spi/README.md)

## Reflect

- If you were adding a new sensor to the SCB0 bus, what would you need to check first, to avoid breaking the four sensors already there?
- Have you ever run into code that "mostly works, but occasionally gets a wrong value"? Could that be a symptom of bus contention?

## References

- [SDK: cm33/sensors/01_i2c_bus_scan.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/01_i2c_bus_scan.c)
- [SDK: cm33/sensors/06_raw_register_access.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/06_raw_register_access.c)
- [SDK: cm33/sensors/02_read_imu.c (proving the wire before trusting the driver)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/02_read_imu.c)
- [J1 — The sensor bus and its lock (SDK docs built from commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__j1__sensor__bus.html)
- [Texas Instruments: Understanding the I2C Bus (SLVA704)](https://www.ti.com/lit/an/slva704/slva704.pdf)

## Examples on the TESAIoT Developer Hub

Try the real thing on the TESAIoT Dev Kit: open an example on the Developer Hub to read the code, download it, or flash a prebuilt firmware image.

- [QWA309 — DFR0522 RGB Dot Matrix](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_rgb_matrix&q=prac_qwa309_rgb_matrix) — controls a DFRobot DFR0522 8x16 RGB matrix (I2C 0x10) on the 3.3 V bus alongside the display, showing clear/fill/pixel/pattern through an LVGL UI.
- [EP01 — DPS368 Monitor](https://dev.tesaiot.dev/?example=developer-hub--int_ep01_dps368_monitor&q=int_ep01_dps368_monitor) — reads atmospheric pressure and temperature from the Infineon DPS368 sensor over I2C, and displays it on an LVGL screen.
- [QWA309 — Header I/O Test](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_header_hw_test&q=prac_qwa309_header_hw_test) — diagnostic: scans the header's 3.3 V I2C bus, and tests UART, SPI, GPIO and PWM, with a console UI.
