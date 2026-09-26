# Module 2 · The OPTIGA™ Trust M secure element

**Module goal:** use the secure element through its SDK by the rules, so the secret key never leaves the chip.

Status **alpha** (content complete, awaiting pilot teaching and feedback) · about 140 minutes

**Module agreement:** every lab only reads status and acquires or releases the chip's access gate. None of them writes data or metadata to the chip, and no step touches the C0 (LcsO) metadata tag.

| Lesson | Topic | Time |
|---|---|---|
| [sec-iot.m02.l01](l01-secure-element-role/README.md) | What the secure element does for us | 70 minutes |
| [sec-iot.m02.l02](l02-chip-access-discipline/README.md) | Rules for accessing the chip | 70 minutes |

## Module checkpoint

- [ ] ran the SDK's chip-access example and can explain the init, acquire, release sequence
- [ ] read the HSM's status without starting a transaction with the chip
