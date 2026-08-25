#!/usr/bin/env python3
"""Create the labels, milestones and 95 backlog issues on GitHub.

Idempotent, and it UPDATES: a user story already present (title starting
with its identifier) is not recreated — its body and its labels are
brought back in line with the specification when they have drifted.

That is what makes the promise in README.md true. "Change the criterion
in the specification, then re-run the scripts" is worth nothing if the
re-run skips every issue that already exists: the document and the board
disagree, and the board is what people read.

    python3 scripts/build_backlog.py && python3 scripts/create_issues.py
    python3 scripts/create_issues.py --dry-run

Requires gh authenticated on the account owning the repository.
"""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKLOG = ROOT / "scripts" / "backlog.json"
from kickoff_lib import repo

REPO = repo()

# Palette: warm for what is urgent, neutral for the rest.
EMBER, EMBER_LO, INK, INK_3 = "FF8A3D", "A8410A", "C9C0B4", "6E665B"

def batches(backlog):
    """{batch: title} taken from the specification, in order."""
    found = {}
    for story in backlog:
        if story.get("batch"):
            found.setdefault(story["batch"], story["batch_title"])
    return dict(sorted(found.items()))


def run(args, check=True):
    return subprocess.run(args, capture_output=True, text=True, check=check)


def ensure_label(name, color, description, dry_run):
    if dry_run:
        print(f"  label {name}")
        return
    run(["gh", "label", "create", name, "--repo", REPO, "--color", color,
         "--description", description[:100], "--force"])


def ensure_milestone(title, description, dry_run):
    if dry_run:
        print(f"  milestone {title}")
        return
    existing = json.loads(run(
        ["gh", "api", f"repos/{REPO}/milestones?state=all", "--jq", "[.[].title]"]
    ).stdout)
    if title in existing:
        return
    run(["gh", "api", f"repos/{REPO}/milestones", "-f", f"title={title}",
         "-f", f"description={description}"])


# The Definition of Done, copied into every story so it is ticked there.
# Reference: DOR_DOD.md. A change to one is a change to both — and to
# .github/ISSUE_TEMPLATE/user_story.md, which carries the same list for
# stories opened by hand.
DEFINITION_OF_DONE = """**The story does what it promised**

- [ ] Every acceptance criterion above is checked, one by one
- [ ] CI is green
- [ ] It respects the golden rules — no hard-coded value, business logic in the right layer, no string outside the translation layer
- [ ] `routes` lists exactly the paths the story needed, no more, and every view uses the named helper rather than a string path
- [ ] Its error and empty states exist and lead somewhere
- [ ] Accessibility holds: touch targets, contrast, no information carried by colour alone
- [ ] The journey is walked **on the real target device** *and* **against the deployed environment** — not only in a desktop browser, not only on localhost
- [ ] Nothing is left from writing it: no debugger breakpoint, no console log, no commented-out attempt, no dead code the story replaced
- [ ] The **verification pass** was asked for and done: every acceptance criterion walked through in the running app — plus a security review if the story touched auth, input, uploads, money or a third-party call

**What the story leaves behind** — in the same commit as the code, never in a pass at the end

- [ ] The success criterion is instrumented — whatever it is read from exists and produces a number
- [ ] Every decision taken along the way is written **with its reason**, in `docs/decisions/`
- [ ] Every trap paid is written in `AGENTS.md`, where the next person will hit it
- [ ] `docs/SCHEMA.md` and `docs/ARCHITECTURE.md` say what the code now does, if the story moved the structure
- [ ] `docs/SCENARIOS.md` covers what the story added, each scenario naming the test that verifies it
- [ ] `README.md`, `AGENTS.md` and `.env.example` are updated if a command, a variable or a URL changed — and no key is in the code"""


