"""Generate full counter guides from Data Dragon champion detail."""

from __future__ import annotations

import re
from typing import Any

# Tag-based counter pools — champions that generally beat each archetype
COUNTER_POOLS: dict[str, list[dict[str, str]]] = {
    "Fighter": [
        {"champion": "Vayne", "role": "Top/ADC", "reason": "True damage and kiting punish bruisers who need to stay in melee range."},
        {"champion": "Quinn", "role": "Top", "reason": "Range and vault disengage stop fighters from ever reaching you."},
        {"champion": "Teemo", "role": "Top", "reason": "Blind shuts down auto-attack trade patterns; shrooms zone all-ins."},
        {"champion": "Kayle", "role": "Top", "reason": "Outranges and outscales — slow with W to kite extended trades."},
        {"champion": "Gnar", "role": "Top", "reason": "Mini form harass, Mega form CC — controls fight distance."},
    ],
    "Tank": [
        {"champion": "Vayne", "role": "Top/ADC", "reason": "% HP true damage melts tanks regardless of armor stacks."},
        {"champion": "Gwen", "role": "Top", "reason": "% HP damage and Hallowed Mist dodge tank engage tools."},
        {"champion": "KogMaw", "role": "ADC", "reason": "% HP magic damage on every auto — shreds frontline."},
        {"champion": "Fiora", "role": "Top", "reason": "Max-health true damage and outduels tanks in side lane."},
        {"champion": "Brand", "role": "Support/Mid", "reason": "Percent-max-HP burn punishes stacking HP items."},
    ],
    "Mage": [
        {"champion": "Yasuo", "role": "Mid", "reason": "Wind Wall blocks key skillshots; dash gap-close after spell rotation."},
        {"champion": "Fizz", "role": "Mid", "reason": "Playful/Trickster dodges burst; all-in after cooldowns are spent."},
        {"champion": "Zed", "role": "Mid", "reason": "All-in assassin punishes immobile mages after they use spells."},
        {"champion": "Kassadin", "role": "Mid", "reason": "Scales past mages with R gap-close and magic damage shield."},
        {"champion": "Sylas", "role": "Mid", "reason": "Can steal their ultimate and survive burst with W heal."},
    ],
    "Assassin": [
        {"champion": "Malzahar", "role": "Mid", "reason": "Point-and-click suppression stops dashes and burst combos."},
        {"champion": "Lissandra", "role": "Mid", "reason": "Self-ult or W-R stops all-in; reliable point-and-click CC."},
        {"champion": "Annie", "role": "Mid", "reason": "Instant stun combo before the assassin can commit with R."},
        {"champion": "Pantheon", "role": "Mid/Top", "reason": "Point-and-click W stun and early all-in before assassin spikes."},
        {"champion": "Galio", "role": "Mid", "reason": "W magic shield and CC chain shuts down assassination windows."},
    ],
    "Marksman": [
        {"champion": "Draven", "role": "ADC", "reason": "Dominates early lane before ADC reaches item spikes."},
        {"champion": "Lucian", "role": "ADC", "reason": "Burst and mobility win short trades in lane."},
        {"champion": "Leona", "role": "Support", "reason": "Hard CC stops immobile ADCs from kiting."},
        {"champion": "Nautilus", "role": "Support", "reason": "Point-and-click hook catches low-mobility carries."},
        {"champion": "Zed", "role": "Mid", "reason": "Assassinates ADC in side lane and teamfights."},
    ],
    "Support": [
        {"champion": "Leona", "role": "Support", "reason": "Hard engage punishes enchanters who can't trade back."},
        {"champion": "Nautilus", "role": "Support", "reason": "Point-and-click CC locks down low-HP supports."},
        {"champion": "Blitzcrank", "role": "Support", "reason": "Hook pick potential deletes squishy supports in fog."},
        {"champion": "Pyke", "role": "Support", "reason": "Execute threat and roam pressure outplays passive supports."},
        {"champion": "Brand", "role": "Support", "reason": "Lane poke and percent-HP burn win extended trades."},
    ],
}

