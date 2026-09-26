# Module 4 · Logic analyzer and protocol analyzer

**Module goal:** capture digital signals and decode protocols to prove what is really happening on the wire.

Status **alpha** (in trial use) · about 130 minutes

**You need:** a logic analyzer that works with PulseView, and a TESAIoT Dev Kit flashed with the QWA309 Header I/O Test example

| Lesson | Topic | Time |
|---|---|---|
| [elec.m04.l01](l01-capture-a-signal/README.md) | Capturing your first digital signal | 65 minutes |
| [elec.m04.l02](l02-decode-i2c-and-uart/README.md) | Decoding I2C and UART | 65 minutes |

## Module checkpoint

- [ ] can capture a blinking signal on a header pin and measure its pulse width and frequency
- [ ] can fully decode an I2C bus scan, including address and ACK, and compare it against what the screen shows
- [ ] can decode UART at 115200 baud and explain the symptom of setting the wrong baud rate
