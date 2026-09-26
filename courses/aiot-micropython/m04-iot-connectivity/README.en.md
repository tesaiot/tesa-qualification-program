# Module 4 — IoT Platform Connectivity

> IoT Platform Connectivity · [Course page](../README.md)

Connect to WiFi, learn to read network values properly, publish telemetry and take commands over MQTT to a self-hosted platform, then move up to MQTTs over TLS.

## Module objectives

Bring the board onto the network in a way you can diagnose when it breaks (dBm, DHCP, gateway, DNS), send two-way real data over MQTT to a self-installed TESAIoT Community Edition, and send the same values through a TLS-encrypted channel while being able to say what it protects.

## Network and platform to use when learning on your own

- **WiFi:** your home WiFi or phone hotspot, set up per the table in lesson 1.4 (an English name with no spaces, a password of at least 8 characters, the 2.4 GHz band). The board cannot use WiFi that needs a browser login.
- **Plain MQTT (port 1883):** the public practice broker `broker.hivemq.com` (backup `test.mosquitto.org`), with a unique code in your `client_id` and topic, such as a nickname followed by a random 4-digit number (`nok4821`), or [TESAIoT Community Edition](https://github.com/tesaiot/tesaiot-community-edition) installed on your own computer (lessons 4.5–4.6)
- **MQTTs (lessons 4.7–4.9):** your TESAIoT Platform account; the device's credentials come from the platform's device management page (a self-installed CE cannot be used for MQTTs from the board, because its root CA does not match the one baked into the firmware — see lesson 4.7)
- If learning in a group, your organiser may have already prepared a broker and device identity for you

## Lessons

| Lesson | Topic | Time (min) | Slides |
|---|---|---|---|
| [4.1](l01-wifi-networking/README.md) | WiFi and networking: dBm, DHCP, IP and DNS | 50 | [slides.md](l01-wifi-networking/slides.md) |
| [4.2](l02-network-status-code/README.md) | The network status screen: reading the wifi code | 55 | [slides.md](l02-network-status-code/slides.md) |
| [4.3](l03-network-status-lab/README.md) | Hands-on: your team's network status page | 65 | [slides.md](l03-network-status-lab/slides.md) |
| [4.4](l04-mqtt-concepts/README.md) | MQTT: pub/sub, topics, QoS and a data budget | 55 | [slides.md](l04-mqtt-concepts/slides.md) |
| [4.5](l05-mqtt-platform/README.md) | MQTT with a self-hosted platform: telemetry and commands | 75 | [slides.md](l05-mqtt-platform/slides.md) |
| [4.6](l06-mqtt-telemetry-lab/README.md) | Hands-on: two-way telemetry | 65 | [slides.md](l06-mqtt-telemetry-lab/slides.md) |
| [4.7](l07-tls-concepts/README.md) | TLS: certificates, the chain of trust and the handshake | 55 | [slides.md](l07-tls-concepts/slides.md) |
| [4.8](l08-tesaiot-module/README.md) | The tesaiot module: MQTTs to the platform | 75 | [slides.md](l08-tesaiot-module/slides.md) |
| [4.9](l09-secure-telemetry-lab/README.md) | Hands-on: sending real values over an encrypted channel | 70 | [slides.md](l09-secure-telemetry-lab/slides.md) |

The lessons in this module come in sets of three: concept → code walk-through → hands-on (the third lesson of each set has practice files and solutions).

## Module checkpoint

You pass this module when you can do every item below (the details are in the **Lab** section of the hands-on lessons):

- [ ] The network status page shows a table of networks sorted by strength, the IP address from DHCP, and a ping time that updates every 3 seconds
- [ ] You can explain where the problem lies if the gateway passes but the internet stays silent
- [ ] Publish JSON from a real sensor every 5 seconds, and a `{"cmd":"toggle"}` command switches a light on the board
- [ ] Your team's telemetry appears on the platform's dashboard over TLS, and you can say what serverTLS protects and what it does not
