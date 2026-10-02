---
name: project-kickoff
description: Start a Rails web project from the kickoff template, applying the delivery-by-user-story method — repository, a 25-line AGENTS.md, labels, the seven-status board with its Roadmap and Epics views, wiki, local recette environment, [Epic], [US], [Task] and [BUG] issues on their templates with dependencies and release milestones, deployment pull request and release notes. Use when starting a new project ("kick off", "new project", "nouveau projet", "lancer un projet", "set up the repo", "bootstrap"), when turning a need into user stories on a board, or when preparing a [Déploiement] pull request and its GitHub release.
---

# Starting a project with kickoff

**The method is authoritative**:
`/Users/albert/Documents/Claude/ObsiClaud/dev/methode/Méthode - Livraison applicative par user story.md`.
Read it once, starting with the eight-line summary and § 10 bis; come back to the rest when a question
comes up. This skill does not copy it: it says **which gestures do, with the `romain-nicod/kickoff`
template, what the method asks for.**

No mention of the assistant or of its editor in the repository, the issues, the pull requests or the
commits, and no `Co-authored-by:` line (nor `Co-Authored-By:`) in a commit or a pull request.

---

## 1. Setting the ground

Ask once for what cannot be worked out:

| Value | Used for |
|---|---|
| The project's name, and one sentence | `kickoff.yml`, README |
| Repository `owner/name` | a new private repository on the **personal account** (Q8) |
| The project's folder in the vault | first line of `AGENTS.md` |
| Production hosting, if it is known | `AGENTS.md`, `docs/DEPLOYMENT.md` |
| The need, in whatever form it comes | the first `[US]` issues |

Check the active account before creating anything: `gh api user --jq .login`.

## 2. Creating the repository

```bash
gh repo create <owner>/<name> --template romain-nicod/kickoff --private --clone
```

The clone lives in `~/Documents/Claude/code/<name>`. Fill in the five values of `kickoff.yml`, then:

```bash
# The identity of the account that merges, before the first commit; the clone's worktrees
# share it. Any other address makes a second author appear in GitHub's history.
git config --local user.name "Romain Nicod"
git config --local user.email 296897605+romain-nicod@users.noreply.github.com
bin/kickoff --dry-run
bin/kickoff
# 🔴 Never `rails new` before `bin/kickoff`: it is bin/kickoff that puts Rails' own ignore
# rules into .gitignore, which `rails new --skip .` will not write ("skip .gitignore"), and
# the boilerplate ends on a `git add .` that would commit all of tmp/, log/ and storage/.
rails new -d postgresql \
  -m https://raw.githubusercontent.com/romain-nicod/rails-ready/main/template.rb --skip .
python3 scripts/after_rails_new.py
```

`after_rails_new.py` exits non-zero when those rules are missing, and it names the missing gems
(`capybara`, `selenium-webdriver`, `sentry-rails`): add them, `bundle install`. In the same go:

- create the project's vault folder and its map, linked into the graph;
- record the repository in `ObsiClaud/dev/Dépôts AI-GMENTED.md` (line, paragraph, overlap);
- before the first push, read what git really ignores — a silent `.gitignore` costs a secret or a
  thousand files:

```bash
git check-ignore -v .env config/master.key tmp/cache log/development.log storage/x
git ls-files log tmp storage 'config/*.key' | grep -v '\.keep$'   # must print nothing
```

## 3. Configuring GitHub

In this order — **the labels first**: GitHub silently drops a label that does not exist from an issue
created on a template.

```bash
python3 scripts/setup_repo.py --dry-run && python3 scripts/setup_repo.py
gh auth refresh -s project --hostname github.com
python3 scripts/setup_project.py --dry-run && python3 scripts/setup_project.py
```

Labels: `type:epic`, `type:user-story`, `Task`, `type:bug`, `type:defect`, `remediation:validée`, `à revoir par Romain`, `status:blocked`. Board:
`Backlog · Ready · In progress · En recette · In review · À déployer · Done`. Those names are
identifiers: the scripts create them literally, and translating one breaks the board.

Then walk Romain, step by step, through what the API does not do:

- the board's workflows, the Kanban grouping, the Roadmap dates and the Epics grouping:
  `docs/BOARD.md`, "To do by hand";
- the wiki's first page: `docs/WIKI.md`, "First publication".

## 4. `AGENTS.md`, 25 lines at most

Fill in what `bin/kickoff` left: the board URL (printed by `setup_project.py`), production, the
deployment script. **Only what is specific to the project**: never the method. Traps go to
`docs/wiki/Traps.md`, decisions to an ADR page of `docs/wiki/`. `CLAUDE.md` stays at three lines.
Check: `wc -l AGENTS.md CLAUDE.md`.

## 5. Creating the issues on their templates

**A need Romain states becomes an `[US]` right away**; a need too big becomes several stories. The body
follows `.github/ISSUE_TEMPLATE/user_story.md`: **review header first**, then state, story, `CA-01…`
criteria, impacts (each one filled in or "none"), out of scope, tasks, DoD. Write the body in a
scratch file, never in the repository.

🔴 **Epic → story → task, dependencies, milestone** (method § 3 bis) — commands in `docs/BOARD.md`,
"Epics, dependencies and milestones":

- every `[US]` and `[BUG]` is a native sub-issue of an **`[Epic]`** (`epic.md`, label `type:epic`);
  no orphan story;
- a dependency is a native *blocked by* relation, never only a sentence;
- one **milestone per release** (`vX.Y.0 — <theme>`, with a due date); an issue gets it when it moves
  to *Ready* at the latest.

