# {{PROJECT_NAME}}

**Live** — not deployed yet. This line carries the URL and its access
caveats from the first deployment on. It is the first thing a reader
needs; it does not belong at the bottom of the page.

{{TAGLINE}}

---

## 1. What the product does

<!-- Three to five lines. Who it serves, what problem it solves. Not the
     list of technologies — the value. If you cannot write it without
     naming a framework, the product is not defined yet. -->

## 2. How it works

<!-- The main user journey, in numbered steps. This is the section that
     lets someone pick the project up six months later. -->

1.
2.
3.

## 3. Stack

| Layer | Technology |
|---|---|
| Application | |
| Database | |
| Front end | |
| Quality | |

## 4. Structural decisions

<!-- The choices you would not guess by reading the code and would risk
     breaking. Each one in a line, with its reason. The detail goes in
     docs/wiki/ as ADR pages. -->

-
-

## 5. Running it locally

Requirements: <!-- exact versions, and the traps of this machine -->

```bash
git clone git@github.com:{{REPO}}.git
cd {{REPO_NAME}}
cp .env.example .env   # then fill in your own values — see section 6
```

<!-- The application skeleton comes from `rails-ready`, our Rails
     template — see docs/BOILERPLATE.md for the exact command and what
     it decides. If you did not use it, say why under section 4. -->

## 6. Environment variables

| Variable | Required | Use |
|---|---|---|
| | | |

🔴 **Every key lives in `.env`, and `.env` is never pushed** (golden rule
28). One mechanism, no exception. `.env.example` carries the same
variable names with empty values and is updated **in the same commit** as
any new variable. In production there is no `.env`: the values are the
host's secrets. See [`docs/SECRETS.md`](docs/SECRETS.md).

## 7. Tests and quality

```bash
bin/rails test
bin/rails test:system
bin/rubocop
bin/brakeman --no-pager
bundle exec bundler-audit --update
bin/importmap audit
```

The CI runs all of them on every pull request. See [`docs/TESTS.md`](docs/TESTS.md).

## 8. Deployment

<!-- Host and deployment script, filled in with the first deployment, in
     the same commit. -->

Every production deployment has its `[Déploiement] vX.Y.Z` pull request,
merged last in its batch, then its GitHub release: the
[releases](https://github.com/{{REPO}}/releases) are the deployment log.
See [`docs/DEPLOIEMENT.md`](docs/DEPLOIEMENT.md) and
[`CHANGELOG.md`](CHANGELOG.md).

## 9. Project tracking

The project follows the delivery method by user story — see
[`AGENTS.md`](AGENTS.md).

- **[Issues](https://github.com/{{REPO}}/issues)** — `[US]` and `[BUG]`,
  reviewed by Romain, and `[Task]` as their sub-issues, on the templates
  of `.github/ISSUE_TEMPLATE/`.
- **Board** — `Backlog · Ready · In progress · En recette · In review ·
  À déployer · Done`. See [`docs/BOARD.md`](docs/BOARD.md).
- **[Labels](docs/LABELS.md)** — `type:user-story`, `Task`, `type:bug`,
  `à revoir par Romain`, `status:blocked`.
- **[Wiki](https://github.com/{{REPO}}/wiki)** — delivered stories,
  architecture, decisions, written in `docs/wiki/`. See
  [`docs/WIKI.md`](docs/WIKI.md).

The repository and the board are configured by script:

```bash
python3 scripts/setup_repo.py
python3 scripts/setup_project.py       # needs: gh auth refresh -s project
```

## 10. Working framework

| Axis | Document |
|---|---|
| **Delivery** | [`AGENTS.md`](AGENTS.md) · [`docs/BOARD.md`](docs/BOARD.md) · [`docs/LABELS.md`](docs/LABELS.md) · [`docs/RECETTE.md`](docs/RECETTE.md) · [`docs/DEPLOIEMENT.md`](docs/DEPLOIEMENT.md) · [`docs/WIKI.md`](docs/WIKI.md) |
| **Engineering** | [`CONTRIBUTING.md`](CONTRIBUTING.md) · [`docs/ENVIRONMENTS.md`](docs/ENVIRONMENTS.md) · [`docs/CODE_HYGIENE.md`](docs/CODE_HYGIENE.md) · [`docs/TESTS.md`](docs/TESTS.md) · [`docs/SECRETS.md`](docs/SECRETS.md) |
| **Quality** | [`GOLDEN_RULES.md`](GOLDEN_RULES.md) · [`docs/QUALITY.md`](docs/QUALITY.md) · [`docs/NAMING.md`](docs/NAMING.md) |
| **Product** | [`docs/PRD.md`](docs/PRD.md) · [`docs/PROMPTS.md`](docs/PROMPTS.md) — one prompt per deliverable, each with what to check in the answer |
| **Architecture** | [`docs/wiki/Architecture.md`](docs/wiki/Architecture.md) · [`docs/SCHEMA.md`](docs/SCHEMA.md) · [`docs/wiki/Decisions.md`](docs/wiki/Decisions.md) · [`docs/SYSTEM_DESIGN.md`](docs/SYSTEM_DESIGN.md) |
| **Boilerplate** | [`docs/BOILERPLATE.md`](docs/BOILERPLATE.md) — `rails-ready`, our Rails template, and what it decides for you |

Three before writing a line of code: `AGENTS.md` and the method it links
to, `GOLDEN_RULES.md` for how we write, `CONTRIBUTING.md` for the diff.

## 11. Licence

<!-- State it explicitly. All rights reserved, MIT, CC BY, dual: implicit is
     the one thing it must not be. A repository with no LICENSE file grants
     nobody anything, whatever the README says, and that surprises people
     who assumed public meant reusable. -->
