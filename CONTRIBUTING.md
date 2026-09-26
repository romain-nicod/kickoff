# Contributing

This repository applies the "Delivery by user story" method:
`/Users/albert/Documents/Claude/ObsiClaud/dev/methode/Méthode - Livraison applicative par user story.md`.
Branches, commits, tests, the recette environment, pull requests, review and deployment are
authoritative there; what is specific to this repository is in [AGENTS.md](AGENTS.md), and the coding
rules are in [GOLDEN_RULES.md](GOLDEN_RULES.md).

This page only adds the identity of the commits, branch hygiene and one rule about writing.

## Identity of the commits

No `Co-authored-by:` line (nor `Co-Authored-By:`), in a commit or in a pull request. Every clone
carries, before its first commit, the identity of the account that merges; its worktrees share it:

```bash
git config --local user.name "Romain Nicod"
git config --local user.email 296897605+romain-nicod@users.noreply.github.com
```

Any other address makes GitHub add a co-author at every squash merge.

## Branch hygiene

Automatic on every project (method § 6). GitHub deletes the remote branch on merge: the
`delete_branch_on_merge` setting is applied by `python3 scripts/setup_repo.py`. The rest is up to the
agent, from the main clone.

**Once a merge is established**, the story's worktree and local branch disappear. A merge is
established through the API, never on the board's word: a squash merge does not make the branch an
ancestor of `main`, and `git branch -d` would refuse it wrongly.

```bash
gh api repos/{{REPO}}/pulls/<PR number> --jq .merged_at        # a date, otherwise stop
git -C code/{{REPO_NAME}} worktree remove ../{{REPO_NAME}}-worktrees/us-NNN-slug   # refuses a modified worktree
git -C code/{{REPO_NAME}} branch -D us-NNN-slug
git -C code/{{REPO_NAME}} fetch --prune origin
```

**A branch closed without a merge, or replaced**, is first saved as a bundle outside the repository,
then deleted locally and on GitHub:

```bash
mkdir -p ~/Documents/Claude/projects/{{REPO_NAME}}/branches
git -C code/{{REPO_NAME}} bundle create ~/Documents/Claude/projects/{{REPO_NAME}}/branches/<branch>-YYYYMMDD.bundle <branch>
git bundle verify ~/Documents/Claude/projects/{{REPO_NAME}}/branches/<branch>-YYYYMMDD.bundle   # must answer "okay", otherwise stop
git -C code/{{REPO_NAME}} push origin --delete <branch>
git -C code/{{REPO_NAME}} branch -D <branch>
```

**No `worktree-agent-*` branch survives the session** that created it: its worktree and its branch are
deleted before handing back, with the same backup if it carries unmerged work.

**Monthly check**: list what is left and write, for every branch, its reason to exist (an open story on
the board); otherwise, treat it as above.

```bash
git -C code/{{REPO_NAME}} fetch --prune origin
git -C code/{{REPO_NAME}} worktree list
git -C code/{{REPO_NAME}} branch -vv
gh api repos/{{REPO}}/branches --paginate --jq '.[].name'
```

## The deliverable is the diff

Aim for **the smallest diff that does the work**: Romain should see the change, not go looking for it.

- Never touch the indentation of a line you are not changing: a shift makes ten lines look modified
  when only one is.
- Never retype a block to change a word in it: the risk of losing a closing tag is real, and the diff
  becomes unreadable.
- QA passes (security, accessibility, formatting) are commits separate from behaviour commits.
- Read `git diff` before saying it is done: a correct file can still produce an unreadable diff.

The test before pushing: how many lines changed, for how many useful lines? Past two for one, cut it
differently.
