# Environments

Four environments, and no shared staging: the local recette environment stands in for it.

| Environment | Where | Port | Data | Who puts code there |
|---|---|---|---|---|
| Development | `code/{{REPO_NAME}}/` and one worktree per story, `code/{{REPO_NAME}}-worktrees/us-NNN-slug/` | `3000` (another port per worktree running at the same time) | fixtures and seeds | the story's session, on its branch |
| Test | the worktree's `test` database, then CI | — | fixtures | `bin/rails test`, `bin/rails test:system` |
| Recette | `code/{{REPO_NAME}}-recette/`, local `recette` branch | `3100` | synthetic only | the agent merges the *En recette* stories there; Romain tests there — [RECETTE.md](RECETTE.md) |
| Production | <!-- host and URL --> | — | real | the deployment script, on the merge commit of the `[Déploiement]` pull request — [DEPLOYMENT.md](DEPLOYMENT.md) |

## Development

```bash
bin/setup
bin/rails server    # http://127.0.0.1:3000
```

<!-- The traps of this machine: the service that has to be running, the version that has to match,
     the tool that needs an option. -->

## Variables that change from one environment to the next

| Variable | Development | Recette | Production |
|---|---|---|---|
| `SENTRY_DSN` | empty | removed by `bin/recette` | host secret |
| `SMTP_*` | empty: emails kept in memory | Mailpit on `127.0.0.1`, in `.env.recette.local` | Infomaniak relay, host secrets |
| `DATABASE_URL` | — | set by `bin/recette`, one per worktree | host secret |

The names and what they are for: `.env.example`. Where the values live: [SECRETS.md](SECRETS.md).
