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

# Refined pools for common tag combinations
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

SUMMARY_TEMPLATES: dict[str, str] = {
    "Fighter": "{name} wins extended melee trades and wants to stick to you. Respect their all-in windows and kite between cooldowns.",
    "Tank": "{name} soaks damage and enables teamfights with CC. Avoid extended fights — focus % HP damage and kiting.",
    "Mage": "{name} wins with skillshot combos and burst from range. Respect cooldown windows and punish missed spells.",
    "Assassin": "{name} wins short burst windows and roams. Play safe when their gap-close and ult are available.",
    "Marksman": "{name} scales with items and wants to auto-attack freely. Punish early weakness and hard-engage before they itemize.",
    "Support": "{name} enables their team with peel or engage. Target them in fights and respect their key CC or shield tools.",
}

TAG_COMBO_SUMMARIES: dict[frozenset[str], str] = {
    frozenset({"Support", "Mage"}): "{name} is an enchanter support who wins by shielding, buffing, and controlling space. Hard engage and burst punish slow shield reactions.",
    frozenset({"Support", "Tank"}): "{name} is a tank support who wins lane with CC chains and body-blocking. Poke and % HP damage reduce their frontline value.",
    frozenset({"Fighter", "Tank"}): "{name} is a juggernaut who wins long trades and becomes unkillable with items. Kite, short-trade, and respect their W/R power spikes.",
    frozenset({"Assassin", "Fighter"}): "{name} is a skirmisher who wins with dash chains and burst combos. Point-and-click CC and early all-ins shut them down.",
    frozenset({"Mage", "Assassin"}): "{name} is a burst mage who wins with spell rotation and pick potential. Magic resist and hard CC before they commit win the matchup.",
}

# Keywords for ability tip transformation
CC_KEYWORDS = {
    "stun": "Stuns — respect the CC window and don't face-check without vision.",
    "root": "Roots in place — sidestep or hide behind minions; allies may follow up.",
    "knockup": "Knockup — unstoppable CC; don't commit when this ability is available.",
    "knock back": "Knockback — can disrupt your engage or reposition you into danger.",
    "suppress": "Suppression — cannot be cleansed with QSS; play safe when it's up.",
    "silence": "Silence — removes your ability to cast spells; disengage immediately.",
    "charm": "Charm — forces you to walk toward them; sidestep or hide behind minions.",
    "fear": "Fear — forces retreat; don't chase into fog when this is available.",
    "taunt": "Taunt — forces you to attack them; back off when this is active.",
    "slow": "Applies slow — movement speed reduction makes you vulnerable to follow-up.",
    "pull": "Pulls you toward them — stay out of range or bait it on cooldown.",
    "grab": "Grab/hook — hide behind minions and punish the long cooldown if it misses.",
}

MECHANIC_KEYWORDS = {
    "shield": "Grants a shield — burst through it quickly or wait for it to expire before committing.",
    "heal": "Heals — short trades prevent healing value; buy anti-heal.",
    "untargetable": "Makes them untargetable — don't waste key abilities while it's active.",
    "invulnerable": "Invulnerability — disengage and wait it out; do not burn cooldowns.",
    "true damage": "True damage — ignores armor/MR; respect the raw damage output.",
    "execute": "Execute — lethal at low HP; recall or heal before the threshold.",
    "percent": "% HP damage — stacking HP items helps them less; still respect the raw numbers.",
    "magic damage": "Deals magic damage — consider Mercury's Treads or MR items.",
    "physical damage": "Deals physical damage — consider Plated Steelcaps or armor.",
    "reset": "Resets on kill — do not chase after takedowns; they will outrun or snowball.",
    "global": "Global range — recall at low HP even without direct vision.",
    "steals": "Steals stats or abilities — avoid isolated 1v1s when this is available.",
}

ULT_THREAT_WORDS = ("ultimate", "global", "execute", "suppress", "knockup", "untargetable", "invulnerable")


