"""Quest chapter: t0. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, anyof, MAIN, SIDE  # noqa: F401

MI = "modern_industrialization:"

# Sections follow the real MI recipe chain: hammer -> bronze -> bronze parts and firebrick -> boiler,
# copper parts -> pipes -> the four steam machines (every one of them except the furnace needs fluid pipes).
S_ORE, S_ALLOY, S_BRONZE, S_FIRE = "Charcoal and Ore", "The First Alloy", "Bronze Parts", "Firebrick"
S_COPPER, S_STEAM, S_MACHINES = "Copper Parts", "Raising Steam", "Steam Machines"

CHAPTER = Chapter("t0", "I. Fire and Bronze", "modern_industrialization:bronze_ingot",
        ["Heat drives chemistry: reduce ore with carbon, mix metals into alloys, and let steam do the work."], MAIN, [
    # --- charcoal and ore -------------------------------------------------------------------
    Q("t0_charcoal", 0, -1, [item("minecraft:charcoal", 8)], "Pyrolysis", subtitle="Wood, heat, and no air", section=S_ORE, deps=["gs_ready"], xp=25, desc=[
        "&6You remember the first fire you ever tamed. It was smaller than this, and it frightened you more.&r",
        "&eWhat:&r &eCharcoal&r is almost pure carbon: fuel, and the reducing agent that turns ore into metal.",
        "&eChemistry:&r Heat wood without enough oxygen to burn and the volatile compounds escape as smoke, tar, methanol and acetic acid. What's left is carbon. This is &epyrolysis&r.",
        "&eHow:&r Smelt logs in a furnace.",
        "&eTip:&r A tree farm now saves hours later. Charcoal fuels everything until you have coke."]),
    Q("t0_copper", 0, 1, [item("minecraft:copper_ingot", 16)], "Copper", subtitle="The first metal humans smelted", section=S_ORE, deps=["gs_ready"], xp=20, desc=[
        "&eWhat:&r Copper is three quarters of bronze, and MI uses it for rotors, gears and wires.",
        "&eChemistry:&r Smelting is &ereduction&r: carbon pulls oxygen away from the metal oxide and leaves metal behind, CuO + C → Cu + CO.",
        "&eHow:&r Copper ore is common near the surface, especially in dripstone caves. Smelt the raw copper.",
        "&eTip:&r You'll need far more than sixteen: this chapter's pipes, rotors and gears are mostly copper."]),
    Q("t0_tin", 2, 2, [item(MI + "raw_tin", 4), item(MI + "tin_ingot", 4)], "Tin", subtitle="The other quarter of bronze", section=S_ORE, deps=["t0_copper"], xp=25, desc=[
        "&eWhat:&r Tin is soft on its own, but a little of it makes copper much harder.",
        "&eChemistry:&r Real tin comes from cassiterite, SnO₂. Carbon reduces it the same way: SnO₂ + 2C → Sn + 2CO.",
        "&eHow:&r Tin ore here comes from Modern Industrialization (MI). It's grey with pale specks and fairly common underground. Mine it and smelt the raw tin."]),
    Q("t0_guide", 0, -3, [item(MI + "guidebook")], "The MI Guidebook", subtitle="Every machine and multiblock, explained", section=S_ORE, deps=["gs_ready"],
      optional=True, tokens=1, xp=15, desc=[
        "&eWhat:&r Modern Industrialization's own manual. It explains each machine and shows multiblock layouts.",
        "&eHow:&r 8 copper nuggets around a book. Break a copper ingot into nuggets first.",
        "&eTip:&r JEI (R/U) also shows multiblock shapes in 3D."]),
    Q("t0_pressure_plates", 0, 0, [item("minecraft:heavy_weighted_pressure_plate", 3)], "Heavy Iron Plates", subtitle="The striking face of the Forge Hammer",
      section=S_ORE, deps=["gs_ready"], xp=15, desc=[
        "&eWhat:&r The Forge Hammer's head is three heavy weighted pressure plates.",
        "&eChemistry:&r Iron is dense (7.9 g/cm³), so a slab of it carries a lot of momentum into each blow. That's all a hammer is.",
        "&eHow:&r 2 iron ingots side by side make 1 heavy weighted pressure plate. You need 3, plus 4 more ingots for the base."]),

    # --- the forge hammer and the first alloy ---------------------------------------------
    Q("t0_hammer", 2, 0, [item(MI + "forge_hammer")], "The Forge Hammer", subtitle="Your first workstation", section=S_ORE,
      deps=["t0_charcoal", "t0_pressure_plates"], xp=25, desc=[
        "&eWhat:&r MI's first workstation. It crushes ore and ingots into dust and hammers ingots into plates, rods and bolts.",
        "&eHow:&r 3 heavy weighted pressure plates over 4 iron ingots. Place it and right-click to use.",
        "&eTip:&r Ores give at most &e2x&r here. Bigger yields come later from &eacids&r, not bigger hammers. Make a spare: the Steam Compressor uses one up."]),
    Q("t0_dust", 4, 0, [item(MI + "copper_dust", 3), item(MI + "tin_dust", 1)], "Metal Dust", subtitle="Crush ingots so they can mix", section=S_ALLOY,
      deps=["t0_hammer", "t0_tin"], xp=20, desc=[
        "&eWhat:&r Solid ingots can't blend. Powders can.",
        "&eChemistry:&r Grinding a metal to powder gives it a huge surface area, so the two metals mix evenly when they melt together.",
        "&eHow:&r Put copper and tin ingots in the Forge Hammer: 1 ingot makes 1 dust."]),
    Q("t0_bronze_dust", 6, 0, [item(MI + "bronze_dust", 3)], "Mixing Bronze", subtitle="3 copper + 1 tin", section=S_ALLOY, deps=["t0_dust"], xp=25, desc=[
        "&eWhat:&r Bronze dust is the blended alloy, ready to melt into ingots.",
        "&eChemistry:&r Traditional bronze is about 88% copper and 12% tin by mass. Tin atoms jam the copper crystal so its layers can't slide, which makes it harder.",
        "&eHow:&r Craft 3 copper dust with 1 tin dust to get 3 bronze dust.",
        "&eTip:&r The Steam Mixer later turns the same inputs into 4 bronze dust instead of 3."]),
    Q("t0_bronze", 8, 0, [item(MI + "bronze_ingot", 8)], "The First Alloy", subtitle="Humanity's first engineered material", section=S_ALLOY,
      deps=["t0_bronze_dust"], xp=50, size=1.5, desc=[
        "&6Metal that never existed until a mind decided it should. The feeling is an old friend.&r",
        "&eWhat:&r &eBronze&r is harder than either copper or tin alone, and it's the frame of your whole steam age.",
        "&eChemistry:&r An &ealloy&r is a mixture of metals. Its properties can beat its ingredients because the mixed atoms resist being pushed out of line.",
        "&eHow:&r Smelt bronze dust in any furnace.",
        "&eTip:&r The boiler, casings and machines ahead eat about sixty ingots. Keep the copper and tin coming."]),
    Q("t0_opt_block", 6, 3, [item(MI + "bronze_block", 4)], "Bronze Age Hoard", subtitle="Four blocks of bronze", section=S_ALLOY,
      deps=["t0_bronze"], optional=True, tokens=1, xp=20, desc=[
        "&eWhat:&r 36 ingots of bronze, stored as blocks.",
        "&eChemistry:&r Bronze resists corrosion: its surface forms a thin layer of copper compounds that protects the metal underneath. Bronze statues can last thousands of years.",
        "&eHow:&r 9 bronze ingots make 1 block."]),
    Q("t0_opt_paxel", 8, 3, [item("mekanismtools:bronze_paxel")], "Bronze Paxel", subtitle="Your alloy, as a tool", section=S_ALLOY, deps=["t0_bronze"],
      optional=True, tokens=1, xp=20, desc=[
        "&eWhat:&r Mekanism Tools makes paxels from bronze too.",
        "&eChemistry:&r Ancient bronze tools replaced stone ones because bronze can be cast, sharpened and repaired. Stone can only be chipped.",
        "&eHow:&r Craft a bronze pickaxe, axe and shovel, then combine them with 2 sticks."]),
    Q("t0_opt_armor", 0, 0, [item("mekanismtools:bronze_helmet"), item("mekanismtools:bronze_chestplate"), item("mekanismtools:bronze_leggings"),
                             item("mekanismtools:bronze_boots")], "Bronze Armour", subtitle="Better than iron, and you made the metal",
      section=S_ALLOY, deps=["t0_bronze"], optional=True, tokens=1, xp=25, desc=[
        "&eWhat:&r A full set of Mekanism Tools bronze armour: a little tougher than iron.",
        "&eChemistry:&r Bronze Age armies wore bronze plate and scale. It was heavy, but a cast and hammered tin-bronze plate turned blades that would cut leather.",
        "&eHow:&r The usual armour shapes, in bronze ingots: 24 ingots for the set."]),

    # --- bronze parts ---------------------------------------------------------------------
    Q("t0_plates", 10, 0, [item(MI + "bronze_plate", 4)], "Bronze Plates", subtitle="The sheet metal of the steam age", section=S_BRONZE, deps=["t0_bronze"], xp=25, desc=[
        "&eWhat:&r Almost every steam machine is built from plates.",
        "&eHow:&r Hammer bronze ingots in the Forge Hammer. Without a hammer tool, 2 ingots make 1 plate.",
        "&eTip:&r With an Iron Hammer in the tool slot it's 1 ingot per plate, and the Steam Compressor later does it 1:1 for free."]),
    Q("t0_parts", 12, 0, [item(MI + "bronze_rod", 2), item(MI + "bronze_bolt", 4), item(MI + "bronze_ring", 1)],
      "Rods, Bolts and Rings", subtitle="Small parts for bigger parts", section=S_BRONZE, deps=["t0_plates"], xp=25, desc=[
        "&eWhat:&r Gears need bolts and a ring; rings need rods and bolts.",
        "&eHow:&r In the Forge Hammer, 1 bronze ingot makes 1 rod, 2 bolts or 1 ring. By hand, 4 rods and 4 bolts make 2 rings (check JEI).",
        "&eTip:&r Make a few extra of each. Every gear takes 4 bolts and a ring."]),
    Q("t0_gear", 14, 0, [item(MI + "bronze_gear")], "Bronze Gears", subtitle="The heart of every machine casing", section=S_BRONZE, deps=["t0_parts"], xp=25, desc=[
        "&eWhat:&r Each machine casing needs a gear at its centre.",
        "&eHow:&r 4 bronze plates, 4 bolts and 1 ring (check JEI for the shape).",
        "&eTip:&r Make extra rings and bolts while you're at it. You'll need several casings."]),
    Q("t0_casing", 16, 0, [item(MI + "bronze_machine_casing")], "Bronze Machine Casing", subtitle="The block every steam machine is built around",
      section=S_BRONZE, deps=["t0_gear"], xp=40, desc=[
        "&eWhat:&r The core of every steam machine. You'll also need one for the Dissolver in Chapter II.",
        "&eHow:&r 8 bronze plates around 1 bronze gear.",
        "&eTip:&r The macerator, compressor, mixer, cutter and water pump each take one, and so does every multiblock hatch. Make a few."]),
    Q("t0_glass", 0, 0, [item("minecraft:glass", 8), item("minecraft:glass_pane", 2)], "Glass", subtitle="Windows for tanks, pipes and mixers", section=S_BRONZE,
      deps=["t0_charcoal"], xp=15, desc=[
        "&eWhat:&r Tanks have a glass core, every batch of fluid pipes needs a pane, and the mixer and cutter have glass windows.",
        "&eChemistry:&r Sand is mostly silica, SiO₂. Melt it and cool it quickly and the atoms freeze in a jumble instead of a crystal: that's &eglass&r, a solid with the structure of a liquid.",
        "&eHow:&r Smelt sand. 6 glass blocks make 16 panes."]),
    Q("t0_tank", 16, 2, [item(MI + "bronze_tank")], "Bronze Tank", subtitle="Holds the boiler's water", section=S_BRONZE, deps=["t0_plates", "t0_glass"], xp=20, desc=[
        "&eWhat:&r A bronze tank stores 4 buckets of fluid, and the boiler and water pump each need one.",
        "&eChemistry:&r Bronze resists corrosion from water, which is why it was used for ship fittings for centuries.",
        "&eHow:&r 8 bronze plates around 1 glass block."]),
    Q("t0_opt_wrench", 10, 3, [item(MI + "wrench")], "The Wrench", subtitle="Handle MI machines with care", section=S_BRONZE, deps=["t0_plates"],
      optional=True, tokens=1, xp=20, desc=[
        "&eWhat:&r MI's wrench rotates MI machines, sets which face they output from, and picks them up quickly.",
        "&eHow:&r 5 bronze plates in a wrench shape (check JEI).",
        "&eTip:&r Handy when you rearrange your steam setup for the Coke Oven in Chapter II. Held near a multiblock controller, it also highlights where hatches can go."]),
    Q("t0_opt_barrel", 0, 0, [item(MI + "bronze_barrel")], "Bronze Barrel", subtitle="32 stacks of one item", section=S_BRONZE, deps=["t0_plates"],
      optional=True, tokens=1, xp=20, desc=[
        "&eWhat:&r A barrel that holds 32 stacks of a single item and keeps them when broken.",
        "&eHow:&r 8 bronze plates around a wooden barrel. Right-click to put a stack in, left-click to take one out.",
        "&eTip:&r One barrel of cobblestone or charcoal clears a lot of chest space."]),

    # --- firebrick for the boiler ---------------------------------------------------------
    Q("t0_iron_plate", 0, 0, [item(MI + "iron_plate", 8)], "Iron Plates", subtitle="Two ingots, one plate", section=S_FIRE, deps=["t0_hammer"], xp=20, desc=[
        "&eWhat:&r Iron plates are the first step to the Iron Hammer, the tool that unlocks brick dust.",
        "&eChemistry:&r Hammering metal flat squeezes its crystal grains and tangles their defects, so the plate ends up harder than the ingot. Smiths call it &ework hardening&r.",
        "&eHow:&r In the Forge Hammer, 2 iron ingots make 1 plate (1:1 once you have the Iron Hammer)."]),
    Q("t0_large_plate", 4, -2, [item(MI + "iron_large_plate", 5)], "Large Iron Plates", subtitle="20 iron plates, pressed in fours", section=S_FIRE,
      deps=["t0_iron_plate"], xp=25, desc=[
        "&eWhat:&r The head of the Iron Hammer is made of large plates.",
        "&eHow:&r Craft 4 iron plates in a 2x2 into 1 large plate. That's about 40 iron in total.",
        "&eTip:&r Ultimine an iron vein first. This is the hungriest step of the chapter."]),
    Q("t0_iron_hammer", 6, -2, [item(MI + "iron_hammer")], "The Iron Hammer", subtitle="A tool for the Forge Hammer", section=S_FIRE, deps=["t0_large_plate"], xp=30, desc=[
        "&eWhat:&r Put it in the Forge Hammer's tool slot to unlock better recipes: 1 ingot per plate, and crushing bricks into dust.",
        "&eHow:&r 5 large iron plates and 2 sticks (check JEI). The tool loses durability with each use.",
        "&eTip:&r Only use the tool slot when you need it. Plain recipes don't wear it down."]),
    Q("t0_clay", 0, 0, [item("minecraft:clay_ball", 16)], "Clay", subtitle="Wet earth that remembers its shape", section=S_FIRE, deps=["gs_ready"], xp=15, desc=[
        "&eWhat:&r Clay goes into bricks twice: once as bricks to crush, and again raw in the fire clay mix.",
        "&eChemistry:&r Clay is weathered rock: tiny flakes of aluminosilicate minerals such as kaolinite, Al₂Si₂O₅(OH)₄. Water between the flakes is what makes it mouldable.",
        "&eHow:&r Dig clay blocks from riverbeds, lakes and swamps. Each block breaks into 4 balls.",
        "&eTip:&r The boiler alone needs 12 clay balls and the Steam Blast Furnace in Chapter II far more. Take a whole clay patch."]),
    Q("t0_brick", 0, 0, [item("minecraft:brick", 8)], "Bricks", subtitle="Clay, fired", section=S_FIRE, deps=["t0_clay"], xp=15, desc=[
        "&eWhat:&r Single bricks, the half of fire clay you crush.",
        "&eChemistry:&r Around 600 °C, clay minerals lose the water locked inside their crystals; hotter still, the grains fuse. The result is ceramic, and it can't turn back into clay.",
        "&eHow:&r Smelt clay balls in a furnace."]),
    Q("t0_brick_dust", 8, -2, [item(MI + "brick_dust", 4)], "Brick Dust", subtitle="Crushed, already-fired clay", section=S_FIRE, deps=["t0_iron_hammer", "t0_brick"], xp=20, desc=[
        "&eWhat:&r Brick dust is half of fire clay.",
        "&eChemistry:&r Potters call crushed fired clay &egrog&r. It has already shrunk in the kiln, so mixing it into raw clay stops the new brick cracking when heated.",
        "&eHow:&r Hammer bricks in the Forge Hammer with the Iron Hammer in the tool slot: 1 brick makes 1 dust."]),
    Q("t0_fire_clay", 10, -2, [item(MI + "fire_clay_dust", 6)], "Fire Clay", subtitle="Clay that survives the furnace", section=S_FIRE, deps=["t0_brick_dust"], xp=20, desc=[
        "&eWhat:&r Fire clay is a &erefractory&r: a material that stays solid at temperatures that would ruin ordinary brick.",
        "&eChemistry:&r Refractory clays are rich in alumina (Al₂O₃) and silica (SiO₂), which melt far above a fire's temperature.",
        "&eHow:&r Craft 2 clay balls with 2 brick dust to make 3 fire clay dust."]),
    Q("t0_fire_brick", 13, -2, [item(MI + "fire_clay_brick", 4)], "Fire Clay Bricks", subtitle="Fired once, hard forever", section=S_FIRE, deps=["t0_fire_clay"], xp=20, desc=[
        "&eWhat:&r Single fire bricks, ready to stack into blocks.",
        "&eChemistry:&r Firing drives the bound water out of clay minerals and fuses the grains together. That change can't be undone.",
        "&eHow:&r Smelt fire clay dust in a furnace."]),
    Q("t0_fire_bricks", 16, -2, [item(MI + "fire_clay_bricks", 3)], "Firebrick Blocks", subtitle="The boiler's firebox", section=S_FIRE, deps=["t0_fire_brick"], xp=25, desc=[
        "&eWhat:&r The bronze boiler sits on a row of 3 fire clay brick blocks, and the Steam Furnace on 3 more.",
        "&eHow:&r 4 fire clay bricks in a 2x2 make 1 block.",
        "&eTip:&r Chapter II's Steam Blast Furnace is built from dozens of these. Start stockpiling clay."]),
    Q("t0_opt_diamond_hammer", 0, 0, [item(MI + "diamond_hammer")], "The Diamond Hammer", subtitle="Same slot, a much tougher head", section=S_FIRE,
      deps=["t0_iron_hammer", "t0_compressor"], optional=True, tokens=2, xp=40, desc=[
        "&eWhat:&r A more durable hammer for the Forge Hammer's tool slot. It does the same jobs as the Iron Hammer and wears out far more slowly.",
        "&eChemistry:&r Diamond is carbon locked into a rigid 3D lattice, which makes it the hardest natural material. Iron bends; diamond doesn't.",
        "&eHow:&r The Steam Compressor presses 1 diamond into 1 diamond plate; 4 plates make a large plate. Then 5 large plates and 2 sticks, in the Iron Hammer's shape.",
        "&eTip:&r That's 20 diamonds. Ore yields stay capped at 2x either way, so build it only if you're tired of crafting Iron Hammers."]),
    Q("t0_opt_fireclay_mixer", 0, 0, [item(MI + "fire_clay_dust", 32)], "Fire Clay in Bulk", subtitle="The mixer's better ratio", section=S_FIRE,
      deps=["t0_mixer", "t0_fire_clay"], optional=True, tokens=1, xp=20, desc=[
        "&eWhat:&r Stockpile fire clay for the Steam Blast Furnace in Chapter II.",
        "&eChemistry:&r The same 2 clay + 2 brick dust gives 4 fire clay in the Steam Mixer instead of 3 by hand. Better mixing, better &eyield&r.",
        "&eTip:&r The Steam Macerator grinds bricks and brick blocks into dust too (4 dust per block), so the Iron Hammer can rest."]),

    # --- copper parts ---------------------------------------------------------------------
    Q("t0_copper_plate", 0, 0, [item(MI + "copper_plate", 6)], "Copper Plates", subtitle="Sheet copper for gears and blades", section=S_COPPER,
      deps=["t0_hammer", "t0_copper"], xp=20, desc=[
        "&eWhat:&r Copper gears and curved plates start as flat plates.",
        "&eChemistry:&r Copper is one of the most &emalleable&r metals: its atoms sit in a close-packed lattice whose layers slide over each other without breaking apart.",
        "&eHow:&r In the Forge Hammer, 2 copper ingots make 1 plate (1:1 with the Iron Hammer in the tool slot)."]),
    Q("t0_copper_curved", 0, 0, [item(MI + "copper_curved_plate", 4)], "Curved Copper", subtitle="The cupped face of a blade", section=S_COPPER,
      deps=["t0_copper_plate"], xp=20, desc=[
        "&eWhat:&r Rotor blades are curved copper plates on a copper rod.",
        "&eHow:&r Hammer 2 copper ingots into 1 curved plate, or 1 plate into 1 curved plate with the Iron Hammer in the tool slot.",
        "&eTip:&r Two rotors need 8 blades, and 2 curved plates and a rod make 4 blades."]),
    Q("t0_copper_rod", 0, 0, [item(MI + "copper_rod", 4), item(MI + "copper_bolt", 8)], "Copper Rods and Bolts", subtitle="Spines and fasteners",
      section=S_COPPER, deps=["t0_hammer", "t0_copper"], xp=20, desc=[
        "&eWhat:&r Rods hold blades, bolts hold rotors and gears together, and the Steam Compressor needs 2 rods of its own.",
        "&eHow:&r In the Forge Hammer, 1 copper ingot makes 1 rod or 2 bolts.",
        "&eTip:&r The Steam Cutting Machine later doubles both. Until then, the hammer will do."]),
    Q("t0_copper_blade", 0, 0, [item(MI + "copper_blade", 8)], "Copper Blades", subtitle="Four per rotor", section=S_COPPER,
      deps=["t0_copper_curved", "t0_copper_rod"], xp=20, desc=[
        "&eWhat:&r The vanes of a rotor: they push water and steam through a pipe when the rotor turns.",
        "&eHow:&r 2 curved copper plates stacked on a copper rod make 4 blades."]),
    Q("t0_copper_ring", 0, 0, [item(MI + "copper_ring", 4)], "Copper Rings", subtitle="Hubs for rotors and gears", section=S_COPPER,
      deps=["t0_copper_rod"], xp=20, desc=[
        "&eWhat:&r Every rotor and every gear is built around a ring.",
        "&eHow:&r 4 copper rods and 4 copper bolts make 2 rings, or the Forge Hammer makes 1 ring from 1 ingot."]),
    Q("t0_copper_gear", 0, 0, [item(MI + "copper_gear", 4)], "Copper Gears", subtitle="Every steam machine runs on them", section=S_COPPER,
      deps=["t0_copper_plate", "t0_copper_ring"], xp=25, desc=[
        "&eWhat:&r The macerator, compressor, cutter and water pump each take 2 copper gears, the mixer 1.",
        "&eHow:&r 4 copper plates, 4 copper bolts and 1 copper ring, the same shape as the bronze gear.",
        "&eTip:&r That's 9 gears for the full set of machines. Build them as you need them."]),
    Q("t0_rotor", 22, 1, [item(MI + "copper_rotor", 2)], "Copper Rotors", subtitle="Blades, a ring and bolts", section=S_COPPER,
      deps=["t0_copper_blade", "t0_copper_ring"], xp=30, desc=[
        "&eWhat:&r Rotors push fluid through pipes and pumps.",
        "&eHow:&r 4 copper blades, 1 copper ring and 4 copper bolts (check JEI).",
        "&eTip:&r Fluid pipes take 2 per batch, the mixer 2 and the water pump 2. Make six."]),
    Q("t0_opt_drill_head", 0, 0, [item(MI + "copper_drill_head")], "Copper Drill Head", subtitle="The business end of a drill", section=S_COPPER,
      deps=["t0_copper_gear", "t0_copper_curved"], optional=True, tokens=1, xp=20, desc=[
        "&eWhat:&r The tip of the Steam Mining Drill.",
        "&eHow:&r A copper plate, 2 curved plates, a rod, 2 copper gears and 3 bolts (check JEI).",
        "&eTip:&r Copper is soft for a drill bit, but this one only has to turn. The drill's own power does the work."]),
    Q("t0_opt_drill", 12, 3, [item(MI + "steam_mining_drill")], "Steam Mining Drill", subtitle="A drill that burns fuel", section=S_COPPER, deps=["t0_opt_drill_head"],
      optional=True, tokens=2, xp=40, desc=[
        "&eWhat:&r A fuel-burning mining tool that digs a 3x3 area and can give an easy Silk Touch.",
        "&eHow:&r Furnaces, diamonds, large iron plates, the copper drill head and a bucket (check JEI). Fill it from a water source and feed it solid fuel.",
        "&eTip:&r Silk-touched ore goes into the Forge Hammer for 2 raw ore each."]),
    Q("t0_opt_silk_ore", 0, 0, [anyof([MI + "tin_ore", MI + "deepslate_tin_ore"], 8)], "Ore, Whole", subtitle="Silk-touched tin for the hammer", section=S_COPPER,
      deps=["t0_opt_drill"], optional=True, tokens=1, xp=20, desc=[
        "&eWhat:&r Mine 8 tin ore blocks whole with the drill's Silk Touch mode.",
        "&eChemistry:&r An ore block is mostly worthless rock (&egangue&r) around a little mineral. Crushing it first frees more of the mineral grains, which is why the Forge Hammer gets 2 raw ore from a block.",
        "&eHow:&r Switch the Steam Mining Drill to Silk Touch (see its tooltip), mine tin ore, and hammer each block into 2 raw tin."]),

    # --- raising steam --------------------------------------------------------------------
    Q("t0_boiler", 18, 0, [item(MI + "bronze_boiler")], "Steam Power", subtitle="Fire boils water, steam does work", section=S_STEAM,
      deps=["t0_tank", "t0_fire_bricks", "t0_casing"], xp=75, size=1.5,
      items=[("minecraft:charcoal", 32), (MI + "bronze_furnace", 1)], desc=[
        "&6The engines remember you even if the world doesn't. Pressure, heat, motion: old friends.&r",
        "&eWhat:&r Burn fuel, boil water, and the expanding steam does work. Welcome to the industrial revolution.",
        "&eChemistry:&r Water expands more than 1,600 times in volume when it boils into steam. That pressure is what drives the machines.",
        "&eHow:&r 4 bronze plates, a bronze tank, a furnace and 3 fire clay brick blocks. Give it water and fuel (coal or charcoal), and place steam machines next to it.",
        "&eTip:&r A hot boiler makes 8 mB of steam a tick, enough for four bronze machines at once."]),
    Q("t0_furnace", 20, -2, [item(MI + "bronze_furnace")], "Steam Furnace", subtitle="Smelting without fuel", section=S_STEAM, deps=["t0_boiler"], xp=30, desc=[
        "&eWhat:&r Smelts with steam instead of fuel. Your first automated machine, and the only one that needs no pipes.",
        "&eHow:&r 5 bronze plates, a furnace and 3 fire clay brick blocks. Place it touching the boiler.",
        "&eTip:&r It's as slow as a vanilla furnace, but steam carries heat so well that it costs about a tenth of the fuel."]),
    Q("t0_curved", 22, -1, [item(MI + "bronze_curved_plate", 6)], "Curved Plates", subtitle="The walls of a pipe", section=S_STEAM, deps=["t0_plates"], xp=25, desc=[
        "&eWhat:&r Pipes are made from curved bronze plates.",
        "&eHow:&r Hammer 2 bronze ingots into 1 curved plate in the Forge Hammer. Later the Steam Compressor bends plates into curved plates 1:1.",
        "&eTip:&r You need 6 per batch of 16 pipes. Make 12 to have pipes to spare."]),
    Q("t0_pipes", 24, 0, [item(MI + "fluid_pipe", 8)], "Fluid Pipes", subtitle="Carry water and steam anywhere", section=S_STEAM,
      deps=["t0_curved", "t0_rotor", "t0_glass"], xp=50, size=1.5, desc=[
        "&6Water that goes where you tell it. You used to do that with rivers.&r",
        "&eWhat:&r MI fluid pipes carry water, steam and later every chemical in the pack. Four of the five steam machines are built with them.",
        "&eHow:&r 6 bronze curved plates, 2 copper rotors and a glass pane make 16 pipes.",
        "&eTip:&r A pipe holds one fluid at a time. Right-click a pipe with a wrench to change its connection; item pipes need steel gears, so they wait for Chapter II."]),
    Q("t0_opt_coal_block", 0, 0, [item("minecraft:coal_block", 4)], "Coal by the Block", subtitle="Nine coal, one block, a long burn", section=S_STEAM,
      deps=["t0_boiler"], optional=True, tokens=1, xp=20, desc=[
        "&eWhat:&r A block of coal holds 9 coal and burns as long as all nine, so one block keeps a boiler going far longer between refills.",
        "&eChemistry:&r The energy is in the carbon, not the shape: packing coal tighter doesn't add heat, it just stores more of it in one slot.",
        "&eHow:&r 9 coal in a crafting grid make 1 block.",
        "&eTip:&r Feed boilers coal blocks through a hopper and you can leave them alone for a long time."]),
    Q("t0_opt_steam_bucket", 0, 0, [item(MI + "steam_bucket")], "Steam in a Bucket", subtitle="Boil a bucket of water", section=S_STEAM,
      deps=["t0_boiler"], optional=True, tokens=1, xp=15, desc=[
        "&eWhat:&r Smelt a water bucket in any furnace and you get a bucket of steam: portable power for a machine far from the boiler.",
        "&eChemistry:&r Boiling doesn't change water chemically; H₂O stays H₂O. It only gives the molecules enough energy to escape the liquid, about 2,260 joules per gram.",
        "&eTip:&r Handy for testing a machine before you've run a pipe to it."]),

    # --- steam machines -------------------------------------------------------------------
    Q("t0_diamond", 0, 0, [item("minecraft:diamond", 3)], "Diamonds for Grinding", subtitle="The teeth of the macerator and cutter", section=S_MACHINES,
      deps=["gs_ready"], xp=30, desc=[
        "&eWhat:&r The Steam Macerator grinds with 2 diamonds and the Steam Cutting Machine cuts with 1.",
        "&eChemistry:&r Diamond is the hardest natural material, so it grinds and cuts everything softer than itself. Real industrial saws and grinders are tipped with diamond grit for the same reason.",
        "&eHow:&r Diamond ore is most common near the bottom of the world, around Y -59. An iron pickaxe mines it.",
        "&eTip:&r A Fortune pickaxe helps a lot here."]),
    Q("t0_macerator", 20, -1, [item(MI + "bronze_macerator")], "Steam Macerator", subtitle="Ore and ingots into dust", section=S_MACHINES,
      deps=["t0_pipes", "t0_copper_gear", "t0_diamond"], xp=30, desc=[
        "&eWhat:&r Grinds ore and items into dust without wearing out a tool.",
        "&eHow:&r 2 diamonds, 2 copper gears, a bronze machine casing and 3 fluid pipes. Ores give at most 2x until acids.",
        "&eTip:&r It also grinds bricks into brick dust, so your Iron Hammer can rest."]),
    Q("t0_compressor", 20, 0, [item(MI + "bronze_compressor")], "Steam Compressor", subtitle="Plates at 1 ingot each", section=S_MACHINES,
      deps=["t0_pipes", "t0_copper_gear"], xp=30, desc=[
        "&eWhat:&r Presses ingots into plates 1:1, and plates into curved plates.",
        "&eHow:&r A Forge Hammer, 2 copper rods, 2 copper gears, a bronze machine casing and 3 fluid pipes. The Forge Hammer goes into the recipe, so craft a second one.",
        "&eTip:&r Machines need lots of plates. Keep this one fed."]),
    Q("t0_mixer", 20, 1, [item(MI + "bronze_mixer")], "Steam Mixer", subtitle="Better alloy ratios", section=S_MACHINES, deps=["t0_pipes", "t0_copper_gear"], xp=30, desc=[
        "&eWhat:&r Mixes dusts (like copper and tin into bronze) and fluids.",
        "&eChemistry:&r Same copper and tin, less loss: a good process wastes less of its inputs. That's called &eyield&r.",
        "&eHow:&r 2 glass, a copper gear, 2 copper rotors, a bronze machine casing and 3 fluid pipes. Here 3 copper dust + 1 tin dust makes 4 bronze dust, one more than by hand."]),
    Q("t0_cutter", 20, 2, [item(MI + "bronze_cutting_machine")], "Steam Cutting Machine", subtitle="Rods, bolts and planks", section=S_MACHINES,
      deps=["t0_pipes", "t0_copper_gear", "t0_diamond"], xp=30, desc=[
        "&eWhat:&r Cuts ingots into 2 rods, rods into bolts, and logs into 6 planks.",
        "&eHow:&r A diamond, 2 glass, 2 copper gears, a casing and pipes. It needs &elubricant&r as a cutting fluid. You'll make lubricant from creosote and redstone in Chapter II, so build it now and run it then.",
        "&eTip:&r Until then, the Forge Hammer makes rods and bolts."]),
    Q("t0_pump", 26, 0, [item(MI + "bronze_water_pump")], "Endless Water", subtitle="A boiler that never runs dry", section=S_MACHINES,
      deps=["t0_pipes", "t0_copper_gear", "t0_tank"], xp=40, desc=[
        "&6Fire, water, metal, motion. The pieces of a world are coming back to you.&r",
        "&eWhat:&r A steam-powered pump that pulls water from the ground, so your boiler never runs dry.",
        "&eHow:&r 2 copper rotors, 2 copper gears, a bronze tank, a machine casing and 3 fluid pipes. Place it next to the boiler, or pipe its water into it.",
        "&eTip:&r The Coke Oven in Chapter II runs on steam, so a boiler that never runs dry comes first. Next stop: coke and steel."]),
    Q("t0_opt_mixer", 22, 3, [item(MI + "bronze_dust", 32)], "Efficient Alloying", subtitle="Let the mixer earn its keep", section=S_MACHINES, deps=["t0_mixer"],
      optional=True, tokens=1, xp=20, desc=[
        "&eWhat:&r Mix 32 bronze dust in the Steam Mixer.",
        "&eChemistry:&r In real metallurgy, alloy ratios are measured by mass or by number of atoms. Getting the ratio right matters more than the amount.",
        "&eTip:&r Pipe the macerator's dust straight into the mixer and you'll never mix by hand again."]),
    Q("t0_opt_plates", 0, 0, [item(MI + "bronze_plate", 64)], "Plates at Scale", subtitle="A stack from the compressor", section=S_MACHINES, deps=["t0_compressor"],
      optional=True, tokens=1, xp=20, desc=[
        "&eWhat:&r Press a full stack of bronze plates in the Steam Compressor.",
        "&eHow:&r The compressor gives 1 plate per ingot, where the bare Forge Hammer gives 1 per 2.",
        "&eTip:&r Chapter II's hatches, tanks and steel upgrades are mostly plates. A stack in a barrel saves trips."]),
])
