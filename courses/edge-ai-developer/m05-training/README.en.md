# Module 5 — Training a model and deploying it to several targets

> Training and deploying to several targets · [Course page](../README.md)

Prepare a balanced dataset, train our own model in Docker, squeeze it into int8, then take one single file and run it on the web, Cortex-A and an MCU through Vela, while measuring parity.

## Module goal

Build a model of our own, from data all the way to the chip, and be able to measure exactly what trade-off each target makes.

## Lessons

| Lesson | Topic | Time (min) | Slides |
|---|---|---|---|
| [5.1](l01-dataset-engineering/README.md) | Dataset engineering: class balance, windows and the train/val/test split | 65 | [slides.md](l01-dataset-engineering/slides.md) |
| [5.2](l02-dataset-lab/README.md) | Hands-on: recording a balanced dataset on the board, then splitting it on the PC | 75 | [slides.md](l02-dataset-lab/slides.md) |
| [5.3](l03-training-pipeline/README.md) | Training a model in Docker: one artifact, four targets | 65 | [slides.md](l03-training-pipeline/slides.md) |
| [5.4](l04-inside-training/README.md) | Inside training: Keras, Conv1D, gradient descent, int8 and the confusion matrix | 70 | [slides.md](l04-inside-training/slides.md) |
| [5.5](l05-train-lab/README.md) | Hands-on: fill in a training script and run it in Docker | 75 | [slides.md](l05-train-lab/slides.md) |
| [5.6](l06-web-runtime/README.md) | Running a model on the web: LiteRT.js, int8 I/O and parity | 70 | [slides.md](l06-web-runtime/slides.md) |
| [5.7](l07-web-parity-lab/README.md) | Hands-on: matching the web's verdict to the PC's, and the Cortex-A story | 75 | [slides.md](l07-web-parity-lab/slides.md) |
| [5.8](l08-quantize-and-vela/README.md) | Quantizing and Vela: getting our model onto the Ethos-U55 | 70 | [slides.md](l08-quantize-and-vela/slides.md) |
| [5.9](l09-three-targets-lab/README.md) | Hands-on: comparing three targets — MCU, web and PC | 75 | [slides.md](l09-three-targets-lab/slides.md) |

Lessons come in pairs: a concept lesson followed by a **hands-on** lesson with a practice file, a solution, and a lab.

## Module checkpoint

You pass this module once you can do all of the following (details are in the **Lab** section of each hands-on lesson):

- [ ] A clean, balanced, split dataset from the board — every set (train/val/test) has all three classes in close-to-equal proportion (lesson 5.2).
- [ ] Successfully train a Keras model in Docker, getting a report of float32 accuracy, int8 accuracy and a confusion matrix on a test set the model has never seen, along with the `model_int8.tflite` and `.norm.npz` files (lesson 5.5).
- [ ] The web file's verdict matches the PC side within tolerance (max|score_pc − score_web| ≤ TOL, and the winning class matches), and can explain why they don't need to match bit for bit (lesson 5.7).
- [ ] A comparison table of three targets (MCU, web, PC) with real numbers, explaining why accuracy matches but latency differs, and why the MCU needs Vela (lesson 5.9).
