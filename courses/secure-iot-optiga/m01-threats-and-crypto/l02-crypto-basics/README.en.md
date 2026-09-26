---
id: sec-iot.m01.l02
lang: en
title: {th: พื้นฐานวิทยาการเข้ารหัสสำหรับระบบฝังตัว, en: Crypto basics for embedded systems}
summary: {th: 'แยกหน้าที่ของ hash, MAC, ลายเซ็นดิจิทัล การเข้ารหัสสองแบบ และใบรับรอง X.509', en: 'Tell apart hashes, MACs, digital signatures, the two kinds of encryption and X.509 certificates.'}
level: L3
time_min: {concept: 20, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [sec-iot.m01.l01]
objectives:
- {th: เลือกเครื่องมือเข้ารหัสที่เหมาะกับเป้าหมาย ความลับ ความถูกต้อง หรือการยืนยันตัวตน ได้ถูกต้องอย่างน้อย 4 ใน 5 กรณี, en: 'Pick the right primitive for confidentiality, integrity or authenticity in at least 4 of 5 cases.'}
- {th: 'อ่านใบรับรอง X.509 แล้วระบุ subject, issuer, อายุ และ public key ได้', en: 'Read an X.509 certificate and identify subject, issuer, validity and public key.'}
- {th: อธิบายว่าทำไมกุญแจลับควรอยู่ในชิปความปลอดภัยแทนหน่วยความจำแฟลชทั่วไป, en: Explain why private keys belong in a secure element rather than general flash.}
develops:
- {skill: sec.crypto, to: 3}
context: {platform: psoc-edge-e84, lang: c, secure_element: optiga-trust-m, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
slides: slides.md
source:
- {repo: 'https://github.com/tesaiot/tesaiot-pse84-devkit-sdk', path: bento-firmware-template-mtb-only, ref: ef72c1b658178eee8c38b1e47d28b006f80a59b5, license: Apache-2.0}
- {repo: 'https://github.com/Infineon/optiga-trust-m', path: examples/optiga/example_optiga_crypt_ecdsa_sign.c, ref: release-v5.3.0, license: MIT}
source_sha256: b710c1756ff73dfa4897a54c5aea65d278fa169278d96ddffc1f0efb973ac7e4
---

# Lesson 1.2: Crypto basics for embedded systems

> Module 1 · Threat modelling and crypto fundamentals · [Module overview](../README.md) · [Course home](../../README.md)

The STRIDE table in the last lesson was full of the words TLS, certificate and signature. This lesson pulls those tools apart one at a time:
which property each one gives you, which it **cannot** give you, and why a private key belongs in a chip, not in a file.

## Objectives

By the end of this lesson you will:

1. Pick the right cryptographic primitive for a goal — confidentiality, integrity or authentication — correctly in at least 4 of 5 cases
2. Read an X.509 certificate and identify its subject, issuer, validity period and public key
3. Explain why a private key belongs in a secure element rather than in general-purpose flash

## Before you start

- **Already covered:** [Lesson 1.1: Threat modelling an IoT device](../l01-threat-modelling/README.md). Keep your threat model table open beside you.
- **Tools:** a computer with `openssl` on its terminal (already present on Linux and macOS; on Windows use Git Bash or WSL) and internet access.
- **Board:** not needed for this lesson. Every experiment runs on the computer, but the data you read is the real data the board uses.

## See it work first

Open a terminal and ask for the certificate from the same broker the board connects to.

```bash
openssl s_client -connect mqtt.tesaiot.dev:8884 -servername mqtt.tesaiot.dev -showcerts </dev/null
```

The result has two certificates. As this lesson is written (26 Sep 2026), the first has subject `CN = mqtt.tesaiot.dev`, issued by `CN = TESAIoT Intermediate CA`.
The second is `TESAIoT Intermediate CA` itself, issued by `TESAIoT Root CA`. The dates you see may differ, because the server's certificate is renewed periodically.

**Guess first:** which certificate does the board's firmware already have embedded — the server's, the intermediate's, or the root's?
Write your answer down in your learning log, then find out in lab step 3.

## Concepts

### 1. Three goals, four families of tool

When choosing a tool, first ask which property you need: **confidentiality** (others cannot read it), **integrity** (you can tell if it was changed),
or **authentication** (you can tell who created this data). Then pick from the table.

| Tool | Uses what key | Gives you | Cannot give you | On our node |
|---|---|---|---|---|
| A hash, e.g. SHA-256 | No key | A fixed-size fingerprint of the data; change one bit and the whole result changes | No way to know who created it — anyone can recompute it | The pinned CA's fingerprint in the firmware |
| A MAC, e.g. HMAC-SHA256 | One secret key shared by both sides | Integrity, and knowing it came from someone who holds the key | Cannot be proved to a third party, because either side could have created it | The OPTIGA™ Trust M can compute an HMAC (`optiga_crypt_hmac`) |
| A digital signature, e.g. ECDSA P-256 | A key pair — sign with the private key, verify with the public key | Integrity, authentication, and proof that holds up to a third party | Does not hide the data | The CertificateVerify signature in mTLS, the Protected Update manifest |
| Symmetric encryption, e.g. AES | The same secret key for encrypting and decrypting | Confidentiality, and speed | Needs a way to agree on the key first | Data inside a TLS record |
| Asymmetric key agreement, e.g. ECDHE | A temporary key pair on each side | A shared secret key without ever sending a key over the wire | Does not verify who the other side is — needs a signature alongside it | The `ECDHE` part of the ciphersuite name |

A real example of the pitfall here is in the SDK's [02_model_signature_hook.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/02_model_signature_hook.c).
The function that verifies an AI model's signature fully checks the CRC of the file's trailer, but still returns "could not verify" (`-10`), not "passed" (`+1`).
The comment in the file explains why: returning pass because the CRC matches would turn a signature into a checksum, because anyone can recompute a CRC and overwrite it.
A cryptographic hash like SHA-256 has exactly the same problem if no key is involved.

### 2. X.509 certificates and the chain of trust

An X.509 certificate ([RFC 5280](https://www.rfc-editor.org/rfc/rfc5280)) is a document in which the issuer signs a statement that
"this public key belongs to this subject, during this period." There are four fields you need to be able to read.

- **subject** — the certificate's owner, e.g. `CN = mqtt.tesaiot.dev`
- **issuer** — whoever signed this certificate, e.g. `CN = TESAIoT Intermediate CA`
- **validity** — the period from `notBefore` to `notAfter`
- **subjectPublicKeyInfo** — the subject's algorithm and public key

The broker's chain is: the server's certificate ← TESAIoT Intermediate CA ← TESAIoT Root CA. The device can trust the server's certificate
because it can walk the signatures back up until it reaches a certificate it already trusts in its firmware — that certificate is called the **trust anchor**.

The device side also has two sets of its own certificates, as recorded in [chapter C4 of the SDK docs](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__c4__mtls__optiga.html) and in `mqtt_mtls_setup.c`.

- The factory certificate in slot `0xE0E0` has subject `CN=InfineonIoTNode`, **identical on every chip**, issued by `Infineon OPTIGA(TM) Trust M CA 300`.
  The only fields that differ per chip are the serial number and the public key, so this certificate proves "this is a genuine Trust M," but not which device it is.
- TESAIoT's own certificate in slot `0xE0E1`, obtained after enrolment, has the `device_id` as its subject, issued by `TESAIoT MCU CA`.

There is something you need to know about **validity**: in the mbedTLS configuration for CM33_NS at this commit
([mbedtls_user_config.h](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/configs/mbedtls_user_config.h)),
the option `MBEDTLS_HAVE_TIME_DATE` is disabled, which, as the same file's comment explains, is the part that checks a certificate's validity period.
CRL parsing (`MBEDTLS_X509_CRL_PARSE_C`) is disabled too. With this configuration, the device does not reject a certificate for being expired or revoked.
Write this down in the "remaining risk" section of your threat model.

### 3. Why a private key belongs in a chip

A private key in a file or in flash can be read out in several ways: whoever holds the firmware image, whoever can plug into the debug port, or whoever can
desolder the flash chip and read it, walks away with the key too. Once they have it, they are your device in every respect — they can make as many copies as they like.
This is why ETSI EN 303 645 provision 5.4-1 requires security parameters to be stored securely, and cites a secure element as one example.

The OPTIGA™ Trust M changes the question from "where is the key" to "who can tell the chip to use the key."

- The key is **generated inside the chip** and there is no command to read it out. In Infineon's example dump ([trust_m3_json.txt](https://github.com/Infineon/optiga-trust-m-overview/blob/a45b86bda014efeebfb85f084f779cedb07b32dc/data/object_dumps/trust_m3_json.txt), MIT),
  slot `0xE0F0`'s metadata has only Change = never and Execute = always — no read permission at all.
- A program sends the key's **slot name** (its OID) together with a digest, and gets a signature back, as in the example in the next section.
- The chip's hardware is certified to Common Criteria EAL6+ (high), as [Infineon states](https://github.com/Infineon/optiga-trust-m-overview), so it resists physical attack far better than ordinary flash.

And it is just as important to be complete about what the chip does **not** protect against.

- If the firmware on the MCU is compromised, the attacker can ask the chip to sign anything, for as long as they control the board. The chip prevents the key from being **stolen or cloned**, not **misused** while the board itself is compromised.
- The I2C wire between the MCU and the chip is not encrypted in the SDK's default configuration (`OPTIGA_COMMS_DEFAULT_PROTECTION_LEVEL` is `OPTIGA_COMMS_NO_PROTECTION` in `optiga_lib_config_mtb.h`).
  The key itself never travels on the wire, but the digest and the signature do. Infineon offers a Shielded Connection feature for cases where you need to guard against tapping this wire.

## Worked example

Here is a signature made with a key inside the chip, taken from Infineon's example
([example_optiga_crypt_ecdsa_sign.c @ release-v5.3.0](https://github.com/Infineon/optiga-trust-m/blob/release-v5.3.0/examples/optiga/example_optiga_crypt_ecdsa_sign.c), lines 80–93, © 2021-2024 Infineon Technologies AG, MIT).
The board's SDK uses this version of the host library, per the `proj_cm55/deps/optiga-trust-m.mtb` file.

```c
/* SPDX-FileCopyrightText: 2021-2024 Infineon Technologies AG
 * SPDX-License-Identifier: MIT */
        /**
         * 2. Sign the digest using Private key from Key Store ID E0F0
         */
        optiga_lib_status = OPTIGA_LIB_BUSY;
        return_status = optiga_crypt_ecdsa_sign(
            me,
            digest,
            sizeof(digest),
            OPTIGA_KEY_ID_E0F0,
            signature,
            &signature_length
        );

        WAIT_AND_CHECK_STATUS(return_status, optiga_lib_status);
```

Reading it piece by piece:

- `digest` is the 32-byte SHA-256 of the data — the signature is over the digest, not over the raw data
- `OPTIGA_KEY_ID_E0F0` is the key's **slot name**, not the key itself — at no point does the key appear in the MCU's RAM
- `signature` is the result that comes out — it is public data; anyone can verify it with the public key
- This call is **asynchronous**: it returns immediately, and the real result arrives through a callback that sets `optiga_lib_status`, with `WAIT_AND_CHECK_STATUS` waiting for that value to stop being `OPTIGA_LIB_BUSY`.
  We will come back to this in lesson 2.2, on why you must hold the chip's access gate for the whole wait.

In the board's firmware, the same job lives in `trustm_ecdsa_sign()`, which TLS calls when building CertificateVerify (lesson 3.1).

## Practice

Pick one tool per scenario, and say which property it provides. This is the rubric for objective 1 — you need at least 4 of 5 correct.

1. The platform sends the device a new certificate, and the device must be sure it really came from the platform, not from someone else. ____
2. You need to keep the CA's "fingerprint" in a document, so someone else can compare it against the certificate the server sends. ____
3. A temperature reading crossing a coffee shop's WiFi must not be readable by the person at the next table. ____
4. Two sensors from the same company already share a secret key, and need to know a message was not altered in transit. ____
5. A device and a server need to end up with a shared AES key, without ever sending that key across the network. ____

<details><summary>Solution</summary>

1. **A digital signature** gives integrity and authentication — this is the basis of Protected Update in lesson 4.2
2. **A hash (SHA-256)** — a fingerprint needs no key, because the trust comes from the channel through which you obtained this value (a document you already trust)
3. **Symmetric encryption**, e.g. AES inside TLS, gives confidentiality
4. **A MAC (HMAC)** — once you already share a key, a MAC is faster than a signature, but it cannot be proved to a third party
5. **Key agreement (ECDHE)** — gives a shared key without sending it, but needs a signature alongside it, otherwise you might agree a key with an attacker in the middle

</details>

## Check your understanding

The questions below are part of the full set in [quiz.yaml](quiz.yaml), which the automated grader uses.

1. Why does the signature-verification function in `02_model_signature_hook.c` not return "passed," even when the file trailer's CRC is correct? *(objective 1)*
   - a) Because CRC is too slow
   - b) Because anyone can recompute a CRC — it tells you the data was not corrupted in transit, but not who wrote it
   - c) Because CRC needs a secret key
   - d) Because CRC only works on already-encrypted data

   <details><summary>Solution</summary>

   **b.** Verifying who created something needs a key. Without a key-based check, returning "passed" is lying about having verified it.

   </details>

2. The factory certificate in slot `0xE0E0` has subject `CN=InfineonIoTNode` on every chip. Which conclusion is correct? *(objective 2)*
   - a) This certificate can tell you which device it is
   - b) This certificate is definitely forged
   - c) This certificate proves it is a genuine Trust M, but you need the serial number or public key to tell devices apart
   - d) This certificate has no public key

   <details><summary>Solution</summary>

   **c.** The only fields that differ per chip are the serial number and the public key. To bind a permission to a specific device, bind it to those two values, not to the subject.

   </details>

