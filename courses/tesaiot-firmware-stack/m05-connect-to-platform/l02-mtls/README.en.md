---
id: fw-stack.m05.l02
lang: en
title:
  th: "ยืนยันตัวตนทั้งสองฝั่งด้วย mTLS"
  en: "Mutual authentication with mTLS"
summary:
  th: "ยืนยันตัวตนทั้งสองฝั่งด้วย mTLS"
  en: "Mutual authentication with mTLS"
level: L3
time_min: {concept: 15, lab: 45, check: 5}
hardware: {emulator: false, boards: [none]}
prerequisites: [fw-stack.m02.l07]
objectives:
  - th: "ส่ง telemetry ด้วย mTLS โดยใช้ client certificate และ private key ของอุปกรณ์"
    en: "Send telemetry with mTLS using the device client certificate and private key"
  - th: "เปรียบเทียบ Server-TLS กับ mTLS ในด้านความปลอดภัยและการดูแลกุญแจ"
    en: "Compare Server-TLS and mTLS for security and key handling"
develops:
  - {skill: sec.tls, to: 3}
  - {skill: sec.crypto, to: 2}
  - {skill: iot.cloud-platform, to: 2}
context: {platform: host-pc, lang: c}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "examples/embedded-devices/intermediate/device-mtls"
  ref: d2ed42c4a31232f553b6b8cef9ee7373db348c21
source_sha256: 7bacd8d7235d679063b13261538ad0e6689ef1866f92d2d5898c03b8d9b43ff6
---

# Mutual authentication with mTLS

## Objectives

1. Send telemetry with mTLS using the device client certificate and private key
2. Compare Server-TLS and mTLS for security and key handling

## Concepts

### What mTLS is: the device must prove it holds the private key that matches its own certificate

mTLS (mutual TLS, or two-way TLS) adds a step to the ordinary handshake: after the server presents its own certificate for the device to check (as with Server-TLS in the previous lesson), the server also asks for the device's certificate back, and the device must prove it holds the private key paired with that certificate (by signing part of the handshake with that key). The key point is that the private key is never sent over the network at all — only a "signature" proving the device holds the key ever travels. This is different from Server-TLS, where the device has to send a secret (an API key or a password) through the tunnel every time it connects.

### The files that must be present, and the code's check before connecting

This example (`device-mtls`) always needs `client_cert.pem` and `client_key.pem` in `certs_credentials/`. `main.c` checks with `file_exists(crt) && file_exists(key)` before it ever tries to send data. If either is missing, it prints an error and exits immediately — there is no attempt to connect without a certificate. Once both files are present, the code sets `tls.client_cert = crt; tls.client_key = key;` and still keeps `tls.verify_peer = 1U` on, as in the previous lesson — the device still checks the server exactly as before; it now also has to present its own certificate.

### CSR-based devices: the key never leaves the machine that created it

For devices that request a certificate through a CSR (Certificate Signing Request), the example's README states that the bundle downloaded from the Admin Portal does **not** include the private key, because the key is generated on the device's own side while creating the CSR (with `scripts/generate_csr.sh`, which calls `openssl` and then immediately `chmod 600`s the key file). The platform only ever receives the CSR, which carries the public key, to sign into a certificate — the private key itself never travels off the machine that created it. Even if the downloaded bundle leaks, the key does not leak with it. Users must copy this key into `certs_credentials/client_key.pem` themselves before use (a helper script, `sync_csr_key.sh <DEVICE_ID>`, is provided for this).

### The CA used to check the server is still the system trust store — not the bundle's ca-chain.pem

Unlike the previous lesson, where the MQTTS branch used the device's own `ca-chain.pem` to check the broker, this mTLS example sets `tls.ca_chain = NULL;` on both branches (HTTPS and MQTTS), with a source comment saying to use system trust and never force the device's own CA — because both endpoints still use certificates from a public CA, exactly as before. What mTLS adds is not a different way of checking the server (that stays identical); it is that the device must also present its own certificate back.

### mTLS uses different ports from Server-TLS

The platform clearly separates the mTLS listeners from the Server-TLS ones: mTLS uses HTTPS port 9444 and MQTTS port 8883 (per the defaults in `config.h`: `DEFAULT_API_BASE_URL` ending in `:9444`, `DEFAULT_MQTT_PORT = 8883U`), while Server-TLS uses 443 and 8884. The README warns that sending mTLS HTTPS to port 443 instead of 9444 lands on the wrong endpoint for mTLS, and runs into the SAN/domain mismatch it warns about.

### Comparing Server-TLS and mTLS: the trade-off between security and key-management burden

Both encrypt the channel equally, and the device checks the server the same way in both (`verify_peer = 1` always). The difference is in how the device proves itself. Server-TLS is simpler to start with, because it only needs one secret — but that secret travels across the network every time the device connects (even though it is inside an encrypted tunnel), and if it leaks, an attacker can impersonate the device immediately with nothing else needed. mTLS never sends a secret across the network during authentication at all, but in exchange it carries the burden of managing certificates and keys: there must be a system to issue certificates, renew them before they expire, and keep the private key safe. If one device's private key leaks, an attacker can impersonate that device until its certificate is revoked and a new keypair is issued — but the impact is limited to that one device, because each device has its own certificate and its own topic ACL (`device/<device_id>/…`). Never letting the key leave the device at all, the way OPTIGA Trust M's secure element does (lesson 5.3), is a further step down that same risk.

