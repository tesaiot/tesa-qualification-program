---
id: sec-iot.m05.l03
lang: en
title: {th: 'งานปลายทาง: อุปกรณ์ที่ปลอดภัยหนึ่งชิ้น', en: 'Capstone: one secure device'}
summary: {th: รวม threat model การลงทะเบียน mTLS และการอัปเดตแบบป้องกัน เป็นอุปกรณ์หนึ่งชิ้นพร้อมหลักฐาน, en: 'Combine the threat model, enrolment, mTLS and protected update into one device with evidence.'}
level: L3
time_min: {concept: 5, practise: 10, lab: 55, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [sec-iot.m05.l02]
objectives:
- {th: ส่งอุปกรณ์ที่ลงทะเบียนแล้ว เชื่อมต่อด้วย mTLS และส่งข้อมูลขึ้นแพลตฟอร์มได้ พร้อม log เป็นหลักฐาน, en: 'Deliver an enrolled device that connects over mTLS and publishes to the platform, with logs as evidence.'}
- {th: ปรับ threat model จากโมดูลแรกให้สะท้อนมาตรการที่ทำจริง และระบุความเสี่ยงที่ยังเหลือ, en: Update the module-one threat model to reflect implemented mitigations and remaining risks.}
develops:
- {skill: sec.fundamentals, to: 3}
- {skill: iot.cloud-platform, to: 3}
- {skill: soft.communication, to: 2}
assesses:
- {skill: sec.fundamentals, level: 3, evidence: resources/evidence-checklist.md}
context: {platform: psoc-edge-e84, lang: c, secure_element: optiga-trust-m, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
source:
- {repo: 'https://github.com/tesaiot/tesaiot-pse84-devkit-sdk', path: bento-firmware-template-mtb-only, ref: ef72c1b658178eee8c38b1e47d28b006f80a59b5, license: Apache-2.0}
source_sha256: dc7346f30dec843e6c540e989b749aca4801d3c3a8ca330207d05ef03b3d0ff0
---

# Lesson 5.3: Capstone — one secure device

> Module 5 · Secure device provisioning · [Module overview](../README.md) · [Course home](../../README.md)

This final piece of work does not measure whether the device "looks like it works" — it measures whether you can **prove** it works as claimed.
You will deliver one device that is enrolled, connects over mTLS with a key inside the chip, publishes to the platform, and comes with a threat model updated to match reality.

## Objectives

By the end of this lesson you will:

1. Deliver an enrolled device that connects over mTLS and publishes to the platform, with logs as evidence
2. Update the threat model from the first module to reflect the mitigations you actually implemented, and list the risks that remain

## Before you start

- **Already covered:** every lesson in this course, especially the labs of [3.1](../../m03-mtls-to-platform/l01-tls-and-mtls/README.md), [3.2](../../m03-mtls-to-platform/l02-mqtts-to-tesaiot/README.md) and [5.1](../l01-csr-enrolment/README.md)
- **Files you need:** your threat model from [lesson 1.1](../../m01-threats-and-crypto/l01-threat-modelling/README.md), and the report template [resources/evidence-checklist.md](resources/evidence-checklist.md)
- **Device:** a TESAIoT Dev Kit already registered on the TESAIoT Platform, with a config file that can connect, and the SDK's template with every patch applied (lesson 3.1)
- **Approval:** real enrolment creates a new key inside the chip, and a Protected Update permanently advances the version counter. Both need the instructor's permission first.
  **No step in this task writes metadata tag `C0`.** If any slot's `C0` value changes during this work, stop and report it immediately.

## See it work first

Throughout this course we have met the same pattern again and again: a line that looks like success does not mean success.

- `[PSA-Sign] Using Key OID ...` is printed **before** the signature happens (lesson 3.1)
- `tesaiot_mqtt_publish()` returning `true` means **queued**, not delivered to the broker (lesson 3.2)
- `tesaiot_publish_protected_update()` returning `0` means **requested**, not done (lesson 4.2)
- The function `ota_verify_firmware()` returns `OTA_OK` without checking anything at all (lesson 4.2)

**Ask yourself before you start:** for each item above, what would count as **correct** evidence, and which side would it come from?

## Concepts

This task's evidence comes in four kinds, from weakest to strongest.

1. **A message the device prints.** Useful once you know exactly when that line is printed, and only alongside confirming that an accompanying error line does **not** appear.
2. **State read back from the chip**, such as `0xE0E1`'s metadata before and after. The chip answers truthfully no matter what the host prints.
3. **Evidence from the receiving side**, such as data that reaches a subscriber, or what the platform itself records.
4. **A negative test** — a case that **should fail**, and really does. For example, the mTLS port refusing a client with no certificate. A mitigation that has never been tested to fail has proven nothing.

And evidence must **never leak.** Never attach an MQTT password, a WiFi password, or a bundle file to your report. The firmware's logs are already designed to print only a password's length (`PassLen`, `passphrase=N byte(s)`).
If your report will be shared, replace the `device_id` and the chip's UID with partially masked values.

Your updated threat model must state plainly what is still unprotected. This course has already found at least this many remaining risks in the template at commit `ef72c1b`.

| Remaining risk | From lesson |
|---|---|
| The chip prevents a key from being stolen, but not from being used to sign by firmware that has already been compromised | 1.2 |
| The device does not check a certificate's expiry or revocation (`MBEDTLS_HAVE_TIME_DATE` and CRL are disabled) | 1.2 |
| The I2C wire between the MCU and the chip is not encrypted by default | 1.2 |
| TLS 1.2 sends the device's certificate unencrypted during the handshake | 3.1 |
| If using the factory certificate, identity is bound to the device only by the broker's ACL | 3.1 |
| The config file on LittleFS, which carries the WiFi password, is never stated to be encrypted | 3.2 |
| The template's secure boot chain covers only CM33_S, and only once provisioned | 4.1 |
| The example OTA client still does not verify a firmware image's hash or signature | 4.2 |

## Worked example

Here is a sample of how one row of the evidence table could be filled in, for the claim "connects with mTLS using an enrolled identity." Values in angle brackets are your board's real values.

| Claim | Positive evidence | Negative evidence | Kind |
|---|---|---|---|
| The device connects to the broker with mTLS, and the chip is the one signing with TESAIoT's key | UART: `[mTLS] device pair verified — using TESAIoT identity`, `[PSA-Sign] Using Key OID 0xE0F1 ...`, `[MQTT] Connected to broker`, all within the same connection | No `[PSA-Sign] ERROR: trustm_ecdsa_sign status=...` line · from a computer, `openssl s_client` on port 8883 with no client certificate gets refused with an alert | 1 and 4 |

Notice the positive evidence has three lines, because one line is not enough (lesson 3.1), and the negative evidence proves the port really requires a genuine certificate, rather than letting everyone in.
Other rows in the [resources/evidence-checklist.md](resources/evidence-checklist.md) template follow the same pattern.

## Practice

Classify each item by evidence kind (1 a device message · 2 chip state · 3 the receiving side · 4 a negative test), or mark it **not evidence.**

1. `mosquitto_sub`, already subscribed beforehand, receives the payload the device published ____
2. `optiga.read_metadata(0xE0E1)` before and after a Protected Update shows `D0` changed to the value naming the anchor, and `C0` unchanged ____
3. `tesaiot_mqtt_publish()` returns `true` ____
4. Connecting to port 8884 without a CA gets `Verify return code: 20` ____
5. A screenshot showing "The device can prove it holds the key this certificate names" ____

<details><summary>Solution</summary>

1. **3**, the receiving side
2. **2**, chip state — the chip always answers truthfully
3. **Not evidence** that the data arrived — it only means it was queued
4. **4**, a negative test — it proves that verifying the server's certificate requires the correct anchor
5. **1**, a device message. This sentence comes from `prov_say()` after checking that the certificate matches the key. It carries more weight if paired with the UART log from the same run.

</details>

## Check your understanding

The questions below are part of the full set in [quiz.yaml](quiz.yaml), which the automated grader uses.

1. Which set of evidence is enough to claim "the chip successfully signed CertificateVerify with the enrolled key"? *(objective 1)*
   - a) The line `[PSA-Sign] Using Key OID 0xE0F1` alone
   - b) The device pair verified line, the Using Key OID 0xE0F1 line, no ERROR line from `trustm_ecdsa_sign`, and `[MQTT] Connected to broker`, all in the same connection
   - c) The screen shows connected
   - d) `tesaiot_mqtt_connect()` returns `true`

   <details><summary>Solution</summary>

   **b.** Per the criteria from chapter C4 that we used in lesson 3.1.

   </details>

