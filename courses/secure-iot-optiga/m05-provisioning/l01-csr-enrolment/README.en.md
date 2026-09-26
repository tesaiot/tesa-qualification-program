---
id: sec-iot.m05.l01
lang: en
title: {th: ลงทะเบียนด้วย CSR, en: Enrolment with a CSR}
summary: {th: สร้างคำขอใบรับรองจากกุญแจในชิป ส่งให้แพลตฟอร์ม และติดตามคำขอจนได้ใบรับรอง, en: 'Create a certificate request from the on-chip key, send it to the platform and track it to a certificate.'}
level: L3
time_min: {concept: 20, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [sec-iot.m04.l02]
objectives:
- {th: อธิบายเนื้อหาของ CSR และเหตุผลที่กุญแจลับไม่ต้องออกจากชิป, en: Explain what a CSR contains and why the private key never leaves the chip.}
- {th: ติดตามคำขอด้วย correlation id และ OID ปลายทางตามตัวอย่างของ SDK, en: Track a request by correlation id and target OIDs as the SDK example does.}
- {th: ระบุสัญญาเรื่องบัฟเฟอร์ที่ฟังก์ชันส่ง CSR กำหนดให้ผู้เรียก, en: State the buffer contract the CSR publishing function imposes on its caller.}
develops:
- {skill: sec.crypto, to: 3}
- {skill: sec.secure-element, to: 3}
- {skill: iot.cloud-platform, to: 2}
context: {platform: psoc-edge-e84, lang: c, secure_element: optiga-trust-m, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
source:
- {repo: 'https://github.com/tesaiot/tesaiot-pse84-devkit-sdk', path: bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/05_csr_enrolment.c, ref: ef72c1b658178eee8c38b1e47d28b006f80a59b5, license: Apache-2.0}
source_sha256: 9e6c815120dc9fb3c372e982d015fd8d496e3ee494ea511352442228161dc253
---

# Lesson 5.1: Enrolment with a CSR

> Module 5 · Secure device provisioning · [Module overview](../README.md) · [Course home](../../README.md)

A device leaves the factory with a certificate from Infineon that can only prove it is a genuine Trust M (lesson 3.1).
Enrolment means obtaining a certificate that **our platform** issues, tied to that specific device's `device_id`, without the private key ever leaving the chip even once.

## Objectives

By the end of this lesson you will:

1. Explain what a CSR contains, and why the private key does not need to leave the chip
2. Track a request by correlation id and target OIDs, as the SDK's example does
3. State the buffer contract the CSR-publishing function imposes on its caller

## Before you start

- **Already covered:** [Lesson 4.2: Protected Update](../../m04-secure-boot-and-update/l02-protected-update/README.md), and certificates from [lesson 1.2](../../m01-threats-and-crypto/l02-crypto-basics/README.md)
- **On your computer:** `openssl`, and a fresh `lab_key.pem` you can regenerate following lab 1.2, step 5
- **On the board:** the SDK's template, already building. The optional lab that really enrols needs a device that can already reach the platform (lesson 3.2), and the instructor's permission.
- **Read alongside:** [Lesson 5.3 of TESAIoT Firmware Stack: PSoC Edge E84 with the OPTIGA™ Trust M](../../../tesaiot-firmware-stack/m05-connect-to-platform/l03-optiga-mqtt-client/README.md)

## See it work first

When you press HSM Security → Enrol Certificate on the screen, [chapter D2 of the SDK docs](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__d2__enrolment__protected__update.html) says the screen shows these seven sentences, in order.

```text
Connecting to the platform
Generating a key pair inside the secure element
Signing the request with the key that never leaves the chip
Sending the request to the platform
Waiting for the platform
Checking the certificate against the key in the chip
The device can prove it holds the key this certificate names
```

**Guess first:** the third sentence says the request gets "signed." If the request already carries a public key, why sign it at all, and who checks that signature?

## Concepts

### 1. What a CSR is, and why the private key does not need to leave the chip

A CSR (certificate signing request), per [RFC 2986 (PKCS #10)](https://www.rfc-editor.org/rfc/rfc2986), has three main parts:
a **subject** — the name being requested for the certificate, a **public key** being requested for certification, and a **signature** the requester makes over the first two, with the matching private key.

The answer to the guess is that signature. It is a **proof of possession.** The issuer verifies the signature using the public key inside the request; if it verifies, the requester really does hold that pair's private key.
The issuer therefore never needs to see the private key at all. The certificate it issues carries the same subject and public key, plus an issuer and a validity period, signed by the CA.

On our board, chapter D2 states the subject is `CN=<mqtt username>,O=TESAIoT`. The key pair is generated **inside the chip**, and the request is signed with a key that never leaves it.
The full steps, per the header comment of [05_csr_enrolment.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/05_csr_enrolment.c):

1. The device generates a key pair inside the chip, then builds a PEM CSR from the public key (this part is the consumer's job, per the `consumer_must_provide.txt` list)
2. `publish_csr()` wraps the CSR as JSON and publishes it to `device/<id>/commands/csr` on the already-open MQTT session
3. The platform signs it and replies on a different topic — per the SDK's PU contract, `commands/certificate` directly, with no manifest involved
4. The device's subscriber receives the certificate, writes it to the slot, then verifies it matches the key inside the chip (`optiga_verify_cert_key_pair`)

The SDK's [CSR_SUBMISSION_CONTRACT.md](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/modules/tesaiot/docs/CSR_SUBMISSION_CONTRACT.md) opens with rules that have "already cost someone a debugging session."

- **The topic always uses `device_id` (a UUID), never the Trust M's UID.** The UID is the MQTT client id; if you use it in the topic, the broker refuses while the connection itself still looks fine, so the message just seems to vanish.
- **Subscribe to `device/<id>/commands/#` before publishing the CSR.** Replies are not retained; a reply that arrives before the subscription succeeds is gone forever.
- **Someone must tend the session.** With no PINGREQ, the broker closes the session at 90 seconds, and any later reply is lost too.
- **A rejected CSR gets silence.** Nothing replies on the topic at all; the reason lives in the platform's log, and a CSR must be longer than 100 bytes.
- There is also an HTTPS path for administrators or back-end systems holding a JWT, but a device still using its factory certificate uses the MQTT path.

### 2. Tracking a request by correlation id and OID

`05_csr_enrolment.c` explains three readers, **two of which are traps.**

- `trustm_current_correlation_id()` is a new id that `publish_csr()` generates from the TRNG every time it is called. The platform's reply is matched against this id; `NULL` means nothing is outstanding.
- `trustm_requested_target_oid()` and `trustm_requested_anchor_oid()` are the OID pair the most recent **Protected Update** request named.
  `publish_csr()` **does not set either of these.** They are written only by `tesaiot_publish_protected_update()`, and read as `0xE0E1` / `0xE0E8` after a reset.
  After calling `publish_csr()` alone, these two values still describe the previous PU request, or their defaults — never this CSR. Never use them as the sole label for a CSR enrolment.

The reset rule: `trustm_reset_state()` **clears the correlation id.** If called while a reply is still pending, an incoming certificate has nothing left to match against, and gets discarded unread.
Reset when you are done, or when whatever timeout **you** decided on has elapsed — never "just to be tidy." And if you plan to wait for the result with a counter, capture the counter's value **before** publishing, per chapter D2's pitfall 4 —
otherwise a job that had already finished earlier gets counted as this request's answer.

Chapter D2 has one more warning: `trustm_state_t` is only a variable with a timestamp — it is not a state machine, and no `switch` is driven by it.
Four of its values are never written on the normal path (`APPLYING_UPDATE`, `WAITING_FOR_CERTIFICATE`, `COMPLETE`, `APPLYING_FRAGMENTS`); a screen waiting for `COMPLETE` will wait forever.

### 3. The buffer contract of `publish_csr()`

The function's signature, per the [tesaiot_hsm_api docs](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/docs/sdk/tesaiot_hsm/tesaiot_hsm_api.md):

```c
int publish_csr(uint8_t *csr, size_t csr_length, uint16_t target_oid, uint16_t trust_anchor_oid, uint32_t payload_version);
```

The first parameter is `uint8_t *`, not `const uint8_t *`, and example 05 says this is not a typo: `publish_csr()` **builds JSON in place, on top of your own buffer**, to avoid allocating a second large block. The consequences:

1. The buffer must be **writable.** A `const` PEM string that lives in flash will fault.
2. The buffer must be **larger than the CSR.** It has to hold `{"device_id":"<id>","csr":"<CSR with \n escaped>","correlation_id":"<uuid>"}` —
   that is, the CSR plus one extra byte per newline, plus roughly 45 bytes of fixed text, plus the device id and correlation id. The example recommends adding 256 bytes of headroom and not worrying further.
3. `csr_length` is the **length of the CSR**, not the size of the buffer.
4. **Your CSR is gone once the function returns.** The buffer now holds JSON. Keep a copy first if you still need the CSR afterwards.

`trust_anchor_oid` and `payload_version` are accepted but not yet used (reserved). The example still recommends sending the real intended values, so the code stays correct on the day they start to matter.

## Worked example

Taken from [05_csr_enrolment.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/05_csr_enrolment.c), lines 158–172 and 178–184
(TESAIoT PSE84 Dev Kit SDK, © Thai Embedded Systems Association, Apache-2.0)

```c
    /* Refuse rather than publish a fabricated CSR. A CSR the platform signs is
     * a certificate on a real device; the wrong one is worse than none. */
    if (s_csr_len == 0u) {
        printf("  publish_csr() NOT called: s_csr is empty. Build a CSR first —\r\n"
               "    generate the keypair in the chip, then produce the PEM. The\r\n"
               "    archive cannot do this for you (optiga_generate_csr_pem is\r\n"
               "    in consumer_must_provide.txt).\r\n");
        return SDK_EX_NO_DATA;
    }
    if (s_csr_len + 256u > sizeof(s_csr)) {
        printf("  publish_csr() NOT called: %u-byte CSR in a %u-byte buffer "
               "leaves no room for the JSON envelope built in place\r\n",
               (unsigned)s_csr_len, (unsigned)sizeof(s_csr));
        return SDK_EX_REFUSED;
    }
```

```c
    int rc = publish_csr(s_csr, s_csr_len,
                         (uint16_t)EXAMPLE_TARGET_OID,
                         (uint16_t)EXAMPLE_ANCHOR_OID,
                         (uint32_t)EXAMPLE_PAYLOAD_VER);

    /* s_csr now holds the JSON envelope, not the CSR. Do not reuse it as a CSR. */
    s_csr_len = 0u;
```

Three things worth copying into your own work:

1. **Never send a fabricated CSR.** A CSR the platform signs becomes a certificate on a real device — the wrong one is worse than none.
2. **Check the headroom before calling**, using the CSR + 256 bytes rule; the example uses a `static` buffer of 1280 bytes.
3. **Zero the length immediately after calling**, so no one later mistakes the now-JSON buffer for a CSR again.

This example **has publishing disabled by default.** You need a real MQTT session connected to the platform, and a real CSR built from a key inside the chip, before you enable `DEFINES+=EXAMPLE_HSM_PUBLISH_CSR=1`.
The comment gives the reason: a request missing either of those is just noise on someone else's broker.

## Practice

Using example 05's rules, decide for each case whether it is **safe to call `publish_csr()`** or **must be fixed first**, and how you would fix it.

1. `static uint8_t buf[1280];` holding a 620-byte CSR, then calling `publish_csr(buf, 620, 0xE0E1, 0xE0E8, 1)` ____
2. `static const char csr[] = "-----BEGIN CERTIFICATE REQUEST-----\n...";` then calling `publish_csr((uint8_t *)csr, strlen(csr), ...)` ____
3. `static uint8_t buf[700];` holding a 620-byte CSR ____
4. `publish_csr(buf, sizeof(buf), 0xE0E1, 0xE0E8, 1)` where `buf` holds a 620-byte CSR ____
5. After `publish_csr()` returns `0`, the program prints `buf` "to see the CSR that was sent" ____
6. The reply has not arrived yet, but the program calls `trustm_reset_state()` "to start with a clean state" ____

<details><summary>Solution</summary>

1. **Safe to call.** 620 + 256 = 876, which does not exceed 1280.
2. **Must be fixed.** A `const` buffer lives in flash and cannot be written; `publish_csr()` will fault while building JSON on top of it. Copy it into a writable buffer first.
3. **Must be fixed.** 620 + 256 = 876, which exceeds 700 — there is no room for the JSON built in place.
4. **Must be fixed.** `csr_length` must be 620, not the buffer's size.
5. **Must be fixed.** By then, `buf` already holds JSON. Keep a copy before calling if you want to see the CSR afterwards.
6. **Must be fixed.** Resetting clears the correlation id; a certificate arriving afterwards would be discarded. Wait until it is done, or until whatever timeout you actually intended has elapsed.

</details>

## Check your understanding

The questions below are part of the full set in [quiz.yaml](quiz.yaml), which the automated grader uses.

1. Why can the platform issue a certificate without ever seeing the device's private key? *(objective 1)*
   - a) Because the platform can guess the private key from the public key
   - b) Because the CSR carries the public key, and the signature on the CSR proves the requester holds the matching private key
   - c) Because the private key is sent encrypted
   - d) Because certificates have nothing to do with keys

   <details><summary>Solution</summary>

   **b.** This is proof of possession. The issued certificate carries the same public key, so the private key stays inside the chip the whole time.

   </details>

2. After calling only `publish_csr()`, what does `trustm_requested_target_oid()` tell you? *(objective 2)*
   - a) The slot this CSR's certificate will be written to
   - b) The OID from the previous Protected Update request, or its default `0xE0E1` — it says nothing about this CSR
   - c) The chip's UID
   - d) The correlation id

   <details><summary>Solution</summary>

   **b.** This value is written only by `tesaiot_publish_protected_update()`. What tracks a CSR is the correlation id.

   </details>

