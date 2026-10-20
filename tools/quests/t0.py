"""Quest chapter: t0. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

CHAPTER = Chapter("t0", "I. Fire and Bronze", "modern_industrialization:bronze_ingot",
        ["Heat drives chemistry: reduce ore with carbon, mix metals into alloys, and let steam do the work."], MAIN, [
    # --- raw materials --------------------------------------------------------------------
    Q("t0_charcoal", 0, -1, [item("minecraft:charcoal", 8)], "Pyrolysis", subtitle="Wood, heat, and no air", deps=["gs_ready"], xp=25, desc=[
        "&6You remember the first fire you ever tamed. It was smaller than this, and it frightened you more.&r",
        "&eWhat:&r &eCharcoal&r is almost pure carbon: fuel, and the reducing agent that turns ore into metal.",
        "&eChemistry:&r Heat wood without enough oxygen to burn and the volatile compounds escape as smoke, tar, methanol and acetic acid. What's left is carbon. This is &epyrolysis&r.",
        "&eHow:&r Smelt logs in a furnace.",
        "&eTip:&r A tree farm now saves hours later. Charcoal fuels everything until you have coke."]),
    Q("t0_copper", 0, 1, [item("minecraft:copper_ingot", 16)], "Copper", subtitle="The first metal humans smelted", deps=["gs_ready"], xp=20, desc=[
        "&eWhat:&r Copper is three quarters of bronze, and MI uses it for rotors, gears and wires.",
        "&eChemistry:&r Smelting is &ereduction&r: carbon pulls oxygen away from the metal oxide and leaves metal behind, CuO + C → Cu + CO.",
        "&eHow:&r Copper ore is common near the surface, especially in dripstone caves. Smelt the raw copper."]),
    Q("t0_tin", 2, 2, [item("modern_industrialization:raw_tin", 4), item("modern_industrialization:tin_ingot", 4)], "Tin", subtitle="The other quarter of bronze", deps=["t0_copper"], xp=25, desc=[
        "&eWhat:&r Tin is soft on its own, but a little of it makes copper much harder.",
        "&eChemistry:&r Real tin comes from cassiterite, SnO₂. Carbon reduces it the same way: SnO₂ + 2C → Sn + 2CO.",
        "&eHow:&r Tin ore here comes from Modern Industrialization (MI). It's grey with pale specks and fairly common underground. Mine it and smelt the raw tin."]),
    Q("t0_guide", 0, -3, [item("modern_industrialization:guidebook")], "The MI Guidebook", subtitle="Every machine and multiblock, explained", deps=["gs_ready"],
      optional=True, tokens=1, xp=15, desc=[
        "&eWhat:&r Modern Industrialization's own manual. It explains each machine and shows multiblock layouts.",
        "&eHow:&r 8 copper nuggets around a book. Break a copper ingot into nuggets first.",
        "&eTip:&r JEI (R/U) also shows multiblock shapes in 3D."]),

    # --- the forge hammer and the first alloy ---------------------------------------------
    Q("t0_hammer", 2, 0, [item("modern_industrialization:forge_hammer")], "The Forge Hammer", subtitle="Your first workstation", deps=["t0_charcoal", "t0_copper"], xp=25, desc=[
        "&eWhat:&r MI's first workstation. It crushes ore and ingots into dust and hammers ingots into plates, rods and bolts.",
        "&eHow:&r 3 heavy weighted pressure plates over 4 iron ingots. Place it and right-click to use.",
        "&eTip:&r Ores give at most &e2x&r here. Bigger yields come later from &eacids&r, not bigger hammers."]),
    Q("t0_dust", 4, 0, [item("modern_industrialization:copper_dust", 3), item("modern_industrialization:tin_dust", 1)], "Metal Dust", subtitle="Crush ingots so they can mix",
      deps=["t0_hammer", "t0_tin"], xp=20, desc=[
        "&eWhat:&r Solid ingots can't blend. Powders can.",
        "&eChemistry:&r Grinding a metal to powder gives it a huge surface area, so the two metals mix evenly when they melt together.",
        "&eHow:&r Put copper and tin ingots in the Forge Hammer: 1 ingot makes 1 dust."]),
    Q("t0_bronze_dust", 6, 0, [item("modern_industrialization:bronze_dust", 3)], "Mixing Bronze", subtitle="3 copper + 1 tin", deps=["t0_dust"], xp=25, desc=[
        "&eWhat:&r Bronze dust is the blended alloy, ready to melt into ingots.",
        "&eChemistry:&r Traditional bronze is about 88% copper and 12% tin by mass. Tin atoms jam the copper crystal so its layers can't slide, which makes it harder.",
        "&eHow:&r Craft 3 copper dust with 1 tin dust to get 3 bronze dust.",
        "&eTip:&r The Steam Mixer later turns the same inputs into 4 bronze dust instead of 3."]),
    Q("t0_bronze", 8, 0, [item("modern_industrialization:bronze_ingot", 8)], "The First Alloy", subtitle="Humanity's first engineered material",
      deps=["t0_bronze_dust"], xp=50, size=1.5, desc=[
        "&6Metal that never existed until a mind decided it should. The feeling is an old friend.&r",
        "&eWhat:&r &eBronze&r is harder than either copper or tin alone, and it's the frame of your whole steam age.",
        "&eChemistry:&r An &ealloy&r is a mixture of metals. Its properties can beat its ingredients because the mixed atoms resist being pushed out of line.",
        "&eHow:&r Smelt bronze dust in any furnace."]),
    Q("t0_plates", 10, 0, [item("modern_industrialization:bronze_plate", 4)], "Bronze Plates", subtitle="The sheet metal of the steam age", deps=["t0_bronze"], xp=25, desc=[
        "&eWhat:&r Almost every steam machine is built from plates.",
        "&eHow:&r Hammer bronze ingots in the Forge Hammer. Without a hammer tool, 2 ingots make 1 plate.",
        "&eTip:&r With an Iron Hammer in the tool slot it's 1 ingot per plate, and the Steam Compressor later does it 1:1 for free."]),
    Q("t0_parts", 12, 0, [item("modern_industrialization:bronze_rod", 2), item("modern_industrialization:bronze_bolt", 4), item("modern_industrialization:bronze_ring", 1)],
      "Rods, Bolts and Rings", subtitle="Small parts for bigger parts", deps=["t0_plates"], xp=25, desc=[
        "&eWhat:&r Gears need bolts and a ring; rings need rods and bolts.",
        "&eHow:&r In the Forge Hammer, 1 bronze ingot makes 1 rod or 2 bolts. Craft rods and bolts into rings (check JEI).",
        "&eTip:&r Make a few extra of each. Every gear takes 4 bolts and a ring."]),
    Q("t0_gear", 14, 0, [item("modern_industrialization:bronze_gear")], "Bronze Gears", subtitle="The heart of every machine casing", deps=["t0_parts"], xp=25, desc=[
        "&eWhat:&r Each machine casing needs a gear at its centre.",
        "&eHow:&r 4 bronze plates, 4 bolts and 1 ring (check JEI for the shape).",
        "&eTip:&r Make extra rings and bolts while you're at it. You'll need several casings."]),
    Q("t0_casing", 16, 0, [item("modern_industrialization:bronze_machine_casing")], "Bronze Machine Casing", subtitle="The block every steam machine is built around",
      deps=["t0_gear"], xp=40, desc=[
        "&eWhat:&r The core of every steam machine. You'll also need one for the Dissolver in Chapter II.",
        "&eHow:&r 8 bronze plates around 1 bronze gear.",
        "&eTip:&r Multiblock hatches each need a casing too. Make a few."]),

    # --- fire clay for the boiler ---------------------------------------------------------
    Q("t0_large_plate", 4, -2, [item("modern_industrialization:iron_large_plate", 5)], "Large Iron Plates", subtitle="20 iron plates, pressed in fours",
      deps=["t0_hammer"], xp=25, desc=[
        "&eWhat:&r The head of the Iron Hammer is made of large plates.",
        "&eHow:&r Hammer iron ingots into plates (2 ingots per plate), then craft 4 plates into 1 large plate. That's about 40 iron in total.",
        "&eTip:&r Ultimine an iron vein first. This is the hungriest step of the chapter."]),
    Q("t0_iron_hammer", 6, -2, [item("modern_industrialization:iron_hammer")], "The Iron Hammer", subtitle="A tool for the Forge Hammer", deps=["t0_large_plate"], xp=30, desc=[
        "&eWhat:&r Put it in the Forge Hammer's tool slot to unlock better recipes: 1 ingot per plate, and crushing bricks into dust.",
        "&eHow:&r 5 large iron plates and 2 sticks (check JEI). The tool loses durability with each use.",
        "&eTip:&r Only use the tool slot when you need it. Plain recipes don't wear it down."]),
    Q("t0_brick_dust", 8, -2, [item("modern_industrialization:brick_dust", 4)], "Brick Dust", subtitle="Crushed, already-fired clay", deps=["t0_iron_hammer"], xp=20, desc=[
        "&eWhat:&r Brick dust is half of fire clay.",
        "&eChemistry:&r Potters call crushed fired clay &egrog&r. It has already shrunk in the kiln, so mixing it into raw clay stops the new brick cracking when heated.",
        "&eHow:&r Smelt clay balls into bricks, then hammer bricks in the Forge Hammer with the Iron Hammer in the tool slot."]),
    Q("t0_fire_clay", 10, -2, [item("modern_industrialization:fire_clay_dust", 6)], "Fire Clay", subtitle="Clay that survives the furnace", deps=["t0_brick_dust"], xp=20, desc=[
        "&eWhat:&r Fire clay is a &erefractory&r: a material that stays solid at temperatures that would ruin ordinary brick.",
        "&eChemistry:&r Refractory clays are rich in alumina (Al₂O₃) and silica (SiO₂), which melt far above a fire's temperature.",
        "&eHow:&r Craft 2 clay balls with 2 brick dust to make 3 fire clay dust."]),
    Q("t0_fire_brick", 13, -2, [item("modern_industrialization:fire_clay_brick", 4)], "Fire Clay Bricks", subtitle="Fired once, hard forever", deps=["t0_fire_clay"], xp=20, desc=[
        "&eWhat:&r Single fire bricks, ready to stack into blocks.",
        "&eChemistry:&r Firing drives the bound water out of clay minerals and fuses the grains together. That change can't be undone.",
        "&eHow:&r Smelt fire clay dust in a furnace."]),
    Q("t0_fire_bricks", 16, -2, [item("modern_industrialization:fire_clay_bricks", 3)], "Firebrick Blocks", subtitle="The boiler's firebox", deps=["t0_fire_brick"], xp=25, desc=[
        "&eWhat:&r The bronze boiler sits on a row of 3 fire clay brick blocks.",
        "&eHow:&r 4 fire clay bricks in a 2x2 make 1 block.",
        "&eTip:&r Chapter II's Steam Blast Furnace is built from dozens of these. Start stockpiling clay."]),
    Q("t0_tank", 16, 2, [item("modern_industrialization:bronze_tank")], "Bronze Tank", subtitle="Holds the boiler's water", deps=["t0_casing"], xp=20, desc=[
        "&eWhat:&r A bronze tank stores fluid, and the boiler needs one to hold its water.",
        "&eChemistry:&r Bronze resists corrosion from water, which is why it was used for ship fittings for centuries.",
        "&eHow:&r 8 bronze plates around 1 glass block."]),

    # --- steam ----------------------------------------------------------------------------
    Q("t0_boiler", 18, 0, [item("modern_industrialization:bronze_boiler")], "Steam Power", subtitle="Fire boils water, steam does work",
      deps=["t0_casing", "t0_fire_bricks", "t0_tank"], xp=75, size=1.5,
      items=[("minecraft:charcoal", 32), ("modern_industrialization:bronze_furnace", 1)], desc=[
        "&6The engines remember you even if the world doesn't. Pressure, heat, motion: old friends.&r",
        "&eWhat:&r Burn fuel, boil water, and the expanding steam does work. Welcome to the industrial revolution.",
        "&eChemistry:&r Water expands more than 1,600 times in volume when it boils into steam. That pressure is what drives the machines.",
        "&eHow:&r Craft it from bronze plates, a bronze tank, a furnace and 3 fire clay brick blocks. Give it water and fuel (coal or charcoal), and place steam machines next to it.",
        "&eTip:&r Steam flows into adjacent machines, or through MI fluid pipes once you have them."]),
    Q("t0_furnace", 20, -2, [item("modern_industrialization:bronze_furnace")], "Steam Furnace", subtitle="Smelting without fuel", deps=["t0_boiler"], xp=30, desc=[
        "&eWhat:&r Smelts with steam instead of fuel. Your first automated machine.",
        "&eHow:&r Place it touching the boiler, or pipe steam to it later.",
        "&eTip:&r It smelts the same things as a vanilla furnace, so dust and raw ore can go straight in."]),
    Q("t0_macerator", 20, -1, [item("modern_industrialization:bronze_macerator")], "Steam Macerator", subtitle="Ore and ingots into dust", deps=["t0_boiler"], xp=30, desc=[
        "&eWhat:&r Grinds ore and items into dust without wearing out a tool.",
        "&eHow:&r 1 ore makes 2 raw ore here (capped at 2x until acids).",
        "&eTip:&r It also grinds bricks into brick dust, so your Iron Hammer can rest."]),
    Q("t0_compressor", 20, 0, [item("modern_industrialization:bronze_compressor")], "Steam Compressor", subtitle="Plates at 1 ingot each", deps=["t0_boiler"], xp=30, desc=[
        "&eWhat:&r Presses ingots into plates 1:1, and plates into curved plates.",
        "&eHow:&r Place it touching the boiler and put ingots in. Curved plates come from plates you put back in.",
        "&eTip:&r Machines need lots of plates. Keep this one fed."]),
    Q("t0_mixer", 20, 1, [item("modern_industrialization:bronze_mixer")], "Steam Mixer", subtitle="Better alloy ratios", deps=["t0_boiler"], xp=30, desc=[
        "&eWhat:&r Mixes dusts (like copper and tin into bronze) and fluids.",
        "&eChemistry:&r Same copper and tin, less loss: a good process wastes less of its inputs. That's called &eyield&r.",
        "&eHow:&r 3 copper dust + 1 tin dust makes 4 bronze dust here, one more than by hand."]),
    Q("t0_cutter", 20, 2, [item("modern_industrialization:bronze_cutting_machine")], "Steam Cutting Machine", subtitle="Rods, bolts and planks", deps=["t0_boiler"], xp=30, desc=[
        "&eWhat:&r Cuts ingots into 2 rods, rods into bolts, and logs into 6 planks.",
        "&eHow:&r It needs &elubricant&r as a cutting fluid. You'll make lubricant from creosote and redstone in Chapter II, so build it now and run it then.",
        "&eTip:&r Until then, the Forge Hammer makes rods and bolts."]),
    Q("t0_curved", 22, -1, [item("modern_industrialization:bronze_curved_plate", 6)], "Curved Plates", subtitle="The walls of a pipe",
      deps=["t0_furnace", "t0_macerator", "t0_compressor"], xp=25, desc=[
        "&eWhat:&r Pipes are made from curved bronze plates.",
        "&eHow:&r Put bronze plates in the Steam Compressor, or hammer 2 ingots into 1 curved plate.",
        "&eTip:&r You need 6 per batch of 16 pipes. Make 12 to have pipes to spare."]),
    Q("t0_rotor", 22, 1, [item("modern_industrialization:copper_rotor", 2)], "Copper Rotors", subtitle="Blades, a ring and bolts",
      deps=["t0_compressor", "t0_mixer", "t0_cutter"], xp=30, desc=[
        "&eWhat:&r Rotors push fluid through pipes and pumps.",
        "&eHow:&r 4 copper blades, 1 copper ring and 4 copper bolts. Blades are curved copper plates on a copper rod (check JEI).",
        "&eTip:&r Every part comes from the Forge Hammer or the Steam Compressor."]),
    Q("t0_pipes", 24, 0, [item("modern_industrialization:fluid_pipe", 8)], "Fluid Pipes", subtitle="Carry water and steam anywhere", deps=["t0_curved", "t0_rotor"], xp=50, desc=[
        "&eWhat:&r MI fluid pipes carry water, steam and later every chemical in the pack.",
        "&eHow:&r 6 bronze curved plates, 2 copper rotors and a glass pane make 16 pipes.",
        "&eTip:&r Right-click a pipe end with an empty hand to set it to insert or extract. Item pipes need steel gears, so they wait for Chapter II."]),
    Q("t0_pump", 26, 0, [item("modern_industrialization:bronze_water_pump")], "Endless Water", subtitle="A boiler that never runs dry", deps=["t0_pipes"], xp=40, desc=[
        "&6Fire, water, metal, motion. The pieces of a world are coming back to you.&r",
        "&eWhat:&r A steam-powered pump that pulls water from the ground, so your boiler never runs dry.",
        "&eHow:&r Copper rotors, copper gears, a bronze tank, a machine casing and fluid pipes (check JEI). Place it next to the boiler, or pipe its water into it.",
        "&eTip:&r The Coke Oven in Chapter II runs on steam, so a boiler that never runs dry comes first. Next stop: coke and steel."]),

    # --- optional side quests -------------------------------------------------------------
    Q("t0_opt_block", 6, 3, [item("modern_industrialization:bronze_block", 4)], "Bronze Age Hoard", subtitle="Four blocks of bronze",
      deps=["t0_bronze"], optional=True, tokens=1, xp=20, desc=[
        "&eWhat:&r 36 ingots of bronze, stored as blocks.",
        "&eChemistry:&r Bronze resists corrosion: its surface forms a thin layer of copper compounds that protects the metal underneath. Bronze statues can last thousands of years.",
        "&eHow:&r 9 bronze ingots make 1 block."]),
    Q("t0_opt_paxel", 8, 3, [item("mekanismtools:bronze_paxel")], "Bronze Paxel", subtitle="Your alloy, as a tool", deps=["t0_bronze"], optional=True, tokens=1, xp=20, desc=[
        "&eWhat:&r Mekanism Tools makes paxels from bronze too.",
        "&eChemistry:&r Ancient bronze tools replaced stone ones because bronze can be cast, sharpened and repaired. Stone can only be chipped.",
        "&eHow:&r Craft a bronze pickaxe, axe and shovel, then combine them with 2 sticks."]),
    Q("t0_opt_wrench", 10, 3, [item("modern_industrialization:wrench")], "The Wrench", subtitle="Handle MI machines with care", deps=["t0_plates"], optional=True, tokens=1, xp=20, desc=[
        "&eWhat:&r MI's wrench rotates MI machines, sets which face they output from, and picks them up quickly.",
        "&eHow:&r 5 bronze plates in a wrench shape (check JEI).",
        "&eTip:&r Handy when you rearrange your steam setup for the Coke Oven in Chapter II. Held near a multiblock controller, it also highlights where hatches can go."]),
    Q("t0_opt_drill", 12, 3, [item("modern_industrialization:steam_mining_drill")], "Steam Mining Drill", subtitle="A drill that burns fuel", deps=["t0_parts"],
      optional=True, tokens=2, xp=40, desc=[
        "&eWhat:&r A fuel-burning mining tool that digs a 3x3 area and can give an easy Silk Touch.",
        "&eHow:&r Furnaces, diamonds, large iron plates, a copper drill head and a bucket (check JEI). Read its tooltip for fuel and mode controls.",
        "&eTip:&r Diamonds are the hard part. Mine deep, around Y -59."]),
    Q("t0_opt_mixer", 22, 3, [item("modern_industrialization:bronze_dust", 32)], "Efficient Alloying", subtitle="Let the mixer earn its keep", deps=["t0_mixer"],
      optional=True, tokens=1, xp=20, desc=[
        "&eWhat:&r Mix 32 bronze dust in the Steam Mixer.",
        "&eChemistry:&r In real metallurgy, alloy ratios are measured by mass or by number of atoms. Getting the ratio right matters more than the amount.",
        "&eTip:&r Pipe the macerator's dust straight into the mixer and you'll never mix by hand again."]),
    Q("t0_opt_coal_block", 0, 0, [item("minecraft:coal_block", 4)], "Coal by the Block", subtitle="Nine coal, one block, a long burn",
      deps=["t0_boiler"], optional=True, tokens=1, xp=20, desc=[
        "&eWhat:&r A block of coal holds 9 coal and burns as long as all nine, so one block keeps a boiler going far longer between refills.",
        "&eChemistry:&r The energy is in the carbon, not the shape: packing coal tighter doesn't add heat, it just stores more of it in one slot.",
        "&eHow:&r 9 coal in a crafting grid make 1 block.",
        "&eTip:&r Feed boilers coal blocks through a hopper and you can leave them alone for a long time."]),
    Q("t0_opt_diamond_hammer", 0, 0, [item("modern_industrialization:diamond_hammer")], "The Diamond Hammer", subtitle="Same slot, a much tougher head",
      deps=["t0_iron_hammer", "t0_compressor"], optional=True, tokens=2, xp=40, desc=[
        "&eWhat:&r A more durable hammer for the Forge Hammer's tool slot. It does the same jobs as the Iron Hammer and wears out far more slowly.",
        "&eChemistry:&r Diamond is carbon locked into a rigid 3D lattice, which makes it the hardest natural material. Iron bends; diamond doesn't.",
        "&eHow:&r The Steam Compressor presses 1 diamond into 1 diamond plate; 4 plates make a large plate. Then 5 large plates and 2 sticks, in the Iron Hammer's shape.",
        "&eTip:&r That's 20 diamonds. Ore yields stay capped at 2x either way, so build it only if you're tired of crafting Iron Hammers."]),
])
