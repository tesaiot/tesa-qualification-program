---
id: fw-stack.m05.l01
lang: en
title:
  th: "ส่งข้อมูลขึ้น TESAIoT Platform ด้วย Server-TLS"
  en: "Telemetry to the TESAIoT Platform with Server-TLS"
summary:
  th: "ส่งข้อมูลขึ้น TESAIoT Platform ด้วย Server-TLS"
  en: "Telemetry to the TESAIoT Platform with Server-TLS"
level: L3
time_min: {concept: 15, lab: 45, check: 5}
hardware: {emulator: false, boards: [none]}
prerequisites: [fw-stack.m02.l07]
objectives:
  - th: "ส่ง telemetry ขึ้นแพลตฟอร์มผ่าน HTTPS หรือ MQTTS แบบ Server-TLS ด้วยตัวอย่างภาษา C"
    en: "Send telemetry to the platform over HTTPS or MQTTS with Server-TLS using the C example"
  - th: "อธิบายว่า CA certificate ทำหน้าที่อะไรในการยืนยันตัวตนของเซิร์ฟเวอร์"
    en: "Explain what the CA certificate does when verifying the server"
develops:
  - {skill: sec.tls, to: 2}
  - {skill: proto.mqtt, to: 2}
  - {skill: iot.cloud-platform, to: 2}
context: {platform: host-pc, lang: c}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "examples/embedded-devices/entry/device-servertls"
  ref: d2ed42c4a31232f553b6b8cef9ee7373db348c21
source_sha256: 5c92d7e997b190c09690e4c2997cfb568c378be73ec1a78b590d920e8f68c4cc
---

# Telemetry to the TESAIoT Platform with Server-TLS

## Objectives

1. Send telemetry to the platform over HTTPS or MQTTS with Server-TLS using the C example
2. Explain what the CA certificate does when verifying the server

## Concepts

### Who Server-TLS verifies, and what the device proves itself with

Server-TLS (one-way TLS) is a TLS handshake in which the server side always presents its own certificate for the device to check first. The device checks that the certificate is signed by a trusted CA and matches the hostname it intended to connect to — that is the only thing Server-TLS verifies: the server's identity. The handshake itself does not verify the device's identity. The device has to prove itself with a separate "secret" it holds, sent inside the tunnel once it is encrypted. In this example's code (`main.c`), this shows up as `tls.client_cert` and `tls.client_key` always being set to `NULL` (no device-side certificate), while `tls.verify_peer = 1U` stays on the whole time — the device still checks the server, it just never presents a certificate of its own.

### The two ways this example proves the device's identity: an API key vs. username/password

This example (`device-servertls`) can send data two ways, chosen through the `COMM_MODE` environment variable: HTTPS and MQTTS. Both are still Server-TLS (the server proves itself with a certificate either way), but the device proves itself differently on each path — HTTPS sends only the `X-API-KEY` header, read from `api_key.txt` (the code has a comment "omit Bearer", meaning no Bearer token is sent as well), while MQTTS uses `username = device_id` with a `password` from `mqtt_password.txt`, whose hash the backend checks against its database. Either way, the secret (the API key or the password) always travels inside the already-encrypted TLS tunnel, never in the clear.

### ca-chain.pem is the broker's trust anchor, but this example's HTTPS path uses the system trust store instead

`main.c` sets up the initial TLS config with `tls.ca_chain = file_exists(PATH_CA_CHAIN) ? PATH_CA_CHAIN : NULL;` — if a `ca-chain.pem` file (from the bundle downloaded from the Admin Portal) exists in the `certs_credentials/` folder, the code uses it as the trust anchor when connecting over MQTTS (also setting `tls.sni_name = mqtt_host`), to check that the broker's certificate was issued by the platform's own internal CA. But on entering the HTTPS branch, the code immediately overwrites this with `tls.ca_chain = NULL;`, with a source comment saying to use system trust — because the platform's public HTTPS endpoint uses a certificate from a public CA the OS already trusts, so it does not need to carry its own `ca-chain.pem` to check again. This is a detail that differs by connection path within the same example, not a fixed rule that Server-TLS must always use `ca-chain.pem`.

### Ports are split by authentication method, not by protocol

The platform separates listeners by how the device proves itself. Server-TLS uses MQTT port 8884 and HTTPS port 443 (per the defaults in `config.h`: `DEFAULT_MQTT_PORT = 8884U`, `DEFAULT_API_BASE_URL`), while mTLS (the next lesson) uses different ports. If Server-TLS username/password credentials are used to connect to port 8883 (the mTLS port), TLS is closed right after CONNECT, because that listener expects the device's certificate, not a username/password.

### The order of steps, and what fails when one is missing

This example's order is: (1) read credentials from files in `certs_credentials/` — device_id, api_key or the MQTT username/password, and `endpoints.json` if present; (2) open the TLS handshake to the configured endpoint, always checking the server's certificate (`verify_peer = 1U` is never turned off); (3) once the handshake succeeds, send the device's credential inside the tunnel (a header, or the MQTT CONNECT packet); (4) send the JSON payload `{device_id, timestamp, data}` to the topic `device/<device_id>/telemetry` (MQTTS) or the `/api/v1/telemetry` endpoint (HTTPS). If step 1 is missing (no credential file), the program stops immediately with an error. If step 2 fails (for example the server's certificate has expired, or the device's clock is wrong enough that the certificate looks like it is not valid yet), the handshake always fails before step 3 is reached. If step 2 succeeds but step 3 is wrong (for example the password has expired), the broker answers with a rejection code (MQTT CONNACK code 5, "Not authorized") — a different cause than a TLS problem. The example's README clearly separates these two cases under Troubleshooting.

## Worked example

