<!-- Deployment pull request — title "[Déploiement] vX.Y.Z", branch `deploy/vX.Y.Z`.
     GitHub does not apply this template on its own. Two ways to call it:
       gh pr create --base main --head deploy/vX.Y.Z --title "[Déploiement] vX.Y.Z" \
         --body-file .github/PULL_REQUEST_TEMPLATE/deployment.md
     or open https://github.com/<owner>/<repo>/compare/main...deploy/vX.Y.Z?expand=1&template=deployment.md
     Full instructions: docs/DEPLOYMENT.md.

     The title and the three CHANGELOG.md headings below stay in French on purpose:
     scripts/publish_release.py matches them literally, and so does the wiki page.

     ⚠️ This pull request opens AFTER the whole batch is merged, and merges LAST. A
     feature pull request merged after it would reach production without appearing in
     the release note. -->

## Version

- `VERSION`: `X.Y.Z` (previous: `X.Y.Z`) — **minor** when the batch brings at least one story, **patch** when it only holds fixes
- Production right now: commit `…`
- Batch: every pull request merged since `vX.Y.Z` up to `…`
- Milestone delivered: `vX.Y.0 — …` — what is not ready moves to the next milestone, one line each here:

## Release note

The `## vX.Y.Z — DD/MM/YYYY` section of `CHANGELOG.md`, visible in this pull request's diff, **is** the release note: it is not copied here. It carries three headings:

- [ ] *User stories et fonctionnalités déployées* — story title, number, pull request
- [ ] *Corrections, outillage et documentation*
- [ ] *À savoir* — what is shipped but inactive, migrations, actions expected
- [ ] `python3 scripts/wiki_release_notes.py` run: `docs/wiki/Release-notes.md` carries the section, and the repository wiki publishes it on merge

## Migrations reaching production

<!-- The deployment guard is updated IN this pull request: Romain sees and approves
     every migration before it goes out. One line per new migration, or "none". -->

| Migration | SHA-256 fingerprint | Reviewed: reversible without touching the database? |
|---|---|---|
| none | | |

## Before the merge — Romain

- [ ] No pull request of the batch is still waiting to be merged: this one is the last
- [ ] CI green on the last commit of `deploy/vX.Y.Z`
- [ ] The diff only touches `VERSION`, `CHANGELOG.md`, `docs/wiki/Release-notes.md` and the migration guard
- [ ] Every migration in the table above is reviewed and approved
- [ ] Nothing under "À savoir" needs a prior action that has not been taken

## After the merge — agent

- [ ] Deploy **the merge commit** with the project's script: CI green, backup, rollback, verification
- [ ] `python3 scripts/publish_release.py`: tag `vX.Y.Z` and GitHub release from the changelog section
- [ ] Verified in production: <!-- URL and journeys checked -->
- [ ] Stories of the batch moved to *Done*
- [ ] Milestone closed (`gh api -X PATCH repos/<owner>/<repo>/milestones/<n> -f state=closed`)

## Rollback

<!-- The exact command of the project's script, and where the backup taken before the
     deployment lives. -->
