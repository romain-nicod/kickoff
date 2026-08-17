#!/usr/bin/env python3
"""Extract the backlog from the reference specification.

Single source: docs/specification.md. The script rewrites
nothing, it reads the tables and produces scripts/backlog.json, consumed
by create_issues.py. Re-run it after any change to the specification
rather than editing an issue by hand.

    python3 scripts/build_backlog.py
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "docs" / "specification.md"
OUT = ROOT / "scripts" / "backlog.json"

spec = SPEC.read_text(encoding="utf-8")

# ---------------------------------------------------------------- epics
# "## E1 — Discovery and decision"
epics = {}
for match in re.finditer(r"^## (E\d+) — (.+)$", spec, re.M):
    epics[match.group(1)] = match.group(2).strip()

# ------------------------------------------------------- user stories
# | **US-101** | Proposal on launch | As a ... | 1. ...<br>2. ... | P1 |
stories = {}
current_epic = None
for line in spec.splitlines():
    heading = re.match(r"^## (E\d+) — ", line)
    if heading:
        current_epic = heading.group(1)
        continue
    if line.startswith("## Business rules"):
        current_epic = None

    row = re.match(
        r"^\| \*\*(US-\d+)\*\* \| (.+?) \| (.+?) \| (.+?) \| (P\d) \|$", line
    )
    if row and current_epic:
        story_id, feature, story, criteria, priority = row.groups()
        stories[story_id] = {
            "id": story_id,
            "epic": current_epic,
            "epic_title": epics[current_epic],
            "feature": feature.strip(),
            "story": story.strip(),
            "criteria": [c.strip() for c in criteria.split("<br>") if c.strip()],
            "priority": priority,
        }

# --------------------------------------------------------- complexity
# | US-101 | Proposal on launch | **5** | JS · RAILS · SQL | P1 |
for line in spec.splitlines():
    row = re.match(
        r"^\| (US-\d+) \| (.+?) \| \*\*(\d+)\*\* \| (.+?) \| (P\d) \|$", line
    )
    if row:
        story_id, _, points, nature, _ = row.groups()
        if story_id in stories:
            stories[story_id]["points"] = int(points)
            stories[story_id]["nature"] = nature.strip()

# ------------------------------------------------------------ batches
# "**B1 — The demo that works** — 36 points" then "| US-106 | ... | 2 |"
current_batch = None
for line in spec.splitlines():
    batch = re.match(r"^\*\*(B\d) — (.+?)\*\* — \d+ points$", line)
    if batch:
        current_batch = (batch.group(1), batch.group(2))
        continue
    row = re.match(r"^\| (US-\d+) \| (.+?) \| (\d+) \|$", line)
    if row and current_batch:
        story_id = row.group(1)
        if story_id in stories:
            stories[story_id]["batch"] = current_batch[0]
            stories[story_id]["batch_title"] = current_batch[1]

backlog = sorted(stories.values(), key=lambda s: (int(s["epic"][1:]), s["id"]))

missing = [s["id"] for s in backlog if "points" not in s]
if missing:
    raise SystemExit(f"No complexity found for: {', '.join(missing)}")

OUT.write_text(json.dumps(backlog, ensure_ascii=False, indent=2), encoding="utf-8")

batched = sum(1 for s in backlog if "batch" in s)
total = sum(s["points"] for s in backlog)
print(f"{len(backlog)} user stories · {total} points · {batched} batched · "
      f"{len(epics)} epics")