> **Before you run the example (checked 26 Sep 2026):** at this commit the example's `config.h` still defaults to the platform's former domain ending in .com, which has moved to tesaiot.dev.
> The former API domain no longer resolves; the former MQTT name still works for now. Set `DEFAULT_API_BASE_URL` to `https://tesaiot.dev` and `DEFAULT_MQTT_HOST` to `mqtt.tesaiot.dev`
> (tracked in [developer-hub issue #3](https://github.com/tesaiot/developer-hub/issues/3)).

This example is written in C and runs on a computer first (GCC/Clang with OpenSSL, mbedTLS or wolfSSL, or libcurl) so the protocol is easy to see, before you carry the same ideas over to the board. The excerpts below are copied from the actual files (Apache-2.0, tesaiot/developer-hub, commit `d2ed42c`).

[`main.c`](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/entry/device-servertls/main.c#L297-L301) — the initial TLS config: no device-side certificate, but the server is still always checked:

```c
  /* Mongoose TLS conf */
  iot_tls_conf_t tls; (void)memset(&tls, 0, sizeof(tls));
  tls.ca_chain = file_exists(PATH_CA_CHAIN) ? PATH_CA_CHAIN : NULL;
  tls.client_cert = NULL; tls.client_key = NULL; /* serverTLS */
  tls.verify_peer = 1U; tls.connect_timeout_ms = (uint32_t)(HTTP_CONNECT_TIMEOUT_SEC * 1000L); tls.total_timeout_ms = (uint32_t)(HTTP_TOTAL_TIMEOUT_SEC * 1000L);
```

[`main.c`](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/entry/device-servertls/main.c#L331-L341) — the MQTTS branch: uses the device's own `ca-chain.pem` to check the broker, and proves itself with username/password:

```c
    if (is_mode_mqtts() != 0) {
      /* MQTTS (Server‑TLS): username/password + CA verify */
      char topic[MAX_TOPIC_SIZE]; (void)snprintf(topic, sizeof(topic), "device/%s/telemetry", dev_id);
      iot_mqtt_req_t mreq; (void)memset(&mreq, 0, sizeof(mreq));
      mreq.host = mqtt_host; mreq.port = (uint16_t)mqtt_port; mreq.client_id = dev_id;
      mreq.username = (mqtt_user[0] != '\0') ? mqtt_user : dev_id; /* fallback to device_id */
      mreq.password = (mqtt_pass[0] != '\0') ? mqtt_pass : NULL;
      mreq.topic = topic; mreq.payload = json; mreq.payload_len = strlen(json);
      mreq.qos = 1U; mreq.retain = 0U; mreq.keepalive_sec = 30U; mreq.timeout_ms = (uint32_t)(HTTP_TOTAL_TIMEOUT_SEC * 1000L);
      tls.sni_name = mqtt_host;
      const int rc = iot_mqtts_publish(&mreq, &tls);
```

[`main.c`](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/entry/device-servertls/main.c#L344-L354) — the HTTPS branch: uses the system trust store instead of `ca-chain.pem`, and proves itself with `X-API-KEY`:

```c
    } else {
      /* HTTPS (Server‑TLS): Bearer/X-API-KEY */
      /* ... */
      tls.ca_chain = NULL;
      tls.sni_name = NULL;
      iot_http_req_t hreq; (void)memset(&hreq, 0, sizeof(hreq));
      hreq.url = url; hreq.body = json; hreq.body_len = strlen(json);
      /* For Server‑TLS HTTPS, send only X-API-KEY (omit Bearer) */
      hreq.api_key = api_key; /* include device API key header */
      hreq.timeout_ms = (uint32_t)(HTTP_TOTAL_TIMEOUT_SEC * 1000L);
      const int rc = iot_https_post(&hreq, &tls);
```

- [Example README](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/entry/device-servertls/README.md) · [code folder](https://github.com/tesaiot/developer-hub/tree/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/entry/device-servertls) · commit `d2ed42c`
- You need device credentials from the TESAIoT Platform, following the steps in the README. Never commit real credentials to a public repository.

## Common mistakes

- **Assuming Server-TLS also verifies the device's identity** — Server-TLS only verifies the server side. The device must prove itself separately with an API key or username/password. Missing this can lead to under-protecting the API key/password, from the mistaken belief that the certificate already does that job.
- **Using the wrong port for the mode (8883 instead of 8884, or the reverse)** — ports are split by how the device authenticates, not by whether TLS is used. Using the mTLS port with Server-TLS credentials closes the TLS connection right after CONNECT.
- **Seeing MQTT CONNACK Code 5 (Not authorized) and assuming it is a TLS/certificate problem** — Code 5 only happens **after** the TLS handshake has already succeeded, so it is a problem at the device-authentication step (a wrong or not-yet-synced username/password), not a certificate problem.
- **Assuming `ca-chain.pem` must be used to verify every connection path** — in this example, only MQTTS uses the device's own `ca-chain.pem`; HTTPS uses the operating system's trust store instead. That is a choice specific to this example, not a general rule for Server-TLS.

## Try a change

1. **Guess** before you change anything: pick one value the example's README explains in the How section, and write down what you expect to change on the screen or in the log.
2. **Change and run**: build + flash, then compare against your guess. If it does not match, find which part you misunderstood.
3. **Extend**: add one thing the example does not yet have, and keep a photo or video in your portfolio.

## Check your understanding

- Whose identity does Server-TLS verify, and whose does it not verify?
- If the device's clock is wrong, why might TLS fail?

The answers are in the example's README and in the code. If you cannot answer one, go back and read the Why / What / How section again.

## References

- [Example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--device-servertls&q=device-servertls)
- The example lives in tesaiot/developer-hub (Apache-2.0) and is referenced by link
