---
id: c-found.m02.l03
lang: en
title: {th: Git สำหรับงานเฟิร์มแวร์, en: Git for firmware work}
summary: {th: 'เก็บประวัติของเฟิร์มแวร์ด้วย commit, branch และ tag โดยไม่เก็บไฟล์ build และข้อมูลลับ', en: 'Keep firmware history with commits, branches and tags, without build outputs or secrets.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m02.l02]
objectives:
- {th: สร้าง repository ของโปรเจกต์เฟิร์มแวร์ที่มี .gitignore ตัดไฟล์ build และ dependency ที่ดึงมา, en: Create a firmware repository whose .gitignore excludes build outputs and fetched dependencies.}
- {th: ใช้ branch สำหรับงานใหม่ และ tag สำหรับเฟิร์มแวร์ที่ปล่อยจริง พร้อมข้อความ commit ที่อธิบายเหตุผล, en: 'Use branches for new work and tags for released firmware, with commit messages that explain why.'}
- {th: ตรวจก่อน push ว่าไม่มีรหัส WiFi กุญแจ หรือ token อยู่ในประวัติ และอธิบายว่าทำไมการลบภายหลังไม่พอ, en: 'Check before pushing that no WiFi password, key or token is in history, and explain why deleting it later is not enough.'}
develops:
- {skill: vcs.git, to: 3}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
source_sha256: f97e33451587c1d0040c802e74aa4f15a78ee7f60b19929449a97194df01cea8
---

## Objectives

By the end of this lesson, you will be able to

1. Create a firmware project repository whose `.gitignore` excludes build outputs and fetched dependencies.
2. Use branches for new work and tags for firmware that actually ships, with commit messages that explain the reasoning.
3. Check before pushing that no WiFi password, key or token is in the history, and explain why deleting it afterward isn't enough.

Takes about 70 minutes (concepts 15 · practice 25 · lab 25 · check 5). You need Git and bash on your machine.

## Before you start

Two review questions from lessons 2.1 and 2.2.

1. Which folders appear after `make getlibs` and `make build`, and roughly how big are they?
2. If the Makefile sets `ENABLE_PAGE_EXAMPLES ?= 0` and you enable examples from the command line, what extra thing does your build record need to note?

## See it work first

In the template folder you built in lesson 2.1, have Git count how many files it would commit right now.

```sh
cd bento-firmware-template-mtb-only
git init
git status --short --untracked-files=all | wc -l
du -sh build proj_*/build 2>/dev/null
```

**Predict before you run it:** roughly how many thousand does that first number come to? Then look at how large the build folders are combined. Every byte of those files can be recreated with `make build`. Committing them to history would bloat the repository with every build, and every diff would fill up with files no one reads. Now copy [examples/firmware.gitignore](examples/firmware.gitignore) to `.gitignore` and count again. The drop is what shouldn't be in history.

## Concepts

### 1. What belongs in a repository, and what doesn't

There is one rule: **keep what can't be regenerated; don't keep what can.** The SDK's top-level `.gitignore` states this rule right in its first comment.

```gitignore
# Build output. Every one of these is reproducible from what is committed.
build/
build-*/
mtb_shared/
*.o
*.a
.DS_Store
```

Source: [tesaiot-pse84-devkit-sdk's .gitignore lines 1-7](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/.gitignore#L1-L7) (Apache-2.0, tesaiot-pse84-devkit-sdk)

| Keep | Don't keep |
|---|---|
| `.c` / `.h` source, the Makefile and `*.mk` files | `build/` and `build-*/` for every project |
| `deps/*.mtb` files, which say what to fetch and at what version | `mtb_shared/` (re-fetchable with `make getlibs`) |
| BSP settings and files the Configurator generates, which the SDK's template also keeps | `.o`, `.elf`, `.hex`, `.map` (a released hex belongs attached to a release instead) |
| The template's `LICENSE` and `NOTICE` (Apache-2.0 requires keeping them) | Your machine's own secret files |

Notice the `*.a` line in the SDK's file: the consequence is that the public repository has no prebuilt libraries at all — they come with the release zip (lesson 2.1). Your own project has to make this decision deliberately; that's why our example file leaves it as a choice near the end. One more thing to know: `.gitignore` only affects files that have **never been tracked**. A file that's already been committed must be removed with `git rm --cached <path>`, and anyone can still force-add an ignored file with `git add -f` — which is why we add another layer of checking with a hook.

### 2. Branches for work, tags for what ships, commit messages for the reasoning

- **A branch** separates one piece of work from the main line. `git switch -c fix/sw2-debounce`, finish it, test it on the board, then merge it back — so the main line always stays in a state that builds and flashes.
- **A tag** pins a name to the commit that became a real, shipped firmware. Use an annotated tag: `git tag -a fw-v0.1.0 -m "..."`, then `git push origin fw-v0.1.0`. The SDK follows the same rule — its releases are named like `fw-c-only-v1.10.0`, with the hex and `SHA256SUMS.txt` attached to the release, not committed.
- **A commit message**'s first line says what was done; the body says **why**. A diff can tell you what changed, but never why. Six months later, whoever runs into an odd-looking line will want the reason more than anything else.

Compare two messages for the same change (a made-up example — the numbers are illustrative, not a real measurement):

```text
Unhelpful:      fix button

Helpful:        Debounce SW2 in time, not by reading the pin twice

                Two reads 200 ns apart sample the same bounce, so one press
                counted two or three times on the bench (10 presses -> 23).
                Require 3 agreeing polls at 10 ms, as the SDK's
                io/04_gpio_led_button.c does.
                Evidence: 10 presses -> 10 counts, board A, commit abc1234.
                Not verified: long presses over 5 s.
```

The SDK itself writes this kind of reasoning into code comments throughout every file we've read across module 1 — the same habit works for commit messages. A message template is in [examples/commit-template.txt](examples/commit-template.txt).

### 3. Secrets in history: deleting them later isn't enough

Git keeps **every version** of every file. If you commit a WiFi password once and remove it in the next commit, it's still there in the earlier commit. Anyone who already cloned or forked has a full copy, and their `git log -p` will show it. Rewriting history with a tool like `git filter-repo` and force-pushing only removes it from your own copy — not from anyone else's machine. So the first thing to do once a secret has leaked is **change the password or revoke that key.** Cleaning up history comes after, and only prevents it from leaking again.

The right approach is to never let a secret into the source in the first place. The SDK's WiFi example states this rule directly: "A credential compiled into an example is a credential in a public repository." ([10_wifi_join.c lines 71-84](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/connectivity/10_wifi_join.c#L71-L84)). That's why it reads the SSID and password from storage on the board, not from a `#define`. For values that need to live in a file during development, use a file that's ignored, and commit a sample file next to it holding only a placeholder, such as `"<your-password>"`.

Before pushing, search the whole history, not just the current files.

```sh
git grep -nIiE '(pass(word)?|secret|token|api_key)' $(git rev-list --all)   # every commit, every branch
git log -p --all -S 'PRIVATE KEY'                                         # commits that added or removed this text
```

The TESA Open Knowledge library you're reading right now checks every file the same way before publishing, with the `secrets` checker in `tools/validate.py`.

## Worked example

Setting up a repository for a project forked from the template. Do this inside your own `bento-firmware-template-mtb-only` folder.

**Part 1: start a clean repository**

```sh
git init
cp <this lesson's folder>/examples/firmware.gitignore .gitignore
git status --short --untracked-files=all | wc -l        # must be lower than before the .gitignore existed
git add .
git commit -m "Import bento-firmware-template-mtb-only from fw-c-only-v1.10.0"
```

**Part 2: work on a branch, then tag what ships**

```sh
git switch -c docs/build-record
mkdir -p docs && cp <the build record you filled in during lesson 2.1> docs/build-record.md
git add docs/build-record.md
git commit                                                # write the reasoning, following commit-template.txt
git switch main && git merge --no-ff docs/build-record
git tag -a fw-v0.1.0 -m "First build of the template on board A; record in docs/build-record.md"
git log --oneline --decorate --graph -5
```

(If your main line is called `master`, use that name instead of `main`.)

**Part 3: install the hook, then get it to reject something**

```sh
cp <this lesson's folder>/solution/pre-commit.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
printf '#define WIFI_PASSWORD "not-a-placeholder"\n' > wifi_secrets_test.h
git add -f wifi_secrets_test.h && git commit -m "test"    # must be rejected
git reset -q wifi_secrets_test.h && rm wifi_secrets_test.h
```

You should see a message like `blocked: looks like a real secret`. Then try changing the value to `"<your-password>"` and see whether the hook allows it this time. (We use `git add -f` because this filename is already excluded by `.gitignore` — which is exactly why we need this extra layer of hook.)

## Practice

Open [practice/pre-commit.sh](practice/pre-commit.sh). There are 4 gaps to fill in — more than in previous lessons, matching this module's pace.

1. Get the list of staged files.
2. Reject files under `build/`, `build-*/`, `mtb_shared/`, and `.o` files.
3. Reject newly added lines that assign a real-looking value to a secret-looking name, but allow placeholder values like `<...>` and empty values.
4. Reject the header line of a private key file.

Check your work with a test that creates a fresh, temporary repository for every case and deletes it itself, never touching your own repository.

```sh
bash examples/test_hook.sh practice/pre-commit.sh
```

Before filling anything in, you'll see `3 passed, 6 failed`. The three that pass are the cases the hook is supposed to "allow" — a hook that does nothing at all also passes those. If there were only those three tests, an empty hook would look like it's working. That's exactly why there also have to be cases the hook must "reject".

## Solution

Try it yourself for at least 15 minutes first, then open [solution/pre-commit.sh](solution/pre-commit.sh). Worth comparing:

- `--diff-filter=ACM` skips deleted files, and this command still works even on the very first commit, before `HEAD` exists.
- The pattern `"[^"<]` is the heart of telling a real value apart from a placeholder — a value starting with `<`, and an empty value, both pass.
- The hook prints the line where it found a secret, so a person can fix it, but never prints the contents of a private key, because logs can get copied and pasted elsewhere too.
- A hook like this can have false positives — for example, a variable named `TEST_PASSED`. Accept that limitation, and fix the name or the pattern when you hit one, rather than disabling the hook.

## Check your understanding

Answer the 5 questions in [quiz.yaml](quiz.yaml) (shown at the bottom of this page on the website), covering all three objectives. Getting 4 or more right counts as finishing the lesson.

## Lab

**Task:** bring a project forked from the template into Git, ready for a team to work on, with evidence that there are no build files and no secrets.

1. Do parts 1 through 3 until you have a first commit, one branch merged back, and the tag `fw-v0.1.0` on the commit you successfully built and flashed.
2. Build again with `make build -j`, then run `git status --short`. The result should be empty. If any file shows up, fix `.gitignore` and explain what that file is.
3. Run both history-search commands from concept 3. Note what you find. If you find a word like `password` in the template's source, check whether it's a real value or just a field name or a comment.
4. If you have a remote (such as a private GitHub repository), push both the branch and the tag, then check on the web page that the tag points to the right commit.

**Evidence to keep in your portfolio:** the output of `git log --oneline --decorate --graph` showing the merged branch and tag, the empty `git status --short` output after building, the message the hook used to reject your test commit, and the results of your history search with an explanation.

## Going further

- Read [Pro Git](https://git-scm.com/book/en/v2)'s "Git Branching" chapter and its "Tagging" section, then try setting a tag-naming rule for your team that states both the variant and the version, the way the SDK does.
- Try moving the hook's checks into CI too, where they can't be skipped with `--no-verify`. That's the subject of lesson 6.2.

Next lesson, moving into module 3: [lesson 3.1, an introduction to SWD and GDB](../../m03-debugging/l01-swd-and-gdb/README.md)

## Reflect

- If you discovered tomorrow that a cloud token had leaked into a commit three weeks ago, and five classmates had already cloned it, what would you do first, and why?
- Looking at your commit messages from the past week, how many of them would still make sense to you six months from now?

## References

- [Pro Git (the open Git book)](https://git-scm.com/book/en/v2)
- [SDK: the mtb-only template README (what getlibs fetches, and what you must supply yourself)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/README.en.md)
- [SDK: the repository's top-level .gitignore](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/.gitignore)
- [SDK: cm33/connectivity/10_wifi_join.c (credentials come from storage, not a #define)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/connectivity/10_wifi_join.c)
- [SDK: release fw-c-only-v1.10.0 (an example of a tag name, with a hex attached alongside SHA256SUMS)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/releases/tag/fw-c-only-v1.10.0)
