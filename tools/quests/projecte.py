"""Quest chapter: projecte (ProjectE 'lite'). See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

Pack rules (pack/kubejs/server_scripts/phase4_projecte.js, pack/config/ProjectE/custom_emc.json):
the Philosopher's Stone needs chemlib:oganesson, condensers/collectors/relays are removed, and metals,
gems, dusts, ores, plates and Nether Stars have no EMC. Only building blocks and similar keep EMC.
"""
from questlib import Q, Chapter, item, tick, anyof, SIDE  # noqa: F401

PE = "projecte:"
BAGS = [PE + c + "_alchemical_bag" for c in (
    "white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray",
    "light_gray", "cyan", "purple", "blue", "brown", "green", "red", "black")]

CHAPTER = Chapter("projecte", "Equivalent Exchange", PE + "philosophers_stone",
        ["A builder's toy for a demigod who has already mastered the elements."], SIDE, [
    # --- The stone and the table (y=0) --------------------------------------------------------
    Q("pe_stone", 0, 0, [item(PE + "philosophers_stone")], "The Philosopher's Stone", deps=["t6_table"], xp=300,
      size=1.5, shape="hexagon", subtitle="Oganesson, at the heart of an old legend", desc=[
        "&6You remember turning one thing into another with a thought. Now you know what it really costs.&r",
        "&eWhat:&r the Philosopher's Stone transmutes blocks in the world and is the key to every ProjectE item.",
        "&eChemistry:&r alchemists spent centuries looking for a stone that turns lead into gold. Real transmutation needs a nuclear reaction, and you've already done that: it's how you made oganesson.",
        "&eHow:&r redstone dust and glowstone dust in a ring around one oganesson (this pack's recipe).",
        "&eTip:&r it isn't used up in crafting recipes, so one stone lasts forever."]),
    Q("pe_world", 2, 0, [tick()], "World Transmutation", deps=["pe_stone"], xp=50,
      subtitle="Right-click to reshape the land", optional=True, tokens=1, desc=[
        "&eWhat:&r right-click a block with the stone to turn it into a related block: stone and cobblestone, dirt, grass and sand, one wood or flower type into the next.",
        "&eHow:&r an outline shows what will change before you click; sneak-click for the reverse direction. ProjectE's keybinds change the area size and shape.",
        "&eTip:&r a whole hillside of stone into cobblestone (or back) takes seconds. Click the checkmark once you've tried it."]),
    Q("pe_table", 4, 0, [item(PE + "transmutation_table")], "Transmutation Table", deps=["pe_stone"], xp=150,
      subtitle="Learn a block once, make it forever", desc=[
        "&eWhat:&r the Transmutation Table turns items into EMC and EMC back into any item you've learned.",
        "&eHow:&r four obsidian in the corners, four stone on the sides, the Philosopher's Stone in the centre.",
        "&eTip:&r your EMC and your learned items belong to you, not the table: every table you open shows the same list."]),
    Q("pe_learn", 6, 0, [tick()], "Burn to Learn", deps=["pe_table"], xp=50,
      subtitle="What EMC can and can't do here", optional=True, tokens=1, desc=[
        "&eWhat:&r placing an item in the table's burn slot destroys it, adds its EMC to your total and teaches you that item.",
        "&eHow:&r burn a stack of something cheap (cobblestone, logs, sand), then try to burn an iron ingot. The ingot has no EMC, so it can't be learned.",
        "&eTip:&r stone, wood, glass, terracotta, wool and other building materials all work. Click the checkmark when you understand the rule."]),
    Q("pe_covalence", 8, 0, [item(PE + "low_covalence_dust", 8), item(PE + "medium_covalence_dust", 8), item(PE + "high_covalence_dust", 8)],
      "Covalence Dust", deps=["pe_stone"], xp=60, subtitle="ProjectE's crafting dusts", desc=[
        "&eWhat:&r three dusts used for ProjectE storage and repairs.",
        "&eChemistry:&r a covalent bond is two atoms sharing electrons. The name fits: these dusts bind items together.",
        "&eHow:&r low: charcoal and 8 cobblestone. Medium: an iron ingot and redstone. High: a diamond and coal. Each recipe makes 40.",
        "&eTip:&r covalence dust repairs tools in a crafting grid: the matching dust for the tool's material."]),
    Q("pe_chest", 10, 0, [item(PE + "alchemical_chest")], "Alchemical Chest", deps=["pe_covalence"], xp=60,
      subtitle="A big chest for ProjectE items", desc=[
        "&eWhat:&r a large chest, and the base of the Alchemical Bag.",
        "&eHow:&r one of each covalence dust on top, stone, a diamond and stone in the middle, iron, a chest and iron on the bottom."]),
    Q("pe_bag", 12, 0, [anyof(BAGS)], "Alchemical Bag", deps=["pe_chest"], xp=100,
      subtitle="The same inventory everywhere you go", optional=True, tokens=1, desc=[
        "&eWhat:&r an Alchemical Bag shares its inventory with every bag of the same colour you own.",
        "&eHow:&r three high covalence dust on top, wool on each side of an Alchemical Chest, and three wool below. Dye the wool for a different colour.",
        "&eTip:&r keep one colour for building blocks so your supplies follow you between builds."]),
    Q("pe_repair", 9, -1.5, [item(PE + "repair_talisman")], "Repair Talisman", deps=["pe_covalence"], xp=75,
      optional=True, tokens=1, subtitle="Optional: slowly mends your gear", desc=[
        "&eWhat:&r while it's in your inventory it slowly repairs your damaged tools and armor.",
        "&eHow:&r covalence dusts, string and paper (check JEI for the pattern)."]),
    Q("pe_tablet", 11, -1.5, [item(PE + "transmutation_tablet")], "Transmutation Tablet", deps=["pe_table", "pe_dm"], xp=300,
      optional=True, tokens=2, subtitle="Optional: the table, in your pocket", desc=[
        "&eWhat:&r a portable Transmutation Table.",
        "&eHow:&r four Dark Matter blocks, four stone and a Transmutation Table. That's sixteen Dark Matter: a real project.",
        "&eTip:&r worth it for big builds far from home."]),

    # --- Why EMC is limited (y=2) --------------------------------------------------------------
    Q("pe_why", 0, 2, [tick()], "The Law of Conservation", deps=["pe_stone"], xp=50,
      subtitle="Why you can't conjure metal", optional=True, tokens=1, desc=[
        "&eWhat:&r in this pack, EMC works on building blocks only. Metals, gems, dusts, ores and plates have no EMC.",
        "&eHow:&r read the second page, then click the checkmark.",
        "{@pagebreak}",
        "&eThe rule:&r ProjectE normally gives every item an EMC value, so a pile of cobblestone can become diamonds. In a chemistry pack that would skip everything you've built.",
        "&eChemistry:&r matter isn't created or destroyed in a chemical reaction (Lavoisier, 1789). Iron comes from iron oxide, Fe₂O₃ + 3CO → 2Fe + 3CO₂. Copper comes from its ores. Gold comes from anode sludge and aqua regia. You can rearrange atoms; you can't conjure them.",
        "&eSo:&r ingots, nuggets, raw ores, dusts, gems, plates, gears, rods, wires and storage blocks are set to EMC 0. Nether Stars, the Dragon Egg and the Beacon are 0 too, because the Seed of a New World needs them.",
        "&eAlso removed:&r Energy Condensers, Collectors and Relays. They turn EMC into unlimited items or power.",
        "&eWhat's left:&r a terraforming and building tool. Stone, wood, glass, sand, dirt and decoration are what a demigod reshapes the world with, and those still have EMC."]),

    # --- Fuels and Dark Matter (y=2) ----------------------------------------------------------
    Q("pe_coal", 2, 2, [item(PE + "alchemical_coal", 4)], "Alchemical Coal", deps=["pe_stone"], xp=50,
      subtitle="Four coal, compressed", desc=[
        "&eWhat:&r a dense fuel and the first step toward Dark Matter.",
        "&eChemistry:&r coal is mostly carbon. Packing more energy into less mass is what refining fuel is all about.",
        "&eHow:&r the Philosopher's Stone and four coal (shapeless). It must be real coal, not charcoal.",
        "&eTip:&r it also burns far longer than coal in a furnace."]),
    Q("pe_mobius", 4, 2, [item(PE + "mobius_fuel", 4)], "Mobius Fuel", deps=["pe_coal"], xp=60,
      subtitle="Four alchemical coal, compressed", desc=[
        "&eWhat:&r the next fuel tier.",
        "&eHow:&r the Philosopher's Stone and four alchemical coal. That's 16 coal per Mobius Fuel.",
        "&eTip:&r automate coal now (Create crushing, MI quarries or a coal farm); the next steps need a lot."]),
    Q("pe_aeternalis", 6, 2, [item(PE + "aeternalis_fuel", 8)], "Aeternalis Fuel", deps=["pe_mobius"], xp=100,
      subtitle="Four Mobius fuel, compressed", desc=[
        "&eWhat:&r the top fuel, and the main ingredient of Dark Matter.",
        "&eHow:&r the Philosopher's Stone and four Mobius Fuel. Each one is 64 coal; this quest asks for eight (512 coal).",
        "&eTip:&r packaged autocrafting (PackagedAuto or AE2) can do the whole chain while you build."]),
    Q("pe_dm", 8, 2, [item(PE + "dark_matter")], "Dark Matter", deps=["pe_aeternalis"], xp=250,
      size=1.5, shape="gear", subtitle="Eight Aeternalis around a diamond block", desc=[
        "&6You remember materials no forge could make. This one you made from coal and patience.&r",
        "&eWhat:&r Dark Matter is ProjectE's strongest crafting material: tools, armor and rings.",
        "&eHow:&r eight Aeternalis Fuel around a diamond block. The diamonds come from real mining or synthesis; EMC can't make them here.",
        "&eTip:&r four Dark Matter make a Dark Matter Block, used by the tablet and the Dark Matter Furnace."]),
    Q("pe_dm_tools", 10, 2, [anyof([PE + "dm_pick", PE + "dm_axe", PE + "dm_shovel", PE + "dm_sword", PE + "dm_hoe",
                                    PE + "dm_shears", PE + "dm_hammer"])],
      "Dark Matter Tools", deps=["pe_dm"], xp=100, subtitle="Unbreakable tools", optional=True, tokens=1, desc=[
        "&eWhat:&r Dark Matter tools never break and dig very fast. Their charge key widens what they mine.",
        "&eHow:&r like diamond tools, but Dark Matter replaces the head and diamonds the handle (the pickaxe is 3 Dark Matter and 2 diamonds).",
        "&eTip:&r charge the Dark Matter Hammer to mine a wider area: great for clearing land."]),
    Q("pe_dm_armor", 12, 2, [item(PE + "dm_helmet"), item(PE + "dm_chestplate"), item(PE + "dm_leggings"), item(PE + "dm_boots")],
      "Dark Matter Armor", deps=["pe_dm"], xp=300, optional=True, tokens=2,
      subtitle="Optional: a full set of 24 Dark Matter", desc=[
        "&eWhat:&r very strong armor that doesn't wear out.",
        "&eHow:&r shaped like diamond armor, all Dark Matter: helmet 5, chestplate 8, leggings 7, boots 4.",
        "&eTip:&r that's 24 Dark Matter. Automate the fuel chain first."]),
    Q("pe_bhb", 12, 3.5, [item(PE + "black_hole_band")], "Black Hole Band", deps=["pe_dm"], xp=100,
      optional=True, tokens=1, subtitle="Optional: pulls in every item nearby", desc=[
        "&eWhat:&r while active, it draws nearby items toward you.",
        "&eHow:&r an Iron Band (eight iron around a lava bucket) between two Dark Matter, with string above and below.",
        "&eTip:&r switch it off near your storage system."]),
    Q("pe_rm", 10, 3.5, [item(PE + "red_matter")], "Red Matter", deps=["pe_dm"], xp=300,
      optional=True, tokens=2, subtitle="Optional: beyond Dark Matter", desc=[
        "&eWhat:&r the strongest ProjectE material, for Red Matter tools and armor.",
        "&eHow:&r three Dark Matter in the middle row with three Aeternalis Fuel above and three below.",
        "&eTip:&r each one is three Dark Matter plus 384 coal of fuel. Only for the truly committed."]),
    Q("pe_nova", 4, 3.5, [item(PE + "nova_catalyst")], "Rapid Reorganisation", deps=["pe_mobius"], xp=50,
      secret=True, loot="secret", subtitle="Secret: TNT with ambitions", desc=[
        "&6You remember reshaping mountains. The quick way was never the tidy way.&r",
        "&eWhat:&r a Nova Catalyst: TNT and Mobius Fuel. A much bigger blast.",
        "&eChemistry:&r TNT is trinitrotoluene, C₇H₅N₃O₆. It carries its own oxygen, which is why it burns so fast.",
        "&eTip:&r never near your base. Ever."]),
], links=[("t6_table", -2, 0)])
