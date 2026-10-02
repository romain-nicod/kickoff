#!/usr/bin/env python3
"""Create the GitHub board (Projects v2) described by .github/board.json
and file every issue into it.

The board is DESCRIBED in one place and APPLIED here. Adding a view or a
field is an edit to `.github/board.json`, never to this script.

The seven statuses are those of the method, in its order:

    Backlog · Ready · In progress · En recette · In review · À déployer · Done

REQUIREMENT — the gh token must carry the `project` scope, which
`gh auth login` does not grant by default:

    gh auth refresh -s project --hostname github.com

Then:

    python3 scripts/setup_project.py
    python3 scripts/setup_project.py --dry-run

The board itself is found by its LINK to the repository, not by its
title: the titles in service predate this template. Failing that, by
title; failing that, it is created. `--project N` names it outright.

Idempotent, and never destructive: re-running reuses the board, creates
only the fields and views that are missing, adds only the issues that are
absent, and never moves an item that already has a status. Nothing is
ever deleted or renamed — a field and a view are matched BY NAME, so
renaming one in board.json creates a second one next to the first.

The one exception is the built-in Status field, whose options must be
REPLACED to become the method's. That gives them new ids and every item
loses its status, so the script refuses on a board that already holds
statuses unless --force-statuses is given.

THREE THINGS THE API DOES NOT EXPOSE, walked through by hand in
docs/BOARD.md: the board's built-in workflows, the grouping and the
sorting of a view, and the two date fields of the Roadmap layout.
A board view created here IS already grouped by Status — that one is not
manual, contrary to what this script said before it was measured.
"""

import argparse
import json
import subprocess
import sys
import time
from datetime import date, timedelta
from pathlib import Path

from kickoff_lib import repo, owner as repo_owner

ROOT = Path(__file__).resolve().parent.parent
BOARD = ROOT / ".github" / "board.json"

OWNER = repo_owner()
REPO = repo()

WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday",
            "saturday", "sunday"]

# Set on a view by `configuration: {visibleFieldIds: […]}`, the only part
# of a view's configuration the API accepts. It applies the SET of
# columns, not their order: GitHub re-sorts them its own way.
VIEW_FEATURES = "GraphQL-Features: projects_v2_views"


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


def graphql(query, check=True, **variables):
    args = ["api", "graphql", "-H", VIEW_FEATURES, "-f", f"query={query}"]
    for name, value in variables.items():
        args += ["-f", f"{name}={value}"]
    result = gh(args, check=check)
    if result.returncode != 0 or not result.stdout:
        return None
    return json.loads(result.stdout).get("data")


def read_board():
    if not BOARD.exists():
        sys.exit(f"{BOARD.relative_to(ROOT)} is missing")
    spec = json.loads(BOARD.read_text(encoding="utf-8"))
    readme = spec.get("readme_file")
    if readme:
        path = ROOT / readme
        spec["readme"] = path.read_text(encoding="utf-8") if path.exists() else None
    return spec


def check_scope():
    result = gh(["project", "list", "--owner", OWNER, "--format", "json"],
                check=False)
    if result.returncode != 0:
        sys.exit("The gh token is missing the project scope.\n"
                 "Run: gh auth refresh -s project --hostname github.com")


def find_project_by_repository():
    """The board already linked to this repository, if there is exactly one.

    Matching by title does not survive a second project. The template's
    title carries `{{PROJECT_NAME}}` until `bin/kickoff` substitutes it,
    and the boards created before this script existed were named by
    hand — « Mac Studio — delivery » next to « Engineering Portfolio —
    livraison ». Run against them, a match by title would create a
    second board beside the real one, silently.

    The link between a board and its repository is a fact GitHub holds:
    a board on the repository's Projects tab IS this project's board,
    whatever it is called. Two linked boards is a question only a human
    can answer, so the script stops and asks for --project.
    """
    owner, name = REPO.split("/", 1)
    query = """
      query($owner: String!, $name: String!) {
        repository(owner: $owner, name: $name) {
          projectsV2(first: 20) {
            nodes { id number title url closed }
          }
        }
      }
    """
    result = gh(["api", "graphql", "-f", "query=" + query,
                 "-f", "owner=" + owner, "-f", "name=" + name], check=False)
    if result.returncode != 0:
        return None
    repository = (json.loads(result.stdout).get("data") or {}).get("repository")
    if not repository:
        return None
    boards = [node for node in (repository.get("projectsV2") or {}).get("nodes", [])
              if not node.get("closed")]
    if len(boards) > 1:
        sys.exit("several boards are linked to " + REPO + ":\n"
                 + "\n".join("  #%s  %s" % (b["number"], b["title"])
                              for b in boards)
                 + "\nPass --project <number> to say which one to apply to.")
    return boards[0] if boards else None


