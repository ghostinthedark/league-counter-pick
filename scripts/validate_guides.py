"""Validate that all champions have complete guide sections in matchups.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.counters.ddragon import get_champion_detail, list_champions  # noqa: E402

MATCHUP_FILE = ROOT / "data" / "counters" / "matchups.json"

PREMIUM_CHAMPIONS = frozenset({
    "Garen", "Darius", "Yasuo", "Lux", "Zed",
    "Ahri", "Mordekaiser", "Sett", "Thresh", "Jinx",
})

REQUIRED_SECTIONS = (
    "summary",
    "counter_picks",
    "ability_tips",
    "laning_tips",
    "power_spikes",
    "items_to_consider",
)

MIN_COUNTERS = 5
MIN_LANING = 5
MIN_SPIKES = 3
MIN_ITEMS = 3
MIN_SPELLS = 4  # P + at least Q/W/E/R (Thresh has no innate P combat in some patches — allow 4+)


def validate() -> tuple[bool, list[str]]:
    if not MATCHUP_FILE.exists():
        return False, [f"Missing file: {MATCHUP_FILE}"]

    data = json.loads(MATCHUP_FILE.read_text(encoding="utf-8"))
    errors: list[str] = []
    all_champs = list_champions()
    champ_names = {c["name"] for c in all_champs}

    missing_champs = sorted(champ_names - set(data.keys()))
    if missing_champs:
        errors.append(f"Missing {len(missing_champs)} champions: {missing_champs[:5]}...")

    extra = sorted(set(data.keys()) - champ_names)
    if extra:
        errors.append(f"Unknown champion keys: {extra[:5]}")

    for champ in all_champs:
        name = champ["name"]
        entry = data.get(name)
        if not entry:
            continue

        for section in REQUIRED_SECTIONS:
            if section not in entry or not entry[section]:
                errors.append(f"{name}: missing or empty '{section}'")

        counters = entry.get("counter_picks", [])
        if len(counters) < MIN_COUNTERS:
            errors.append(f"{name}: only {len(counters)} counter picks (need {MIN_COUNTERS})")

        laning = entry.get("laning_tips", [])
        if len(laning) < MIN_LANING:
            errors.append(f"{name}: only {len(laning)} laning tips (need {MIN_LANING})")

        spikes = entry.get("power_spikes", [])
        if len(spikes) < MIN_SPIKES:
            errors.append(f"{name}: only {len(spikes)} power spikes (need {MIN_SPIKES})")

        items = entry.get("items_to_consider", [])
        if len(items) < MIN_ITEMS:
            errors.append(f"{name}: only {len(items)} items (need {MIN_ITEMS})")

        detail = get_champion_detail(champ["id"])
        expected_keys = {s["key"] for s in detail["spells"]}
        tip_keys = {t["key"] for t in entry.get("ability_tips", [])}
        missing_spells = expected_keys - tip_keys
        if len(tip_keys) < MIN_SPELLS or missing_spells:
            errors.append(
                f"{name}: ability tips missing keys {sorted(missing_spells)} "
                f"(have {sorted(tip_keys)})"
            )

        for tip in entry.get("ability_tips", []):
            if not tip.get("tip") or len(tip["tip"]) < 30:
                errors.append(f"{name} {tip.get('key')}: tip too short or empty")

    ok = len(errors) == 0
    return ok, errors


def main() -> None:
    ok, errors = validate()
    data = json.loads(MATCHUP_FILE.read_text(encoding="utf-8"))
    premium = sum(1 for n in data if n in PREMIUM_CHAMPIONS)
    print(f"Champions in matchups.json: {len(data)}")
    print(f"Premium guides: {premium}")
    print(f"Full guides: {len(data)}")

    if ok:
        print("VALIDATION PASSED — all champions have complete guide sections.")
        raise SystemExit(0)

    print(f"VALIDATION FAILED — {len(errors)} issue(s):")
    for err in errors[:30]:
        print(f"  - {err}")
    if len(errors) > 30:
        print(f"  ... and {len(errors) - 30} more")
    raise SystemExit(1)


if __name__ == "__main__":
    main()