TAG_COMBO_POOLS: dict[frozenset[str], list[dict[str, str]]] = {
    frozenset({"Support", "Mage"}): [
        {"champion": "Leona", "role": "Support", "reason": "All-in engage collapses enchanter supports before shields matter."},
        {"champion": "Nautilus", "role": "Support", "reason": "Point-and-click CC bypasses peel and shield timing."},
        {"champion": "Brand", "role": "Support", "reason": "Poke and percent-HP burn out-trade shield-based supports."},
        {"champion": "Pyke", "role": "Support", "reason": "Execute threat and roam pressure punishes passive laning."},
        {"champion": "Xerath", "role": "Support", "reason": "Long-range poke forces enchanters to spend mana healing."},
    ],
    frozenset({"Support", "Tank"}): [
        {"champion": "Vayne", "role": "ADC", "reason": "% HP true damage shreds tank supports in extended fights."},
        {"champion": "Brand", "role": "Support", "reason": "Percent-max-HP burn makes stacking HP items a liability."},
        {"champion": "Gwen", "role": "Top", "reason": "% HP damage and mobility kites tank supports."},
        {"champion": "Morgana", "role": "Support", "reason": "Black Shield blocks hook/engage and outranges tank supports."},
        {"champion": "KogMaw", "role": "ADC", "reason": "On-hit % HP damage melts tank frontline."},
    ],
    frozenset({"Fighter", "Tank"}): [
        {"champion": "Vayne", "role": "Top/ADC", "reason": "True damage and kiting beat juggernauts who need to stick."},
        {"champion": "Gwen", "role": "Top", "reason": "% HP damage and Hallowed Mist dodge key abilities."},
        {"champion": "Kayle", "role": "Top", "reason": "Range advantage and scaling outduel juggernauts late."},
        {"champion": "Quinn", "role": "Top", "reason": "Never lets juggernauts reach melee range."},
        {"champion": "Fiora", "role": "Top", "reason": "Parry denies key abilities; true damage outscales."},
    ],
    frozenset({"Assassin", "Fighter"}): [
        {"champion": "Malzahar", "role": "Mid", "reason": "Suppression stops dash chains and burst combos."},
        {"champion": "Pantheon", "role": "Mid", "reason": "Point-and-click stun and early all-in before they scale."},
        {"champion": "Garen", "role": "Top", "reason": "Q silence stops dash chains; simple kit beats mechanics."},
        {"champion": "Annie", "role": "Mid", "reason": "Instant stun combo before they can commit with R."},
        {"champion": "Lissandra", "role": "Mid", "reason": "Self-ult stops all-in; reliable CC throughout the fight."},
    ],
    frozenset({"Mage", "Assassin"}): [
        {"champion": "Galio", "role": "Mid", "reason": "W magic shield and CC chain shuts down burst windows."},
        {"champion": "Malzahar", "role": "Mid", "reason": "Suppression and passive spell shield counter all-in patterns."},
        {"champion": "Vladimir", "role": "Mid", "reason": "Pool dodges key abilities; outscales in side lane."},
        {"champion": "Lissandra", "role": "Mid", "reason": "Point-and-click CC stops dash-in burst combos."},
        {"champion": "Annie", "role": "Mid", "reason": "Point-and-click stun before they can commit."},
    ],
}

# Champion-specific counter overrides where tags alone mislead (e.g. jungle enchanters).
SUMMARY_OVERRIDES: dict[str, str] = {
    "Ivern": (
        "Ivern wins with fast camp clears, Triggerseed shields, and Daisy teamfights. "
        "Invade early, burst through shields, and punish long Daisy cooldown."
    ),
}

