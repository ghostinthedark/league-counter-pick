# Riot API Notes — Production Key Path

## Key Types

| Key Type | Use Case | Rate Limit | Expires? |
|----------|----------|------------|----------|
| **Development** | Local testing only | Low | Every 24 hours |
| **Personal** | Private/small group only | 20/sec, 100/2min | No |
| **Production** | Public apps for everyone | 500/10sec, 30k/10min | No |

**You cannot launch a public app with a Development or Personal key.**

---

## What Riot Requires for Production Key

1. **Working prototype** — live site users can try (not just GitHub code)
2. **Your own domain** — e.g. `yourapp.com`
3. **Domain verification** — upload `riot.txt` to `https://yourdomain.com/riot.txt`
4. **Terms of Service** — public page on your site
5. **Privacy Policy** — public page on your site
6. **Secure API key** — key on backend only, never in mobile app code

Riot will **not** accept GitHub repos instead of a live website.

---

## Application Process

1. Go to https://developer.riotgames.com/
2. Click **Register Product**
3. Choose Production (for public) or Personal (for private beta with friends only)
4. Fill out the form describing your counter-pick app
5. Host app on your domain and verify ownership
6. Wait for Developer Relations review

**What Riot likes:**
- Apps that help players improve
- Counter-pick guides, stat trackers, coaching tools
- Polished, complete user experience

**What Riot rejects:**
- Apps that "solve" the game or automate decisions
- Incomplete or low-quality products
- Missing ToS/Privacy Policy

---

## Current App: API Key Usage

The **Counter Pick app v1** uses **Data Dragon** (Riot's free static data CDN) for champion names, icons, and ability descriptions. **No API key is required** for the current features.

Your `.env` API key is saved for planned features:
- Personal match history sync
- LP tracking
- Champion performance stats from your account

When you add those features, the key must stay on the **server** (in `.env`), never in the frontend JavaScript.

---

## Regenerating Your Development Key

Development keys expire every 24 hours:

1. Log in to https://developer.riotgames.com/
2. Copy the new key from your dashboard
3. Update `RIOT_API_KEY` in `.env`
4. Restart the server

---

## Free Deployment Options (for Production application)

| Service | Use For | Cost |
|---------|---------|------|
| Render.com | Python API backend | Free tier |
| Railway.app | Python API backend | Free tier |
| Vercel / Netlify | Static frontend | Free |
| Namecheap / Cloudflare | Domain name | ~$10-15/year |

After deploy, add `riot.txt` verification file to your domain root.

---

## Store Publishing Costs (Optional Later)

| Store | Cost |
|-------|------|
| Google Play | ~$25 one-time |
| Apple App Store | ~$99/year |
| PWA (home screen install) | $0 |

PWA is the free path — users install from browser without app store fees.
