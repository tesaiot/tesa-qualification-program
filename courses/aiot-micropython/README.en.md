# AIoT in Action: From Touch Screen to IoT Platform (MicroPython)

> Adapted from AIoT in Action — Embedded Systems for AIoT Developer, © 2026 Assoc. Prof. Wiroon Sriborrirux, Embedded Systems Engineering, Department of Electrical Engineering, Faculty of Engineering, Burapha University (BUU), Advance Innovation Centre (AIC) · BENTO & TESAIoT (CC BY 4.0 / MIT)

Thai version: [README.md](README.md). The lessons, slides and code comments are in Thai (technical terms and code in English).

Learn **AIoT** hands-on on the PSoC Edge boards — the **Eva Kit** or the **TESAIoT Dev Kit** — in **MicroPython**. You start by playing the apps that ship on the board, so you see where the course ends, then peel it open layer by layer until you can build the whole chain yourself:

**touch screen → hardware → sensors → network → MQTT → IoT platform → your own product**

The same example files run on both boards: the code asks the board how many LEDs it has, what its button is called and which sensors are present. No compiler, no C toolchain.

## Who it is for

- Anyone, including entrepreneurs, who wants to understand how an AIoT system works from the real thing
- Software developers who know some Python and want to work with hardware, sensors and IoT
- Engineering and science learners who want a hands-on start in embedded systems
- Educators who want ready lessons with slides, code, practice files and solutions

You need basic Python (variables, if, loops, functions). No electronics background is required. You can learn alone or in a team of two to four per board.

## Outcomes

1. Explain how sensing, on-device decisions, the display and the destination platform share the work in an AIoT system, decide which work should stay on the board and which should leave it, and give at least one industrial example.
2. Write MicroPython programs that drive the board's hardware (LEDs, button, touch pads, analog input) and build a touch-screen UI whose on-screen state matches the real hardware in every test.
3. Read sensor data (IMU, compass, CapSense, potentiometer), choose and apply a suitable filter, and design a real-time HMI dashboard that stays within its widget budget and update rate and runs for 10 minutes.
4. Connect the board to WiFi, send and receive data over MQTT in both directions, and compare the port 1883 channel with TLS-encrypted MQTTs (serverTLS): what it protects and what it still does not.
5. Assemble everything into an AIoT mini-product that solves one real problem, keeps working when the network drops, sends data in a schema you designed, and present it in 10 minutes.

## What you need