CHAMPION_COUNTER_OVERRIDES: dict[str, list[dict[str, str]]] = {
    "Ivern": [
        {"champion": "Lee Sin", "role": "Jungle", "reason": "Invades early and wins skirmishes before Ivern finishes camp setup."},
        {"champion": "Graves", "role": "Jungle", "reason": "Fast clear and burst — steals camps and collapses on Ivern."},
        {"champion": "Elise", "role": "Jungle", "reason": "Early pressure and cocoon punishes slow, shield-reliant junglers."},
        {"champion": "Nidalee", "role": "Jungle", "reason": "Invades and spears chunk Ivern before Daisy comes online."},
        {"champion": "Kindred", "role": "Jungle", "reason": "Kites Daisy and marks camps — denies Ivern's clear identity."},
    ],
    "Graves": [
        {"champion": "Karthus", "role": "Jungle", "reason": "Global pressure and faster scaling teamfights outvalue Graves mid-game."},
        {"champion": "Rammus", "role": "Jungle", "reason": "Armor stack reduces burst; taunt stops shotgun all-ins."},
        {"champion": "Malphite", "role": "Top/Jungle", "reason": "Armor and R disengage shut down short-range DPS."},
        {"champion": "Poppy", "role": "Jungle/Top", "reason": "W blocks E dash; extended fights favor Poppy."},
        {"champion": "Kindred", "role": "Jungle", "reason": "Kiting and R save from Graves burst windows."},
    ],
    "Kindred": [
        {"champion": "Rengar", "role": "Jungle", "reason": "One-shot burst before Lamb can stack marks safely."},
        {"champion": "Kha'Zix", "role": "Jungle", "reason": "Isolation burst kills Kindred before R can save them."},
        {"champion": "Vi", "role": "Jungle", "reason": "Point-and-click ult locks down mobile marksmen jungler."},
        {"champion": "Nautilus", "role": "Support", "reason": "Hard CC stops kiting and denies mark stack resets."},
        {"champion": "Warwick", "role": "Jungle", "reason": "R suppression holds Kindred in place for team collapse."},
    ],
}

SUMMARY_TEMPLATES: dict[str, str] = {
    "Fighter": "{name} wins extended melee trades and wants to stick to you. Respect their all-in windows and kite between cooldowns.",
    "Tank": "{name} soaks damage and enables teamfights with CC. Avoid extended fights — focus % HP damage and kiting.",
    "Mage": "{name} wins with skillshot combos and burst from range. Respect cooldown windows and punish missed spells.",
    "Assassin": "{name} wins short burst windows and roams. Play safe when their gap-close and ult are available.",
    "Marksman": "{name} scales with items and wants to auto-attack freely. Punish early weakness and hard-engage before they itemize.",
    "Support": "{name} enables their team with peel or engage. Target them in fights and respect their key CC or shield tools.",
}

TAG_COMBO_SUMMARIES: dict[frozenset[str], str] = {
    frozenset({"Support", "Mage"}): "{name} is an enchanter who wins by shielding, buffing, and controlling space. Hard engage and burst punish slow shield reactions.",
    frozenset({"Support", "Tank"}): "{name} is a tank support who wins lane with CC chains and body-blocking. Poke and % HP damage reduce their frontline value.",
    frozenset({"Fighter", "Tank"}): "{name} is a juggernaut who wins long trades and becomes unkillable with items. Kite, short-trade, and respect their W/R power spikes.",
    frozenset({"Assassin", "Fighter"}): "{name} is a skirmisher who wins with dash chains and burst combos. Point-and-click CC and early all-ins shut them down.",
    frozenset({"Mage", "Assassin"}): "{name} is a burst mage who wins with spell rotation and pick potential. Magic resist and hard CC before they commit win the matchup.",
}

CC_PATTERNS: list[tuple[str, str]] = [
    (r"\bstun(?:s|ned)?\b", "stun"),
    (r"\broot(?:s|ed)?\b", "root"),
    (r"\bknock\s*up\b", "knockup"),
    (r"\bknock(?:s|ed)?\s*back\b", "knockback"),
    (r"\bsuppress(?:es|ion|ed)?\b", "suppress"),
    (r"\bsilenc(?:e|es|ed)\b", "silence"),
    (r"\bcharm(?:s|ed)?\b", "charm"),
    (r"\bfear(?:s|ed)?\b", "fear"),
    (r"\btaunt(?:s|ed)?\b", "taunt"),
    (r"\bslow(?:s|ed)?\b", "slow"),
    (r"\bhook\b|\bgrab\b|\bpull(?:s|ed)?\b", "hook"),
]

