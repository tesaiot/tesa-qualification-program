---
id: sec-iot.m03.l01
lang: en
title: {th: TLS และ mTLS, en: TLS and mTLS}
summary: {th: เข้าใจ handshake ของ TLS 1.3 และสิ่งที่เพิ่มขึ้นเมื่ออุปกรณ์ต้องยืนยันตัวตนด้วยใบรับรองของตัวเอง, en: Understand the TLS 1.3 handshake and what changes when the device authenticates with its own certificate.}
level: L3
time_min: {concept: 20, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [sec-iot.m02.l02]
objectives:
- {th: วาดขั้นตอน handshake ของ TLS 1.3 และระบุขั้นที่เซิร์ฟเวอร์และอุปกรณ์พิสูจน์ตัวตน, en: Draw the TLS 1.3 handshake and mark where server and device prove their identity.}
- {th: อธิบายว่าเมื่อใช้ชิปความปลอดภัย การลงลายเซ็นระหว่าง handshake เกิดขึ้นในชิปโดยกุญแจลับไม่ออกมา, en: Explain that with a secure element the handshake signature happens inside the chip and the private key never leaves.}
- {th: วินิจฉัยสาเหตุของการเชื่อมต่อ TLS ล้มเหลวที่พบบ่อยอย่างน้อยสามแบบ, en: Diagnose at least three common causes of TLS connection failure.}
develops:
- {skill: sec.tls, to: 3}
- {skill: sec.crypto, to: 3}
context: {platform: psoc-edge-e84, lang: c, secure_element: optiga-trust-m, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
slides: slides.md
source:
- {repo: 'https://github.com/tesaiot/tesaiot-pse84-devkit-sdk', path: bento-firmware-template-mtb-only, ref: ef72c1b658178eee8c38b1e47d28b006f80a59b5, license: Apache-2.0}
- {repo: 'https://github.com/tesaiot/developer-hub', path: examples/embedded-devices/intermediate/device-mtls, ref: d2ed42c4a31232f553b6b8cef9ee7373db348c21, license: Apache-2.0}
source_sha256: 5c9a2da3bf6e81c88c38add984a8d445eac91966fe9fa7a6c745daf7aaadca63
---

# Lesson 3.1: TLS and mTLS

> Module 3 · mTLS to the TESAIoT Platform · [Module overview](../README.md) · [Course home](../../README.md)

TLS is the reason our telemetry can cross a coffee shop's WiFi without anyone reading or altering it along the way.
mTLS adds one more thing: it has the **device** prove itself with its own certificate too. This lesson walks the handshake message by message,
points out exactly where the secure element gets called, and practises reading the symptoms when a connection fails.

## Objectives

By the end of this lesson you will:

1. Draw the TLS 1.3 handshake and mark where the server and the device each prove their identity
2. Explain that, with a secure element, the handshake signature happens inside the chip and the private key never leaves
3. Diagnose at least three common causes of TLS connection failure

## Before you start

- **Already covered:** [Lesson 2.2: The chip-access discipline](../../m02-optiga-trust-m/l02-chip-access-discipline/README.md), and the `cert01` file whose fingerprint you already verified in the [lesson 1.2](../../m01-threats-and-crypto/l02-crypto-basics/README.md) lab
- **Tools:** `openssl` on your computer. This lesson's main lab runs on a computer; the on-board part is an optional lab for anyone whose device is already registered with the platform.
- **If you do the optional on-board lab:** the SDK's template needs every patch under `third_party_patches/` applied, following the steps in
  [third_party_patches/README.md](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/third_party_patches/README.md),
  and verified with `PATCHED.sha256` — every line must read `OK`. That README warns that without the `secure-sockets/0003` patch, the firmware still builds and runs, but mTLS will not use the key inside the chip, and the broker will reject the device.
- **Read alongside:** [Lesson 5.2 of TESAIoT Firmware Stack: Mutual authentication with mTLS](../../../tesaiot-firmware-stack/m05-connect-to-platform/l02-mtls/README.md), which uses the computer-side example.

## See it work first

Here is the UART log while the board connects with mTLS, per [chapter C4 of the SDK docs](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__c4__mtls__optiga.html) (text as in the source; real values replace `%`).

```text
[MQTT] Waiting for WiFi...
[MQTT] WiFi connected
[MQTT] Start request received
[MQTT-Config] Mode=0, Broker=%s:8883, Client=%s, User=%s, PassLen=%u
[mTLS] Setting up OPTIGA Trust M (cert=0xE0E0, key=0xE0F0)
[mTLS] Certificate read: %u bytes PEM
[mTLS] OPTIGA Trust M setup complete (key_id=%lu)
[MQTT] Instance created
[MQTT] Connecting to '%s:8883' as '%s'...
[PSA-Sign] Using Key OID 0xE0F0 for TLS CertificateVerify (slot=%lu)
[MQTT] Connected to broker
```

**Guess first:** which line marks the moment the chip signs, and does that line, on its own, prove the signature **succeeded**?
Write your answer down, then compare it in Concepts section 2.

## Concepts

### 1. The TLS 1.3 handshake, and where each side proves itself

This diagram summarises [RFC 8446](https://www.rfc-editor.org/rfc/rfc8446) section 2. Messages in curly braces `{}` are already encrypted with the handshake key.

```text
 Device (client)                                         broker (server)
 ClientHello + key_share + signature_algorithms  ──────▶
                                                  ◀──────  ServerHello + key_share
                                                           {EncryptedExtensions}
                                                           {CertificateRequest}   ← present only when the server asks for mTLS
                                                           {Certificate}          ← the server's certificate and chain
                                                           {CertificateVerify}    ← the server signs the transcript
                                                  ◀──────  {Finished}
 {Certificate}          ← mTLS: the device's certificate
 {CertificateVerify}    ← mTLS: the device signs the transcript (inside the chip)
 {Finished}                                     ──────▶
 [Application Data: MQTT CONNECT, PUBLISH ...]  ◀─────▶  [Application Data]
```

**The server proves itself** with three messages: `Certificate` states who it claims to be, and the device walks the chain up to its pinned trust anchor.
`CertificateVerify` is a signature over the hash of the entire conversation so far, proving the server really holds that certificate's private key.
And `Finished` confirms that both sides saw the same conversation.

**The device proves itself** only if the server sends a `CertificateRequest` — that is mTLS. The device answers with its own `Certificate` and `CertificateVerify`.
In server-TLS mode there is no `CertificateRequest`, so the device authenticates later instead, inside MQTT CONNECT, with a username and password that travel inside the already-encrypted channel.

**A fact worth separating out:** the broker `mqtt.tesaiot.dev` can speak TLS 1.3 (you will see this in the lab), but CM33_NS's mbedTLS configuration at commit `ef72c1b`
enables only `MBEDTLS_SSL_PROTO_TLS1_2` and disables `MBEDTLS_SSL_PROTO_TLS1_3`. The comment in the file gives the reason: TLS 1.3 needs PSA crypto, which conflicted with WiFi at the time.
So the board speaks **TLS 1.2** with the broker, which differs from 1.3 in two ways that matter for security.

- In 1.2, the server signs the ECDHE parameters inside the `ServerKeyExchange` message; it never sends a `CertificateVerify`
- In 1.2, both sides' certificates travel **unencrypted.** Anyone who can capture packets can read the device's certificate; if its subject carries the `device_id`, whoever captured it now knows which device it is. In 1.3 this part is already encrypted.

On the device side in 1.2, it sends `Certificate`, then `ClientKeyExchange`, then `CertificateVerify` — the chip's signature is still on this last message, exactly as before.

### 2. The signature happens inside the chip; the key never comes out

Chapter C4 walks the whole path. The function `mqtt_mtls_setup_optiga()` in
[mqtt_mtls_setup.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/modules/tesaiot_mqtt/mqtt_mtls_setup.c)
prepares everything before the handshake, in this order (summarised, not quoted):

1. Hold a touch-hold with the reason "Preparing secure element for mTLS", open OPTIGA's application, and call `optiga_manager_init()` **before** any TLS work
2. Choose an identity: if `optiga_verify_cert_key_pair(0xE0E1, 0xE0F1)` confirms that TESAIoT's certificate and key are really a matching pair, use that pair; otherwise fall back to the factory pair, `0xE0E0` / `0xE0F0`
3. Read the certificate from the chosen slot as PEM, and hand it to the TLS stack with `cy_tls_set_client_cert()`
4. Register the chip's driver with PSA and create an **opaque key handle**, ECC P-256, sign-only, at location `PSA_KEY_LOCATION_OPTIGA`.
   `psa_generate_key()` here does not create a key inside the chip — it only registers a **name** that the driver translates into the key's OID
5. Hand the handle to the TLS stack with `cy_tls_set_optiga_key_id()`, which comes from the secure-sockets patch

During the handshake, when `CertificateVerify` needs to be built, mbedTLS calls PSA, PSA forwards to the driver's `optiga_psa_sign()`, and the driver calls `trustm_ecdsa_sign()` with the key's OID and the hash.
That function holds the gate and the touch-hold for the entire signature (the discipline from lesson 2.2) — at no point on this path does a byte of the private key leave the chip.

If the ciphersuite uses SHA-384, the driver truncates the hash to its leftmost 256 bits before sending it to the chip, and the key handle's policy is set to `PSA_ALG_ECDSA(PSA_ALG_ANY_HASH)` to allow for this case.

**The answer to the guess:** the `[PSA-Sign] Using Key OID ...` line is printed **before** the signature happens. Chapter C4 stresses that it means only "starting to sign with the OID we found."
The signal that it succeeded is that line **and** no `[PSA-Sign] ERROR: trustm_ecdsa_sign status=0x....` line following it **and** getting `[MQTT] Connected to broker`.
(The log above is the factory-pair case; if TESAIoT's pair passes verification, the log instead carries `[mTLS] device pair verified — using TESAIoT identity`, with OID `0xE0F1`.)

Chapter C4 also gives a way to prove the chip really is the one signing: remove the chip from the bus, then reconnect. The result is that the mTLS setup fails and there is no connection, because **there is no backup private key in flash to fall back on.**
This step touches the board's hardware, so this course has you read the result from the docs rather than doing it yourself.

**What mTLS proves, and what it does not.** If the device uses the factory pair, the certificate `CN=InfineonIoTNode` is identical on every chip, so the handshake proves only that this is a genuine Trust M.
Chapter C4 concludes that, at the firmware level, nothing binds the identity the device claims (its client id, its `device_id`) to the certificate it presents. The real decision-maker lives on the broker side —
the ACL that grants access to `device/{id}/#` only to a client whose certificate is pinned by public-key fingerprint or serial number, not by subject.
After enrolment (lesson 5.1), the certificate in slot `0xE0E1` carries the `device_id` as its subject, issued by `TESAIoT MCU CA`, which binds identity far more tightly.

And things that neither plain TLS nor mTLS **protect against:**

- Data at rest on the device or on the platform — TLS protects only data in transit
- An endpoint that has already been compromised, whether the device or the broker
- A misconfigured ACL — mTLS tells you "who," but the ACL tells you "what they can do"
- An expired or revoked certificate, in this commit's mbedTLS configuration for CM33_NS (lesson 1.2)
- A connection that does not verify the server's certificate at all, such as the HTTPS path in [03_https_session.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/connectivity/03_https_session.c), whose comment says it sets `CY_AWS_ROOTCA_VERIFY_NONE`.
  Data is still encrypted, but this only stops a passive eavesdropper, not an active attacker in the middle.

### 3. Reading the symptoms when a connection fails

This table collects the symptoms the SDK and the Developer Hub examples have recorded from real experiments. Read the log first — do not guess yet.

| Symptom | Cause | How to check or fix it |
|---|---|---|
| The handshake fails before MQTT CONNECT, in a way that does not look like a password problem | The trust anchor in the firmware does not match the broker's CA (see the comment in `tesaiot_root_ca.h`) | Compare the CA fingerprint the broker sends against the pinned value, the way lab 1.2 did |
| The device sends Certificate and ClientKeyExchange, then closes the connection with no CertificateVerify; mbedTLS reports `-0x4F80` | `optiga_manager_init()` was never called before TLS, so the signature fails right at asking for the gate | Per chapter C4's pitfall 3, you must init before any TLS work |
| `psa_sign_hash()` refuses with `PSA_ERROR_NOT_PERMITTED (-133)`, no CertificateVerify | The key's policy allows only SHA-256, but the negotiated ciphersuite uses SHA-384 | Use policy `PSA_ALG_ECDSA(PSA_ALG_ANY_HASH)` (CSR contract section 5.2, and the comment in `mqtt_mtls_setup.c`) |
| `[PSA-Sign] ERROR: trustm_ecdsa_sign status=0x0102` | The chip and the touchscreen collided on I2C | touch-hold does not wrap the whole transaction, or something issued a raw resume (lesson 2.2) |
| TLS closes the connection after CONNECT, in server-TLS mode | You connected to port 8883, which is mTLS's port | server-TLS uses 8884, per the device-servertls README; on the board the port comes from `tls_mode`, not from a `port=` setting |
| The first connection of a boot succeeds; a later one, after a disconnect, fails with `-0x3E80` | TLS teardown has already destroyed the PSA key handle | Current firmware detects this and re-registers it. If you see the log line `PSA key ... no longer exists` and then the connection succeeds anyway, this is normal |

## Worked example

The [device-mtls](https://github.com/tesaiot/developer-hub/tree/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/intermediate/device-mtls) example on the Developer Hub
does the same mTLS on a computer (C, with Mongoose). Taken from
[main.c](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/intermediate/device-mtls/main.c), lines 335–343 and 385–387
(© 2025 TESAIoT Platform (TESA), Apache-2.0)

```c
  /* Resolve credential files */
  char ca[512], crt[512], key[512];
  join_path(ca,  sizeof(ca),  certs_dir, FILE_CA_CHAIN);
  join_path(crt, sizeof(crt), certs_dir, FILE_CLIENT_CERT);
  join_path(key, sizeof(key), certs_dir, FILE_CLIENT_KEY);
  if (!(file_exists(crt) && file_exists(key))) {
    (void)fprintf(stderr, "mTLS requires client_cert.pem and client_key.pem in %s\n", certs_dir);
    return 1;
  }
```

```c
  /* Mongoose TLS base conf (we may tweak CA per mode below) */
  iot_tls_conf_t tls; (void)memset(&tls, 0, sizeof(tls));
  tls.client_cert = crt; tls.client_key = key;
```

Compare the two worlds. On a computer, the private key is a **file**, `client_key.pem`, that the TLS library reads into RAM — whoever can copy the file can become this device.
On the board, the equivalent line in the code is `cy_tls_set_optiga_key_id()`, which sends only the key's **name**, and every signature then runs inside the chip.
This example's own README also notes that the bundle produced by CSR enrolment never carries the private key in its ZIP, for exactly this security reason.

One more thing worth noticing in the same file: the MQTTs path sets `tls.ca_chain = NULL` to use the operating system's trust store. The comment was written back when the platform still used a domain with a public CA.
The broker `mqtt.tesaiot.dev`, which we met in lesson 1.2, uses TESAIoT's own CA, which is not in the OS trust store. To use this example against this broker, you must point `ca_chain` at a verified CA file instead.
Lab step 4 will let you see this symptom for yourself.

Try opening the examples on the Developer Hub:

- [TESA IoT Device → Platform (mTLS) — HTTPS or MQTTS via Mongoose](https://dev.tesaiot.dev/?example=developer-hub--device-mtls&q=device-mtls)
- [TESA IoT Device → Platform (Server-TLS) — HTTPS or MQTTS via Mongoose](https://dev.tesaiot.dev/?example=developer-hub--device-servertls&q=device-servertls), to compare against server-TLS mode

## Practice

Order the TLS 1.3 mTLS handshake messages correctly, then mark each message **S** if the server proves itself with it, or **D** if the device does.

`Finished (device)` · `ServerHello` · `CertificateVerify (device)` · `ClientHello` · `Certificate (server)` · `CertificateRequest` · `Certificate (device)` · `CertificateVerify (server)` · `EncryptedExtensions` · `Finished (server)`

<details><summary>Solution</summary>

1. `ClientHello`
2. `ServerHello`
3. `EncryptedExtensions`
4. `CertificateRequest` (the server is asking the device to prove itself; this message alone proves nothing yet)
5. `Certificate (server)` **S**
6. `CertificateVerify (server)` **S**
7. `Finished (server)` **S** — confirms the conversation was not tampered with
8. `Certificate (device)` **D**
9. `CertificateVerify (device)` **D** — this is the message the OPTIGA™ Trust M signs
10. `Finished (device)` **D**

</details>

## Check your understanding

The questions below are part of the full set in [quiz.yaml](quiz.yaml), which the automated grader uses.

1. In mTLS, which message proves the device really holds the certificate's private key? *(objective 1)*
   - a) ClientHello
   - b) Certificate
   - c) CertificateVerify
   - d) EncryptedExtensions

   <details><summary>Solution</summary>

   **c.** `Certificate` only states who it claims to be — anyone could send someone else's certificate. `CertificateVerify` is a signature over the transcript that only whoever holds the private key can produce.

   </details>

2. What does `psa_generate_key()` do inside `mqtt_mtls_setup_optiga()`? *(objective 2)*
   - a) Creates a new key pair inside the chip on every connection
   - b) Copies the private key out of the chip into RAM
   - c) Registers an opaque handle that the driver translates into the key's OID inside the chip — it creates nothing inside the chip
   - d) Creates an AES key for the TLS record

   <details><summary>Solution</summary>

   **c.** Chapter C4 states that this handle holds no key material at all — only the name of a key that already lives inside the chip.

   </details>

