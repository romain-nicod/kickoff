# Operations — the maintenance page and the monitoring

🔴 **Every site has both before its first production deployment.** Romain's rule, 27/09/2026. A
visitor never meets a raw `502`, and Romain never learns from a reader that the site is down.

Both are delivered as the two stories created at kickoff (see the `project-kickoff` skill, § 5).
The deployment pull request that first reaches production checks they are done.

---

## 1. The maintenance page

### One page, one file

[`public/maintenance.html`](../public/maintenance.html): self-contained (no stylesheet, script or
image to fetch), in the language of the product's readers, readable on a phone, light and dark, a
contact, and a reload every 30 s so the site comes back on its own. Whatever serves it answers
**`503` with `Retry-After`**, so search engines do not index it. A static site moves the file to
the root it serves; it stays **one** file whichever path serves it.

### The cases it covers

Numbered once, here; a project's story refers to these numbers.

| Case | Situation | What serves the page |
|---|---|---|
| **A1** | A deployment: the application restarts | the edge, or the local proxy |
| **A2** | Voluntary maintenance: a restore, a long migration | the same, switched on by a flag file |
| **A3** | The application is down or hangs | the same, after a timeout |
| **A4** | The application answers **`500`** | **nobody — on purpose.** A `500` is a failure to repair, not maintenance; dressing it up would hide it. The application's own error page stays |
| **A5** | The local proxy itself is down | the edge, or the service worker |
| **B1** | The host is off, asleep or rebooting | the edge, or the service worker |
| **B2** | The host's network is cut | the edge, or the service worker |
| **B3** | The tunnel or VPN agent on the host is down | the edge, or the service worker |
| **B4** | The tunnel provider has an outage | the service worker only |
| **B5** | Host down, on a device that never visited the site | the edge only |

### Who serves it, by exposure

**Behind Cloudflare** — a Worker on the site's route fetches the origin and returns the page when
the origin fails to answer or answers `502`, `503`, `504` or a Cloudflare `52x`/`530` (a tunnel
with no connector). The edge answers even when the host is off: **one mechanism covers A1–A3,
A5 and B1–B3, and B5.** The page's content is bundled into the Worker from `public/maintenance.html`
at deploy time, never copied by hand. ⚠️ The exact status a dead tunnel returns to a Worker is to
be observed in recette before the rule is trusted.

**Without an edge** (Tailscale Funnel, a box port, a VPS without a relay) — two pieces:

- **the local reverse proxy** serves the page when the application does not answer (A1–A3), and on
  a flag file (A2). Its restart policy is `always`: it becomes a link of the chain;
- **a service worker**, installed on the first visit, caches **this page and nothing else**, and
  shows it when the network does not answer or answers `502`/`503`/`504`, with a timeout of a few
  seconds (A5, B1–B4). It never caches a page behind a login, it survives a sign-out, and a version
  that uninstalls itself is written and tried before the first one ships.
- **B5 stays uncovered.** Say so in the project's story, not later.

Reference implementation: PEF Blog, `romain-nicod/site-pef-blog` #333 (local proxy) and #368
(service worker); case map in the vault note `PEF Blog - Cadrage page de maintenance - 20260915`.

---

## 2. The monitoring

🔴 **A monitor running on the host cannot report the host's death.** On-host dashboards (Uptime
Kuma and the like) are a complement, never the monitoring. On Romain's servers, three incidents
out of seven were found by chance, one after eleven hours; and a machine found off turned out,
after two and a half hours of diagnosis, to have been unplugged on purpose. **An outside monitor
does not only detect a failure: it qualifies a silence.**

Four services, each one named in the project's `AGENTS.md` (*Operations* line):

| # | Service | What it watches | Where it runs |
|---|---|---|---|
| **M1** | **External probe** | `GET /up` on the **public name**, every 5 min at most; alert after two consecutive failures, and when it comes back | outside the host and outside its network |
| **M2** | **Heartbeat** (dead man's switch, healthchecks.io) | each scheduled piece of work pings on success: backups, the job worker, nightly jobs. No ping in time = alert | the host pings; the alert comes from outside |
| **M3** | **Errors** — Sentry (`SENTRY_DSN`) | exceptions of the application, server side and browser side | the application |
| **M4** | **Expiry** | the TLS certificate (when the project renews it) and the domain name | the probe of M1, or the registrar's reminders to a read address |

Rules:

- **One named recipient** per alert, on a channel read while travelling. An alert sent to an
  address nobody reads is not monitoring.
- 🔴 **Each alert is fired once, on purpose, before the go-live**: stop the application for M1,
  withhold one ping for M2, raise a test exception for M3. **A monitor that never fired is a
  hypothesis.** The date of each test goes in the deployment pull request.
- The probe reads the **public** name, from outside: a check on `127.0.0.1` proves the process
  lives, not that readers reach it.
- A maintenance on purpose (A2) pauses M1 first, or it will page for nothing — and a monitor that
  cries wolf gets muted.

---

## 3. Before the first production deployment

- [ ] `public/maintenance.html` carries the real contact; `scripts/check_placeholders.py` passes
- [ ] A1 seen: the page shown during a real deployment, with `503` and `Retry-After`
- [ ] B1 seen, or B5 written down as uncovered: the host (or the tunnel) stopped on purpose
- [ ] A4 seen: a `500` still shows the application's error page, not the maintenance page
- [ ] M1 to M4 in place, each one named in `AGENTS.md`, each alert fired once and received
