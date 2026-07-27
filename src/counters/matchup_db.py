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


def get_matchup(champion_id: str) -> dict[str, Any] | None:
    data = _load()
    return data.get(champion_id) or data.get(champion_id.lower())


def list_curated_ids() -> list[str]:
    return list(_load().keys())