3. The log shows `[PSA-Sign] Using Key OID 0xE0F1 for TLS CertificateVerify`, and then the connection closes. Which conclusion is correct? *(objective 3)*
   - a) The chip signed successfully; the problem must be on the broker
   - b) This line is printed before the signature happens — you must check whether an ERROR line from `trustm_ecdsa_sign` follows before concluding anything
   - c) The key has leaked out of the chip
   - d) You must switch the port to 8884

   <details><summary>Solution</summary>

   **b.** This line only means signing has started. If it is followed by `status=0x0102`, go back to lesson 2.2. If there is no ERROR line, look next at the broker side and its ACL.

   </details>

4. Why, in TLS 1.2, can someone capturing packets learn which device it is, even though the MQTT data is encrypted? *(objective 1)*
   - a) Because the password is sent unencrypted
   - b) Because both sides' certificates travel unencrypted during the TLS 1.2 handshake
   - c) Because TLS 1.2 has no encryption at all
   - d) Because MQTT CONNECT sits outside TLS

   <details><summary>Solution</summary>

   **b.** In TLS 1.3 the certificates are already inside the encrypted part. This belongs in the "remaining risk" section of your threat model, because the firmware at this commit speaks TLS 1.2.

   </details>

## Lab

**See a real handshake from your own computer.** Use the `cert01` file whose fingerprint you already matched against the SDK (lab 1.2, step 3) as your trust anchor.

