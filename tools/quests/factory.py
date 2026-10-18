"""Quest chapter: factory. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, kill, anyof, MAIN, SIDE  # noqa: F401

CHAPTER = Chapter("factory", "Mob Data and Big Crafting", "hostilenetworks:sim_chamber",
        ["Monifactory-inspired machinery: simulate mobs, craft on giant tables, and fold whole factories into a block."], SIDE, [
    # --- Hostile Neural Networks (y=0) ---------------------------------------------------------
    Q("mf_learner", 0, 0, [item("hostilenetworks:deep_learner"), item("hostilenetworks:blank_data_model")], "Deep Learning", deps=["gs_iron"], xp=40,
      subtitle="Teach a model by fighting", desc=[
        "&6You remember knowing every creature by name. You can learn them again, one fight at a time.&r",
        "&eWhat:&r Hostile Neural Networks records mobs into data models. Trained models later make mob drops without the mob.",
        "&eHow:&r craft the Deep Learner and a Blank Data Model (check JEI). Put models in the Deep Learner and keep it in your inventory while you fight.",
        "&eTip:&r start with a mob whose drops you'll need in bulk, like blazes, slimes or endermen."]),
    Q("mf_model", 2, 0, [item("hostilenetworks:data_model")], "Your First Model", deps=["mf_learner"], xp=40,
      subtitle="Attune a blank model to one mob", desc=[
        "&eWhat:&r a data model attuned to one mob type. It starts at Faulty and levels up as you kill that mob.",
        "&eHow:&r right-click a mob with a Blank Data Model, or craft a specific model (check JEI). Then hunt with the Deep Learner.",
        "&eTip:&r tiers go Faulty, Basic, Advanced, Superior, Self Aware. Higher tiers are more accurate, so fewer simulations fail."]),
    Q("mf_sim", 4, 0, [item("hostilenetworks:sim_chamber"), item("hostilenetworks:prediction_matrix", 4)], "Simulation", deps=["mf_model", "t4_mv"], xp=150,
      subtitle="Mob drops from power and matrices", desc=[
        "&eWhat:&r the Simulation Chamber runs a trained model on FE and prediction matrices to make predictions and mob drops.",
        "&eHow:&r it needs an &eMV electronic circuit&r (aluminum chemistry). Insert a model of Basic tier or better, matrices and power.",
        "&eTip:&r pipe matrices in and drops out; one chamber per model keeps things simple."]),
    Q("mf_fab", 6, 0, [item("hostilenetworks:loot_fabricator")], "Loot Fabricator", deps=["mf_sim"], xp=150,
      size=1.5, subtitle="Choose exactly which drop you want", desc=[
        "&6You remember making things appear from nothing. This is the mortal version: data, power and patience.&r",
        "&eWhat:&r turns predictions into the specific drop you pick (blaze rods, ender pearls, slime balls and more).",
        "&eHow:&r also needs an MV electronic circuit. Feed it predictions from the chamber and select the output in its GUI.",
        "&eTip:&r simulated blazes are a cheap blaze-rod source for Silent Gear alloys and brewing."]),
    Q("mf_self_aware", 3, -1.5, [tick()], "Self Aware", deps=["mf_sim"], xp=150,
      optional=True, tokens=2, subtitle="Optional: max out a data model", desc=[
        "&eWhat:&r train one data model all the way to Self Aware, the top tier.",
        "&eHow:&r keep killing that mob with the model in your Deep Learner, or let the Simulation Chamber train it. Click the checkmark when you've done it.",
        "&eTip:&r a Self Aware model almost never fails a simulation."]),
    Q("mf_twilight_pred", 7, -1.5, [item("hostilenetworks:twilight_prediction", 4)], "Twilight Predictions", deps=["mf_sim", "t5_twilight"], xp=100,
      optional=True, tokens=1, subtitle="Optional: simulate Twilight Forest mobs", desc=[
        "&eWhat:&r Twilight Forest mobs give their own prediction type.",
        "&eHow:&r train a model on a Twilight mob and run it in the Simulation Chamber.",
        "&eTip:&r the Loot Fabricator shows which drops each prediction can become."]),

    # --- Extended Crafting (y=2.5) -------------------------------------------------------------
    Q("mf_components", 0, 2.5, [item("extendedcrafting:black_iron_slate"), item("extendedcrafting:basic_component"), item("extendedcrafting:basic_catalyst")], "Black Iron Parts",
      deps=["t1_steel"], xp=40, subtitle="Slates, components and catalysts", desc=[
        "&eWhat:&r Extended Crafting tables are built from black iron slates plus a component and a catalyst of matching tier.",
        "&eHow:&r black iron ingot = iron ingot + black dye (shapeless). Two ingots make a slate. A component takes a slate, luminessence (glowstone, redstone, gunpowder) and iron; four components ring a black iron ingot for the catalyst.",
        "&eTip:&r make extra black iron; every table tier and the Crafting Core need more."]),
    Q("mf_basic_table", 2, 2.5, [item("extendedcrafting:black_iron_ingot", 8), item("extendedcrafting:basic_table")], "Extended Crafting", deps=["mf_components"], xp=50,
      subtitle="The 3x3 table that starts the ladder", desc=[
        "&eWhat:&r the Basic Table is a 3x3 table for Extended Crafting recipes, and the base of every bigger table.",
        "&eHow:&r black iron slate, basic component and catalyst, an iron block and a crafting table.",
        "&eTip:&r each bigger table is crafted from the one before it, so don't use this one up as decoration."]),
    Q("mf_adv_table", 4, 2.5, [item("extendedcrafting:advanced_table")], "5x5: Advanced Table", deps=["mf_basic_table", "t4_mv"], xp=100,
      subtitle="Needs an MV electronic circuit", desc=[
        "&eWhat:&r a 5x5 crafting grid for mid-game recipes.",
        "&eChemistry:&r its &eMI electronic circuit&r rests on aluminum, won by electrolysis of alumina: 2Al₂O₃ → 4Al + 3O₂.",
        "&eHow:&r the Basic Table, gold blocks, advanced component and catalyst, plus the electronic circuit (check JEI)."]),
    Q("mf_elite_table", 6, 2.5, [item("extendedcrafting:elite_table")], "7x7: Elite Table", deps=["mf_adv_table", "t5_hv"], xp=200,
      subtitle="Needs an HV digital circuit", desc=[
        "&eWhat:&r a 7x7 grid. Crystaltine and many late parts are crafted here.",
        "&eChemistry:&r the &eMI digital circuit&r needs polyethylene, chains of ethylene (C₂H₄) from cracking oil.",
        "&eHow:&r the Advanced Table, diamond blocks, elite component and catalyst, plus the digital circuit."]),
    Q("mf_ult_table", 8, 2.5, [item("extendedcrafting:ultimate_table")], "9x9: Ultimate Table", deps=["mf_elite_table", "t6_pu"], xp=400,
      size=1.5, shape="hexagon", subtitle="Needs an EV processing unit", desc=[
        "&6You remember building worlds on a table far bigger than this. Nine by nine will do for now.&r",
        "&eWhat:&r the endgame's biggest crafts happen here, including the Seed of a New World.",
        "&eChemistry:&r the &eMI processing unit&r needs PVC: polyvinyl chloride, (C₂H₃Cl)ₙ, made from ethylene and chlorine.",
        "&eHow:&r the Elite Table, emerald blocks, ultimate component and catalyst, plus the processing unit."]),
    Q("mf_packaged", 4, 4, [item("packagedauto:packager"), item("packagedauto:unpackager")], "Packaged Automation", deps=["t5_ae2", "mf_adv_table"], xp=150,
      subtitle="Let AE2 run the big tables for you", desc=[
        "&eWhat:&r Packaged Auto lets AE2 autocraft with Extended Crafting tables, through the PackagedExCrafting addon.",
        "&eHow:&r encode recipes in the Encoder, then set up a Packager, a PackagedExCrafting crafter and an Unpackager by your ME network (tooltips and JEI explain each block).",
        "&eTip:&r one setup per table size handles every recipe of that size."]),
    Q("mf_ender_crafter", 0, 4, [item("extendedcrafting:ender_crafter"), item("extendedcrafting:ender_alternator", 2)], "Ender Crafting", deps=["mf_components", "t2_nether"], xp=60,
      optional=True, tokens=1, subtitle="Optional: slow crafting, no hands needed", desc=[
        "&eWhat:&r the Ender Crafter finishes its recipes over time, faster with more Ender Alternators nearby.",
        "&eHow:&r ender ingots (iron + ender pearl), eyes of ender and a crafting table (check JEI).",
        "&eTip:&r a ring of alternators around the crafter speeds it up a lot."]),
    Q("mf_crafting_core", 7, 4, [item("extendedcrafting:crafting_core"), item("extendedcrafting:pedestal", 4)], "Combination Crafting", deps=["mf_elite_table"], xp=150,
      optional=True, tokens=1, subtitle="Optional: a core ringed by pedestals", desc=[
        "&eWhat:&r put the main item on the Crafting Core and the extras on Pedestals around it. The core uses FE to fuse them.",
        "&eHow:&r elite components and catalysts, a frame and black iron (check JEI). JEI shows every combination recipe.",
        "&eTip:&r pipe FE into the core; it won't start without power."]),
    Q("mf_crystaltine", 9, 4, [item("extendedcrafting:crystaltine_ingot", 4)], "Crystaltine", deps=["mf_elite_table"], xp=150,
      optional=True, tokens=1, subtitle="Optional: diamond, lapis and a Nether Star", desc=[
        "&eWhat:&r a late crafting metal made on the Elite Table.",
        "&eChemistry:&r lapis lazuli's blue comes from lazurite, a sodium aluminosilicate with trapped sulfur ions (S₃⁻).",
        "&eHow:&r diamonds, lapis, iron, gold and a Nether Star in a 7x4 pattern (check JEI)."]),

    # --- Compact Machines (y=6.5) --------------------------------------------------------------
    Q("mf_compact", 0, 6.5, [item("compactmachines:personal_shrinking_device")], "Compact Machines", deps=["t3_hull"], xp=75,
      subtitle="A whole factory inside one block", desc=[
        "&eWhat:&r fold an entire factory into a single block. The Personal Shrinking Device lets you walk inside it.",
        "&eHow:&r shrinking and enlarging modules, an eye of ender, copper, iron and glass panes (check JEI).",
        "&eTip:&r it also shows you which machine room you're in and takes you back out."]),
    Q("mf_cm_walls", 2, 6.5, [item("compactmachines:wall", 16)], "Machine Walls", deps=["mf_compact"], xp=30,
      subtitle="Polished deepslate, made compact", desc=[
        "&eWhat:&r Compact Machine Walls frame every machine block.",
        "&eHow:&r crafted from polished deepslate (check JEI).",
        "&eTip:&r inside a room the walls are unbreakable; these crafted ones aren't."]),
    Q("mf_cm_modules", 4, 6.5, [item("compactmachines:shrinking_module", 2), item("compactmachines:enlarging_module", 2)], "Atom Modules", deps=["mf_cm_walls"], xp=40,
      subtitle="One shrinks, one enlarges", desc=[
        "&eWhat:&r every Compact Machine needs one Atom Shrinking Module and one Atom Enlarging Module.",
        "&eHow:&r an eye of ender, a light pressure plate, a stone button and a piston (sticky for shrinking).",
        "&eTip:&r make spares; each new machine eats a pair."]),
    Q("mf_cm_room", 6, 6.5, [dim("compactmachines:compact_world")], "Step Inside", deps=["mf_cm_modules"], xp=100,
      size=1.5, subtitle="Craft a machine and shrink into it", desc=[
        "&6You remember holding a world in your palm. This one is smaller, but it's yours.&r",
        "&eWhat:&r craft a Compact Machine, place it, and right-click it with the Personal Shrinking Device to enter its room.",
        "&eHow:&r walls + both modules + a metal sets the size: copper = tiny, iron = small, gold = normal, obsidian = giant, netherite = colossal (check JEI for the rest).",
        "&eTip:&r tunnels carry items, fluids and power through the walls; perfect for a compact chemical line."]),

    # --- Odds and ends (y=9) -------------------------------------------------------------------
    Q("mf_facade", 0, 9, [item("cable_facades:facade_wrench")], "Hide the Cables", deps=["t3_hull"], xp=25,
      subtitle="Cables that look like any block", desc=[
        "&eWhat:&r Cable Facades disguise cables and pipes as any block. Tidy factories, same throughput.",
        "&eHow:&r craft the Facade Wrench, then apply blocks to cables (check JEI).",
        "&eTip:&r facades on MI pipes make chemical lines much easier to look at."]),
    Q("mf_cake", 2, 9, [item("telepastries:overworld_cake")], "Teleporting Cake", deps=["t2_nether"], xp=40,
      subtitle="Eat a slice, change dimension", desc=[
        "&eWhat:&r TelePastries cakes teleport you to their dimension when you eat a slice.",
        "&eHow:&r the Overworld Cake brings you home. Refill it with saplings; the Nether Cake takes obsidian.",
        "&eTip:&r place the Overworld Cake in your Nether hub for a quick ride home."]),
    Q("mf_cake_end", 3, 10.5, [item("telepastries:end_cake")], "Cake at the End", deps=["mf_cake", "w_end"], xp=40,
      optional=True, tokens=1, subtitle="Optional: a slice to the End", desc=[
        "&eWhat:&r a cake that sends you to the End.",
        "&eHow:&r a cake surrounded by eyes of ender. Refill it with eyes of ender.",
        "&eTip:&r leave it in your base so the End is one bite away."]),

    # --- More mob data (y=-1.5 / -3) -----------------------------------------------------------
    Q("mf_kill_blaze", 1, -1.5, [kill("minecraft:blaze", 30)], "Training Data: Blazes", deps=["mf_model", "t2_nether"], xp=60,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: kill 30 blazes with a model loaded", desc=[
        "&eWhat:&r every kill with a matching model in your Deep Learner adds data. Blaze models are worth it: blaze rods feed brewing, Powah and Create's Blaze Burners.",
        "&eHow:&r put a blaze data model in the Deep Learner, keep it in your inventory, and hunt blazes at a Nether Fortress.",
        "&eTip:&r a blaze model at a high tier turns the Simulation Chamber into an endless rod farm."]),
    Q("mf_kill_ender", 5, -1.5, [kill("minecraft:enderman", 30)], "Training Data: Endermen", deps=["mf_model"], xp=60,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: kill 30 endermen with a model loaded", desc=[
        "&eWhat:&r ender pearls go into Entangled blocks, AE2 seeds, Powah ender cells and teleporting. An enderman model makes them renewable.",
        "&eHow:&r load an enderman data model and hunt them at night, in warped forests, or in the End.",
        "&eTip:&r wear a carved pumpkin, or look at their feet, so they don't attack you first."]),
    Q("mf_predictions", 5, -3, [item("hostilenetworks:overworld_prediction", 4), item("hostilenetworks:nether_prediction", 4), item("hostilenetworks:end_prediction", 4)], "Three Worlds of Data", deps=["mf_sim", "w_end"], xp=100,
      optional=True, tokens=1, subtitle="Optional: predictions from every dimension", desc=[
        "&eWhat:&r each simulation gives a prediction for the mob's home dimension as well as the drop. Overworld, Nether and End predictions are used in recipes and Fabrication Directives.",
        "&eHow:&r run simulations of one mob from each dimension, such as a zombie, a blaze and an enderman.",
        "&eTip:&r predictions stack up fast; send them to storage with a pipe."]),
    Q("mf_data_center", 9, -1.5, [item("hostilenetworks:data_center"), item("hostilenetworks:data_center_io_port")], "The Data Center", deps=["mf_fab"], xp=300,
      optional=True, tokens=2, subtitle="Optional: 25 simulations at once", desc=[
        "&6You remember watching a million lives at once. This is a pale copy, but a useful one.&r",
        "&eWhat:&r the Data Center runs up to 25 Self Aware data models at the same time, each making one drop per cycle.",
        "&eHow:&r a Sim Chamber, a Loot Fabricator, a Nether Star, echo shards and obsidian. Build a 7x7x7 hollow shell: obsidian floor, black stained glass walls and ceiling, with the controller in a bottom wall facing out (JEI shows the rules).",
        "&eTip:&r IO ports in the shell let pipes feed inputs and pull the drops. A Fabrication Directive picks which drop each slot makes."]),

    # --- More Extended Crafting (y=4) ----------------------------------------------------------
    Q("mf_flux_crafter", 2, 4, [item("extendedcrafting:flux_crafter"), item("extendedcrafting:flux_alternator", 2)], "Flux Crafting", deps=["mf_basic_table"], xp=60,
      optional=True, tokens=1, subtitle="Optional: crafting powered by FE", desc=[
        "&eWhat:&r the Flux Crafter runs special recipes using FE delivered by nearby Flux Alternators, like the Flux Star.",
        "&eHow:&r gold and redstone ingots (check JEI). Place alternators around the crafter and power them.",
        "&eTip:&r JEI's Flux Crafter tab lists every recipe and the FE each one needs."]),
    Q("mf_auto_table", 11, 4, [item("extendedcrafting:basic_auto_table")], "Auto Tables", deps=["mf_crystaltine"], xp=100,
      optional=True, tokens=1, subtitle="Optional: tables that craft by themselves", desc=[
        "&eWhat:&r Auto Tables remember a recipe and craft it with FE whenever the ingredients are inside. Each table size has its own.",
        "&eHow:&r a crafting table of the same size plus crystaltine components (check JEI).",
        "&eTip:&r the Ultimate Auto Table is also the heart of Packaged ExCrafting's Ultimate Crafter (see the Applied Energistics page)."]),

    # --- More Compact Machines (y=8) -----------------------------------------------------------
    Q("mf_cm_machine", 7, 8, [item("compactmachines:machine", 4)], "A Room for Every Line", deps=["mf_cm_room"], xp=75,
      optional=True, tokens=1, subtitle="Optional: four compact machines", desc=[
        "&eWhat:&r one compact machine per chemical line keeps your base tidy: a sulfuric acid room, a chlorine room, a petrochemical room.",
        "&eHow:&r craft more machines (check JEI for the sizes) and enter each with the Personal Shrinking Device.",
        "&eTip:&r a room only runs while the chunk with its machine block is loaded, so claim and force-load your factory."]),
], links=[("t4_mv", -2, 0), ("t1_steel", -2, 2.5), ("t3_hull", -2, 6.5), ("t5_ae2", -2, 4)])
