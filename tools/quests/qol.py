"""Quest chapter: qol (Basics group). See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

A catalogue page: the hub ql_start (after gs_table), then one row per topic, mostly optional entries.
Rows: base comforts, backpacks and pocket crafting, getting around, controls and multiplayer, and
(from y=10) the Utilitarian mod, merged in from the old utilitarian.py chapter (ut_* keys unchanged).
"""
from questlib import Q, Chapter, item, dim, tick, anytag, anyof, MAIN, SIDE  # noqa: F401

CHAPTER = Chapter("qol", "Quality of Life", "akashictome:tome",
        ["Small things that make a big difference."], SIDE, [
    Q("ql_start", -1, 1, [tick()], "Comfort First", deps=["gs_table"], xp=10, size=1.5, shape="hexagon",
      subtitle="A catalogue of small conveniences", desc=[
        "&6You remember never wasting a motion. These small things feel familiar.&r",
        "&eWhat:&r this page collects the mods that save time and clicks: guidebooks, backpacks, waystones, maps, keybinds and the Utilitarian shortcuts.",
        "&eHow:&r each row is one topic. Nearly everything here is optional, so pick what helps you. Click the checkmark to open the page.",
        "&eTip:&r none of this is needed for the main path, but most of it pays for itself within an hour."]),

    # --- Basics (y=0) --------------------------------------------------------------------------
    Q("q_tome", 0, 0, [item("akashictome:tome")], "One Book to Rule Them All", deps=["ql_start"], xp=20,
      subtitle="Every guidebook in one item", desc=[
        "&eWhat:&r the Akashic Tome merges every mod's guidebook into one item.",
        "&eHow:&r craft it, then right-click it with other guidebooks to add them.",
        "&eTip:&r right-click the tome to choose which book to open."]),
    Q("q_compass", 2, 0, [item("naturescompass:naturescompass"), item("explorerscompass:explorerscompass")], "Find Anything", deps=["ql_start", "gs_iron"], xp=30,
      subtitle="Compasses for biomes and structures", desc=[
        "&eWhat:&r Nature's Compass finds biomes; Explorer's Compass finds structures (Nether Fortresses, Ancient Cities, villages).",
        "&eHow:&r craft both (check JEI), right-click to pick a target, then follow the needle.",
        "&eTip:&r the Explorer's Compass is the fastest way to find an Ancient City for the Deeper and Darker quests."]),
    Q("q_torch", 4, 0, [item("torchmaster:megatorch")], "No More Mob Spawns", deps=["ql_start", "gs_iron"], xp=40,
      subtitle="One torch, a huge safe radius", desc=[
        "&eWhat:&r the Mega Torch stops hostile mobs spawning naturally in a huge radius.",
        "&eHow:&r check JEI for the recipe and place it near the middle of your base.",
        "&eTip:&r it blocks natural spawns only. Spawners and Simulation Chambers still work."]),
    Q("q_grave", 6, 0, [tick()], "Graves", deps=["ql_start", "gs_iron"], xp=10,
      subtitle="Your items wait where you fell", desc=[
        "&eWhat:&r if you die, Corail Tombstone keeps your items in a grave where you fell.",
        "&eHow:&r walk back and open the grave to recover everything. Click the checkmark once you've read this.",
        "&eTip:&r JourneyMap drops a waypoint where you died, so the grave is easy to find."]),
    Q("q_backups", 8, 0, [tick()], "Backups", deps=["ql_start"], xp=10,
      optional=True, tokens=1, subtitle="Optional: automatic world saves", desc=[
        "&eWhat:&r Simple Backups saves your world automatically.",
        "&eHow:&r on a server, backups live in the server's backups folder. In single player, look in your instance folder.",
        "&eTip:&r copy a backup somewhere else before trying risky reactor builds."]),
    Q("q_dreadlamp", 5, -1.5, [item("torchmaster:dreadlamp")], "Dread Lamp", deps=["q_torch", "t2_nether"], xp=40,
      optional=True, tokens=1, subtitle="Optional: the Mega Torch for Nether mobs", desc=[
        "&eWhat:&r the Dread Lamp blocks Nether mob spawns in a large radius, the way the Mega Torch does for Overworld mobs.",
        "&eHow:&r check JEI. Place it at your Nether base or portal hub.",
        "&eTip:&r place it before building in the Nether so your base stays quiet."]),

    Q("gs_sleep", 0, 0, [anytag("comforts:sleeping_bags")], "Rest Anywhere", subtitle="Skip the night, keep your spawn", deps=["ql_start", "gs_bed"], xp=20, desc=[
        "&eWhat:&r A &esleeping bag&r from Comforts skips the night without moving your spawn point, so it's ideal while exploring.",
        "&eHow:&r 3 wool of one colour in a vertical column. Any colour of sleeping bag counts.",
        "&eTip:&r Hammocks skip the day instead (Gear and Comfort page)."]),
    # --- Backpacks (y=2) -----------------------------------------------------------------------
    Q("q_stick", 8, 2, [item("crafting_on_a_stick:crafting_table")], "Crafting on a Stick", deps=["ql_start"], xp=20,
      subtitle="A crafting table that fits in your pocket", desc=[
        "&eWhat:&r a crafting table you carry around. Right-click it to open a 3x3 grid anywhere: in a mine, out exploring, mid-build.",
        "&eHow:&r craft it from a crafting table and a stick (check JEI). The same mod makes pocket versions of the stonecutter, smithing table, anvil, grindstone, loom and cartography table.",
        "&eTip:&r it saves a hotbar slot over placing and breaking tables. The pocket stonecutter is great for building with Create Deco and Rechiseled blocks."]),
    Q("q_stick_more", 8, 3.5, [item("crafting_on_a_stick:stonecutter"), item("crafting_on_a_stick:smithing_table")], "A Whole Workshop", deps=["q_stick"], xp=20, optional=True, tokens=1,
      subtitle="Pocket stonecutter and smithing table", desc=[
        "&eWhat:&r optional: the pocket stonecutter and smithing table.",
        "&eHow:&r each one is its block plus a stick (check JEI).",
        "&eTip:&r the smithing table is how netherite and Apotheosis upgrades are applied, so it's handy to carry."]),
    Q("q_bp_up", 0, 2, [item("sophisticatedbackpacks:pickup_upgrade"), item("sophisticatedbackpacks:magnet_upgrade")], "Backpack Upgrades", deps=["ql_start", "gs_backpack"], xp=40,
      subtitle="Pickup and magnet upgrades", desc=[
        "&eWhat:&r pickup and magnet upgrades pull items straight into your backpack.",
        "&eHow:&r craft an Upgrade Base, then the upgrades (check JEI). Put them in the backpack's upgrade slots.",
        "&eTip:&r set a filter on the pickup upgrade so it only grabs ores and drops you actually want."]),
    Q("q_bp_iron", 2, 2, [item("sophisticatedbackpacks:iron_backpack")], "Iron Backpack", deps=["ql_start", "gs_backpack"], xp=30,
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
    Q("q_waystone", 0, 5.5, [item("waystones:waystone")], "Waystones", deps=["ql_start", "gs_iron"], xp=40,
      subtitle="Teleport between your places", desc=[
        "&eWhat:&r waystones are teleport points. Activate one by right-clicking it, then warp between any you've activated.",
        "&eHow:&r found in villages, or craft one (check JEI). Place them at your base, mines and portals.",
        "&eTip:&r warping costs a little XP depending on distance; check the config if it seems steep."]),
    Q("q_warp_scroll", 1, 7, [item("waystones:warp_scroll", 4)], "Warp Scrolls", deps=["q_waystone"], xp=30,
      optional=True, tokens=1, subtitle="Optional: one-use trips to any waystone", desc=[
        "&eWhat:&r a single-use warp to any activated waystone, handy before you can afford a Warp Stone.",
        "&eHow:&r paper, an ender pearl, gold nuggets and an ink sac (check JEI).",
        "&eTip:&r keep one in your backpack for emergencies."]),
    Q("q_map", 2, 5.5, [tick()], "Maps", deps=["ql_start"], xp=15,
      subtitle="JourneyMap and FTB Chunks", desc=[
        "&eWhat:&r JourneyMap draws a minimap and a full world map as you explore, with waypoints.",
        "&eHow:&r press &eJ&r for the full JourneyMap. FTB Chunks has its own map for claims (check Controls for its key). Click the checkmark when you've tried them.",
        "&eTip:&r drop a waypoint at every rich ore deposit you find. Deposits are rare, so note the depth too."]),
    Q("q_tips", 6, 5.5, [tick()], "Inventory Tricks", deps=["ql_start"], xp=10,
      subtitle="Sorting, dragging and a trash slot", desc=[
        "&eWhat:&r small mods that save hours: Mouse Tweaks (drag and scroll to move stacks), Inventory Tweaks (sorting) and TrashSlot (a trash can in your inventory).",
        "&eHow:&r try a scroll-wheel drag over stacks, the sort button, and the trash slot by your hotbar. Click the checkmark when done.",
        "&eTip:&r Polymorph shows a button when two recipes share a grid; click it to pick the one you want."]),

    # --- More basics (y=-1.5) ------------------------------------------------------------------
    Q("ql_feral", 3, -1.5, [item("torchmaster:feral_flare_lantern")], "Feral Flare Lantern", deps=["q_torch", "t2_nether"], xp=30,
      optional=True, tokens=1, subtitle="Optional: light a whole cave at once", desc=[
        "&eWhat:&r the lantern places invisible light sources in the dark spots around it, so a cave or a big hall lights up without a single torch.",
        "&eHow:&r gold ingots, glass and glowstone dust (check JEI). Place it in the middle of the room.",
        "&eTip:&r great for a clean-looking factory floor. It still lets mobs spawn in spots it can't reach."]),
    Q("ql_tomb", 6, -3, [tick()], "Grave Tricks", deps=["q_grave"], xp=10,
      optional=True, tokens=1, subtitle="Optional: more from Corail Tombstone", desc=[
        "&eWhat:&r Corail Tombstone does more than store your items: it adds scrolls, tablets and the Ankh of Prayer, plus a book that makes items soulbound.",
        "&eHow:&r search 'tombstone' in JEI to browse them. Click the checkmark when you've had a look.",
        "&eTip:&r by default only you can open your grave, so a death on a server doesn't mean losing your gear to someone else."]),
    Q("ql_lootr", 8, -1.5, [tick()], "Loot for Everyone", deps=["ql_start", "gs_iron"], xp=10,
      optional=True, tokens=1, subtitle="Optional: every player gets their own chest loot", desc=[
        "&eWhat:&r with Lootr, structure chests (dungeons, temples, villages, mineshafts) hold separate loot for each player.",
        "&eHow:&r open any generated chest. You get your own roll; your friends still get theirs. Click the checkmark when you've seen one.",
        "&eTip:&r on a server, nobody has to race to a dungeon first."]),

    # --- More backpack upgrades (y=2 / 3.5) ----------------------------------------------------
    Q("ql_bp_stack", 4, 2, [item("sophisticatedbackpacks:stack_upgrade_tier_1")], "Stack Upgrade", deps=["q_bp_iron"], xp=30,
      optional=True, tokens=1, subtitle="Optional: more items per slot", desc=[
        "&eWhat:&r a stack upgrade multiplies how many items each backpack slot holds. Higher tiers multiply more.",
        "&eHow:&r check JEI; each tier is built from the one before it.",
        "&eTip:&r stack upgrades make a backpack the best place to carry dust and ingots between machines."]),
    Q("ql_bp_tools", 6, 2, [item("sophisticatedbackpacks:tool_swapper_upgrade")], "Tool Swapper", deps=["ql_bp_stack"], xp=30,
      optional=True, tokens=1, subtitle="Optional: the right tool, automatically", desc=[
        "&eWhat:&r swaps the tool in your hand for the best one in your backpack when you start mining a block or hitting a mob.",
        "&eHow:&r check JEI, then put it in an upgrade slot and fill the backpack with tools.",
        "&eTip:&r pairs well with a paxel; it switches to shears or a sword only when needed."]),
    Q("ql_bp_refill", 5, 3.5, [item("sophisticatedbackpacks:refill_upgrade")], "Refill Upgrade", deps=["ql_bp_stack"], xp=30,
      optional=True, tokens=1, subtitle="Optional: never run out of torches", desc=[
        "&eWhat:&r keeps chosen hotbar items topped up from the backpack: torches, blocks, food.",
        "&eHow:&r check JEI. Set the items to refill in the upgrade's tab.",
        "&eTip:&r refill building blocks while bridging and you'll never stop to open your inventory."]),
    Q("ql_stick_anvil", 10, 3.5, [item("crafting_on_a_stick:anvil"), item("crafting_on_a_stick:grindstone")], "Pocket Anvil", deps=["q_stick_more"], xp=20,
      optional=True, tokens=1, subtitle="Optional: repair and disenchant anywhere", desc=[
        "&eWhat:&r pocket versions of the anvil and grindstone, opened with right-click.",
        "&eHow:&r each one is its block plus a stick (check JEI).",
        "&eTip:&r the pocket anvil wears down like a placed one, so carry a spare for long trips."]),

    # --- Controls and commands (x=10..14) ------------------------------------------------------
    Q("ql_ultimine", 10, 0, [tick()], "FTB Ultimine", deps=["ql_start", "gs_stone"], xp=15,
      subtitle="Break a whole vein in one swing", desc=[
        "&eWhat:&r Ultimine breaks every connected matching block at once: a full ore vein, a tree, a strip of stone.",
        "&eHow:&r hold the Ultimine key (default &e`&r, the key left of 1) and break a block. Arrow keys up and down change the shape. Click the checkmark when you've tried it.",
        "&eTip:&r it can cost extra hunger, so eat first. Shapes include tunnels and flat planes for clearing space."]),
    Q("ql_team", 12, 0, [tick()], "Form a Team", deps=["ql_start"], xp=15,
      subtitle="Share quests, claims and loot", desc=[
        "&eWhat:&r FTB Teams groups players into a party. Teammates share quest progress and claimed chunks.",
        "&eHow:&r open the Teams screen from the button on your inventory screen (or use /ftbteams) and create a party, then invite friends. Click the checkmark when done.",
        "&eTip:&r playing alone? A solo party still lets you set chunk permissions for visitors."]),
    Q("ql_home", 14, 0, [tick()], "Homes and /back", deps=["ql_team"], xp=15,
      subtitle="FTB Essentials teleport commands", desc=[
        "&eWhat:&r FTB Essentials adds /sethome and /home (one home by default), /back to return to where you died or last teleported, /spawn, and /tpa to ask to teleport to a friend.",
        "&eHow:&r stand at your base and type /sethome, then try /home from somewhere else. Click the checkmark when done.",
        "&eTip:&r each command has a short cooldown. /back after a death walks you straight to your grave."]),
    Q("ql_zoom", 10, 2, [tick()], "Just Zoom", deps=["ql_start"], xp=10,
      optional=True, tokens=1, subtitle="Optional: a spyglass without the spyglass", desc=[
        "&eWhat:&r Just Zoom lets you zoom in on the distance with a key, no item needed.",
        "&eHow:&r find its key under Options → Controls, and hold it to zoom (its options are in the Mods menu). Click the checkmark when you've tried it.",
        "&eTip:&r handy for spotting structures, meteorites and villages from a hilltop."]),
    Q("ql_ping", 12, 2, [tick()], "Ping Wheel", deps=["ql_team"], xp=10,
      optional=True, tokens=1, subtitle="Optional: point things out to friends", desc=[
        "&eWhat:&r Ping Wheel puts a marker on the spot you look at, visible to the other players nearby.",
        "&eHow:&r find its keys under Options → Controls. Look at something and ping it. Click the checkmark when done.",
        "&eTip:&r ping an ore deposit or a dangerous mob instead of typing coordinates."]),
    Q("ql_chatheads", 14, 2, [tick()], "Chat Heads", deps=["ql_team"], xp=10,
      optional=True, tokens=1, subtitle="Optional: see who's talking", desc=[
        "&eWhat:&r Chat Heads shows each player's face next to their messages in chat.",
        "&eHow:&r nothing to set up; it works as soon as someone talks. Click the checkmark when you've seen it.",
        "&eTip:&r its options are in the Mods menu if you want to change how heads are shown."]),
    Q("ql_trade", 12, 4, [item("minecraft:emerald", 16)], "Trade Cycling", deps=["ql_start", "gs_iron"], xp=30,
      optional=True, tokens=1, subtitle="Reroll a villager's offers", desc=[
        "&eWhat:&r Trade Cycling adds a button to the villager trade screen that rerolls the offers of a villager nobody has traded with yet.",
        "&eHow:&r give a villager a job block, open its trades and press the cycle button until the offer you want appears. Earn 16 emeralds by trading.",
        "&eTip:&r once you trade, the offers lock. Cycle a librarian until it sells the enchanted book you need."]),
    Q("ql_baron", 12, 5.5, [item("minecraft:emerald_block", 4)], "Merchant Prince", deps=["ql_trade"], xp=40,
      secret=True, loot="secret", subtitle="Secret: a demigod with a market stall", desc=[
        "&eWhat:&r four emerald blocks: 36 emeralds. The villagers have noticed you.",
        "&eChemistry:&r emerald is beryl, Be₃Al₂Si₆O₁₈, coloured green by traces of chromium.",
        "&eTip:&r every Warp Stone needs an emerald, so a good trading hall pays for your travel network."]),
    Q("ql_belt", 14, 4, [item("toolbelt:belt")], "Tool Belt", deps=["ql_start", "gs_iron"], xp=20,
      optional=True, tokens=1, subtitle="Optional: tools on a quick wheel", desc=[
        "&eWhat:&r the Tool Belt holds tools outside your hotbar and opens as a radial menu so you can swap fast.",
        "&eHow:&r leather and string (check JEI). Keep it in your inventory; find its key under Options → Controls.",
        "&eTip:&r put the wrench, the config card and your paxel on the belt."]),
    Q("ql_pouch", 16, 4, [item("toolbelt:pouch", 2)], "Belt Pouches", deps=["ql_belt"], xp=20,
      optional=True, tokens=1, subtitle="Optional: more slots on the belt", desc=[
        "&eWhat:&r each pouch adds a slot to your tool belt.",
        "&eHow:&r craft pouches, then craft them together with the belt (check JEI).",
        "&eTip:&r a full belt keeps your hotbar free for blocks and food."]),

    # --- More getting around (y=7) -------------------------------------------------------------
    Q("ql_waystones", 3, 7, [anyof(["waystones:waystone", "waystones:mossy_waystone", "waystones:sandy_waystone", "waystones:deepslate_waystone",
                                    "waystones:blackstone_waystone", "waystones:end_stone_waystone"], 4)], "A Waystone Network", deps=["q_waystone"], xp=40,
      optional=True, tokens=1, subtitle="Optional: four more waystones", desc=[
        "&eWhat:&r one waystone is a landmark; four make a network. Base, mine, Nether portal and a far-off biome.",
        "&eHow:&r any four waystones of any style (check JEI for the variants), or bring back ones found in villages.",
        "&eTip:&r name each one clearly ('Bauxite Mine -40') so the list stays readable."]),
    Q("ql_warpstone", 5, 7, [item("waystones:warp_stone")], "Warp Stone", deps=["ql_waystones"], xp=40,
      optional=True, tokens=1, subtitle="Optional: warp from anywhere", desc=[
        "&eWhat:&r a reusable item that opens the waystone menu wherever you stand. It recharges after each use.",
        "&eHow:&r amethyst shards, ender pearls and an emerald (check JEI). It's also sold in the Market.",
        "&eTip:&r with a Warp Stone, warp scrolls become backup only."]),
    Q("ql_waypoints", 7, 7, [tick()], "Waypoints", deps=["q_map"], xp=10,
      optional=True, tokens=1, subtitle="Optional: never lose a deposit again", desc=[
        "&eWhat:&r JourneyMap waypoints mark places on the minimap and in the world, with distance shown on screen.",
        "&eHow:&r open the full map (&eJ&r) and right-click a spot to add a waypoint, or use JourneyMap's waypoint key (see Controls). Click the checkmark when you've made one.",
        "&eTip:&r JourneyMap makes a death waypoint for you; share waypoints with teammates in chat."]),

    # ===== Utilitarian (merged from the old utilitarian chapter; recipes checked against utilitarian-1.21.1-0.19.2.jar) =====
    # --- Bulk wood recipes (y=10) ---------------------------------------------------------------
    Q("ut_sticks", 0, 10, [tick()], "Utilitarian Shortcuts", deps=["ql_start"], xp=10,
      subtitle="Logs straight to sticks, chests and ladders", desc=[
        "&eWhat:&r the Utilitarian mod adds bulk recipes that skip the planks step (two logs in a column make 16 sticks), plus small handy blocks: tiny coal, the Trowel, the Angel Block, Snad and more. This row is its catalogue.",
        "&eHow:&r press U on any log in JEI to see every log shortcut. Click the checkmark when you've had a look.",
        "&eTip:&r the bulk recipes give the same items as the vanilla ones, just with fewer clicks and no waste."]),
    Q("ut_chests", 2, 10, [item("minecraft:chest", 4), item("minecraft:ladder", 24)], "Chests and Ladders", deps=["ut_sticks"], xp=10,
      optional=True, tokens=1, subtitle="Optional: eight logs, four chests", desc=[
        "&eWhat:&r logs in a chest ring make 4 chests at once. Seven logs in a ladder shape make 24 ladders.",
        "&eHow:&r the same shapes as the plank recipes, but with logs (check JEI).",
        "&eTip:&r three logs in a V make 12 bowls, and logs between iron make a hopper without a chest."]),
    Q("ut_building", 4, 10, [anytag("minecraft:wooden_slabs", 24), anytag("minecraft:wooden_stairs", 16)], "Slabs and Stairs", deps=["ut_sticks"], xp=15,
      optional=True, tokens=1, subtitle="Optional: a row of logs, a stack of slabs", desc=[
        "&eWhat:&r three logs in a row make 24 slabs; six logs in a stair shape make 16 stairs.",
        "&eHow:&r use logs of one wood type in the usual slab or stair shape (check JEI).",
        "&eTip:&r two slabs placed diagonally in the grid turn back into a plank, so leftover slabs are never wasted."]),
    Q("ut_doors", 6, 10, [anytag("minecraft:wooden_doors", 12), anytag("minecraft:wooden_trapdoors", 12)], "Doors and Trapdoors", deps=["ut_building"], xp=15,
      optional=True, tokens=1, subtitle="Optional: six logs, a dozen doors", desc=[
        "&eWhat:&r six logs in a door shape make 12 doors; six logs in a trapdoor shape make 12 trapdoors.",
        "&eHow:&r one wood type per craft (check JEI). Two logs side by side also make 4 pressure plates.",
        "&eTip:&r doors placed side by side open together, so a double door needs only one click."]),
    Q("ut_redye", 8, 10, [anytag("c:concretes", 8)], "Re-Dyeing", deps=["ut_doors"], xp=15,
      optional=True, tokens=1, subtitle="Optional: wrong colour? Dye it again", desc=[
        "&eWhat:&r Utilitarian lets you re-dye concrete, concrete powder, terracotta, stained glass, glass panes and candles that already have a colour.",
        "&eChemistry:&r real pigments are chemicals too: concrete's colours come from metal oxides, like iron oxide (Fe₂O₃) for red and brown.",
        "&eHow:&r eight coloured blocks around one dye re-colours all eight, or one block plus one dye does a single block (check JEI).",
        "&eTip:&r it also mixes blue and yellow dye into green, so cactus isn't the only green."]),

    # --- Early tools and fuel (y=12) ------------------------------------------------------------
    Q("ut_tiny_coal", 0, 12, [item("utilitarian:tiny_coal", 8), item("utilitarian:tiny_charcoal", 8)], "Tiny Coal", deps=["ut_sticks", "gs_coal"], xp=15,
      subtitle="One coal split eight ways", desc=[
        "&eWhat:&r one coal or charcoal makes 8 tiny pieces. Each burns for 10 seconds, so you don't waste a whole coal on one item.",
        "&eChemistry:&r charcoal is wood heated without air (pyrolysis): water and volatile compounds are driven off, leaving mostly carbon.",
        "&eHow:&r put one coal or charcoal in the crafting grid. Eight tiny pieces craft back into one.",
        "&eTip:&r this pack's furnaces cook faster than vanilla, so one tiny coal covers more than one item."]),
    Q("ut_trowel", 2, 12, [item("utilitarian:trowel")], "The Trowel", deps=["ut_sticks", "gs_iron"], xp=15,
      subtitle="Places random blocks from your hotbar", desc=[
        "&eWhat:&r the Trowel places a random block from your hotbar each time you use it. Great for natural-looking walls and paths.",
        "&eHow:&r two iron ingots and a stick (check JEI). Sneak-use it to switch between hotbar only and your whole inventory.",
        "&eTip:&r fill the hotbar with stone, cobblestone, andesite and tuff, and a plain wall looks weathered in seconds."]),
    Q("ut_angel", 4, 12, [item("utilitarian:angel_block", 4)], "Angel Block", deps=["ut_sticks", "gs_iron"], xp=25,
      subtitle="A block you can place in mid-air", desc=[
        "&eWhat:&r the Angel Block can be placed in empty air, with nothing next to it. It's the start of any sky bridge or floating build.",
        "&eHow:&r two feathers, two gold ingots and obsidian (check JEI). Use it while looking at empty air.",
        "&eTip:&r it's a building block, not flight. Flying in this pack is a chemistry milestone (see the Nether chapter)."]),

    # --- Blocks that move things (y=14) ---------------------------------------------------------
    Q("ut_snad", 0, 14, [item("utilitarian:snad", 4)], "Snad", deps=["ut_tiny_coal"], xp=20,
      subtitle="Sand that makes plants grow taller", desc=[
        "&eWhat:&r cactus, sugar cane, kelp and bamboo grow taller and faster on Snad. Soul Snad does the same for nether wart.",
        "&eChemistry:&r sand is mostly quartz grains, SiO₂, the same compound as the Nether quartz and certus you'll meet later.",
        "&eHow:&r two sand make one Snad (red sand makes Red Snad, soul sand makes Soul Snad).",
        "&eTip:&r a column of sugar cane on Snad is the fastest paper source for Sophisticated upgrades and Iron Furnace augments."]),
    Q("ut_magnet", 2, 14, [item("utilitarian:magnet")], "Block Magnet", deps=["ut_trowel"], xp=25,
      optional=True, tokens=1, subtitle="Optional: powered magnet that lifts iron blocks", desc=[
        "&eWhat:&r with a redstone signal, the Block Magnet pulls iron blocks, steel blocks and anvils below it up towards it.",
        "&eChemistry:&r iron is ferromagnetic: its atoms' tiny magnetic moments line up in domains. The recipe is an electromagnet, an iron core with copper on each side.",
        "&eHow:&r copper ingot, iron block, copper ingot in a row. Place it, put an iron block somewhere below, and power the magnet.",
        "&eTip:&r a magnet and a lever make a simple lift for iron blocks: power it to pull them up, cut the power to let them fall."]),
    Q("ut_fluid_hopper", 4, 14, [item("utilitarian:fluid_hopper")], "Fluid Hopper", deps=["ut_trowel", "gs_bucket"], xp=25,
      subtitle="A hopper for liquids", desc=[
        "&eWhat:&r the Fluid Hopper moves fluids the way a hopper moves items: it collects fluid from above and passes it on, the way a hopper does with items (check its JEI page).",
        "&eHow:&r iron ingots around a bucket, with white dye on top (check JEI).",
        "&eTip:&r under an infinite water source it fills a tank for your first steam boiler without any pump."]),
    Q("ut_dropper", 6, 14, [item("utilitarian:well_behaved_dropper")], "Well Behaved Dropper", deps=["ut_trowel"], xp=20,
      optional=True, tokens=1, subtitle="Optional: a dropper that doesn't spray", desc=[
        "&eWhat:&r a dropper that drops items neatly in front of itself instead of flinging them in random directions.",
        "&eHow:&r a dropper with a gold nugget on each side (check JEI).",
        "&eTip:&r drop items onto a pressure plate or into water streams and they land exactly where you planned."]),

    # --- Redstone and sound (y=16) --------------------------------------------------------------
    Q("ut_clock", 0, 16, [item("utilitarian:redstone_clock")], "Redstone Clock", deps=["ut_snad"], xp=20,
      subtitle="A pulse generator in one block", desc=[
        "&eWhat:&r the Redstone Clock pulses a redstone signal on its own, with no repeater loop.",
        "&eHow:&r chiseled stone bricks with redstone on four sides (check JEI). Right-click it with an empty hand to change the speed; sneak to change it faster.",
        "&eTip:&r a slow clock on a dispenser or a Well Behaved Dropper makes a simple timed feeder."]),
    Q("ut_tps", 2, 16, [item("utilitarian:tps_meter")], "TPS Meter", deps=["ut_clock"], xp=25,
      optional=True, tokens=1, subtitle="Optional: how hard is the server working?", desc=[
        "&eWhat:&r the TPS Meter gives a redstone signal based on the dimension's ticks per second. A healthy server runs at 20.",
        "&eHow:&r four comparators around obsidian (check JEI).",
        "&eTip:&r wire it to a lamp in your factory: if it dims, something you built is lagging the server."]),
    Q("ut_muffler", 4, 16, [item("utilitarian:sound_muffler")], "Sound Muffler", deps=["ut_clock"], xp=15,
      optional=True, tokens=1, subtitle="Optional: silence a noisy machine room", desc=[
        "&eWhat:&r the Sound Muffler mutes sounds in a radius around it. Your crushers, pumps and boilers go quiet.",
        "&eChemistry:&r real soundproofing works the same way: soft, porous fibres like wool turn sound energy into a tiny amount of heat.",
        "&eHow:&r any wool plus a note block, shapeless.",
        "&eTip:&r one in the middle of a machine row is usually enough. Its tooltip shows the radius."]),

    # --- Traders, raiders and mobs (y=18) -------------------------------------------------------
    Q("ut_carpet", 0, 18, [anyof(["utilitarian:white_soliciting_carpet", "utilitarian:orange_soliciting_carpet", "utilitarian:magenta_soliciting_carpet",
        "utilitarian:light_blue_soliciting_carpet", "utilitarian:yellow_soliciting_carpet", "utilitarian:lime_soliciting_carpet",
        "utilitarian:pink_soliciting_carpet", "utilitarian:gray_soliciting_carpet", "utilitarian:light_gray_soliciting_carpet",
        "utilitarian:cyan_soliciting_carpet", "utilitarian:purple_soliciting_carpet", "utilitarian:blue_soliciting_carpet",
        "utilitarian:brown_soliciting_carpet", "utilitarian:green_soliciting_carpet", "utilitarian:red_soliciting_carpet",
        "utilitarian:black_soliciting_carpet"])], "Trader Carpet", deps=["ut_clock"], xp=15,
      subtitle="Wandering traders land here, not on you", desc=[
        "&eWhat:&r a wandering trader arriving nearby appears on a Trader Carpet instead of right in your face.",
        "&eHow:&r any carpet plus a small flower, shapeless. Each colour has its own carpet.",
        "&eTip:&r put it in a little market stall by your base. JEI also shows a trapped version, if you're feeling unkind."]),
    Q("ut_banner", 2, 18, [item("utilitarian:no_soliciting_banner")], "No Soliciting", deps=["ut_carpet"], xp=15,
      optional=True, tokens=1, subtitle="Optional: a banner that keeps traders away", desc=[
        "&eWhat:&r the No Soliciting Banner stops wandering traders from spawning in the chunks around it.",
        "&eHow:&r wool, a lead and a stick, in a banner shape (check JEI).",
        "&eTip:&r use either the carpet or the banner: carpet if you like the trader's goods, banner if you don't."]),
    Q("ut_raider", 4, 18, [item("utilitarian:no_raider_block")], "Outpost Claim", deps=["ut_banner"], xp=40,
      optional=True, tokens=1, subtitle="Optional: stop pillagers returning to an outpost", desc=[
        "&eWhat:&r place the Raider Outpost Claim Block inside a pillager outpost and raiders stop coming back to it.",
        "&eHow:&r the recipe uses an ominous (illager) banner, which a pillager captain drops (check JEI).",
        "&eTip:&r claim the outpost before building there; it makes a fine tower base."]),
    Q("ut_unname", 6, 18, [item("utilitarian:unname_tag")], "Un-Name Tag", deps=["ut_banner"], xp=15,
      optional=True, tokens=1, subtitle="Optional: undo a name tag", desc=[
        "&eWhat:&r the Un-Name Tag removes a mob's custom name.",
        "&eHow:&r a name tag plus white dye, shapeless. Use it on the named mob.",
        "&eTip:&r useful when a pet name typo has been bothering you for weeks."]),
    Q("ut_slime", 8, 18, [item("utilitarian:slime_bucket")], "Slime in a Bucket", deps=["ut_unname"], xp=25,
      secret=True, loot="secret", subtitle="Secret: it gets excited near its friends", desc=[
        "&6You remember finding hidden things by feel. The slime remembers too.&r",
        "&eWhat:&r you scooped a small slime into a bucket. It gets visibly excited when you carry it into a slime chunk.",
        "&eHow:&r use an empty bucket on a small slime. Place it again by using the bucket on the ground.",
        "&eTip:&r slime chunks spawn slimes underground at any light level, which makes them the best spot for a slime farm."]),

    # ===== ATM10-aligned round (2026-10-19): vanilla workshop blocks, redstone and the other pylons =====
    # --- the vanilla workshop (y=20) ------------------------------------------------------------
    Q("ql_enchanting", 0, 0, [item("minecraft:enchanting_table"), item("minecraft:bookshelf", 15), item("minecraft:book", 3)], "The Enchanting Table", deps=["ql_start", "gs_ironpick"], xp=40,
      optional=True, tokens=1, subtitle="Optional: books, obsidian and a diamond or two", desc=[
        "&eWhat:&r the enchanting table, with the 15 bookshelves it needs for level 30 enchantments. Apotheosis makes it much deeper (Magic group).",
        "&eChemistry:&r paper is pressed cellulose fibre; old books yellow because acids left in the paper slowly break those chains (and lignin oxidises).",
        "&eHow:&r table: a book, 2 diamonds and 4 obsidian. Bookshelf: 6 planks and 3 books. Book: 3 paper and a leather.",
        "&eTip:&r leave one block of air between the table and the shelves, or they don't count."]),
    Q("ql_anvil", 0, 0, [item("minecraft:anvil")], "Anvil", deps=["ql_start", "gs_iron"], xp=20,
      optional=True, tokens=1, subtitle="Optional: repair, rename, combine", desc=[
        "&eWhat:&r the anvil joins enchanted books to tools, repairs gear with its own material, and renames items.",
        "&eChemistry:&r a real anvil is a block of hardened steel on a softer body: the hard face doesn't dent, the soft body doesn't crack.",
        "&eHow:&r 3 iron blocks and 4 iron ingots: 31 iron in all.",
        "&eTip:&r every repair raises the 'too expensive' cost. Combine books first, then put them on the tool in one go."]),
    Q("ql_map_clock", 0, 0, [item("minecraft:map"), item("minecraft:compass"), item("minecraft:clock")], "Map, Compass and Clock", deps=["ql_start", "gs_iron"], xp=20,
      optional=True, tokens=1, subtitle="Optional: the vanilla navigator's kit", desc=[
        "&eWhat:&r a map draws the land as you walk; a compass points to world spawn (or a lodestone); a clock shows the time of day, even underground.",
        "&eChemistry:&r a real compass needle is magnetised iron. The first ones (China, about 1,000 years ago) used lodestone, naturally magnetic magnetite, Fe₃O₄.",
        "&eHow:&r map: paper around a compass. Compass: 4 iron around redstone. Clock: 4 gold around redstone.",
        "&eTip:&r JourneyMap does the mapping for you; a framed map on the wall is still a nice trophy."]),
    Q("ql_redstone", 0, 0, [item("minecraft:lever"), item("minecraft:redstone_torch", 4), item("minecraft:repeater", 2)], "Redstone Basics", deps=["ql_start", "gs_ironpick"], xp=20,
      optional=True, tokens=1, subtitle="Optional: switches, inverters and delays", desc=[
        "&eWhat:&r the three parts of most redstone builds: a lever (a switch), a redstone torch (a NOT gate) and a repeater (a delay and a booster).",
        "&eChemistry:&r redstone is fiction, but the logic is real: a torch is an inverter, exactly like a transistor wired as a NOT gate in every chip you own.",
        "&eHow:&r lever: a stick on cobblestone. Torch: redstone on a stick. Repeater: 2 torches and redstone on stone.",
        "&eTip:&r MI and Mekanism machines can be switched off with redstone; a lever by your machines saves power at night."]),
    Q("ql_daylight", 0, 0, [item("minecraft:daylight_detector")], "Daylight Detector", deps=["ql_redstone", "t2_quartz"], xp=20,
      optional=True, tokens=1, subtitle="Optional: a switch that knows the time", desc=[
        "&eWhat:&r it outputs a signal that follows the sun. Right-click it to invert, so it fires at night instead.",
        "&eChemistry:&r a real light sensor is a photodiode: light knocks electrons loose in a semiconductor and a current flows. Same physics as a solar panel, just smaller.",
        "&eHow:&r glass, Nether quartz and wooden slabs (check JEI).",
        "&eTip:&r inverted, it switches on street lamps at dusk."]),
    Q("ql_conduit", 0, 0, [item("minecraft:conduit")], "Conduit Power", deps=["ql_start", "ex_treasure"], xp=60,
      optional=True, tokens=1, subtitle="Optional: breathe and see underwater", desc=[
        "&eWhat:&r an activated conduit gives Conduit Power to players in the water nearby: no drowning, night vision underwater and faster mining. A bigger frame also attacks hostile mobs.",
        "&eChemistry:&r nautilus shells are aragonite, a form of calcium carbonate (CaCO₃) with a different crystal packing from calcite. The pearly sheen is layers of it thinner than a wavelength of light.",
        "&eHow:&r a heart of the sea (buried treasure) in 8 nautilus shells (drowned and fishing). Place it in water inside a frame of prismarine (check the wiki shape in JEI's info tab).",
        "&eTip:&r perfect for an underwater base, or for clearing an ocean monument."]),

    # --- the other pylons (y=22): flight is in Chapter II; these guard and farm a claim ---------
    Q("ql_pylon_harvester", 0, 0, [tick()], "Harvester Pylon", deps=['t2_pylon', 'fd_breed'], optional=True, tokens=0, xp=0, icon="pylons:harvester_pylon", subtitle="Moved: see Harvester Pylon", desc=["&eMoved:&r this step is now \"Harvester Pylon\" on the Pylons page. Click to dismiss."]),
    Q("ql_pylon_interdiction", 0, 0, [tick()], "Interdiction Pylon", deps=['t2_pylon', 't2_debris'], optional=True, tokens=0, xp=0, icon="pylons:interdiction_pylon", subtitle="Moved: see Interdiction Pylon", desc=["&eMoved:&r this step is now \"Interdiction Pylon\" on the Pylons page. Click to dismiss."]),
    Q("ql_pylon_guard", 0, 0, [tick()], "Guard Pylons", deps=['t2_pylon', 'ql_team'], optional=True, tokens=0, xp=0, icon="pylons:protection_pylon", subtitle="Moved: see Protection Pylon", desc=["&eMoved:&r this step is now \"Protection Pylon\" on the Pylons page. Click to dismiss."]),
], links=[("gs_table", -3, 0), ("gs_bed", -3, -1.5), ("gs_iron", -3, 2), ("gs_backpack", -3, 3.5), ("gs_stone", 10, -1.5)])