- [ ] **1. Server-TLS on TLS 1.3.** Watch the state message by message, and map each line to the diagram in Concepts section 1.
  ```bash
  openssl s_client -connect mqtt.tesaiot.dev:8884 -servername mqtt.tesaiot.dev \
    -state -CAfile cert01 -partial_chain </dev/null 2>&1 | grep -E '^SSL_connect|Verify return'
  ```
  You must see `read server certificate`, followed by `TLSv1.3 read server certificate verify`, and `Verify return code: 0 (ok)`. Circle the lines where the server proves itself.
- [ ] **2. Force TLS 1.2, the way the board does.** Add `-tls1_2` to the same command. Which line disappears, and which one appears instead (look for `read server key exchange`)? Write down where the server signs in 1.2.
- [ ] **3. The mTLS port without a device certificate.** Connect to port 8883 the same way.
  ```bash
  openssl s_client -connect mqtt.tesaiot.dev:8883 -servername mqtt.tesaiot.dev \
    -state -CAfile cert01 -partial_chain </dev/null 2>&1 | grep -E '^SSL_connect|alert|Verify return'
  ```
  Find the line `read server certificate request`, and see how the server responds when the device (here, openssl) has no certificate to give. Try again with `-tls1_2` and compare the alert message between the two versions.
- [ ] **4. Forget the trust anchor.** Rerun step 1 without `-CAfile cert01 -partial_chain`. Record the `Verify return code`, then explain what happens if your own device or program has no copy of this CA.
- [ ] **5. Diagnose.** Pick three rows from the Concepts section 3 table. Write down how you would reproduce each symptom (on a computer or on the board), and where you would look for evidence.
- [ ] **Optional on-board lab:** if your device already has a `device_id` on the platform and every patch is applied, set `tls_mode=mtls` in the `/.tesaiot_config` file, then trigger a connection from the TESAIoT page on the screen.
  Record every log line starting with `[mTLS]` and `[PSA-Sign]`, and decide, by the three criteria in Concepts section 2, whether the signature succeeded. Lesson 3.2 will walk through configuring this file in more detail.