def find_project_by_number(number):
    """The board the operator named. It must exist — a typo here would
    otherwise fall through to a creation nobody asked for."""
    result = gh(["project", "view", str(number), "--owner", OWNER,
                 "--format", "json"], check=False)
    if result.returncode != 0:
        sys.exit("no board #%s under %s" % (number, OWNER))
    return json.loads(result.stdout)


def find_project(title):
    listing = json.loads(gh(["project", "list", "--owner", OWNER,
                             "--format", "json"]).stdout)
    for project in listing.get("projects", []):
        if project["title"] == title:
            return project
    return None


def create_project(title):
    created = json.loads(gh(["project", "create", "--owner", OWNER,
                             "--title", title, "--format", "json"]).stdout)
    print(f"  board created: #{created['number']}")
    return created


def link_repository(number, dry_run):
    """Show the board in the repository's Projects tab. Harmless when the
    link already exists: gh then refuses, and the refusal is ignored.

    Without this, the board exists only under its OWNER — it is absent
    from every repository page, which is the usual reason somebody says
    "I cannot find my board".
    """
    if dry_run:
        print(f"  would link the board to {REPO}")
        return
    gh(["project", "link", str(number), "--owner", OWNER, "--repo", REPO],
       check=False)
    print(f"  linked to {REPO}")


def describe(project_id, spec, dry_run):
    """The board's own description and README — the first thing anybody
    who opens the board reads."""
    short = spec.get("short_description")
    readme = spec.get("readme")
    if not short and not readme:
        return
    if dry_run:
        print("  would set the board description and README")
        return

    fields = [f'projectId: "{project_id}"']
    if short:
        fields.append(f"shortDescription: {json.dumps(short, ensure_ascii=False)}")
    if readme:
        fields.append(f"readme: {json.dumps(readme, ensure_ascii=False)}")
    query = ("mutation { updateProjectV2(input: {%s}) "
             "{ projectV2 { id } } }" % ", ".join(fields))
    if graphql(query, check=False) is None:
        print("  ⚠️  description and README unchanged")
    else:
        print("  description and README set")


def fields(number):
    listing = json.loads(gh(["project", "field-list", str(number),
                             "--owner", OWNER, "--limit", "50",
                             "--format", "json"]).stdout)
    return {f["name"]: f for f in listing["fields"]}


def option_id(field, name):
    for option in field.get("options", []):
        if option["name"] == name:
            return option["id"]
    return None


def options_literal(options):
    return ", ".join(
        "{name: %s, color: %s, description: %s}"
        % (json.dumps(o["name"], ensure_ascii=False),
           o.get("color", "GRAY"),
           json.dumps(o.get("description", ""), ensure_ascii=False))
        for o in options)


def set_status_options(field, statuses, items_with_status, force, dry_run):
    """Replace the options of the built-in Status field by the method's.

    `gh project field-create` cannot touch Status: only the GraphQL
    mutation can. ⚠️ Replacing the options gives them new ids, so every
    item loses its status. On a board that already holds statuses the
    script therefore stops and says so, unless --force-statuses is given.

    Returns True when the options are the method's once it has run.
    """
    wanted = [s["name"] for s in statuses]
    current = [option["name"] for option in field.get("options", [])]
    if current == wanted:
        print(f"  Status: {' · '.join(wanted)} (already in place)")
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
        print(f"  would set Status: {' · '.join(wanted)}")
        return True

    query = """
    mutation {
      updateProjectV2Field(input: {
        fieldId: "%s"
        singleSelectOptions: [%s]
      }) { projectV2Field { ... on ProjectV2SingleSelectField { id } } }
    }""" % (field["id"], options_literal(statuses))

    if graphql(query, check=False) is not None:
        print(f"  Status: {' · '.join(wanted)}")
        return True
    print("  ⚠️  Status options unchanged — set them by hand (docs/BOARD.md)")
    return False


