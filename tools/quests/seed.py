"""Quest chapter: seed (the finale). See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

The Seed of a New World sits in the centre; its ingredient lines run in from the left and right,
and the Antimatter Core line comes up from below. Recipe: pack/kubejs/server_scripts/phase4_chemistry.js
sections 3 (energy cores) and 4 (the 9x9 Seed recipe).
"""
from questlib import Q, Chapter, item, dim, tick, kill, anytag, MAIN, SIDE  # noqa: F401

MI = "modern_industrialization:"
MEK = "mekanism:"
PB = "{@pagebreak}"

CHAPTER = Chapter("seed", "The Seed of a New World", "kubejs:seed_of_a_new_world",
        ["Every tier in one 9x9 grid. The act of making a world."], MAIN, [
    # ---------------------------------------------------------------- opening
    Q("sd_intro", 0, -6, [tick()], "The Last Recipe", deps=["t7_nasa"], xp=200, size=1.5, shape="hexagon",
      subtitle="One grid, thirteen ingredients", desc=[
        "&6Now it comes back, what all of this was for. Not machines. A world.&r",
        "&eWhat:&r the Seed of a New World is the pack's final craft: a 9x9 Ultimate Table recipe that uses something from every tier you've climbed.",
        "&eHow:&r every ingredient has its own branch, from raw material to finished part, and each branch ends in a checklist quest with the exact count. Finish all eight checklists and the Ultimate Table, and the Seed opens.",
        "&eTip:&r you can start the cheap lines (coke, water, acids, plastic) right away. The Antimatter Cores at the bottom take the longest.",
        PB,
        "&eThe full recipe:&r 4 coke, 8 ChemLib water, 4 hydrogen, 4 hydrofluoric acid buckets, 8 sulfuric acid buckets, 12 polyethylene buckets, "
        "8 processing units, 4 stainless steel plates, 8 oganesson, 4 plutonium pellets, 4 polonium pellets, 4 Nether Stars, "
        "8 Antimatter Cores and 1 Dragon Egg. 81 slots, every one filled.",
        "&eWhy these:&r read them in order and they retell the climb: fire (coke), the elements (synthesized water), "
        "the Acid Age (sulfuric and hydrofluoric acid), the Oil Age, the machine ages, the atomic age, and the energy you learned to bottle at the end.",
        "&eWhere:&r the Extended Crafting Ultimate Table (9x9). JEI shows the layout; press U on the Seed."]),
    # ---------------------------------------------------------------- left: fire, water, hydrogen (y=-4)
    Q("sd_coke", -7, -5, [item(MI + "coke", 4)], "Coke", deps=["sd_intro"], section="Fire and Water", xp=100,
      tokens=1, subtitle="The fuel that started your steel", desc=[
        "&eWhat:&r the four corners of the Seed are coke, the first thing your coke oven ever made.",
        "&eChemistry:&r coke is coal baked without air. Heat drives off water, tar and coal gas, leaving a hard, porous lump that is mostly carbon.",
        "&eHow:&r any coke oven or MI Coke Oven. Four pieces.",
        "&eTip:&r it's fitting that the last recipe starts with the first fuel.",
        PB,
        "&eDeep dive: why coke, not coal?&r",
        "Raw coal is full of volatile hydrocarbons and sulfur. In a blast furnace they would boil off, foul the iron and choke the burden.",
        "Coking (about 1000 °C, no oxygen) cooks them out. What's left is strong enough to carry the weight of ore above it and burns hot and clean.",
        "In the furnace, coke does two jobs: it burns for heat, and its carbon monoxide strips oxygen from iron oxide: Fe₂O₃ + 3CO → 2Fe + 3CO₂."]),
    Q("sd_hydrogen", -9, -3, [item("chemlib:hydrogen", 12)], "Hydrogen, Element 1", deps=["sd_intro"], xp=100,
      tokens=1, subtitle="The simplest atom there is", desc=[
        "&eWhat:&r the Seed takes 4 hydrogen itself, and its 8 synthesized water need 16 more to build. Start with a dozen and keep the Dissolver running.",
        "&eChemistry:&r one proton and one electron. Hydrogen makes up about three quarters of all the ordinary matter in the universe by mass.",
        "&eHow:&r the Alchemistry Dissolver breaks ChemLib water into 2 hydrogen + 1 oxygen. Other compounds give hydrogen too (check JEI).",
        "&eTip:&r it's the same element you used for the Potion of Flying back in Chapter II.",
        PB,
        "&eDeep dive: the first element&r",
        "Almost all the hydrogen in existence was made in the first few minutes after the Big Bang. Every other element was built from it later, inside stars.",
        "Stars fuse hydrogen into helium. Bigger stars go on to carbon, oxygen and up to iron. Heavier elements need supernovae and neutron-star collisions.",
        "So hydrogen is the right place to start a new world: it's where the old one started too."]),
    Q("sd_water", -7, -3, [item("chemlib:water", 8)], "Synthesized Water", deps=["sd_hydrogen", "sd_oxygen"], xp=100,
      tokens=1, subtitle="H₂O, built one molecule at a time", desc=[
        "&eWhat:&r 8 ChemLib water, made from elements rather than scooped from a lake.",
        "&eChemistry:&r 2H₂ + O₂ → 2H₂O. The reaction releases a lot of energy: it's what powers a hydrogen fuel cell.",
        "&eHow:&r Alchemistry Combiner: 2 hydrogen + 1 oxygen → 1 water.",
        "&eTip:&r the Dissolver gives you the oxygen along with the hydrogen, so nothing is wasted.",
        PB,
        "&eDeep dive: why build water at all?&r",
        "You could pour a bucket. The point of the Seed is that every part of a world can be made from its elements, and water is the most important compound of all.",
        "Water's bent shape (104.5° between the two O-H bonds) makes it polar. That polarity is why it dissolves salts, why ice floats, and why it holds so much heat.",
        "No water, no life. It's on the Seed eight times."]),
    # ---------------------------------------------------------------- left: the Acid Age (y=0)
    Q("sd_sulfur", -9, 0, [item(MI + "sulfur_dust", 16)], "Sulfur", deps=["sd_intro"], section="The Acid Age", xp=100,
      tokens=1, subtitle="Brimstone, in quantity", desc=[
        "&eWhat:&r eight buckets of acid need 16 sulfur dust.",
        "&eChemistry:&r sulfur is a yellow non-metal. Most of the world's supply comes from scrubbing it out of oil and gas, much as you do in petrochemistry.",
        "&eHow:&r sulfuric purification of crude oil and fuels in the MI Chemical Reactor, or from ore processing byproducts (check JEI)."]),
    Q("sd_acid", -7, 0, [item(MI + "sulfuric_acid_bucket")], "The King of Chemicals", deps=["sd_sulfur", "sd_o2"], xp=150,
      tokens=1, subtitle="Sulfuric acid, one more time", desc=[
        "&eWhat:&r the acid that unlocked 5x ore processing. The Seed needs eight buckets.",
        "&eChemistry:&r S + O₂ → SO₂, then 2SO₂ + O₂ → 2SO₃, then SO₃ + H₂O → H₂SO₄. MI's Chemical Reactor does it in one step from sulfur, oxygen and water.",
        "&eHow:&r Chemical Reactor: 1 sulfur dust + 200 mB oxygen + 200 mB water → 500 mB sulfuric acid.",
        "&eTip:&r one reactor makes the full 8000 mB in a few minutes.",
        PB,
        "&eDeep dive: the Contact Process&r",
        "Industry makes sulfuric acid by the contact process. Burning sulfur gives SO₂; a vanadium(V) oxide catalyst at about 450 °C turns it into SO₃.",
        "SO₃ isn't simply added to water: the reaction is so violent it makes a mist of acid. It's absorbed into concentrated acid first (making oleum, H₂S₂O₇), then diluted.",
        "More sulfuric acid is made than any other chemical. A country's output of it was once used as a measure of its industrial strength."]),
    # ---------------------------------------------------------------- left: the Oil Age (y=4)
    Q("sd_ethylene", -9, 4, [item(MI + "ethylene_bucket")], "Ethylene", deps=["sd_cracked"], xp=100,
      tokens=1, subtitle="C₂H₄, the plastic monomer", desc=[
        "&eWhat:&r the feedstock for polyethylene. 12 buckets of plastic need about 8.6 buckets of ethylene.",
        "&eChemistry:&r ethylene has a carbon-carbon double bond. That bond is what lets thousands of molecules link into a chain.",
        "&eHow:&r steam-crack naphtha or light fuel and distil the result, or dehydrate ethanol in the Chemical Reactor (check JEI)."]),
    Q("sd_pe", -7, 4, [item(MI + "polyethylene_bucket")], "Polymerise", deps=["sd_ethylene", "sd_catalyst"], xp=150,
      tokens=1, subtitle="Many small molecules, one long chain", desc=[
        "&eWhat:&r the Seed uses 12 buckets of polyethylene, more than any other ingredient.",
        "&eChemistry:&r n C₂H₄ → (–CH₂–CH₂–)ₙ. The double bond opens and each monomer joins the next.",
        "&eHow:&r Chemical Reactor: 500 mB ethylene + a tiny pile of chromium (or lead) dust → 700 mB polyethylene.",
        "&eTip:&r the chromium is a catalyst in real life too (see the next page).",
        PB,
        "&eDeep dive: catalysts that make plastic&r",
        "Most of the world's high-density polyethylene is made with chromium catalysts (the Phillips process) or titanium-aluminium ones (Ziegler-Natta).",
        "The metal centre grabs an ethylene molecule and slots it into the growing chain, again and again. The result is a long, straight chain that packs tightly: strong, stiff plastic.",
        "Without a catalyst you need huge pressures and get a branched, softer plastic (LDPE). Same formula, different shape, different material."]),
    # ---------------------------------------------------------------- right: the machine ages (y=-4)
    Q("sd_unit", 7, -5, [item(MI + "processing_unit", 8)], "Eight Processing Units", deps=["sd_pu_board", "sd_chipset", "sd_digital"], xp=150,
      tokens=1, subtitle="The EV brain, eight times over", desc=[
        "&eWhat:&r processing units are MI's EV circuits. The Seed takes eight, and each Energy Core needs one more.",
        "&eChemistry:&r they're built on PVC boards. PVC is polyethylene with a chlorine atom on every other carbon, which makes it harder and flame-resistant.",
        "&eHow:&r MI Assembler (check JEI). Queue sixteen: eight for the Seed and eight for the cores.",
        "&eTip:&r processing units are slow. Start them first and let them run while you do the other lines."]),
    Q("sd_stainless", 7, -3, [item(MI + "stainless_steel_plate", 36)], "Stainless Steel", deps=["sd_ss_ingot"], xp=150,
      tokens=1, subtitle="Steel that guards itself", desc=[
        "&eWhat:&r 4 plates for the Seed itself and 4 for each of the 8 Energy Core shells: 36 in all.",
        "&eChemistry:&r stainless steel is iron with at least 10.5% chromium, often with nickel. The chromium forms a thin Cr₂O₃ film that heals itself when scratched.",
        "&eHow:&r plates from stainless steel ingots in the Compressor. Ingots from the Electric Blast Furnace (check JEI).",
        PB,
        "&eDeep dive: passivation&r",
        "Ordinary iron rusts because its oxide flakes off and exposes fresh metal. Chromium oxide does the opposite: it's a dense layer a few nanometres thick that sticks.",
        "Scratch it and the exposed chromium reacts with oxygen in the air and seals the gap within moments. That's why stainless steel stays shiny.",
        "Nickel keeps the steel in its austenite form at room temperature: tough, non-magnetic and easy to work."]),
    # ---------------------------------------------------------------- right: the atomic age (y=0)
    Q("sd_oganesson", 7, -1, [item("chemlib:oganesson", 8)], "Oganesson ×8", deps=["sd_intro", "t6_table"], xp=250,
      tokens=1, subtitle="Element 118, eight times", desc=[
        "&eWhat:&r the last element on the periodic table. You made one to finish the table; the Seed wants eight.",
        "&eChemistry:&r oganesson-294 has a half-life of under a millisecond. Only a handful of atoms have ever been made.",
        "&eHow:&r Alchemistry Fusion Chamber: fuse two elements whose atomic numbers add up to 118 (check JEI for the pairs).",
        "&eTip:&r automate the inputs. Eight by hand is a long afternoon.",
        PB,
        "&eDeep dive: making element 118&r",
        "In 2002 a team in Dubna, Russia fired calcium-48 ions (20 protons) at a californium-249 target (98 protons). 20 + 98 = 118.",
        "Over months of beam time they saw about three atoms. Each decayed by alpha emission within a millisecond, into livermorium (116).",
        "It sits in the noble gas column, but it may not behave like one: its electrons move so fast that relativity smears out its shells. Your Fusion Chamber does the same addition, rather more reliably."]),
    Q("sd_plutonium", 7, 1, [item(MEK + "pellet_plutonium", 4)], "Plutonium Pellets", deps=["sd_fluorite_dust"], xp=200,
      tokens=1, subtitle="Element 94, from your reactor's waste", desc=[
        "&eWhat:&r four plutonium pellets for the Seed.",
        "&eChemistry:&r uranium-238 in a reactor captures a neutron and decays twice: U-238 → U-239 → Np-239 → Pu-239.",
        "&eHow:&r Mekanism: nuclear waste → Isotopic Centrifuge → plutonium → Chemical Crystallizer → pellet.",
        "&eTip:&r a running fission reactor makes waste whether you want it or not. This is a good use for it."]),
    Q("sd_polonium", 9, 0, [item(MEK + "pellet_polonium", 36)], "Polonium Pellets", deps=["sd_fluorite_dust"], xp=250,
      tokens=1, subtitle="Element 84, in bulk", desc=[
        "&eWhat:&r 4 pellets for the Seed and 4 for each of the 8 Energy Core shells: 36 in all. Polonium also feeds the SPS that makes antimatter.",
        "&eChemistry:&r Marie and Pierre Curie found polonium in 1898 and named it after Poland. Po-210 is so radioactive that a gram of it glows from its own heat.",
        "&eHow:&r Mekanism: nuclear waste → Solar Neutron Activator → polonium → Chemical Crystallizer → pellet.",
        "&eTip:&r activators only work in daylight. Build a row of them, not one."]),
    # ---------------------------------------------------------------- right: trophies (y=4)
    Q("sd_wither", 7, 3, [kill("minecraft:wither", 1)], "The Wither", deps=["sd_skulls"], xp=300, loot="boss",
      subtitle="Four stars means four fights", desc=[
        "&eWhat:&r every Nether Star comes from a Wither. The Seed needs four.",
        "&eHow:&r soul sand T-shape, three wither skeleton skulls on top. Fight it somewhere you don't mind losing.",
        "&eTip:&r fight it underground or in a sealed box so it can't fly off, and bring milk for the wither effect."]),
    Q("sd_dragon", 7, 5, [kill("minecraft:ender_dragon", 1)], "The Dragon", deps=["sd_end"], xp=300, loot="boss",
      subtitle="The egg sits at the very centre", desc=[
        "&eWhat:&r the Dragon Egg is the Seed's centre slot.",
        "&eHow:&r kill the Ender Dragon. The egg appears on top of the exit portal. Push it off with a piston or knock it onto a torch; clicking it makes it teleport.",
        "&eTip:&r if someone on the server already took the egg, there's another way. Look into the Antiprotonic Nucleosynthesizer."]),
    # ---------------------------------------------------------------- bottom: the Antimatter Core line
    Q("sd_pellets", -2, 10, [item(MEK + "pellet_antimatter", 32)], "Thirty-Two Antimatter Pellets", deps=["sd_first_antimatter"], xp=400,
      subtitle="The bulk of the work", desc=[
        "&eWhat:&r each Antimatter Core takes 4 antimatter pellets, so eight cores need 32.",
        "&eChemistry:&r an antiproton has the proton's mass and the opposite charge. When one meets a proton both vanish into energy (and a spray of lighter particles).",
        "&eHow:&r SPS → antimatter gas → Chemical Crystallizer. Keep both running non-stop.",
        "&eTip:&r a second SPS halves the wait, if you can feed it the polonium and the power.",
        PB,
        "&eDeep dive: how much energy?&r",
        "E = mc². Annihilating 1 gram of antimatter with 1 gram of matter releases about 1.8 × 10¹⁴ J, roughly the energy of a 43-kiloton explosion.",
        "Real labs (CERN's Antiproton Decelerator) have made only nanograms in decades, and keep them for minutes at most in magnetic traps.",
        "Your SPS is far kinder than physics, but it still asks for a lot of power. That's the price of reversing every charge in an atom."]),
    Q("sd_quantum", 2, 10, [item(MI + "quantum_circuit", 8)], "Eight Quantum Circuits", deps=["sd_qparts"], xp=400,
      subtitle="One for every core", desc=[
        "&eWhat:&r MI's top circuit. Each Antimatter Core needs one.",
        "&eHow:&r MI Assembler (check JEI). Quantum circuit boards come first.",
        "&eTip:&r quantum circuits also build the fusion reactor and the quantum armour in the Creation chapter. Make spares."]),
    Q("sd_cores2", 0, 8, [item("kubejs:antimatter_core", 2)], "Two Cores", deps=["t7_cores", "sd_charged", "sd_pellets", "sd_quantum"], xp=400,
      tokens=1, subtitle="A production line, not a one-off", desc=[
        "&eWhat:&r you've made one Antimatter Core. Make it two.",
        "&eHow:&r Empty Energy Core (4 stainless plates, 4 polonium pellets, 1 processing unit) → MI Assembler at 512 EU/t to charge it → MI Assembler at 2048 EU/t with 4 antimatter pellets and 1 quantum circuit.",
        "&eTip:&r two assemblers, one for each step, let the cores flow without you."]),
    Q("sd_cores4", 0, 6, [item("kubejs:antimatter_core", 4)], "Four Cores", deps=["sd_cores2"], xp=500,
      tokens=1, subtitle="Halfway to eight", desc=[
        "&eWhat:&r four Antimatter Cores. The Seed's diamond of power is half built.",
        "&eHow:&r keep the line running. Each core is about 3 million EU to charge and 12 million more to upgrade.",
        "&eTip:&r if your network sags while the assemblers run, give them their own generator.",
        PB,
        "&eDeep dive: the energy budget&r",
        "Charging: 512 EU/t × 6000 ticks = about 3.1 million EU. Upgrading: 2048 EU/t × 6000 ticks = about 12.3 million EU.",
        "That's about 15 million EU per core, or about 123 million EU for all eight, before counting the SPS that makes the antimatter.",
        "A fission reactor with a turbine, or a Mekanism fusion reactor, makes this a matter of hours. A wall of solar panels makes it a matter of weeks."]),
    # ---------------------------------------------------------------- the checklist (moved from t7)
    Q("t7_seed_basics", -4, -4, [item(MI + "coke", 4), item("chemlib:water", 8), item("chemlib:hydrogen", 4)], "Fire, Water and Hydrogen",
      deps=["sd_coke", "sd_water", "sd_hydrogen"], xp=200,
      subtitle="Seed checklist: where it all began", desc=[
        "&eWhat:&r the Seed's corners and outer ring hold the first things you learned: coke from your coke oven, and water synthesized from its elements.",
        "&eHow:&r 4 coke, 8 ChemLib water (Combiner: 2 hydrogen + 1 oxygen each) and 4 hydrogen, all held at once.",
        "&eTip:&r both are cheap now. Make spares."]),
    Q("t7_seed_acid", -4, 0, [anytag("warbucks:sulfuric_acid_buckets", 8)], "Eight Buckets of Acid", deps=["sd_acid"], xp=200,
      subtitle="Seed checklist: the Acid Age", desc=[
        "&eWhat:&r 8 buckets of sulfuric acid, the chemical that unlocked 5x ore processing.",
        "&eHow:&r fill buckets from your sulfuric acid tanks. MI, Mekanism and ChemLib acid buckets all count, in any mix.",
        "&eTip:&r buckets don't stack. Clear inventory space first, or keep them in a backpack."]),
    Q("t7_seed_hf", -4, 2, [item(MEK + "hydrofluoric_acid_bucket", 4)], "Four Buckets of HF", deps=["sd_hf", "t6_hf"], xp=200,
      subtitle="Seed checklist: the acid that eats glass", desc=[
        "&eWhat:&r 4 buckets of hydrofluoric acid, the acid that opened the road to nuclear fuel.",
        "&eChemistry:&r CaF₂ + H₂SO₄ → CaSO₄ + 2HF. HF is a weak acid by strength, yet it etches glass and soaks through skin: fluoride grabs silicon and calcium.",
        "&eHow:&r Chemical Dissolution Chamber: fluorite + sulfuric acid → HF gas. A Rotary Condensentrator in liquid mode turns the gas into fluid; fill buckets from it.",
        "&eTip:&r never store HF in glass, in real life. In game, a Mekanism fluid tank is fine."]),
    Q("t7_seed_pe", -4, 4, [item(MI + "polyethylene_bucket", 12)], "Twelve Buckets of Plastic", deps=["sd_pe"], xp=200,
      subtitle="Seed checklist: the Oil Age", desc=[
        "&eWhat:&r 12 buckets of polyethylene, the most of any ingredient.",
        "&eHow:&r polymerise ethylene in the Chemical Reactor, as in Petrochemistry.",
        "&eTip:&r fill them straight from your polymerisation reactor's output."]),
    Q("t7_seed_tech", 4, -4, [item(MI + "processing_unit", 8), item(MI + "stainless_steel_plate", 4)], "Circuits and Steel",
      deps=["sd_unit", "sd_stainless"], xp=200,
      subtitle="Seed checklist: the machine ages", desc=[
        "&eWhat:&r 8 processing units and 4 stainless steel plates.",
        "&eHow:&r both come from lines you already run. Keep these apart from the ones meant for Energy Cores.",
        "&eTip:&r processing units are slow to make, so start these early."]),
    Q("t7_seed_nuclear", 4, 0, [item("chemlib:oganesson", 8), item(MEK + "pellet_plutonium", 4), item(MEK + "pellet_polonium", 4)], "Heavy Elements",
      deps=["sd_oganesson", "sd_plutonium", "sd_polonium"], xp=300,
      subtitle="Seed checklist: the atomic age", desc=[
        "&eWhat:&r 8 oganesson, 4 plutonium pellets and 4 polonium pellets.",
        "&eHow:&r oganesson from the Fusion Chamber; pellets from your reactor's waste.",
        "&eTip:&r keep 4 polonium pellets aside. The core shells will happily eat them all."]),
    Q("t7_seed_stars", 4, 4, [item("minecraft:nether_star", 4), item("minecraft:dragon_egg")], "Stars and an Egg", deps=["sd_stars", "sd_dragon"], xp=300,
      subtitle="Seed checklist: trophies of the old world", desc=[
        "&eWhat:&r 4 Nether Stars, and the Dragon Egg at the very centre.",
        "&eHow:&r defeat the Wither four times; kill the Ender Dragon for the egg.",
        "&eTip:&r on a server, agree who crafts the Seed before anyone grabs the egg."]),
    Q("t7_seed_cores", 0, 4, [item("kubejs:antimatter_core", 8)], "Eight Antimatter Cores", deps=["sd_cores4"], xp=500, size=1.25,
      subtitle="Seed checklist: the hardest part", desc=[
        "&eWhat:&r eight Antimatter Cores ring the centre of the recipe.",
        "&eHow:&r that's 32 antimatter pellets, 32 polonium pellets, 32 stainless plates, 8 processing units and 8 quantum circuits in total.",
        "&6Eight suns in your pack. You have carried heavier things.&r"]),
    Q("t7_seed", 0, 0, [item("kubejs:seed_of_a_new_world")], "Seed of a New World",
      deps=["mf_ult_table", "sd_ult_catalyst", "t7_seed_basics", "t7_seed_acid", "t7_seed_hf", "t7_seed_pe", "t7_seed_cores", "t7_seed_tech", "t7_seed_nuclear", "t7_seed_stars"],
      xp=3000, size=2.0, shape="hexagon", subtitle="The endgame goal", desc=[
        "&6Every lesson, in one 9x9 grid. You hold it, and it holds a world.&r",
        "&eWhat:&r a recipe on the Ultimate Table that needs something from every tier.",
        "&eHow:&r 4 coke, 8 water, 4 hydrogen, 4 hydrofluoric acid, 8 sulfuric acid, 12 polyethylene, 8 processing units, 4 stainless plates, 8 oganesson, 4 plutonium, 4 polonium, 4 Nether Stars, 8 Antimatter Cores, and the Dragon Egg at the centre.",
        "&eTip:&r check JEI for the exact layout before you fill the table. One wrong slot and nothing happens.",
        PB,
        "&eDeep dive: reading the grid&r",
        "The pattern is symmetrical in every direction. Coke holds the four corners. Water and sulfuric acid line the outer ring, with hydrofluoric acid tucked just inside each corner. Plastic forms crosses on all four sides.",
        "Stainless steel and processing units make an inner square. Oganesson, plutonium and Nether Stars sit closer in. Eight Antimatter Cores form a diamond around the centre.",
        "And in the middle, one Dragon Egg: the only thing in the old world that was already a seed of something new."]),
    # ---------------------------------------------------------------- optional / secret
    Q("sd_opt_auto", 0, -8, [item("extendedcrafting:ultimate_auto_table")], "Ultimate Auto Table", deps=["sd_intro", "mf_ult_table"], xp=150,
      optional=True, tokens=2, subtitle="Optional: let the table fill itself", desc=[
        "&eWhat:&r an auto-crafting version of the Ultimate Table. Set the recipe once, then pipe the ingredients in.",
        "&eHow:&r check JEI for the recipe. It needs power to craft.",
        "&eTip:&r useful if your team wants a second Seed, or for the other 9x9 recipes in the pack."]),
    Q("sd_opt_ledger", 2, -8, [tick()], "The Bill of Materials", deps=["sd_intro"], xp=50,
      optional=True, tokens=1, subtitle="Optional: everything, counted from scratch", desc=[
        "&eWhat:&r a shopping list for the whole Seed, Energy Cores included.",
        "&eHow:&r read the next page, then tick this quest.",
        PB,
        "&eSeed only:&r 4 coke, 8 water, 4 hydrogen, 4 hydrofluoric acid buckets, 8 sulfuric acid buckets, 12 polyethylene buckets, 8 processing units, 4 stainless plates, 8 oganesson, 4 plutonium pellets, 4 polonium pellets, 4 Nether Stars, 1 Dragon Egg.",
        "&eEight cores:&r 32 stainless plates, 32 polonium pellets, 8 processing units, 32 antimatter pellets, 8 quantum circuits, about 123 million EU.",
        "&eGrand total:&r 36 stainless plates, 36 polonium pellets, 16 processing units, 32 antimatter pellets, 8 quantum circuits, plus everything above.",
        "&eIn raw terms:&r 16 sulfur dust for the acid, 20 hydrogen (16 for the water, 4 as is) and 8 oxygen, fluorite and a little more sulfuric acid for the HF, about 8.6 buckets of ethylene."]),
    Q("sd_opt_wither4", 9, 3, [kill("minecraft:wither", 4)], "Four Withers", deps=["sd_wither"], xp=300,
      optional=True, tokens=2, loot="boss", subtitle="Optional: one for every star", desc=[
        "&eWhat:&r kill the Wither four times, once for each Nether Star in the Seed.",
        "&eHow:&r a wither skeleton farm makes the skulls easy. Fight in a sealed bunker each time.",
        "&eTip:&r Looting on your sword raises the skull drop chance from wither skeletons."]),
    Q("sd_secret_egg", 9, 5, [item("minecraft:dragon_egg", 2)], "A Second Egg", deps=["sd_dragon"], xp=200,
      secret=True, loot="secret", tokens=2, subtitle="Secret: a chicken egg, rewritten", desc=[
        "&eWhat:&r you found it: the Antiprotonic Nucleosynthesizer turns an ordinary egg into a Dragon Egg with a little antimatter.",
        "&eChemistry:&r nucleosynthesis means building heavier nuclei from lighter ones. Stars do it slowly. Mekanism does it with an egg and 4 mB of antimatter.",
        "&eTip:&r now every player on the server can have a Seed of their own."]),

    # ===== the Seed's component tree (ATM10-style detail pass, 2026-10-19) =====
    # --- fire and water
    Q("sd_oxygen", 0, 0, [item("chemlib:oxygen", 8)], "Oxygen, Element 8", deps=["sd_intro"], xp=80,
      subtitle="One atom in every water molecule", desc=[
        "&eWhat:&r 8 ChemLib oxygen, one for each of the Seed's 8 synthesized waters.",
        "&eChemistry:&r oxygen is 89% of water by mass, even though water has twice as many hydrogen atoms. Oxygen atoms are 16 times heavier.",
        "&eHow:&r the Alchemistry Dissolver gives oxygen along with hydrogen when it breaks down water and many other compounds."]),
    # --- the acid age
    Q("sd_o2", 0, 0, [item(MI + "oxygen_bucket")], "Oxygen for the Reactor", deps=["sd_intro"], xp=60,
      subtitle="MI oxygen, by the bucket", desc=[
        "&eWhat:&r the Chemical Reactor's acid recipe burns sulfur in MI oxygen: 200 mB per 500 mB of acid, so 3200 mB for eight buckets.",
        "&eHow:&r Electrolyzer (water) or the Centrifuge (liquid air). Fill one bucket to prove the line runs."]),
    Q("sd_fluorite", 0, 0, [item(MEK + "fluorite_gem", 4)], "Fluorite for HF", deps=["sd_intro"], xp=80,
      subtitle="Four gems, four buckets", desc=[
        "&eWhat:&r one fluorite gem dissolves into 1000 mB of HF, so four gems fill the Seed's four HF buckets.",
        "&eChemistry:&r CaF₂ + H₂SO₄ → CaSO₄ + 2HF. Sulfuric acid is stronger and less volatile, so it pushes the hydrogen fluoride out of the mineral.",
        "&eHow:&r mine fluorite ore deep down; the Enrichment Chamber turns its dust into gems."]),
    Q("sd_hf", 0, 0, [item(MEK + "hydrofluoric_acid_bucket")], "Hydrofluoric Acid", deps=["sd_fluorite", "sd_acid"], xp=100,
      subtitle="The acid that eats glass", desc=[
        "&eWhat:&r your first HF bucket for the Seed.",
        "&eHow:&r Chemical Dissolution Chamber: fluorite gem + sulfuric acid gas → HF gas. Rotary Condensentrator (liquid mode) → fluid → bucket.",
        "&eTip:&r three more and the checklist is done."]),
    # --- the oil age
    Q("sd_naphtha", 0, 0, [item(MI + "naphtha_bucket")], "Naphtha", deps=["sd_intro"], section="The Oil Age", xp=60,
      subtitle="Sweet naphtha, ready to crack", desc=[
        "&eWhat:&r the start of the plastic branch: 12 buckets of polyethylene trace back to about 34 buckets of naphtha.",
        "&eHow:&r Distillery (sour naphtha from crude), then hydrotreat it with hydrogen in the Chemical Reactor."]),
    Q("sd_cracked", 0, 0, [item(MI + "steam_cracked_naphtha_bucket")], "Cracked Naphtha", deps=["sd_naphtha"], xp=60,
      subtitle="Steam snaps the chains", desc=[
        "&eWhat:&r the mix that ethylene is distilled from.",
        "&eHow:&r Chemical Reactor: 1000 mB naphtha + 100 mB steam → 1000 mB steam-cracked naphtha."]),
    Q("sd_catalyst", 0, 0, [item(MI + "chromium_tiny_dust", 9)], "Chromium Catalyst", deps=["sd_intro"], xp=60,
      subtitle="A pinch for every half bucket", desc=[
        "&eWhat:&r one tiny chromium dust polymerises 500 mB of ethylene into 700 mB of polyethylene.",
        "&eHow:&r craft 1 chromium dust into 9 tiny dusts. That's most of the 18 runs the Seed's plastic needs; make a second dust."]),
    # --- the machine ages
    Q("sd_ss_dust", 0, 0, [item(MI + "stainless_steel_dust", 36)], "Stainless Dust", deps=["sd_intro"], section="The Machine Ages", xp=80,
      subtitle="Thirty-six plates start as powder", desc=[
        "&eWhat:&r 36 stainless steel plates (4 for the Seed, 32 for the core shells) start as 36 dusts.",
        "&eHow:&r Mixer: 6 iron + 1 chromium + 1 nickel + 1 manganese dust → 9 stainless dust. Four runs."]),
    Q("sd_ss_ingot", 0, 0, [item(MI + "stainless_steel_ingot", 36)], "Stainless Ingots", deps=["sd_ss_dust"], xp=80,
      subtitle="Melted, then frozen", desc=[
        "&eWhat:&r the ingots for the Seed's plates.",
        "&eHow:&r Electric Blast Furnace → hot ingot → Vacuum Freezer (or Heat Exchanger). Then Compressor → plates."]),
    Q("sd_pvc", 0, 0, [item(MI + "polyvinyl_chloride_bucket")], "PVC for the Boards", deps=["sd_intro"], xp=80,
      subtitle="1500 mB per board", desc=[
        "&eWhat:&r every processing unit board is laminated with 1500 mB of PVC. Sixteen units (8 for the Seed, 8 for the cores) need 24 buckets.",
        "&eHow:&r acetylene + HCl → vinyl chloride; polymerise with tiny chromium dust."]),
    Q("sd_platinum", 0, 0, [item(MI + "platinum_plate", 16)], "Platinum for the Boards", deps=["sd_intro"], xp=80,
      subtitle="Four plates a board", desc=[
        "&eWhat:&r 16 platinum plates: enough for the first four boards.",
        "&eHow:&r keep the Platinum Line (sludge → aqua regia → hexachloroplatinate → calcine) running the whole time you work on the Seed."]),
    Q("sd_pu_board", 0, 0, [item(MI + "processing_unit_board", 4)], "Processing Unit Boards", deps=["sd_pvc", "sd_platinum"], xp=100,
      subtitle="The first batch of four", desc=[
        "&eWhat:&r the base of every processing unit.",
        "&eHow:&r Assembler: digital circuit board, 4 platinum plates, 2 cadmium batteries, 8 annealed copper cable and 1500 mB PVC."]),
    Q("sd_chipset", 0, 0, [item(MI + "random_access_memory", 8), item(MI + "arithmetic_logic_unit", 4), item(MI + "memory_management_unit", 4)], "Chips by the Batch", deps=["sd_intro"], xp=100,
      subtitle="RAM, ALUs and MMUs for four units", desc=[
        "&eWhat:&r each processing unit takes 2 RAM, 1 ALU and 1 MMU. This is the set for four.",
        "&eHow:&r RAM in the Chemical Reactor (wafer, antimony, aluminium, argon, SBR); ALU and MMU in the Assembler.",
        "&eTip:&r one silicon boule is 32 wafers. That covers the RAM and MMUs for all sixteen units."]),
    Q("sd_digital", 0, 0, [item(MI + "digital_circuit", 16)], "Digital Circuits", deps=["sd_intro"], xp=100,
      subtitle="Four per processing unit", desc=[
        "&eWhat:&r 16 digital circuits, enough for four processing units.",
        "&eHow:&r Assembler: a digital circuit board, 4 electronic circuits, an AND, an OR and 2 NOT gates.",
        "&eTip:&r all sixteen units need 64. Put three Assemblers on this branch alone."]),
    # --- the atomic age
    Q("sd_fluorite_dust", 0, 0, [item(MEK + "dust_fluorite", 40)], "Fluorite for the Pellets", deps=["sd_intro"], section="The Atomic Age", xp=80,
      subtitle="One dust for every pellet", desc=[
        "&eWhat:&r 4 plutonium pellets and 36 polonium pellets need 40 fluorite dust.",
        "&eHow:&r Crusher: fluorite gem → dust. Occultism's crusher spirits give more per ore."]),
    # --- trophies
    Q("sd_skulls", 0, 0, [item("minecraft:wither_skeleton_skull", 3), item("minecraft:soul_sand", 4)], "Skulls and Soul Sand", deps=["sd_intro"], section="Trophies of the Old World", xp=100,
      subtitle="What it takes to summon a Wither", desc=[
        "&eWhat:&r one Wither's worth: 3 wither skeleton skulls and 4 soul sand.",
        "&eHow:&r wither skeletons in Nether fortresses drop skulls now and then; Looting helps. Soul sand is in Soul Sand Valleys."]),
    Q("sd_stars", 0, 0, [item("minecraft:nether_star", 4)], "Four Nether Stars", deps=["sd_wither"], xp=200,
      subtitle="One for every arm of the cross", desc=[
        "&eWhat:&r the Seed's four Nether Stars, held at once.",
        "&eHow:&r four Withers. Each drops one star.",
        "&eTip:&r the Fusion Chamber already ate one star. These four are for the Seed alone."]),
    Q("sd_eyes", 0, 0, [item("minecraft:ender_eye", 12)], "Eyes of Ender", deps=["sd_intro"], xp=80,
      subtitle="Find the stronghold, fill the frame", desc=[
        "&eWhat:&r enough eyes to find a stronghold and light its portal.",
        "&eHow:&r ender pearl + blaze powder. Throw one and follow it; it flies toward the nearest stronghold."]),
    Q("sd_end", 0, 0, [dim("minecraft:the_end")], "The End", deps=["sd_eyes"], xp=150,
      subtitle="Step through the portal", desc=[
        "&eWhat:&r the dragon's island.",
        "&eTip:&r bring blocks, a bow and slow-falling potions. Flight makes the crystal towers far easier."]),
    # --- eight suns
    Q("sd_shells", 0, 0, [item("kubejs:energy_core_empty", 2)], "Core Shells", deps=["sd_stainless", "sd_polonium", "sd_unit"], section="Eight Suns", xp=150,
      subtitle="Stainless, polonium and a processing unit", desc=[
        "&eWhat:&r empty Energy Cores, the first stage of every Antimatter Core.",
        "&eHow:&r crafting table: 4 stainless steel plates around a processing unit, with 4 polonium pellets."]),
    Q("sd_charged", 0, 0, [item("kubejs:energy_core", 2)], "Charged Cores", deps=["sd_shells"], xp=200,
      subtitle="Three million EU each", desc=[
        "&eWhat:&r Energy Cores filled with raw electrical energy.",
        "&eHow:&r MI Assembler at 512 EU/t for 6000 ticks per core.",
        "&eTip:&r a core takes five minutes to charge. A second Assembler doubles the pace."]),
    Q("sd_first_antimatter", 0, 0, [item(MEK + "pellet_antimatter", 8)], "Eight Pellets", deps=["sd_intro", "t7_antimatter"], xp=200,
      subtitle="Two cores' worth of antimatter", desc=[
        "&eWhat:&r the first quarter of the 32 antimatter pellets.",
        "&eHow:&r SPS → antimatter gas → Chemical Crystallizer, 1000 mB per pellet.",
        "&eTip:&r if the SPS stalls, it's usually power or polonium. Watch both."]),
    Q("sd_qparts", 0, 0, [item(MI + "quantum_circuit_board", 2), item(MI + "qubit", 4)], "Boards and Qubits", deps=["sd_intro", "t7_quantum"], xp=200,
      subtitle="Two quantum circuits' worth", desc=[
        "&eWhat:&r each quantum circuit is a board, 2 qubits, 2 cooling cells and 4 processing units.",
        "&eHow:&r Assembler. The boards wait on helium-3 and iridium plates; the qubits on tritium and cryofluid.",
        "&eTip:&r eight circuits need 8 boards and 16 qubits. Keep the helium-3 centrifuges running."]),
    # --- the ultimate table
    Q("sd_ult_component", 0, 0, [item("extendedcrafting:ultimate_component", 8)], "Ultimate Components", deps=["sd_intro"], section="The Ultimate Table", xp=100,
      subtitle="Black iron, luminessence and emerald", desc=[
        "&eWhat:&r the 9x9 table needs 4 components and a catalyst made of 4 more.",
        "&eHow:&r a black iron slate, luminessence and 2 emeralds each (crafting table)."]),
    Q("sd_ult_catalyst", 0, 0, [item("extendedcrafting:ultimate_catalyst")], "Ultimate Catalyst", deps=["sd_ult_component"], xp=100,
      subtitle="The table's focus", desc=[
        "&eWhat:&r the centre of the Ultimate Table recipe.",
        "&eHow:&r 4 ultimate components around a black iron ingot. The table itself adds 2 elite tables, an emerald block and a processing unit (Monifactory page)."]),
], links=[("t7_antimatter", -4, 10), ("t7_cores", 4, 8), ("mf_ult_table", -2, -8)])