def body_for(story):
    batch = story.get("batch")
    meta = [
        f"**Epic** {story['epic']} — {story['epic_title']}",
        f"**Priority** {story['priority']}",
        f"**Complexity** {story['points']} pts ({story['nature']})",
        f"**Batch** {batch} — {story['batch_title']}" if batch
        else "**Batch** out of bootcamp scope",
    ]
    criteria = "\n".join(f"- [ ] {c}" for c in story["criteria"])

    return f"""> {" · ".join(meta)}

### User story

{story["story"]}

### Acceptance criteria

{criteria}

### Success criterion

{story["success"]}

### Definition of Done

Merged is not done. The reference is `DOR_DOD.md`; this copy is here so
it gets ticked on the story itself.

{DEFINITION_OF_DONE}

---

<sub>Quoted verbatim from the reference specification
`docs/specification.md`, section {story["epic"]}. An acceptance or
success criterion is never translated nor reworded: if it must change, it
changes in the specification first.</sub>
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--only", help="identifier prefix, e.g. US-1")
    args = parser.parse_args()

    backlog = json.loads(BACKLOG.read_text(encoding="utf-8"))
    batch_titles = batches(backlog)

    print("Labels")
    epics = {s["epic"]: s["epic_title"] for s in backlog}
    for epic, title in sorted(epics.items(), key=lambda kv: int(kv[0][1:])):
        ensure_label(f"epic:{epic}", INK_3, title, args.dry_run)
    for prio, color in (("P1", EMBER), ("P2", EMBER_LO), ("P3", INK_3)):
        ensure_label(f"prio:{prio}", color,
                     {"P1": "Core journey and bootcamp scope",
                      "P2": "Personalisation",
                      "P3": "Vision, not committed"}[prio], args.dry_run)
    for batch, title in batch_titles.items():
        ensure_label(f"batch:{batch}", INK, f"{batch} — {title}", args.dry_run)
    out_of_scope = sum(1 for s in backlog if not s.get("batch"))
    ensure_label("batch:out-of-scope", INK_3,
                 f"Out of the committed scope: {out_of_scope} stories",
                 args.dry_run)
    for points in (1, 2, 3, 4, 5, 8, 13):
        ensure_label(f"pts:{points}", INK_3,
                     f"Relative complexity {points}", args.dry_run)

    print("Milestones")
    for batch, title in batch_titles.items():
        points = sum(s["points"] for s in backlog if s.get("batch") == batch)
        stories = sum(1 for s in backlog if s.get("batch") == batch)
        ensure_milestone(f"{batch} — {title}",
                         f"{stories} stories, {points} points.", args.dry_run)

    print("Issues")
    # Read the existing issues even on a dry run: reading changes nothing,
    # and a preview that cannot tell you what it would UPDATE is a preview
    # of half the work.
    existing = {}
    issues = json.loads(run(
        ["gh", "issue", "list", "--repo", REPO, "--state", "all",
         "--limit", "500", "--json", "number,title,body,labels"]
    ).stdout)
    for issue in issues:
        key = issue["title"].split(" ")[0]
        existing[key] = {
            "number": issue["number"],
            "title": issue["title"],
            "body": issue["body"] or "",
            "labels": {label["name"] for label in issue["labels"]},
        }

    created = updated = unchanged = 0
    for story in backlog:
        if args.only and not story["id"].startswith(args.only):
            continue
        title = f"{story['id']} — {story['feature']}"
        labels = [f"epic:{story['epic']}", f"prio:{story['priority']}",
                  f"pts:{story['points']}"]
        labels.append(f"batch:{story['batch']}" if story.get("batch")
                      else "batch:out-of-scope")

        known = existing.get(story["id"])
        if known:
            # Only the labels this script owns are compared. A label a
            # human added by hand — `blocked`, `needs-design` — is theirs,
            # and re-running must not wipe it.
            ours = {l for l in known["labels"]
                    if l.split(":")[0] in ("epic", "prio", "pts", "batch")}
            wanted_body = body_for(story)
            drifted = [
                name for name, same in (
                    ("title", known["title"] == title),
                    ("body", known["body"].strip() == wanted_body.strip()),
                    ("labels", ours == set(labels)),
                ) if not same
            ]
            if not drifted:
                unchanged += 1
                continue

            print(f"  {title} — {', '.join(drifted)} out of date")
            if args.dry_run:
                updated += 1
                continue

            cmd = ["gh", "issue", "edit", str(known["number"]),
                   "--repo", REPO, "--title", title, "--body", wanted_body]
            for label in labels:
                cmd += ["--add-label", label]
            for stale in ours - set(labels):
                cmd += ["--remove-label", stale]
            result = run(cmd, check=False)
            if result.returncode != 0:
                print(f"  FAILED {title}: {result.stderr.strip()}",
                      file=sys.stderr)
                continue
            updated += 1
            time.sleep(0.7)
            continue

        cmd = ["gh", "issue", "create", "--repo", REPO, "--title", title,
               "--body", body_for(story)]
        for label in labels:
            cmd += ["--label", label]
        if story.get("batch"):
            cmd += ["--milestone",
                    f'{story["batch"]} — {batch_titles[story["batch"]]}']

        if args.dry_run:
            print(f"  {title}  [{', '.join(labels)}]")
            created += 1
            continue

        result = run(cmd, check=False)
        if result.returncode != 0:
            print(f"  FAILED {title}: {result.stderr.strip()}", file=sys.stderr)
            continue
        created += 1
        print(f"  {title} → {result.stdout.strip()}")
        time.sleep(0.7)   # GitHub secondary rate limit on content creation

    print(f"\n{created} issues created, {updated} updated, "
          f"{unchanged} already in line with the specification.")


if __name__ == "__main__":
    main()
