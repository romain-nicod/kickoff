# Public exposure

How production is reached from the Internet. **Default: a Cloudflare Tunnel**, for every new
project. Decided 27/09/2026.

## The default

The domain is registered and served by Cloudflare. `cloudflared` runs on the production host,
opens an **outbound** connection to Cloudflare, and forwards to the app on `127.0.0.1`.

- No inbound port on the router, the host's address never published, an IP change or CGNAT is
  invisible. The host can sit in an empty house for a year.
- The certificate is Cloudflare's, renewed by Cloudflare: no ACME quota, no DNS-01 token.
- Free plan protections come with it: DDoS mitigation, managed WAF rules, custom and
  rate-limiting rules, Bot Fight Mode, DNSSEC, and Cloudflare Access (Zero Trust, free up to
  50 users) to put a login in front of `/admin` or of the whole site.

## What it costs, stated plainly

🔴 **Cloudflare terminates TLS.** The traffic is readable at its edge before being re-encrypted
into the tunnel. Private content, photos included, crosses a third party in clear. Accepted as
the default; a project whose brief forbids it says so and takes an exception below.

⚠️ **Private responses must say so.** Anything behind a login is served `Cache-Control:
private` (or `no-store`), otherwise the CDN may keep a copy. Check it with `curl -sI` on the
public name, not in the tests.

## Exceptions — only for these two reasons

| Reason | Why the tunnel does not fit | What to write down |
|---|---|---|
| **Weight** | the free and Pro plans cap a request body at **100 MB** (`413` above), and the CDN terms target sites serving mostly non-HTML (video, large image or file hosting) | the largest single request the app accepts, and the monthly volume served |
| **Licence** | the terms of the content, of a client or of a dependency forbid a third party from decrypting or caching it | the clause, quoted, and its source |

Any other reason is not an exception. An exception is written in the project's `AGENTS.md` with
the route chosen instead.

## Rails side

- `config.hosts` lists the public name: `cloudflared` forwards the `Host` header untouched, and
  HostAuthorization answers `403` to a name it does not know.
- `config.assume_ssl = true` and `config.force_ssl = true`: TLS ends before the app.
- The tunnel reaches the app from `127.0.0.1`; the real client address arrives in
  `X-Forwarded-For` and `CF-Connecting-IP`. Trust only the loopback as a proxy, or rate limits
  key on a header the client wrote.

## Setting it up

Run on the production host. The login is Romain's: it prints a URL he opens on his own machine.

```bash
cloudflared tunnel login
cloudflared tunnel create <project>
cloudflared tunnel route dns <project> <domain>
```

Then `~/.cloudflared/config.yml` (tunnel id, credentials file, one `ingress` rule to
`http://127.0.0.1:<port>` and a final `http_status:404`), and a service that starts at boot
without a logged-in session. Check from **outside** the host: `curl -sI https://<domain>/up`.