🔴 **The review header** opens every issue, in English: ⚠️ *To validate by Romain* or 🟢 *Nothing to
validate*, then **three checklists** — *Impacted screens*, *Wireframes to validate* (one link per
screen), *Specs to validate* (one path per spec) — one checkbox per item, each list filled in or
"none", and a last line with parent · blocked by · blocks · milestone. Romain ticks what he has
validated; the issue turns 🟢 when every box is ticked, and the `à revoir par Romain` label follows
the emoji.

🔴 **A screen impacted ⇒ the agent creates its wireframe and links it, every time**, when the issue is
created, without being asked. **A spec needed ⇒ the agent writes it** and links it. "To be produced"
is never a lasting state.

```bash
gh issue create --repo <owner>/<name> --title "[US] <need or journey>" \
  --label "type:user-story" --label "à revoir par Romain" --body-file <body.md>
gh project item-add <n> --owner <owner> --url <issue URL>
```

- **`[Task] <concrete action>`** on `task.md`, label `Task`, attached to the story as a sub-issue:

  ```bash
  id=$(gh api repos/<owner>/<name>/issues/<task number> --jq .id)
  gh api repos/<owner>/<name>/issues/<story number>/sub_issues -F sub_issue_id="$id"
  ```

- **`[BUG] <the faulty behaviour>`** on `bug.md`, labels `type:bug` and `à revoir par Romain`: a defect
  observed on the recette environment, in production, in a QA review, or a flaky test. Same cycle as a
  story.
- **`[DEFECT] <the error>`** on `defect.md`, label `type:defect`: an error in how the work was done —
  a step skipped, a rule ignored, a check claimed without being run. Filed by the agent **in the session
  that made it**, before anything else: what happened, why, previous occurrences, prevention. See
  `docs/DEFECTS.md`.
- **Two stories exist in every project from day one**, whatever the need: `[US] Show a maintenance
  page when the site does not answer` and `[US] Be warned when the site, its jobs or its backups
  stop`. Their cases and services are numbered in `docs/OPERATIONS.md` (A1–B5, M1–M4); the
  criteria cite those numbers, and say which cases the project's exposure leaves uncovered. The
  first deployment to production waits for both.
- From three issues to review on: vault note `<Project> - Revue des US - YYYYMMDD`, one checkbox and
  one comment line per issue.
- **Romain moves them to *Ready*.** The agent then removes the label:
  `gh issue edit <n> --remove-label "à revoir par Romain"`.

## 6. During the stories — the commands; the method is authoritative

- Worktree and branch: `git -C code/<name> worktree add -b us-NNN-slug ../<name>-worktrees/us-NNN-slug origin/main`.
- Changing a status (*In progress*, *En recette*, *In review*, *Done*): `docs/BOARD.md`, "Moving a
  story".
- Tests: `docs/TESTS.md`; pull request on `.github/PULL_REQUEST_TEMPLATE.md`, `Closes` for the story
  and for every task.
- Recette environment: creation, rebuild for every batch and `bin/recette prepare` in
  `docs/RECETTE.md`.
- **Never a merge into `main`**: Romain merges, nobody else. Only the local `recette` branch receives
  merges from the agent.
- **Branch hygiene, automatic**: `setup_repo.py` turns on branch deletion at merge. After every merge
  established through the API (`gh api repos/<owner>/<name>/pulls/<n> --jq .merged_at`), delete the
  story's worktree and local branch. A branch closed without a merge, or replaced, is saved as a bundle
  (`git bundle verify` must answer "okay"), then deleted locally and on GitHub. No `worktree-agent-*`
  branch survives its session. Monthly check of what is left. Commands: `CONTRIBUTING.md`, "Branch
  hygiene".

## 7. Deploying a batch

1. **Wait until the whole batch is merged.** The deployment pull request opens afterwards and **merges
   last**: one merged after it would go out without appearing in the release note.
2. Branch `deploy/vX.Y.Z` from `origin/main`: `VERSION`, the `## vX.Y.Z — DD/MM/YYYY` section at the top
   of `CHANGELOG.md` with its three headings, and **the migration guard** updated
   (`docs/DEPLOYMENT.md`, Rails section).
3. The `[Déploiement] vX.Y.Z` pull request:

   ```bash
   gh pr create --base main --head deploy/vX.Y.Z --title "[Déploiement] vX.Y.Z" \
     --body-file .github/PULL_REQUEST_TEMPLATE/deployment.md
   ```

4. CI green, Romain merges. Deploy **the merge commit** with the project's script.
5. Production verified, then:

   ```bash
   python3 scripts/publish_release.py --dry-run
   python3 scripts/publish_release.py
   ```

6. The issues of the batch move to *Done*, and the release's milestone is closed.

## 8. Traps

- `setup_project.py` refuses to rewrite the statuses of a board that already holds items: the options
  of *Status* would get new identifiers and every item would lose its own.
- A wiki repository only renders `master`; the *Wiki* workflow publishes nothing until Romain has
  created the first page.
- `publish_release.py` refuses to move a tag that is already published: a fix takes a new number.
- A secret never goes through the conversation nor through the command line: the host's secrets are
  entered by Romain, step by step.

## What is authoritative

| Subject | Where |
|---|---|
| The delivery cycle | the method note in the vault |
| Templates, scripts, the Rails stack, this skill | the `kickoff` repository; `~/.claude/skills/project-kickoff` is a symbolic link to `skills/project-kickoff` of its main clone |
| The rules of a project | its own `AGENTS.md` |
| The application's generator | `rails-ready` |
