#!/usr/bin/env python3
"""Create the GitHub board (Projects v2) and file every issue into it.

Beyond the built-in Status, the board carries three fields: delivery
batch, complexity in points and priority. That is what answers, at a
glance, the only question that matters at the end of week one: how many
points were actually delivered.

REQUIREMENT — the gh token must carry the `project` scope, which
`gh auth login` does not grant by default:

    gh auth refresh -s project --hostname github.com

Then:

    python3 scripts/setup_project.py

Idempotent: re-running reuses the existing board, adds only missing
issues, and refreshes every field value.
"""

import json
import subprocess
import sys

from kickoff_lib import repo, owner as repo_owner

OWNER = repo_owner()
REPO = repo()
TITLE = "{{PROJECT_NAME}} — delivery"

BATCHES = ["B0", "B1", "B2", "B3", "B4", "B5", "out of scope"]
PRIORITIES = ["P1", "P2", "P3"]


def gh(args, check=True):
    result = subprocess.run(["gh"] + args, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"failed: gh {' '.join(args)}\n{result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result


def check_scope():
    result = gh(["project", "list", "--owner", OWNER, "--format", "json"],
                check=False)
    if result.returncode != 0:
        sys.exit("The gh token is missing the project scope.\n"
                 "Run: gh auth refresh -s project --hostname github.com")


def find_or_create_project():
    listing = json.loads(gh(["project", "list", "--owner", OWNER,
                             "--format", "json"]).stdout)
    for project in listing.get("projects", []):
        if project["title"] == TITLE:
            return project["number"], project["id"]

    created = json.loads(gh(["project", "create", "--owner", OWNER,
                             "--title", TITLE, "--format", "json"]).stdout)
    print(f"board created: #{created['number']} — {created['url']}")
    return created["number"], created["id"]


def fields(number):
    listing = json.loads(gh(["project", "field-list", str(number),
                             "--owner", OWNER, "--format", "json"]).stdout)
    return {f["name"]: f for f in listing["fields"]}


def ensure_fields(number):
    existing = fields(number)

    # Earlier French field names, dropped so the board reads in one language.
    for stale in ("Lot", "Priorité"):
        if stale in existing:
            gh(["project", "field-delete", "--id", existing[stale]["id"]])
            print(f"  dropped stale field {stale}")

    existing = fields(number)
    if "Batch" not in existing:
        gh(["project", "field-create", str(number), "--owner", OWNER,
            "--name", "Batch", "--data-type", "SINGLE_SELECT",
            "--single-select-options", ",".join(BATCHES)])
    if "Points" not in existing:
        gh(["project", "field-create", str(number), "--owner", OWNER,
            "--name", "Points", "--data-type", "NUMBER"])
    if "Priority" not in existing:
        gh(["project", "field-create", str(number), "--owner", OWNER,
            "--name", "Priority", "--data-type", "SINGLE_SELECT",
            "--single-select-options", ",".join(PRIORITIES)])

    return fields(number)


def option_id(field, name):
    for option in field.get("options", []):
        if option["name"] == name:
            return option["id"]
    return None


def main():
    check_scope()
    number, project_id = find_or_create_project()
    field_map = ensure_fields(number)

    issues = json.loads(gh(["issue", "list", "--repo", REPO, "--state", "all",
                            "--limit", "500", "--json",
                            "number,title,url,labels,state"]).stdout)

    items = json.loads(gh(["project", "item-list", str(number), "--owner", OWNER,
                           "--limit", "500", "--format", "json"]).stdout)
    known = {i.get("content", {}).get("url"): i["id"] for i in items["items"]}

    for issue in issues:
        labels = [label["name"] for label in issue["labels"]]
        item_id = known.get(issue["url"])

        if not item_id:
            added = json.loads(gh(["project", "item-add", str(number),
                                   "--owner", OWNER, "--url", issue["url"],
                                   "--format", "json"]).stdout)
            item_id = added["id"]
            print(f"  added: {issue['title']}")

        batch = next((l.split(":")[1] for l in labels if l.startswith("batch:")), None)
        if batch == "out-of-scope":
            batch = "out of scope"
        priority = next((l.split(":")[1] for l in labels if l.startswith("prio:")), None)
        points = next((l.split(":")[1] for l in labels if l.startswith("pts:")), None)
        # A closed issue is delivered; everything else waits in Todo, so the
        # board never shows a column-less pile on first open.
        status = "Done" if issue["state"] == "CLOSED" else "Todo"

        base = ["project", "item-edit", "--id", item_id, "--project-id", project_id]
        for field_name, value in (("Batch", batch), ("Priority", priority),
                                  ("Status", status)):
            oid = option_id(field_map[field_name], value) if value else None
            if oid:
                gh(base + ["--field-id", field_map[field_name]["id"],
                           "--single-select-option-id", oid], check=False)
        if points:
            gh(base + ["--field-id", field_map["Points"]["id"],
                       "--number", points], check=False)

    print(f"\nboard ready: https://github.com/users/{OWNER}/projects/{number}")
    print("Add a Board view in the UI (+ next to the view tabs → Board, "
          "group by Status): creating a view is not exposed by the API.")


if __name__ == "__main__":
    main()