3. Which of these correctly states `publish_csr()`'s buffer contract? *(objective 3)*
   - a) The buffer can be `const`, and `csr_length` is the buffer's size
   - b) The buffer must be writable, larger than the CSR by enough room for the JSON built on top of it; `csr_length` is the CSR's length; and the CSR is gone after the call
   - c) The function allocates a fresh buffer for you
   - d) The CSR must be sent as DER only

   <details><summary>Solution</summary>

   **b.** Example 05 spells this out in four points, and recommends 256 bytes of headroom.

   </details>

## Lab

**Main lab: track a request without sending it, and read a CSR by eye**

- [ ] Build example 05 without enabling publishing.
  ```bash
  make build ENABLE_PAGE_EXAMPLES=1 SDK_EXAMPLE_CM33=cm33/security/05_csr_enrolment
  make program BENTO_WORKSPACE="$(cd .. && pwd)"
  ```
  Record the lines `correlation id on entry`, `requested target OID`, `requested anchor OID`, the `trustm_update_state` and `trustm_reset_state` lines, and the `SKIPPED publish_csr()` message.
  Explain why the example dares to call `trustm_reset_state()` right there (look at the condition just before it).
- [ ] Build a CSR on your computer from the test key from lesson 1.2, using an obviously fake UUID, then read every part of it.
  ```bash
  openssl ecparam -name prime256v1 -genkey -noout -out lab_key.pem
  openssl req -new -key lab_key.pem -subj "/CN=00000000-0000-0000-0000-000000000000/O=TESAIoT" -out lab.csr
  openssl req -in lab.csr -noout -text
  openssl req -in lab.csr -noout -verify
  ```
  Find the subject, the public key and the signature algorithm in the output. The last line must say self-signature verify OK — this is the proof of possession a CA verifies.