def generate_guide(detail: dict[str, Any]) -> dict[str, Any]:
    """Build a full counter guide from champion detail."""
    tags = detail.get("tags", [])
    name = detail["name"]
    spells = detail.get("spells", [])

    return {
        "summary": _generate_summary(name, tags),
        "counter_picks": _generate_counter_picks(tags),
        "ability_tips": [_generate_ability_tip(spell) for spell in spells],
        "laning_tips": _generate_laning_tips(name, tags, spells),
        "power_spikes": _generate_power_spikes(name, tags, spells),
        "items_to_consider": _generate_items(tags, spells),
    }


def _generate_summary(name: str, tags: list[str]) -> str:
    tag_set = frozenset(tags)
    for combo, template in TAG_COMBO_SUMMARIES.items():
        if combo.issubset(tag_set):
            return template.format(name=name)

    primary = tags[0] if tags else "Fighter"
    template = SUMMARY_TEMPLATES.get(primary, SUMMARY_TEMPLATES["Fighter"])
    if len(tags) > 1:
        secondary = tags[1]
        template = (
            f"{name} is a {primary.lower()}/{secondary.lower()} who "
            f"{template.split(' wins ', 1)[1] if ' wins ' in template else template.split('. ', 1)[-1]}"
        )
        return template
    return template.format(name=name)


def _generate_counter_picks(tags: list[str]) -> list[dict[str, str]]:
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

    seen: set[str] = set()
    unique: list[dict[str, str]] = []
    for entry in pool:
        champ = entry["champion"]
        if champ not in seen:
            seen.add(champ)
            unique.append(entry)
        if len(unique) >= 5:
            break

    return unique[:5]


def _generate_ability_tip(spell: dict[str, Any]) -> dict[str, str]:
    key = spell["key"]
    name = spell["name"]
    desc = spell.get("description", "")
    desc_lower = desc.lower()

    tip_parts: list[str] = []

    if key == "R":
        tip_parts.append(f"ULTIMATE — {name} is their biggest teamfight threat.")
    elif key == "P":
        tip_parts.append(f"Passive — learn when {name} activates in lane trades.")

    for keyword, advice in CC_KEYWORDS.items():
        if keyword in desc_lower:
            tip_parts.append(advice)
            break

    for keyword, advice in MECHANIC_KEYWORDS.items():
        if keyword in desc_lower:
            tip_parts.append(advice)
            break

    if "allies can dash" in desc_lower or "ally can dash" in desc_lower:
        tip_parts.append("Allies can dash to the target — don't get caught isolated near rooted teammates.")
    elif re.search(r"\b(dash|blink|leap)\b", desc_lower) and key != "P":
        tip_parts.append("Mobility tool — track its cooldown before committing to trades.")

    cooldown = spell.get("cooldown", "")
    if cooldown and key not in ("P", "R"):
        first_cd = cooldown.split("/")[0]
        if first_cd.isdigit() and 8 <= int(first_cd) <= 30:
            tip_parts.append(f"~{first_cd}s cooldown early — punish hard when it's down.")

    core = _first_sentence(desc)
    if core:
        actionable = _make_actionable(core, name, key)
        if not _is_redundant(actionable, tip_parts):
            tip_parts.append(actionable)

    if not tip_parts:
        tip_parts.append(f"Respect {name} — play around its cooldown in lane.")

    return {"key": key, "name": name, "tip": " ".join(tip_parts)}


def _is_redundant(actionable: str, existing: list[str]) -> bool:
    """Skip actionable line if it repeats an earlier keyword advice."""
    lower = actionable.lower()
    for part in existing:
        pl = part.lower()
        if "shield" in pl and "shield" in lower:
            return True
        if "root" in pl and "root" in lower:
            return True
        if "slow" in pl and "slow" in lower:
            return True
    return False


def _first_sentence(text: str) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return sentences[0] if sentences else text[:200]