def next_weekday(name):
    """The next occurrence of that weekday, today included."""
    target = WEEKDAYS.index(name.lower())
    today = date.today()
    return today + timedelta(days=(target - today.weekday()) % 7)


def iteration_literal(config):
    """The iterations of a Sprint field. `iterations` is required by the
    API — an iteration field cannot be created empty."""
    duration = int(config.get("duration_days", 14))
    start = next_weekday(config.get("starts_on", "monday"))
    count = int(config.get("count", 4))
    iterations = ", ".join(
        '{title: "Sprint %d", startDate: "%s", duration: %d}'
        % (n + 1, (start + timedelta(days=duration * n)).isoformat(), duration)
        for n in range(count))
    return ('{startDate: "%s", duration: %d, iterations: [%s]}'
            % (start.isoformat(), duration, iterations))


def ensure_fields(project_id, number, spec, dry_run):
    """Create the fields board.json asks for and the board does not have.

    An existing field is LEFT ALONE, options included: rewriting the
    options of a single-select erases the value every item carries, and
    a field the team has filled in is worth more than a template.
    """
    present = fields(number)
    for field in spec.get("fields", []):
        name, kind = field["name"], field["type"]
        if name in present:
            print(f"  field: {name} (already there, left untouched)")
            continue
        if dry_run:
            print(f"  would create field: {name} ({kind})")
            continue

        extra = ""
        if kind == "SINGLE_SELECT":
            extra = f", singleSelectOptions: [{options_literal(field['options'])}]"
        elif kind == "ITERATION":
            extra = f", iterationConfiguration: {iteration_literal(field.get('iteration', {}))}"

        query = ("mutation { createProjectV2Field(input: {projectId: \"%s\", "
                 "dataType: %s, name: %s%s}) { projectV2Field { "
                 "... on ProjectV2FieldCommon { id name } } } }"
                 % (project_id, kind, json.dumps(name, ensure_ascii=False), extra))
        if graphql(query, check=False) is None:
            print(f"  ⚠️  field not created: {name} — create it by hand")
        else:
            print(f"  field: {name} ({kind})")


def ensure_views(project_id, number, spec, dry_run):
    """Create the missing views, set their filter and their visible
    fields, and rename GitHub's lone default table."""
    query = ('query($p:ID!){node(id:$p){... on ProjectV2'
             '{views(first:50){nodes{id name layout}}}}}')
    data = graphql(query, p=project_id)
    by_name = {v["name"]: v for v in data["node"]["views"]["nodes"]}

    # GitHub names the first view "View 1": it is All items under another
    # name, so it is renamed rather than left as a duplicate.
    if "View 1" in by_name and "All items" not in by_name and not dry_run:
        rename = ('mutation($v:ID!,$n:String!){updateProjectV2View'
                  '(input:{viewId:$v,name:$n}){projectV2View{id name}}}')
        graphql(rename, check=False, v=by_name["View 1"]["id"], n="All items")
        by_name["All items"] = by_name.pop("View 1")

    field_ids = {name: f["id"] for name, f in fields(number).items()}

    for view in spec.get("views", []):
        name = view["name"]
        existing = by_name.get(name)
        if not existing:
            if dry_run:
                print(f"  would create view: {name} ({view['layout']})")
                continue
            create = ('mutation($p:ID!,$n:String!,$l:ProjectV2ViewLayout!)'
                      '{createProjectV2View(input:{projectId:$p,name:$n,'
                      'layout:$l}){projectV2View{id name}}}')
            data = graphql(create, check=False, p=project_id, n=name,
                           l=view["layout"])
            if data is None:
                print(f"  ⚠️  view not created: {name}")
                continue
            existing = data["createProjectV2View"]["projectV2View"]
            print(f"  view: {name}")
        elif dry_run:
            print(f"  view: {name} (already there) — filter and columns refreshed")
            continue

        # The filter and the visible columns ARE refreshed on an existing
        # view: they are the view's definition, they hold no data, and a
        # filter left stale is a view that quietly lies.
        if view.get("filter"):
            update = ('mutation($v:ID!,$f:String!){updateProjectV2View'
                      '(input:{viewId:$v,filter:$f}){projectV2View{id filter}}}')
            if graphql(update, check=False, v=existing["id"],
                       f=view["filter"]) is None:
                print(f"      ⚠️  filter refused: {view['filter']}")

        # Measured: "Roadmap views do not support visible fields." The
        # columns of a roadmap are its date fields, set by hand.
        if view["layout"] == "ROADMAP_LAYOUT":
            continue

        wanted = [field_ids[f] for f in view.get("fields", []) if f in field_ids]
        missing = [f for f in view.get("fields", []) if f not in field_ids]
        if missing:
            print(f"      ⚠️  {name}: unknown field(s) {', '.join(missing)}")
        if wanted:
            ids = ", ".join(f'"{i}"' for i in wanted)
            columns = ("mutation { updateProjectV2View(input: {viewId: \"%s\", "
                       "configuration: {visibleFieldIds: [%s]}}) "
                       "{ projectV2View { id } } }" % (existing["id"], ids))
            if graphql(columns, check=False) is None:
                print(f"      ⚠️  columns of {name} unchanged")


