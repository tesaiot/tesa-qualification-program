---
id: c-found.m06.l02
lang: th
title: {th: CI สำหรับเฟิร์มแวร์, en: CI for firmware}
summary: {th: ให้ GitHub Actions build ตรวจรูปแบบโค้ด วิเคราะห์แบบสถิต และรัน test ทุกการเปลี่ยนแปลง, en: 'Have GitHub Actions build, format-check, statically analyse and test every change.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m06.l01]
objectives:
- {th: เขียน workflow ของ GitHub Actions ที่รัน unit test บนเครื่องโฮสต์ทุก pull request, en: Write a GitHub Actions workflow that runs the host unit tests on every pull request.}
- {th: เพิ่มขั้นตรวจรูปแบบโค้ดด้วย clang-format และวิเคราะห์แบบสถิตด้วย cppcheck, en: Add a clang-format check and cppcheck static analysis.}
- {th: อธิบายว่าอะไรที่ CI บน runner สาธารณะตรวจได้ และอะไรที่ต้องทดสอบบนบอร์ดจริง, en: Explain what CI on public runners can check and what still needs a real board.}
develops:
- {skill: test.cicd, to: 3}
- {skill: vcs.git, to: 2}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: pre-alpha
translation: pending
---

## เป้าหมาย

1. เขียน workflow ของ GitHub Actions ที่รัน unit test บนเครื่องโฮสต์ทุก pull request
2. เพิ่มขั้นตรวจรูปแบบโค้ดด้วย clang-format และวิเคราะห์แบบสถิตด้วย cppcheck
3. อธิบายว่าอะไรที่ CI บน runner สาธารณะตรวจได้ และอะไรที่ต้องทดสอบบนบอร์ดจริง

> **บทเรียนนี้อยู่ระหว่างเขียน** (สถานะ pre-alpha) หน้านี้มีเฉพาะเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว
> เนื้อหา ตัวอย่าง แบบฝึก และเช็กความเข้าใจจะตามมา ถ้าอยากช่วยเขียน ดู [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## แนวคิด

หัวข้อที่บทเรียนนี้จะครอบคลุม

- workflow, job และ step
- ตรวจรูปแบบและวิเคราะห์แบบสถิต
- cross-build บน runner
- สิ่งที่ต้องทดสอบบนฮาร์ดแวร์

## แหล่งอ้างอิง

- [GitHub Actions documentation](https://docs.github.com/en/actions)
- [ClangFormat](https://clang.llvm.org/docs/ClangFormat.html)
- [Cppcheck](https://cppcheck.sourceforge.io/)
