"""Quest chapter: factory. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, kill, anytag, anyof, MAIN, SIDE  # noqa: F401

# ATM10 mirror (2026-10-20, user decision): the Hostile Neural Networks part follows ATM10's "hostile_neural_networks"
# chapter quest for quest (its item list, order and shape only; all text is ours). ATM10 asks for a prediction of each
# mob; our engine can't ask for an item with a data component, so each of those quests asks for the drop the Loot
# Fabricator makes from that mob's predictions. Extended Crafting and Compact Machines stay as our own sections.
HNN = "Mob Simulation"


def sim(key, mob, drop, title, mirror, ids=None, note=None, optional=True, size=None, xp=40):
    """One simulated mob: fabricate its drop from predictions (hunting it also works)."""
    task = anyof(ids) if ids else item(drop)
    return Q(key, 0, 0, [task], "Simulated " + title, deps=["mf_fab"], xp=xp, optional=optional, size=size, section=HNN,
             mirror=mirror, subtitle=("Optional: " if optional else "") + f"{mob} predictions into loot", desc=[
                 f"&eWhat:&r run a {mob} data model in the Simulation Chamber, then turn its predictions into drops in the Loot Fabricator.",
                 "&eHow:&r train the model to Basic or better, simulate it, and pick this drop in the Fabricator's menu (check JEI for the full list).",
                 "&eTip:&r " + (note or "hunting the mob also counts; the point is never having to again.")])


CHAPTER = Chapter("factory", "Mob Data and Big Crafting", "hostilenetworks:sim_chamber",
        ["Monifactory-inspired machinery: simulate mobs, craft on giant tables, and fold whole factories into a block."], SIDE, [
    # --- Hostile Neural Networks (y=0) ---------------------------------------------------------
    Q("mf_learner", 0, 0, [item("hostilenetworks:deep_learner")], "Deep Learning", deps=["mf_hnn_hub"], xp=40, section=HNN, mirror="3E3CBDCEAB0FF28F",
      subtitle="Teach a model by fighting", desc=[
        "&6You remember knowing every creature by name. You can learn them again, one fight at a time.&r",
        "&eWhat:&r Hostile Neural Networks records mobs into data models. Trained models later make mob drops without the mob.",
        "&eHow:&r craft the Deep Learner (check JEI). Put models in the Deep Learner and keep it in your inventory while you fight.",
        "&eTip:&r start with a mob whose drops you'll need in bulk, like blazes, slimes or endermen."]),
    Q("mf_model", 2, 0, [item("hostilenetworks:data_model")], "Your First Model", deps=["mf_learner", "mf_blank_model"], xp=40, section=HNN, mirror="34CD54347E9821B5",
      subtitle="Attune a blank model to one mob", desc=[
        "&eWhat:&r a data model attuned to one mob type. It starts at Faulty and levels up as you kill that mob.",
        "&eHow:&r right-click a mob with a Blank Data Model, or craft a specific model (check JEI). Then hunt with the Deep Learner.",
        "&eTip:&r tiers go Faulty, Basic, Advanced, Superior, Self Aware. Higher tiers are more accurate, so fewer simulations fail."]),
    Q("mf_sim", 4, 0, [item("hostilenetworks:sim_chamber"), item("hostilenetworks:prediction_matrix")], "Simulation", deps=["mf_learner", "mf_blank_model", "t4_mv"], xp=150, section=HNN, mirror="104EBBC08B4733F5",
      subtitle="Mob drops from power and matrices", desc=[
        "&eWhat:&r the Simulation Chamber runs a trained model on FE and prediction matrices to make predictions and mob drops.",
        "&eHow:&r it needs an &eMV electronic circuit&r (aluminum chemistry). Insert a model of Basic tier or better, matrices and power.",
        "&eTip:&r pipe matrices in and drops out; one chamber per model keeps things simple."]),
    Q("mf_fab", 6, 0, [item("hostilenetworks:loot_fabricator")], "Loot Fabricator", deps=["mf_sim"], xp=150, section=HNN, mirror="14B3542ECB59869C",
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
    Q("mf_twilight_pred", 7, -1.5, [item("hostilenetworks:twilight_prediction")], "Twilight Predictions", deps=["mf_sim", "t5_twilight"], xp=100, section=HNN, mirror="14F7F256DA863280",
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
      subtitle="Cables that look like any block", optional=True, tokens=1, desc=[
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
    Q("mf_predictions", 5, -3, [item("hostilenetworks:overworld_prediction")], "Overworld Predictions", deps=["mf_sim"], xp=40, section=HNN, mirror="2559201BCF5D497C",
      subtitle="Data from an Overworld mob", desc=[
        "&eWhat:&r each simulation gives a prediction for the mob's home dimension as well as the drop. Overworld, Nether and End predictions are used in recipes and Fabrication Directives.",
        "&eHow:&r simulate any Overworld mob, such as a zombie or a cow. The Nether and End ones are their own quests.",
        "&eTip:&r predictions stack up fast; send them to storage with a pipe."]),
    Q("mf_data_center", 9, -1.5, [item("hostilenetworks:data_center"), anytag("c:obsidians"), item("minecraft:black_stained_glass"), item("hostilenetworks:data_center_io_port")],
      "The Data Center", deps=["mf_fab"], xp=300, size=2.0, shape="gear", section=HNN, mirror="3F3F3174BD9D03BD", loot="t5",
      subtitle="25 simulations at once", desc=[
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

    # --- ATM10-alignment round (2026-10-19): MI addon with no other home -------------------------
    Q("mf_multiblock_builder", 0, 0, [item("industrialization_overdrive:terminal")], "Multiblock Builder",
      subtitle="Place a whole MI multiblock in one go", deps=["t4_mv", "t3_ebf"], xp=80, optional=True, tokens=1, desc=[
        "&eWhat:&r Industrialization Overdrive's Multiblock Builder places every missing block of an MI multiblock from your inventory (or a linked ME network). Other modes copy and paste a formed one, or tear it down.",
        "&eHow:&r steel plates, glass panes and an &eMI electronic circuit&r (MV). Look at the controller and press the key combination its tooltip shows; another key cycles the modes.",
        "&eTip:&r carry the casings, hatches and coils first: it only places what you have."]),

    # ===== ATM10 mirror: hostile_neural_networks (2026-10-20) ================================================
    Q("mf_hnn_hub", 0, 0, [item("minecraft:redstone")], "Neural Networks", deps=["gs_redstone"], xp=15, size=2.0, shape="gear",
      section=HNN, mirror="37EBB8E0D6E5F821", subtitle="Redstone: the wiring of a mob simulator", desc=[
        "&6You remember knowing every creature by heart. A machine can learn them for you now.&r",
        "&eWhat:&r Hostile Neural Networks trains data models on the mobs you fight, then simulates them for their drops. This page also holds Extended Crafting and Compact Machines.",
        "&eChemistry:&r redstone stands in for real conductors. Real circuits run on copper traces and doped silicon.",
        "&eHow:&r pick up any redstone. The learner and models below need it.",
        "&eTip:&r the Simulation Chamber and Loot Fabricator need an MV electronic circuit in this pack."]),
    Q("mf_blank_model", 0, 0, [item("hostilenetworks:blank_data_model")], "Model Framework", deps=["mf_hnn_hub"], xp=20, section=HNN,
      mirror="58C2ABED43B2EA61", subtitle="An empty model, waiting for a mob", desc=[
        "&eWhat:&r a blank data model. Right-click a mob with it (or craft a specific one) to attune it.",
        "&eHow:&r check JEI: redstone, stone and a few common parts.",
        "&eTip:&r make several; each mob type needs its own model."]),
    Q("mf_pred_nether", 0, 0, [item("hostilenetworks:nether_prediction")], "Nether Predictions", deps=["mf_sim"], xp=40, section=HNN,
      mirror="10E8BC20D406D9FB", subtitle="Data from a Nether mob", desc=[
        "&eWhat:&r simulating a Nether mob (blaze, ghast, magma cube, wither skeleton and more) also gives a generalised Nether prediction.",
        "&eHow:&r put a Nether mob's model in the Simulation Chamber with matrices and power.",
        "&eTip:&r a blaze model doubles as a blaze rod farm through the Loot Fabricator."]),
    Q("mf_pred_end", 0, 0, [item("hostilenetworks:end_prediction")], "End Predictions", deps=["mf_sim"], xp=40, section=HNN,
      mirror="5A23107C363A209E", subtitle="Data from an End mob", desc=[
        "&eWhat:&r End mobs (enderman, shulker, the dragon) give a generalised End prediction when simulated.",
        "&eHow:&r an enderman model is the easy one: endermen walk the Overworld at night.",
        "&eTip:&r ender pearls from the fabricator feed AE2, Entangled and teleporting."]),

    # --- one prediction per simulated mob (each quest asks for the drop you fabricate from that mob) ------------
    sim("mf_sim_chicken", "chicken", "minecraft:feather", "Chicken", "7EBBEB504C38898A"),
    sim("mf_sim_mimic", "mimic", "artifacts:crystal_heart", "Mimic", "2F6F888610373E21",
        ids=["artifacts:steadfast_spikes", "artifacts:shock_pendant", "artifacts:crystal_heart", "artifacts:superstitious_hat", "artifacts:power_glove"],
        note="a mimic model fabricates artifacts; any of the ones listed counts."),
    sim("mf_sim_wilden", "wilden", "ars_nouveau:wilden_horn", "Wilden", "1FD43610960E3450",
        ids=["ars_nouveau:wilden_horn", "ars_nouveau:wilden_spike", "ars_nouveau:wilden_wing"],
        note="the Ars Nouveau wilden model gives horns, spikes and wings for familiars and rituals."),
    sim("mf_sim_blaze", "blaze", "minecraft:blaze_rod", "Blaze", "12172C1449296E06"),
    sim("mf_sim_piglich", "piglich", "allthemodium:piglich_heart", "Piglich", "5905241071D1960A", optional=False, size=1.5, xp=150,
        note="the Piglich is a boss of the Allthemodium dimensions; its model is expensive to run."),
    sim("mf_sim_cod", "cod", "minecraft:cod", "Cod", "3B9D8E374CDAFD6C"),
    sim("mf_sim_creeper", "creeper", "minecraft:gunpowder", "Creeper", "2571C1D19F83BB3B",
        note="gunpowder is the old black powder: potassium nitrate, charcoal and sulfur."),
    sim("mf_sim_cow", "cow", "minecraft:leather", "Cow", "3364DD88B5450365"),
    sim("mf_sim_drowned", "drowned", "minecraft:copper_ingot", "Drowned", "0DCF732A8B8E5704"),
    sim("mf_sim_elder", "elder guardian", "minecraft:wet_sponge", "Elder Guardian", "364A1936C5AFFB4E"),
    sim("mf_sim_dragon", "ender dragon", "minecraft:dragon_breath", "Ender Dragon", "6B945A5B293C0153", optional=False, xp=150),
    sim("mf_sim_enderman", "enderman", "minecraft:ender_pearl", "Enderman", "6C71A6DB57FC3EE7"),
    sim("mf_sim_evoker", "evoker", "minecraft:totem_of_undying", "Evoker", "1447705D6E49EBF6"),
    sim("mf_sim_ghast", "ghast", "minecraft:ghast_tear", "Ghast", "5FE40F753A69537E"),
    sim("mf_sim_glow_squid", "glow squid", "minecraft:glow_ink_sac", "Glow Squid", "5D9752510C66985D"),
    sim("mf_sim_magma", "magma cube", "minecraft:magma_cream", "Magma Cube", "280CA599D29791DF"),
    sim("mf_sim_sheep", "sheep", "minecraft:white_wool", "Sheep", "20FF2AE066B99DB3"),
    sim("mf_sim_squid", "squid", "minecraft:ink_sac", "Squid", "203E1B5BD21F00D1",
        note="real squid ink is mostly melanin, the same pigment as in skin and hair."),
    sim("mf_sim_spider", "spider", "minecraft:spider_eye", "Spider", "2DDE880D44E1FCDF"),
    sim("mf_sim_snow_golem", "snow golem", "minecraft:snowball", "Snow Golem", "35D3DEB3F43A8A06"),
    sim("mf_sim_slime", "slime", "minecraft:slime_ball", "Slime", "6961D45456433D56"),
    sim("mf_sim_skeleton", "skeleton", "minecraft:bone", "Skeleton", "6367CB97FA648E63",
        note="bone is mostly hydroxyapatite, Ca₅(PO₄)₃(OH), which is why bone meal is a phosphate fertiliser."),
    sim("mf_sim_shulker", "shulker", "minecraft:shulker_shell", "Shulker", "3F7FCDBEFFE5954A"),
    sim("mf_sim_warden", "warden", "minecraft:echo_shard", "Warden", "54E7ABFDFAA024E5", optional=False, xp=150),
    sim("mf_sim_witch", "witch", "minecraft:glowstone_dust", "Witch", "0807EF853E6D72B2"),
    sim("mf_sim_wither_skeleton", "wither skeleton", "minecraft:wither_skeleton_skull", "Wither Skeleton", "44791B697386A4BA"),
    sim("mf_sim_wither", "wither", "minecraft:nether_star", "Wither", "1D4D3CC361892A9E", optional=False, xp=200,
        note="simulated Withers mean Nether Stars without the fight; the Seed of a New World needs several."),
    sim("mf_sim_iron_golem", "iron golem", "minecraft:iron_ingot", "Iron Golem", "57577942A32FCB1F"),
    sim("mf_sim_rabbit", "rabbit", "minecraft:rabbit_foot", "Rabbit", "3BF3C32C603A8F57"),
    sim("mf_sim_polar_bear", "polar bear", "minecraft:salmon", "Polar Bear", "7F18BDDE7B20AD8D"),
    sim("mf_sim_pig", "pig", "minecraft:porkchop", "Pig", "77D5DAF30864466E"),
    sim("mf_sim_phantom", "phantom", "minecraft:phantom_membrane", "Phantom", "14437C59E04C7C5B"),
    sim("mf_sim_guardian", "guardian", "minecraft:prismarine_crystals", "Guardian", "7715A8287C00CCBC"),
    sim("mf_sim_hoglin", "hoglin", "minecraft:porkchop", "Hoglin", "4ED66AB8C1116797", ids=["minecraft:porkchop", "minecraft:leather"]),
    sim("mf_sim_vindicator", "vindicator", "minecraft:emerald", "Vindicator", "17280CDCFAAE4B87"),
    sim("mf_sim_zombified_piglin", "zombified piglin", "minecraft:gold_ingot", "Zombified Piglin", "37BEAA6576CD0507"),
    sim("mf_sim_zombie", "zombie", "minecraft:rotten_flesh", "Zombie", "597D92D3ED5E3868"),
], links=[("t4_mv", -2, 0), ("t1_steel", -2, 2.5), ("t3_hull", -2, 6.5), ("t5_ae2", -2, 4)], mirror="hostile_neural_networks")