CC_ADVICE: dict[str, str] = {
    "stun": "Hard stun — don't commit when it's available; sidestep or hide behind minions.",
    "root": "Roots in place — sidestep the skillshot or hide behind minions; allies may dash to follow up.",
    "knockup": "Knockup — unstoppable CC; disengage when this ability is ready.",
    "knockback": "Knockback — can disrupt your engage or peel you into their team.",
    "suppress": "Suppression — cannot be cleansed with QSS; play safe when it's up.",
    "silence": "Silence — removes spell casts; disengage immediately if it lands.",
    "charm": "Charm — forces you to walk toward them; sidestep or break line-of-sight.",
    "fear": "Fear — forces retreat; don't chase into fog when this is available.",
    "taunt": "Taunt — forces auto-attacks; back off when this is active.",
    "slow": "Applies slow — movement reduction sets up follow-up damage.",
    "hook": "Hook/grab — stand behind minions; punish the long cooldown if it misses.",
}


def generate_guide(detail: dict[str, Any]) -> dict[str, Any]:
    """Build a full counter guide from champion detail."""
    tags = detail.get("tags", [])
    name = detail["name"]
    spells = detail.get("spells", [])
    key_ability = _pick_key_ability(spells)

    return {
        "summary": _generate_summary(name, tags, spells),
        "counter_picks": _generate_counter_picks(name, tags),
        "ability_tips": [
            _generate_ability_tip(spell, key=key_ability) for spell in spells
        ],
        "laning_tips": _generate_laning_tips(name, tags, spells),
        "power_spikes": _generate_power_spikes(name, tags, spells)[:3],
        "items_to_consider": _generate_items(tags, spells)[:3],
    }


def _generate_summary(name: str, tags: list[str], spells: list[dict]) -> str:
    if name in SUMMARY_OVERRIDES:
        return SUMMARY_OVERRIDES[name]

    tag_set = frozenset(tags)
    for combo, template in TAG_COMBO_SUMMARIES.items():
        if combo.issubset(tag_set):
            return template.format(name=name)

    spell_text = " ".join(s.get("description", "") for s in spells).lower()
    if _is_jungle_champion(spell_text):
        return (
            f"{name} wins through jungle control and objective setup. "
            "Invade early, punish slow clears, and collapse before they scale."
        )

    primary = tags[0] if tags else "Fighter"
    template = SUMMARY_TEMPLATES.get(primary, SUMMARY_TEMPLATES["Fighter"])
    if len(tags) > 1:
        secondary = tags[1].lower()
        role = f"{primary.lower()}/{secondary}"
        if " wins " in template:
            rest = template.split(" wins ", 1)[1]
            return f"{name} is a {role} who wins {rest}"
        return f"{name} is a {role}. {template.format(name=name)}"
    return template.format(name=name)


def _generate_counter_picks(name: str, tags: list[str]) -> list[dict[str, str]]:
    if name in CHAMPION_COUNTER_OVERRIDES:
        return CHAMPION_COUNTER_OVERRIDES[name][:5]

    tag_set = frozenset(tags)
    pool: list[dict[str, str]] = []

    for combo, counters in TAG_COMBO_POOLS.items():
        if combo.issubset(tag_set):
            pool.extend(counters)

    if not pool:
        for tag in tags:
            pool.extend(COUNTER_POOLS.get(tag, []))

    if not pool:
        pool = COUNTER_POOLS["Fighter"]

    # Exclude the champion themselves and dedupe
    seen: set[str] = set()
    unique: list[dict[str, str]] = []
    for entry in pool:
        champ = entry["champion"]
        if champ != name and champ not in seen:
            seen.add(champ)
            unique.append(entry)

    # Backfill if self was in pool (e.g. Draven, Pantheon)
    if len(unique) < 5:
        for tag in tags:
            for entry in COUNTER_POOLS.get(tag, []):
                champ = entry["champion"]
                if champ != name and champ not in seen:
                    seen.add(champ)
                    unique.append(entry)
                if len(unique) >= 5:
                    break
            if len(unique) >= 5:
                break

    if len(unique) < 5:
        for entry in COUNTER_POOLS["Fighter"]:
            champ = entry["champion"]
            if champ != name and champ not in seen:
                seen.add(champ)
                unique.append(entry)
            if len(unique) >= 5:
                break

    return unique[:5]


