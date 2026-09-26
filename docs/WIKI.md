# The wiki

The method files these in the project's GitHub wiki (§ 1, § 7, Q12): **every delivered story** (its
journey, how it works), **the architecture diagrams**, **the decisions and ADRs**, the practical
guides. The vault keeps nothing but a link to them.

## A single source: `docs/wiki/`

A GitHub wiki is a separate repository, which pull requests do not show. Pages are therefore written
in `docs/wiki/`, in the story's pull request, where Romain reviews them; the workflow
`.github/workflows/wiki.yml` publishes them on every merge to `main` that touches that folder.

- One page per file, named `Title-With-Dashes.md`: that is the page's name in the wiki.
- A page edited in the wiki interface is overwritten at the next publication.
- A page removed from `docs/wiki/` stays in the wiki: delete it by hand.
- The workflow only uses the token GitHub provides, never a personal one.

## What goes where

| Content | Where |
|---|---|
| Page of a delivered story | `docs/wiki/US-NNN-<slug>.md`, in the story's pull request |
| Architecture diagram | [`docs/wiki/Architecture.md`](wiki/Architecture.md), in the pull request that changes the structure |
| Decision | `docs/wiki/ADR-NNNN-<slug>.md`, plus a line in [`Decisions.md`](wiki/Decisions.md) |
| Cross-cutting trap | [`docs/wiki/Traps.md`](wiki/Traps.md) |
| Release notes | `docs/wiki/Release-notes.md`, **generated** from `CHANGELOG.md` by `scripts/wiki_release_notes.py`, in the deployment pull request |
| Data schema | [`docs/SCHEMA.md`](SCHEMA.md): it changes in the same commit as the migration |
| Commands, variables | `README.md`, `.env.example` |
| State of the project, cross-cutting lessons | the vault |

## First publication — Romain, once

GitHub only creates the wiki's repository once a first page has been saved by hand.

1. Open `https://github.com/{{REPO}}/wiki`.
2. Click **Create the first page**, keep the title `Home`, click **Save page**.
3. **Actions** tab → **Wiki** workflow → **Run workflow** → **Run workflow**.
4. Reload the wiki: the `Home` page is the one from `docs/wiki/Home.md`.

Until step 2 is done, the workflow says so and finishes without an error.

## Publishing by hand

```bash
git clone https://github.com/{{REPO}}.wiki.git /tmp/{{REPO_NAME}}.wiki
cp -R docs/wiki/. /tmp/{{REPO_NAME}}.wiki/
git -C /tmp/{{REPO_NAME}}.wiki add -A
git -C /tmp/{{REPO_NAME}}.wiki commit -m "Publish docs/wiki"
git -C /tmp/{{REPO_NAME}}.wiki push origin HEAD:master
```

A wiki repository only renders the `master` branch. ⚠️ Pushing `main` is accepted without an error:
`HEAD` stays on `master`, and nothing written on `main` is displayed. The failure is silent — the push
succeeds and the page does not change (verified on 25/08/2026).
