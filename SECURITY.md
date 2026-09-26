# นโยบายความปลอดภัย (Security Policy)

*English: [below](#english)*

## แจ้งปัญหาความปลอดภัยแบบส่วนตัว

ถ้าพบช่องโหว่หรือข้อมูลลับหลุดในคลังนี้ **อย่าเปิด issue สาธารณะ** ให้แจ้งผ่านช่องทางส่วนตัวของ GitHub

1. ไปที่แท็บ **Security** ของ repository แล้วกด **Report a vulnerability**
   หรือเปิดลิงก์ https://github.com/tesaiot/tesa-qualification-program/security/advisories/new
2. บอกว่าพบที่ไฟล์ใด บรรทัดใด หรือหน้าใด ผลกระทบคืออะไร และทำซ้ำได้อย่างไร

ถ้าใช้ช่องทางนี้ไม่ได้ ส่งอีเมลถึง contact@tesa.or.th (ช่องทางติดต่อสาธารณะของ TESA ที่ https://www.tesa.or.th/contact)
โดยขึ้นหัวเรื่องว่า `[TESA Open Knowledge] Security` และอย่าแนบรหัสผ่านหรือกุญแจที่พบมาในอีเมล บอกแค่ตำแหน่งก็พอ

เราจะตอบรับเรื่อง ประเมินผลกระทบ แก้ไข แล้วเผยแพร่ security advisory เมื่อแก้เสร็จ และให้เครดิตผู้แจ้งถ้าผู้แจ้งต้องการ

## ขอบเขต

อยู่ในขอบเขต
- โค้ดในคลังนี้: `tools/`, `site/`, workflow ใน `.github/` และโค้ดตัวอย่างในบทเรียน
- ข้อมูลลับที่หลุดเข้ามา เช่น รหัส Wi-Fi, token, รหัสผ่านของ MQTT broker, กุญแจส่วนตัว หรือใบรับรองที่มีกุญแจ
- ขั้นตอนในบทเรียนที่ถ้าทำตามแล้วทำให้ระบบของผู้เรียนไม่ปลอดภัย เช่น สอนให้ปิดการตรวจใบรับรอง TLS โดยไม่อธิบายความเสี่ยง

นอกขอบเขต (แจ้งเจ้าของโดยตรง)
- ช่องโหว่ในผลิตภัณฑ์หรือบริการที่บทเรียนใช้ เช่น ชิปและ SDK ของผู้ผลิต ให้แจ้งผ่านช่องทางความปลอดภัยของผู้ผลิตรายนั้น
  (สำหรับ Infineon คือ PSIRT ของ Infineon) ส่วนแพลตฟอร์มหรือเครื่องมืออื่น ให้แจ้งผู้ดูแลแพลตฟอร์มนั้น

## บทเรียนไม่มีข้อมูลลับจริง

- โค้ดทุกไฟล์ในบทเรียนใช้ **ค่าตัวแทน** เช่น `WIFI_SSID = "<your-ssid>"` และ `WIFI_PASSWORD = "<your-password>"`
  ไม่มีรหัส Wi-Fi, token, รหัสผ่าน broker หรือกุญแจจริง
- ภาพหน้าจอต้องไม่เห็นรหัสผ่าน token หรือ QR ที่มีข้อมูลลับ
- ห้ามใส่ path ภายในของเครื่องหรือเซิร์ฟเวอร์ใด ๆ
- ถ้าบทเรียนต้องใช้ใบรับรองหรือกุญแจ ให้บอกวิธีสร้างหรือขอเอง ไม่แจกไฟล์ที่ใช้งานได้จริง

ถ้าคุณพบข้อมูลลับจริงในคลังนี้ อย่านำไปลองใช้ แจ้งตามช่องทางข้างบน ข้อมูลลับที่เคย push ขึ้น repository สาธารณะแล้วถือว่ารั่ว
ต้องเปลี่ยนที่ต้นทาง ลบออกจากไฟล์อย่างเดียวไม่พอ

---

## English

**Report privately.** If you find a vulnerability or a leaked secret in this repository, **do not open a public issue.**
Use GitHub private vulnerability reporting: open the repository's **Security** tab and choose **Report a vulnerability**, or go to
https://github.com/tesaiot/tesa-qualification-program/security/advisories/new. Say where you found it (file, line or page), what
the impact is and how to reproduce it. If that channel is unavailable, e-mail contact@tesa.or.th (TESA's public contact, listed
at https://www.tesa.or.th/contact) with the subject `[TESA Open Knowledge] Security`. Do not paste any secret you found; the
location is enough. We acknowledge, assess, fix, then publish a security advisory, and credit the reporter if they wish.

**In scope:** code in this repository (`tools/`, `site/`, workflows in `.github/`, lesson example code); leaked secrets such as
Wi-Fi passwords, tokens, MQTT broker credentials, private keys or certificates with keys; and lesson steps that would leave a
learner's system insecure, such as disabling TLS certificate checks without explaining the risk.
**Out of scope:** vulnerabilities in products or services a lesson uses. Report chip and SDK issues to the vendor's own product
security channel (for Infineon, Infineon PSIRT) and platform or tool issues to their maintainers.

**Lessons never contain real credentials.** Code uses placeholders such as `WIFI_SSID = "<your-ssid>"` and
`WIFI_PASSWORD = "<your-password>"`; screenshots show no passwords, tokens or secret-bearing QR codes; no internal machine or
server paths are published; lessons that need certificates or keys explain how to create or request them and never ship working
ones. If you find a real secret here, do not try it; report it. A secret that has been pushed to a public repository is
compromised and must be changed at its source; deleting it from the file is not enough.