def add_issues(number, project_id, status_field, status_ok, dry_run):
    items = json.loads(gh(["project", "item-list", str(number), "--owner",
                           OWNER, "--limit", "500", "--format",
                           "json"]).stdout)["items"]
    on_board = {i.get("content", {}).get("url") for i in items}

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
        if dry_run:
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force-statuses", action="store_true",
                        help="rewrite Status even if items already carry "
                             "one (they lose it)")
    parser.add_argument("--project", type=int, metavar="N",
                        help="apply to this board instead of looking for "
                             "it; needed when the repository has two")
    args = parser.parse_args()

    spec = read_board()
    title = spec["title"]

    check_scope()

    # Three routes, narrowest first. The board of an existing project is
    # found by its link to the repository, never by its title: the titles
    # in service predate this template and do not follow it.
    if args.project:
        project = find_project_by_number(args.project)
        print("  board #%s, named on the command line" % project["number"])
    else:
        project = find_project_by_repository()
        if project:
            print("  board #%s « %s », already linked to %s"
                  % (project["number"], project["title"], REPO))
        else:
            project = find_project(title)
            if project:
                print("  board #%s, matched by title « %s »"
                      % (project["number"], title))

    if not project:
        if args.dry_run:
            print(f"  would create the board « {title} » with Status "
                  f"{' · '.join(s['name'] for s in spec['status'])}")
            print("\nDry run — nothing was written.")
            return
        project = create_project(title)
    number, project_id = project["number"], project["id"]

    link_repository(number, args.dry_run)
    describe(project_id, spec, args.dry_run)

    items = json.loads(gh(["project", "item-list", str(number), "--owner",
                           OWNER, "--limit", "500", "--format",
                           "json"]).stdout)["items"]
    with_status = [i for i in items if i.get("status")]

    status_ok = set_status_options(fields(number)["Status"], spec["status"],
                                   with_status, args.force_statuses,
                                   args.dry_run)

    ensure_fields(project_id, number, spec, args.dry_run)
    add_issues(number, project_id, fields(number)["Status"], status_ok,
               args.dry_run)

    if args.dry_run:
        ensure_views(project_id, number, spec, args.dry_run)
        print("\nDry run — nothing was written.")
        return

    ensure_views(project_id, number, spec, args.dry_run)

    print(f"\nboard ready: {project.get('url', f'#{number}')}")
    print("Left by hand, once (docs/BOARD.md): the built-in workflows, the "
          "grouping and sorting of Prioritized backlog / Roadmap / Epics, "
          "and the two date fields of the Roadmap layout.")


if __name__ == "__main__":
    main()
