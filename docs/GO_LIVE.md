# Go-live checklist

Run it the **day before** the demo, not the morning of.

## Before deploying

- [ ] `main` is green in CI
- [ ] Feature freeze declared: no merge after this point except a
      Blocker fix
- [ ] Linter and tests pass locally too
- [ ] Security scan shows no new warning
- [ ] No secret in the diff — one last look before it is public

## Deploying

- [ ] Secrets set in the host's configuration
- [ ] Migrations run on release
- [ ] Reference data loaded once, and verified by a count
- [ ] The health check answers: `curl -sI https://<host>/up` → 200

## Smoke test, on the real device

Not on a desktop browser.

- [ ] The main journey, end to end, as a first-time user
- [ ] The permission the app needs, refused: the journey still works
- [ ] Offline or degraded network: a message, not a blank screen
- [ ] The screen in the real conditions of use — light, motion, one hand

## Rollback

The plan is one command, known before it is needed:

```bash
git revert <sha> && git push origin main
```

Plus the host's own "redeploy previous version" button. **Find it and
write its exact location here before the demo:**

> _to fill in_

## Monitoring, the minimum that is worth it

- A health check hit by the host
- The host's logs, open in a tab during the demo
- One person watching them: the QA & demo owner

Anything more elaborate is a distraction at this scale. What matters is
knowing within ten seconds whether a failure is the app, the network or
a third party.
