# Board

The GitHub board (Projects v2) is the project's **place of coordination**: at a glance, it says what
is waiting for whom. The rules of the cycle are authoritative in the method
(`/Users/albert/Documents/Claude/ObsiClaud/dev/methode/Méthode - Livraison applicative par user story.md`,
§ 2.1); this page only says how the board is installed and kept.

**Board:** <!-- URL printed by scripts/setup_project.py -->

## The seven statuses

The names of the statuses are identifiers: `scripts/setup_project.py` creates them literally, and two
of them stay in French because the method's vocabulary names them that way.

| Status | Set by |
|---|---|
| Backlog | the agent, when a `[US]` or a `[BUG]` is created (label `à revoir par Romain`) |
| Ready | **Romain** |
| In progress | the agent, when the worktree opens |
| En recette | the agent, branch merged into the recette environment, every test green |
| In review | the agent, pull request opened and CI green |
| À déployer | the board's workflow, on merge |
| Done | the agent, once the deployment is verified |

A defect found on the recette environment or in review sends the story back to **In progress**.

## Installation

```bash
gh auth refresh -s project --hostname github.com   # once per machine
python3 scripts/setup_project.py --dry-run
python3 scripts/setup_project.py
```

The script creates the board, links it to the repository, sets the seven statuses, adds the issues it
is missing (open ones in *Backlog*, closed ones in *Done*) and creates five views: *Kanban*,
*À revoir par Romain*, *All items*, *Roadmap* and *Epics*. It never moves an item that already holds a status.

⚠️ Rewriting the options of *Status* gives them new identifiers: every item loses its status. On a
board that already holds statuses the script stops; `--force-statuses` overrides it.

### To do by hand, once

The API exposes neither the built-in workflows nor the grouping of the views.

1. Open the board → `⋯` menu, top right → **Workflows**.
2. **Item closed** → enable → *Set value*: `Status` = `À déployer`.
3. **Pull request merged** → enable → `Status` = `À déployer`.
4. **Auto-add to project** → enable → filter `is:issue is:open` on this repository.
5. **Kanban** view → `⋯` → *Group by* → `Status`.
6. **Roadmap** view → *Date fields* → start and target = `Milestone` → `⋯` → *Group by* →
   `Milestone`. Each release then shows as a band ending on its due date.
7. **Epics** view → `⋯` → *Group by* → `Parent issue`. Add the *Sub-issues progress* field if
   GitHub does not show it.

If the script could not set the statuses: `Status` → *Edit field* → create the options in the order of
the table above, with exactly those names.

## Epics, dependencies and milestones

The rules are the method's (§ 3 bis); these are the commands.

```bash
# A story or a bug becomes a native sub-issue of its epic (same call for a task under its story)
id=$(gh api repos/{{OWNER}}/<repo>/issues/<story> --jq .id)
gh api repos/{{OWNER}}/<repo>/issues/<epic>/sub_issues -F sub_issue_id="$id"

# <story> is blocked by <other>: a native relation, shown on the issue and on the board
id=$(gh api repos/{{OWNER}}/<repo>/issues/<other> --jq .id)
gh api repos/{{OWNER}}/<repo>/issues/<story>/dependencies/blocked_by -F issue_id="$id"

# One milestone per release, with its due date; an issue gets it when it moves to Ready
gh api repos/{{OWNER}}/<repo>/milestones -f title="vX.Y.0 — <theme>" -f due_on="YYYY-MM-DDT00:00:00Z"
gh issue edit <n> --milestone "vX.Y.0 — <theme>"
```

After each change, the review header at the top of the issue body is brought in line: the native
relation is authoritative, the header mirrors it.

## Moving a story

```bash
gh project field-list <n> --owner {{OWNER}} --format json   # id of the Status field and of its options
gh project item-list <n> --owner {{OWNER}} --format json    # id of the item
gh project item-edit --id <item> --project-id <project> \
  --field-id <Status field> --single-select-option-id <option>
```

No GitHub Action with a personal token for these transitions, as long as nothing demands one.