def _first_cooldown(spell: dict[str, Any]) -> int | None:
    raw = spell.get("cooldown", "")
    if not raw:
        return None
    first = raw.split("/")[0].strip()
    if first.isdigit():
        return int(first)
    return None


def _detect_cc(desc_lower: str) -> str | None:
    for pattern, label in CC_PATTERNS:
        if re.search(pattern, desc_lower):
            return label
    return None


def _detect_damage_type(desc_lower: str) -> str | None:
    if "true damage" in desc_lower:
        return "true"
    if "magic damage" in desc_lower:
        return "magic"
    if "physical damage" in desc_lower:
        return "physical"
    return None


def _is_jungle_champion(spell_text: str) -> bool:
    markers = (
        "jungle camp",
        "non-epic monster",
        "cannot attack or be attacked by non-epic",
        "smite",
    )
    return any(m in spell_text for m in markers)


def _is_jungle_only_passive(desc: str) -> bool:
    dl = desc.lower()
    return (
        "cannot attack or be attacked by non-epic" in dl
        or ("jungle camp" in dl and "ally" not in dl[:80])
    )


def _pick_key_ability(spells: list[dict]) -> str:
    best_key = "R"
    best_score = -1
    for spell in spells:
        key = spell["key"]
        desc = spell.get("description", "").lower()
        score = 0
        cd = _first_cooldown(spell)
        if key == "R":
            score += 4
        if _detect_cc(desc):
            score += 3
        if any(w in desc for w in ("hook", "grab", "charm", "suppress", "execute")):
            score += 4
        if "global" in desc:
            score += 3
        if cd and cd >= 14:
            score += 2
        if "shield" in desc and key in ("W", "E"):
            score += 1
        if score > best_score:
            best_score = score
            best_key = key
    return best_key


def _generate_ability_tip(spell: dict[str, Any], *, key: str) -> dict[str, str]:
    spell_key = spell["key"]
    name = spell["name"]
    desc = spell.get("description", "")
    desc_lower = desc.lower()
    cd = _first_cooldown(spell)
    cc = _detect_cc(desc_lower)
    dmg = _detect_damage_type(desc_lower)
    is_key = spell_key == key

    parts: list[str] = []

    if is_key:
        parts.append("THE KEY ABILITY.")

    if spell_key == "P" and _is_jungle_only_passive(desc):
        parts.append(
            f"{name} is jungle-focused — in lane, respect their Q/W/E instead. "
            "Invade or match roams to deny camp control."
        )
    elif spell_key == "P":
        if "move speed" in desc_lower or "movement speed" in desc_lower:
            parts.append(
                f"{name} grants move speed on takedowns or procs. "
                "CC immediately after kills — don't chase into reset speed."
            )
        elif "shield" in desc_lower:
            parts.append(
                f"{name} generates shields from movement or actions. "
                "Break the shield with any damage before committing to trades."
            )
        elif "stack" in desc_lower or "stacks" in desc_lower:
            parts.append(
                f"{name} stacks over time — short trades prevent full passive value."
            )
        else:
            core = _condense_mechanic(_first_sentence(desc))
            parts.append(f"{name} passive: {core} Respect it in extended trades.")

    if "brush" in desc_lower or "bush" in desc_lower:
        parts.append(
            "Creates brush — ward it immediately; they gain combat advantages and bonus damage inside."
        )

    if "summon" in desc_lower and spell_key == "R":
        parts.append(
            "Summons a pet — focus it down or CC it; it adds significant frontline pressure."
        )

    if cc and spell_key != "P":
        parts.append(CC_ADVICE[cc])

    if "shield" in desc_lower and spell_key != "P":
        parts.append(
            "Grants a shield — burst through it or wait for it to break before committing."
        )

    if "heals" in desc_lower or re.search(r"\bheal(?:s|ing)?\b", desc_lower):
        if "heal" in desc_lower and "health" not in desc_lower[:20]:
            parts.append("Healing — take short trades and buy anti-heal (Oblivion Orb / Bramble Vest).")

    if "untargetable" in desc_lower or "cannot be targeted" in desc_lower:
        parts.append("Makes them untargetable — don't waste key abilities during this window.")

    if "true damage" in desc_lower:
        parts.append("True damage — ignores armor/MR; respect the raw damage.")

    if "execute" in desc_lower or "missing health" in desc_lower:
        parts.append("Execute damage — recall or heal before the kill threshold.")

    if "global" in desc_lower:
        parts.append("Global range — recall at low HP even without direct vision.")

    if "allies can dash" in desc_lower or "ally can dash" in desc_lower:
        parts.append(
            "Allies can dash to the target — don't get caught isolated near CC'd teammates."
        )
    elif re.search(r"\b(dash|blink|leap)\b", desc_lower) and spell_key != "P":
        parts.append("Mobility tool — track its cooldown before committing to trades.")

    if dmg == "magic" and spell_key != "P":
        parts.append("Magic damage — Mercury's Treads or early MR reduces burst.")
    elif dmg == "physical" and spell_key != "P":
        parts.append("Physical damage — Plated Steelcaps or early armor helps.")

    if cd and spell_key not in ("P",) and cd >= 8:
        parts.append(f"{cd}s cooldown at rank 1 — punish hard when it's down.")

    if spell_key == "R" and not is_key:
        parts.append(f"Ultimate — {name} is their biggest teamfight threat. Track its cooldown.")

    if len(parts) <= (1 if is_key else 0):
        core = _condense_mechanic(_first_sentence(desc))
        if spell_key == "P":
            parts.append(f"{name}: {core}")
        else:
            parts.append(f"Respect {name} — {core}")

    tip = " ".join(parts)
    tip = re.sub(r"\s+", " ", tip).strip()
    return {"key": spell_key, "name": name, "tip": tip}