3. Which of these describes something the OPTIGA™ Trust M does **not** protect against? *(objective 3)*
   - a) Reading out the private key to copy it
   - b) A key being used to sign something by firmware that has already been compromised, while the attacker still controls the board
   - c) Desoldering the flash chip to read the key
   - d) Recovering the key from a firmware image file

   <details><summary>Solution</summary>

   **b.** The chip does whatever the connected MCU tells it to. It prevents the key from being stolen, but it has no way to know whether the MCU itself has been compromised.

   </details>

4. In the mbedTLS configuration for CM33_NS at commit `ef72c1b`, will the device reject an expired server certificate? *(objective 2)*
   - a) It always rejects it
   - b) No, not for date reasons, because `MBEDTLS_HAVE_TIME_DATE` is disabled
   - c) Only rejects it if there is a CRL
   - d) It depends on the broker

   <details><summary>Solution</summary>

   **b.** This configuration disables checking a certificate's validity period, and disables CRL parsing too. It must be recorded as a remaining risk.

   </details>

## Lab

**Read a real certificate, make a real signature.** Write down every result in your learning log.

- [ ] **1. Capture the chain.** Save the certificates the broker sends into a file.
  ```bash
  openssl s_client -connect mqtt.tesaiot.dev:8884 -servername mqtt.tesaiot.dev -showcerts </dev/null 2>/dev/null \
    | awk '/BEGIN CERT/,/END CERT/' > chain.pem
  csplit -s -z -f cert chain.pem '/-----BEGIN CERTIFICATE-----/' '{*}'
  ```
