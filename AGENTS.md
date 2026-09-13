# {{PROJECT_NAME}} — AGENTS.md

- Vault : `{{VAULT_FOLDER}}` (carte du projet, pièges, état d'avancement).
- Méthode, à lire avant toute US : `/Users/albert/Documents/Claude/ObsiClaud/dev/methode/Méthode - Livraison applicative par user story.md` (résumé en 8 lignes et § 10 bis d'abord).
- Dépôt : https://github.com/{{REPO}} · board : <!-- URL du Project, affichée par scripts/setup_project.py --> · wiki : https://github.com/{{REPO}}/wiki (source : `docs/wiki/`).
- Stack : Rails, PostgreSQL, Minitest, Capybara/Selenium. Commandes : `bin/setup`, `bin/rails test`, `bin/rails test:system`, `bin/rubocop`, `bin/brakeman --no-pager`, `bundle exec bundler-audit --update`, `bin/importmap audit`.
- Ports : dev `3000` dans `code/{{REPO_NAME}}` ; recette `3100` dans `code/{{REPO_NAME}}-recette` (branche locale `recette`, `bin/recette prepare|start`). Voir [docs/RECETTE.md](docs/RECETTE.md).
- Issues sur les gabarits de `.github/ISSUE_TEMPLATE/` : `[US]` et `[BUG]`, revus par Romain qui les passe en *Ready* ; `[Task]`, sous-issues tenues par l'agent.
- Une US = un worktree `code/{{REPO_NAME}}-worktrees/us-NNN-slug/`, une branche `us-NNN-slug`, une PR.
- Hygiène des branches : après merge constaté, supprimer branche locale et worktree ; branche fermée ou remplacée supprimée partout après bundle ; aucune `worktree-agent-*` après sa session ; contrôle mensuel ([CONTRIBUTING.md](CONTRIBUTING.md)).
- Production : <!-- URL publique --> · déploiement : <!-- script du projet --> puis `python3 scripts/publish_release.py` ([docs/DEPLOIEMENT.md](docs/DEPLOIEMENT.md)).
- Emails : note vault `dev/outils/Emails - Envoi SMTP Infomaniak et tests Mailpit.md` · erreurs : Sentry (`SENTRY_DSN`).

## Interdits

- Romain seul merge : jamais de merge, d'auto-merge ni de merge programmé par un agent (seule la branche locale `recette` fait exception).
- Aucun secret dans Git ; aucune mention de l'assistant ou de son éditeur, nulle part ; aucune ligne `Co-authored-by:` dans un commit ou une PR.
- Identité Git du clone, avant tout commit : `git config --local user.name "Romain Nicod"` et `git config --local user.email 296897605+romain-nicod@users.noreply.github.com`.
- Code, commentaires et noms de tests en anglais ; commits, issues, PR et interface en français.

## Pièges

- Pièges transverses : [docs/wiki/Pieges.md](docs/wiki/Pieges.md).
