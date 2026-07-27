"""Generate premium matchup guides for all champions using curated knowledge + Data Dragon spell data."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.counters.ddragon import get_champion_detail, list_champions  # noqa: E402

MATCHUP_FILE = ROOT / "data" / "counters" / "matchups.json"

# Curated premium content per champion (excluding the 10 hand-written entries preserved as-is).
# Each entry: summary, counters[(champ, role, reason)], abilities{P/Q/W/E/R: tip}, laning[], spikes[], items[]
GUIDES: dict[str, dict] = {}


def _load_guides_from_module() -> None:
    """Import champion guide data from matchup_knowledge module."""
    global GUIDES
    from scripts import matchup_knowledge  # noqa: WPS433

    GUIDES.update(matchup_knowledge.CHAMPION_GUIDES)


def _build_entry(champ_name: str, champ_id: str, guide: dict, spells: list[dict]) -> dict:
    spell_map = {s["key"]: s["name"] for s in spells}
    ability_tips = []
    for key in ("P", "Q", "W", "E", "R"):
        if key not in spell_map:
            continue
        tip_text = guide.get("abilities", {}).get(key)
        if not tip_text:
            continue
        ability_tips.append({"key": key, "name": spell_map[key], "tip": tip_text})

    counter_picks = [
        {"champion": c[0], "role": c[1], "reason": c[2]}
        for c in guide.get("counters", [])
    ]

    return {
        "summary": guide["summary"],
        "counter_picks": counter_picks,
        "ability_tips": ability_tips,
        "laning_tips": guide.get("laning", []),
        "power_spikes": guide.get("spikes", []),
        "items_to_consider": guide.get("items", []),
    }


def generate() -> dict:
    _load_guides_from_module()
    existing: dict = {}
    if MATCHUP_FILE.exists():
        existing = json.loads(MATCHUP_FILE.read_text(encoding="utf-8"))

    result = dict(existing)
    all_champs = list_champions()
    missing = []
    for champ in all_champs:
        name = champ["name"]
        if name in result:
            continue
        if name not in GUIDES:
            missing.append(name)
            continue
        detail = get_champion_detail(champ["id"])
        result[name] = _build_entry(name, champ["id"], GUIDES[name], detail["spells"])

    if missing:
        print(f"WARNING: {len(missing)} champions missing curated data: {missing[:10]}...")
        raise SystemExit(f"Missing guides for {len(missing)} champions")

    return result


def main() -> None:
    data = generate()
    MATCHUP_FILE.parent.mkdir(parents=True, exist_ok=True)
    MATCHUP_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(data)} champion guides to {MATCHUP_FILE}")


if __name__ == "__main__":
    main()
