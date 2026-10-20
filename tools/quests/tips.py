"""Quest chapter: tips (Tips and Tricks). See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

New 2026-10-19, prefix tp_. Short, standalone tips for this pack: every quest is optional, a checkmark (tokens=0)
or a small "obtain" task (tokens=1). Shape: one hub at the top and a honeycomb of tips below it, four themed rows
(finding things, comfort and travel, this pack's own rules, chemistry and mining). The tips have no dependencies,
so the page reads as a board of cards, not a line. Manual layout: the x/y below are used as written.
Facts checked against CLAUDE.md, docs/CHANGELOG.md and pack/kubejs (qol_world.js, qol_furnace_speed.js,
phase4_chemistry.js) and the Warbucks Core source (ElementPerks.java).
"""
from questlib import Q, Chapter, item, tick, anyof, IDS, MAIN, SIDE  # noqa: F401

COLOURS = ["white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray", "light_gray", "cyan",
           "purple", "blue", "brown", "green", "red", "black"]
SLEEPING_BAGS = [f"comforts:sleeping_bag_{c}" for c in COLOURS if f"comforts:sleeping_bag_{c}" in IDS]
HAMMOCKS = [f"comforts:hammock_{c}" for c in COLOURS if f"comforts:hammock_{c}" in IDS]
WAYSTONES = ["waystones:waystone", "waystones:mossy_waystone", "waystones:sandy_waystone", "waystones:deepslate_waystone",
             "waystones:blackstone_waystone", "waystones:end_stone_waystone"]

# Honeycomb rows: 5, 6, 5, 6 tips, 2 cells apart; odd rows are offset by one cell.
R1, R2, R3, R4 = 2.25, 3.75, 5.25, 6.75


def tip(key, x, y, title, subtitle, icon, desc, tasks=None, tokens=0):
    """One optional tip: a checkmark (no tokens) unless it asks for an item (1 token)."""
    return Q(key, x, y, tasks or [tick()], title, subtitle=subtitle, icon=icon, optional=True,
             tokens=tokens, xp=10, desc=desc)


