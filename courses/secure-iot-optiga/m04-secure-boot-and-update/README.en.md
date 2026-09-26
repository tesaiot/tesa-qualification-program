# Module 4 · Secure boot and Protected Update

**Module goal:** understand the chain of trust from boot onwards, and how updates are protected against rollback.

Status **alpha** (content complete, awaiting pilot teaching and feedback) · about 140 minutes

**Module agreement:** no lab provisions the device's secure boot or writes the C0 (LcsO) metadata tag. The optional lab that sends a real Protected Update permanently advances the target slot's version counter, so it needs the instructor's permission first.

| Lesson | Topic | Time |
|---|---|---|
| [sec-iot.m04.l01](l01-secure-boot/README.md) | Secure boot and the chain of trust | 70 minutes |
| [sec-iot.m04.l02](l02-protected-update/README.md) | Protected Update | 70 minutes |

## Module checkpoint

- [ ] a chain-of-trust diagram for the board, from boot through to the application
- [ ] can explain the anti-rollback counter and the effect of the manifest lock
