# League Counter Pick — Session Summary

Built: July 26, 2026

## Goal

Mobile app for League of Legends that tells you how to counter enemy champions — counter picks, ability warnings, and laning tips.

**Example:** Facing Garen → app explains his E spin ramps damage if you stay close, suggests Vayne/Quinn/Teemo counters.

---

## What's Included in This Folder

Complete working beta of the Counter Pick app:

- FastAPI backend (`api/`)
- Champion data layer (`src/counters/`)
- 10 curated matchup guides (`data/counters/matchups.json`)
- Mobile-first web UI (`web/static/`)
- Start script (`scripts/start-counter-app.bat`)
- API key configured in `.env`

---

## How It Works

```
Phone Browser → FastAPI Server → Data Dragon (champion icons/names)
                               → matchups.json (curated tips)
```

No Riot API key needed for current counter-pick features. Data Dragon is Riot's free public CDN for static game data.

---

## Start Command

```bash
cd "C:\Users\Michael\OneDrive\Documents\league app beta testing"
pip install -r requirements.txt
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

Open http://127.0.0.1:8000

---

## Files Reference

| File | Purpose |
|------|---------|
| `README.md` | Full setup and usage |
| `BETA-TESTING.md` | Test scenarios and checklist |
| `RIOT-API-NOTES.md` | Production API key path |
| `data/counters/matchups.json` | All counter-pick content |
| `.env` | Riot API key + account settings |

---

## Next Steps

1. Beta test on your phone
2. Tell me which champions to add next
3. Deploy to a domain when ready for Riot Production key
4. Add champ-select mode (pick your role + enemy = tailored advice)

---

## Original Project

This app was built inside `league-analytics` and copied here for beta testing. Both folders stay in sync — edit either one, or ask to update both.
