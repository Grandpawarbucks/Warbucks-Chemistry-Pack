"""Quest chapter: pylons (side page). See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

Mirror of ATM10's "Pylons" chapter (user decision 2026-10-20: quest for quest where we have the mod; same items,
order, clusters and sizes; the text is ours). All 12 of its item quests are here; ATM10's credits checkmark is
skipped. The main path's Infusion Pylon (t2_pylon, flight) and the QoL page's pylon quests stay where they are; this
page is the full set, one pylon and one filter per quest. Pack gate: the Infusion Pylon needs chemlib:hydrogen
(phase4_flight.js). LAYOUT group: logistics (ATM10 files Pylons there).
"""
from questlib import Q, Chapter, item, anytag, MAIN, SIDE  # noqa: F401

P = "pylons:"
S_CORE, S_FILTERS = "The Pylons", "Filters"
FRAME = "the pylon frame (quartz slabs, iron bars and polished blackstone)"

CHAPTER = Chapter("pylons", "Pylons", P + "infusion_pylon",
        ["Standing stones that bend the rules of a chunk."], SIDE, mirror="pylons", quests=[
    Q("py_start", 0, 0, [item("minecraft:polished_blackstone")], "Pylons", section=S_CORE, deps=["t2_polished"], xp=50,
      size=2.0, shape="gear", mirror="30B0240543253EFB", subtitle="Polished blackstone is where every pylon starts", desc=[
        "&6You remember marking ground as yours with a single stone. These are close enough.&r",
        "&eWhat:&r Pylons are blocks that change the rules in an area: give you an effect, farm for you, keep mobs out, keep players out, or protect what you've built.",
        "&eHow:&r every pylon is " + FRAME + " around a core block. Most take a filter to tell them what to act on.",
        "&eTip:&r polished blackstone comes from the Nether: smelt or stonecut blackstone, then polish it."]),
    # The four corner pylons and the centre one
    Q("py_expulsion", 0, 0, [item(P + "expulsion_pylon")], "Expulsion Pylon", section=S_CORE, deps=["py_start", "py_player_filter"], xp=60,
      size=1.5, mirror="32E52AD6EF194A60", subtitle="Uninvited guests leave", desc=[
        "&eWhat:&r the Expulsion Pylon sends other players out of the chunks around it. Whitelist friends with a Player Filter.",
        "&eHow:&r " + FRAME + " around a diamond block (check JEI).",
        "&eTip:&r with FTB Teams, your team is whitelisted automatically."]),
    Q("py_interdiction", 0, 0, [item(P + "interdiction_pylon")], "Interdiction Pylon", section=S_CORE,
      deps=["py_start", "py_mob_filter", "py_lifeless_filter"], xp=80, size=1.5, mirror="5B5FC539BD1F4A73",
      subtitle="Not that mob, not here", desc=[
        "&eWhat:&r stops chosen mobs spawning around it. A Mob Filter names the mob; a Lifeless Filter blocks all natural spawns.",
        "&eHow:&r " + FRAME + " around a netherite block (check JEI). Put the filter inside.",
        "&eTip:&r a phantom filter over your base means sleepless nights are only a figure of speech."]),
    Q("py_harvester", 0, 0, [item(P + "harvester_pylon")], "Harvester Pylon", section=S_CORE, deps=["py_start", "py_hoe"], xp=50,
      size=1.5, mirror="12ED1EE85E146A4B", subtitle="A pylon that farms for you", desc=[
        "&eWhat:&r harvests ripe crops in a square around it and puts them in a chest above it, wearing down a hoe as it goes.",
        "&eChemistry:&r every harvest carries nitrogen, phosphorus and potassium out of the soil. Real farms put it back with fertiliser; this one forgives you.",
        "&eHow:&r " + FRAME + " around a hay bale. Put it level with the crops, a hoe inside and a chest on top.",
        "&eTip:&r an Unbreaking hoe lasts far longer; a Mending one never runs out."]),
    Q("py_infusion", 0, 0, [item(P + "infusion_pylon")], "Infusion Pylon", section=S_CORE, deps=["py_start", "py_potion_filter", "t2_hydrogen"],
      xp=80, size=1.5, mirror="18246A48C20B29D8", subtitle="An effect that follows you everywhere", desc=[
        "&eWhat:&r the Infusion Pylon applies a potion filter's effect to its owner, anywhere. With a Flying filter, that's flight.",
        "&eChemistry:&r its core needs hydrogen, the lightest element: the gas that lifted the first balloons.",
        "&eHow:&r in this pack: 2 quartz slabs, 2 iron bars, a block of emerald, 3 polished blackstone and 1 &ehydrogen&r from your Dissolver (check JEI).",
        "&eTip:&r the main path's Wings of a God quest walks through the flight filter step by step."]),
    Q("py_protection", 0, 0, [item(P + "protection_pylon")], "Protection Pylon", section=S_CORE,
      deps=["py_start", "py_mob_filter", "py_block_filter"], xp=60, size=1.5, mirror="2F5263A4166BFCD6",
      subtitle="Keep your own hands off your best work", desc=[
        "&eWhat:&r stops chosen blocks being broken, or chosen mobs being hurt, in its range. A pet or a showpiece is safe even from your own sword.",
        "&eHow:&r " + FRAME + " around a honeycomb block (check JEI). Add a Block Filter or a Mob Filter.",
        "&eTip:&r protect the glass of your evaporation tower before the first creeper finds it."]),
    # Filters
    Q("py_player_filter", 0, 0, [item(P + "player_filter")], "Player Filter", section=S_FILTERS, deps=["py_start"], xp=30,
      mirror="403F76908A8A5661", subtitle="Names the friends who may stay", desc=[
        "&eWhat:&r a Player Filter lists players for the Expulsion Pylon to let through.",
        "&eHow:&r cyan terracotta, green dye and glass around a diamond (check JEI). Right-click a player with it to add them.",
        "&eTip:&r one filter holds several names."]),
    Q("py_mob_filter", 0, 0, [item(P + "mob_filter")], "Mob Filter", section=S_FILTERS, deps=["py_start"], xp=30,
      mirror="011F787E620DE9E8", subtitle="Names one kind of mob", desc=[
        "&eWhat:&r a Mob Filter names a mob type for the Interdiction or Protection Pylon.",
        "&eHow:&r cyan terracotta, green dye and glass around netherite (check JEI). Use it on the mob to set it.",
        "&eTip:&r one filter per mob type; a pylon takes several."]),
    Q("py_potion_filter", 0, 0, [item(P + "potion_filter")], "Potion Filter", section=S_FILTERS, deps=["py_start"], xp=30,
      mirror="09D18512037386C1", subtitle="Store an effect in glass", desc=[
        "&eWhat:&r a Potion Filter stores a potion effect for the Infusion Pylon.",
        "&eHow:&r 2 cyan terracotta, green dye, an emerald and 5 glass. Drink a potion, then right-click the filter to store the effect.",
        "&eTip:&r it only works once it holds an hour of the effect, so brew Long or Extra Long potions."]),
    Q("py_hoe", 0, 0, [anytag("minecraft:hoes")], "A Spare Hoe", section=S_FILTERS, deps=["py_start"], xp=20,
      mirror="034A9FBCA6D79BB6", icon="minecraft:iron_hoe", subtitle="Any hoe, for the Harvester", desc=[
        "&eWhat:&r the Harvester Pylon needs a hoe to work, and wears it down by one point per harvest.",
        "&eHow:&r any hoe counts: wood, iron, diamond or a modded one.",
        "&eTip:&r the better the hoe, the longer between refills."]),
    Q("py_lifeless_filter", 0, 0, [item(P + "lifeless_filter")], "Lifeless Filter", section=S_FILTERS, deps=["py_start"], xp=60,
      mirror="5C2C29ECA67F9B49", subtitle="No natural spawns at all", desc=[
        "&eWhat:&r the Lifeless Filter makes an Interdiction Pylon block every natural spawn over a much larger area.",
        "&eHow:&r cyan terracotta, green dye and glass around a Nether Star (check JEI).",
        "&eTip:&r spawners and breeding still work, so farms inside the area keep running."]),
    Q("py_block_filter", 0, 0, [item(P + "block_filter")], "Block Filter", section=S_FILTERS, deps=["py_start"], xp=30,
      mirror="77B185799366ACD2", subtitle="Names the blocks to protect", desc=[
        "&eWhat:&r a Block Filter lists blocks the Protection Pylon keeps from being broken.",
        "&eHow:&r cyan terracotta, green dye and glass around a honeycomb (check JEI). Use it on a block to add it.",
        "&eTip:&r list the glass and casings of a multiblock so a slip of the pickaxe can't break it."]),
], links=[("t2_polished", 0, 0), ("t2_pylon", 0, 0)])
