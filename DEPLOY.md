# Deploy Counter Pick for FREE

Your app will live at: **`https://league-counter-pick.onrender.com`** (or similar)

No credit card required. No custom domain purchase needed for beta/Riot verification.

---

## What "free domain" means

| Option | Cost | Example |
|--------|------|---------|
| **Render subdomain** | $0 | `league-counter-pick.onrender.com` |
| **Custom .com domain** | ~$10–15/year | `counterpick.gg` |

For Riot Production API verification, the free `onrender.com` URL works — you upload `riot.txt` to your app root.

**Trade-off:** Free Render apps sleep after 15 min idle. First visit after sleep takes ~30–60 seconds to wake up.

---

## Step 1 — Push code to GitHub (one time)

### A. Create a GitHub account
Go to https://github.com/signup if you don't have one.

### B. Create a new repository
1. Go to https://github.com/new
2. Name: `league-counter-pick`
3. Set to **Public**
4. Do NOT add README (we already have one)
5. Click **Create repository**

### C. Push this folder to GitHub

Open **Command Prompt** in this folder and run:

```bat
cd "C:\Users\Michael\OneDrive\Documents\league app beta testing"
git init
git add .
git commit -m "Initial counter pick app for deployment"
git branch -M main
git remote set-url origin https://github.com/ghostinthedark/league-counter-pick.git
git push -u origin main
```

If `origin` is not set yet, use `git remote add origin ...` instead of `set-url`.

---

## Step 2 — Deploy on Render (free)

1. Go to https://dashboard.render.com/register and sign up (use "Sign in with GitHub")
2. Click **New +** → **Blueprint**
3. Connect your `league-counter-pick` GitHub repo
4. Render reads `render.yaml` automatically — click **Apply**
5. Wait 2–5 minutes for deploy to finish
6. Your live URL appears at the top (e.g. `https://league-counter-pick.onrender.com`)

**Test it:** Open the URL on your phone. Search "Garen".

---

## Step 3 — Riot verification (when ready)

1. Register product at https://developer.riotgames.com/
2. Riot gives you a verification string
3. Edit `web/static/riot.txt` — paste ONLY the string, save, push to GitHub
4. Render auto-redeploys in ~2 min
5. Verify at `https://YOUR-URL.onrender.com/riot.txt`
6. Submit your Production API key application

---

## Environment variables (optional, on Render dashboard)

The counter-pick app works without any env vars. Add these later if you add match history features:

| Key | Value |
|-----|-------|
| `RIOT_API_KEY` | Your key from developer.riotgames.com |
| `RIOT_GAME_NAME` | Your summoner name |
| `RIOT_TAG_LINE` | Your tag (e.g. NA1) |

**Never commit `.env` to GitHub** — it's already in `.gitignore`.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| App slow first load | Normal on free tier — server was sleeping |
| Build failed | Check Render logs; ensure `requirements.txt` exists |
| 404 on champions | Wait for cold start to finish, refresh |
| Git push rejected | Create repo on GitHub first, check username in remote URL |

---

## Upgrade later (optional)

- **$7/mo Render Starter** — always on, no sleep
- **Custom domain** — buy from Namecheap/Cloudflare, point DNS to Render
