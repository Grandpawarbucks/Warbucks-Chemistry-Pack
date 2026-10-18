"""Quest chapter: start. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

CHAPTER = Chapter("start", "Getting Started", "minecraft:oak_sapling",
        ["You wake in a world you didn't make, with a god's patience and none of a god's power.",
         "These first steps get you fed, armed, rested and ready for chemistry."], MAIN, [
    Q("gs_wake", 0, 0, [tick()], "The Awakening", size=2.0, shape="gear", xp=10, deps=["wel_ready"], desc=[
        "&6You remember being more than this.&r The memory is fading, but one idea stays clear:",
        "&eeverything is made of elements, and elements can be taken apart and put back together.&r",
        "",
        "This book walks you from your first log to antimatter. Follow the lines: each quest unlocks the next.",
        "How: click the checkmark on the right to begin."]),
    Q("gs_jei", 2, -2, [tick()], "Tip: Recipes (JEI)", deps=["gs_wake"], xp=10, desc=[
        "Press &eR&r over any item to see how it's made, or &eU&r to see what it's used in.",
        "Every recipe in this pack, including the ones changed for progression, shows in JEI.",
        "How: try it on a quest icon, then click the checkmark."]),
    Q("gs_table", 2, 0, [item("minecraft:crafting_table")], "Wood and a Workbench", deps=["gs_wake"], xp=10,
      items=[("minecraft:torch", 8)], desc=[
        "Punch a tree for logs, turn them into planks, and craft a crafting table.",
        "How: any wood works. Planks in a 2x2 grid make the table."]),
    Q("gs_stone", 4, 0, [item("minecraft:stone_pickaxe")], "Stone Age", deps=["gs_table"], xp=15, desc=[
        "Make a wooden pickaxe, mine some cobblestone, then craft a stone pickaxe.",
        "How: tip: FTB Ultimine lets you mine a whole vein at once. Hold the &e`&r key (grave/tilde) while breaking blocks."]),
    Q("gs_food", 4, -2, [item("minecraft:bread", 4)], "Something to Eat", deps=["gs_table"], xp=15,
      items=[("minecraft:bread", 8)], desc=[
        "Gods don't need to eat. You do, for now.",
        "How: break grass for seeds, farm wheat, and craft bread (3 wheat). AppleSkin shows the hunger each food restores."]),
    Q("gs_sleep", 6, -2, [item("comforts:sleeping_bag_white")], "Rest Anywhere", deps=["gs_food"], xp=20, desc=[
        "A &esleeping bag&r skips the night without moving your spawn point, so it's great while exploring.",
        "How: craft it from wool (any colour works for the recipe; this quest wants a white one). Hammocks skip the day."]),
    Q("gs_furnace", 6, 0, [item("minecraft:furnace"), item("minecraft:charcoal", 4)], "Fire", deps=["gs_stone"], xp=20, desc=[
        "Fire is your first chemistry tool. Cooking logs in a furnace makes &echarcoal&r (more on why in Chapter I).",
        "How: 8 cobblestone make a furnace. Smelt a log with a log or planks as fuel."]),
    Q("gs_iron", 8, 0, [item("minecraft:iron_ingot", 16)], "Iron", deps=["gs_furnace"], xp=25, desc=[
        "Mine iron ore (it's common around Y 16 and in mountains) and smelt it.",
        "How: Iron Furnaces (see the Storage and Logistics chapter) smelt faster once you have spare iron."]),
    Q("gs_ironpick", 10, -1, [item("minecraft:iron_pickaxe")], deps=["gs_iron"], xp=25, desc=[
        "Needed for diamonds, redstone and gold, and to start the journey to the Nether."]),
    Q("gs_bucket", 10, 1, [item("minecraft:water_bucket")], "Water", deps=["gs_iron"], xp=15, desc=[
        "Water is the most important chemical in this pack: steam, electrolysis and acids all start with it.",
        "How: 3 iron ingots make a bucket. Fill it at any water source."]),
    Q("gs_backpack", 8, 2, [item("sophisticatedbackpacks:backpack")], "A Backpack", deps=["gs_iron"], xp=20, desc=[
        "More inventory, and it can be upgraded later (pickup, magnet, feeding and more).",
        "How: craft it from leather, string and a chest. Wear it in the chest slot or keep it in your inventory."]),
    Q("gs_claim", 12, 0, [tick()], "Claim Your Land", deps=["gs_ironpick"], xp=20, desc=[
        "FTB Chunks protects your base and can keep it loaded while you're away.",
        "How: press &eM&r to open the map, then drag over chunks to claim them. Right-click a claimed chunk to force-load it (needed for the flight pylon later).",
        "Click the checkmark when done."]),
    Q("gs_paxel", 12, 2, [item("mekanismtools:iron_paxel")], "The Paxel", deps=["gs_iron"], xp=25, desc=[
        "A &epaxel&r is a pickaxe, axe and shovel in one tool. Mekanism Tools adds them for every material, from wood to refined obsidian.",
        "How: craft an iron pickaxe, axe and shovel together with sticks (check JEI)."]),
    Q("gs_silent", 14, 2, [item("silentgear:blueprint_paper"), item("silentgear:pickaxe")], "Tools from Parts", deps=["gs_paxel"], xp=40, desc=[
        "Silent Gear builds tools from parts. Each part's stats come from its &ematerial&r, so better chemistry means better tools.",
        "How: make Blueprint Paper, craft a Pickaxe Blueprint, then craft a pickaxe head and rod. The Tools and Comfort chapter goes deeper."]),
    Q("gs_ready", 14, 0, [tick()], "Ready for Chemistry", size=1.5, shape="hexagon", deps=["gs_claim", "gs_bucket"], xp=50, items=[("minecraft:copper_ingot", 16), ("modern_industrialization:tin_ingot", 8)], desc=[
        "&6Fed, armed, sheltered.&r Now the real work begins: fire, ore, alloys, and the slow road back to divinity.",
        "How: click to open Chapter I."]),
])
