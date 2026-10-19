"""Quest chapter: t7. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

MI = "modern_industrialization:"
AA = "ad_astra:"
MEK = "mekanism:"

CHAPTER = Chapter("t7", "VIII. Beyond the Sky", "ad_astra:tier_1_rocket",
        ["Leave the cradle. Make matter from energy. Seed a new world."], MAIN, [
    # ---------------------------------------------------------------- leaving the planet
    Q("t7_nasa", 0, 0, [item(AA + "nasa_workbench")], "Leaving the Cradle", deps=["t6_pu"], xp=400,
      subtitle="Every rocket starts on this bench", desc=[
        "&6The stars were close once, close enough to touch. Time to stop looking at them from the ground.&r",
        "&eWhat:&r the NASA Workbench assembles every Ad Astra rocket.",
        "&eHow:&r in this pack it needs an EV (Highly Advanced) hull, so processing units come first."]),
    Q("t7_parts", 2, 0, [item(AA + "rocket_nose_cone"), item(AA + "rocket_fin", 4), item(AA + "steel_tank", 2), item(AA + "steel_engine")], "Rocket Parts", deps=["t7_nasa"], xp=200,
      subtitle="Nose cone, fins, tanks and an engine", desc=[
        "&eWhat:&r a Tier 1 rocket needs a nose cone, 4 fins, 2 steel tanks, a steel engine and 6 steel blocks.",
        "&eChemistry:&r real rockets carry their own oxidiser (often liquid oxygen) as well as fuel, because there's no air to burn in once you're up. Ad Astra simplifies this: its tanks take fuel only (MI diesel, biodiesel or cryo fuel; see Rocket Fuel).",
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
        "&eWhat:&r in this pack rockets burn anything in the Ad Astra fuel tag: MI diesel or biodiesel, or Ad Astra's cryo fuel. Ad Astra's own oil refining is removed.",
        "&eChemistry:&r a kilogram of diesel releases about 45 MJ when it burns: more than ten times a good battery.",
        "&eHow:&r fill the rocket from buckets or pipes (check its GUI for how much it holds). Cryo fuel comes from Ad Astra's Cryo Freezer (check JEI).",
        "&eTip:&r bring spare fuel for the trip home."]),
    Q("t7_rocket", 6, 0, [item(AA + "tier_1_rocket"), dim(AA + "moon")], "One Small Step", deps=["t7_launchpad", "t7_fuel", "t7_suit_full"], xp=600, size=1.5,
      subtitle="Reach the Moon", desc=[
        "&6The Moon looks smaller than you remember. Or perhaps you were larger.&r",
        "&eHow:&r build the rocket in the NASA Workbench, place it on the pad, fuel it, climb in and launch. Pick the Moon on the planet screen.",
        "&eTip:&r place a bed or waystone near your landing site before exploring."]),
    Q("t7_desh", 8, -2, [item(AA + "raw_desh", 8), item(AA + "desh_plate", 4)], "Desh", deps=["t7_rocket"], xp=200,
      optional=True, tokens=1, subtitle="Optional: the Moon's own metal", desc=[
        "&eWhat:&r desh is Ad Astra's lunar metal, needed for the Tier 2 rocket and oxygen equipment.",
        "&eHow:&r mine desh ore on the Moon, smelt it, and press the ingots into plates in Ad Astra's Compressor.",
        "&eTip:&r the Moon also has cheese ore. Really."]),
    Q("t7_distributor", 10, -2, [item(AA + "oxygen_distributor")], "A Breathable Room", deps=["t7_desh"], xp=200,
      optional=True, tokens=1, subtitle="Optional: bring an atmosphere with you", desc=[
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
        "&6Matter from nothing but energy. Even the oldest part of you is impressed.&r",
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
    Q("t7_cores", 18, 0, [item("kubejs:antimatter_core")], "Antimatter Core", deps=["t7_core_charge", "t7_antimatter", "t7_quantum"], xp=1000, size=1.5,
      subtitle="The heart of the Seed", desc=[
        "&6It hums in your hand like a small sun. You were this, once.&r",
        "&eWhat:&r a charged core, upgraded with antimatter and a quantum circuit.",
        "&eHow:&r MI Assembler at 2048 EU/t for 6000 ticks: charged Energy Core + 4 antimatter pellets + 1 quantum circuit.",
        "&eTip:&r the Seed needs eight. Start a production line, not a one-off."]),
    # The Seed's checklist, the Seed itself and t7_creation moved to tools/quests/seed.py and creation.py.
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

    # ---------------------------------------------------------------- the quantum circuit (ATM10-aligned, 2026-10-19)
    # Every Antimatter Core needs a quantum circuit, so this line is on the main path to the Seed.
    Q("t7_cryo", 0, 0, [item(MI + "cryofluid_bucket")], "Cryofluid", deps=["t6_nitrogen", "t6_monazite"], xp=200,
      subtitle="Argon and helium, colder than anything", desc=[
        "&eWhat:&r cryofluid fills cooling cells and qubits. Superconductors only work this cold.",
        "&eChemistry:&r liquid helium boils at −269 °C, four degrees above absolute zero. Nothing else stays liquid that cold.",
        "&eHow:&r Vacuum Freezer: 140 mB argon + 60 mB helium → 200 mB cryofluid.",
        "&eTip:&r the recipe draws 256 EU/t, more than a plain freezer allows. Put machine upgrades in it (Electrochemistry and Petrochemistry side quests)."]),
    Q("t7_cooling", 0, 0, [item(MI + "cooling_cell", 4)], "Cooling Cells", deps=["t7_cryo", "t6_hx_small"], xp=200,
      subtitle="A bucket of cold, sealed in tin", desc=[
        "&eWhat:&r cooling cells keep superconductor cable and quantum circuits below their critical temperature.",
        "&eHow:&r Assembler: 3 fluid pipes, 2 small heat exchangers, 6 tin plates and 1000 mB cryofluid.",
        "&eTip:&r every quantum circuit uses 2 directly, plus more inside its cable. Make a stack."]),
    Q("t7_superconductor", 0, 0, [item(MI + "superconductor_wire", 6), item(MI + "superconductor_cable", 6)], "Superconductor Cable", deps=["t7_cooling", "t6_rare_pgm"], xp=300,
      subtitle="Zero resistance, kept cold", desc=[
        "&eWhat:&r the cable of the quantum tier.",
        "&eChemistry:&r below its critical temperature a superconductor carries current with no loss at all and pushes magnetic fields out (the Meissner effect).",
        "&eHow:&r Mixer: 1 iridium + 3 annealed copper + 3 yttrium + 2 neodymium dust → 9 superconductor dust. Kanthal-tier EBF → hot ingot → freezer → plate → Wiremill (2 wire per plate). Assembler: 3 wire + 2 cooling cells + 1000 mB PVC → 6 cable."]),
    Q("t7_carbon", 0, 0, [item(MI + "carbon_dust", 2), item(MI + "carbon_plate", 2)], "Pure Carbon", deps=["t7_nasa"], xp=75,
      subtitle="Coal, with everything else spun out", desc=[
        "&eWhat:&r carbon plates hold each qubit.",
        "&eChemistry:&r coal is carbon plus hydrogen, sulfur and ash. The Centrifuge spins the rest away.",
        "&eHow:&r Centrifuge: 1 coal dust → 1 carbon dust. Compressor: carbon dust → carbon plate."]),
    Q("t7_tritium", 0, 0, [item(MI + "tritium_bucket")], "Tritium", deps=["t6_mi_reactor"], xp=200,
      subtitle="Hydrogen with two neutrons", desc=[
        "&eWhat:&r every qubit needs 50 mB of tritium.",
        "&eChemistry:&r tritium (³H) is radioactive, with a half-life of about 12 years. Real tritium is bred in reactors by hitting lithium or deuterium with neutrons.",
        "&eHow:&r Centrifuge: 1000 mB hydrogen → 20 mB deuterium + 1 mB tritium. That's slow; the Nuclear Reactor turns fluids in its fluid hatches into heavier isotopes much faster (check JEI under the reactor)."]),
    Q("t7_qubit", 0, 0, [item(MI + "qubit", 2)], "Qubits", deps=["t7_superconductor", "t7_carbon", "t7_tritium"], xp=300,
      subtitle="A bit that is both until you look", desc=[
        "&eWhat:&r the core of a quantum circuit.",
        "&eChemistry:&r a qubit holds a superposition of 0 and 1. Real ones are superconducting loops kept a hair above absolute zero, which is why yours needs cryofluid.",
        "&eHow:&r Assembler: 2 arithmetic logic units, 2 carbon plates, 2 glass panes, 6 superconductor wire, 250 mB cryofluid and 50 mB tritium."]),
    Q("t7_pu_battery", 0, 0, [item(MI + "plutonium_battery", 2)], "Plutonium Battery", deps=["t7_superconductor", "t6_mi_plutonium"], xp=250,
      subtitle="Power from decay", desc=[
        "&eWhat:&r the quantum tier's battery: the circuit board and the quantum hull each take two.",
        "&eChemistry:&r radioisotope generators turn decay heat into electricity. The Voyager probes still run on plutonium-238, launched in 1977.",
        "&eHow:&r Assembler: a battery alloy plate, 4 battery alloy curved plates, 2 superconductor cable and 2 MI plutonium dust."]),
    Q("t7_he3", 0, 0, [item(MI + "helium_3_bucket")], "Helium-3", deps=["t6_monazite"], xp=200,
      subtitle="The rarest helium", desc=[
        "&eWhat:&r every quantum circuit board needs 50 mB of helium-3.",
        "&eChemistry:&r helium-3 has one neutron instead of two. Earth has almost none; the Moon's soil holds more, implanted by the solar wind.",
        "&eHow:&r Centrifuge: 1000 mB helium → 5 mB helium-3. That's 10 buckets of helium per board, so tap every helium source you have."]),
    Q("t7_qboard", 0, 0, [item(MI + "quantum_circuit_board")], "Quantum Circuit Board", deps=["t7_pu_battery", "t7_he3"], xp=300,
      subtitle="Superconductor, plutonium and iridium", desc=[
        "&eHow:&r Assembler: a processing unit board, 12 superconductor cable, 2 plutonium batteries, 6 iridium plates and 50 mB helium-3.",
        "&eTip:&r iridium comes from the Platinum Line's residue. Plan for 6 plates per board."]),
    Q("t7_quantum", 0, 0, [item(MI + "quantum_circuit")], "Quantum Circuit", deps=["t7_qboard", "t7_qubit"], xp=600, size=1.5, shape="hexagon",
      items=[(MI + "cooling_cell", 2)], subtitle="The IV circuit, and the Seed's last secret", desc=[
        "&6A thought that holds every answer until it is asked. This one you didn't remember. You built it.&r",
        "&eWhat:&r the top MI circuit. Each Antimatter Core needs one, so the Seed needs eight.",
        "&eHow:&r Assembler: 4 processing units, 2 cooling cells, 2 qubits and a quantum circuit board.",
        "&eTip:&r automate the whole line before you need eight. Cooling cells and helium-3 are the slow parts."]),
    Q("t7_opt_qhull", 0, 0, [item(MI + "quantum_machine_hull")], "Quantum Hull", deps=["t7_quantum"], xp=200,
      optional=True, tokens=2, subtitle="Optional: the IV machine hull", desc=[
        "&eWhat:&r the base of MI's fusion reactor, replicator and quantum machines (Creation chapter).",
        "&eHow:&r Assembler: a quantum machine casing, a quantum circuit, 2 plutonium batteries and 3 superconductor cable."]),
], links=[("t7_seed", 21, 0)])
