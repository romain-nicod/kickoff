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
import time

from kickoff_lib import repo, owner as repo_owner

OWNER = repo_owner()
REPO = repo()
TITLE = "{{PROJECT_NAME}} — delivery"

BATCHES = ["B0", "B1", "B2", "B3", "B4", "B5", "out of scope"]

# The five columns of Le Wagon's project template, rather than GitHub's
# default three. `Ready` and `In review` are the two that earn their place:
# without `Ready` there is nowhere to put a story that met the Definition
# of Ready but has not started, and without `In review` a pull request
# waiting on a reviewer looks exactly like work in progress.
STATUSES = ["Backlog", "Ready", "In progress", "In review", "Done"]

# Prioritisation in MoSCoW, as Le Wagon's template reads it. It is derived
# from the specification's own P1/P2/P3 — the document does not change, the
# board speaks the shared language.
MOSCOW = ["Must Have", "Should Have", "Can Have", "Won't Have"]
MOSCOW_OF = {"P1": "Must Have", "P2": "Should Have", "P3": "Can Have"}


def gh(args, check=True, retries=3):
    """Run `gh`, retrying GitHub's temporary Projects conflicts.

    Adding many items to a board in a row makes the API answer "your
    attempt to move this item created a temporary conflict" — it is a lock
    on the board, not a bad request, and it succeeds on the next try. A
    hundred issues added one by one hits it several times, so the retry is
    not an optimisation: without it the board is silently incomplete.
    """
    for attempt in range(retries):
        result = subprocess.run(["gh"] + args, capture_output=True, text=True)
        if result.returncode == 0:
            return result
        if "temporary conflict" not in result.stderr:
            break
        time.sleep(1 + attempt)

    if check:
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


def set_status_options(project_id, field):
    """Rewrite the built-in Status field's options.

    `gh project field-create` cannot touch Status: GitHub creates it with
    the project and only the GraphQL mutation can change its options.
    Idempotent — it is skipped when the five are already in place.
    """
    current = [o["name"] for o in field.get("options", [])]
    if current == STATUSES:
        return

    options = ", ".join(
        '{name: "%s", color: %s, description: ""}' % (name, colour)
        for name, colour in zip(STATUSES,
                                ["GRAY", "BLUE", "YELLOW", "PURPLE", "GREEN"])
    )
    query = """
    mutation {
      updateProjectV2Field(input: {
        fieldId: "%s"
        singleSelectOptions: [%s]
      }) { projectV2Field { ... on ProjectV2SingleSelectField { id } } }
    }""" % (field["id"], options)

    result = gh(["api", "graphql", "-f", f"query={query}"], check=False)
    if result.returncode == 0:
        print(f"  Status: {' · '.join(STATUSES)}")
    else:
        print("  ⚠️  Status options unchanged — the token may lack the "
              "project scope on this owner")
        print(f"      {result.stderr.strip()}")


def fields(number):
    listing = json.loads(gh(["project", "field-list", str(number),
                             "--owner", OWNER, "--format", "json"]).stdout)
    return {f["name"]: f for f in listing["fields"]}


def ensure_fields(number, project_id):
    existing = fields(number)

    # Earlier French field names, dropped so the board reads in one language.
    for stale in ("Lot", "Priorité"):
        if stale in existing:
            gh(["project", "field-delete", "--id", existing[stale]["id"]])
            print(f"  dropped stale field {stale}")

    existing = fields(number)
    if "Status" in existing:
        set_status_options(project_id, existing["Status"])

    if "MoSCoW Priority" not in existing:
        gh(["project", "field-create", str(number), "--owner", OWNER,
            "--name", "MoSCoW Priority", "--data-type", "SINGLE_SELECT",
            "--single-select-options", ",".join(MOSCOW)])
    if "Route" not in existing:
        # The Rails route a story is reached by. Empty until the story is
        # started — routes are written before the code, so this is the
        # first thing filled in and the fastest way to spot two stories
        # that are really one.
        gh(["project", "field-create", str(number), "--owner", OWNER,
            "--name", "Route", "--data-type", "TEXT"])

    # The P1/P2/P3 field is superseded by MoSCoW: two priority columns on
    # one board is two answers to one question. The `prio:` label stays on
    # the issue, and stays the source.
    if "Priority" in existing:
        gh(["project", "field-delete", "--id", existing["Priority"]["id"]],
           check=False)
        print("  dropped Priority — superseded by MoSCoW Priority")

    if "Batch" not in existing:
        gh(["project", "field-create", str(number), "--owner", OWNER,
            "--name", "Batch", "--data-type", "SINGLE_SELECT",
            "--single-select-options", ",".join(BATCHES)])
    if "Points" not in existing:
        gh(["project", "field-create", str(number), "--owner", OWNER,
            "--name", "Points", "--data-type", "NUMBER"])
    return fields(number)


def option_id(field, name):
    for option in field.get("options", []):
        if option["name"] == name:
            return option["id"]
    return None


def main():
    check_scope()
    number, project_id = find_or_create_project()
    field_map = ensure_fields(number, project_id)

    issues = json.loads(gh(["issue", "list", "--repo", REPO, "--state", "all",
                            "--limit", "500", "--json",
                            "number,title,url,labels,state"]).stdout)

    items = json.loads(gh(["project", "item-list", str(number), "--owner", OWNER,
                           "--limit", "500", "--format", "json"]).stdout)
    known = {i.get("content", {}).get("url"): i["id"] for i in items["items"]}
    # Where each story already stands. Re-running the script must never drag
    # work backwards: a story someone moved to "In progress" stays there.
    current_status = {i.get("content", {}).get("url"): i.get("status")
                      for i in items["items"]}

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
        # A closed issue is delivered; everything else waits in Backlog, so
        # the board never shows a column-less pile on first open. Nothing is
        # ever moved OUT of Backlog by this script: where a story stands is
        # the team's answer, not the generator's, and re-running must never
        # drag work back.
        status = "Done" if issue["state"] == "CLOSED" else (
            None if current_status.get(issue["url"]) else "Backlog"
        )

        # A story outside every batch is out of the committed scope, which
        # is exactly what "Won't Have" says.
        moscow = MOSCOW_OF.get(priority) if batch else "Won't Have"

        base = ["project", "item-edit", "--id", item_id, "--project-id", project_id]
        for field_name, value in (("Batch", batch), ("MoSCoW Priority", moscow),
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
