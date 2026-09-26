# Secure IoT with OPTIGA™ Trust M

Level **L3** · status **alpha** · 5 modules, 11 lessons · about 20 hours

Security is where TESA and Infineon can teach more deeply than anyone else: the TESAIoT Dev Kit carries an OPTIGA™ Trust M
secure element, and the public SDK already has examples and docs for mTLS, Protected Update and CSR enrolment.
This course turns that material into lessons, starting from the attacker's point of view before touching the chip.
Every SDK link is pinned to commit `ef72c1b`.

The whole course follows one device: a sensor node on the TESAIoT Dev Kit that publishes to the TESAIoT Platform over MQTTS.
You threat-model it first, add one mitigation per lesson, and in the capstone hand the device over with evidence that each mitigation works.
Every fact in the lessons points to a file in the SDK, the SDK documentation, a TESAIoT Developer Hub example or public Infineon material,
and every lesson says plainly what TLS, mTLS, the secure element, secure boot and Protected Update do **not** protect against.

The lesson pages are Thai-first; English lesson pages are pending (`translation: pending`).

## Who it is for

- Firmware developers who finished Embedded C Foundations or equivalent
- Anyone who must connect devices securely to an IoT platform
- You need a TESAIoT Dev Kit, and a TESAIoT platform account or instance for the mTLS lessons

**What to prepare:** the TESAIoT PSE84 Dev Kit SDK at commit `ef72c1b` with ModusToolbox 3.6 (the version the SDK README requires),
a computer with `openssl` and `mosquitto-clients`, and a device registered on the TESAIoT Platform for modules 3 to 5.

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

This course is **alpha**: every lesson has its content, excerpts quoted from the real sources, practice with answers, a `quiz.yaml` check and a lab.
It still needs a teaching trial with real learners and their feedback. The English lesson pages are not translated yet (`translation: pending`).

**Chip safety warning.** The OPTIGA life-cycle state (LcsO) moves one way only and cannot be undone, as the SDK examples README states.
No SDK example writes metadata tag C0 or advances that state, and no lesson in this course asks you to.
Labs that change the chip in other ways (enrolment, which generates a new key, and Protected Update, which permanently advances the version counter)
are separate optional labs that need the instructor's approval first, and provisioning the device for secure boot is outside the labs.

## Main references

- [TESAIoT PSE84 Dev Kit SDK (Apache-2.0) README](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/README.md)
- [Security / HSM (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__feat__security.html)
- [C4 — mTLS: the OPTIGA-backed TLS identity (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__c4__mtls__optiga.html)
- [D2 — Enrolment and Protected Update end to end (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__d2__enrolment__protected__update.html)
- [Infineon optiga-trust-m (host library, MIT) @ release-v5.8.3](https://github.com/Infineon/optiga-trust-m/tree/release-v5.8.3)
- [Infineon optiga-trust-m @ release-v5.3.0](https://github.com/Infineon/optiga-trust-m/tree/release-v5.3.0), the release the SDK pins in `proj_cm55/deps/optiga-trust-m.mtb`
- TESAIoT Developer Hub examples: [device-servertls](https://dev.tesaiot.dev/?example=developer-hub--device-servertls&q=device-servertls) · [device-mtls](https://dev.tesaiot.dev/?example=developer-hub--device-mtls&q=device-mtls) · [c_ota_client](https://dev.tesaiot.dev/?example=developer-hub--c_ota_client&q=c_ota_client) · [pse84_tesaiot_client](https://dev.tesaiot.dev/?example=developer-hub--pse84_tesaiot_client&q=pse84_tesaiot_client) (Cypress EULA, linked only)
- Companion course: [TESAIoT Firmware Stack module 5, connecting to the TESAIoT Platform securely](../tesaiot-firmware-stack/m05-connect-to-platform/README.md)
- [ETSI EN 303 645 V3.1.3 (2024-09) Cyber Security for Consumer Internet of Things: Baseline Requirements](https://www.etsi.org/deliver/etsi_en/303600_303699/303645/03.01.03_60/en_303645v030103p.pdf)

## Licence

- Content: CC BY 4.0
- The course has no separate code files; the short snippets written for the lesson pages are Apache-2.0
- Short excerpts quoted with a link to file and commit come from the TESAIoT PSE84 Dev Kit SDK and the TESAIoT Developer Hub (Apache-2.0) and from Infineon's optiga-trust-m examples (MIT); each excerpt names its source and licence where it is quoted
- The `pse84_tesaiot_client` example is under the Cypress (Infineon) EULA and is only linked, never copied; the SDK's `tesaiot_mqtt` module files, which were developed from that project, are likewise only linked and summarised

## How to cite TESA

When you use, share or adapt this course, credit it as follows:

> "Secure IoT with OPTIGA™ Trust M" from TESA Open Knowledge by the Thai Embedded Systems Association (TESA), https://github.com/tesaiot/tesa-qualification-program, licensed under CC BY 4.0

Add "(adapted)" at the end of the credit, with a short note of what you changed, when you change the material.
Crediting TESA does not mean TESA endorses your work. Details and examples are in [ATTRIBUTION.md](../../ATTRIBUTION.md).