- [ ] Count its size with `wc -c < lab.csr` and its line count with `grep -c '' lab.csr`, then compute how large `publish_csr()`'s buffer would need to be by example 05's formula, and compare it against the +256-byte rule. Delete the test key file afterwards.
- [ ] Draw a sequence diagram of enrolment, showing every relevant MQTT topic (`commands/#`, `commands/csr`, `commands/certificate`), where proof of possession is checked, and where the device verifies the certificate matches its key.

**Optional lab: real enrolment — only with the instructor's permission**

Enrolling creates a new key pair inside the chip; the old key in that slot is gone permanently, and it writes the new certificate to slot `0xE0E1` with a plain write. If that slot is already locked by a Protected Update, the button refuses before doing anything.

- [ ] With the device connected to the platform in its current mode (lesson 3.2), press HSM Security → Enrol Certificate, and record all seven on-screen sentences against "See it work first."
- [ ] Record the `[CSR] Using DIRECT PUBLISH ...` and `[Subscriber] Certificate from platform (N bytes)` UART lines, per chapter D2.
- [ ] Switch to `tls_mode=mtls` and reconnect. Look for the line `[mTLS] device pair verified — using TESAIoT identity` from lesson 3.1, which means the firmware has chosen to use the certificate and key you just enrolled.