## Going further

We now know how the secure channel works. The next lesson follows the whole data path — from the configuration file on the board, through the MQTT task, to the broker —
including joining WiFi with credentials from storage, and comparing MQTTs against HTTPS.

Next lesson: [Lesson 3.2: MQTTs to the TESAIoT Platform](../l02-mqtts-to-tesaiot/README.md)

## Reflect

- In your own work, if a device's certificate travels unencrypted during the handshake, who benefits from that information?
- If mTLS already proves the device's identity, why is an ACL on the broker side still needed?
- Which log line in your own system looks like success, but is actually printed before the work has actually happened?

## References

- [RFC 8446: The Transport Layer Security (TLS) Protocol Version 1.3](https://www.rfc-editor.org/rfc/rfc8446)
- [C4 — mTLS: the OPTIGA-backed TLS identity (SDK docs built from commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__c4__mtls__optiga.html)
- [SDK: tesaiot_mqtt/mqtt_mtls_setup.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/modules/tesaiot_mqtt/mqtt_mtls_setup.c) (linked, not copied)
- [SDK: proj_cm33_ns/configs/mbedtls_user_config.h](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/configs/mbedtls_user_config.h)
- [SDK: third_party_patches/README.md](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/third_party_patches/README.md)
- [SDK: CSR_SUBMISSION_CONTRACT.md, section 5.2 (CertificateVerify with a key inside OPTIGA)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/modules/tesaiot/docs/CSR_SUBMISSION_CONTRACT.md)
- Examples on the Developer Hub (Apache-2.0): [device-servertls](https://dev.tesaiot.dev/?example=developer-hub--device-servertls&q=device-servertls) · [device-mtls](https://dev.tesaiot.dev/?example=developer-hub--device-mtls&q=device-mtls)
