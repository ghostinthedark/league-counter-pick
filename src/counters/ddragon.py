"""League Data Dragon client for champion static data (no API key required)."""

from __future__ import annotations

import time
from typing import Any

import requests

DDRAGON_BASE = "https://ddragon.leagueoflegends.com/cdn"
VERSIONS_URL = "https://ddragon.leagueoflegends.com/api/versions.json"

_cache: dict[str, Any] = {}
_cache_ts: float = 0.0
_CACHE_TTL = 3600.0


def _get_version() -> str:
    global _cache_ts
    if "version" in _cache and (time.monotonic() - _cache_ts) < _CACHE_TTL:
        return _cache["version"]
    response = requests.get(VERSIONS_URL, timeout=15)
    response.raise_for_status()
    version = response.json()[0]
    _cache["version"] = version
    _cache_ts = time.monotonic()
    return version


def _fetch_json(path: str) -> Any:
    version = _get_version()
    url = f"{DDRAGON_BASE}/{version}/{path}"
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    return response.json()


def list_champions() -> list[dict[str, Any]]:
    if "champions" in _cache and (time.monotonic() - _cache_ts) < _CACHE_TTL:
        return _cache["champions"]

    payload = _fetch_json("data/en_US/champion.json")
    champions = []
    for champ_id, info in payload["data"].items():
        champions.append(
            {
                "id": champ_id,
                "key": info["key"],
                "name": info["name"],
                "title": info["title"],
                "tags": info.get("tags", []),
                "image": info["image"]["full"],
            }
        )
    champions.sort(key=lambda c: c["name"])
    _cache["champions"] = champions
    return champions


def get_champion_detail(champion_id: str) -> dict[str, Any]:
    cache_key = f"detail:{champion_id.lower()}"
    if cache_key in _cache and (time.monotonic() - _cache_ts) < _CACHE_TTL:
        return _cache[cache_key]

    version = _get_version()
    payload = _fetch_json(f"data/en_US/champion/{champion_id}.json")
    info = payload["data"][champion_id]

    spells = []
    for spell_key in ("passive", "q", "w", "e", "r"):
        if spell_key == "passive":
            passive = info["passive"]
            spells.append(
                {
                    "key": "P",
                    "name": passive["name"],
                    "description": _clean_html(passive["description"]),
                }
            )
        else:
            idx = {"q": 0, "w": 1, "e": 2, "r": 3}[spell_key]
            spell = info["spells"][idx]
            spells.append(
                {
                    "key": spell_key.upper(),
                    "name": spell["name"],
                    "description": _clean_html(spell["description"]),
                    "cooldown": spell.get("cooldownBurn", ""),
                    "cost": spell.get("costBurn", ""),
                }
            )

    detail = {
        "id": champion_id,
        "name": info["name"],
        "title": info["title"],
        "tags": info.get("tags", []),
        "lore": info.get("lore", ""),
        "image": info["image"]["full"],
        "spells": spells,
        "version": version,
    }
    _cache[cache_key] = detail
    return detail


def champion_image_url(image_file: str) -> str:
    version = _get_version()
    return f"{DDRAGON_BASE}/{version}/img/champion/{image_file}"


def spell_image_url(champion_id: str, spell_key: str) -> str:
    version = _get_version()
    key_map = {"P": "passive", "Q": "Q", "W": "W", "E": "E", "R": "R"}
    suffix = key_map.get(spell_key.upper(), spell_key)
    if suffix == "passive":
        return f"{DDRAGON_BASE}/{version}/img/passive/{champion_id}_P.png"
    return f"{DDRAGON_BASE}/{version}/img/spell/{champion_id}{suffix}.png"


def _clean_html(text: str) -> str:
    import re

    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    return text.strip()
