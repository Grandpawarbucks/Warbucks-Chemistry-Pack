"""Quest chapter: qol. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

CHAPTER = Chapter("qol", "Quality of Life", "akashictome:tome",
        ["Small things that make a big difference."], SIDE, [
    # --- Basics (y=0) --------------------------------------------------------------------------
    Q("q_tome", 0, 0, [item("akashictome:tome")], "One Book to Rule Them All", deps=["gs_table"], xp=20,
      subtitle="Every guidebook in one item", desc=[
        "&6You remember a library that held everything. A single book will have to do.&r",
        "&eWhat:&r the Akashic Tome merges every mod's guidebook into one item.",
        "&eHow:&r craft it, then right-click it with other guidebooks to add them.",
        "&eTip:&r right-click the tome to choose which book to open."]),
    Q("q_compass", 2, 0, [item("naturescompass:naturescompass"), item("explorerscompass:explorerscompass")], "Find Anything", deps=["gs_iron"], xp=30,
      subtitle="Compasses for biomes and structures", desc=[
        "&eWhat:&r Nature's Compass finds biomes; Explorer's Compass finds structures (Nether Fortresses, Ancient Cities, villages).",
        "&eHow:&r craft both (check JEI), right-click to pick a target, then follow the needle.",
        "&eTip:&r the Explorer's Compass is the fastest way to find an Ancient City for the Deeper and Darker quests."]),
    Q("q_torch", 4, 0, [item("torchmaster:megatorch")], "No More Mob Spawns", deps=["gs_iron"], xp=40,
      subtitle="One torch, a huge safe radius", desc=[
        "&eWhat:&r the Mega Torch stops hostile mobs spawning naturally in a huge radius.",
        "&eHow:&r check JEI for the recipe and place it near the middle of your base.",
        "&eTip:&r it blocks natural spawns only. Spawners and Simulation Chambers still work."]),
    Q("q_grave", 6, 0, [tick()], "Graves", deps=["gs_iron"], xp=10,
      subtitle="Your items wait where you fell", desc=[
        "&eWhat:&r if you die, Corail Tombstone keeps your items in a grave where you fell.",
        "&eHow:&r walk back and open the grave to recover everything. Click the checkmark once you've read this.",
        "&eTip:&r JourneyMap drops a waypoint where you died, so the grave is easy to find."]),
    Q("q_backups", 8, 0, [tick()], "Backups", deps=["gs_iron"], xp=10,
      subtitle="Automatic world saves", desc=[
        "&eWhat:&r Simple Backups saves your world automatically.",
        "&eHow:&r on a server, backups live in the server's backups folder. In single player, look in your instance folder.",
        "&eTip:&r copy a backup somewhere else before trying risky reactor builds."]),
    Q("q_dreadlamp", 5, -1.5, [item("torchmaster:dreadlamp")], "Dread Lamp", deps=["q_torch", "t2_nether"], xp=40,
      optional=True, tokens=1, subtitle="Optional: the Mega Torch for Nether mobs", desc=[
        "&eWhat:&r the Dread Lamp blocks Nether mob spawns in a large radius, the way the Mega Torch does for Overworld mobs.",
        "&eHow:&r check JEI. Place it at your Nether base or portal hub.",
        "&eTip:&r place it before building in the Nether so your base stays quiet."]),

    # --- Backpacks (y=2) -----------------------------------------------------------------------
    Q("q_stick", 8, 2, [item("crafting_on_a_stick:crafting_table")], "Crafting on a Stick", deps=["gs_table"], xp=20,
      subtitle="A crafting table that fits in your pocket", desc=[
        "&eWhat:&r a crafting table you carry around. Right-click it to open a 3x3 grid anywhere: in a mine, out exploring, mid-build.",
        "&eHow:&r craft it from a crafting table and a stick (check JEI). The same mod makes pocket versions of the stonecutter, smithing table, anvil, grindstone, loom and cartography table.",
        "&eTip:&r it saves a hotbar slot over placing and breaking tables. The pocket stonecutter is great for building with Create Deco and Rechiseled blocks."]),
    Q("q_stick_more", 8, 3.5, [item("crafting_on_a_stick:stonecutter"), item("crafting_on_a_stick:smithing_table")], "A Whole Workshop", deps=["q_stick"], xp=20, optional=True, tokens=1,
      subtitle="Pocket stonecutter and smithing table", desc=[
        "&eWhat:&r optional: the pocket stonecutter and smithing table.",
        "&eHow:&r each one is its block plus a stick (check JEI).",
        "&eTip:&r the smithing table is how netherite and Apotheosis upgrades are applied, so it's handy to carry."]),
    Q("q_bp_up", 0, 2, [item("sophisticatedbackpacks:pickup_upgrade"), item("sophisticatedbackpacks:magnet_upgrade")], "Backpack Upgrades", deps=["gs_backpack"], xp=40,
      subtitle="Pickup and magnet upgrades", desc=[
        "&eWhat:&r pickup and magnet upgrades pull items straight into your backpack.",
        "&eHow:&r craft an Upgrade Base, then the upgrades (check JEI). Put them in the backpack's upgrade slots.",
        "&eTip:&r set a filter on the pickup upgrade so it only grabs ores and drops you actually want."]),
    Q("q_bp_iron", 2, 2, [item("sophisticatedbackpacks:iron_backpack")], "Iron Backpack", deps=["gs_backpack"], xp=30,
      subtitle="More slots and more upgrade space", desc=[
        "&eWhat:&r each backpack tier adds inventory rows and upgrade slots: iron, gold, diamond, netherite.",
        "&eHow:&r surround your backpack with iron ingots (check JEI). It keeps everything inside.",
        "&eTip:&r stack upgrades multiply how many items fit in each slot."]),
    Q("q_bp_feeding", 1, 3.5, [item("sophisticatedbackpacks:feeding_upgrade")], "Feeding Upgrade", deps=["q_bp_up"], xp=30,
      optional=True, tokens=1, subtitle="Optional: never stop to eat again", desc=[
        "&eWhat:&r eats food from the backpack automatically when you're hungry.",
        "&eHow:&r check JEI. Farmer's Delight meals restore a lot per bite.",
        "&eTip:&r set a filter so it doesn't eat your golden apples."]),
    Q("q_bp_netherite", 3, 3.5, [item("sophisticatedbackpacks:netherite_backpack")], "Netherite Backpack", deps=["q_bp_iron"], xp=150,
      optional=True, tokens=2, subtitle="Optional: the biggest backpack", desc=[
        "&eWhat:&r the top tier: the most inventory slots and upgrade space.",
        "&eHow:&r ring the backpack with gold, then diamonds, then smith in a netherite ingot with a netherite upgrade template.",
        "&eTip:&r a netherite backpack has room for several stack upgrades at once."]),

    # --- Getting around (y=5.5) ----------------------------------------------------------------
    Q("q_waystone", 0, 5.5, [item("waystones:waystone")], "Waystones", deps=["gs_iron"], xp=40,
      subtitle="Teleport between your places", desc=[
        "&eWhat:&r waystones are teleport points. Activate one by right-clicking it, then warp between any you've activated.",
        "&eHow:&r found in villages, or craft one (check JEI). Place them at your base, mines and portals.",
        "&eTip:&r warping costs a little XP depending on distance; check the config if it seems steep."]),
    Q("q_warp_scroll", 1, 7, [item("waystones:warp_scroll", 4)], "Warp Scrolls", deps=["q_waystone"], xp=30,
      optional=True, tokens=1, subtitle="Optional: one-use trips to any waystone", desc=[
        "&eWhat:&r a single-use warp to any activated waystone, handy before you can afford a Warp Stone.",
        "&eHow:&r paper, an ender pearl, gold nuggets and an ink sac (check JEI).",
        "&eTip:&r keep one in your backpack for emergencies."]),
    Q("q_map", 2, 5.5, [tick()], "Maps", deps=["gs_table"], xp=15,
      subtitle="JourneyMap and FTB Chunks", desc=[
        "&eWhat:&r JourneyMap draws a minimap and a full world map as you explore, with waypoints.",
        "&eHow:&r press &eJ&r for the full JourneyMap. FTB Chunks has its own map for claims (check Controls for its key). Click the checkmark when you've tried them.",
        "&eTip:&r drop a waypoint at every rich ore deposit you find. Deposits are rare, so note the depth too."]),
    Q("q_claim", 4, 5.5, [tick()], "Claim Your Land", deps=["q_map"], xp=20,
      subtitle="Protect your base with FTB Chunks", desc=[
        "&6You remember a whole world that answered to you. Start with a few chunks.&r",
        "&eWhat:&r claimed chunks are protected from other players and explosions (per your team settings). Force-loaded chunks keep machines running while you're away.",
        "&eHow:&r open the FTB Chunks map and drag across chunks to claim them (the map's help shows the controls). Click the checkmark when done.",
        "&eTip:&r force-load your main factory so chemical lines don't stall when you travel."]),
    Q("q_tips", 6, 5.5, [tick()], "Inventory Tricks", deps=["gs_table"], xp=10,
      subtitle="Sorting, dragging and a trash slot", desc=[
        "&eWhat:&r small mods that save hours: Mouse Tweaks (drag and scroll to move stacks), Inventory Tweaks (sorting) and TrashSlot (a trash can in your inventory).",
        "&eHow:&r try a scroll-wheel drag over stacks, the sort button, and the trash slot by your hotbar. Click the checkmark when done.",
        "&eTip:&r Polymorph shows a button when two recipes share a grid; click it to pick the one you want."]),

    # --- Building (y=9) ------------------------------------------------------------------------
    Q("q_effortless", 0, 9, [item("effortlessbuilding:randomizer_tool")], "Effortless Building", deps=["gs_table"], xp=20,
      subtitle="Mirror, array and line building", desc=[
        "&eWhat:&r Effortless Building adds mirror, array and line modes for big builds.",
        "&eHow:&r open its menu (check Controls) and pick a mode. The randomizer places a random mix of the blocks you load into it.",
        "&eTip:&r the randomizer with stone, andesite and cobblestone makes natural-looking walls."]),
    Q("q_gadget", 2, 9, [item("buildinggadgets2:gadget_building")], "Building Gadgets", deps=["t3_hull"], xp=40,
      subtitle="Place whole surfaces with FE", desc=[
        "&eWhat:&r FE-powered gadgets that place, swap, copy and remove blocks in bulk.",
        "&eHow:&r iron, redstone, lapis and a diamond (check JEI). Charge it in an energy cube.",
        "&eTip:&r link the gadget to a chest or backpack so it pulls blocks from storage."]),
    Q("q_gadget_copy", 1, 10.5, [item("buildinggadgets2:gadget_copy_paste"), item("buildinggadgets2:template_manager")], "Copy and Paste", deps=["q_gadget"], xp=60,
      optional=True, tokens=1, subtitle="Optional: copy a whole build", desc=[
        "&eWhat:&r copy an area and paste it elsewhere; the Template Manager saves copies to share.",
        "&eHow:&r check JEI. Great for repeating a chemical reactor cell or a row of machines.",
        "&eTip:&r templates can be shared with friends on the server."]),
    Q("q_gadget_exchange", 3, 10.5, [item("buildinggadgets2:gadget_exchanging")], "Exchanging Gadget", deps=["q_gadget"], xp=40,
      optional=True, tokens=1, subtitle="Optional: swap blocks in place", desc=[
        "&eWhat:&r replaces blocks in an area with another block, keeping the shape.",
        "&eHow:&r check JEI. Perfect for turning a cobble shell into something pretty.",
        "&eTip:&r it uses the blocks in your inventory, so carry enough."]),
])
