# Environments

Three environments, one rule: **nothing reaches production that has not
run on the real target device first.**

| Environment | Where | Who deploys | Data |
|---|---|---|---|
| **Development** | localhost | everyone, all the time | fixtures |
| **Staging** | _to choose_ | automatic on `main` | the same fixtures |
| **Production** | _to choose_ | manual, from `main` | the same fixtures |

<!-- Pick the host early. A deployment done in the last week is a
     deployment that fails in the last week. -->

## Development

```bash
```

<!-- The exact commands, plus the traps of this machine: the service
     that must be running, the version that must match, the tool that
     needs a flag. -->

**Testing on a real device from your machine**: same network, bind the
server to `0.0.0.0`, open the machine's local IP on the device. Some
things — gestures, safe areas, viewport height — cannot be validated
anywhere else.

## Staging

Deployed automatically from `main`, so that "it works on my machine" is
never the last word. Same data as production: with a small fixture set,
there is no reason for the two to diverge.

## Production

Deployed manually, from `main`, by the tech lead. Never on demo day
morning: the freeze is the day before.

Checklist: [`GO_LIVE.md`](GO_LIVE.md).

## Environment variables

| Variable | Dev | Staging | Prod |
|---|---|---|---|
| | | | |

See [`SECRETS.md`](SECRETS.md).
