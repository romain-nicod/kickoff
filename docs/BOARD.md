# Board

The GitHub board (Projects v2) is the project's **place of coordination**: at a glance, it says what
is waiting for whom. The rules of the cycle are authoritative in the method
(`/Users/albert/Documents/Claude/ObsiClaud/dev/methode/Méthode - Livraison applicative par user story.md`,
§ 2.1); this page only says how the board is installed and kept.

**Board:** <!-- URL printed by scripts/setup_project.py -->

## The board is described in one file

[`.github/board.json`](../.github/board.json) holds the whole board: its title, its description, the
seven statuses, the custom fields and every view with its filter and its columns. Its README text
lives beside it in [`.github/board.md`](../.github/board.md).

`scripts/setup_project.py` applies that description. **Adding a view or a field is an edit to
`board.json`, never to the script.**

The shape comes from the board built for the HotelRooms project
([ai-gmented-pm/hotelrooms](https://github.com/ai-gmented-pm/hotelrooms), Le Wagon certification,
Bloc 2), where it ran a four-developer team; it is stripped here of everything that belonged to that
project — its fictitious `Developer` roster, its Rails `Route` field, its hard-coded sprint dates.

## The seven statuses

The names of the statuses are identifiers: the script creates them literally, and two of them stay in
French because the method's vocabulary names them that way.

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

There is **no Blocked status**, on purpose: a story stopped by something outside itself takes the
`status:blocked` label and shows up in the *Blocked* view. A status would let it drift silently; a
label forces a comment saying what blocks it.

## The fields

| Field | Why |
|---|---|
| `MoSCoW` | What ships if time runs out. Named without an accent because a view filter addresses a field by its lowercased name — `moscow:"Won't have"` |
| `Phase` | The stretch of the project a story belongs to. **The options shipped by the template are placeholders** — rename them to the project's own phases before the first story |
| `Sprint` | Iterations, two weeks, starting on the first Wednesday after the board is created. The *Current sprint* view filters on `sprint:@current` and never needs editing again |
| `Estimate` | Story points. Only worth filling once a few sprints give it a scale |
| `Start date`, `Target date` | Left in English: the Roadmap layout is configured on two date fields, and these are the names it offers first |

## The views

| View | Layout | Filter |
|---|---|---|
| Kanban | board | — |
| À revoir par Romain | table | `label:"à revoir par Romain"` |
| Current sprint | board | `sprint:@current` |
| Prioritized backlog | table | `-status:Done -moscow:"Won't have"` |
| Roadmap | roadmap | `-label:Task` |
| Epics | table | `-label:Task` |
| Defects | table | `label:type:defect` |
| Blocked | table | `label:"status:blocked"` |
| All items | table | — |

## Installation

```bash
gh auth refresh -s project --hostname github.com   # once per machine
python3 scripts/setup_project.py --dry-run
python3 scripts/setup_project.py
```

The script creates the board, links it to the repository, writes its description and README, sets the
seven statuses, creates the fields and the views of `board.json`, and adds the issues it is missing
(open ones in *Backlog*, closed ones in *Done*).

**It never deletes and never renames.** A field and a view are matched by name, so renaming one in
`board.json` creates a second one next to the first instead of renaming it. An existing field is left
untouched, its options included: rewriting the options of a single-select erases the value every item
carries. A view's filter and columns, which hold no data, ARE refreshed — a stale filter is a view
that quietly lies.

⚠️ The one exception is `Status`: its options must be **replaced** to become the method's, which gives
them new identifiers and makes every item lose its status. On a board that already holds statuses the
script stops; `--force-statuses` overrides it, and then every item must be placed again.

### To do by hand, once

The API sets the layout, the filter and the columns of a view. It does **not** expose the built-in
workflows, the grouping and sorting of a view, nor the date fields of the Roadmap layout.

1. Open the board → `⋯` menu, top right → **Workflows**.
2. **Item closed** → enable → *Set value*: `Status` = `À déployer`.
3. **Pull request merged** → enable → `Status` = `À déployer`.
4. **Auto-add to project** → enable → filter `is:issue is:open` on this repository.
5. **Prioritized backlog** → `⋯` → *Group by* → `MoSCoW`.
6. **Roadmap** → `⋯` → *Date fields* → `Start date` → `Target date`; *Markers* → `Milestone`, so the
   due date of each release shows as a vertical line (method § 3 bis.2); *Group by* → `Milestone`.
   GitHub positions items on date or iteration fields only: a milestone is a marker, not a date field.
7. **Epics** → `⋯` → *Group by* → `Parent issue`. Add the *Sub-issues progress* field if GitHub does
   not show it.

A board view created by the script is **already grouped by `Status`** — measured, not assumed; there
is nothing to do for *Kanban* or *Current sprint*.

If the script could not set the statuses: `Status` → *Edit field* → create the options in the order of
the table above, with exactly those names.

## "I cannot see the board on my repository"

A Projects v2 board belongs to an **owner** — a user or an organisation — and never to a repository. A
repository only carries a *link* to it. So a board is invisible from a repository until
`gh project link` is run, which the script does on every run:

```bash
gh project link <n> --owner <owner> --repo <owner>/<repo>
```

And a board owned by an organisation never appears under a personal account, whatever the repository:
it lives at `https://github.com/orgs/<org>/projects/<n>`, and `gh project list --owner <user>` does not
list it. Check which owner holds it before looking for a bug:

```bash
gh api graphql -f query='query{repository(owner:"OWNER",name:"REPO"){projectsV2(first:10){nodes{number title url}}}}'
```

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
