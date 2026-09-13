#!/usr/bin/env python3
"""Create the GitHub board (Projects v2) of the delivery method and file
every issue into it.

The seven statuses are those of the method, in its order:

    Backlog · Ready · In progress · En recette · In review · À déployer · Done

REQUIREMENT — the gh token must carry the `project` scope, which
`gh auth login` does not grant by default:

    gh auth refresh -s project --hostname github.com

Then:

    python3 scripts/setup_project.py
    python3 scripts/setup_project.py --dry-run

Idempotent: re-running reuses the board, adds only the missing issues and
never moves an item that already has a status. Moving items is the
agent's job, one `gh project item-edit` at a time — see docs/BOARD.md.

Two things the API does not expose, walked through by hand in
docs/BOARD.md: the board's built-in workflows (an issue closed by a merge
goes to `À déployer`) and the grouping of the Kanban view.
"""

import argparse
import json
import subprocess
import sys
import time

from kickoff_lib import repo, owner as repo_owner

OWNER = repo_owner()
REPO = repo()
TITLE = "{{PROJECT_NAME}} — livraison"

STATUSES = ["Backlog", "Ready", "In progress", "En recette", "In review",
            "À déployer", "Done"]
COLOURS = ["GRAY", "BLUE", "YELLOW", "ORANGE", "PURPLE", "PINK", "GREEN"]

# Created when missing, matched by name, never recreated.
VIEWS = [
    ("Kanban", "BOARD_LAYOUT", None),
    ("À revoir par Romain", "TABLE_LAYOUT", 'label:"à revoir par Romain"'),
    ("All items", "TABLE_LAYOUT", None),
]


