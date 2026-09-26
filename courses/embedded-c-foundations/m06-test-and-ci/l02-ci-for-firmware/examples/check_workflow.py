# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: Apache-2.0
#
# examples/check_workflow.py — ตรวจ workflow ของบทเรียน 6.2 ในเครื่อง ก่อน push ขึ้น GitHub
#
#     python3 -m venv .venv && .venv/bin/pip install pyyaml==6.0.3
#     .venv/bin/python check_workflow.py ../practice/firmware-ci.yml
#
# ตรวจ "โครง" ของ workflow ตามกติกาของบทเรียน ไม่ได้รัน workflow จริง
# ผลจริงดูได้บนแท็บ Actions ของ repo คุณหลัง push เท่านั้น
import re
import sys

try:
    import yaml
except ImportError:
    print("NOT CHECKED: PyYAML is not installed (pip install pyyaml==6.0.3)")
    sys.exit(3)

# job ที่ต้องมี และขั้นของ ci.sh ที่ job นั้นต้องเรียก
STAGES = {"tests": "tests", "format": "format", "static-analysis": "static", "cross-compile": "cross"}
# สิ่งที่ต้องเห็นในคำสั่งของแต่ละ job เพื่อให้รู้ว่าเครื่องมือมาจากไหน และรุ่นอะไร
TOOLS = {
    "tests": (r"--branch\s+v2\.7\.0", "Unity cloned at the tag v2.7.0"),
    "format": (r"clang-format==\d+\.\d+\.\d+", "clang-format installed at an exact version"),
    "static-analysis": (r"apt-get install.*\bcppcheck\b", "cppcheck installed with apt"),
    "cross-compile": (r"apt-get install.*\bgcc-arm-none-eabi\b", "gcc-arm-none-eabi installed with apt"),
}
SHA_PIN = re.compile(r"^[^@\s]+@[0-9a-f]{40}$")


def main(path):
    try:
        with open(path, encoding="utf-8") as f:
            wf = yaml.safe_load(f)
    except (OSError, yaml.YAMLError) as e:
        print(f"FAIL  file reads as YAML: {e}")
        return 1
    if not isinstance(wf, dict):
        print("FAIL  file is a workflow mapping")
        return 1

    results = []

    def check(ok, rule, detail=""):
        results.append(ok)
        print(("PASS  " if ok else "FAIL  ") + rule + ("" if ok or not detail else f": {detail}"))

    # YAML 1.1 อ่านคีย์ on เป็นค่า true ของ boolean ไม่ใช่ข้อความ "on" จึงต้องหาทั้งสองแบบ
    triggers = wf.get("on", wf.get(True))
    if isinstance(triggers, str):
        triggers = [triggers]
    check(triggers is not None and "pull_request" in triggers,
          "runs on every pull request", f"triggers are {triggers!r}")

    check(wf.get("permissions") == {"contents": "read"},
          "GITHUB_TOKEN is read-only (permissions: contents: read)", f"got {wf.get('permissions')!r}")

    jobs = wf.get("jobs") or {}
    steps_of = {name: (job or {}).get("steps") or [] for name, job in jobs.items()}

    unpinned = [f"{name}: {s['uses']}" for name, steps in steps_of.items() for s in steps
                if isinstance(s, dict) and "uses" in s
                and not s["uses"].startswith(("./", "docker://")) and not SHA_PIN.match(s["uses"])]
    check(not unpinned, "every action is pinned to a full commit SHA", ", ".join(unpinned))

    leftovers = [name for name, steps in steps_of.items() for s in steps
                 if isinstance(s, dict) and "TODO" in f"{s.get('name', '')} {s.get('run', '')}"]
    check(not leftovers, "no TODO placeholder is left", ", ".join(sorted(set(leftovers))))

    # ขั้นที่กลืนความล้มเหลวจะเขียวเสมอ: || true, || : หรือ continue-on-error
    swallowed = [name for name, steps in steps_of.items()
                 if (jobs.get(name) or {}).get("continue-on-error")]
    swallowed += [name for name, steps in steps_of.items() for s in steps
                  if isinstance(s, dict) and (s.get("continue-on-error")
                                              or re.search(r"\|\|\s*(true|:)(\s|$|;)", str(s.get("run", ""))))]
    check(not swallowed, "no step hides a failure (|| true, continue-on-error)",
          ", ".join(sorted(set(swallowed))))

    for name, stage in STAGES.items():
        if name not in jobs:
            check(False, f"job '{name}' exists")
            continue
        job = jobs[name] or {}
        runs = "\n".join(str(s.get("run", "")) for s in steps_of[name] if isinstance(s, dict))
        check(re.search(rf"\bci\.sh\s+{stage}\b", runs) is not None,
              f"job '{name}' runs 'bash ci.sh {stage}'")
        pattern, what = TOOLS[name]
        check(re.search(pattern, runs) is not None, f"job '{name}': {what}")
        runner = str(job.get("runs-on", ""))
        check(bool(runner) and "latest" not in runner,
              f"job '{name}' names a fixed runner image", f"runs-on is {runner!r}")
        check("timeout-minutes" in job, f"job '{name}' sets timeout-minutes")

    failed = results.count(False)
    print(f"{len(results) - failed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python check_workflow.py <workflow.yml>", file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
