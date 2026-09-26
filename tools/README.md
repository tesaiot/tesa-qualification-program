# เครื่องมือตรวจและสร้างข้อมูล · Tools

[ภาษาไทย](#ภาษาไทย) · [English](#english)

## ภาษาไทย

เครื่องมือในโฟลเดอร์นี้ตรวจว่าเนื้อหาทั้ง repo ตรงตามสัญญา (BUILD_SPEC) และสร้างไฟล์ที่ต้องสร้างจากข้อมูล
ทุกตัวเป็น Python ธรรมดา ใช้ Python 3.11 ขึ้นไป (CI ใช้ 3.12) และรันบนเครื่องของผู้เขียนได้โดยไม่ต้องมีอินเทอร์เน็ต

### ติดตั้ง

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r tools/requirements.txt
```

### ก่อนเปิด pull request ให้รันสามคำสั่งนี้

```bash
python3 tools/validate.py          # ตรวจทุกอย่าง error = exit 1, warning แสดงแยกท้ายรายงาน
python3 tools/gen_credits.py       # สร้าง CREDITS.md ใหม่จาก courses/*/credits.yaml
python3 tools/gen_reuse.py         # สร้าง REUSE.toml ใหม่ แล้วรัน `reuse lint`
```

### เครื่องมือแต่ละตัว

| คำสั่ง | ทำอะไร |
|---|---|
| `python3 tools/validate.py` | ตรวจ schema, โครงสร้างหลักสูตร/โมดูล/บทเรียน, รหัสทักษะ, ลิงก์และภาพ, ถ้อยคำ, เครดิต, ความลับในโค้ด, เส้นทางภายใน และการให้เครดิต TESA · `--strict` นับ warning เป็น error · `--list-checks` ดูรายการตรวจทั้งหมด · `--json FILE` เขียนผลเป็น JSON |
| `python3 tools/check_terms.py [ไฟล์หรือโฟลเดอร์]` | ตรวจถ้อยคำที่ห้ามใช้ในข้อความที่ผู้เรียนอ่าน (ดูด้านล่าง) |
| `python3 tools/export.py --out DIR` | เขียน `skills.json` `courses.json` `coverage.json` `case.json` ให้เว็บไซต์ใช้ |
| `python3 tools/gen_credits.py [--check]` | สร้าง `CREDITS.md` · `--check` ออก exit 1 ถ้าไฟล์ไม่ตรงกับ credits.yaml |
| `python3 tools/gen_reuse.py [--check]` | สร้าง `REUSE.toml` ตามนโยบายใน `tools/policy.yaml` · `--check` ออก exit 1 ถ้าไม่ตรง |
| `python3 tools/check_authorship.py [--range A..B]` | ตรวจทุก commit ว่าผู้เขียนและผู้ร่วมเขียนเป็นคน ไม่มีเครดิตผู้ช่วย AI · exit 1 ถ้าพบ · exit 2 ถ้าตรวจไม่ได้ (เช่น clone แบบ shallow) |
| `python3 tools/i18n_stale.py [--strict]` | บอกว่าหน้า `README.en.md` ใดแปลจากเนื้อหาไทยฉบับเก่า · `--hash README.md` พิมพ์ค่าที่ต้องใส่ |
| `python -m pytest tools/tests -q` | ทดสอบเครื่องมือเอง ทุกข้อตรวจต้องพิสูจน์ได้ทั้งตอนผ่านและตอนไม่ผ่าน |

### ถ้อยคำที่ห้ามใช้

ข้อความที่ผู้เรียนอ่านใช้คำว่า บทเรียน โมดูล หลักสูตร ไม่ใช้ `คาบ` หรือ `คาบเรียน` ในความหมายของชั่วโมงเรียน
และไม่เรียกหน่วยการเรียนว่า `session N` ใน `courses/**` เป็น error ที่อื่นเป็น warning

- ใช้ได้: `คาบเวลา`, `คาบของสัญญาณ`, `คาบ (period)`, คาบตามด้วยตัวเลขและหน่วยเวลา เช่น `มีคาบ 20 ms`, `คาบเกี่ยว`
- ไม่ตรวจ: โค้ดใน code block, โค้ดในบรรทัด, URL และปลายทางของลิงก์, ไฟล์โค้ด, บล็อก `source:` ใน front matter

### เมื่อเครื่องมือฟ้อง

- **secrets**: เปลี่ยนค่าเป็นตัวแทน เช่น `"<รหัสผ่านของคุณ>"` ถ้าเป็นค่าที่ตั้งใจให้ผู้เรียนเห็นจริง
  ให้เพิ่มบรรทัดใน `tools/credentials_allow.txt` พร้อมเหตุผล ถ้าเคย push รหัสผ่านจริงไปแล้ว ต้องเปลี่ยนรหัสที่เครือข่ายด้วย
- **leaks**: ถ้าบรรทัดนั้นเป็นรูปแบบที่ตัวตรวจอีกตัวใช้ค้นหา (ไม่ใช่การรั่วจริง) ใส่คำ `validate:ignore-leak` ไว้ในบรรทัดเดียวกัน
- **i18n**: หลังแปลเสร็จ ใส่ `source_sha256:` ใน front matter ของ `README.en.md` ด้วยค่าจาก
  `python3 tools/i18n_stale.py --hash <โฟลเดอร์บทเรียน>/README.md`
- **time**: เวลารวมใน `time_min` ต้องอยู่ระหว่าง 10–240 นาที ถ้าเกิน 75 นาทีจะเตือน ยกเว้นโฟลเดอร์บทเรียนที่ชื่อมีคำว่า `lab`
- **tesa-cite / tesa-footer**: ทุก `README.md` / `README.en.md` ของหลักสูตรต้องจบด้วยหัวข้อ `อ้างอิง TESA` /
  `How to cite TESA` ที่มี URL ของ repo และทุก `slides.md` ต้องมี `footer:` ที่มีคำว่า TESA (ใช้บรรทัดเครดิตจาก `site.config.yaml`)

ค่าที่เครื่องมือใช้ร่วมกันอยู่ใน `tools/policy.yaml` ส่วนที่อยู่เว็บ URL ของ repo และบรรทัดเครดิตอ่านจาก
`site.config.yaml` เสมอ ถ้าไฟล์นั้นหายไป เครื่องมือจะใช้ค่าสำรองใน policy และแจ้งเตือน

## English

These tools check that the whole repository keeps the content contract (BUILD_SPEC) and generate the
files that are derived from data. They are plain Python 3.11+ (CI runs 3.12) and run offline.

### Install

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r tools/requirements.txt
```

### Before you open a pull request

```bash
python3 tools/validate.py          # errors -> exit 1; warnings are listed separately
python3 tools/gen_credits.py       # regenerate CREDITS.md from courses/*/credits.yaml
python3 tools/gen_reuse.py         # regenerate REUSE.toml, then run `reuse lint`
```

### The tools

| Command | What it does |
|---|---|
| `python3 tools/validate.py` | Schemas, course/module/lesson structure, skill ids, links and images, wording, credits, secrets, internal paths, TESA credit. `--strict` turns warnings into errors; `--list-checks`; `--json FILE`. Prints `::error file=…,line=…::` annotations when `GITHUB_ACTIONS` is set. |
| `python3 tools/check_terms.py [paths]` | Forbidden learner-facing wording (below). |
| `python3 tools/export.py --out DIR` | Writes `skills.json`, `courses.json`, `coverage.json`, `case.json` for the site. |
| `python3 tools/gen_credits.py [--check]` | Builds `CREDITS.md`; `--check` exits 1 when it is stale. |
| `python3 tools/gen_reuse.py [--check]` | Builds `REUSE.toml` from `tools/policy.yaml` and the credits; `--check` exits 1 when stale. |
| `python3 tools/check_authorship.py [--range A..B]` | Checks every commit: authors and co-authors are people, no AI-assistant credit · exit 1 when found · exit 2 when it could not check (e.g. a shallow clone). |
| `python3 tools/i18n_stale.py [--strict]` | Lists English pages translated from an older Thai body; `--hash README.md` prints the value to record. |
| `python -m pytest tools/tests -q` | Self-tests: every check is shown to pass on a clean fixture AND to fail on a one-change mutation of it. |

### Checks (`python3 tools/validate.py --list-checks`)

`yaml` `schema` `skills` `catalog` `structure` `prereq` `tracks` `roles` `links` `alt` (warning)
`evidence` `pairs` `slides` `quiz` `translation` `credits` `terms` `size` `secrets` `leaks`
`tesa-footer` `tesa-cite` `tesa-notice` `time` `config` (warning) `internal`.
`time`: a lesson's `time_min` total outside 10–240 min is an ERROR; above 75 min is a WARNING unless the
lesson folder name contains `lab` (limits in `tools/policy.yaml`).
A check that crashes is reported as an `internal` ERROR ("could not check"), never as a pass.

### Wording

Learner-facing text says lesson / module / course. It never uses `คาบ` or `คาบเรียน` for a class
period, nor `session N` for a unit of learning: ERROR in `courses/**`, WARNING elsewhere. Allowed:
`คาบเวลา`, `คาบของสัญญาณ`, `คาบ (period)`, a period with a time unit (`มีคาบ 20 ms`), `คาบเกี่ยว`.
Not scanned: fenced and inline code, URLs and link targets, code files, the front-matter `source:` block.

### When a check fails

- **secrets** — replace the value with a `"<placeholder>"`. Add a value to `tools/credentials_allow.txt`
  only with a written reason. A real password that was ever pushed must also be changed on the network.
- **leaks** — a line that is another checker's own pattern (not a leak) may carry `validate:ignore-leak`.
- **i18n** — after translating, record `source_sha256:` in the `README.en.md` front matter, using
  `python3 tools/i18n_stale.py --hash <lesson>/README.md`.
- **tesa-cite / tesa-footer** — every course `README.md` / `README.en.md` ends with an `อ้างอิง TESA` /
  `How to cite TESA` section containing the repo URL; every `slides.md` has a `footer:` containing TESA
  (the credit line in `site.config.yaml`).

Shared settings live in `tools/policy.yaml`. The site origin/base, repo URL and credit line are always read
from `site.config.yaml`; if it is missing, the tools use the policy fallback and say so.

### Outputs for the site (`export.py`)

- `skills.json` — framework, levels, importance, areas, groups, skills with `uuid` and `url`, roles.
  `uuid = uuid5(NAMESPACE_URL, "<origin><base>/skills/<id>/")`.
- `courses.json` — catalog, each in-tree course.yaml with its modules and lessons (front matter flattened,
  plus `path`, `readme`, `readme_en`, `en` = EN front matter, `files`), and the tracks.
- `coverage.json` — `skills.<id>` = `[{lesson, course, mode, level, to|evidence}]`, `courses.<id>` totals,
  and overall `totals` including the uncovered skill ids.
- `case.json` — a CASE 1.1-shaped CFPackage: CFDocument, CFItems (`Group`, `Skill`;
  `humanCodingScheme` = id), CFAssociations `isChildOf` (skill → group, group → document), CFDefinitions.
  Timestamps come from `SOURCE_DATE_EPOCH`, else the last commit of `skills/skills.yaml`.
