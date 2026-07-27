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
from src.counters.guide_generator import generate_guide  # noqa: E402
from src.counters.matchup_db import get_matchup  # noqa: E402

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
    matchup = get_matchup(champ["id"])

    if matchup:
        guide = {
            "summary": matchup.get("summary", f"How to play against {detail['name']}."),
            "counter_picks": matchup.get("counter_picks", []),
            "ability_tips": matchup.get("ability_tips", []),
            "laning_tips": matchup.get("laning_tips", []),
            "power_spikes": matchup.get("power_spikes", []),
            "items_to_consider": matchup.get("items_to_consider", []),
        }
    else:
        guide = generate_guide(detail)

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
        "has_curated_guide": matchup is not None,
    }


WEB_DIR = ROOT / "web" / "static"
if WEB_DIR.exists():
    app.mount("/", StaticFiles(directory=str(WEB_DIR), html=True), name="static")
