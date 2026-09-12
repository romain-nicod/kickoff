# Recette locale

La recette est l'endroit où Romain teste les US *En recette* avant de relire leurs PR. La méthode
fait foi (§ 5) ; cette page dit comment elle est installée et tenue dans ce dépôt.

## Le modèle

| | Développement | Recette |
|---|---|---|
| Dossier | `code/{{REPO_NAME}}/` | `code/{{REPO_NAME}}-recette/`, worktree du clone principal |
| Branche | `main`, ou `us-NNN-slug` dans un worktree d'US | `recette`, **locale**, reconstruite à chaque lot |
| Port | `3000` | `3100`, sur `127.0.0.1` uniquement |
| Données | fixtures, seeds | synthétiques uniquement, base propre au worktree |
| Emails | en mémoire | capturés par Mailpit, jamais envoyés |

**L'agent peut merger dans `recette`, jamais dans `main`.** La branche `recette` n'est jamais poussée
ni mergée ailleurs.

## Côté Romain

Ouvrir `code/{{REPO_NAME}}-recette/` dans VS Code, puis dans son terminal :

```bash
bin/recette start
```

L'adresse, la branche et le commit testés s'affichent : http://127.0.0.1:3100. Ctrl+C arrête le
serveur.

## Côté agent

**Création, une fois**, depuis le clone principal :

```bash
git -C code/{{REPO_NAME}} fetch origin
git -C code/{{REPO_NAME}} worktree add -b recette ../{{REPO_NAME}}-recette origin/main
```

**À chaque lot**, serveur de recette arrêté :

```bash
git -C code/{{REPO_NAME}}-recette status --porcelain    # doit être vide, sinon s'arrêter
git -C code/{{REPO_NAME}}-recette fetch origin
git -C code/{{REPO_NAME}}-recette switch recette
git -C code/{{REPO_NAME}}-recette reset --hard origin/main
git -C code/{{REPO_NAME}}-recette merge --no-ff origin/us-012-refuse-double-vote
bin/recette prepare                                      # lancé depuis code/{{REPO_NAME}}-recette
```

⚠️ `reset --hard` efface les merges de la recette précédente, et eux seuls : ils se refont depuis les
branches d'US. Il ne touche ni `main` ni une branche d'US. Un conflit de merge arrête la
reconstruction : le résoudre dans la branche de l'US, jamais dans `recette`.

Puis écrire dans le board, sur chaque US intégrée, la liste exacte présente en recette :

```bash
git -C code/{{REPO_NAME}}-recette log --oneline origin/main..recette
```

## Installation dans l'application — une fois

Le stack Rails fournit `bin/recette`, `lib/recette.rb` et `test/lib/recette_test.rb`. `lib/recette.rb`
refuse une base externe, une écoute hors de `127.0.0.1`, un port invalide et un relais d'emails qui
ne serait pas sur ce Mac ; il retire de l'environnement les secrets de production, `SMTP_*`,
`SENTRY_*` et `PG*` ; il génère `.env.recette.local` (mode 600, ignoré par Git) avec un
`SECRET_KEY_BASE` propre au worktree.

Il reste quatre fichiers à compléter dans l'application.

`config/environments/recette.rb` :

```ruby
require_relative "production"

# Local recette (docs/RECETTE.md): production settings, served over HTTP on
# this Mac's loopback, with a synthetic database and captured emails.
Rails.application.configure do
  config.assume_ssl = false
  config.force_ssl = false
  config.hosts = [ "127.0.0.1" ]
  config.host_authorization = {}
  config.active_storage.service = :recette
  config.cache_store = :memory_store
  # Jobs run inside the server process, so an email sent later still
  # reaches Mailpit.
  config.active_job.queue_adapter = :async
  config.action_mailer.default_url_options = {
    host: "127.0.0.1", port: ENV.fetch("PORT"), protocol: "http"
  }
  if ENV["SMTP_ADDRESS"].present?
    # Mailpit on this Mac: it captures everything and relays nothing.
    config.action_mailer.delivery_method = :smtp
    config.action_mailer.smtp_settings = {
      address: ENV.fetch("SMTP_ADDRESS"),
      port: Integer(ENV.fetch("SMTP_PORT", "1025")),
      user_name: ENV["SMTP_USERNAME"], password: ENV["SMTP_PASSWORD"],
      authentication: (ENV["SMTP_USERNAME"].present? ? :plain : nil),
      enable_starttls_auto: false
    }
  else
    config.action_mailer.delivery_method = :test
  end
  config.session_store :cookie_store, httponly: true, same_site: :lax,
    key: "_recette_#{ENV.fetch('RECETTE_ID')}"
  config.x.recette_revision = ENV.fetch("RECETTE_REVISION", "non identifiée")
  config.x.recette_branch = ENV.fetch("RECETTE_BRANCH", "non identifiée")
end
```

Dans `config/database.yml`, `config/cable.yml` et `config/storage.yml` :

```yaml
# config/database.yml
recette:
  <<: *default
  url: <%= ENV["DATABASE_URL"] %>

# config/cable.yml
recette:
  adapter: async

# config/storage.yml
recette:
  service: Disk
  root: <%= Rails.root.join("tmp/recette/storage") %>
```

Les seeds doivent pouvoir tourner sans aucun secret de production : ils créent des comptes et des
contenus fictifs, et affichent comment se connecter sans écrire de mot de passe dans le dépôt.

Facultatif : un bandeau dans le layout qui affiche `Rails.configuration.x.recette_branch` et
`recette_revision` quand `Rails.env.recette?`, pour que Romain sache toujours ce qu'il teste.

## Emails : Mailpit

Mailpit tourne sur le Mac de Romain : SMTP sur `127.0.0.1:1025`, interface sur
http://127.0.0.1:8025, sans aucun relais. Installation, identifiants et arrêt du service : note vault
`dev/outils/Emails - Envoi SMTP Infomaniak et tests Mailpit.md`.

Pour capturer les emails de cette recette, ouvrir `.env.recette.local` dans un éditeur et
décommenter les lignes `SMTP_*`, en recopiant l'identifiant et le mot de passe depuis le fichier de
Mailpit indiqué dans la note. Ne jamais les passer sur la ligne de commande. Sans `SMTP_ADDRESS`, les
emails restent en mémoire (`:test`). Si Mailpit refuse l'authentification sans TLS, voir la note.

## Contrôles

```bash
bin/rails test test/lib/recette_test.rb
```

Les tests automatisés tournent sur leur base `test`, jamais sur la base de recette.

## Limites connues

- HTTP sur la boucle locale : le TLS de production n'est pas testé ici.
- Les jobs tournent dans le processus du serveur ; aucun worker ni tâche récurrente n'est lancé.
- Déplacer le worktree change son identifiant, donc sa base : préparer à nouveau.