## Worked example

> **Before you run the example (checked 26 Sep 2026):** at this commit the example's `config.h` still defaults to the platform's former domain ending in .com, which has moved to tesaiot.dev.
> The former API domain no longer resolves; the former MQTT name still works for now. Set `DEFAULT_API_BASE_URL` to `https://tesaiot.dev:9444` and `DEFAULT_MQTT_HOST` to `mqtt.tesaiot.dev`
> (tracked in [developer-hub issue #3](https://github.com/tesaiot/developer-hub/issues/3)).

This example is written in C and runs on a computer first (GCC/Clang with OpenSSL, mbedTLS or wolfSSL, or libcurl) so the protocol is easy to see, before you carry the same ideas over to the board. The excerpts below are copied from the actual files (Apache-2.0, tesaiot/developer-hub, commit `d2ed42c`).

[`main.c`](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/intermediate/device-mtls/main.c#L336-L343) — both the device's certificate and its key must exist before anything starts:

```c
  char ca[512], crt[512], key[512];
  join_path(ca,  sizeof(ca),  certs_dir, FILE_CA_CHAIN);
  join_path(crt, sizeof(crt), certs_dir, FILE_CLIENT_CERT);
  join_path(key, sizeof(key), certs_dir, FILE_CLIENT_KEY);
  if (!(file_exists(crt) && file_exists(key))) {
    (void)fprintf(stderr, "mTLS requires client_cert.pem and client_key.pem in %s\n", certs_dir);
    return 1;
  }
```

[`main.c`](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/intermediate/device-mtls/main.c#L386-L388) — the TLS config binds the device's certificate/key, and still checks the server exactly as before:

```c
  iot_tls_conf_t tls; (void)memset(&tls, 0, sizeof(tls));
  tls.client_cert = crt; tls.client_key = key;
  tls.verify_peer = 1U; tls.connect_timeout_ms = (uint32_t)(HTTP_CONNECT_TIMEOUT_SEC * 1000L); tls.total_timeout_ms = (uint32_t)(HTTP_TOTAL_TIMEOUT_SEC * 1000L);
```

[`main.c`](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/intermediate/device-mtls/main.c#L412-L419) — the MQTTS branch: no username/password at all, because the certificate does that job instead:

```c
    if (is_mode_mqtts() != 0) {
      /* Send via MQTTS (mTLS) */
      /* ... */
      tls.ca_chain = NULL; tls.sni_name = mqtt_host;
      char topic[MAX_TOPIC_SIZE]; (void)snprintf(topic, sizeof(topic), "device/%s/telemetry", device_id);
      iot_mqtt_req_t mreq; (void)memset(&mreq, 0, sizeof(mreq));
      mreq.host = mqtt_host; mreq.port = (uint16_t)mqtt_port; mreq.client_id = device_id; mreq.username = NULL; mreq.password = NULL;
      mreq.topic = topic; mreq.payload = json_buf; mreq.payload_len = strlen(json_buf); mreq.qos = 1U; mreq.retain = 0U; mreq.keepalive_sec = 30U; mreq.timeout_ms = (uint32_t)(HTTP_TOTAL_TIMEOUT_SEC * 1000L);
```

- [Example README](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/intermediate/device-mtls/README.md) · [code folder](https://github.com/tesaiot/developer-hub/tree/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/intermediate/device-mtls) · commit `d2ed42c`
- You need device credentials from the TESAIoT Platform, following the steps in the README. Never commit real credentials to a public repository.

## Common mistakes

- **Forgetting that a CSR-based device's bundle has no private key in it** — if you see an error about a missing key, run `./scripts/sync_csr_key.sh <DEVICE_ID>` to copy the key from the machine that created the CSR. Do not ask the platform for a new key — it never had this key in the first place.
- **Using a Server-TLS port with mTLS credentials, or the reverse** — mTLS uses 9444 (HTTPS) and 8883 (MQTTS). Going to 443 or 8884 lands on an endpoint that is not mTLS, and runs into a SAN/domain mismatch.
- **Assuming mTLS means the server's certificate no longer needs to be checked** — `tls.verify_peer = 1U` is still on, exactly as with Server-TLS. mTLS only adds the device having to prove itself too; it does not reduce checking the server side at all.
- **Assuming Server-TLS and mTLS both use `X-API-KEY`** — mTLS uses no API key at all (`hreq.api_key = NULL`). If HTTPS returns an error in mTLS mode, check the device's certificate/key, not the API key.

## Try a change

1. **Guess** before you change anything: pick one value the example's README explains in the How section, and write down what you expect to change on the screen or in the log.
2. **Change and run**: build + flash, then compare against your guess. If it does not match, find which part you misunderstood.
3. **Extend**: add one thing the example does not yet have, and keep a photo or video in your portfolio.

## Check your understanding

- What does mTLS add on top of Server-TLS?
- If a device's private key leaks, what is the impact?

The answers are in the example's README and in the code. If you cannot answer one, go back and read the Why / What / How section again.

## References

- [Example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--device-mtls&q=device-mtls)
- The example lives in tesaiot/developer-hub (Apache-2.0) and is referenced by link
