---
id: aiot-mpy.m04.l01
lang: en
title: {th: 'WiFi และเครือข่าย: dBm DHCP IP และ DNS', en: 'WiFi and networking: dBm, DHCP, IP and DNS'}
summary: {th: เปิดดูสิ่งที่เกิดขึ้นระหว่างที่บอร์ด "กำลังต่อ" ตั้งแต่ความแรงสัญญาณเป็น dBm การเข้าร่วมวง DHCP และเลข IP จนถึงเหตุผลที่ต้อง ping สองปลายทาง เพื่อให้บอกได้ว่าเน็ตขาดตรงไหน ไม่ใช่แค่บอกว่าพัง, en: 'Open up what happens while the board is "connecting", from signal strength in dBm through joining the network, DHCP and the IP address, to why you ping two targets so you can say where the network breaks, not just that it broke.'}
level: L2
time_min: {concept: 30, lab: 15, check: 5}
hardware: {emulator: true, boards: [eva-kit, devkit]}
prerequisites: [aiot-mpy.m03.l09]
objectives:
  - {th: เทียบความแรงสัญญาณสองค่าที่เป็น dBm ได้ด้วยกฎ "ทุก 10 dB คือ 10 เท่า ทุก 3 dB ราว 2 เท่า" โดยไม่ใช้เครื่องคิดเลข เช่นบอกได้ว่า −50 dBm แรงกว่า −80 dBm อยู่ 1000 เท่า และจัดวงที่บอร์ดต่อเข้าเกณฑ์หน้างาน (ดีกว่า −60 · −67 · ต่ำกว่า −80), en: 'Compare two signal strengths in dBm with the rule "every 10 dB is 10×, every 3 dB is about 2×" without a calculator, e.g. state that −50 dBm is 1000× stronger than −80 dBm, and place the board''s network against the field thresholds (better than −60, −67, below −80).'}
  - {th: เรียงห้าขั้นตั้งแต่บอร์ดถามหา AP จนได้เลข IP พร้อมเกตเวย์และ DNS ได้ถูกลำดับ และบอกได้ว่าขั้น 1–3 เป็นเรื่องของ WiFi ส่วนขั้น 4–5 เป็นเรื่องของ IP ผ่าน DHCP แบบ DORA ซึ่งพังคนละแบบ, en: 'Put the five steps from the board asking for access points to receiving an IP address, gateway and DNS in the right order, and say that steps 1–3 are WiFi while steps 4–5 are IP via DHCP (DORA), which fail in different ways.'}
  - {th: แปลผล ping เกตเวย์คู่กับ ping 8.8.8.8 ได้ถูกครบสามกรณี (ผ่านทั้งคู่ · เกตเวย์ผ่านแต่เน็ตไม่ผ่าน · เกตเวย์ไม่ผ่าน) และบอกได้ว่าต้องไปแก้ที่ไหน, en: 'Interpret a gateway ping paired with an 8.8.8.8 ping correctly in all three cases (both pass, gateway passes but internet fails, gateway fails) and say where the fix belongs.'}
  - {th: 'อธิบายข้อจำกัดสองข้อของโมดูล wifi บนบอร์ดนี้ได้: wifi.ping() รับเฉพาะเลข IP เพราะยังไม่มีตัวแปลชื่อ (resolver) เปิดให้ Python เรียก และไม่มี netmask กับ gateway ให้อ่าน โค้ดจึงต้องเดาเกตเวย์เป็น .1 แล้วพิสูจน์ด้วย ping', en: 'Explain two limits of the board''s wifi module: wifi.ping() accepts IP numbers only because no resolver is exposed to Python, and netmask and gateway cannot be read, so code guesses the gateway as .1 and proves the guess with ping.'}