- [ ] **2. Read the four fields** of each certificate (`cert00`, `cert01`), and fill in a table of subject, issuer, notBefore, notAfter and key algorithm.
  ```bash
  openssl x509 -in cert00 -noout -subject -issuer -dates
  openssl x509 -in cert00 -noout -text | grep -A1 'Public Key Algorithm'
  ```
- [ ] **3. Compare against the firmware's trust anchor.** Compute the SHA-256 fingerprint of the intermediate certificate, and compare it against the value
  `e3ff5011703755b697227a17945837b7b43616a060d14b37995b62c24e0d7e98` that the SDK records in
  [tesaiot_config_defaults.h](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/modules/tesaiot_config/tesaiot_config_defaults.h)
  as the value of the CA pinned in `tesaiot_root_ca.h`.
  ```bash
  openssl x509 -in cert01 -noout -fingerprint -sha256
  ```
  Do they match? And was your guess in "See it work first" correct?
- [ ] **4. Hash vs. MAC.** Change one character in a message and see how much the result changes. Then try an HMAC with a test key.
  ```bash
  printf 'temp=25.0' | openssl dgst -sha256
  printf 'temp=25.1' | openssl dgst -sha256
  printf 'temp=25.0' | openssl dgst -sha256 -hmac lab-key-not-a-secret
  ```