- **A board**: BENTO PSoC Edge **Eva Kit** (KIT_PSE84_EVAL_EPC2) or **TESAIoT Dev Kit** (KIT_PSE84_AI SoM on the QWA309 base) with the BENTO MicroPython firmware — **or start without a board** in the BENTO Emulator inside BENTO IDE (some lessons need the real board; see each lesson's hardware line)
- **BENTO IDE** — <https://ide.tesaiot.dev/> write code and press **Program to Device** from the browser; the BENTO Emulator is built in
- **WiFi** from lesson 1.4 (first connection) and throughout module 4 · networks that need a web login do not work for the board; use a phone hotspot
- **TESAIoT Community Edition** for lessons 4.5–4.6 — a self-hosted IoT platform (<https://github.com/tesaiot/tesaiot-community-edition>) · **a TESAIoT Platform account** for MQTTs in lessons 4.7–4.9 (a self-installed CE cannot take MQTTs from the board; see lesson 4.7) · the other plain-MQTT lessons and the capstone use a public practice broker. When learning in a group, the organiser may prepare a broker and device identities for you
- A notebook or file for your own **learning log**; the slides say what to record

## Course map

Five modules, 36 lessons: about 36 hours as in the source course (twelve 3-hour sets); the lesson estimates add up to about 38 hours, 45–75 minutes per lesson. Lessons come in sets of three: **concept → code walk-through → hands-on**.

| Module | Lessons | Hours (approx.) | Topic |
|---|---|---|---|
| [Module 1 — Existing UI-based Application](m01-ui-application/README.md) | 6 | 6.8 | Meet the board through the apps it ships with, put your first lines on screen with lcd and ui, then send a value out over the network and take a command back. |
| [Module 2 — UI-to-Hardware Interfacing](m02-ui-to-hardware/README.md) | 9 | 9.4 | Drive LEDs and read the button with gpio, build a touch control panel that controls the real LEDs, then read the knob and CapSense and filter the signal. |
| [Module 3 — Sensor Visualization on HMI](m03-sensor-hmi/README.md) | 9 | 8.9 | Turn acceleration into tilt, sample correctly and draw real-time charts, and assemble a four-card mini-HMI dashboard that keeps running. |
| [Module 4 — IoT Platform Connectivity](m04-iot-connectivity/README.md) | 9 | 9.4 | Join WiFi and read the network, send telemetry and take commands over MQTT with a self-hosted platform, then move to MQTTs over TLS. |
| [Module 5 — Capstone: AIoT Mini-Product](m05-capstone/README.md) | 3 | 3.3 | Start from a real problem, design with a canvas and a schema, assemble Sense → Decide → Show → Send into a mini-product that survives a network drop, and present it in 10 minutes. |

<details><summary>All lessons</summary>

**Module 1 — Existing UI-based Application**

- [Lesson 1.1 — Board tour: play with the real thing first](m01-ui-application/l01-board-tour/README.md)
- [Lesson 1.2 — First lines on screen: the lcd and ui modules](m01-ui-application/l02-first-lines-on-screen/README.md)
- [Lesson 1.3 — Inside the box: two cores, AIoT and your team's screen](m01-ui-application/l03-inside-the-box/README.md)
- [Lesson 1.4 — Leaving the desk: the first WiFi connection](m01-ui-application/l04-wifi-first-connect/README.md)
- [Lesson 1.5 — Values out, commands back: MQTT on a public broker](m01-ui-application/l05-values-out-commands-back/README.md)
- [Lesson 1.6 — Hands-on: a real value leaves the board, module 1 wrap-up](m01-ui-application/l06-link-lab/README.md)

**Module 2 — UI-to-Hardware Interfacing**

- [Lesson 2.1 — The gpio module: LEDs, a button and a board that describes itself](m02-ui-to-hardware/l01-gpio-leds-buttons/README.md)
- [Lesson 2.2 — Behind LEDs and buttons: active-low, debouncing and the endless loop](m02-ui-to-hardware/l02-active-low-debounce/README.md)
- [Lesson 2.3 — Hands-on: running lights, a button, and the broker](m02-ui-to-hardware/l03-led-button-lab/README.md)
- [Lesson 2.4 — The touch screen and your first widgets](m02-ui-to-hardware/l04-touch-widgets/README.md)
- [Lesson 2.5 — The event loop: touch the screen, light the real LED](m02-ui-to-hardware/l05-event-loop/README.md)
- [Lesson 2.6 — Hands-on: your touch control panel and the next widgets](m02-ui-to-hardware/l06-touch-panel-lab/README.md)
- [Lesson 2.7 — Analog and touch: the ADC, the potentiometer and CapSense](m02-ui-to-hardware/l07-adc-capsense/README.md)
- [Lesson 2.8 — Filtering: EMA vs Median, then the gauge code](m02-ui-to-hardware/l08-filters/README.md)
- [Lesson 2.9 — Hands-on: the potentiometer gauge and touch slider](m02-ui-to-hardware/l09-pot-capsense-lab/README.md)

**Module 3 — Sensor Visualization on HMI**

- [Lesson 3.1 — The accelerometer and tilt: roll and pitch](m03-sensor-hmi/l01-accelerometer-tilt/README.md)
- [Lesson 3.2 — Gyro, the complementary filter and the level code](m03-sensor-hmi/l02-gyro-fusion/README.md)
- [Lesson 3.3 — Hands-on: the digital level](m03-sensor-hmi/l03-digital-level-lab/README.md)
- [Lesson 3.4 — Sampling right: Nyquist, aliasing and the ring buffer](m03-sensor-hmi/l04-sampling/README.md)
- [Lesson 3.5 — ui.Chart: multi-series plots and the real loop period](m03-sensor-hmi/l05-realtime-chart/README.md)
- [Lesson 3.6 — Hands-on: a three-axis acceleration chart](m03-sensor-hmi/l06-accel-chart-lab/README.md)
- [Lesson 3.7 — HMI design: cards, visual order, colour and the widget budget](m03-sensor-hmi/l07-hmi-design/README.md)
- [Lesson 3.8 — Building the dashboard: four cards in one loop](m03-sensor-hmi/l08-dashboard-build/README.md)
- [Lesson 3.9 — Hands-on: the mini-HMI dashboard and the 10-minute soak test](m03-sensor-hmi/l09-dashboard-lab/README.md)

**Module 4 — IoT Platform Connectivity**

- [Lesson 4.1 — WiFi and networking: dBm, DHCP, IP and DNS](m04-iot-connectivity/l01-wifi-networking/README.md)
- [Lesson 4.2 — The network status screen: reading the wifi code](m04-iot-connectivity/l02-network-status-code/README.md)
- [Lesson 4.3 — Hands-on: your team's network status page](m04-iot-connectivity/l03-network-status-lab/README.md)
- [Lesson 4.4 — MQTT: pub/sub, topics, QoS and the data budget](m04-iot-connectivity/l04-mqtt-concepts/README.md)
- [Lesson 4.5 — MQTT with a self-hosted platform: telemetry and commands](m04-iot-connectivity/l05-mqtt-platform/README.md)
- [Lesson 4.6 — Hands-on: two-way telemetry](m04-iot-connectivity/l06-mqtt-telemetry-lab/README.md)
- [Lesson 4.7 — TLS: certificates, the chain of trust and the handshake](m04-iot-connectivity/l07-tls-concepts/README.md)
- [Lesson 4.8 — The tesaiot module: MQTTs to the platform](m04-iot-connectivity/l08-tesaiot-module/README.md)
- [Lesson 4.9 — Hands-on: real readings over an encrypted channel](m04-iot-connectivity/l09-secure-telemetry-lab/README.md)

**Module 5 — Capstone: AIoT Mini-Product**

- [Lesson 5.1 — From a real problem to a design: canvas, schema and designing for failure](m05-capstone/l01-problem-to-design/README.md)
- [Lesson 5.2 — The starter: Sense, Decide, Show, Send](m05-capstone/l02-capstone-starter/README.md)
- [Lesson 5.3 — Build and present your AIoT mini-product](m05-capstone/l03-build-and-present/README.md)

</details>

## Licences

- **Content** (slides, READMEs, own diagrams and screenshots) — CC BY 4.0
- **Code** (`examples/`, `practice/`, `solution/`, `shared/`) — MIT, Copyright (c) 2026 Wiroon Sriborrirux, Advance Innovation Centre (AIC), Burapha University (full licence text in the repository's `LICENSES/MIT.txt`)
- **Third-party images** keep their own licences; authors, sources and licences are listed in [credits.yaml](credits.yaml). Figures from Infineon's board guide are used for teaching; rights remain with Infineon Technologies AG.

## Source

Adapted from **AIoT in Action — Embedded Systems for AIoT Developer** by Assoc. Prof. Wiroon Sriborrirux, Embedded Systems Engineering, Department of Electrical Engineering, Faculty of Engineering, Burapha University (BUU), Advance Innovation Centre (AIC) ([repository](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer) @ `a80bbe88` · [slides site](https://advance-innovation-centre-aic.github.io/embedded-systems-for-aiot-developer/)). The twelve decks were split into lessons, grouped into five modules, and the wording was adapted for a general audience. BENTO & TESAIoT.

## How to cite TESA

When you use, adapt or redistribute this course or part of it, credit it as follows (add "(adapted)" after the title if you changed it, and keep the upstream AIC credit):

> "AIoT in Action: From Touch Screen to IoT Platform (MicroPython)" from TESA Open Knowledge by the Thai Embedded Systems Association (TESA), https://github.com/tesaiot/tesa-qualification-program, licensed under CC BY 4.0 · Adapted from AIoT in Action — Embedded Systems for AIoT Developer, © 2026 Assoc. Prof. Wiroon Sriborrirux, Embedded Systems Engineering, Department of Electrical Engineering, Faculty of Engineering, Burapha University (BUU), Advance Innovation Centre (AIC) · BENTO & TESAIoT (CC BY 4.0 / MIT)

Attribution does not mean that TESA or Infineon endorse or certify your course or work. "TESA", "TQP" and "Certified by TESA and Infineon" are marks of the programme.
