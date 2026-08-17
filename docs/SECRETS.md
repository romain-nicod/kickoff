# Secrets

**No secret ever enters Git.** Not in a commit, not in a comment, not in
a fixture, not "temporarily to test the deploy".

## Where they live

| Secret | Development | Staging / production |
|---|---|---|
| | local file, gitignored | host secret |

Check `.gitignore` before adding anything new;
`git check-ignore -v <file>` answers in one line.

## `.env.example`

`.env.example` is versioned and lists every variable the app can read,
with no real value. When you add a variable, add it there **in the same
commit** — that file is how the next person finds out it exists.

```bash
cp .env.example .env   # then fill in your own values
```

## Sharing them

Out of band: a password manager, not the team chat, not an email, not a
commit. Whoever sets up the host puts the value in the host's secrets
and tells the others **where it lives**, never what it is.

## If a secret leaks

Immediately, in this order:

1. **Revoke and rotate** at the provider. A key in a Git history is
   compromised — even in a private repository, even after a force push.
2. Replace it in the host's secrets.
3. Then, and only then, consider cleaning the history.

Rotating first is the whole point: history rewriting is slow and
imperfect, revocation is instant and total.

## What is not a secret

Reference data, design tokens, the specification. They live in the
repository on purpose. A private repository is private for intellectual
property, not because it holds credentials — and that distinction is
what keeps the real secrets outside of it.