- [ ] **5. Signature.** Generate a P-256 key pair on your computer, sign, verify, then change the message and verify again.
  ```bash
  printf 'temp=25.0' > msg.txt
  openssl ecparam -name prime256v1 -genkey -noout -out lab_key.pem
  openssl ec -in lab_key.pem -pubout -out lab_pub.pem
  openssl dgst -sha256 -sign lab_key.pem -out msg.sig msg.txt
  openssl dgst -sha256 -verify lab_pub.pem -signature msg.sig msg.txt
  printf 'temp=99.9' > msg.txt
  openssl dgst -sha256 -verify lab_pub.pem -signature msg.sig msg.txt
  ```
  The first check must say `Verified OK`; the second must say `Verification failure`.
- [ ] **6. Ask yourself.** The file `lab_key.pem` sits on your disk. Anyone who can copy this file could sign anything in your place.
  Write two or three sentences on how the OPTIGA™ Trust M changes this on the board, and what risk still remains. Then delete the test key file.

## Going further

We have seen how the chip lets a key stay put without ever coming out. The next lesson opens up the real chip on the TESAIoT Dev Kit — what objects live inside it, what the metadata tells you,
and which commands change the chip in ways that cannot be undone.

Next lesson: [Lesson 2.1: What the secure element does for us](../../m02-optiga-trust-m/l01-secure-element-role/README.md)