2. Which of these belongs in the "remaining risk" section of the threat model after finishing this task? *(objective 2)*
   - a) None, because mTLS is already in use
   - b) The secure boot chain covers only CM33_S, and the device does not check a certificate's expiry
   - c) The private key lives in flash
   - d) The MQTT password is printed on the console

   <details><summary>Solution</summary>

   **b.** Items c and d are not true of a device that follows this course. Item a is threat modelling with your eyes closed — mTLS does not fix every provision.

   </details>

3. Why must a report include negative tests? *(objective 2)*
   - a) To make the report longer
   - b) Because a mitigation that has never been tested to fail might pass every time whether it works or not
   - c) Because the platform requires it
   - d) Because positive tests are always wrong

   <details><summary>Solution</summary>

   **b.** This is the same principle as "a verifiable mitigation" from lesson 1.1 — a test must be able to go red.

   </details>

## Lab

**Deliver one device with an evidence report.** This takes about 55 minutes; fill in [resources/evidence-checklist.md](resources/evidence-checklist.md) as you go.

- [ ] **1. Starting state.** (mtb-mpy) Read `0xE0E1`'s metadata, and record tags `C0` and `D0`. If `C0` is not `01`, stop and tell your instructor. On mtb-only, record that you skipped this step and why.
- [ ] **2. Enrol.** (once the instructor has approved) HSM Security → Enrol Certificate, in whichever mode currently connects. Keep the on-screen sentences and the UART lines, per lesson 5.1's optional lab. The verdict must be "The device can prove it holds the key this certificate names."
- [ ] **3. Switch to mTLS.** Set `tls_mode=mtls` and reconnect. Keep the log from `[MQTT] Waiting for WiFi...` through to `[MQTT] Connected to broker`, then judge it against lesson 3.1's three criteria.
- [ ] **4. Publish, and prove it arrived.** Publish telemetry, then collect evidence from the receiving side, per lab 3.2 step 4. State clearly where the evidence came from.
- [ ] **5. At least two negative tests.** For example: port 8883 refusing a client with no certificate (lab 3.1 step 3), server verification failing with no anchor (lab 3.1 step 4), or `SECURE_BOOT=yes` being refused by the build system (lab 4.1 step 2).
- [ ] **6. Protected Update (if your instructor allows it).** Follow lesson 4.2's optional lab, keep the metadata before and after, and the result of reconnecting, which must show the line `Ignoring a Protected Update bundle nobody asked for` if any bundle gets sent.
- [ ] **7. Final state.** Read `0xE0E1`'s metadata once more; `C0` must equal step 1's value.
- [ ] **8. Update the threat model** from lesson 1.1. Every STRIDE row needs a status (not done / done / tested and passed). The ETSI table needs evidence or a reason for each row. The remaining-risk section must have at least three items from the Concepts table, each with one line of plan.
- [ ] **9. Check for leaks.** Search your whole report and every attachment for passwords, bundle files, or a private key, before submitting.

