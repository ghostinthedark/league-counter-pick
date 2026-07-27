"""Curated counter-pick and matchup instructions per champion."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent.parent
MATCHUP_FILE = ROOT / "data" / "counters" / "matchups.json"

_matchups: dict[str, Any] | None = None


def _load() -> dict[str, Any]:
    global _matchups
    if _matchups is None:
        if not MATCHUP_FILE.exists():
            _matchups = {}
        else:
            _matchups = json.loads(MATCHUP_FILE.read_text(encoding="utf-8"))
    return _matchups


def get_matchup(champion_id: str, champion_name: str | None = None) -> dict[str, Any] | None:
    data = _load()
    for key in (champion_name, champion_id, champion_id.lower()):
        if key and key in data:
            return data[key]
    return None


def is_premium_guide(champion_name: str) -> bool:
    """Hand-curated Yasuo-quality guides."""
    premium = {
        "Garen", "Darius", "Yasuo", "Lux", "Zed",
        "Ahri", "Mordekaiser", "Sett", "Thresh", "Jinx",
    }
    return champion_name in premium


def list_curated_ids() -> list[str]:
    return list(_load().keys())
