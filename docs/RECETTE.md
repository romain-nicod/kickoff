# Local recette environment

The recette environment is where Romain tests the *En recette* stories before reviewing their pull
requests. The method is authoritative (§ 5); this page says how it is installed and kept in this
repository. The word `recette` stays: it names a branch, a port, a script and a Rails environment.

## The model

| | Development | Recette |
|---|---|---|
| Folder | `code/{{REPO_NAME}}/` | `code/{{REPO_NAME}}-recette/`, a worktree of the main clone |
| Branch | `main`, or `us-NNN-slug` in a story worktree | `recette`, **local**, rebuilt for every batch |
| Port | `3000` | `3100`, on `127.0.0.1` only |
| Data | fixtures, seeds | synthetic only, database private to the worktree |
| Emails | in memory | captured by Mailpit, never sent |

**The agent may merge into `recette`, never into `main`.** The `recette` branch is never pushed, and
never merged anywhere else.

## Romain's side

Open `code/{{REPO_NAME}}-recette/` in VS Code, then in its terminal:

```bash
bin/recette start
```

The address, the branch and the commit under test are printed: http://127.0.0.1:3100. Ctrl+C stops the
server.

## The agent's side

**Creation, once**, from the main clone:

```bash
git -C code/{{REPO_NAME}} fetch origin
git -C code/{{REPO_NAME}} worktree add -b recette ../{{REPO_NAME}}-recette origin/main
```

**For every batch**, with the recette server stopped:

```bash
git -C code/{{REPO_NAME}}-recette status --porcelain    # must be empty, otherwise stop
git -C code/{{REPO_NAME}}-recette fetch origin
git -C code/{{REPO_NAME}}-recette switch recette
git -C code/{{REPO_NAME}}-recette reset --hard origin/main
git -C code/{{REPO_NAME}}-recette merge --no-ff origin/us-012-refuse-double-vote
bin/recette prepare                                      # run from code/{{REPO_NAME}}-recette
```

⚠️ `reset --hard` wipes the merges of the previous recette, and nothing else: they are redone from the
story branches. It touches neither `main` nor a story branch. A merge conflict stops the rebuild:
resolve it in the story's branch, never in `recette`.

Then write on the board, on every story merged in, the exact list of what is on the recette
environment:

```bash
git -C code/{{REPO_NAME}}-recette log --oneline origin/main..recette
```

## Installing it in the application — once

The Rails stack ships `bin/recette`, `lib/recette.rb` and `test/lib/recette_test.rb`. `lib/recette.rb`
refuses an external database, a listener outside `127.0.0.1`, an invalid port and a mail relay that is
not on this Mac; it removes the production secrets, `SMTP_*`, `SENTRY_*` and `PG*` from the
environment; and it generates `.env.recette.local` (mode 600, ignored by Git) with a `SECRET_KEY_BASE`
private to the worktree.

Four files are left to fill in, in the application.

`config/environments/recette.rb`:

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
  config.x.recette_revision = ENV.fetch("RECETTE_REVISION", "unidentified")
  config.x.recette_branch = ENV.fetch("RECETTE_BRANCH", "unidentified")
end
```

In `config/database.yml`, `config/cable.yml` and `config/storage.yml`:

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

The seeds have to run without a single production secret: they create fictional accounts and content,
and print how to sign in without writing a password into the repository.

Optional: a banner in the layout showing `Rails.configuration.x.recette_branch` and
`recette_revision` when `Rails.env.recette?`, so Romain always knows what he is testing.

## Emails: Mailpit

Mailpit runs on Romain's Mac: SMTP on `127.0.0.1:1025`, interface on http://127.0.0.1:8025, with no
relay at all. Installation, credentials and how to stop the service: vault note
`dev/outils/Emails - Envoi SMTP Infomaniak et tests Mailpit.md`.

To capture this recette's emails, open `.env.recette.local` in an editor and uncomment the `SMTP_*`
lines, copying the user name and password from the Mailpit file the note points at. Never pass them on
the command line. Without `SMTP_ADDRESS`, emails stay in memory (`:test`). If Mailpit refuses
authentication without TLS, see the note.

## Checks

```bash
bin/rails test test/lib/recette_test.rb
```

The automated tests run against their own `test` database, never against the recette one.

## Known limits

- HTTP on the loopback: production's TLS is not tested here.
- Jobs run inside the server process; no worker and no recurring task is started.
- Moving the worktree changes its identifier, hence its database: prepare it again.
