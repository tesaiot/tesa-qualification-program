# Module 5 · UART, I2C and SPI with a logic analyzer

**Module goal:** communicate over three fundamental buses, and verify them with a logic analyzer against real signals.

Status: **alpha** (experimental) · Approximate time: 210 minutes

Every lesson has content, examples you can run on your computer, practice with a solution, a check for understanding, and a lab. The course code runs and has been checked on a computer; the on-board labs are still waiting for a teaching trial.

| Lesson | Topic | Time |
|---|---|---|
| [c-found.m05.l01](l01-uart/README.md) | UART | 70 min |
| [c-found.m05.l02](l02-i2c/README.md) | I2C | 70 min |
| [c-found.m05.l03](l03-spi/README.md) | SPI | 70 min |

## End-of-module checkpoint

- [ ] Capture a real UART frame from the board's pins, decode it by eye first, then confirm it with a decoder.
- [ ] Capture I2C signals during a bus scan, and decode the address and ACK with a logic analyzer.
- [ ] Capture an SPI transaction and prove with a picture that setting the wrong mode gives the wrong byte.
- [ ] Explain how UART, I2C and SPI differ along three dimensions: wire count, device addressing, and speed.
