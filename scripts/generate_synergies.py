"""Generate premium synergy guides for all champions using tags + known duo combos."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.counters.ddragon import get_champion_detail, list_champions  # noqa: E402

SYNERGY_FILE = ROOT / "data" / "synergies" / "synergies.json"

PREMIUM_CHAMPIONS: frozenset[str] = frozenset({
    "Garen", "Darius", "Yasuo", "Lux", "Zed",
    "Ahri", "Mordekaiser", "Sett", "Thresh", "Jinx",
})

# (partner, role, reason, strength 55-95)
KNOWN_DUO_SYNERGIES: dict[str, list[tuple[str, str, str, int]]] = {
    "Yasuo": [
        ("Malphite", "Top/Jungle", "Malphite R knockup guarantees Yasuo R on the entire team — the classic wombo combo.", 95),
        ("Diana", "Mid/Jungle", "Diana R pulls and knocks up enemies for instant Last Breath.", 92),
        ("Gragas", "Jungle/Mid", "Gragas R displaces enemies into Yasuo's tornado or knocks them airborne.", 90),
        ("Alistar", "Support", "Headbutt + Pulverize knockup sets up tornado without landing Q first.", 88),
        ("Wukong", "Top/Jungle", "Cyclone R knockup feeds Yasuo's ultimate across the whole teamfight.", 87),
        ("Amumu", "Jungle", "Curse of the Sad Mummy root and stun chains directly into Last Breath.", 86),
        ("Jarvan IV", "Jungle", "Cataclysm trap + knockup from flag combo creates a kill zone for Yasuo R.", 85),
        ("Rell", "Support", "Rell R pulls enemies together — perfect setup for knockup and Yasuo ult.", 84),
        ("Nautilus", "Support", "R knockup on carry plus hook pick into Yasuo follow-up.", 82),
        ("Orianna", "Mid", "Shockwave on an engager who lands in the middle of the enemy team.", 80),
    ],
    "Jinx": [
        ("Thresh", "Support", "Dark Passage saves Jinx during Get Excited! chases; hook sets up rocket poke.", 95),
        ("Lulu", "Support", "Whimsy peel and Wild Growth let Jinx free-fire rockets in teamfights.", 92),
        ("Nautilus", "Support", "Hard engage locks targets for rocket barrages and passive reset chains.", 88),
        ("Leona", "Support", "Solar Flare plus Zenith Blade guarantees Jinx follow-up damage.", 87),
        ("Renata Glasc", "Support", "Bailout revives Jinx mid-fight so passive resets keep rolling.", 86),
        ("Milio", "Support", "Cleanses CC and speed boosts extend Jinx's kiting and rocket uptime.", 85),
        ("Blitzcrank", "Support", "Hook picks start fights Jinx finishes with rockets and passive resets.", 84),
        ("Braum", "Support", "Unbreakable blocks skillshots while Jinx stacks passive from safe range.", 80),
        ("Yuumi", "Support", "Attach and amplify Jinx hypercarry scaling into the late game.", 78),
        ("Karma", "Support", "Shield and speed let Jinx reposition for trap and rocket angles.", 76),
    ],
    "Thresh": [
        ("Jinx", "ADC", "Lantern enables Jinx resets; Flay positions enemies for rocket splash.", 95),
        ("Lucian", "ADC", "Hook into Lucian burst combo — Passives proc instantly off Thresh CC.", 90),
        ("Draven", "ADC", "Axe catch off hook; Thresh peel keeps Draven alive for snowball.", 88),
        ("Samira", "ADC", "Thresh CC triggers Samira style rating for fast S and R.", 87),
        ("Jhin", "ADC", "Root and hook guarantee Jhin W root and fourth shot execute.", 86),
        ("Caitlyn", "ADC", "Hook into trap headshot combo — classic lane bully pattern.", 85),
        ("Aphelios", "ADC", "Peel and lantern let Aphelios swap weapons safely in extended fights.", 82),
        ("Kalista", "ADC", "Thresh R disengage plus lantern synergizes with Kalista hop rhythm.", 80),
        ("Yasuo", "Mid", "Hook into knockup for instant Last Breath without Yasuo landing Q.", 78),
        ("Orianna", "Mid", "Thresh flays enemies onto Orianna ball for Shockwave.", 76),
    ],
    "Malphite": [
        ("Yasuo", "Mid/ADC", "Unstoppable Force knockup is the gold-standard Yasuo R setup.", 95),
        ("Orianna", "Mid", "Malphite R carries the ball into the enemy backline for Shockwave.", 92),
        ("Miss Fortune", "ADC", "MF channels Bullet Time while Malphite R keeps enemies in the cone.", 90),
        ("Yasuo", "Mid", "Double knockup wombo — Malphite R into Yasuo Last Breath.", 95),
        ("Jinx", "ADC", "Teamfight engage lets Jinx open with rockets on grouped enemies.", 82),
        ("Veigar", "Mid", "Enemies knocked into Event Horizon edge for guaranteed stun.", 80),
        ("Anivia", "Mid", "R knockup holds enemies inside Glacial Storm and wall choke.", 78),
        ("Brand", "Support/Mid", "AoE knockup groups enemies for Pyroclasm bounces.", 76),
        ("Lissandra", "Mid", "Malphite R plus Lissandra R on carry creates unbreakable CC chain.", 75),
        ("Ashe", "ADC", "Permafrost slow plus Malphite R creates pick and teamfight engage.", 74),
    ],
    "Lux": [
        ("Morgana", "Support", "Double binding — Dark Binding into Light Binding guarantees pick kills.", 90),
        ("Caitlyn", "ADC", "Lux root sets Caitlyn trap headshot for massive lane poke.", 88),
        ("Jhin", "ADC", "Root guarantees Jhin W and fourth shot — long-range execute duo.", 86),
        ("Ezreal", "ADC", "Artillery mage poke from two angles overwhelms lane.", 82),
        ("Jarvan IV", "Jungle", "Cataclysm trap plus Lux R laser on immobile targets.", 80),
        ("Yasuo", "Mid", "Lux R knockup sets up Last Breath from range.", 78),
        ("Seraphine", "Support", "Double long-range charm/root and shield for poke lanes.", 76),
        ("Xerath", "Mid", "Artillery duo — zone entire map with combined ult range.", 75),
        ("Ziggs", "Mid", "Siege and poke from two angles breaks towers without fighting.", 74),
        ("Swain", "Support", "Root into Nevermove pull for extended CC chain.", 72),
    ],
    "Garen": [
        ("Yuumi", "Support", "Attach Garen for unkillable spinning demon — heals and speed amplify his stickiness.", 92),
        ("Lulu", "Support", "Wild Growth plus Garen R execute makes him unkillable in the middle of the enemy team.", 88),
        ("Leona", "Support", "Leona locks targets while Garen runs them down with Judgment.", 85),
        ("Nautilus", "Support", "Hook and root guarantee Garen can reach immobile carries.", 82),
        ("Senna", "Support", "Senna root plus Garen flash-Q silence combo for picks.", 80),
        ("Taric", "Support", "Double tank frontline; Taric R invulnerability during Garen spin.", 78),
        ("Braum", "Support", "Braum passive stacks with Garen auto-attack focus fire.", 76),
        ("Morgana", "Support", "Black Shield lets Garen walk through CC to reach carries.", 75),
        ("Sett", "Top", "Double frontline bruisers that dive and split attention.", 72),
        ("Darius", "Top", "Lane kingdom duo — both punish extended trades and lack of escape.", 70),
    ],
    "Darius": [
        ("Yuumi", "Support", "Yuumi heals through Darius bleed trades and adds AP to Noxian Guillotine.", 90),
        ("Lulu", "Support", "Speed and shield let Darius reach carries and survive focus fire.", 86),
        ("Thresh", "Support", "Hook and Flay bring targets into Darius Apprehend range.", 84),
        ("Leona", "Support", "Hard CC locks targets for Darius to stack passive and ult.", 82),
        ("Nautilus", "Support", "Root guarantees Darius can Apprehend and stack Hemorrhage.", 80),
        ("Garen", "Top", "Double lane bully — enemies cannot trade into both.", 78),
        ("Sett", "Top", "Front-to-back bruiser duo that splits enemy focus.", 76),
        ("Jarvan IV", "Jungle", "Cataclysm trap keeps enemies in Darius spin and bleed zone.", 75),
        ("Hecarim", "Jungle", "Hecarim E knockback into Darius Apprehend for reposition picks.", 74),
        ("Morgana", "Support", "Black Shield on Darius during ghost flash all-ins.", 72),
    ],
    "Ahri": [
        ("Evelynn", "Jungle", "Charm sets up Eve charm — double charm CC chain from fog.", 88),
        ("Jarvan IV", "Jungle", "Cataclysm trap plus Ahri charm guarantees Spirit Rush cleanup.", 86),
        ("Elise", "Jungle", "Cocoon plus Ahri charm for layered pick CC.", 84),
        ("Nautilus", "Support", "Hook into charm for guaranteed pick in bot or roam.", 82),
        ("Thresh", "Support", "Hook plus charm extends pick range across the map.", 80),
        ("Lee Sin", "Jungle", "Lee kick into Ahri charm for reposition combos.", 78),
        ("Amumu", "Jungle", "Amumu Q plus Ahri charm chain CC in teamfights.", 76),
        ("Vi", "Jungle", "Vi R lockdown plus Ahri charm for unbreakable CC.", 75),
        ("Lulu", "Support", "Peel and speed for Ahri to charm safely and Spirit Rush out.", 74),
        ("Poppy", "Jungle", "Poppy E into wall plus Ahri charm for stun chain.", 72),
    ],
    "Zed": [
        ("Taliyah", "Mid/Jungle", "Taliyah W wall plus Zed R for guaranteed isolation kills.", 88),
        ("Nocturne", "Jungle", "Paranoia darkness plus Zed R on isolated target — global pick duo.", 86),
        ("Pyke", "Support", "Double execute reset potential in skirmishes and roams.", 84),
        ("Leona", "Support", "Hard CC guarantees Zed can land shurikens and all-in.", 82),
        ("Thresh", "Support", "Hook sets up Death Mark without Zed using gap closer.", 80),
        ("Yuumi", "Support", "Attach after Zed R for cleanup and escape.", 78),
        ("Talon", "Mid", "Double assassin roam pressure — one creates, one finishes.", 76),
        ("Kha'Zix", "Jungle", "Isolation and reset chain from two angles.", 75),
        ("Elise", "Jungle", "Cocoon into Death Mark for guaranteed picks.", 74),
        ("Syndra", "Mid", "Scatter stun into Zed all-in on immobile targets.", 72),
    ],
    "Mordekaiser": [
        ("Yuumi", "Support", "Yuumi in Realm of Death makes 1v1 a 2v1 — nearly unlosable.", 92),
        ("Orianna", "Mid", "Morde R isolates carry; Orianna shockwave cleans up the 4v4.", 86),
        ("Lulu", "Support", "Shield and speed during Realm of Death skirmishes.", 84),
        ("Thresh", "Support", "Hook into Morde pull for double displacement.", 82),
        ("Nautilus", "Support", "Root guarantees Morde can hit Q and pull.", 80),
        ("Amumu", "Jungle", "Amumu R groups enemies for Morde R on carry.", 78),
        ("Morgana", "Support", "Black Shield on Morde during all-in and Realm fights.", 76),
        ("Brand", "Support", "AoE burn while Morde isolates the highest-value target.", 74),
        ("Swain", "Support", "Drain tank duo that wins extended frontline fights.", 72),
        ("Darius", "Top", "Double juggernaut — enemies cannot kill both before losing a carry.", 70),
    ],
    "Sett": [
        ("Yasuo", "Mid", "Sett R knockup into Yasuo Last Breath — front-to-back wombo.", 90),
        ("Orianna", "Mid", "Sett R carries ball carrier into enemy team for Shockwave.", 88),
        ("Yuumi", "Support", "Attach during Sett W and R for amplified damage and healing.", 86),
        ("Lulu", "Support", "Wild Growth when Sett W is charging in the middle of 5 enemies.", 84),
        ("Thresh", "Support", "Flay positions enemies for Sett E and W center.", 82),
        ("Jinx", "ADC", "Sett R throws enemy into Jinx rocket range for fight start.", 80),
        ("Miss Fortune", "ADC", "Sett R groups enemies in MF Bullet Time cone.", 78),
        ("Darius", "Top", "Frontline bruiser duo that splits attention and wins extended fights.", 76),
        ("Garen", "Top", "Double frontline — Sett W true damage plus Garen spin.", 74),
        ("Pantheon", "Support/Mid", "Pantheon R plus Sett engage for global fight presence.", 72),
    ],
    "Samira": [
        ("Nautilus", "Support", "Nautilus CC instantly raises Samira style to S for Blade Whirl.", 92),
        ("Leona", "Support", "Triple CC from Leona guarantees fast style rating.", 90),
        ("Alistar", "Support", "Headbutt knockup plus pulverize for style and R.", 88),
        ("Thresh", "Support", "Hook and flay into Samira E for style and burst.", 86),
        ("Rell", "Support", "Rell W dismount knockup triggers Samira style instantly.", 84),
        ("Rakan", "Support", "Charm plus knockup for fast style buildup.", 82),
        ("Braum", "Support", "Passive stacks plus unbreakable for safe style building.", 80),
        ("Taric", "Support", "Double stun from E sync for style and invulnerability.", 78),
        ("Pyke", "Support", "Hook into Samira all-in for bot lane snowball.", 76),
        ("Yuumi", "Support", "Attach during Inferno Trigger for amplified cleanup.", 74),
    ],
    "Miss Fortune": [
        ("Amumu", "Jungle", "Amumu R root holds enemies in Bullet Time for full channel.", 95),
        ("Leona", "Support", "Solar Flare plus Zenith Blade root for Bullet Time setup.", 90),
        ("Morgana", "Support", "Dark Binding plus Bullet Time — classic bot lane wombo.", 88),
        ("Nautilus", "Support", "R knockup groups enemies in cone.", 86),
        ("Orianna", "Mid", "Shockwave groups enemies for full Bullet Time channel.", 84),
        ("Malphite", "Top/Jungle", "Unstoppable Force knockup into Bullet Time.", 92),
        ("Jarvan IV", "Jungle", "Cataclysm trap for guaranteed Bullet Time value.", 82),
        ("Seraphine", "Support", "Double ult channel — MF Bullet Time plus Seraphine R.", 80),
        ("Yuumi", "Support", "Attach during Bullet Time for safe full channel.", 78),
        ("Lulu", "Support", "Wild Growth peel while MF channels in teamfight.", 76),
    ],
    "Orianna": [
        ("Malphite", "Top/Jungle", "Malphite R carries ball for perfect Shockwave.", 95),
        ("Hecarim", "Jungle", "Hecarim R fear into ball Shockwave on grouped enemies.", 90),
        ("Wukong", "Top/Jungle", "Cyclone knockup groups for Shockwave.", 88),
        ("Jarvan IV", "Jungle", "Cataclysm trap plus Shockwave on trapped enemies.", 86),
        ("Sett", "Top", "Sett R throws enemy into ball range for follow-up Shockwave.", 84),
        ("Rell", "Support", "Rell R pull into Shockwave center.", 82),
        ("Amumu", "Jungle", "Curse groups for Shockwave.", 80),
        ("Sejuani", "Jungle", "Glacial Prison plus Shockwave CC chain.", 78),
        ("Gragas", "Jungle", "Gragas R displaces into ball.", 76),
        ("Nocturne", "Jungle", "Paranoia darkness plus ball delivery on carry.", 74),
    ],
    "Kalista": [
        ("Taric", "Support", "Taric R invulnerability during Kalista all-in and teamfight.", 95),
        ("Renata Glasc", "Support", "Bailout saves Kalista mid-hop for extended fight.", 90),
        ("Thresh", "Support", "Lantern plus hook for Kalista hop rhythm.", 88),
        ("Braum", "Support", "Unbreakable plus passive stacks with Kalista attack speed.", 86),
        ("Nautilus", "Support", "Hard engage for Kalista to hop into and stack spears.", 84),
        ("Lulu", "Support", "Speed and shield for hop kiting.", 82),
        ("Morgana", "Support", "Black Shield prevents hop-interrupting CC.", 80),
        ("Rakan", "Support", "Engage plus charm for Kalista follow-up.", 78),
        ("Leona", "Support", "Lockdown for Kalista to stack Rend.", 76),
        ("Yuumi", "Support", "Attach during Kalista hop fights.", 74),
    ],
    "Xayah": [
        ("Rakan", "Support", "Lovers' duo — Rakan engage plus Xayah E root for guaranteed picks.", 98),
        ("Rakan", "Support", "Battle Dance and Featherstorm combo is the signature wombo.", 98),
        ("Thresh", "Support", "Hook into Xayah E root for pick kills.", 82),
        ("Leona", "Support", "Hard CC guarantees E root on immobile targets.", 80),
        ("Nautilus", "Support", "Root into feather recall for burst.", 78),
        ("Lulu", "Support", "Peel for Xayah to safely stack feathers.", 76),
        ("Braum", "Support", "Shield blocks while Xayah sets up E.", 74),
        ("Rell", "Support", "Rell engage groups for R featherstorm.", 72),
        ("Amumu", "Jungle", "Amumu R groups for E and R.", 70),
        ("Jarvan IV", "Jungle", "Cataclysm trap for feather recall.", 68),
    ],
    "Rakan": [
        ("Xayah", "ADC", "Battle Dance plus Featherstorm — the premier bot lane duo.", 98),
        ("Xayah", "ADC", "Rakan engage sets up Xayah E root and R damage.", 98),
        ("Samira", "ADC", "Rakan knockup triggers Samira style instantly.", 84),
        ("Jinx", "ADC", "Engage lets Jinx follow with rockets.", 82),
        ("Lucian", "ADC", "Rakan W plus Lucian burst combo.", 80),
        ("Tristana", "ADC", "Jump plus Rakan engage for all-in.", 78),
        ("Kai'Sa", "ADC", "Rakan charm plus Kai'Sa passive proc.", 76),
        ("Yasuo", "Mid", "Rakan R charm knockup into Last Breath.", 74),
        ("Orianna", "Mid", "Rakan R into Shockwave.", 72),
        ("Jarvan IV", "Jungle", "Double engage with global R presence.", 70),
    ],
    "Lucian": [
        ("Braum", "Support", "Braum passive stacks instantly off Lucian double tap.", 92),
        ("Nami", "Support", "Ebb and Flow bounce plus Lucian E for lane dominance.", 88),
        ("Thresh", "Support", "Hook into Lucian full combo burst.", 86),
        ("Leona", "Support", "Lockdown for Lucian to proc passive repeatedly.", 84),
        ("Nautilus", "Support", "Root guarantees Lucian full rotation.", 82),
        ("Morgana", "Support", "Binding plus Lucian burst for picks.", 80),
        ("Rakan", "Support", "Engage plus charm for all-in.", 78),
        ("Yuumi", "Support", "Attach amplifies Lucian mid-game spike.", 76),
        ("Jarvan IV", "Jungle", "Cataclysm trap for Lucian R.", 74),
        ("Orianna", "Mid", "Ball delivery for Lucian all-in follow-up.", 72),
    ],
    "Kog'Maw": [
        ("Lulu", "Support", "Wild Growth and speed make Kog'Maw unkillable hypercarry.", 95),
        ("Yuumi", "Support", "Attach and heal through Kog's immobile positioning.", 92),
        ("Milio", "Support", "Cleanse CC and speed for Kog to free-fire.", 90),
        ("Renata Glasc", "Support", "Bailout revives Kog during Bio-Arcane Barrage.", 88),
        ("Braum", "Support", "Unbreakable blocks key skillshots while Kog shreds.", 84),
        ("Thresh", "Support", "Peel and lantern for immobile Kog.", 82),
        ("Nautilus", "Support", "Engage creates space for Kog to DPS.", 80),
        ("Taric", "Support", "Invulnerability during Kog R range fights.", 78),
        ("Karma", "Support", "Shield and speed for positioning.", 76),
        ("Janna", "Support", "Monsoon disengage saves Kog from divers.", 74),
    ],
    "Twitch": [
        ("Lulu", "Support", "Wild Growth during Rat-Ta-Tat-Tat makes Twitch unkillable.", 92),
        ("Yuumi", "Support", "Attach during spray for amplified damage.", 90),
        ("Taric", "Support", "Taric R invulnerability during Twitch R channel.", 88),
        ("Renata Glasc", "Support", "Bailout if Twitch gets focused during ult.", 86),
        ("Orianna", "Mid", "Shockwave groups for Twitch spray.", 82),
        ("Morgana", "Support", "Black Shield on Twitch during stealth engage.", 80),
        ("Braum", "Support", "Shield while Twitch positions for spray angle.", 78),
        ("Janna", "Support", "Peel after Twitch stealth engage.", 76),
        ("Karma", "Support", "Speed for Twitch reposition during ult.", 74),
        ("Milio", "Support", "Cleanse and speed for spray uptime.", 72),
    ],
    "Caitlyn": [
        ("Morgana", "Support", "Dark Binding into trap headshot — lane bully classic.", 92),
        ("Lux", "Support", "Light Binding into trap for long-range poke picks.", 90),
        ("Zyra", "Support", "Root into trap headshot combo.", 88),
        ("Lux", "Mid", "Double binding from bot and mid for picks.", 86),
        ("Nautilus", "Support", "Root guarantees trap placement.", 84),
        ("Leona", "Support", "Hard CC into trap headshot execute.", 82),
        ("Janna", "Support", "Peel for Caitlyn to trap control objectives.", 78),
        ("Thresh", "Support", "Hook into trap for pick kills.", 80),
        ("Bard", "Support", "Meeps plus trap zone control.", 76),
        ("Ashe", "ADC", "Double ADC poke — perm slow into trap.", 72),
    ],
    "Aphelios": [
        ("Thresh", "Support", "Peel and lantern for weapon swap safety.", 90),
        ("Lulu", "Support", "Protect while Aphelios cycles red/green weapons.", 88),
        ("Nautilus", "Support", "Engage creates space for weapon setup.", 86),
        ("Braum", "Support", "Shield blocks while Aphelios sets up calibrum marks.", 84),
        ("Renata Glasc", "Support", "Bailout during Aphelios all-in windows.", 82),
        ("Taric", "Support", "Invulnerability during extended teamfight DPS.", 80),
        ("Yuumi", "Support", "Attach amplifies late-game weapon mastery.", 78),
        ("Milio", "Support", "Cleanse CC during immobile weapon phases.", 76),
        ("Karma", "Support", "Shield and speed for repositioning.", 74),
        ("Leona", "Support", "Lockdown for calibrum mark follow-up.", 72),
    ],
    "Vayne": [
        ("Lulu", "Support", "Wild Growth plus Vayne Condemn peel — hypercarry protection.", 92),
        ("Taric", "Support", "Taric R during Vayne tumble fights.", 88),
        ("Thresh", "Support", "Lantern and peel for immobile Vayne.", 86),
        ("Poppy", "Top/Jungle", "Poppy W stops dashes — Vayne shreds tanks.", 82),
        ("Braum", "Support", "Shield and passive with Vayne attack speed.", 80),
        ("Renata Glasc", "Support", "Bailout during Vayne focus fire.", 78),
        ("Morgana", "Support", "Black Shield on Vayne during tumble.", 76),
        ("Janna", "Support", "Monsoon saves Vayne from divers.", 74),
        ("Yuumi", "Support", "Attach during Vayne late-game shred.", 72),
        ("Karma", "Support", "Speed for tumble kiting.", 70),
    ],
    "Ashe": [
        ("Ziggs", "Mid", "Global ult plus Enchanted Crystal Arrow pick combo.", 88),
        ("Jarvan IV", "Jungle", "Cataclysm trap plus Arrow for picks.", 86),
        ("Amumu", "Jungle", "Amumu R plus Arrow for layered CC.", 84),
        ("Sejuani", "Jungle", "Glacial Prison plus Arrow chain.", 82),
        ("Morgana", "Support", "Binding plus Arrow for bot lane picks.", 80),
        ("Nautilus", "Support", "Root into Arrow stun.", 78),
        ("Lux", "Support", "Double long-range CC.", 76),
        ("Braum", "Support", "Shield while Ashe kites with perm slow.", 74),
        ("Thresh", "Support", "Hook into Arrow for extended CC.", 72),
        ("Malphite", "Top", "Malphite R engage plus Ashe Arrow follow.", 70),
    ],
    "Jarvan IV": [
        ("Orianna", "Mid", "Cataclysm trap plus Shockwave on trapped enemies.", 92),
        ("Yasuo", "Mid", "EQ knockup in cataclysm for Last Breath.", 90),
        ("Miss Fortune", "ADC", "Cataclysm trap for full Bullet Time.", 88),
        ("Azir", "Mid", "Shurima shuffle into cataclysm.", 84),
        ("Anivia", "Mid", "Wall plus cataclysm creates unescapable zone.", 82),
        ("Lux", "Mid", "Laser on trapped targets.", 80),
        ("Gnar", "Top", "Gnar R into cataclysm wall stun.", 78),
        ("Veigar", "Mid", "Event Horizon edge on cataclysm.", 76),
        ("Brand", "Support", "AoE burn on trapped group.", 74),
        ("Ashe", "ADC", "Arrow on cataclysm targets.", 72),
    ],
    "Amumu": [
        ("Miss Fortune", "ADC", "Curse of the Sad Mummy plus Bullet Time — iconic combo.", 95),
        ("Yasuo", "Mid", "Amumu R knockup into Last Breath.", 90),
        ("Orianna", "Mid", "Shockwave on grouped Curse targets.", 88),
        ("Brand", "Support", "Pyroclasm bounces on grouped enemies.", 86),
        ("Vel'Koz", "Mid/ADC", "Lifeform Disintegration Ray on rooted group.", 84),
        ("Lux", "Mid", "Laser on immobile Curse targets.", 82),
        ("Anivia", "Mid", "Glacial Storm on grouped enemies.", 80),
        ("Katarina", "Mid", "Resets off grouped Curse targets.", 78),
        ("Jinx", "ADC", "Rocket splash on grouped enemies.", 76),
        ("Samira", "ADC", "Style rating off Amumu R.", 74),
    ],
    "Leona": [
        ("Samira", "ADC", "Triple CC raises Samira style to S instantly.", 92),
        ("Jinx", "ADC", "Lockdown for rocket follow-up.", 90),
        ("Lucian", "ADC", "Leona all-in plus Lucian burst.", 88),
        ("Miss Fortune", "ADC", "Solar Flare plus Bullet Time setup.", 86),
        ("Draven", "ADC", "Axe catch off Leona CC.", 84),
        ("Tristana", "ADC", "Jump plus Leona CC for all-in.", 82),
        ("Kai'Sa", "ADC", "Passive proc off Leona CC stack.", 80),
        ("Yasuo", "Mid", "Leona R stun into Last Breath.", 78),
        ("Orianna", "Mid", "Leona engage carries ball.", 76),
        ("Jarvan IV", "Jungle", "Double engage lockdown.", 74),
    ],
    "Nautilus": [
        ("Samira", "ADC", "Nautilus CC triggers Samira style for R.", 92),
        ("Jinx", "ADC", "Hook and root for rocket barrage.", 90),
        ("Lucian", "ADC", "Root for Lucian full rotation.", 88),
        ("Draven", "ADC", "Hook into axe catch.", 86),
        ("Kai'Sa", "ADC", "CC stacks Kai'Sa passive.", 84),
        ("Miss Fortune", "ADC", "R knockup groups for Bullet Time.", 82),
        ("Yasuo", "Mid", "R knockup into Last Breath.", 80),
        ("Orianna", "Mid", "Hook flay into ball.", 78),
        ("Ahri", "Mid", "Hook into charm.", 76),
        ("Jarvan IV", "Jungle", "Double tank engage.", 74),
    ],
    "Lulu": [
        ("Jinx", "ADC", "Wild Growth plus Get Excited! — classic hypercarry protection.", 92),
        ("Kog'Maw", "ADC", "Speed and shield for immobile hypercarry.", 95),
        ("Twitch", "ADC", "Wild Growth during spray.", 90),
        ("Vayne", "ADC", "Peel plus Condemn for self-peel duo.", 88),
        ("Aphelios", "ADC", "Protect during weapon swap windows.", 86),
        ("Kai'Sa", "ADC", "Speed for repositioning.", 84),
        ("Garen", "Top", "Wild Growth on spinning Garen.", 82),
        ("Darius", "Top", "Shield during ghost all-in.", 80),
        ("Sett", "Top", "Wild Growth during Sett W.", 78),
        ("Hecarim", "Jungle", "Speed boost amplifies Hecarim charge.", 76),
    ],
    "Yuumi": [
        ("Garen", "Top", "Attach Garen for unkillable spin — meme-tier but effective.", 92),
        ("Darius", "Top", "Heal through bleed trades; amplify Noxian Guillotine.", 90),
        ("Kog'Maw", "ADC", "Attach hypercarry for amplified Bio-Arcane Barrage.", 92),
        ("Jinx", "ADC", "Attach during Get Excited! chase.", 88),
        ("Sett", "Top", "Attach during Sett W and R.", 86),
        ("Mordekaiser", "Top", "2v1 in Realm of Death.", 90),
        ("Hecarim", "Jungle", "Speed plus attach for charge damage.", 84),
        ("Miss Fortune", "ADC", "Attach during Bullet Time channel.", 82),
        ("Twitch", "ADC", "Attach during spray.", 80),
        ("Dr. Mundo", "Top", "Double unkillable — heal stacking.", 78),
    ],
}

# Tag-based partner pools: champion tags -> recommended partners
TAG_PARTNERS: dict[str, list[tuple[str, str, str, int]]] = {
    "Marksman+Support": [
        ("Thresh", "Support", "Hook picks and lantern peel cover immobile ADC weaknesses.", 82),
        ("Lulu", "Support", "Enchanter peel lets your ADC scale safely into late game.", 80),
        ("Nautilus", "Support", "Hard engage creates space for ADC to DPS freely.", 78),
        ("Leona", "Support", "All-in CC guarantees ADC follow-up damage.", 76),
        ("Braum", "Support", "Unbreakable blocks key skillshots during extended trades.", 74),
    ],
    "Marksman+Tank": [
        ("Leona", "Support", "Tank engage frontline enables ADC positioning behind.", 80),
        ("Nautilus", "Support", "Hook and root guarantee ADC can output damage.", 78),
        ("Alistar", "Support", "W+Q combo creates pick windows for ADC.", 76),
        ("Rell", "Support", "R pull groups enemies for ADC AoE.", 74),
        ("Braum", "Support", "Frontline shield for safe farming.", 72),
    ],
    "Mage+Tank": [
        ("Amumu", "Jungle", "AoE CC groups enemies for mage burst.", 82),
        ("Malphite", "Top/Jungle", "R knockup sets up skillshot combos.", 80),
        ("Jarvan IV", "Jungle", "Cataclysm trap for guaranteed ability hits.", 78),
        ("Sejuani", "Jungle", "Glacial Prison plus mage follow-up.", 76),
        ("Nautilus", "Support", "Hook into mage CC chain.", 74),
    ],
    "Assassin+Tank": [
        ("Leona", "Support", "Hard CC guarantees assassin can land full combo.", 82),
        ("Nautilus", "Support", "Root and hook for pick setup.", 80),
        ("Jarvan IV", "Jungle", "Cataclysm isolates targets for assassination.", 78),
        ("Elise", "Jungle", "Cocoon into assassin burst.", 76),
        ("Thresh", "Support", "Hook extends pick range.", 74),
    ],
    "Fighter+Support": [
        ("Yuumi", "Support", "Attach amplifies bruiser all-in and sustain.", 82),
        ("Lulu", "Support", "Shield and speed for bruiser stickiness.", 80),
        ("Thresh", "Support", "Flay brings targets into melee range.", 78),
        ("Morgana", "Support", "Black Shield prevents CC during all-in.", 76),
        ("Nautilus", "Support", "CC chain for extended trades.", 74),
    ],
    "Tank+Mage": [
        ("Orianna", "Mid", "Ball delivery on engager for Shockwave.", 84),
        ("Brand", "Support", "AoE burn on grouped CC targets.", 80),
        ("Lux", "Mid", "Long-range laser on immobile targets.", 78),
        ("Vel'Koz", "Mid", "True damage on grouped enemies.", 76),
        ("Anivia", "Mid", "Wall and storm on CC'd targets.", 74),
    ],
    "Tank+Marksman": [
        ("Jinx", "ADC", "Engage creates rocket splash targets.", 80),
        ("Miss Fortune", "ADC", "Grouped CC enables full Bullet Time.", 82),
        ("Ashe", "ADC", "Permafrost plus engage for picks.", 76),
        ("Kai'Sa", "ADC", "Passive proc off CC stack.", 74),
        ("Samira", "ADC", "CC triggers style for Blade Whirl.", 78),
    ],
    "Assassin+Assassin": [
        ("Talon", "Mid", "Double mid pressure and roam chains.", 78),
        ("Nocturne", "Jungle", "Darkness plus isolation for picks.", 76),
        ("Pyke", "Support", "Double execute reset potential.", 74),
        ("Kha'Zix", "Jungle", "Isolation from two angles.", 72),
        ("Evelynn", "Jungle", "Charm setup from stealth.", 70),
    ],
}

ROLE_MAP: dict[str, str] = {
    "Marksman": "ADC",
    "Support": "Support",
    "Tank": "Top/Jungle",
    "Fighter": "Top/Jungle",
    "Mage": "Mid",
    "Assassin": "Mid/Jungle",
}

ENGAGE_CHAMPS = {
    "Malphite", "Amumu", "Leona", "Nautilus", "Alistar", "Rell", "Sejuani",
    "Jarvan IV", "Wukong", "Gragas", "Hecarim", "Rakan", "Ornn", "Sion",
    "Zac", "Maokai", "Poppy", "K'Sante", "Ambessa",
}

FOLLOWUP_CHAMPS = {
    "Yasuo", "Samira", "Miss Fortune", "Orianna",
    "Vel'Koz", "Brand", "Lux", "Anivia", "Katarina",
}

ENCHANTER_CHAMPS = {
    "Lulu", "Janna", "Yuumi", "Milio", "Renata Glasc", "Karma", "Soraka",
    "Nami", "Sona", "Seraphine", "Taric",
}

HYPERCARRY_CHAMPS = {
    "Jinx", "Kog'Maw", "Twitch", "Vayne", "Aphelios", "Smolder", "Zeri",
    "Kai'Sa", "Tristana",
}

def _champ_tags(name: str, all_champs: dict[str, dict]) -> list[str]:
    info = all_champs.get(name)
    return info["tags"] if info else []


def _primary_role(tags: list[str]) -> str:
    for tag in tags:
        if tag in ROLE_MAP:
            return ROLE_MAP[tag]
    return "Flex"


def _tag_key(tags: list[str]) -> str | None:
    tag_set = set(tags)
    if "Marksman" in tag_set:
        return "Marksman+Support" if len(tag_set & {"Support", "Tank", "Mage"}) == 0 else "Marksman+Tank"
    if "Tank" in tag_set:
        if tag_set & {"Mage"}:
            return "Tank+Mage"
        return "Tank+Marksman"
    if "Assassin" in tag_set:
        return "Assassin+Tank"
    if "Fighter" in tag_set:
        return "Fighter+Support"
    if "Mage" in tag_set:
        return "Mage+Tank"
    if "Support" in tag_set:
        return "Marksman+Support"
    return None


def _generic_partners(name: str, tags: list[str], all_champs: dict[str, dict]) -> list[tuple[str, str, str, int]]:
    picks: list[tuple[str, str, str, int]] = []
    tag_set = set(tags)

    if name in FOLLOWUP_CHAMPS:
        for eng in ("Malphite", "Amumu", "Leona", "Nautilus", "Alistar", "Rell", "Jarvan IV"):
            if eng != name:
                picks.append((eng, _primary_role(_champ_tags(eng, all_champs)),
                              f"{eng} engage sets up {name}'s follow-up damage in teamfights.", 78 - len(picks) * 2))

    if name in ENGAGE_CHAMPS:
        for follow in ("Yasuo", "Miss Fortune", "Orianna", "Jinx", "Samira", "Brand"):
            if follow != name:
                picks.append((follow, _primary_role(_champ_tags(follow, all_champs)),
                              f"{name} CC groups enemies for {follow} to capitalize.", 80 - len(picks) * 2))

    if name in HYPERCARRY_CHAMPS:
        for ench in ("Lulu", "Thresh", "Nautilus", "Renata Glasc", "Milio"):
            if ench != name:
                picks.append((ench, "Support",
                              f"{ench} peel and enable lets {name} scale into a late-game win condition.", 82 - len(picks) * 2))

    if name in ENCHANTER_CHAMPS:
        for carry in ("Jinx", "Kog'Maw", "Vayne", "Aphelios", "Kai'Sa"):
            if carry != name:
                picks.append((carry, "ADC",
                              f"{name} protection amplifies {carry} hypercarry potential.", 82 - len(picks) * 2))

    if "Mage" in tag_set and name not in FOLLOWUP_CHAMPS:
        for tank in ("Amumu", "Jarvan IV", "Malphite", "Nautilus"):
            if tank != name:
                picks.append((tank, _primary_role(_champ_tags(tank, all_champs)),
                              f"{tank} lockdown guarantees {name} skillshot and burst connections.", 76 - len(picks) * 2))

    if "Assassin" in tag_set:
        for setup in ("Leona", "Nautilus", "Elise", "Jarvan IV", "Thresh"):
            if setup != name:
                picks.append((setup, _primary_role(_champ_tags(setup, all_champs)),
                              f"{setup} CC creates the pick window {name} needs to assassinate.", 78 - len(picks) * 2))

    key = _tag_key(tags)
    if key and key in TAG_PARTNERS:
        for partner, role, reason, strength in TAG_PARTNERS[key]:
            if partner != name:
                picks.append((partner, role, reason.replace("ADC", name if "Marksman" in tag_set else "ADC"), strength))

    seen: set[str] = set()
    unique: list[tuple[str, str, str, int]] = []
    for p in picks:
        if p[0] not in seen and p[0] != name:
            seen.add(p[0])
            unique.append(p)
    return unique


def _pick_partners(name: str, tags: list[str], all_champs: dict[str, dict]) -> list[dict]:
    known = KNOWN_DUO_SYNERGIES.get(name, [])
    generic = _generic_partners(name, tags, all_champs)

    merged: list[tuple[str, str, str, int]] = []
    seen: set[str] = set()
    for partner, role, reason, strength in known + generic:
        if partner not in seen and partner != name:
            seen.add(partner)
            merged.append((partner, role, reason, strength))
        if len(merged) >= 5:
            break

    return [
        {"champion": p, "role": r, "reason": reason, "synergy_score": score}
        for p, r, reason, score in merged[:5]
    ]


def _ability_synergy_tips(name: str, spells: list[dict], partners: list[dict]) -> list[dict]:
    partner_names = [p["champion"] for p in partners[:3]]
    ally_str = ", ".join(partner_names) if partner_names else "allies"
    tips: list[dict] = []
    spell_map = {s["key"]: s["name"] for s in spells}

    for key in ("P", "Q", "W", "E", "R"):
        if key not in spell_map:
            continue
        spell_name = spell_map[key]
        if key == "R":
            tip = (
                f"Coordinate {spell_name} timing with {ally_str} — "
                f"layered ultimates win teamfights when fired on the same target cluster."
            )
        elif key == "E":
            tip = (
                f"Use {spell_name} to set up or follow {ally_str}'s engage — "
                f"chain CC before enemies can flash out."
            )
        elif key == "Q":
            tip = (
                f"Lead or follow with {spell_name} after {ally_str} lands CC — "
                f"guaranteed hit combos deal significantly more than solo poke."
            )
        elif key == "W":
            tip = (
                f"{spell_name} provides utility that amplifies {ally_str}'s all-in window — "
                f"sync cooldowns before committing."
            )
        else:
            tip = (
                f"{spell_name} passive synergizes with {ally_str}'s trade pattern — "
                f"proc it during ally CC for maximum value."
            )
        tips.append({"key": key, "name": spell_name, "tip": tip})

    return tips


def _combo_tips(name: str, tags: list[str], partners: list[dict]) -> list[str]:
    top = partners[0]["champion"] if partners else "your duo partner"
    tag_set = set(tags)
    tips = [
        f"Communicate cooldowns with {top} before committing to all-ins.",
        f"Ward together before objective fights so {top} can engage with vision advantage.",
    ]

    if "Marksman" in tag_set:
        tips.extend([
            f"Let {top} engage first — follow with damage only after CC lands.",
            "Match push timing so your support can roam without losing XP.",
            "In teamfights, stay behind frontline and focus whoever your duo CCs.",
        ])
    elif "Support" in tag_set:
        tips.extend([
            "Time engage when your ADC has items completed for maximum kill pressure.",
            "Control bush vision to force favorable engage angles.",
            "Peel for your carry when enemy divers commit — a saved ADC wins fights.",
        ])
    elif "Tank" in tag_set or "Fighter" in tag_set:
        tips.extend([
            f"Flank or front-to-back engage to group enemies for {top}'s AoE.",
            "Flash engage only when your follow-up partner has ult available.",
            "Build tanky enough to survive long enough for your carry to DPS.",
        ])
    elif "Mage" in tag_set:
        tips.extend([
            f"Hold key ability until {top} lands CC — guaranteed combos beat random poke.",
            "Control wave from safe range and call for ganks when enemy overextends.",
            "In teamfights, wait for engage before committing full rotation.",
        ])
    elif "Assassin" in tag_set:
        tips.extend([
            f"Roam with {top} when their CC is up for guaranteed pick kills.",
            "Don't show on map before gank — surprise plus CC chain equals kills.",
            "Target the same carry your duo CCs for focus fire.",
        ])
    else:
        tips.extend([
            f"Sync power spikes with {top} — fight together when both have item completions.",
            "Trade when your duo has cooldown advantage, not when both are on long timers.",
        ])

    return tips[:5]


def _power_spikes(name: str, tags: list[str], partners: list[dict]) -> list[str]:
    top = partners[0]["champion"] if partners else "duo partner"
    spikes = [
        f"Level 2–3: First coordinated all-in with {top} if level advantage.",
        f"Level 6: Both ultimates online — maximum kill pressure window.",
        f"First item completion: Sync fight timing when both hit power spike.",
    ]
    if "Marksman" in tags or any(p["champion"] in HYPERCARRY_CHAMPS for p in partners):
        spikes.append(f"Two-item spike: {name} plus {top} can end games if ahead.")
    if name in ENGAGE_CHAMPS or any(p["champion"] in ENGAGE_CHAMPS for p in partners):
        spikes.append(f"Teamfight item (Sunfire, Jak'Sho): Frontline plus {top} wombo potential.")
    return spikes[:4]


def _items_to_consider(name: str, tags: list[str]) -> list[str]:
    tag_set = set(tags)
    items: list[str] = []
    if "Support" in tag_set:
        items = ["Knight's Vow — link with your carry", "Redemption — teamfight sustain", "Locket of the Iron Solari — AoE shield"]
    elif "Marksman" in tag_set:
        items = ["Guardian Angel — survive focus for peel", "Mercury's Treads — reduce CC duration", "Phantom Dancer — kiting with peel"]
    elif "Tank" in tag_set:
        items = ["Knight's Vow — protect carry", "Zeke's Convergence — amplify ally damage", "Trailblazer — chase after engage"]
    elif "Mage" in tag_set:
        items = ["Horizon Focus — amplify CC'd target damage", "Shadowflame — burst on immobile targets", "Zhonya's Hourglass — survive after combo"]
    elif "Assassin" in tag_set:
        items = ["Youmuu's Ghostblade — roam with partner", "Edge of Night — spell shield during pick", "Opportunity — snowball after pick"]
    elif "Fighter" in tag_set:
        items = ["Sterak's Gage — survive focus in all-in", "Trailblazer — stick to CC'd targets", "Death's Dance — extended fight sustain"]
    else:
        items = ["Control Wards — vision for coordinated picks", "Early Boots — sync roam timing", "Component items that match your duo's spike"]
    return items[:3]


def _summary(name: str, tags: list[str], partners: list[dict]) -> str:
    top = partners[0]["champion"] if partners else "the right partner"
    tag_set = set(tags)
    if name in FOLLOWUP_CHAMPS:
        return (
            f"{name} reaches peak value when paired with hard engage like {top}. "
            f"Set up knockups and CC chains so {name} can unleash full combo damage."
        )
    if name in ENGAGE_CHAMPS:
        return (
            f"{name} creates the fight — pair with follow-up damage from {top} "
            f"to convert engages into teamfight wins."
        )
    if name in HYPERCARRY_CHAMPS:
        return (
            f"{name} scales into a late-game win condition with enabler support from {top}. "
            f"Protect the carry and win through superior teamfight DPS."
        )
    if name in ENCHANTER_CHAMPS:
        return (
            f"{name} amplifies a hypercarry partner like {top}. "
            f"Peel, shield, and speed boost your ADC through the mid game into an unkillable late game."
        )
    if "Assassin" in tag_set:
        return (
            f"{name} thrives with CC-heavy partners like {top} who guarantee pick kills. "
            f"Roam together and snowball through mid-game assassinations."
        )
    if "Mage" in tag_set:
        return (
            f"{name} deals maximum damage when {top} locks down targets. "
            f"Layer skillshots on CC'd enemies for guaranteed burst combos."
        )
    return (
        f"{name} synergizes best with {top} — coordinate engages, "
        f"trade windows, and item spikes to dominate lane and teamfights together."
    )


def _build_guide(name: str, detail: dict, all_champs: dict[str, dict]) -> dict:
    tags = detail.get("tags", [])
    partners = _pick_partners(name, tags, all_champs)
    return {
        "summary": _summary(name, tags, partners),
        "synergy_picks": partners,
        "ability_synergy_tips": _ability_synergy_tips(name, detail["spells"], partners),
        "combo_tips": _combo_tips(name, tags, partners),
        "power_spikes": _power_spikes(name, tags, partners),
        "items_to_consider": _items_to_consider(name, tags),
    }


def generate_all() -> dict[str, dict]:
    champs = list_champions()
    all_champs = {c["name"]: c for c in champs}
    existing: dict = {}
    if SYNERGY_FILE.exists():
        existing = json.loads(SYNERGY_FILE.read_text(encoding="utf-8"))

    result: dict[str, dict] = {}
    for champ in champs:
        name = champ["name"]
        if name in PREMIUM_CHAMPIONS and name in existing:
            result[name] = existing[name]
            continue
        detail = get_champion_detail(champ["id"])
        result[name] = _build_guide(name, detail, all_champs)
    return result


def main() -> None:
    data = generate_all()
    SYNERGY_FILE.parent.mkdir(parents=True, exist_ok=True)
    SYNERGY_FILE.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    premium = sum(1 for n in data if n in PREMIUM_CHAMPIONS)
    print(f"Wrote {len(data)} synergy guides to {SYNERGY_FILE}")
    print(f"  Premium champions: {premium}")
    print(f"  Total partners indexed: {sum(len(g['synergy_picks']) for g in data.values())}")


if __name__ == "__main__":
    main()