## Going further

Enrolment takes several seconds and can wait on the platform for up to a minute. The next lesson looks at how the on-device screen handles work this long without freezing and without going silent.

Next lesson: [Lesson 5.2: On-device provisioning screens](../l02-provisioning-screens/README.md)

## Reflect

- In your own system, where does "resetting state to be clean" cause a later reply to be discarded?
- If a rejected CSR gets no reply at all, how would your team know, and where would you look for evidence?
- Which functions in your own API write over the caller's buffer in a way that the parameter's name or type does not warn you about?

## References

- [SDK: cm33/security/05_csr_enrolment.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/05_csr_enrolment.c)
- [SDK: CSR_SUBMISSION_CONTRACT.md](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/modules/tesaiot/docs/CSR_SUBMISSION_CONTRACT.md)
- [SDK: PROTECTED_UPDATE_CONTRACT.md, section 4.3 (certificates from the CSR path)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/modules/tesaiot/docs/PROTECTED_UPDATE_CONTRACT.md)
- [SDK: tesaiot_hsm_api docs](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/docs/sdk/tesaiot_hsm/tesaiot_hsm_api.md)
- [D2 — Enrolment and Protected Update end to end (SDK docs built from commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__d2__enrolment__protected__update.html)
- [RFC 2986: PKCS #10 Certification Request Syntax](https://www.rfc-editor.org/rfc/rfc2986)
- Examples on the Developer Hub: [PSoC Edge E84 + OPTIGA Trust M: TESAIoT MQTT Client](https://dev.tesaiot.dev/?example=developer-hub--pse84_tesaiot_client&q=pse84_tesaiot_client) (Cypress EULA, link only) · [device-mtls](https://dev.tesaiot.dev/?example=developer-hub--device-mtls&q=device-mtls), whose README notes that a bundle from CSR enrolment carries no private key