def _first_sentence(text: str) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return sentences[0] if sentences else text[:200]


def _condense_mechanic(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > 140:
        return text[:137] + "..."
    return text


def _generate_laning_tips(name: str, tags: list[str], spells: list[dict]) -> list[str]:
    tips: list[str] = []
    tag_set = set(tags)
    spell_text = " ".join(s.get("description", "") for s in spells).lower()
    key_spell = next((s for s in spells if s["key"] == _pick_key_ability(spells)), None)
    key_name = key_spell["name"] if key_spell else "key ability"
    key_cd = _first_cooldown(key_spell) if key_spell else None

    has_hook = any(w in spell_text for w in ("hook", "grab", "rocket grab"))
    has_shield = "shield" in spell_text
    has_dash = any(
        re.search(r"\b(dash|blink|leap)\b", s.get("description", "").lower())
        and "allies can dash" not in s.get("description", "").lower()
        for s in spells
    )

    if _is_jungle_champion(spell_text):
        tips.append(f"Invade {name} early — they are vulnerable before first item and camp setup.")
        tips.append(f"Track {name}'s clear path with wards; collapse on skirmishes at marked camps.")
    if has_hook:
        tips.append(f"Stand behind minions vs {name}'s hook — punish every miss on its long cooldown.")
    if has_shield:
        tips.append(f"Burst through {name}'s shields or wait for them to expire before committing.")
    if "Assassin" in tag_set:
        tips.append(f"Buy early defensive stats — {name} wins burst windows at level 6 and first item.")
    if "Marksman" in tag_set:
        tips.append(f"All-in early — {name} is weak levels 1-3 before first item spike.")
    if "Fighter" in tag_set or ("Tank" in tag_set and "Support" not in tag_set):
        tips.append(f"Kite and short-trade — {name} wins extended melee fights.")
    if "Mage" in tag_set and "Support" not in tag_set:
        tips.append(f"All-in when {name}'s key skillshot is on cooldown — mages are weak without it.")
    if has_dash:
        tips.append(f"Track {name}'s dash cooldown — they are much less threatening while mobility is down.")
    if key_cd and key_cd >= 10:
        tips.append(f"Punish when {key_name} is on cooldown (~{key_cd}s early).")

    generic = [
        f"Control vision around {name} — fog of war lets them land {key_name} for free.",
        f"Short trades prevent {name} from stacking passives or landing full combos.",
        f"Call jungle pressure when {name} pushes — immobile champions are gank targets.",
        f"Buy early boots to dodge skillshots and reposition against {name}.",
        f"Punish {name} when their ultimate is on cooldown — that's their biggest window.",
    ]
    for tip in generic:
        if len(tips) >= 5:
            break
        if tip not in tips:
            tips.append(tip)

    return tips[:5]


def _generate_power_spikes(name: str, tags: list[str], spells: list[dict]) -> list[str]:
    tag_set = set(tags)
    r_spell = next((s for s in spells if s["key"] == "R"), None)
    r_name = r_spell["name"] if r_spell else "ultimate"

    spikes = [f"Level 6: {r_name} unlocks — {name}'s kill pressure spikes significantly"]

    if "Support" in tag_set:
        spikes.append(f"First support item: {name}'s teamfight utility and peel spike hard")
    elif "Mage" in tag_set or "Assassin" in tag_set:
        spikes.append(f"First item completion: {name}'s burst damage becomes lethal in one rotation")
    elif "Marksman" in tag_set:
        spikes.append(f"First item (Kraken/IE): {name} DPS jumps — all-in before this spike")
    elif "Fighter" in tag_set or "Tank" in tag_set:
        spikes.append(f"First item (Trinity/Heartsteel): {name} wins extended trades and duels")
    else:
        spikes.append(f"First item spike: {name} reaches a major power increase")

    spikes.append(f"Level 11: Rank 2 {r_name} — stronger teamfight and pick potential")
    return spikes[:3]


def _generate_items(tags: list[str], spells: list[dict]) -> list[str]:
    items: list[str] = []
    spell_text = " ".join(s.get("description", "") for s in spells).lower()
    tag_set = set(tags)

    has_magic = "magic damage" in spell_text or "Mage" in tag_set
    has_physical = (
        "physical damage" in spell_text
        or "Fighter" in tag_set
        or "Assassin" in tag_set
        or "Marksman" in tag_set
    )
    has_cc = any(w in spell_text for w in ("stun", "root", "charm", "knockup", "suppress", "taunt", "fear"))
    has_heal = "heal" in spell_text
    has_burst = "Assassin" in tag_set or ("Mage" in tag_set and "Support" not in tag_set)

    if has_physical:
        items.append("Plated Steelcaps — reduces auto-attack and physical ability damage")
    if has_magic:
        items.append("Mercury's Treads — MR and tenacity vs magic damage and CC")
    if has_burst:
        items.append("Seeker's Armguard / Hexdrinker — survive all-in burst windows")
    if has_cc and not has_burst and not any("Mercury's Treads" in i for i in items):
        items.append("Mercury's Treads — tenacity reduces CC duration")
    if has_heal:
        items.append("Oblivion Orb / Bramble Vest — cut healing and sustain value")
    if "Assassin" in tag_set:
        items.append("Zhonya's Hourglass — stasis dodges assassination combo")
    if "Marksman" in tag_set and "Tank" in tag_set:
        items.append("Randuin's Omen — reduce crit DPS from ADC")

    if not items:
        items = [
            "Plated Steelcaps or Mercury's Treads — match their primary damage type",
            "Early defensive component — survive their first all-in",
            "Control Wards — deny fog-of-war setups",
        ]

    fallbacks = [
        "Control Wards — deny fog-of-war setups",
        "Early Boots — dodge skillshots and reposition",
        "Stopwatch / Seeker's Armguard — survive burst windows",
    ]
    for fb in fallbacks:
        if len(items) >= 3:
            break
        if fb not in items:
            items.append(fb)

    def _item_key(item: str) -> str:
        return item.split("—")[0].strip().lower()

    seen: set[str] = set()
    unique: list[str] = []
    for item in items:
        key = _item_key(item)
        if key not in seen:
            seen.add(key)
            unique.append(item)

    return unique[:3]