def gh(args, check=True, retries=3):
    """Run `gh`, retrying GitHub's temporary Projects conflicts.

    Adding many items to a board in a row makes the API answer "your
    attempt to move this item created a temporary conflict" — a lock on
    the board, not a bad request, and it succeeds on the next try.
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


def find_project():
    listing = json.loads(gh(["project", "list", "--owner", OWNER,
                             "--format", "json"]).stdout)
    for project in listing.get("projects", []):
        if project["title"] == TITLE:
            return project
    return None


def create_project():
    created = json.loads(gh(["project", "create", "--owner", OWNER,
                             "--title", TITLE, "--format", "json"]).stdout)
    print(f"  board created: #{created['number']}")
    return created


def link_repository(number, dry_run):
    """Show the board in the repository's Projects tab. Harmless when the
    link already exists: gh then refuses, and the refusal is ignored."""
    if dry_run:
        print(f"  would link the board to {REPO}")
        return
    gh(["project", "link", str(number), "--owner", OWNER, "--repo", REPO],
       check=False)


def fields(number):
    listing = json.loads(gh(["project", "field-list", str(number),
                             "--owner", OWNER, "--format", "json"]).stdout)
    return {f["name"]: f for f in listing["fields"]}


def option_id(field, name):
    for option in field.get("options", []):
        if option["name"] == name:
            return option["id"]
    return None


def set_status_options(field, items_with_status, force, dry_run):
    """Replace the options of the built-in Status field by the method's.

    `gh project field-create` cannot touch Status: only the GraphQL
    mutation can. ⚠️ Replacing the options gives them new ids, so every
    item loses its status. On a board that already holds statuses the
    script therefore stops and says so, unless --force-statuses is given.

    Returns True when the options are the method's once it has run.
    """
    current = [option["name"] for option in field.get("options", [])]
    if current == STATUSES:
        print(f"  Status: {' · '.join(STATUSES)} (already in place)")
        return True

    if items_with_status and not force:
        print(f"  ⚠️  Status is {' · '.join(current)}, and "
              f"{len(items_with_status)} item(s) carry a value that a")
        print("      rewrite would erase. Nothing changed. Either add the "
              "missing options by hand")
        print("      (docs/BOARD.md), or re-run with --force-statuses and "
              "re-place every item.")
        return False

    if dry_run:
        print(f"  would set Status: {' · '.join(STATUSES)}")
        return True

    options = ", ".join(
        "{name: %s, color: %s, description: \"\"}"
        % (json.dumps(name, ensure_ascii=False), colour)
        for name, colour in zip(STATUSES, COLOURS))
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
        return True
    print("  ⚠️  Status options unchanged — set them by hand (docs/BOARD.md)")
    print(f"      {result.stderr.strip()}")
    return False


def ensure_views(project_id):
    """Create the missing views, and rename GitHub's lone default table."""
    q = ('query($p:ID!){node(id:$p){... on ProjectV2'
         '{views(first:20){nodes{id name layout}}}}}')
    existing = json.loads(gh(["api", "graphql", "-f", f"query={q}",
                              "-f", f"p={project_id}"]).stdout)
    by_name = {v["name"]: v for v in existing["data"]["node"]["views"]["nodes"]}

    # GitHub names the first view "View 1": it is All items under another
    # name, so it is renamed rather than left as a duplicate.
    if "View 1" in by_name and "All items" not in by_name:
        m = ('mutation($v:ID!,$n:String!){updateProjectV2View'
             '(input:{viewId:$v,name:$n}){projectV2View{id name}}}')
        gh(["api", "graphql", "-f", f"query={m}",
            "-f", f"v={by_name['View 1']['id']}", "-f", "n=All items"],
           check=False)
        by_name["All items"] = by_name.pop("View 1")

    for name, layout, view_filter in VIEWS:
        view = by_name.get(name)
        if not view:
            m = ('mutation($p:ID!,$n:String!,$l:ProjectV2ViewLayout!)'
                 '{createProjectV2View(input:{projectId:$p,name:$n,'
                 'layout:$l}){projectV2View{id name}}}')
            out = gh(["api", "graphql", "-f", f"query={m}",
                      "-f", f"p={project_id}", "-f", f"n={name}",
                      "-f", f"l={layout}"], check=False)
            if not out.stdout:
                continue
            view = json.loads(out.stdout)["data"]["createProjectV2View"]["projectV2View"]
            print(f"  view: {name}")

        if view_filter:
            m = ('mutation($v:ID!,$f:String!){updateProjectV2View'
                 '(input:{viewId:$v,filter:$f}){projectV2View{id}}}')
            gh(["api", "graphql", "-f", f"query={m}", "-f", f"v={view['id']}",
                "-f", f"f={view_filter}"], check=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force-statuses", action="store_true",
                        help="rewrite Status even if items already carry "
                             "one (they lose it)")
    args = parser.parse_args()

    check_scope()
    project = find_project()
    if not project:
        if args.dry_run:
            print(f"  would create the board « {TITLE} » with Status "
                  f"{' · '.join(STATUSES)}")
            print("\nDry run — nothing was written.")
            return
        project = create_project()
    number, project_id = project["number"], project["id"]

    link_repository(number, args.dry_run)

    items = json.loads(gh(["project", "item-list", str(number), "--owner",
                           OWNER, "--limit", "500", "--format",
                           "json"]).stdout)["items"]
    on_board = {i.get("content", {}).get("url") for i in items}
    with_status = [i for i in items if i.get("status")]

    status_ok = set_status_options(fields(number)["Status"], with_status,
                                   args.force_statuses, args.dry_run)
    status_field = fields(number)["Status"]

    issues = json.loads(gh(["issue", "list", "--repo", REPO, "--state", "all",
                            "--limit", "500", "--json",
                            "title,url,state"]).stdout)
    for issue in issues:
        if issue["url"] in on_board:
            continue
        # A new item starts in Backlog; an issue closed before the board
        # existed is history, and lands in Done. Nothing else is decided
        # here: where a story stands is set by whoever works on it.
        wanted = "Done" if issue["state"] == "CLOSED" else "Backlog"
        if args.dry_run:
            print(f"  would add: {issue['title']} → {wanted}")
            continue
        added = json.loads(gh(["project", "item-add", str(number), "--owner",
                               OWNER, "--url", issue["url"], "--format",
                               "json"]).stdout)
        oid = option_id(status_field, wanted) if status_ok else None
        if oid:
            gh(["project", "item-edit", "--id", added["id"], "--project-id",
                project_id, "--field-id", status_field["id"],
                "--single-select-option-id", oid], check=False)
        print(f"  added: {issue['title']} → {wanted if oid else 'no status'}")

    if args.dry_run:
        print("\nDry run — nothing was written.")
        return

    ensure_views(project_id)

    print(f"\nboard ready: {project.get('url', f'#{number}')}")
    print("Left by hand, once (docs/BOARD.md): the built-in workflows — "
          "« Item closed » and « Pull request merged » set À déployer — "
          "and the Kanban grouped by Status.")


if __name__ == "__main__":
    main()
