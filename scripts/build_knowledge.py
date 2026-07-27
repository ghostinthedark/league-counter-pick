#!/usr/bin/env python3
"""Build premium matchup_knowledge.py from compact curated data."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Compact format: name -> (summary, counters, abilities dict, laning list, spikes, items)
# counters: list of (champion, role, reason)
# abilities: {P,Q,W,E,R: tip}

RAW: dict[str, tuple] = {
    "Aatrox": (
        "Aatrox wins extended fights with Q knockups and R revive. Punish when his Q is on cooldown and dodge the sweet-spot edge.",
        [("Fiora", "Top", "Riposte parries Q/W and stuns. Outduels in extended trades."), ("Irelia", "Top", "Mobile and can dodge Q sweet spots. Wins long fights with stacks."), ("Jax", "Top", "Dodges Q with E. Scales harder in side lane duels."), ("Malphite", "Top", "Armor stack reduces Q damage. R disengage stops all-ins."), ("Vayne", "Top/ADC", "Kites the immobile juggernaut. True damage ignores his healing.")],
        {"P": "Aatrox's passive procs on spell hit for bonus damage and a heal zone. Don't stand in the ground circle — it heals him significantly.", "Q": "THE KEY ABILITY. Three casts with outer-edge knockup. Sidestep the outer arc or fight inside close range to deny knockup. Each Q has a long windup.", "W": "Chains that pull after 2 hits. 16s cooldown early. Bait it, then trade while it's down. Don't get double-hit during his Q combo.", "E": "Short dash with slow on enemies hit. He uses E to adjust Q angle. Punish when E is down — he has no escape.", "R": "Revive + AD boost on takedown. If he ults, disengage and wait out the revive. Don't throw everything into his R heal."},
        ["Trade when Q1 is on cooldown — without Q he has no threat.", "Dodge outer Q edge — the knockup enables his full combo.", "Buy Grievous Wounds early to cut his passive and R healing.", "Aatrox pushes with Q — call jungler for ganks.", "Short trades beat extended fights where his passive heals him."],
        ["Level 6: R revive makes all-ins dangerous", "First item (Eclipse/Black Cleaver): Strong duelist", "Level 11: Reduced Q cooldown"],
        ["Plated Steelcaps — reduces auto and Q damage", "Oblivion Orb / Bramble Vest — anti-heal", "Phage / Stridebreaker — if bruiser matchup"]
    ),
    "Akali": (
        "Akali wins with passive ring trades and all-ins after energy dump. Force her to waste shroud and punish when energy is low.",
        [("Galio", "Mid", "W magic shield and point-and-click CC stop her all-ins."), ("Malzahar", "Mid", "Point-and-click ult. Passive blocks her first burst."), ("Diana", "Mid", "W shield and burst. Can match her all-in at 6."), ("Pantheon", "Mid/Top", "Point-and-click W stun. Strong early before she scales."), ("Lee Sin", "Jungle", "Reveal with E and burst before she can shroud.")],
        {"P": "Ring creates movement speed toward enemy. Force her to leave the ring without proccing passive — she loses trade damage.", "Q": "Throws kunai that slow on exit. Back off when she throws Q — the return slow sets up passive.", "W": "Shroud drops smoke for stealth and energy restore. Buy Control Wards. True sight or AoE reveals her. Don't waste key CC into empty shroud.", "E": "Dash to target or back to shroud. THE KEY ABILITY. Track where she E'd in — that's her escape line. CC her before second E.", "R": "Dashes around target with execute damage. Zhonya's/Stasis dodges R2. After R she has no escape if you survive."},
        ["Buy Control Wards to reveal shroud.", "Trade when her energy is below half — she can't full combo.", "Punish after shroud ends — 20s cooldown on W early.", "Don't chase into fog — she wins in shroud trades.", "All-in level 1-3 before she gets 6 kill pressure."],
        ["Level 6: R execute threat", "First back with Hexdrinker/Seeker's", "Protobelt + Shadowflame: One-shot potential"],
        ["Control Wards", "Seeker's Armguard / Hexdrinker", "Mercury's Treads"]
    ),
    "Akshan": (
        "Akshan wins by poking with Q and resetting with passive double-hit. Respect his W revive and E mobility.",
        [("Caitlyn", "ADC", "Outranges his Q. Traps zone his E path."), ("Draven", "ADC", "Bursts him before he can W shield. Wins early trades."), ("Leona", "Support", "Hard CC locks down his E escape."), ("Pantheon", "Mid/Top", "Point-and-click stun stops E dash."), ("Malzahar", "Mid", "Suppression stops E and R mobility.")],
        {"P": "Double-hit passive on every third auto or after ability use. Short trades prevent the two-hit proc.", "Q": "Boomerang through minions — stand outside minion line. Returns for extra damage if you don't move.", "W": "Passive revives allies on takedown. Focus Akshan in fights — don't let him get resets.", "E": "THE KEY ABILITY. Grapple swing for mobility and auto barrage. CC him mid-swing or stand outside the swing path.", "R": "Lock-on snipe across map. Zhonya's/Stasis dodges. Sidestep if you're low — it tracks but has travel time."},
        ["Stand outside minion wave to avoid Q poke.", "All-in when E is on cooldown — he's immobile without it.", "Leona/Naut hard CC stops his swing.", "Don't let him proc passive — short trades only.", "Group vs W revive — don't give him takedown resets."],
        ["Level 3: Q + passive trade pattern", "Level 6: R global execute", "Kraken Slayer + Wits End"],
        ["Early Boots — dodge Q return", "Randuin's Omen — if ADC", "Plated Steelcaps"]
    ),
    "Alistar": (
        "Alistar wins with W+Q engage and R tankiness. Respect his combo range and don't clump for R knockup.",
        [("Morgana", "Support", "Black Shield blocks headbutt+pulverize combo."), ("Janna", "Support", "Tornado and R disengage his engage."), ("Vayne", "ADC", "Condemn into wall stops W+Q. True damage shreds him."), ("Ezreal", "ADC", "E blink dodges combo. Poke from range."), ("Lulu", "Support", "Polymorph stops combo. R saves carry from follow-up.")],
        {"P": "Headbutt after 6 spells heals allies. Don't let him walk up for free trades near minions.", "Q": "Pulverize — ground-targeted AoE knockup. 14s cooldown. Stay spread in teamfights. If Q misses, punish hard.", "W": "Headbutt to target. THE KEY COMBO: W→Q. Stand behind minions or stay out of W range (~650). Flash+Q+W is possible.", "E": "Trample for damage over time. Used after combo for extra damage. Not the main threat.", "R": "Damage reduction + bonus damage. Don't focus him during R — 7s of 55-70% damage reduction. Kite and wait it out."},
        ["Stay behind minions — blocks W target.", "Punish every missed Q — 14s window.", "Morgana E hard counters his engage.", "Don't clump for teamfight R knockup.", "Poke before fights — Alistar has no sustain in lane."],
        ["Level 2: W+Q combo online", "Level 6: R tower dives", "Mobility Boots: Roam threat"],
        ["Mobility Boots", "Mikael's Blessing", "Control Wards"]
    ),
    "Ambessa": (
        "Ambessa wins with aggressive dashes and execute windows. Respect her all-in burst and disengage when she commits.",
        [("Malphite", "Top", "Tank and CC stops her dive. R disengage."), ("Quinn", "Top", "Kites and blinds. Never lets Ambessa commit."), ("Poppy", "Top/Jungle", "W blocks dashes. R knocks her away."), ("Vayne", "Top/ADC", "Condemn and kiting punish melee all-ins."), ("Karma", "Top/Support", "Shield and speed kite her engage.")],
        {"P": "Passive grants bonus effects on ability use. Watch for empowered follow-up autos after each spell.", "Q": "Primary damage ability. THE KEY ABILITY. Trade when Q is on cooldown.", "W": "Defensive or engage tool depending on build. Bait W then re-engage.", "E": "Mobility/damage spell. Track cooldown — after E she's less mobile.", "R": "Execute or teamfight ability. Don't stay low HP. Disengage when she ults."},
        ["Trade on Q cooldown.", "Kite with range — she wants extended all-ins.", "Poppy W stops her dash engage.", "Buy early armor.", "Call jungler — overextends on Q dash."],
        ["Level 6: R kill pressure", "First item spike", "Level 11: Ability maxed"],
        ["Plated Steelcaps", "Bramble Vest", "Phage"]
    ),
    "Amumu": (
        "Amumu wins with R teamfight lockdown and Q gap close. Spread in fights and punish early weak laning.",
        [("Morgana", "Support", "Black Shield blocks Q and R on carry."), ("Mikael's", "Support", "Cleanse R CC off carry."), ("Janna", "Support", "Disengage R with tornado and ult."), ("Olaf", "Top/Jungle", "R ignores Amumu ult CC."), ("Ezreal", "ADC", "E dodges Q. Safe poke from range.")],
        {"P": "Cursed Touch — auto and abilities apply bonus true damage over time. Extended fights stack damage.", "Q": "Bandage Toss — skillshot stun. 10s cooldown. Hide behind minions. If Q misses, Amumu is nearly useless.", "W": "Despair — AoE % HP damage aura. Don't stand near him during extended fights.", "E": "Tantrum — passive damage reduction + AoE burst. Don't auto-trade into E spam.", "R": "THE KEY ABILITY. AoE root around him. Spread out. QSS/Mikael's cleanses root. 140s cooldown — punish after R used."},
        ["Dodge Q — Amumu is harmless without it.", "Spread in teamfights to minimize R value.", "Invade early — Amumu is weak before 6.", "Buy Merc Treads to reduce R duration.", "Morgana E completely shuts down his engage."],
        ["Level 6: R changes teamfights", "Sunfire Aegis completion", "Teamfight with R up"],
        ["Mercury's Treads", "Mikael's Blessing", "Control Wards"]
    ),
    "Anivia": (
        "Anivia wins by walling and bursting with R+E after stun. Respect her passive egg and zone control.",
        [("Kassadin", "Mid", "R dodges Q and scales past her."), ("Fizz", "Mid", "E dodges all skillshots. All-in after egg down."), ("Zed", "Mid", "R dodges burst. All-in when egg is down."), ("Katarina", "Mid", "Shunpo dodges Q. Resets beat her in skirmishes."), ("Sylas", "Mid", "Steals R. Gap close after wall.")],
        {"P": "Rebirth Egg — upon death she becomes an egg that revives. Focus the egg immediately or she respawns at full HP.", "Q": "Flash Frost — stun if hit twice. 10s cooldown. Sidestep or hide behind minions. Stun enables full combo.", "W": "Crystallize — wall blocks paths. THE KEY ABILITY. Don't walk into chokepoints. Walk around walls.", "E": "Frostbite — double damage on chilled targets. Don't get Q'd into E.", "R": "Glacial Storm — channeled AoE. CC interrupts it. Move out of the zone — damage ramps over time."},
        ["Break the egg immediately when she dies.", "Sidestep Q — without stun her damage drops.", "All-in when egg passive is down.", "CC interrupts her R channel.", "Buy Merc Treads for shorter stun."],
        ["Level 6: R zone control", "Rod of Ages / Stormsurge", "Level 11: R rank 2"],
        ["Mercury's Treads", "Verdant Barrier", "Hexdrinker if AD"]
    ),
    "Annie": (
        "Annie wins with flash-Tibbers burst. Track her stun stacks and respect level 6 all-in.",
        [("Yasuo", "Mid", "Wind wall blocks Tibbers and Q."), ("Zed", "Mid", "All-in before she can stun. R dodges burst."), ("Fizz", "Mid", "E dodges Tibbers drop. All-in early."), ("Kassadin", "Mid", "R dodges stun combo. Scales past her."), ("Sylas", "Mid", "Steals Tibbers. W shield survives burst.")],
        {"P": "Pyromania — every 4 spells stuns. COUNT HER SPELLS. At 4 stacks, play safe. She will flash-R.", "Q": "Targeted damage + refunds mana on kill. Farm denial tool. Don't trade when she has stun up.", "W": "Cone fire — stun if passive is ready. Stay out of cone range when she has 3-4 stacks.", "E": "Shield + move speed. Used for stun stack and engage speed.", "R": "THE KEY ABILITY. Tibbers drop with AoE stun. At level 6 with flash, she one-shots. Respect 4-stack + flash range."},
        ["Count stun stacks — at 4, back off.", "Buy Merc Treads to reduce stun.", "All-in when stun is on cooldown.", "She has no escape — gank when pushed.", "Zhonya's if AP to survive Tibbers."],
        ["Level 6 + Flash: One-shot threat", "Lost Chapter / Malignance", "Stun up in teamfights"],
        ["Mercury's Treads", "Hexdrinker / Verdant Barrier", "Zhonya's Hourglass"]
    ),
    "Aphelios": (
        "Apheios wins with weapon rotations and teamfight AOE. Identify his current gun and punish weak windows.",
        [("Draven", "ADC", "Dominates early lane before Aphelios scales."), ("Lucian", "ADC", "Burst and mobility. Strong early all-in."), ("Leona", "Support", "Hard CC stops his immobile self."), ("Nautilus", "Support", "Hook catches him with no escape."), ("Zed", "Mid", "Assassinates the immobile ADC.")],
        {"P": "The Hitman and Hitwoman — weapon cycle. Red= sustain, Green= range, Purple= slow, Blue= AOE, White= DPS. Identify gun color.", "Q": "Changes per weapon. Green Q (Calibrum) is long-range mark. Purple Q (Gravitum) roots. Know which Q is active.", "W": "Weapon switch — no cooldown but limited ammo. Punish when on weak gun (no ammo left).", "E": "Weapon-specific utility. Flash + root gun (Purple) is the main threat.", "R": "THE KEY ABILITY. Moonlight Vigil — hits all enemies hit by Calibrum marks. Don't stand in marked groups."},
        ["All-in early — Aphelios is weak levels 1-3.", "Identify current gun — punish Green/Red transitions.", "Naut/Leona hard engage before he scales.", "Stand spread for R — don't get multi-hit.", "Buy early Boots — dodge skillshots."],
        ["Level 6: R teamfight threat", "Infinity Edge + weapon mastery", "3 items: Teamfight carry"],
        ["Plated Steelcaps", "Early Boots", "Randuin's Omen"]
    ),
    "Ashe": (
        "Ashe wins with poke, global R initiation, and permaslow. Respect her level 1 strength and vision E.",
        [("Yasuo", "ADC/Mid", "Wind wall blocks R and W."), ("Draven", "ADC", "All-in early before she kites."), ("Blitzcrank", "Support", "Hook catches immobile Ashe."), ("Zed", "Mid", "R dodges her burst. Assassinates post-6."), ("Kha'Zix", "Jungle", "Stealth burst on immobile ADC.")],
        {"P": "Frost Shot — every auto slows. Extended fights favor her kiting. Burst before she can kite.", "Q": "Ranger's Focus — attack speed steroid. All-in when Q is not active.", "W": "Volley — cone slow. 15s cooldown. Hide behind minions or sidestep.", "E": "Hawkshot — global vision. Denies bush plays. Track her E cooldown for gank timing.", "R": "THE KEY ABILITY. Global stun arrow. Track cooldown (80s). Don't facecheck. Zhonya's dodges it."},
        ["All-in early — Ashe has no escape.", "Blitz hook is a free kill.", "Hide behind minions for W.", "Track R cooldown — engage when it's down.", "Buy Boots early — reduce slow effectiveness."],
        ["Level 1: W + Frost Shot trade", "Kraken Slayer / Trinity", "Level 6: Global R initiation"],
        ["Plated Steelcaps", "Early Boots", "Hexdrinker if assassin"]
    ),
    "Aurelion Sol": (
        "Aurelion Sol wins with passive star orbit and R stun knockback. Close gap and burst before he scales to orbit monster.",
        [("Fizz", "Mid", "E dodges his abilities. All-in early."), ("Kassadin", "Mid", "R gap close. Scales past him."), ("Yasuo", "Mid", "Wind wall blocks Q and R."), ("Talon", "Mid", "Roams and burst before Sol scales."), ("Katarina", "Mid", "Shunpo dodges Q. Resets in teamfights.")],
        {"P": "Cosmic Creator — stars orbit and grow with level. Extended fights make him stronger. Burst early.", "Q": "Breath of Light — cone damage. THE KEY ABILITY. Sidestep or fight inside close range.", "W": "Astral Flight — flight + speed. He uses W to reposition stars. CC during W channel.", "E": "Comet of Legend — long-range dash. Can cross map. Ward his roam paths.", "R": "The Skies Descend — stun + knockback at edge. Don't get hit by outer ring — inner is safe."},
        ["All-in early before stars scale.", "Close gap — he wants long fights.", "CC during W flight.", "Ward for E roams.", "Buy Merc Treads for R stun."],
        ["Level 6: R disengage", "Rylai's / Liandry's", "Level 11: Orbit damage spikes"],
        ["Mercury's Treads", "Verdant Barrier", "Hexdrinker if AD"]
    ),
    "Aurora": (
        "Aurora wins with spectral mobility and burst combos. CC her during ability windows and punish cooldowns.",
        [("Malzahar", "Mid", "Point-and-click ult stops her dashes."), ("Annie", "Mid", "Point-and-click stun. Burst before she escapes."), ("Galio", "Mid", "W CC and magic shield."), ("Diana", "Mid", "Shield and all-in at 6."), ("Pantheon", "Mid", "Point-and-click W stun.")],
        {"P": "Passive enhances her spectral movement. Watch for empowered follow-up after ability casts.", "Q": "Primary poke/burst. Sidestep and trade when on cooldown.", "W": "Spectral mobility — her escape tool. Save CC for after W use.", "E": "Setup or damage spell. THE KEY ABILITY. Punish when E misses.", "R": "Burst or mobility ult. Zhonya's/Stasis dodges. Disengage when she commits R."},
        ["Point-and-click CC hard counters.", "Trade on Q/E cooldown.", "Buy early MR.", "Gank when she pushes.", "Group before she can pick off carries."],
        ["Level 6: R kill pressure", "First item completion", "Level 11: Full combo online"],
        ["Mercury's Treads", "Verdant Barrier", "Seeker's Armguard"]
    ),
    "Azir": (
        "Azir wins with soldier control and shuffle R. Dive him — he's immobile and weak to all-ins.",
        [("Zed", "Mid", "All-in before soldiers setup. R dodges burst."), ("Fizz", "Mid", "E dodges soldiers. Gap close at 6."), ("Katarina", "Mid", "Shunpo dodges. Resets beat him."), ("Talon", "Mid", "Roams and burst. Outplays pre-6."), ("Syndra", "Mid", "Long range poke. Stun before shuffle.")],
        {"P": "Shurima's Legacy — turret damage and gold. Don't let him scale for free.", "Q": "Conquering Sands — moves soldiers. THE KEY ABILITY. Dodge soldier line. 7s cooldown — punish when Q is down.", "W": "Arise! — places soldiers. Max 3 soldiers. Destroy soldiers by forcing bad positions.", "E": "Shifting Sands — dash to soldier. His escape. CC him before E or catch after E ends.", "R": "Emperor's Divide — wall pushes enemies. Don't get shuffled into team. Flash out of shuffle line."},
        ["All-in early — Azir is weak pre-6.", "Dodge Q soldier line.", "Dive after he uses E — no escape.", "Don't stand between Azir and wall for shuffle.", "Buy early magic resist."],
        ["Level 6: Shuffle threat", "Nashor's Tooth / Luden's", "3 items: Teamfight DPS"],
        ["Mercury's Treads", "Verdant Barrier", "Hexdrinker if AD"]
    ),
    "Bard": (
        "Bard wins with Q stun setup, Meeps damage, and R zone control. Punish when key abilities are down.",
        [("Leona", "Support", "Hard engage before Bard can peel."), ("Nautilus", "Support", "Hook outranges Bard Q."), ("Blitzcrank", "Support", "Hook beats Bard in lane."), ("Draven", "ADC", "Burst before Bard scales Meeps."), ("Lucian", "ADC", "All-in early. Bard has low HP.")],
        {"P": "Traveler's Call — Meeps add damage. Extended trades stack Meeps. Short trades.", "Q": "Cosmic Binding — stun through 2 targets. 11s cooldown. Don't stand in minion line. If Q misses, punish.", "W": "Caretaker's Shrine — health/mana packs. Collect or deny packs. He roams for W.", "E": "Magical Journey — portal through terrain. Wards block surprise portals.", "R": "Tempered Fate — stasis zone. THE KEY ABILITY. Walk out of R zone. Don't clump for teamfight R."},
        ["Punish missed Q — 11s window.", "Blitz/Naut hook beats Bard.", "All-in early — low base HP.", "Walk out of R zone.", "Track Bard roams — ping missing."],
        ["Level 6: R pick potential", "Meeps damage scaling", "Shurelya's / Redemption"],
        ["Mobility Boots", "Control Wards", "Mikael's Blessing"]
    ),
    "Bel'Veth": (
        "Bel'Veth wins with stack scaling and true damage on E. CC her during E and kite before she stacks.",
        [("Vayne", "Top/Jungle", "True damage and kiting. Condemn stops E."), ("Poppy", "Jungle/Top", "W blocks her dash. R disengage."), ("Jax", "Top/Jungle", "Counter-strike blocks autos during E."), ("Kindred", "Jungle", "R saves from execute. Kites her."), ("Malphite", "Top", "R disengage. Armor reduces damage.")],
        {"P": "Death in Lavender — stacks attack speed per kill. Don't let her farm stacks for free.", "Q": "Void Surge — dash + damage. THE KEY ABILITY. Poppy W blocks dash. CC during Q.", "W": "Above and Below — slam + slow. Don't stand in center.", "E": "Royal Maelstrom — channels for true damage + lifesteal. CC IMMEDIATELY. Jax E blocks.", "R": "Endless Banquet — gains stacks and true damage. Disengage when she ults."},
        ["CC during E channel — true damage stops.", "Don't let her stack passive.", "Poppy W blocks Q dash.", "Kite with range early.", "Group vs her — she splits well."],
        ["First back: Blade of the Ruined King", "Level 6: R stacking", "2 items: Attack speed monster"],
        ["Plated Steelcaps", "Randuin's Omen", "Thornmail"]
    ),
    "Blitzcrank": (
        "Blitzcrank wins with hook (Q) picks. Stand behind minions and punish every missed hook.",
        [("Morgana", "Support", "Black Shield blocks hook entirely."), ("Sivir", "ADC", "Spell shield blocks hook."), ("Ezreal", "ADC", "E dodges hook. Safe poke."), ("Alistar", "Support", "Can headbutt hooked ally away or engage first."), ("Milio", "Support", "Shield and disengage.")],
        {"P": "Mana Barrier — shield when low HP. Don't assume he's dead — barrier saves him.", "Q": "THE KEY ABILITY. Rocket Grab — 20s cooldown. ALWAYS stand behind minions. If hook misses, all-in for 20 seconds.", "W": "Overdrive — speed boost. Uses to walk up for hook. Kite when W is active.", "E": "Power Fist — knockup auto. Don't get hooked into E+ R combo.", "R": "Static Field — AoE silence + damage. Don't stand near after hook."},
        ["Always stand behind minions.", "Punish EVERY missed hook — 20s window.", "Morgana/Sivir hard counter.", "Ward bushes — hook from fog.", "Focus Blitz after hook misses in fights."],
        ["Level 2: Hook + E combo", "Level 6: R silence chain", "Mobility Boots roams"],
        ["Mobility Boots", "Control Wards", "Mikael's Blessing"]
    ),
    "Brand": (
        "Brand wins with passive stack explosions and R bounces. Spread in fights and all-in when immobile.",
        [("Yasuo", "Mid", "Wind wall blocks Q and R."), ("Fizz", "Mid", "E dodges all skillshots. All-in at 6."), ("Zed", "Mid", "R dodges burst. All-in after passive proc."), ("Katarina", "Mid", "Shunpo dodges. Resets beat immobile Brand."), ("Sylas", "Mid", "Steals R. Gap close with E.")],
        {"P": "Blaze — abilities apply stacks. At 3 stacks, Ablaze detonates. Don't get 3 stacks — disengage.", "Q": "Sear — stun if target is ablaze. THE KEY ABILITY. Don't get caught with 2 stacks. 8s cooldown.", "W": "Pillar of Flame — AoE. Predictable placement. Move out of W zone.", "E": "Conflagration — spreads blaze to nearby. Spread out in teamfights.", "R": "Pyroclasm — bounces between nearby enemies. SPREAD OUT. Don't clump or R melts team."},
        ["Don't get 3 passive stacks.", "All-in — Brand has no escape.", "Spread for R bounces.", "Yasuo wall blocks Q stun.", "Buy Merc Treads for Q stun."],
        ["Level 6: R teamfight", "Liandry's / Stormsurge", "Level 11: Q rank 3"],
        ["Mercury's Treads", "Verdant Barrier", "Hexdrinker if AD"]
    ),
    "Braum": (
        "Braum wins with passive stacks and unbreakable shield. Don't auto him with passive up and respect Q stun.",
        [("Brand", "Support/ADC", "AoE bypasses shield. Spread damage."), ("Caitlyn", "ADC", "Outranges and traps zone. Headshot procs."), ("Morgana", "Support", "Binding outranges Q. Shield blocks engage."), ("Vel'Koz", "Support", "True damage and long range poke."), ("Lux", "Support", "Long range poke outranges Braum.")],
        {"P": "Concussive Blows — 4 stacks stun. DON'T auto Braum or his marked ally 4 times.", "Q": "Winter's Bite — slow skillshot. 10s cooldown. Sidestep. If Q misses, punish.", "W": "Stand Behind Me — dashes to ally with shield. Can't stop W but focus the carry.", "E": "THE KEY ABILITY. Unbreakable — shield blocks ALL projectiles from direction. Walk around shield or wait it out.", "R": "Glacial Fissure — AoE knockup line. Flash sideways or stay out of line."},
        ["Don't proc 4-stack passive.", "Walk around E shield — don't waste abilities.", "Poke from range — Braum is melee.", "Punish missed Q.", "True damage bypasses shield."],
        ["Level 6: R engage", "Knight's Vow / Locket", "Mid game peel monster"],
        ["Mobility Boots", "Control Wards", "Mikael's Blessing"]
    ),
    "Briar": (
        "Briar wins with W berserk all-ins and E damage reduction. CC her during berserk and kite before 6.",
        [("Vayne", "Top/Jungle", "Condemn stops W leap. True damage."), ("Poppy", "Jungle", "W blocks E dash. R disengage."), ("Morgana", "Support", "Binding stops berserk. Black Shield blocks CC."), ("Janna", "Support", "Disengage and peel from W all-in."), ("Kindred", "Jungle", "R saves allies from berserk execute.")],
        {"P": "Blood Frenzy — heals on attack and ability hit. Buy anti-heal early.", "Q": "Head Rush — dash + Q hold. THE KEY ABILITY. CC during dash. Poppy W blocks.", "W": "Snax/Snack Attack — berserk leap. CC during berserk or disengage. She can't cancel W.", "E": "Chilling Scream — damage reduction + fear if center hit. Don't stand in center cone.", "R": "Certain Death — global leap to furthest enemy. Spread. Zhonya's/Stasis dodges."},
        ["CC during W berserk.", "Buy Grievous Wounds early.", "Kite before level 6.", "Poppy W blocks Q/E.", "Group vs R global engage."],
        ["Level 6: R global threat", "Stridebreaker / BotRK", "Level 11: W damage spikes"],
        ["Plated Steelcaps", "Bramble Vest", "Randuin's Omen"]
    ),
    "Caitlyn": (
        "Caitlyn wins with range, traps, and headshot poke. All-in early and respect trap zone in sieges.",
        [("Draven", "ADC", "All-in early. Outdamages before range advantage."), ("Lucian", "ADC", "Burst combo. Strong early all-in."), ("Blitzcrank", "Support", "Hook beats long range."), ("Leona", "Support", "Hard CC on immobile Cait."), ("Zed", "Mid", "Assassinates in teamfights.")],
        {"P": "Headshot — bonus damage every few autos or on trapped targets. Don't get CC'd into trap headshot.", "Q": "Piltover Peacemaker — line shot. 10s cooldown. Sidestep or hide behind minions.", "W": "THE KEY ABILITY. Yordle Snap Trap — CC on step. Don't walk in straight lines. Clear traps with sweeper.", "E": "90 Caliber Net — slow + Caitlyn knockback. Her escape. All-in when E is down.", "R": "Ace in the Hole — targeted execute. Zhonya's/Stasis dodges. Peel for low HP allies."},
        ["All-in early — weak levels 1-3.", "Sweeper clears traps.", "Blitz hook is free kill.", "All-in when E is down.", "Stand behind minions for Q."],
        ["First back: Headshot damage", "Rapid Firecannon", "2 items: Siege monster"],
        ["Plated Steelcaps", "Early Boots", "Hexdrinker if assassin"]
    ),
    "Camille": (
        "Camille wins with hookshot dives and true damage R isolation. Peel for carry and CC during hookshot.",
        [("Jax", "Top", "E dodges her Q and R. Outscales."), ("Poppy", "Top", "W blocks hookshot. R knocks her off walls."), ("Quinn", "Top", "Kites and blinds. Never lets her engage."), ("Malphite", "Top", "R disengage from R isolation."), ("Darius", "Top", "Extended trades favor Darius.")],
        {"P": "Adaptive Defenses — shield on auto to champions. Short trades prevent shield.", "Q": "Precision Protocol — true damage when fully charged. THE KEY ABILITY. CC before Q2 or fight during windup.", "W": "Tactical Sweep — outer cone damage + heal. Stay inside close range.", "E": "Hookshot — stun on second target. Poppy W blocks. CC if she misses hookshot.", "R": "Hextech Ultimatum — isolates target. Peel carry. QSS/Mikael's if you're the target."},
        ["Poppy W blocks E hookshot.", "CC during Q2 charge.", "Short trades — deny passive shield.", "Peel carry from R isolation.", "Buy early armor."],
        ["Trinity Force", "Level 6: R pick", "Level 11: Q true damage"],
        ["Plated Steelcaps", "Bramble Vest", "Phage"]
    ),
    "Cassiopeia": (
        "Cassiopeia wins with sustained DPS and R face-stun. Turn away from R and all-in when boots aren't online.",
        [("Yasuo", "Mid", "Wind wall blocks R and Q."), ("Fizz", "Mid", "E dodges Twin Fang. All-in at 6."), ("Kassadin", "Mid", "R dodges. Scales past her."), ("Talon", "Mid", "Burst before she scales."), ("Lux", "Mid", "Outranges and pokes.")],
        {"P": "Serpent's Grace — immune to boots MS. She kites well. Gap close is essential.", "Q": "Noxious Blast — poison zone. Don't stand in Q. Poison enables E spam.", "W": "Miasma — ground slow zone. Walk around W. Don't get trapped in miasma.", "E": "THE KEY ABILITY. Twin Fang — spammable on poisoned targets. All-in before poison stacks.", "R": "Petrifying Gaze — stun if facing her. TURN AWAY from R. Flash behind her to dodge."},
        ["Turn away from R — stun if facing.", "All-in early before she scales.", "Don't stand in Q/W poison zones.", "Yasuo wall blocks R.", "Buy Merc Treads anyway for other CC."],
        ["Level 6: R stun threat", "Rod of Ages / Archangel's", "Level 11: E spam DPS"],
        ["Mercury's Treads", "Verdant Barrier", "Hexdrinker if AD"]
    ),
    "Cho'Gath": (
        "Cho'Gath wins with R stack scaling and Q knockup into W silence. Kite and don't feed stacks.",
        [("Vayne", "Top/ADC", "True damage % HP. Kites the tank."), ("Gnar", "Top", "Kite in mini, CC in mega."), ("Kayle", "Top", "Range and scaling. Slow prevents stacks."), ("Darius", "Top", "Extended trades. Cho can't disengage."), ("Gangplank", "Top", "Poke and kites. Orange cleanses silence.")],
        {"P": "Carnivore — HP/mana on kill. Last hits make him tankier. Deny cannon minions.", "Q": "Rupture — delayed knockup. THE KEY ABILITY. Watch ground indicator. 7s cooldown — punish when Q misses.", "W": "Feral Scream — cone silence. Stay out of cone range.", "E": "Vorpal Spikes — auto cleave. Don't auto-trade into stacked E.", "R": "Feast — true damage execute + stack. Don't stay low HP. Each stack makes him bigger."},
        ["Dodge Q knockup — delay telegraph.", "Don't feed R stacks on minions/champions.", "Kite with range — immobile.", "Buy % HP damage (BotRK, Liandry's).", "Punish when Q is on cooldown."],
        ["Level 6: R stack scaling", "Heartsteel / Jak'Sho", "6 stacks: Huge HP pool"],
        ["Mercury's Treads", "Blade of the Ruined King", "Liandry's Anguish"]
    ),
    "Corki": (
        "Corki wins with package burst and mixed damage. Respect package delivery and poke before all-in.",
        [("Yasuo", "Mid", "Wind wall blocks R and skillshots."), ("Zed", "Mid", "All-in before package. R dodges burst."), ("Talon", "Mid", "Burst and roam before Corki scales."), ("Katarina", "Mid", "Shunpo dodges. All-in early."), ("Sylas", "Mid", "Steals R. Gap close.")],
        {"P": "Hextech Munitions — package delivery. THE KEY ABILITY. Package zone = burst. Don't stand in package blast.", "Q": "Phosphorus Bomb — AoE blind. 9s cooldown. Move out of Q zone.", "W": "Valkyrie — dash + fire trail. All-in when W is down.", "E": "Gatling Gun — armor shred channel. Don't stand in front during E.", "R": "Missile Barrage — long range poke. Big missiles at 1/3 ammo. Track ammo count."},
        ["Respect package zone — massive burst.", "All-in when W is down.", "Don't stand in E armor shred.", "Yasuo wall blocks R.", "Buy early MR — mixed damage."],
        ["First package delivery", "Trinity Force / Manamune", "Level 11: R rank 2"],
        ["Mercury's Treads", "Hexdrinker", "Maw of Malmortius"]
    ),
}
