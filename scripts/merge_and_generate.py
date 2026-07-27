#!/usr/bin/env python3
"""Merge all champion guide batches and generate matchups.json."""

from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.counters.ddragon import get_champion_detail, list_champions  # noqa: E402

MATCHUP_FILE = ROOT / "data" / "counters" / "matchups.json"
SCRIPTS = Path(__file__).resolve().parent

# Preserve hand-written entries
PRESERVE = {"Garen", "Darius", "Yasuo", "Lux", "Zed", "Ahri", "Mordekaiser", "Sett", "Thresh", "Jinx"}


def _load_batch(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    # Wrap in dict braces for ast parsing
    if not text.strip().startswith("{"):
        text = "{\n" + text.rstrip().rstrip(",") + "\n}"
    return ast.literal_eval(text)


def _load_build_knowledge_raw() -> dict:
    src = (SCRIPTS / "build_knowledge.py").read_text(encoding="utf-8")
    match = re.search(r"RAW: dict\[str, tuple\] = (\{.*?\n\})\n", src, re.DOTALL)
    if not match:
        raise ValueError("Could not parse RAW from build_knowledge.py")
    return ast.literal_eval(match.group(1))


def _build_entry(guide: tuple, spells: list[dict]) -> dict:
    summary, counters, abilities, laning, spikes, items = guide
    spell_map = {s["key"]: s["name"] for s in spells}
    ability_tips = []
    for key in ("P", "Q", "W", "E", "R"):
        if key in abilities and key in spell_map:
            ability_tips.append({"key": key, "name": spell_map[key], "tip": abilities[key]})
    return {
        "summary": summary,
        "counter_picks": [{"champion": c[0], "role": c[1], "reason": c[2]} for c in counters],
        "ability_tips": ability_tips,
        "laning_tips": list(laning),
        "power_spikes": list(spikes),
        "items_to_consider": list(items),
    }


def main() -> None:
    raw: dict = {}
    raw.update(_load_build_knowledge_raw())

    d_m = SCRIPTS / "matchup_entries_d_m.py"
    if d_m.exists():
        raw.update(_load_batch(d_m))

    m_z = SCRIPTS / "matchup_entries_m_z.py"
    if not m_z.exists():
        # Fallback to league-analytics copy
        alt = Path(r"C:\Users\Michael\OneDrive\Documents\league-analytics\data\counters\matchup_entries_m_z.py")
        if alt.exists():
            m_z = alt
    raw.update(_load_batch(m_z))

    extra = SCRIPTS / "matchup_entries_extra.py"
    if extra.exists():
        raw.update(_load_batch(extra))

    existing = json.loads(MATCHUP_FILE.read_text(encoding="utf-8")) if MATCHUP_FILE.exists() else {}
    result = {k: v for k, v in existing.items() if k in PRESERVE}

    all_champs = list_champions()
    missing = []
    for champ in all_champs:
        name = champ["name"]
        if name in result:
            continue
        if name not in raw:
            missing.append(name)
            continue
        detail = get_champion_detail(champ["id"])
        result[name] = _build_entry(raw[name], detail["spells"])

    if missing:
        print(f"Missing {len(missing)} champions: {missing}")
        raise SystemExit(1)

    MATCHUP_FILE.parent.mkdir(parents=True, exist_ok=True)
    MATCHUP_FILE.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(result)} champion guides to {MATCHUP_FILE}")

    # Also write matchup_knowledge.py for reference
    knowledge_path = SCRIPTS / "matchup_knowledge.py"
    knowledge_path.write_text(
        '"""Curated premium matchup knowledge for all League champions."""\n\n'
        f"CHAMPION_GUIDES: dict[str, dict] = {json.dumps({k: _build_entry(v, []) for k, v in raw.items()}, indent=2)!r}\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
