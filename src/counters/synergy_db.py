"""Curated champion synergy guides — best duo partners and combo advice."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent.parent
SYNERGY_FILE = ROOT / "data" / "synergies" / "synergies.json"

_synergies: dict[str, Any] | None = None

PREMIUM_CHAMPIONS: frozenset[str] = frozenset({
    "Garen", "Darius", "Yasuo", "Lux", "Zed",
    "Ahri", "Mordekaiser", "Sett", "Thresh", "Jinx",
})


def _load() -> dict[str, Any]:
    global _synergies
    if _synergies is None:
        if not SYNERGY_FILE.exists():
            _synergies = {}
        else:
            _synergies = json.loads(SYNERGY_FILE.read_text(encoding="utf-8"))
    return _synergies


def get_synergy(champion_id: str, champion_name: str | None = None) -> dict[str, Any] | None:
    data = _load()
    for key in (champion_name, champion_id, champion_id.lower()):
        if key and key in data:
            return data[key]
    return None


def is_premium_synergy_guide(champion_name: str) -> bool:
    return champion_name in PREMIUM_CHAMPIONS or champion_name in _load()


def search_synergies(query: str, limit: int = 20) -> list[str]:
    q = query.strip().lower()
    if not q:
        return list(_load().keys())[:limit]
    return [name for name in _load() if q in name.lower()][:limit]


def list_synergy_ids() -> list[str]:
    return list(_load().keys())