CHAPTER = Chapter("tips", "Tips and Tricks", "minecraft:spyglass",
        ["Small lessons that save a demigod hours. All optional, read them in any order."], SIDE, [
    Q("tp_start", 0, 0, [tick()], "Tips and Tricks", subtitle="A board of short lessons", size=2.0, shape="gear",
      optional=True, tokens=0, xp=10, icon="minecraft:spyglass", desc=[
        "&6You remember knowing every trick of your own world. These belong to this one.&r",
        "&eWhat:&r each card below is one short tip about this pack: how to look things up, get around, and where it differs from other packs.",
        "&eHow:&r read any card and click its checkmark. Nothing here blocks the main path.",
        "&eTip:&r the top row is the most useful on your first day."]),

    # --- row 1: finding things -------------------------------------------------------------------------
    tip("tp_jei", -4, R1, "Look It Up", "R for recipes, U for uses", "minecraft:knowledge_book", [
        "&eWhat:&r JEI shows every recipe in the pack, including the ones changed for progression.",
        "&eHow:&r hover over any item and press &eR&r for how to make it or &eU&r for what it makes. Type &e@modname&r in the search bar to list one mod's items.",
        "&eTip:&r press &eA&r over an item to bookmark it, and use the &e+&r button in a recipe to fill your crafting grid."]),
    tip("tp_jade", -2, R1, "What Am I Looking At?", "Jade's little panel", "minecraft:spyglass", [
        "&eWhat:&r Jade shows a panel at the top of the screen for the block or mob under your crosshair: its name, its mod and its state.",
        "&eHow:&r look at a machine to see its progress, energy and fluids. Look at an ore to see which tool can mine it.",
        "&eTip:&r when a machine stalls, look at it first: Jade usually shows what's missing."]),
    tip("tp_map", 0, R1, "Maps and Waypoints", "JourneyMap draws as you walk", "minecraft:compass", [
        "&eWhat:&r JourneyMap keeps a minimap and a full world map of everywhere you've been.",
        "&eHow:&r press &eJ&r for the full map and right-click a spot to set a waypoint.",
        "&eTip:&r it drops a waypoint where you die, which leads you straight back to your grave."]),
    tip("tp_claims", 2, R1, "Claim and Force-Load", "FTB Chunks keeps your base safe", "minecraft:filled_map", [
        "&eWhat:&r claimed chunks are protected from other players. Force-loaded chunks keep running while you're away.",
        "&eHow:&r press &eM&r and drag over chunks to claim them. The same map force-loads a claimed chunk (its help text shows the clicks).",
        "&eTip:&r force-load your machine rooms and flight area, not your whole base: you have a limited number."]),
    tip("tp_ultimine", 4, R1, "One Swing, Whole Vein", "FTB Ultimine", "minecraft:iron_pickaxe", [
        "&eWhat:&r Ultimine breaks every connected matching block at once: an ore vein, a tree, a strip of stone.",
        "&eHow:&r hold the &e`&r key (left of 1) while you break a block. The Quality of Life page shows the shapes.",
        "&eTip:&r it costs hunger, so eat before you clear a big vein."]),

    # --- row 2: comfort and travel ------------------------------------------------------------------------
    tip("tp_waystone", -5, R2, "Waystones", "Fast travel between your places", "waystones:waystone", [
        "&eWhat:&r activate a waystone once and you can warp to it from any other waystone.",
        "&eHow:&r get any waystone: find one in a village or craft one (check JEI).",
        "&eTip:&r put one at your base, your mine and your Nether portal. A Warp Stone (Market or JEI) warps from anywhere."],
        tasks=[anyof(WAYSTONES)], tokens=1),
    tip("tp_sleeping_bag", -3, R2, "Sleep Anywhere", "A sleeping bag skips the night", "comforts:sleeping_bag_white", [
        "&eWhat:&r a sleeping bag lets you sleep through the night wherever you are, without moving your spawn point.",
        "&eHow:&r get any sleeping bag (check JEI for the recipe). A hammock does the same for the day.",
        "&eTip:&r keep one in your backpack for long trips and deep mines."],
        tasks=[anyof(SLEEPING_BAGS + HAMMOCKS)], tokens=1),
    tip("tp_backpack", -1, R2, "Carry More", "A backpack, and what it can learn", "sophisticatedbackpacks:backpack", [
        "&eWhat:&r Sophisticated Backpacks hold far more than your inventory and take upgrades: pickup, magnet, feeding, crafting and more.",
        "&eHow:&r get a backpack (leather, string and a chest, check JEI).",
        "&eTip:&r the Market sells upgrade bases, so tokens turn into upgrades early. The backpack quest itself is on the Storage page."]),
    tip("tp_shortcuts", 1, R2, "Fewer Clicks", "Bulk recipes and a crafting table on a stick", "crafting_on_a_stick:crafting_table", [
        "&eWhat:&r Utilitarian adds bulk wood recipes (two logs in a column make 16 sticks; chests and ladders straight from logs). Crafting on a Stick puts a crafting table, stonecutter or anvil in your hand.",
        "&eHow:&r press &eU&r on any log in JEI to see the shortcuts.",
        "&eTip:&r a Tool Belt keeps your spare tools one keypress away."]),
    tip("tp_graves", 3, R2, "Death Is Not the End", "Graves, /back and /home", "tombstone:grave_key", [
        "&eWhat:&r when you die, Corail Tombstone keeps your items in a grave where you fell.",
        "&eHow:&r type &e/back&r to return to the spot, or follow JourneyMap's death waypoint, then open the grave.",
        "&eTip:&r &e/sethome&r at your base and &e/home&r gets you back after a long trip."]),
    tip("tp_teams", 5, R2, "Play Together", "Teams share quests and land", "minecraft:player_head", [
        "&eWhat:&r FTB Teams puts players in a party that shares quest progress and claimed chunks.",
        "&eHow:&r open the Teams screen from your inventory (or use &e/ftbteams&r), create a party and invite your friends.",
        "&eTip:&r on a server, form the party early so claims and quest progress are shared from the start."]),

    # --- row 3: this pack's own rules ----------------------------------------------------------------------
    tip("tp_tokens", -4, R3, "Tokens and the Market", "What quests pay, and what it buys", "kubejs:demigod_token", [
        "&eWhat:&r most quests pay Demigod Tokens; nine of them make one Greater Demigod Token.",
        "&eHow:&r the Demigod's Market pages trade tokens for supplies, and JEI shows every crafting trade (search &eDemigod Token&r, press &eU&r).",
        "&eTip:&r the Market sells more of what you've already made, never a way past a tier."]),
    tip("tp_perks", -2, R3, "Periodic Table Perks", "Collect a whole group for a permanent bonus", "chemlib:aluminum", [
        "&eWhat:&r the pack remembers every element you've held. Hold every element of a group once and you keep a bonus for good, even after death.",
        "&eHow:&r type &e/warbucks elements&r to see your progress. Aluminium, tin, lead and indium (the post-transition metals) give +2 armour toughness.",
        "&eTip:&r you only need to hold each element once; you can use it up afterwards."]),
    tip("tp_flexible", 0, R3, "Quests Notice Everything", "No need to do them in order", "ftbquests:book", [
        "&eWhat:&r the book is flexible: an item quest completes as soon as you have the item, even if the quests before it aren't done yet.",
        "&eHow:&r just play. Craft a pickaxe early and its quest ticks off; claim the reward when you get there.",
        "&eTip:&r many quests take any variant (any wood, any colour), so check the task before you craft a specific one."]),
    tip("tp_furnace", 2, R3, "The Fast Furnace", "Every furnace cooks four times faster", "minecraft:furnace", [
        "&eWhat:&r in this pack every furnace, smoker and blast furnace recipe cooks 4x faster, including modded smelting.",
        "&eHow:&r nothing to do: a stack of iron in a plain furnace is done in well under a minute.",
        "&eTip:&r machines from MI, Mekanism and Create keep their own speeds; only vanilla-style cooking is faster."]),
    tip("tp_days", 4, R3, "Long Days, Little Rain", "More daylight to work in", "minecraft:clock", [
        "&eWhat:&r Overworld days last twice as long (about 20 minutes); nights are normal length.",
        "&eHow:&r dry spells are stretched and rain is cut short, so storms come less often.",
        "&eTip:&r a sleeping bag still skips the night, so you can stay in daylight almost all the time."]),

    # --- row 4: chemistry and mining -------------------------------------------------------------------
    tip("tp_deposits", -5, R4, "Rich Deposits", "Scattered ore is thin; deposits are huge", "warbuckscore:spectrometer", [
        "&eWhat:&r loose ore is rarer here, but about one chunk in 16 to 30 hides a rich deposit of hundreds of ores, at a depth that depends on the metal.",
        "&eHow:&r explore caves, use Jade and Ultimine, and later the &eSpectrometer&r (LV): right-click it to read ore signals in the chunks around you.",
        "&eTip:&r a strong signal is usually a deposit. Walk towards it and scan again."]),
    tip("tp_mining_dim", -3, R4, "The Mining Dimension", "A flat world packed with ore", "allthemodium:teleport_pad", [
        "&eWhat:&r a Teleport Pad placed in the Overworld leads to the Mining dimension: flat layers rich in iron, gold, diamond, redstone, tin, lead, nickel, silver and bauxite.",
        "&eHow:&r craft the pad (ender pearl, allthemodium nuggets, MI steel plates, an analog circuit), stand on it with empty hands and sneak + right-click.",
        "&eTip:&r mobs spawn in the dark there, so light your tunnels."]),
    tip("tp_processing", -1, R4, "More Ore From Chemistry", "Acids multiply ore; plain crushing doesn't", "mekanism:dirty_dust_iron", [
        "&eWhat:&r before acids, every route caps at 2x per ore block. Mekanism's chemistry raises it: oxygen 3x, hydrogen chloride 4x, sulfuric acid 5x.",
        "&eChemistry:&r acids dissolve the ore into a solution, which can be purified far better than a crushed rock.",
        "&eTip:&r spin Mekanism's dirty dust in the MI Centrifuge for byproduct metals."]),
    tip("tp_dissolver", 1, R4, "Everything Is Made of Elements", "The Dissolver takes blocks apart", "alchemistry:dissolver", [
        "&eWhat:&r Alchemistry's Dissolver breaks almost any block or item into its elements; the Combiner builds things back up.",
        "&eChemistry:&r atoms are rearranged, never created or destroyed, so what you take apart you can rebuild.",
        "&eTip:&r it's the only way to get some elements as items, like the hydrogen for your first flight."]),
    tip("tp_formulas", 3, R4, "Read the Formula", "Tooltips show what things are made of", "chemlib:sodium_chloride", [
        "&eWhat:&r chemistry items show their formula in the tooltip: ChemLib's elements and compounds, and many machine fluids and gases (H₂, Cl₂, D₂O and more).",
        "&eHow:&r hover over a compound or a fluid bucket in JEI or your inventory.",
        "&eTip:&r the Lab Notebook page explains the real chemistry behind each machine."]),
    tip("tp_multiblocks", 5, R4, "Building Multiblocks", "Where the 3D layouts are shown", "modern_industrialization:guidebook", [
        "&eWhat:&r big machines are multiblocks. You never have to guess their shape.",
        "&eHow:&r press &eR&r on the controller in JEI for its layout, read the MI guidebook, and use Just Enough Mekanism Multiblocks for Mekanism's.",
        "&eTip:&r MI multiblocks also need the right hatches for items, fluids and energy; the guidebook page for each one lists them."]),
], layout="manual")
