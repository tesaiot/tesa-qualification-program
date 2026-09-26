# Module 5 · Secure device provisioning

**Module goal:** enrol a device with a CSR so the secret key never leaves the chip, and bring everything together into one secure device.

Status **alpha** (content complete, awaiting pilot teaching and feedback) · about 215 minutes

**Module agreement:** real enrolment creates a new key pair on the chip in place of the old one, and Protected Update permanently advances the version counter. Both need the instructor's permission first. No step writes the C0 (LcsO) metadata tag.

| Lesson | Topic | Time |
|---|---|---|
| [sec-iot.m05.l01](l01-csr-enrolment/README.md) | Enrolling with a CSR | 70 minutes |
| [sec-iot.m05.l02](l02-provisioning-screens/README.md) | On-device provisioning screens | 70 minutes |
| [sec-iot.m05.l03](l03-capstone-secure-device/README.md) | Capstone: one secure device | 75 minutes |

## Module checkpoint

- [ ] can explain the CSR's journey, from being generated on the chip to the certificate coming back
- [ ] capstone: one device that is enrolled, connects with mTLS and sends data to the platform, with an evidence report and an updated threat model (also accepts a Protected Update once the instructor allows it)