develops: [{skill: proto.wifi, to: 2}, {skill: proto.tcp-ip, to: 1}, {skill: hw.math, to: 1}, {skill: soft.problem-solving, to: 1}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {repo: 'https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer', path: session-09.html (slides 1–16), ref: a80bbe88a34bcb9bb8d991f42f9252b77cdab079}
source_sha256: 1320dd3303bc5f4632b7ad838813ac9db04dc80e442ee5950497d0f7ba23243a
---

# Lesson 4.1 — WiFi and networking: dBm, DHCP, IP and DNS

> Module 4 — IoT Platform Connectivity · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Open up what happens while the board is "connecting", from signal strength in dBm through joining the network, DHCP and the IP address, to why you ping two targets so you can say where the network breaks, not just that it broke.

## Objectives

By the end of this lesson you will be able to:

1. Compare two signal strengths in dBm with the rule "every 10 dB is 10×, every 3 dB is about 2×" without a calculator, e.g. state that −50 dBm is 1000× stronger than −80 dBm, and place the board's network against the field thresholds (better than −60, −67, below −80)
2. Put the five steps from the board asking for access points to receiving an IP address, gateway and DNS in the right order, and say that steps 1–3 are WiFi while steps 4–5 are IP via DHCP (DORA), which fail in different ways
3. Interpret a gateway ping paired with an 8.8.8.8 ping correctly in all three cases (both pass, gateway passes but internet fails, gateway fails) and say where the fix belongs
4. Explain two limits of the board's wifi module: wifi.ping() accepts IP numbers only because no resolver is exposed to Python, and netmask and gateway cannot be read, so code guesses the gateway as .1 and proves the guess with ping

## Before you start

Review lessons 1.4–1.6, where we called `wifi.connect()` and got online successfully, and picture lessons 3.7–3.9's dashboard,
because lessons 4.1–4.3 will attach a network status page to that same screen. This lesson has no code to write yet.
Have your learning log ready to record numbers read off the screen, and have ready the name and password of the home WiFi or phone hotspot you will connect the board to
(set up per the table in lesson 1.4: an English name with no spaces, a password of at least 8 characters, the 2.4 GHz band).

- **Equipment:** an Eva Kit or TESAIoT Dev Kit board with the BENTO MicroPython firmware installed, or the BENTO Emulator in [BENTO IDE](https://ide.tesaiot.dev/) (this lesson has no code yet; the dBm and IP numbers you record in the lab should be read from a real board connected to your home WiFi or hotspot)
- **Before this:** [Lesson 3.9 — Hands-on: the mini-HMI dashboard and the 10-minute soak test](../../m03-sensor-hmi/l09-dashboard-lab/README.md)

## See it work first

Open the **Wi-Fi Setting** menu that ships with the board (we first met it back in lessons 1.1–1.3), and watch three steps on screen.
First, scanning shows network names with strength in dBm. Second, choosing a network and entering the password makes the screen sit still for a while — that is waiting, not hanging.
Third, getting an IP address lights the icon in the top bar, meaning the board now has an address. These three steps are three lines in our own code:
`wifi.scan()` · `wifi.connect()` · `wifi.ip()`

## Concepts

**"Connected" and "usable" are not the same thing.** Lessons 1.4–1.6 were a tour of the whole path; this set of lessons opens that same box back up to see what a line that ran successfully
actually passed through, why it is sometimes alarmingly slow, and what the numbers it returns mean. The destination in lesson 4.3 is your team's network status page: a table of SSID · dBm ·
channel · security, sorted strongest to weakest, two link-status lamps, a ping to two targets, a dBm gauge ranging −90 to −40, and a rescan button.

**dBm is real power compared with 1 mW on a logarithmic scale.** $P_{\text{dBm}} = 10\log_{10}(P / 1\ \text{mW})$. At −67 dBm,
the antenna receives about 0.2 nanowatts, while 0 dBm is exactly 1 mW. Values on the board are therefore always negative. Remember just two rules: every 10 dB is 10×,
and every 3 dB is about 2×. The Wi-Fi Setting screen uses five bars at thresholds of −50 / −60 / −70 / −80 / −90, while network technicians use
better than −60 for comfortable everything, −67 as the limit for video or voice, and below −80 do not trust it. The 5 GHz band is not "better" than 2.4 GHz —
it trades range for speed. At 10 metres, the FSPL of channel 36 (5180 MHz) is 6.5 dB more than channel 6 (2437 MHz), leaving about a quarter of the power,
and a concrete wall costs another 10–15 dB. Scanning listens channel by channel one at a time, so `wifi.scan()` can block for up to 10 seconds —
show "scanning" text before calling it, never after.

**From radio wave to IP address takes five steps.** Steps 1–3 are WiFi: ask who is around here · the AP answers with its name, strength and channel · ask to join, proving the password.
Steps 4–5 are IP: ask for an address via DHCP (Discover · Offer · Request · Acknowledge), then receive an IP address with a gateway and DNS.
This number is a temporary loan (a lease); power-cycling the board may give a different one, so code must read `wifi.ip()` fresh every time after connecting.
`wifi.connect()` returns `True` only after all five steps succeed; failing at any of them gives the same `False`. If the network's DHCP is full or broken,
we join the WiFi but get no IP address at all, which looks exactly like a failed connection even though it is not.

**Ping two targets, and read the results as a pair.** `wifi.ping(ip, timeout_ms)` returns the round-trip time in milliseconds, or −1 when there is no answer.
Gateway passing and internet passing is normal · gateway passing but 8.8.8.8 silent means the problem is upstream of our router, not on our side ·
gateway failing points to the WiFi link or a wrongly guessed gateway number. MicroPython on this board only gives `wifi.ip()` — there is no netmask
or gateway to read. So code guesses the gateway from the IP's first three octets followed by `.1`, which is correct on most home networks but not all,
and `wifi.ping()` only accepts an IP number — passing `"google.com"` raises `ValueError`, because no name resolver is exposed to Python yet.
This is a gap in the module, not the hardware. We choose 8.8.8.8 because it is easy to remember and almost never goes down.

Our data is wrapped layer by layer before it goes on air, and each layer adds size and can fail on its own — good radio signal but no IP really can happen.
`wifi.connect()` handles the lower layers for us; `wifi.ping()` measures the middle layer; and in lessons 4.4–4.6 we will write the top layer ourselves, with MQTT.

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automatic marking.

1. Network A measures −50 dBm, network B measures −80 dBm. About how many times more power does the antenna receive from A than from B? *(choose one · objective 1)*
   - A) 30 times, because the numbers differ by 30
   - B) 1000 times
   - C) About 1.6 times
   - D) 3 times

   <details><summary>Solution</summary>

   **B** — The difference is 30 dB, and every 10 dB is 10×, so 10 × 10 × 10 = 1000 times. dBm is a logarithmic scale, so a small difference in the number can mean a huge difference in real power.

   </details>