**Pass criteria:** every claim in the report carries at least one of the four evidence kinds; steps 3 and 4 each carry a complete set; at least two negative tests are present; and the threat model lists remaining risks, each with a plan.

## Going further

You have completed the Secure IoT with OPTIGA™ Trust M course. Ways to go further:

- Close the template's gaps in your own work — for example, filling in the OTA client's verification (lesson 4.2), or designing CM33_S to verify the next image (lesson 4.1)
- Read [AN237849 Getting started with PSOC™ Edge security](https://www.infineon.com/AN237849) before planning secure-boot provisioning for a real product
- Review the whole connectivity path in [TESAIoT Firmware Stack module 5](../../../tesaiot-firmware-stack/m05-connect-to-platform/README.md), and try the examples on the [TESAIoT Developer Hub](https://dev.tesaiot.dev/)

Back to the [course home](../../README.md)

## Reflect

- Which claim in your report was hardest to find evidence for, and why?
- Which remaining risk would you accept in a real product, and which would you not?
- If you had two minutes to explain this task to a non-engineer executive, what would you say?

## References

- [ETSI EN 303 645 V3.1.3 (2024-09) Cyber Security for Consumer Internet of Things: Baseline Requirements](https://www.etsi.org/deliver/etsi_en/303600_303699/303645/03.01.03_60/en_303645v030103p.pdf)
- [D2 — Enrolment and Protected Update end to end (SDK docs built from commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__d2__enrolment__protected__update.html)
- [C4 — mTLS: the OPTIGA-backed TLS identity (SDK docs built from commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__c4__mtls__optiga.html)
- [C3 — TESAIoT cloud: config file → MQTT task → broker (SDK docs built from commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__c3__cloud__mqtt.html)
- Examples on the Developer Hub: [device-mtls](https://dev.tesaiot.dev/?example=developer-hub--device-mtls&q=device-mtls) · [c_ota_client](https://dev.tesaiot.dev/?example=developer-hub--c_ota_client&q=c_ota_client) · [pse84_tesaiot_client](https://dev.tesaiot.dev/?example=developer-hub--pse84_tesaiot_client&q=pse84_tesaiot_client) (Cypress EULA, link only)