## Reflect

- In past work, have you ever used a hash or a CRC where you actually needed authentication?
- If your device does not know the current date, how would you handle an expired certificate?
- Who in your organisation can access the firmware image file, and if the key lives inside it, how many people could effectively "become your device"?

## References

- [RFC 5280: Internet X.509 Public Key Infrastructure Certificate and CRL Profile](https://www.rfc-editor.org/rfc/rfc5280)
- [Security / HSM (SDK docs built from commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__feat__security.html)
- [C4 — mTLS: the OPTIGA-backed TLS identity (SDK docs built from commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__c4__mtls__optiga.html)
- [SDK: cm33/security/02_model_signature_hook.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/02_model_signature_hook.c) (Apache-2.0)
- [SDK: proj_cm33_ns/configs/mbedtls_user_config.h](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/configs/mbedtls_user_config.h)
- [Infineon optiga-trust-m (host library, MIT) @ release-v5.3.0](https://github.com/Infineon/optiga-trust-m/tree/release-v5.3.0), the version the SDK uses
- [Infineon optiga-trust-m-overview (MIT): chip features and a sample object dump](https://github.com/Infineon/optiga-trust-m-overview/tree/a45b86bda014efeebfb85f084f779cedb07b32dc)
- [ETSI EN 303 645 V3.1.3 (2024-09)](https://www.etsi.org/deliver/etsi_en/303600_303699/303645/03.01.03_60/en_303645v030103p.pdf), provision 5.4
