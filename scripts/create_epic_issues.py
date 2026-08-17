#!/usr/bin/env python3
"""Create the 14 epic issues and attach every user story as a sub-issue.

The label `epic:Enn` makes stories filterable; a sub-issue link makes the
hierarchy real — GitHub then shows the completion of each epic on the
board, and an epic can be read as one thing rather than as a filter.

    python3 scripts/build_backlog.py && python3 scripts/create_epic_issues.py

Idempotent: an epic already present is reused, and a story already
attached is not attached twice.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKLOG = ROOT / "scripts" / "backlog.json"
SPEC = ROOT / "docs" / "specification.md"
from kickoff_lib import repo

REPO = repo()


def gh(args, check=True):
    result = subprocess.run(["gh"] + args, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"failed: gh {' '.join(args)}\n{result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result


def capabilities():
    """The '> **Capability**: …' line under each epic heading."""
    spec = SPEC.read_text(encoding="utf-8")
    found = {}
    for match in re.finditer(
        r"^## (E\d+) — .+?\n\n> \*\*Capability\*\*: (.+?)\.?$", spec, re.M
    ):
        found[match.group(1)] = match.group(2).strip()
    return found


def body_for(epic, title, capability, stories):
    points = sum(s["points"] for s in stories)
    by_priority = {p: [s for s in stories if s["priority"] == p]
                   for p in ("P1", "P2", "P3")}
    batched = [s for s in stories if s.get("batch")]

    lines = [
        f"> **Capability** — {capability}.",
        "",
        f"**{len(stories)} stories · {points} points** · "
        + " · ".join(f"{p} {len(v)}" for p, v in by_priority.items() if v),
        "",
        "### Stories",
        "",
        "| Story | Points | Priority | Batch |",
        "|---|---|---|---|",
    ]
    for story in stories:
        batch = story.get("batch") or "out of scope"
        lines.append(
            f"| {story['id']} — {story['feature']} | {story['points']} | "
            f"{story['priority']} | {batch} |"
        )

    lines += [
        "",
        f"{len(batched)} of them are in the committed batches (B0–B5); the "
        "rest sit outside the bootcamp scope.",
        "",
        "---",
        "",
        "<sub>Generated from the reference specification "
        f"`docs/specification.md`, section {epic}. This issue is a "
        "container: it is closed when every sub-issue is closed, and it is "
        "never worked on directly.</sub>",
    ]
    return "\n".join(lines)


def main():
    backlog = json.loads(BACKLOG.read_text(encoding="utf-8"))
    caps = capabilities()

    issues = json.loads(gh(["issue", "list", "--repo", REPO, "--state", "all",
                            "--limit", "500", "--json",
                            "number,title,id"]).stdout)
    # The sub-issue API wants the REST database id, not the issue number.
    rest_ids = {}
    for issue in issues:
        data = json.loads(gh(["api", f"repos/{REPO}/issues/{issue['number']}",
                              "--jq", "{id: .id, title: .title}"]).stdout)
        rest_ids[data["title"]] = (issue["number"], data["id"])

    epics = {}
    for story in backlog:
        epics.setdefault(story["epic"], {"title": story["epic_title"],
                                         "stories": []})
        epics[story["epic"]]["stories"].append(story)

    for epic in sorted(epics, key=lambda e: int(e[1:])):
        title = f"{epic} — {epics[epic]['title']}"
        stories = epics[epic]["stories"]

        if title in rest_ids:
            number, _ = rest_ids[title]
            print(f"{title}: already present (#{number})")
        else:
            url = gh(["issue", "create", "--repo", REPO, "--title", title,
                      "--body", body_for(epic, title, caps.get(epic, ""), stories),
                      "--label", f"epic:{epic}"]).stdout.strip()
            number = int(url.rstrip("/").split("/")[-1])
            print(f"{title}: created #{number}")

        attached = json.loads(gh(
            ["api", f"repos/{REPO}/issues/{number}/sub_issues",
             "--jq", "[.[].title]"]).stdout)

        for story in stories:
            story_title = f"{story['id']} — {story['feature']}"
            if story_title in attached:
                continue
            if story_title not in rest_ids:
                print(f"  missing issue for {story_title}", file=sys.stderr)
                continue
            _, rest_id = rest_ids[story_title]
            result = gh(["api", "-X", "POST",
                         f"repos/{REPO}/issues/{number}/sub_issues",
                         "-F", f"sub_issue_id={rest_id}"], check=False)
            if result.returncode != 0:
                print(f"  failed on {story_title}: {result.stderr.strip()[:120]}",
                      file=sys.stderr)
            else:
                print(f"  attached {story_title}")


if __name__ == "__main__":
    main()
