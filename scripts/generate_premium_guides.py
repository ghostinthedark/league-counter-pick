"""Generate premium matchup guides for all champions using Data Dragon + curated knowledge."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.counters.ddragon import get_champion_detail, list_champions  # noqa: E402
from src.counters.guide_generator import generate_guide  # noqa: E402

MATCHUP_FILE = ROOT / "data" / "counters" / "matchups.json"

# Hand-written Yasuo-quality guides — never overwrite.
PREMIUM_CHAMPIONS: frozenset[str] = frozenset({
    "Garen",
    "Darius",
    "Yasuo",
    "Lux",
    "Zed",
    "Ahri",
    "Mordekaiser",
    "Sett",
    "Thresh",
    "Jinx",
})


def _load_build_knowledge() -> dict[str, dict]:
    """Load compact curated guides from build_knowledge.py."""
    try:
        from scripts.build_knowledge import RAW  # noqa: WPS433
    except ImportError:
        return {}

    guides: dict[str, dict] = {}
    for name, raw in RAW.items():
        summary, counters, abilities, laning, spikes, items = raw
        guides[name] = {
            "summary": summary,
            "counters": counters,
            "abilities": abilities,
            "laning": laning,
            "spikes": spikes,
            "items": items,
        }
    return guides


def _build_from_knowledge(name: str, guide: dict, spells: list[dict]) -> dict:
    spell_map = {s["key"]: s["name"] for s in spells}
    ability_tips = []
    for key in ("P", "Q", "W", "E", "R"):
        tip_text = guide.get("abilities", {}).get(key)
        if not tip_text or key not in spell_map:
            continue
        ability_tips.append({"key": key, "name": spell_map[key], "tip": tip_text})

    items = list(guide.get("items", [])[:3])
    fallbacks = [
        "Control Wards — deny fog-of-war setups",
        "Early Boots — dodge skillshots and reposition",
        "Mercury's Treads — MR and tenacity vs CC",
    ]
    for fb in fallbacks:
        if len(items) >= 3:
            break
        if fb not in items:
            items.append(fb)

    return {
        "summary": guide["summary"],
        "counter_picks": [
            {"champion": c[0], "role": c[1], "reason": c[2]}
            for c in guide.get("counters", [])[:5]
        ],
        "ability_tips": ability_tips,
        "laning_tips": guide.get("laning", [])[:5],
        "power_spikes": guide.get("spikes", [])[:3],
        "items_to_consider": items[:3],
    }


def generate_all() -> dict[str, dict]:
    existing: dict = {}
    if MATCHUP_FILE.exists():
        existing = json.loads(MATCHUP_FILE.read_text(encoding="utf-8"))

    knowledge = _load_build_knowledge()
    result: dict[str, dict] = {}

    for champ in list_champions():
        name = champ["name"]
        detail = get_champion_detail(champ["id"])

        if name in PREMIUM_CHAMPIONS and name in existing:
            result[name] = existing[name]
            continue

        if name in knowledge and name not in PREMIUM_CHAMPIONS:
            result[name] = _build_from_knowledge(name, knowledge[name], detail["spells"])
            continue

        result[name] = generate_guide(detail)

    return result


def main() -> None:
    data = generate_all()
    MATCHUP_FILE.parent.mkdir(parents=True, exist_ok=True)
    MATCHUP_FILE.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    premium = sum(1 for n in data if n in PREMIUM_CHAMPIONS)
    knowledge = sum(
        1 for n in data if n not in PREMIUM_CHAMPIONS and n in _load_build_knowledge()
    )
    generated = len(data) - premium - knowledge
    print(f"Wrote {len(data)} champion guides to {MATCHUP_FILE}")
    print(f"  Premium (hand-curated): {premium}")
    print(f"  Enhanced (build_knowledge): {knowledge}")
    print(f"  Generated (Data Dragon): {generated}")


if __name__ == "__main__":
    main()