def _make_actionable(core: str, name: str, key: str) -> str:
    """Turn raw description into a 'respect this' tip."""
    core_lower = core.lower()

    if "root" in core_lower:
        return f"When {name} ({key}) lands, expect follow-up — don't face-check brush or straight-line paths."
    if "shield" in core_lower:
        return f"{name} ({key}) shields allies — burst through the shield or wait for it to break before committing."
    if "dash" in core_lower or "blink" in core_lower:
        return f"{name} ({key}) enables ally dashes or self-reposition — track who's in range to follow up."
    if "slow" in core_lower:
        return f"{name} ({key}) slows on detonation — don't stand clustered or you'll all get hit."
    if "summon" in core_lower:
        return f"{name} ({key}) summons a pet — focus it down or kite; it adds significant DPS and CC."
    if "brush" in core_lower or "bush" in core_lower:
        return f"{name} ({key}) creates brush — ward it immediately; bonus damage and vision advantage inside."
    if "jungle" in core_lower or "monster" in core_lower:
        return f"{name} ({key}) is jungle-focused — in lane, focus on their Q/W/E threat instead."
    if "stun" in core_lower or "knockup" in core_lower:
        return f"{name} ({key}) is hard CC — don't commit when it's available; sidestep or hide behind minions."
    if "heal" in core_lower:
        return f"{name} ({key}) heals — take short trades and buy anti-heal to cut sustain."
    if "damage" in core_lower:
        return f"Respect {name} ({key}) damage — {_condense_mechanic(core)}"

    return f"Respect {name} ({key}): {_condense_mechanic(core)}"


def _condense_mechanic(text: str) -> str:
    """Shorten a description sentence for tip readability."""
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > 120:
        return text[:117] + "..."
    return text


def _generate_laning_tips(name: str, tags: list[str], spells: list[dict]) -> list[str]:
    tips: list[str] = []
    tag_set = set(tags)
    is_ranged = "Mage" in tag_set or "Marksman" in tag_set
    is_melee = "Fighter" in tag_set or "Assassin" in tag_set or ("Tank" in tag_set and "Support" not in tag_set)
    is_support = "Support" in tag_set
    is_assassin = "Assassin" in tag_set

    spell_text = " ".join(s.get("description", "") for s in spells).lower()
    has_hook = any(w in spell_text for w in ("hook", "grab", "pull"))
    has_shield = "shield" in spell_text
    has_poke = any(w in spell_text for w in ("skillshot", "range", "line", "projectile")) or is_ranged
    has_dash = any(
        re.search(r"\b(dash|blink|leap)\b", s.get("description", "").lower())
        and "allies can dash" not in s.get("description", "").lower()
        for s in spells
    )

    if has_hook:
        tips.append(f"Stand behind minions vs {name}'s hook/grab — punish every miss on its long cooldown.")
    if has_shield:
        tips.append(f"Burst through {name}'s shields quickly or wait for them to expire before committing.")
    if is_ranged and not is_support:
        tips.append(f"All-in when {name}'s key skillshot is on cooldown — ranged champs are weak without it.")
    if is_melee:
        tips.append(f"Kite and short-trade — {name} wins extended melee fights; disengage after one rotation.")
    if is_assassin:
        tips.append(f"Buy early defensive stats — {name} wins burst windows at level 6 and first item.")
    if is_support and "Mage" in tag_set:
        tips.append(f"Hard engage beats {name} — collapse before shields and peel come online.")
    if has_dash:
        tips.append(f"Track {name}'s dash cooldown — they are much less threatening while mobility is down.")
    if has_poke and is_support:
        tips.append(f"Don't stand in straight lines — {name}'s poke adds up; trade when their mana is low.")
    if "brush" in spell_text or "bush" in spell_text:
        tips.append(f"Ward brush that {name} creates — they gain combat advantages inside it.")

    # Fill to 5 with tag-generic tips
    generic = [
        f"Punish {name} when their ultimate is on cooldown — that's their biggest threat window.",
        f"Control vision around {name} — fog of war lets them land key abilities for free.",
        f"Short trades prevent {name} from stacking passives or landing full combos.",
        f"Call jungle pressure when {name} pushes — immobile champions are gank targets.",
        f"Buy early boots to dodge skillshots and reposition against {name}.",
    ]
    for tip in generic:
        if len(tips) >= 5:
            break
        if tip not in tips:
            tips.append(tip)

    return tips[:5]


