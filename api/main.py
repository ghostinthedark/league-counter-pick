"""FastAPI application for League Counter Pick app."""

from __future__ import annotations

import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.counters.ddragon import (  # noqa: E402
    champion_image_url,
    get_champion_detail,
    list_champions,
    spell_image_url,
)
from src.counters.matchup_db import get_matchup, is_premium_guide  # noqa: E402
from src.counters.synergy_db import (  # noqa: E402
    get_synergy,
    is_premium_synergy_guide,
    search_synergies,
)

app = FastAPI(
    title="League Counter Pick",
    description="Champion counter-pick instructions and matchup tips",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _find_champion(query: str) -> dict | None:
    q = query.strip().lower()
    if not q:
        return None
    for champ in list_champions():
        if (
            champ["id"].lower() == q
            or champ["name"].lower() == q
            or q in champ["name"].lower()
        ):
            return champ
    return None


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/api/champions")
def champions(search: str | None = Query(None, min_length=1)) -> list[dict]:
    all_champs = list_champions()
    if not search:
        return [
            {
                **c,
                "image_url": champion_image_url(c["image"]),
            }
            for c in all_champs
        ]
    q = search.lower()
    filtered = [
        c
        for c in all_champs
        if q in c["name"].lower() or q in c["id"].lower()
    ]
    return [
        {
            **c,
            "image_url": champion_image_url(c["image"]),
        }
        for c in filtered[:20]
    ]


@app.get("/api/counter/{champion}")
def counter_guide(champion: str) -> dict:
    champ = _find_champion(champion)
    if not champ:
        raise HTTPException(status_code=404, detail=f"Champion '{champion}' not found")

    detail = get_champion_detail(champ["id"])
    matchup = get_matchup(champ["id"], champ["name"])
    if not matchup:
        raise HTTPException(
            status_code=404,
            detail=f"No matchup guide found for '{champion}'",
        )

    guide = {
        "summary": matchup.get("summary", f"How to play against {detail['name']}."),
        "counter_picks": matchup.get("counter_picks", []),
        "ability_tips": matchup.get("ability_tips", []),
        "laning_tips": matchup.get("laning_tips", []),
        "power_spikes": matchup.get("power_spikes", []),
        "items_to_consider": matchup.get("items_to_consider", []),
    }
    has_full_guide = True
    is_premium = is_premium_guide(detail["name"])

    return {
        "champion": {
            "id": detail["id"],
            "name": detail["name"],
            "title": detail["title"],
            "tags": detail["tags"],
            "image_url": champion_image_url(detail["image"]),
        },
        **guide,
        "spells": [
            {
                **s,
                "image_url": spell_image_url(detail["id"], s["key"]),
            }
            for s in detail["spells"]
        ],
        "has_full_guide": has_full_guide,
        "is_premium_guide": is_premium,
        "has_curated_guide": has_full_guide,
    }


@app.get("/api/synergy/{champion}")
def synergy_guide(champion: str) -> dict:
    champ = _find_champion(champion)
    if not champ:
        raise HTTPException(status_code=404, detail=f"Champion '{champion}' not found")

    detail = get_champion_detail(champ["id"])
    synergy = get_synergy(champ["id"], champ["name"])
    if not synergy:
        raise HTTPException(
            status_code=404,
            detail=f"No synergy guide found for '{champion}'",
        )

    guide = {
        "summary": synergy.get("summary", f"Best duo partners for {detail['name']}."),
        "synergy_picks": synergy.get("synergy_picks", []),
        "ability_synergy_tips": synergy.get("ability_synergy_tips", []),
        "combo_tips": synergy.get("combo_tips", []),
        "power_spikes": synergy.get("power_spikes", []),
        "items_to_consider": synergy.get("items_to_consider", []),
    }
    has_full_guide = True
    is_premium = is_premium_synergy_guide(detail["name"])

    return {
        "champion": {
            "id": detail["id"],
            "name": detail["name"],
            "title": detail["title"],
            "tags": detail["tags"],
            "image_url": champion_image_url(detail["image"]),
        },
        **guide,
        "spells": [
            {
                **s,
                "image_url": spell_image_url(detail["id"], s["key"]),
            }
            for s in detail["spells"]
        ],
        "has_full_guide": has_full_guide,
        "is_premium_guide": is_premium,
        "has_curated_guide": has_full_guide,
    }


@app.get("/api/synergies")
def synergies(search: str | None = Query(None, min_length=1)) -> list[dict]:
    all_champs = list_champions()
    champ_map = {c["name"]: c for c in all_champs}

    if search:
        names = search_synergies(search)
    else:
        names = search_synergies("")

    results = []
    for name in names:
        champ = champ_map.get(name)
        if not champ:
            continue
        results.append({
            "id": champ["id"],
            "name": champ["name"],
            "title": champ["title"],
            "tags": champ["tags"],
            "image_url": champion_image_url(champ["image"]),
        })
    return results


WEB_DIR = ROOT / "web" / "static"
if WEB_DIR.exists():
    app.mount("/", StaticFiles(directory=str(WEB_DIR), html=True), name="static")
