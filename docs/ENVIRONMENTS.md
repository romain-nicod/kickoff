# Environnements

Quatre environnements, et pas de préproduction partagée : la recette locale en tient lieu.

| Environnement | Où | Port | Données | Qui y met du code |
|---|---|---|---|---|
| Développement | `code/{{REPO_NAME}}/` et un worktree par US, `code/{{REPO_NAME}}-worktrees/us-NNN-slug/` | `3000` (un autre port par worktree lancé en même temps) | fixtures et seeds | la session de l'US, sur sa branche |
| Test | la base `test` du worktree, puis la CI | — | fixtures | `bin/rails test`, `bin/rails test:system` |
| Recette | `code/{{REPO_NAME}}-recette/`, branche locale `recette` | `3100` | synthétiques uniquement | l'agent y merge les US *En recette* ; Romain y teste — [RECETTE.md](RECETTE.md) |
| Production | <!-- hôte et URL --> | — | réelles | le script de déploiement, sur le commit de merge de la PR `[Déploiement]` — [DEPLOIEMENT.md](DEPLOIEMENT.md) |

## Développement

```bash
bin/setup
bin/rails server    # http://127.0.0.1:3000
```

<!-- Les pièges de cette machine : le service qui doit tourner, la version qui doit correspondre,
     l'outil qui demande une option. -->

## Variables qui changent d'un environnement à l'autre

| Variable | Développement | Recette | Production |
|---|---|---|---|
| `SENTRY_DSN` | vide | retirée par `bin/recette` | secret de l'hôte |
| `SMTP_*` | vide : emails en mémoire | Mailpit sur `127.0.0.1`, dans `.env.recette.local` | relais Infomaniak, secrets de l'hôte |
| `DATABASE_URL` | — | fixée par `bin/recette`, propre au worktree | secret de l'hôte |

Les noms et leur usage : `.env.example`. Où vivent les valeurs : [SECRETS.md](SECRETS.md).
