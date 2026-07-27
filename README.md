# League Counter Pick — Beta Testing

Mobile-friendly League of Legends counter-pick guide. Search any enemy champion and get counter picks, ability tips, and laning advice.

**Example:** Search **Garen** → learn that his **E (Judgment)** spin ramps damage the longer you stay inside it, plus which champions counter him.

---

## Quick Start

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API key

Your Riot API key is stored in `.env` (already configured for beta testing).

Development keys expire every **24 hours** — regenerate at https://developer.riotgames.com/ and update `RIOT_API_KEY` in `.env`.

> **Note:** The counter-pick app uses Data Dragon for champion data and does **not** require an API key to run. The key is included for future features (match history, personal stats).

### 3. Start the app

**Option A — Double-click:**
`scripts\start-counter-app.bat`

**Option B — Command line:**
```bash
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Open in browser

- **PC:** http://127.0.0.1:8000
- **Phone (same Wi‑Fi):** http://YOUR-PC-IP:8000

Find your PC IP: run `ipconfig` in Command Prompt, look for IPv4 Address.

### 5. Install on phone (PWA)

- **Android (Chrome):** Menu → Add to Home screen
- **iPhone (Safari):** Share → Add to Home Screen

---

## What to Test (Beta Checklist)

- [ ] App loads on phone browser
- [ ] Search finds champions (try "Garen", "Yas", "Lux")
- [ ] Popular matchups grid works
- [ ] Garen guide shows counter picks (Vayne, Quinn, Teemo…)
- [ ] Garen E ability tip explains spin damage ramp
- [ ] Back button returns to search
- [ ] Champions without curated guides still show ability data
- [ ] PWA installs to home screen
- [ ] Works on same Wi‑Fi from phone

**Champions with full curated guides:**
Garen, Darius, Yasuo, Lux, Zed, Ahri, Mordekaiser, Sett, Thresh, Jinx

---

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/health` | Server status |
| `GET /api/champions` | List all champions |
| `GET /api/champions?search=garen` | Search champions |
| `GET /api/counter/Garen` | Full counter guide |

---

## Project Structure

```
league app beta testing/
├── api/main.py              # FastAPI server
├── src/counters/
│   ├── ddragon.py           # Champion data from Data Dragon
│   └── matchup_db.py        # Loads curated guides
├── data/counters/
│   └── matchups.json        # Counter picks & ability tips
├── web/static/
│   ├── index.html           # Mobile UI
│   ├── app.js
│   └── styles.css
├── scripts/start-counter-app.bat
├── .env                       # Your API key (keep private)
└── requirements.txt
```

---

## Adding More Champion Guides

Edit `data/counters/matchups.json`. Each champion entry supports:

- `summary` — overview of the matchup
- `counter_picks` — array of `{ champion, role, reason }`
- `ability_tips` — array of `{ key, name, tip }` (use "THE KEY ABILITY" for emphasis)
- `laning_tips` — bullet list
- `power_spikes` — when they're strongest
- `items_to_consider` — suggested items

Copy the Garen entry as a template.

---

## Roadmap to Public Launch

1. **Beta test** locally and on phone (you are here)
2. **Add more champions** to matchups.json
3. **Deploy** to a domain (Render, Railway, Vercel)
4. **Add** Terms of Service + Privacy Policy pages
5. **Verify domain** with Riot (`riot.txt` file)
6. **Apply** for Production API key at developer.riotgames.com
7. **Optional:** Wrap as native app (Expo/Capacitor) for App Store / Play Store

See `RIOT-API-NOTES.md` for Production key requirements.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Can't connect from phone | Use PC IP not 127.0.0.1; check firewall allows port 8000 |
| `pip` not found | Install Python from python.org, check "Add to PATH" |
| Champions not loading | Check internet — app fetches from Data Dragon CDN |
| API key errors | Regenerate key at developer.riotgames.com, update `.env` |

---

## Legal

League Counter Pick is not endorsed by Riot Games. League of Legends and Riot Games are trademarks of Riot Games, Inc.
