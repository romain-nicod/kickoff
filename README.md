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
     docs/decisions/ as ADRs. -->

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
```

## 8. Deployment

<!-- Host, mechanism (automatic on main or manual), and the first-time
     setup steps. Filled in with the first deployment, in the same
     commit. -->

## 9. Project tracking

- **[Issues](https://github.com/{{REPO}}/issues)** — one per user story,
  titled `US-nnn — …`, labelled by epic, priority, batch and complexity.
  Each is a sub-issue of its epic.
- **[Milestones](https://github.com/{{REPO}}/milestones)** — the delivery
  batches.
- **Board** — Status, Batch, Points, MoSCoW Priority, Route. Its fields
  are filled from the labels, so the labels are the source.
- **[Labels](docs/LABELS.md)** — six families, `family:value`, and the
  rule that decides whether a thing deserves a label at all.

The repository itself is configured by script too — labels (ours created,
GitHub's stock set deleted), wiki, pull-request settings, protected
default branch:

```bash
python3 scripts/setup_repo.py
```

Issues are **generated from the specification**, never typed by hand:

```bash
python3 scripts/build_backlog.py       # spec → scripts/backlog.json
python3 scripts/create_issues.py       # labels, milestones, stories
python3 scripts/create_epic_issues.py  # epics + sub-issue links
python3 scripts/setup_project.py       # board and its fields
```

If an acceptance criterion must change, it changes in the specification
first, then the scripts are re-run. Stories discovered along the way are
opened from the issue template **and** added to the specification —
see [`docs/BACKLOG.md`](docs/BACKLOG.md).

**Capacity:** {{DEV_DAYS}} development days × {{TEAM_SIZE}} people ×
{{VELOCITY}} points = **{{CAPACITY}} points**. Measure the real velocity
at the end of week one and re-run that line — it is the only number that
changes the plan.

## 10. Working framework

The method is set up before the code, not after.

| Axis | Document |
|---|---|
| **Engineering** | [`CONTRIBUTING.md`](CONTRIBUTING.md) · [`docs/ENVIRONMENTS.md`](docs/ENVIRONMENTS.md) · [`docs/CODE_HYGIENE.md`](docs/CODE_HYGIENE.md) · [`docs/TESTS.md`](docs/TESTS.md) · [`docs/SECRETS.md`](docs/SECRETS.md) |
| **Delivery** | [`docs/BOARD.md`](docs/BOARD.md) · [`docs/BACKLOG.md`](docs/BACKLOG.md) · [`docs/MILESTONES.md`](docs/MILESTONES.md) · [`docs/DEMO.md`](docs/DEMO.md) |
| **Quality** | [`GOLDEN_RULES.md`](GOLDEN_RULES.md) · [`DOR_DOD.md`](DOR_DOD.md) · [`docs/QUALITY.md`](docs/QUALITY.md) · [`docs/NAMING.md`](docs/NAMING.md) |
<!-- team-only -->
| **Team** | [`ROLES.md`](ROLES.md) · [`TEAM_CHARTER.md`](TEAM_CHARTER.md) · [`CEREMONIES.md`](CEREMONIES.md) · [`docs/STANDUP.md`](docs/STANDUP.md) · [`docs/ONBOARDING.md`](docs/ONBOARDING.md) |
<!-- /team-only -->
| **Launch** | [`docs/GO_LIVE.md`](docs/GO_LIVE.md) |
| **Product** | [`docs/PRD.md`](docs/PRD.md) · [`docs/specification.md`](docs/specification.md) · [`docs/SCENARIOS.md`](docs/SCENARIOS.md) |
| **Prompts** | [`docs/PROMPTS.md`](docs/PROMPTS.md) — one prompt per design deliverable, each with what to check in the answer |
| **Boilerplate** | [`docs/BOILERPLATE.md`](docs/BOILERPLATE.md) — `rails-ready`, our Rails template, and what it decides for you |
| **Architecture** | [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) · [`docs/SCHEMA.md`](docs/SCHEMA.md) · [`docs/decisions/`](docs/decisions/) |
| **Documentation** | [`AGENTS.md`](AGENTS.md) · [`docs/SYSTEM_DESIGN.md`](docs/SYSTEM_DESIGN.md) · [`docs/WIKI.md`](docs/WIKI.md) |

Four before writing a line of code: `GOLDEN_RULES.md` for how we write,
`AGENTS.md` for what this product forbids, `DOR_DOD.md` for when a story
starts and ends, `CONTRIBUTING.md` for how a change reaches `main`.

Two Claude skills are installed in `.claude/skills/` — `methode-projet`
(which deliverable now, who validates it) and `methode-wagon` (how the
code is written here). Any session opened in this repository picks them
up with no setup. They are versioned with the project; they come from
the `kickoff` template, which is authoritative for them.

## 11. Licence

<!-- State it explicitly. "All rights reserved", MIT, dual — implicit is
     the one thing it must not be. -->
