# Beta Testing Guide

## Test on Your Phone

1. Start the app on your PC (see README.md)
2. Find your PC's IP address:
   ```
   ipconfig
   ```
   Look for **IPv4 Address** (e.g. `192.168.1.105`)
3. On your phone browser, go to: `http://192.168.1.105:8000`
4. Add to home screen for app-like experience

---

## Test Scenarios

### Scenario 1: Garen Top Lane
1. Open app
2. Tap **Garen** in Popular Matchups
3. Verify you see:
   - Counter picks: Vayne, Quinn, Teemo, Kayle, Darius
   - E (Judgment) tip about spin damage ramping
   - Laning tips about walking out of spin
   - Items: Bramble Vest, Steelcaps

### Scenario 2: Search Any Champion
1. Type "yas" in search
2. Tap Yasuo
3. Verify wind wall and tornado tips appear

### Scenario 3: Uncurated Champion
1. Search a champion NOT in the curated list (e.g. "Ornn")
2. Verify ability descriptions still load from Data Dragon
3. Note: fewer matchup tips — this is expected for v1

### Scenario 4: Back Navigation
1. Open any guide
2. Tap "← Back to search"
3. Verify search screen returns

---

## Report Issues

When reporting bugs, include:
- Phone model and browser (Chrome/Safari)
- Champion searched
- What you expected vs what happened
- Screenshot if possible

---

## Suggested Improvements to Test For

- [ ] Is text readable on your phone screen?
- [ ] Are ability tips actually useful in-game?
- [ ] Which champions do you face most that are missing guides?
- [ ] Would you use this during champ select?
- [ ] Is anything confusing or missing?

---

## Champions Needing Guides Next

Priority suggestions based on common matchups:
- Renekton, Camille, Fiora, Irelia (top lane)
- Katarina, Syndra, Orianna (mid)
- Draven, Caitlyn, Kai'Sa (ADC)
- Nautilus, Leona, Morgana (support)
- Lee Sin, Kha'Zix, Hecarim (jungle)

Add these by editing `data/counters/matchups.json`.
