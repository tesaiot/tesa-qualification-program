# Secure IoT with OPTIGA™ Trust M

Level **L3** · status **pre-alpha (outline, being written)** · 5 modules, 11 lessons · about 20 hours

Security is where TESA and Infineon can teach more deeply than anyone else: the TESAIoT Dev Kit carries an OPTIGA™ Trust M
secure element, and the public SDK already has examples and docs for mTLS, Protected Update and CSR enrolment.
This course turns that material into lessons, starting from the attacker's point of view before touching the chip.
Every SDK link is pinned to commit `ef72c1b`.

The lesson pages are Thai-first; English lesson pages are pending (`translation: pending`).

## Who it is for

- Firmware developers who finished Embedded C Foundations or equivalent
- Anyone who must connect devices securely to an IoT platform
- You need a TESAIoT Dev Kit, and a TESAIoT platform account or instance for the mTLS lessons

## Outcomes

1. Threat-model an IoT device, naming assets, attackers and verifiable mitigations.
2. Explain and choose hashes, signatures, symmetric and asymmetric encryption and certificates for a task.
3. Use OPTIGA™ Trust M through the SDK under the chip-access rules, keeping private keys inside the chip.
4. Connect a device to the TESAIoT Platform over mTLS and explain every handshake step.
5. Explain secure boot, Protected Update and CSR enrolment, and identify irreversible changes on the chip.

## Modules and lessons

**Module 1 — Threat modelling and crypto basics** ([m01-threats-and-crypto](m01-threats-and-crypto/README.md))

| Lesson | Topic | Time |
|---|---|---|
| sec-iot.m01.l01 | Threat modelling an IoT device | 70 min |
| sec-iot.m01.l02 | Crypto basics for embedded systems | 70 min |

**Module 2 — The OPTIGA™ Trust M secure element** ([m02-optiga-trust-m](m02-optiga-trust-m/README.md))

| Lesson | Topic | Time |
|---|---|---|
| sec-iot.m02.l01 | What a secure element does for us | 70 min |
| sec-iot.m02.l02 | The chip-access discipline | 70 min |

**Module 3 — mTLS to the TESAIoT Platform** ([m03-mtls-to-platform](m03-mtls-to-platform/README.md))

| Lesson | Topic | Time |
|---|---|---|
| sec-iot.m03.l01 | TLS and mTLS | 70 min |
| sec-iot.m03.l02 | MQTTs to the TESAIoT Platform | 70 min |

**Module 4 — Secure boot and Protected Update** ([m04-secure-boot-and-update](m04-secure-boot-and-update/README.md))

| Lesson | Topic | Time |
|---|---|---|
| sec-iot.m04.l01 | Secure boot and the chain of trust | 70 min |
| sec-iot.m04.l02 | Protected Update | 70 min |

**Module 5 — Secure provisioning** ([m05-provisioning](m05-provisioning/README.md))

| Lesson | Topic | Time |
|---|---|---|
| sec-iot.m05.l01 | Enrolment with a CSR | 70 min |
| sec-iot.m05.l02 | Provisioning screens on the device | 70 min |
| sec-iot.m05.l03 | Capstone: one secure device | 75 min |

## Status

This course is an outline (pre-alpha): every lesson has objectives, skills and verified references, but no content or practice yet.
**Chip safety warning.** The OPTIGA life-cycle state (LcsO) moves one way only and cannot be undone, as the SDK examples README states.
No SDK example writes metadata tag C0 or advances that state, and no lesson in this course will ask you to.
Infineon host-library code is linked by repository and tag, not copied.

## Main references

- [TESAIoT PSE84 Dev Kit SDK (Apache-2.0) README](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/README.md)
- [Security / HSM (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__feat__security.html)
- [C4 — mTLS: the OPTIGA-backed TLS identity (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__c4__mtls__optiga.html)
- [D2 — Enrolment and Protected Update end to end (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__d2__enrolment__protected__update.html)
- [Infineon optiga-trust-m (host library, MIT) @ release-v5.8.3](https://github.com/Infineon/optiga-trust-m/tree/release-v5.8.3)
- [ETSI EN 303 645 V3.1.3 (2024-09) Cyber Security for Consumer Internet of Things: Baseline Requirements](https://www.etsi.org/deliver/etsi_en/303600_303699/303645/03.01.03_60/en_303645v030103p.pdf)

## Licence

- Content: CC BY 4.0
- New code added to this course: Apache-2.0
- SDK and Infineon code is not copied; it stays under its own licence at the linked source

## How to cite TESA

When you use, share or adapt this course, credit it as follows:

> "Secure IoT with OPTIGA™ Trust M" from TESA Open Knowledge by the Thai Embedded Systems Association (TESA), https://github.com/tesaiot/tesa-qualification-program, licensed under CC BY 4.0

Add "(adapted)" at the end of the credit, with a short note of what you changed, when you change the material.
Crediting TESA does not mean TESA endorses your work. Details and examples are in [ATTRIBUTION.md](../../ATTRIBUTION.md).
