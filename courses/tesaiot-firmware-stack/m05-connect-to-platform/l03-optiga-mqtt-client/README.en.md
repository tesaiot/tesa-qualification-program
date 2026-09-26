---
id: fw-stack.m05.l03
lang: en
title:
  th: "PSoC Edge E84 กับ OPTIGA™ Trust M: กุญแจที่ไม่ออกจากชิป"
  en: "PSoC Edge E84 with OPTIGA™ Trust M: keys that never leave the chip"
summary:
  th: "PSoC Edge E84 กับ OPTIGA™ Trust M: กุญแจที่ไม่ออกจากชิป"
  en: "PSoC Edge E84 with OPTIGA™ Trust M: keys that never leave the chip"
level: L3
time_min: {concept: 15, lab: 45, check: 5}
hardware: {emulator: false, boards: [eva-kit]}
prerequisites: [fw-stack.m02.l07]
objectives:
  - th: "อธิบาย workflow การ provision อุปกรณ์ที่สร้างและเก็บ private key ใน OPTIGA Trust M"
    en: "Explain the provisioning workflow that creates and keeps the private key inside OPTIGA Trust M"
  - th: "เชื่อมต่อ MQTT over TLS ด้วย certificate ที่เก็บใน OPTIGA ตามตัวอย่าง"
    en: "Connect MQTT over TLS with the certificate stored in OPTIGA, following the example"
develops:
  - {skill: sec.secure-element, to: 2}
  - {skill: sec.tls, to: 3}
  - {skill: sec.fundamentals, to: 2}
context: {platform: psoc-edge-e84, lang: c}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "examples/security/pse84_tesaiot_client"
  ref: d2ed42c4a31232f553b6b8cef9ee7373db348c21
source_sha256: 89e74265a24496cddf54bd8464f01cfda383fff371a706ddbfe6b265694cd653
---

# PSoC Edge E84 with OPTIGA™ Trust M: keys that never leave the chip

## Objectives

1. Explain the provisioning workflow that creates and keeps the private key inside OPTIGA Trust M
2. Connect MQTT over TLS with the certificate stored in OPTIGA, following the example

## Concepts

### What OPTIGA Trust M is, and why the key never leaves the chip

OPTIGA™ Trust M is a secure element (a separate security chip, CC EAL6+ certified) connected to the PSoC Edge E84 over I2C. This chip generates and keeps ECC P-256 keypairs entirely inside itself: the firmware can ask the chip to "sign data", but there is no way to ever read the private key back out — not even by dumping the MCU's memory — because the key never enters the MCU's RAM in the first place. The rest of TLS, such as encrypting data in transit, is still done by mbedTLS on the MCU as usual; only the step that needs the private key (signing during the TLS handshake) is handed off to the chip.

### OIDs: the map of keys and certificates inside the chip

