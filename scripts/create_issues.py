#!/usr/bin/env python3
"""Create the labels, milestones and 95 backlog issues on GitHub.

Idempotent: a user story already present (title starting with its
identifier) is not recreated, so re-running after a specification update
produces no duplicate.

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

---

<sub>Quoted verbatim from the reference specification
`docs/specification.md`, section {story["epic"]}. An acceptance
criterion is never translated nor reworded: if it must change, it changes
in the specification first.</sub>
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
    existing = set()
    if not args.dry_run:
        titles = json.loads(run(
            ["gh", "issue", "list", "--repo", REPO, "--state", "all",
             "--limit", "500", "--json", "title"]
        ).stdout)
        existing = {t["title"].split(" ")[0] for t in titles}

    created = skipped = 0
    for story in backlog:
        if args.only and not story["id"].startswith(args.only):
            continue
        if story["id"] in existing:
            skipped += 1
            continue

        title = f"{story['id']} — {story['feature']}"
        labels = [f"epic:{story['epic']}", f"prio:{story['priority']}",
                  f"pts:{story['points']}"]
        labels.append(f"batch:{story['batch']}" if story.get("batch")
                      else "batch:out-of-scope")

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

    print(f"\n{created} issues created, {skipped} already present.")


if __name__ == "__main__":
    main()
