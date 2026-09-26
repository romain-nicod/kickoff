# {{PROJECT_NAME}} — AGENTS.md

- Vault: `{{VAULT_FOLDER}}` (project map, traps, state of play).
- Method, to be read before any story: `/Users/albert/Documents/Claude/ObsiClaud/dev/methode/Méthode - Livraison applicative par user story.md` (the eight-line summary and § 10 bis first).
- Repository: https://github.com/{{REPO}} · board: <!-- Project URL, printed by scripts/setup_project.py --> · wiki: https://github.com/{{REPO}}/wiki (source: `docs/wiki/`).
- Stack: Rails, PostgreSQL, Minitest, Capybara/Selenium. Commands: `bin/setup`, `bin/rails test`, `bin/rails test:system`, `bin/rubocop`, `bin/brakeman --no-pager`, `bundle exec bundler-audit --update`, `bin/importmap audit`.
- Ports: dev `3000` in `code/{{REPO_NAME}}`; recette `3100` in `code/{{REPO_NAME}}-recette` (local `recette` branch, `bin/recette prepare|start`). See [docs/RECETTE.md](docs/RECETTE.md).
- Issues on the templates of `.github/ISSUE_TEMPLATE/`: `[US]` and `[BUG]`, reviewed by Romain who moves them to *Ready*; `[Task]`, sub-issues kept by the agent.
- One story = one worktree `code/{{REPO_NAME}}-worktrees/us-NNN-slug/`, one branch `us-NNN-slug`, one pull request.
- Branch hygiene: once a merge is established, delete the local branch and the worktree; a branch closed or replaced is deleted everywhere once bundled; no `worktree-agent-*` survives its session; monthly check ([CONTRIBUTING.md](CONTRIBUTING.md)).
- Production: <!-- public URL --> · deployment: <!-- the project's script --> then `python3 scripts/publish_release.py` ([docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)).
- Emails: vault note `dev/outils/Emails - Envoi SMTP Infomaniak et tests Mailpit.md` · errors: Sentry (`SENTRY_DSN`).

## Forbidden

- Romain merges, nobody else: never a merge, an auto-merge or a scheduled merge by an agent (the local `recette` branch is the only exception).
- No secret in Git; no mention of the assistant or of its editor, anywhere; no `Co-authored-by:` line in a commit or a pull request.
- Git identity of the clone, before any commit: `git config --local user.name "Romain Nicod"` and `git config --local user.email 296897605+romain-nicod@users.noreply.github.com`.
- **English everywhere in the repository**: code, comments, test names, commits, issues, pull requests, documentation. Three exceptions, and no fourth: the product's own interface follows the language of its users, a verbatim quote stays as it was said, and the method's vocabulary keeps the words that name things elsewhere — `recette` (a branch, a script, a port), the board statuses and the `à revoir par Romain` label. Renaming those is a migration, not a translation.

## Traps

- Cross-cutting traps: [docs/wiki/Traps.md](docs/wiki/Traps.md).