2. Put what happens while wifi.connect() runs in order, from first to last. *(order · objective 2)*
   - A) The board asks to join the network, proving the password
   - B) The router gives an IP address, with a gateway and DNS
   - C) The board asks which access points are around here
   - D) The board asks for an address via DHCP (DISCOVER / REQUEST)
   - E) The AP answers with its name, strength and channel

   <details><summary>Solution</summary>

   **C → E → A → D → B** — The first three steps are WiFi, and by the end of step 3 the board still has no IP address. The last two steps are IP via DHCP. Whichever step fails, connect() returns the same False, which is why ping is needed to tell apart where it actually failed.

   </details>

3. The status page shows the gateway ping at 3 ms, but the 8.8.8.8 ping times out. Which conclusion is correct? *(choose one · objective 3)*
   - A) The board's WiFi link dropped; reconnect
   - B) The problem is upstream of the router, not on our board
   - C) The guessed gateway of .1 is wrong
   - D) You should ping "google.com" instead of 8.8.8.8

   <details><summary>Solution</summary>

   **B** — The gateway answering means the WiFi link and the guessed gateway number both work. Silence from a destination outside the home means the break is beyond the router. A silent gateway, on the other hand, points to the WiFi link or a wrongly guessed gateway.

   </details>

4. Which statements about the wifi module on this board are correct? Choose every correct one. *(choose all that apply · objective 4)*
   - A) wifi.ping("google.com") raises ValueError, because no name resolver is exposed to Python yet
   - B) Code can read the real netmask and gateway from the firmware
   - C) The gateway in the code is a guess from the IP address (the first three octets followed by .1), so it must be proven with ping
   - D) The domain-name limitation exists because the radio chip cannot speak DNS

   <details><summary>Solution</summary>

   **A, C** — The board only gives wifi.ip(); there is no netmask or gateway to read, so the code guesses the gateway and fires a ping to prove it. The DNS matter is a gap in the module — the chip itself can speak DNS; nobody has opened that door on the Python side yet.

   </details>

5. The board has joined the WiFi network successfully, but the network's DHCP is full. What symptom would you see? *(choose one · objective 2)*
   - A) WiFi connects, but there is no IP address, which looks like a failed connection
   - B) wifi.scan() finds no networks at all
   - C) It gets a normal IP address, but the 8.8.8.8 ping fails
   - D) The RSSI value becomes positive

   <details><summary>Solution</summary>

   **A** — DHCP belongs to steps 4–5, which are about IP, not WiFi. The radio signal is good and joining succeeds, but nobody hands out an address, so it cannot talk to anyone outside the room, even though it looks like the connection failed.

   </details>

## Lab

**Read the network around you as numbers** (about 15 minutes). Do this on a real board, and record in your learning log.

- [ ] Open Wi-Fi Setting and record the name and dBm value of the three strongest networks, and the weakest one you can see
- [ ] Compute how many dB apart the strongest and weakest networks are, and how many times the power differs, using the rule 10 dB = 10×, 3 dB ≈ 2×
- [ ] Place the network the board connects to against the field thresholds: better than −60 · around −67 · below −80
- [ ] Connect to your home WiFi or hotspot and record the IP address you get, then write down the gateway you "guess" (the first three octets followed by `.1`), to prove it with ping in lesson 4.3
- [ ] Build a three-row table in your learning log: gateway ping result · 8.8.8.8 ping result · where the problem lies, covering all three cases

## Going further

Lesson 4.2 reads through the network status page's code move by move, along with the `wifi` module's eight names, and the values on the Wi-Fi Setting page that are not from a real measurement.

Next lesson: [Lesson 4.2 — The network status screen: reading the wifi code](../l02-network-status-code/README.md)

## Reflect

- When a teammate says "the signal is just a little weak", what number would you ask back for, and what does a 20 dB difference mean in multiples?
- A shed 300 metres from the house — should it use 2.4 or 5 GHz, and which formula helps decide before buying anything?
- How is a system that can say "where it broke" worth more than one that only says "it's broken", in the work you want to do?
