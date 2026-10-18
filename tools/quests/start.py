"""Quest chapter: start. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

CHAPTER = Chapter("start", "Getting Started", "minecraft:oak_sapling",
        ["You wake in a world you didn't make, with a god's patience and none of a god's power.",
         "These first steps get you fed, armed, rested and ready for chemistry."], MAIN, [
    Q("gs_wake", 0, 0, [tick()], "The Awakening", subtitle="Everything is made of elements",
      size=2.0, shape="gear", xp=10, deps=["wel_ready"], desc=[
        "&6You remember being more than this.&r The memory is fading, but one idea stays clear: everything is made of elements, and elements can be taken apart and put back together.",
        "&eWhat:&r This book walks you from your first log to antimatter. Follow the lines: each quest unlocks the next.",
        "&eHow:&r Click the checkmark on the right to begin."]),
    Q("gs_jei", 2, -2, [tick()], "Tip: Recipes (JEI)", subtitle="R for recipes, U for uses", deps=["gs_wake"], xp=10, desc=[
        "&eWhat:&r JEI shows every recipe in the pack, including the ones changed for progression.",
        "&eHow:&r Press &eR&r over any item to see how it's made, or &eU&r to see what it's used in. Try it on a quest icon, then click the checkmark.",
        "&eTip:&r Type &e@modname&r in the JEI search bar to list everything one mod adds."]),
    Q("gs_jade", 2, -4, [tick()], "Tip: What Am I Looking At?", subtitle="Jade names every block", deps=["gs_jei"], xp=10, desc=[
        "&eWhat:&r Jade shows a small panel at the top of the screen for whatever block you're looking at.",
        "&eHow:&r Look at any block or machine. Jade shows its name, its mod, and for machines their progress, energy and fluids.",
        "&eTip:&r When a machine isn't working, look at it first. Jade usually tells you why."]),
    Q("gs_table", 2, 0, [item("minecraft:crafting_table")], "Wood and a Workbench", subtitle="Logs, planks, and your first table",
      deps=["gs_wake"], xp=10, items=[("minecraft:torch", 8)], desc=[
        "&eWhat:&r Every tool starts at a crafting table.",
        "&eChemistry:&r Wood is mostly cellulose, (C₆H₁₀O₅)ₙ: long chains of sugar molecules. Later you'll take it apart atom by atom.",
        "&eHow:&r Punch a tree for logs, turn them into planks, and put 4 planks in a 2x2 grid. Any wood works."]),
    Q("gs_woodpick", 4, 0, [item("minecraft:wooden_pickaxe")], "A Wooden Pick", subtitle="Just enough to break stone", deps=["gs_table"], xp=10, desc=[
        "&eWhat:&r A wooden pickaxe is weak, but it can mine stone, and stone is your next step.",
        "&eHow:&r Craft sticks from planks, then 3 planks and 2 sticks in the pickaxe shape.",
        "&eTip:&r Don't bother upgrading it. Stone is minutes away."]),
    Q("gs_stone", 6, 0, [item("minecraft:stone_pickaxe")], "Stone Age", subtitle="Cobblestone tools", deps=["gs_woodpick"], xp=15, desc=[
        "&eWhat:&r Stone tools last longer and can mine iron ore.",
        "&eHow:&r Mine some cobblestone with the wooden pickaxe, then craft a stone pickaxe.",
        "&eTip:&r FTB Ultimine mines a whole vein at once. Hold the &e`&r key (grave/tilde) while breaking blocks."]),
    Q("gs_food", 4, -2, [item("minecraft:bread", 4)], "Something to Eat", subtitle="Wheat, bread, and a full belly",
      deps=["gs_table"], xp=15, items=[("minecraft:bread", 8)], desc=[
        "&eWhat:&r Gods don't need to eat. You do, for now.",
        "&eChemistry:&r Baking turns starch and protein into new compounds. The brown crust comes from the &eMaillard reaction&r between sugars and amino acids.",
        "&eHow:&r Break grass for seeds, farm wheat, and craft bread from 3 wheat.",
        "&eTip:&r AppleSkin shows how much hunger and saturation each food restores."]),
    Q("gs_sleep", 6, -2, [item("comforts:sleeping_bag_white")], "Rest Anywhere", subtitle="Skip the night, keep your spawn", deps=["gs_food"], xp=20, desc=[
        "&eWhat:&r A &esleeping bag&r skips the night without moving your spawn point, so it's great while exploring.",
        "&eHow:&r Craft it from wool. Any colour works for the recipe; this quest wants a white one.",
        "&eTip:&r Hammocks skip the day instead."]),
    Q("gs_shelter", 8, -2, [tick()], "A Roof Overhead", subtitle="Walls, a door, and light", deps=["gs_sleep"], xp=15, desc=[
        "&eWhat:&r Monsters spawn in the dark. A small, lit, enclosed room keeps you safe while you work.",
        "&eHow:&r Build four walls and a roof, add a door, and light the inside with torches. Click the checkmark when you're done.",
        "&eTip:&r Leave room to grow. Your steam machines in Chapter I need floor space."]),
    Q("gs_chest", 4, 2, [item("minecraft:chest", 2)], "Somewhere to Put Things", subtitle="Two chests for your first stockpile", deps=["gs_table"], xp=10, desc=[
        "&eWhat:&r You'll collect far more than you can carry. Chests hold 27 stacks each, and two side by side make a double chest.",
        "&eHow:&r 8 planks in a ring make a chest.",
        "&eTip:&r Inventory sorting works in chests too. Check Controls for the sort key."]),
    Q("gs_coal", 6, 2, [item("minecraft:coal", 16)], "Coal", subtitle="Ancient carbon from the ground", deps=["gs_stone"], xp=15, desc=[
        "&eWhat:&r Coal fuels furnaces now, and becomes coke and steel in Chapter II.",
        "&eChemistry:&r Coal is plant matter buried for millions of years. Heat and pressure drove off most of its hydrogen and oxygen and left mostly carbon.",
        "&eHow:&r Coal ore is the black-speckled stone common in exposed cliffs and mountains. Mine it with any pickaxe.",
        "&eTip:&r Save extra coal. The Coke Oven eats a lot of it."]),
    Q("gs_torch", 8, 2, [item("minecraft:torch", 32)], "Light in the Dark", subtitle="Combustion you can carry", deps=["gs_coal"], xp=15, desc=[
        "&eWhat:&r Torches stop monsters spawning and light up caves.",
        "&eChemistry:&r A torch is &ecombustion&r: carbon reacting with oxygen, C + O₂ → CO₂, releasing heat and light.",
        "&eHow:&r One coal or charcoal on top of one stick makes 4 torches."]),
    Q("gs_furnace", 8, 0, [item("minecraft:furnace"), item("minecraft:charcoal", 4)], "Fire", subtitle="Your first chemistry tool", deps=["gs_stone"], xp=20, desc=[
        "&eWhat:&r Fire is your first chemistry tool. Cooking logs in a furnace makes &echarcoal&r (more on why in Chapter I).",
        "&eChemistry:&r A furnace drives reactions with heat: it cooks food, reduces ores to metal and chars wood into carbon.",
        "&eHow:&r 8 cobblestone in a ring make a furnace. Smelt a log, using a log or planks as fuel."]),
    Q("gs_iron", 10, 0, [item("minecraft:iron_ingot", 16)], "Iron", subtitle="Ore, heat, and carbon make metal", deps=["gs_furnace"], xp=25, desc=[
        "&eWhat:&r Iron is the metal of your first real tools, buckets and armour.",
        "&eChemistry:&r Iron ore is iron oxide. In the furnace, carbon pulls the oxygen away: Fe₂O₃ + 3C → 2Fe + 3CO. That's &ereduction&r.",
        "&eHow:&r Mine iron ore (it's common around Y 16 and in mountains) and smelt it.",
        "&eTip:&r Iron Furnaces (see the Storage and Logistics chapter) smelt faster once you have spare iron."]),
    Q("gs_ironpick", 12, -1, [item("minecraft:iron_pickaxe")], "Iron Pickaxe", subtitle="Diamonds, gold and redstone open up", deps=["gs_iron"], xp=25, desc=[
        "&eWhat:&r Needed for diamonds, redstone and gold, and to start the journey to the Nether.",
        "&eChemistry:&r Iron is harder than stone because its atoms sit in a regular metal lattice held by metallic bonds, which bend rather than shatter.",
        "&eHow:&r 3 iron ingots and 2 sticks."]),
    Q("gs_shield", 10, -2, [item("minecraft:shield")], "Shield", subtitle="Block the arrows", deps=["gs_iron"], xp=15, desc=[
        "&eWhat:&r A shield blocks arrows, melee hits and creeper blasts while you hold right-click.",
        "&eHow:&r 1 iron ingot and 6 planks (check JEI for the shape).",
        "&eTip:&r Hold it in your off-hand so you can block and swing at the same time."]),
    Q("gs_armor", 12, -3, [item("minecraft:iron_helmet"), item("minecraft:iron_chestplate"), item("minecraft:iron_leggings"), item("minecraft:iron_boots")],
      "Iron Armour", subtitle="A full set before you dig deep", deps=["gs_shield"], xp=30, desc=[
        "&eWhat:&r A full set of iron armour makes caves and the night survivable.",
        "&eHow:&r Helmet, chestplate, leggings and boots take 24 iron ingots in total.",
        "&eTip:&r Ultimine through an iron vein and you'll have this set in minutes."]),
    Q("gs_bucket", 12, 1, [item("minecraft:water_bucket")], "Water", subtitle="The most important chemical in the pack", deps=["gs_iron"], xp=15, desc=[
        "&eWhat:&r Water is the most important chemical in this pack: steam, electrolysis and acids all start with it.",
        "&eChemistry:&r H₂O is a small, polar molecule. That polarity lets it dissolve salts and acids, which is why chemists call it the universal solvent.",
        "&eHow:&r 3 iron ingots make a bucket. Fill it at any water source."]),
    Q("gs_backpack", 10, 2, [item("sophisticatedbackpacks:backpack")], "A Backpack", subtitle="More pockets, upgradeable later", deps=["gs_iron"], xp=20, desc=[
        "&eWhat:&r More inventory, and it can be upgraded later (pickup, magnet, feeding and more).",
        "&eHow:&r Craft it from leather, string and a chest (check JEI). Wear it in the chest slot or keep it in your inventory.",
        "&eTip:&r Backpack upgrades are in the Demigod Token shop."]),
    Q("gs_claim", 14, -1, [tick()], "Claim Your Land", subtitle="Protect your base with FTB Chunks", deps=["gs_ironpick", "gs_armor"], xp=20, desc=[
        "&eWhat:&r FTB Chunks protects your base and can keep it loaded while you're away.",
        "&eHow:&r Press &eM&r to open the map, then drag over chunks to claim them. Click the checkmark when done.",
        "&eTip:&r Right-click a claimed chunk to force-load it. You'll need that for the flight pylon later."]),
    Q("gs_paxel", 12, 3, [item("mekanismtools:iron_paxel")], "The Paxel", subtitle="Pickaxe, axe and shovel in one", deps=["gs_iron"], xp=25, desc=[
        "&eWhat:&r A &epaxel&r is a pickaxe, axe and shovel in one tool. Mekanism Tools adds them for every material, from wood to refined obsidian.",
        "&eHow:&r Craft an iron pickaxe, axe and shovel together with 2 sticks (check JEI).",
        "&eTip:&r One tool slot instead of three leaves more room for ore."]),
    Q("gs_silent", 14, 3, [item("silentgear:blueprint_paper"), item("silentgear:pickaxe")], "Tools from Parts", subtitle="Silent Gear: stats come from materials",
      deps=["gs_paxel"], xp=40, desc=[
        "&eWhat:&r Silent Gear builds tools from parts. Each part's stats come from its &ematerial&r, so better chemistry means better tools.",
        "&eHow:&r Make Blueprint Paper, craft a Pickaxe Blueprint, then craft a pickaxe head and rod.",
        "&eTip:&r The Tools and Comfort chapter goes deeper."]),
    Q("gs_ready", 16, 0, [tick()], "Ready for Chemistry", subtitle="Fed, armed, sheltered", size=1.5, shape="hexagon",
      deps=["gs_claim", "gs_bucket"], xp=50, items=[("minecraft:copper_ingot", 16), ("modern_industrialization:tin_ingot", 8)], desc=[
        "&6Fed, armed, sheltered.&r Now the real work begins: fire, ore, alloys, and the slow road back to divinity.",
        "&eHow:&r Click to open Chapter I. The copper and tin in the reward are a head start on your first alloy.",
        "&eTip:&r Bring spare coal and iron. Chapter I eats both."]),

    # --- optional side quests -------------------------------------------------------------
    Q("gs_opt_ores", 14, -3, [item("minecraft:coal"), item("minecraft:raw_iron"), item("minecraft:raw_copper"), item("minecraft:raw_gold"),
                              item("minecraft:redstone"), item("minecraft:lapis_lazuli"), item("minecraft:diamond"), item("minecraft:emerald")],
      "Rock Collector", subtitle="One of every vanilla ore drop", deps=["gs_ironpick"], optional=True, tokens=2, xp=30, desc=[
        "&eWhat:&r Collect one drop from every vanilla ore. Emeralds only generate in mountain biomes.",
        "&eChemistry:&r Real ores are minerals: iron comes from oxides like hematite (Fe₂O₃), copper often from sulfides like chalcopyrite (CuFeS₂), and diamond is pure carbon.",
        "&eTip:&r Every one of these can go into the Dissolver later. Keep spares."]),
    Q("gs_opt_cook", 6, -4, [item("farmersdelight:cooking_pot"), item("farmersdelight:beef_stew")], "Kitchen Chemistry", subtitle="Farmer's Delight: a proper meal",
      deps=["gs_food"], optional=True, tokens=1, xp=20, desc=[
        "&eWhat:&r Farmer's Delight meals restore more hunger and give the Nourishment and Comfort effects.",
        "&eChemistry:&r Stewing denatures proteins: heat unfolds them, which is why meat turns firm and tender.",
        "&eHow:&r Craft a Cooking Pot (iron, bricks, a water bucket and a wooden shovel), set it over a campfire or stove, and cook raw beef, a carrot and a potato.",
        "&eTip:&r Check JEI for the Cooking Pot's other recipes."]),
    Q("gs_opt_spyglass", 8, 4, [item("minecraft:spyglass")], "A Closer Look", subtitle="Copper and amethyst", deps=["gs_torch"], optional=True, tokens=1, xp=15, desc=[
        "&eWhat:&r A spyglass lets you scout terrain and spot ore in cliff faces from far away.",
        "&eChemistry:&r Amethyst is quartz (SiO₂). Its purple colour comes from traces of iron in the crystal.",
        "&eHow:&r 2 copper ingots and 1 amethyst shard. Amethyst geodes sit underground, ringed with smooth basalt."]),
    Q("gs_opt_paxels", 14, 5, [item("mekanismtools:wood_paxel"), item("mekanismtools:stone_paxel"), item("mekanismtools:gold_paxel"), item("mekanismtools:diamond_paxel")],
      "Paxel Collector", subtitle="Wood, stone, gold and diamond", deps=["gs_paxel"], optional=True, tokens=2, xp=30, desc=[
        "&eWhat:&r Craft the early paxels you skipped, plus a diamond one for the long haul.",
        "&eChemistry:&r Gold is soft because its atoms slide past each other easily. Diamond is the hardest natural material because every carbon atom is locked to four neighbours.",
        "&eHow:&r Same recipe as the iron paxel: pickaxe, axe and shovel of one material, plus 2 sticks."]),
])
