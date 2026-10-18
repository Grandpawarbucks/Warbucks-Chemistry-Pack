"""Quest chapter: t7. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

MI = "modern_industrialization:"
AA = "ad_astra:"
MEK = "mekanism:"

CHAPTER = Chapter("t7", "VIII. Creation", "ad_astra:tier_1_rocket",
        ["Leave the cradle. Make matter from energy. Seed a new world."], MAIN, [
    # ---------------------------------------------------------------- leaving the planet
    Q("t7_nasa", 0, 0, [item(AA + "nasa_workbench")], "Leaving the Cradle", deps=["t6_pu"], xp=400,
      subtitle="Every rocket starts on this bench", desc=[
        "&6You remember the stars up close. Time to stop looking at them from the ground.&r",
        "&eWhat:&r the NASA Workbench assembles every Ad Astra rocket.",
        "&eHow:&r in this pack it needs an EV (Highly Advanced) hull, so processing units come first."]),
    Q("t7_parts", 2, 0, [item(AA + "rocket_nose_cone"), item(AA + "rocket_fin", 4), item(AA + "steel_tank", 2), item(AA + "steel_engine")], "Rocket Parts", deps=["t7_nasa"], xp=200,
      subtitle="Nose cone, fins, tanks and an engine", desc=[
        "&eWhat:&r a Tier 1 rocket needs a nose cone, 4 fins, 2 steel tanks, a steel engine and 6 steel blocks.",
        "&eChemistry:&r a rocket carries its own oxidiser as well as fuel: there's no air to burn in once you're up.",
        "&eHow:&r all parts are crafted from steel plates and rods (check JEI). The nose cone uses a lightning rod."]),
    Q("t7_suit", 2, -2, [item(AA + "space_helmet"), item(AA + "oxygen_loader")], "Breathe", deps=["t7_nasa"], xp=200,
      subtitle="Space has no air", desc=[
        "&eWhat:&r the Oxygen Loader fills your space suit's tank.",
        "&eChemistry:&r it accepts plain water, but 100 mB of water gives only 4 mB of oxygen. Pure O₂ from your electrolysis line (2H₂O → 2H₂ + O₂) goes in 1:1.",
        "&eHow:&r pipe MI or Mekanism oxygen into the loader, power it, and put the suit in the slot."]),
    Q("t7_suit_full", 4, -2, [item(AA + "space_suit"), item(AA + "space_pants"), item(AA + "space_boots")], "The Full Suit", deps=["t7_suit"], xp=150,
      subtitle="Helmet alone won't do", desc=[
        "&eWhat:&r the full set keeps you alive in vacuum and in the cold of the Moon.",
        "&eHow:&r check JEI for each piece. Wear all four before launch.",
        "&eTip:&r the chest piece holds the oxygen. Watch the gauge on your HUD."]),
    Q("t7_launchpad", 4, 0, [item(AA + "launch_pad")], "Launch Pad", deps=["t7_parts"], xp=100,
      subtitle="Somewhere to stand the rocket", desc=[
        "&eWhat:&r rockets are placed on a launch pad, not on the bare ground.",
        "&eHow:&r craft it (check JEI) and place it in the open, with clear sky above.",
        "&eTip:&r build a pad on each world you visit so you always have somewhere to land and relaunch."]),
    Q("t7_fuel", 4, 2, [item(MI + "diesel_bucket", 3)], "Rocket Fuel", deps=["t7_nasa", "t5_diesel"], xp=150,
      subtitle="Ad Astra burns your diesel", desc=[
        "&eWhat:&r in this pack rockets run on MI diesel (biodiesel works too). Ad Astra's own oil refining is removed.",
        "&eChemistry:&r a kilogram of diesel releases about 45 MJ when it burns: more than ten times a good battery.",
        "&eHow:&r fill the rocket from buckets or pipes (check its GUI for how much it holds).",
        "&eTip:&r bring spare fuel for the trip home."]),
    Q("t7_rocket", 6, 0, [item(AA + "tier_1_rocket"), dim(AA + "moon")], "One Small Step", deps=["t7_launchpad", "t7_fuel", "t7_suit_full"], xp=600, size=1.5,
      subtitle="Reach the Moon", desc=[
        "&6The Moon looks smaller than you remember. Or perhaps you were larger.&r",
        "&eHow:&r build the rocket in the NASA Workbench, place it on the pad, fuel it, climb in and launch. Pick the Moon on the planet screen.",
        "&eTip:&r place a bed or waystone near your landing site before exploring."]),
    Q("t7_desh", 8, -2, [item(AA + "raw_desh", 8), item(AA + "desh_plate", 4)], "Desh", deps=["t7_rocket"], xp=200,
      subtitle="The Moon's own metal", desc=[
        "&eWhat:&r desh is Ad Astra's lunar metal, needed for the Tier 2 rocket and oxygen equipment.",
        "&eHow:&r mine desh ore on the Moon, smelt it, and press the ingots into plates in Ad Astra's Compressor.",
        "&eTip:&r the Moon also has cheese ore. Really."]),
    Q("t7_distributor", 10, -2, [item(AA + "oxygen_distributor")], "A Breathable Room", deps=["t7_desh"], xp=200,
      subtitle="Bring an atmosphere with you", desc=[
        "&eWhat:&r the Oxygen Distributor fills a sealed room with air, so you can take off your helmet.",
        "&eHow:&r built from an Oxygen Loader, a large gas tank, fans, an oxygen gear and desh plates. Feed it oxygen and power.",
        "&eTip:&r any gap in the walls lets the air out. Seal the room completely, doors included."]),
    # ---------------------------------------------------------------- antimatter
    Q("t7_sps", 8, 2, [item(MEK + "sps_port", 2), item(MEK + "supercharged_coil")], "Supercritical Phase Shifter", deps=["t6_waste"], xp=300,
      subtitle="A multiblock that turns polonium into antimatter", desc=[
        "&eWhat:&r the SPS is Mekanism's largest machine. It needs huge amounts of power.",
        "&eHow:&r Just Enough Mekanism Multiblocks shows the full layout in JEI. Ports feed polonium in and power the supercharged coil.",
        "&eTip:&r feed it from a fission reactor and turbine, or several Flux Networks plugs."]),
    Q("t7_crystallizer", 10, 2, [item(MEK + "chemical_crystallizer")], "Bottling Antimatter", deps=["t7_sps"], xp=150,
      subtitle="Antimatter gas becomes a pellet", desc=[
        "&eWhat:&r the SPS outputs antimatter as a gas. The Chemical Crystallizer packs 1000 mB of it into one pellet.",
        "&eHow:&r pipe antimatter from the SPS output port into the crystallizer.",
        "&eTip:&r pipe the SPS straight into the crystallizer so the antimatter never sits in a tank."]),
    Q("t7_antimatter", 12, 0, [item(MEK + "sps_casing", 4), item(MEK + "pellet_antimatter")], "Antimatter", deps=["t7_rocket", "t7_crystallizer"], xp=1000, size=1.75, shape="hexagon",
      subtitle="Matter with every charge reversed", desc=[
        "&6Matter from nothing but energy. This is the first thing you've made that you once made too.&r",
        "&eChemistry:&r when matter meets antimatter both vanish into pure energy, E = mc². One gram of each releases about 1.8 × 10¹⁴ J.",
        "&eHow:&r SPS → antimatter gas → Chemical Crystallizer → antimatter pellet.",
        "&eTip:&r it's the most energy-dense substance there is. Antimatter Cores need four pellets each."]),
    # ---------------------------------------------------------------- energy cores
    Q("t7_core_empty", 14, -2, [item("kubejs:energy_core_empty")], "Empty Energy Core", deps=["t6_waste"], xp=300,
      subtitle="A stainless shell around polonium", desc=[
        "&eWhat:&r the vessel for the most concentrated energy you can hold.",
        "&eChemistry:&r polonium gives off so much heat by decay that a gram of it glows. Here it seeds the core.",
        "&eHow:&r craft: 4 stainless steel plates + 4 polonium pellets + a processing unit in the centre.",
        "&eTip:&r the Complete Periodic Table quest rewards one empty core."]),
    Q("t7_core_charge", 16, -2, [item("kubejs:energy_core")], "Charge the Core", deps=["t7_core_empty"], xp=400,
      subtitle="About three million EU, poured into one item", desc=[
        "&eWhat:&r an empty core holds nothing until you charge it with raw electrical energy.",
        "&eHow:&r MI Assembler at 512 EU/t for 6000 ticks: about 3 million EU per core.",
        "&eTip:&r give it its own power line. A charging core will starve every other machine on the network."]),
    Q("t7_cores", 18, 0, [item("kubejs:energy_core"), item("kubejs:antimatter_core")], "Antimatter Core", deps=["t7_core_charge", "t7_antimatter"], xp=1000, size=1.5,
      subtitle="The heart of the Seed", desc=[
        "&6You feel it humming in your hand. You remember being this.&r",
        "&eWhat:&r a charged core, upgraded with antimatter and a quantum circuit.",
        "&eHow:&r MI Assembler at 2048 EU/t for 6000 ticks: charged Energy Core + 4 antimatter pellets + 1 quantum circuit.",
        "&eTip:&r the Seed needs eight. Start a production line, not a one-off."]),
    # ---------------------------------------------------------------- the Seed's checklist
    Q("t7_seed_basics", 20, -6, [item(MI + "coke", 4), item("chemlib:water", 8), item("chemlib:hydrogen", 4)], "Fire, Water, Hydrogen", deps=["t7_cores"], xp=200,
      subtitle="Seed checklist: where it all began", desc=[
        "&eWhat:&r the Seed's corners and edges hold the first things you learned: coke from your coke oven, and water and hydrogen synthesized as chemicals.",
        "&eHow:&r 4 coke, 8 ChemLib water and 4 ChemLib hydrogen (from the Alchemistry Dissolver and Combiner).",
        "&eTip:&r all three are cheap now. Make spares."]),
    Q("t7_seed_acid", 20, -4, [item(MI + "sulfuric_acid_bucket", 8)], "Eight Buckets of Acid", deps=["t7_cores"], xp=200,
      subtitle="Seed checklist: the Acid Age", desc=[
        "&eHow:&r fill buckets from your sulfuric acid tanks.",
        "&eWhat:&r 8 buckets of sulfuric acid, the chemical that unlocked 5x ore processing.",
        "&eTip:&r buckets don't stack. Clear inventory space first."]),
    Q("t7_seed_pe", 20, -2, [item(MI + "polyethylene_bucket", 16)], "Sixteen Buckets of Plastic", deps=["t7_cores"], xp=200,
      subtitle="Seed checklist: the Oil Age", desc=[
        "&eHow:&r polymerise ethylene in the Chemical Reactor, as in Petrochemistry.",
        "&eWhat:&r 16 buckets of polyethylene, the most of any ingredient.",
        "&eTip:&r fill them straight from your polymerisation reactor's output."]),
    Q("t7_seed_cores", 20, 0, [item("kubejs:antimatter_core", 8)], "Eight Antimatter Cores", deps=["t7_cores"], xp=500, size=1.25,
      subtitle="Seed checklist: the hardest part", desc=[
        "&eWhat:&r eight Antimatter Cores ring the centre of the recipe.",
        "&eHow:&r that's 32 antimatter pellets, 32 polonium pellets and 8 quantum circuits in total.",
        "&eTip:&r a second SPS halves the wait."]),
    Q("t7_seed_tech", 20, 2, [item(MI + "processing_unit", 8), item(MI + "stainless_steel_plate", 4)], "Circuits and Steel", deps=["t7_cores"], xp=200,
      subtitle="Seed checklist: the machine ages", desc=[
        "&eWhat:&r 8 processing units and 4 stainless steel plates.",
        "&eHow:&r both come from lines you already run. Queue them in your assemblers.",
        "&eTip:&r processing units are slow to make, so start these early."]),
    Q("t7_seed_nuclear", 20, 4, [item("chemlib:oganesson", 8), item(MEK + "pellet_plutonium", 4), item(MEK + "pellet_polonium", 4)], "Heavy Elements", deps=["t7_cores", "t6_table"], xp=300,
      subtitle="Seed checklist: the atomic age", desc=[
        "&eWhat:&r 8 oganesson, 4 plutonium pellets and 4 polonium pellets.",
        "&eHow:&r oganesson from the Fusion Chamber; pellets from your reactor's waste.",
        "&eTip:&r automate the fusion chamber for oganesson; eight by hand is slow."]),
    Q("t7_seed_stars", 20, 6, [item("minecraft:nether_star", 4), item("minecraft:dragon_egg")], "Stars and an Egg", deps=["t7_cores"], xp=300,
      subtitle="Seed checklist: trophies of the old world", desc=[
        "&eWhat:&r 4 Nether Stars, and the Dragon Egg at the very centre.",
        "&eHow:&r summon and defeat the Wither four times; kill the Ender Dragon for the egg.",
        "&eTip:&r there's only one Dragon Egg per world. On a server, agree who crafts the Seed."]),
    Q("t7_seed", 22, 0, [item("kubejs:seed_of_a_new_world")], "Seed of a New World", deps=["t7_cores", "t6_table", "mf_ult_table", "t7_seed_basics", "t7_seed_acid", "t7_seed_pe", "t7_seed_cores", "t7_seed_tech", "t7_seed_nuclear", "t7_seed_stars"],
      xp=3000, size=2.0, shape="hexagon", subtitle="The endgame goal", desc=[
        "&6Every lesson, in one 9x9 grid.&r",
        "&eWhat:&r a recipe on the Ultimate Table that needs something from every tier.",
        "&eHow:&r 4 coke, 8 water, 4 hydrogen, 8 sulfuric acid, 16 polyethylene, 8 processing units, 4 stainless plates, 8 oganesson, 4 plutonium, 4 polonium, 4 Nether Stars, 8 Antimatter Cores, and the Dragon Egg at the centre.",
        "&eTip:&r check JEI for the exact layout before you fill the table."]),
    Q("t7_creation", 25, 0, [tick()], "A New World", deps=["t7_seed"], xp=2000, size=2.5, shape="gear", tokens=50,
      subtitle="The demigod, restored", desc=[
        "&6You took the world apart, element by element, and learned to build it again.&r",
        "Fire, steel, acid, oil, silicon, the atom, antimatter. Every tier was a lesson in chemistry, and you mastered them all.",
        "&6The worlds out there are blank canvases now. Go make them yours.&r"]),
    # ---------------------------------------------------------------- optional side quests
    Q("t7_opt_cheese", 6, -4, [item(AA + "cheese")], "Made of Cheese", deps=["t7_rocket"], xp=50,
      optional=True, tokens=1, subtitle="Optional: test an old rumour", desc=[
        "&eWhat:&r the old rumour is partly true: the Moon has cheese ore.",
        "&eHow:&r mine moon cheese ore and smelt it (or macerate it in MI).",
        "&eTip:&r it's food. Lunar picnic, anyone?"]),
    Q("t7_opt_orbit", 8, -4, [dim(AA + "earth_orbit")], "Low Earth Orbit", deps=["t7_rocket"], xp=150,
      optional=True, tokens=1, subtitle="Optional: look down on home", desc=[
        "&eWhat:&r every planet has an orbit dimension above it, a good place for a space station.",
        "&eHow:&r pick Earth Orbit on the rocket's planet screen.",
        "&eTip:&r bring building blocks and a way home."]),
    Q("t7_opt_planets", 10, -4, [dim(AA + "moon"), dim(AA + "mars"), dim(AA + "venus"), dim(AA + "mercury"), dim(AA + "glacio")], "Grand Tour", deps=["t7_rocket"], xp=500,
      optional=True, tokens=2, subtitle="Optional: visit every planet", desc=[
        "&eWhat:&r the Moon (Tier 1 rocket), Mars (Tier 2), Venus and Mercury (Tier 3) and Glacio (Tier 4).",
        "&eHow:&r a dimension task completes on arrival. Plan fuel and oxygen for each trip.",
        "&eTip:&r Venus and Mercury are hot enough to cook an ordinary space suit. Bring the netherite one."]),
    Q("t7_opt_hot_suit", 4, -4, [item(AA + "netherite_space_helmet"), item(AA + "netherite_space_suit")], "Heat-Proof Suit", deps=["t7_suit_full", "w_mars"], xp=150,
      optional=True, tokens=1, subtitle="Optional: armour for hot planets", desc=[
        "&eWhat:&r the netherite space suit survives the heat of Venus and Mercury.",
        "&eWhat:&r the netherite space suit survives the heat of Venus and Mercury.",
        "&eHow:&r the chest piece is a netherite chestplate with ostrum plates (from Mars), gas tanks and an oxygen gear. Check JEI for the rest."]),
    Q("t7_opt_tier4", 12, -4, [item(AA + "tier_4_rocket"), dim(AA + "glacio")], "Glacio", deps=["w_venus"], xp=400,
      optional=True, tokens=2, subtitle="Optional: the frozen planet in another system", desc=[
        "&eWhat:&r Glacio orbits another star and needs a Tier 4 rocket built from calorite.",
        "&eHow:&r calorite comes from Venus. The tanks, engine and blocks are all calorite (check JEI).",
        "&eTip:&r it's the only planet outside our solar system. Take a look at the sky."]),
    Q("t7_opt_nucleo", 12, 3, [item(MEK + "antiprotonic_nucleosynthesizer")], "Antiprotonic Nucleosynthesizer", deps=["t7_antimatter"], xp=300,
      optional=True, tokens=2, subtitle="Optional: transmute items with antimatter", desc=[
        "&eWhat:&r Mekanism's late-game machine uses antimatter to rebuild one item into another.",
        "&eHow:&r check JEI for the recipe and for what it can transmute.",
        "&eTip:&r it uses antimatter as fuel, so it needs your SPS running."]),
])