OPTIGA stores data in numbered slots called OIDs. This example uses these main ones: `0xE0C2` holds the Factory UID (the hardware's identity number, read-only, 27 bytes); `0xE0E0` holds the Factory Certificate (provisioned at the factory), paired with the key at `0xE0F0`; `0xE0E1` holds the Device Certificate (issued by the TESAIoT Platform through Protected Update), paired with the key at `0xE0F1`; and `0xE0E3` holds the trust anchor (ROOT_CA) used to verify Protected Update signatures. Each certificate must always be used with the key at its matching OID (`0xE0E0`↔`0xE0F0`, `0xE0E1`↔`0xE0F1`) — pairing them wrongly signs the TLS handshake with a key that does not match the certificate being presented.

### Access conditions: the key cannot be read, but it can be told to sign

The OID Access Conditions table in the upstream documentation states clearly that the key slots `0xE0F0` and `0xE0F1` have Read = Never (never readable, under any circumstance) but Execute = Always (always usable to sign, for example during a TLS handshake). The certificate slot `0xE0E0` is Change = Never (unwritable again after provisioning), while `0xE0E1` can be rewritten (`Change = Always*`), though changing the metadata's own access rules is locked once the lifecycle state (`LcsO`) reaches Operational (`0x07`). This "usable but unreadable" property is the heart of the "hardware root of trust": even if the firmware has a vulnerability or is reached through a debugger, the key still cannot be copied out — unlike a key stored in the MCU's flash, which a debugger or a firmware bug can read out.

### Two-Certificate PKI and SAFE MODE: why there are two certificates

This example uses two paired certificates: the Factory Certificate (`0xE0E0`+`0xE0F0`, provisioned at the factory, used to bootstrap or recover) and the Device Certificate (`0xE0E1`+`0xE0F1`, issued by the TESAIoT Platform through Protected Update, used in normal operation). Every time the device powers on or resets, the firmware enters "SAFE MODE" by defaulting `g_force_factory_cert = true`, forcing it to use the Factory Certificate first. The upstream README gives the reason: the Device Certificate (`0xE0E1`) may not match the Device Key (`0xE0F1`) after a reset, because the pairing of a freshly provisioned key stays in temporary memory until its certificate has been successfully written, while the Factory Certificate and Factory Key are always correctly paired. Starting with the Factory Certificate therefore guarantees the MQTT connection works for recovery. The user then chooses to run Protected Update to switch over to the Device Certificate.

### The order of steps for obtaining a usable certificate (the Protected Update workflow)

The order for obtaining the Device Certificate is: (1) OPTIGA generates an ECC P-256 keypair inside the chip itself (at OID `0xE0F1`); (2) it creates a CSR (Certificate Signing Request) signed with that in-chip key; (3) it connects to MQTT with the Factory Certificate first (per SAFE MODE), then sends the CSR to the platform; (4) the platform issues a certificate and sends back a signed Protected Update manifest; (5) OPTIGA checks the manifest's signature against the trust anchor at `0xE0E3` first — if the signature does not match, it refuses to write it; if it matches, it writes the new certificate to OID `0xE0E1`. Throughout this process, the private key at `0xE0F1` never leaves the chip — only the CSR (which carries the public key) and the certificate ever travel over the network. Checking the manifest's signature before every write is what causes a forged update to be rejected.

### Connecting MQTT over TLS with a key inside OPTIGA: binding TLS to the secure element at boot

At startup, the firmware reads the current certificate from OPTIGA (`read_certificate_from_optiga()`), then registers OPTIGA's secure-element driver with PSA Crypto (`optiga_psa_register()`, followed by `psa_crypto_init()`). It then creates a PSA key handle located at `PSA_KEY_LOCATION_OPTIGA` through `psa_generate_key()` — "generate" here means attaching a PSA handle to an OID that already holds a key from the factory; it does not create a new key at this step. It then binds the TLS layer to that key with `cy_tls_set_optiga_key_id()`, and sets the TLS client certificate with `cy_tls_set_client_cert()`. When connecting to the platform's MQTT broker (port `8883` when mutual-auth is on), during the CertificateVerify step of the TLS handshake, mbedTLS calls back into this driver to sign a hash with the key at whichever OID is selected (`0xE0F0` or `0xE0F1`, depending on which certificate is in use). The result is an ECDSA signature handed back to mbedTLS for the next handshake packet — with no byte of the key itself ever flowing through the MCU's RAM.

## Worked example

> **Before you run the example (checked 26 Sep 2026):** at this commit the example's `mqtt_client_config.h` still sets `MQTT_BROKER_ADDRESS` and `MQTT_SNI_HOSTNAME` to the platform's former MQTT name ending in .com.
> That name still works for now, but the platform has moved to tesaiot.dev: set both to `mqtt.tesaiot.dev` (tracked in [developer-hub issue #3](https://github.com/tesaiot/developer-hub/issues/3)).

This example's code lives on the Developer Hub (pinned to commit `d2ed42c`) — read the [example README](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/security/pse84_tesaiot_client/README.md) for the full OID table, the two-certificate PKI, and SAFE MODE, then follow the code in this order (runs on the PSoC Edge E84 board with the OPTIGA™ Trust M; this project has the Eva Kit BSP: APP_KIT_PSE84_EVAL_EPC2).

- [`main.c`](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/security/pse84_tesaiot_client/main.c#L491-L536) — the boot-time sequence: read the certificate from OPTIGA, register the PSA secure-element driver, bind TLS to the key inside OPTIGA
- [`optiga_psa_se.c`](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/security/pse84_tesaiot_client/optiga_psa_se.c#L285-L323) — the sign function (`optiga_psa_sign`) that mbedTLS calls during the TLS handshake, asking OPTIGA to sign a hash with the key at the selected OID
- [`optiga_trust_helpers.c`](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/security/pse84_tesaiot_client/optiga_trust_helpers.c#L768-L824) — `trustm_gen_ecc_keypair()`, which calls `optiga_crypt_ecc_generate_keypair()` with `export_private=false`, the part that keeps a key generated in the chip from ever being exported
- [`mqtt_task.c`](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/security/pse84_tesaiot_client/mqtt_task.c#L824-L834) — selecting the certificate (`tesaiot_select_mqtt_certificate()`) and then switching the signing key's OID to match the selected certificate before every connection
- See the full folder at [`examples/security/pse84_tesaiot_client/`](https://github.com/tesaiot/developer-hub/tree/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/security/pse84_tesaiot_client)
- You need device credentials from the TESAIoT Platform, following the steps in the README. Never commit real credentials to a public repository.

This code is under the Cypress (Infineon) EULA, so it is referenced by link only — no code is copied into this lesson.

## Common mistakes

- **Assuming this example's code generates a new key every time the board boots** — `psa_generate_key()` here only attaches a PSA key handle to an OID that already holds a key from the factory (`OPTIGA_TLS_ATTACH_ONLY`); it does not create a new key each time. The actual key is created only once, either during provisioning (for the Factory Key) or during the Protected Update workflow (for the Device Key).
- **Pairing a certificate with a key at the wrong OID** — certificate `0xE0E0` must only be paired with key `0xE0F0`, and `0xE0E1` only with `0xE0F1`. The code in `mqtt_task.c` therefore switches `optiga_psa_set_signing_key_oid()` to match whichever certificate is selected, every time, before connecting. Forgetting to switch it means the TLS handshake is signed with a key that does not match the certificate.
- **Assuming a board reset gets you the Device Certificate right away** — every reset returns the firmware to SAFE MODE (using the Factory Certificate) first. Protected Update has to be run again each time you want to switch to the Device Certificate.
- **Rerunning `make getlibs` and forgetting `./apply_patches.sh`** — the upstream README warns that the patches get wiped along with the library; `secure-sockets` can no longer use the key inside OPTIGA during the TLS handshake. `./apply_patches.sh` must be rerun every time after `make getlibs`.

## Try a change

1. **Guess** before you change anything: pick one value the example's README explains in the How section, and write down what you expect to change on the screen or in the log.
2. **Change and run**: build + flash, then compare against your guess. If it does not match, find which part you misunderstood.
3. **Extend**: add one thing the example does not yet have, and keep a photo or video in your portfolio.

## Check your understanding

- Why is a private key inside a secure element safer than one in flash?
- What does Protected Update do with the certificate?

The answers are in the example's README and in the code. If you cannot answer one, go back and read the Why / What / How section again.

## References

- [Example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--pse84_tesaiot_client&q=pse84_tesaiot_client)
- This code is under the Cypress (Infineon) EULA, so it is referenced by link only
