# Module 3 — Sensor Visualization on HMI

> Sensor Visualization on HMI · [Course page](../README.md)

Turn acceleration into tilt angles, sample a signal correctly and draw it live, and assemble a four-card Mini-HMI Dashboard that keeps running.

## Module objectives

Read a real sensor (the IMU, the compass, CapSense, the knob) and tell its story on screen so a reader understands it: a two-axis digital level, a three-axis acceleration chart that knows its loop's real period, and a four-card dashboard that stays within the widget budget and runs for ten minutes.

## Lessons

| Lesson | Topic | Time (min) | Slides |
|---|---|---|---|
| [3.1](l01-accelerometer-tilt/README.md) | The accelerometer and tilt: roll and pitch | 45 | [slides.md](l01-accelerometer-tilt/slides.md) |
| [3.2](l02-gyro-fusion/README.md) | Gyro, the complementary filter and the level code | 55 | [slides.md](l02-gyro-fusion/slides.md) |
| [3.3](l03-digital-level-lab/README.md) | Hands-on: a digital level | 70 | [slides.md](l03-digital-level-lab/slides.md) |
| [3.4](l04-sampling/README.md) | Sampling a signal correctly: Nyquist, aliasing and the ring buffer | 50 | [slides.md](l04-sampling/slides.md) |
| [3.5](l05-realtime-chart/README.md) | ui.Chart: multi-series charts and the loop's real period | 55 | [slides.md](l05-realtime-chart/slides.md) |
| [3.6](l06-accel-chart-lab/README.md) | Hands-on: a three-axis acceleration chart | 70 | [slides.md](l06-accel-chart-lab/slides.md) |
| [3.7](l07-hmi-design/README.md) | HMI design: cards, eye path, colour and the widget budget | 55 | [slides.md](l07-hmi-design/slides.md) |
| [3.8](l08-dashboard-build/README.md) | Assembling a dashboard: four cards in one loop | 60 | [slides.md](l08-dashboard-build/slides.md) |
| [3.9](l09-dashboard-lab/README.md) | Hands-on: the Mini-HMI Dashboard and a 10-minute test | 75 | [slides.md](l09-dashboard-lab/slides.md) |

The lessons in this module come in sets of three: concept → code walk-through → hands-on (the third lesson of each set has practice files and solutions).

## Module checkpoint

You pass this module when you can do every item below (the details are in the **Lab** section of the hands-on lessons):

- [ ] Laid flat, it reads about 0°; tilted, the roll/pitch bars move in the correct direction, and threshold lamps light one at a time
- [ ] Three chart lines run live, the stop button really stops the data, and the screen reports the loop's real period in milliseconds
- [ ] You can explain aliasing from your own loop's real period figure
- [ ] The four-card dashboard stays within the 32-widget budget and runs continuously for 10 minutes with no hang and no Traceback