def _generate_power_spikes(name: str, tags: list[str], spells: list[dict]) -> list[str]:
    spikes: list[str] = []
    tag_set = set(tags)

    # Find R cooldown for level 6 context
    r_spell = next((s for s in spells if s["key"] == "R"), None)
    r_name = r_spell["name"] if r_spell else "ultimate"

    spikes.append(f"Level 6: {r_name} unlocks — {name}'s kill pressure spikes significantly")

    if "Support" in tag_set:
        spikes.append(f"First support item: {name}'s teamfight utility and peel spike hard")
    elif "Mage" in tag_set or "Assassin" in tag_set:
        spikes.append(f"First item completion: {name}'s burst damage becomes lethal in one rotation")
    elif "Marksman" in tag_set:
        spikes.append(f"First item (IE/Navori): {name} auto-attack DPS jumps — all-in before this spike")
    elif "Fighter" in tag_set or "Tank" in tag_set:
        spikes.append(f"First item (Trinity/Heartsteel): {name} wins extended trades and duels")

    spikes.append(f"Level 11: Rank 2 {r_name} — stronger teamfight and pick potential")

    if "Assassin" in tag_set:
        spikes.append(f"First back with Serrated Dirk: {name} has lethal combo damage pre-6 items")
    elif "Marksman" in tag_set:
        spikes.append(f"2+ items: {name} becomes a teamfight hypercarry — hard engage before they scale")

    return spikes[:4]


def _generate_items(tags: list[str], spells: list[dict]) -> list[str]:
    items: list[str] = []
    spell_text = " ".join(s.get("description", "") for s in spells).lower()

    has_magic = "magic damage" in spell_text or "Mage" in tags
    has_physical = "physical damage" in spell_text or "Fighter" in tags or "Assassin" in tags or "Marksman" in tags
    has_cc = any(w in spell_text for w in ("stun", "root", "charm", "knockup", "suppress", "taunt", "fear"))
    has_heal = "heal" in spell_text
    has_shield = "shield" in spell_text
    has_burst = "Assassin" in tags or ("Mage" in tags and "Support" not in tags)

    if has_physical:
        items.append("Plated Steelcaps — reduces auto-attack and physical ability damage")
    if has_magic:
        items.append("Mercury's Treads — MR and tenacity vs magic damage and CC")
    if has_cc and "Mage" in tags:
        items.append("Verdant Barrier / Hexdrinker — early survivability vs burst combos")
    if has_burst:
        items.append("Seeker's Armguard / Hexdrinker — survive all-in burst windows")
    if has_heal or has_shield:
        items.append("Oblivion Orb / Bramble Vest — cut healing and shield sustain value")
    if "Marksman" in tags:
        items.append("Randuin's Omen / Thornmail — reduce crit DPS if you're a tank")
    if "Tank" in tags:
        items.append("Lord Dominik's Regards / Void Staff — % HP and penetration vs tanks")
    if "Assassin" in tags:
        items.append("Zhonya's Hourglass — stasis dodges assassination combo")

    if not items:
        items = [
            "Plated Steelcaps or Mercury's Treads — match their primary damage type",
            "Early defensive component — survive their first all-in",
            "Control Wards — deny fog-of-war setups",
        ]

    seen: set[str] = set()
    unique: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            unique.append(item)

    return unique[:4]
