# Deployment

Every release to production goes through **its own deployment pull request**, a rule shared by all of
Romain's web sites and applications. The method is authoritative (§ 6); this page says how to apply it
in this repository.

## The cycle of a version

1. **The whole batch of stories is merged by Romain.** The issues sit in *À déployer*.

   ⚠️ **The deployment pull request opens after the batch is merged, and merges last.** A feature pull
   request merged after it reaches production without appearing in the release note (observed on PEF on
   12/09/2026).
2. **The agent prepares the version** on a branch started from `origin/main`:

   ```bash
   git fetch origin
   git switch -c deploy/vX.Y.Z origin/main
   ```

   It updates `VERSION` and adds the `## vX.Y.Z — DD/MM/YYYY` section at the top of `CHANGELOG.md`,
   with its three headings (the model is a comment in the file). **If there are new migrations, it
   reviews them and adds them to the deployment guard in that same branch**: Romain sees and approves
   in the pull request what is going to production.

   Then it **regenerates the wiki page of the release notes**, in the same branch:

   ```bash
   python3 scripts/wiki_release_notes.py
   ```

   It copies the sections of `CHANGELOG.md` into `docs/wiki/Release-notes.md`, which
   `.github/workflows/wiki.yml` publishes to the wiki once the pull request is merged: **every release
   has its release note in the repository's wiki** (Romain's rule of 25/09/2026), written once.
   `python3 scripts/wiki_release_notes.py --check` fails when the page and the changelog diverge.

   Nothing else changes in that branch.
3. **It opens the pull request**, titled `[Déploiement] vX.Y.Z`, on the dedicated template. GitHub does
   not apply that template on its own; two ways to call it:

   ```bash
   git push -u origin deploy/vX.Y.Z
   gh pr create --base main --head deploy/vX.Y.Z --title "[Déploiement] vX.Y.Z" \
     --body-file .github/PULL_REQUEST_TEMPLATE/deployment.md
   ```

   or, in the browser:
   `https://github.com/{{REPO}}/compare/main...deploy/vX.Y.Z?expand=1&template=deployment.md`
4. **CI green → Romain reviews and merges.**
5. **The agent deploys the merge commit** with the project's script (below).
6. **It publishes the release**, once production is verified:

   ```bash
   python3 scripts/publish_release.py --dry-run
   python3 scripts/publish_release.py
   ```

   The script reads `VERSION` and `CHANGELOG.md` at the deployed commit, sets the `vX.Y.Z` tag, pushes
   it and creates the GitHub release with the changelog section, word for word. It refuses to move a
   tag that is already published.
7. **The stories of the batch move to *Done*.** The list of GitHub releases is the trail of
   deployments.

The `[Déploiement] vX.Y.Z` title and the three headings of `CHANGELOG.md` stay in French: they are
identifiers, matched literally by `scripts/publish_release.py`.

## Numbering

`MAJOR.MINOR.PATCH`. The **minor** goes up for a version that brings at least one story; the **patch**
for a version that only holds fixes; the **major** on Romain's decision. `VERSION` stays at `0.0.0`
until something is in production.

## The project's deployment script

<!-- To fill in at the first deployment: path of the script, host, command. -->

**Script:** _to fill in_ · **Production:** _to fill in_

Whatever the hosting, it does at least this, in this order:

1. refuse if the CI of this commit of `main` has not finished green;
2. refuse any new migration missing from the deployment guard;
3. back up the database and the files, and say where;
4. deploy **this commit**, not the state of a working folder;
5. run the migrations, then verify production (`/up`, one main journey);
6. roll back to the previous version if the verification fails, and say so.

While it runs, visitors get the maintenance page, never a raw `502` (case A1 of
[OPERATIONS.md](OPERATIONS.md)). The **first** deployment to production also needs the checklist of
OPERATIONS.md § 3: the maintenance page and the four monitors, each alert fired once.

## Rolling back

An agent never pushes to `main`: no `git revert` pushed directly. Rolling back redeploys the previous
version, by its tag, with the same script; the fix follows the normal cycle (story or defect, pull
request, merge by Romain, new patch version).
