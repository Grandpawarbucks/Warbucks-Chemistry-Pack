"""Quest chapter: t6. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

MI = "modern_industrialization:"
MEK = "mekanism:"
GEN = "mekanismgenerators:"

CHAPTER = Chapter("t6", "VII. Materials and Nuclear", "mekanism:pellet_polonium",
        ["Purity and precision: semiconductors, PVC, isotopes.",
         "Then transmutation: any element from any other."], MAIN, [
    # ---------------------------------------------------------------- silicon
    Q("t6_argon", 2, -4, [item(MI + "argon_bucket")], "Argon from Air", deps=["t5_hv"], xp=150,
      subtitle="The lazy gas that protects hot silicon", desc=[
        "&6You once stirred the sky. Now you pour it, liquid, into a tank.&r",
        "&eWhat:&r argon is an inert blanket gas. Growing a silicon crystal in air would ruin it.",
        "&eChemistry:&r air is 78% N₂, 21% O₂ and about 0.9% argon. Cool it until it liquefies, then separate the parts.",
        "&eHow:&r the Vacuum Freezer (or Pressurizer) with an Air Intake makes liquid air. The Centrifuge splits it into oxygen, nitrogen and a little argon.",
        "&eTip:&r the Heat Exchanger gives far more argon while it cools hot ingots."]),
    Q("t6_silicon", 4, -4, [item(MI + "monocrystalline_silicon"), item(MI + "silicon_wafer", 4)], "Semiconductor Silicon", deps=["t6_argon"], xp=250,
      subtitle="One perfect crystal, sliced thin", desc=[
        "&eWhat:&r computer chips need silicon purer than 99.9999999%, grown as one single crystal.",
        "&eChemistry:&r a seed crystal is pulled slowly out of molten silicon (the Czochralski process). Every atom lines up with the one below it.",
        "&eHow:&r EBF: 32 silicon dust + 1 tiny iridium dust + argon → monocrystalline silicon. Cut it into wafers with lubricant.",
        "&eTip:&r iridium comes from osmium byproducts or the platinum line's residue (below)."]),
    Q("t6_chips", 6, -4, [item(MI + "random_access_memory", 2), item(MI + "arithmetic_logic_unit"), item(MI + "memory_management_unit")], "Chips", deps=["t6_silicon"], xp=200,
      subtitle="Memory, logic and control on silicon", desc=[
        "&eWhat:&r a processing unit needs RAM, an ALU and an MMU.",
        "&eChemistry:&r a pinch of aluminum (p-type) or phosphorus (n-type) in silicon changes how it carries current. That's 'doping', the basis of every transistor.",
        "&eHow:&r Assembler. The ALU uses a diamond plate and logic gates, the MMU silicon wafers and platinum fine wire. Check JEI for RAM."]),
    # ---------------------------------------------------------------- PVC
    Q("t6_acetylene", 2, -2, [item(MI + "acetylene_bucket")], "Acetylene", deps=["t5_hv"], xp=150,
      subtitle="The welding gas, from methane", desc=[
        "&eWhat:&r acetylene (C₂H₂) has a triple bond, which makes it very reactive.",
        "&eChemistry:&r heat methane hard enough and pairs of molecules lose hydrogen and join: 2CH₄ → C₂H₂ + 3H₂.",
        "&eHow:&r Electric Blast Furnace: 200 mB methane → 200 mB acetylene. Cracked naphtha also gives a little."]),
    Q("t6_vinyl", 4, -2, [item(MI + "vinyl_chloride_bucket")], "Vinyl Chloride", deps=["t6_acetylene", "t4_salt"], xp=150,
      subtitle="Acetylene meets hydrochloric acid", desc=[
        "&eChemistry:&r C₂H₂ + HCl → C₂H₃Cl. HCl adds across the triple bond. This was the original industrial route to PVC.",
        "&eHow:&r Chemical Reactor: 1 B acetylene + 1 B hydrochloric acid → 1 B vinyl chloride.",
        "&eTip:&r your salt line's chlorine and hydrogen make the HCl."]),
    Q("t6_pvc", 6, -2, [item(MI + "polyvinyl_chloride_bucket")], "PVC", deps=["t6_vinyl"], xp=250,
      subtitle="Petrochemistry meets chlor-alkali", desc=[
        "&eWhat:&r polyvinyl chloride, (C₂H₃Cl)ₙ, is tough, fire-resistant and insulates EV circuit boards.",
        "&eChemistry:&r just like polyethylene, but every other carbon carries a chlorine atom. That's why PVC doesn't burn easily.",
        "&eHow:&r Chemical Reactor: 500 mB vinyl chloride + 4 tiny lead or chromium dust → 300 mB PVC."]),
    # ---------------------------------------------------------------- EV
    Q("t6_cadmium", 4, 0, [item(MI + "cadmium_dust", 4), item(MI + "cadmium_battery", 2)], "Cadmium Battery", deps=["t5_hv"], xp=200,
      subtitle="Nickel-cadmium cells for the EV hull", desc=[
        "&eWhat:&r the EV hull and processing unit board each need 2 cadmium batteries.",
        "&eChemistry:&r a NiCd cell runs Cd + 2NiO(OH) + 2H₂O → Cd(OH)₂ + 2Ni(OH)₂, and it can be recharged by running it backwards.",
        "&eHow:&r MI centrifuges monazite dust into cadmium (in reality, it's mostly a by-product of zinc refining). Then craft the battery with annealed copper cable.",
        "&eTip:&r cadmium is toxic in real life. Here it just needs a lot of monazite."]),
    Q("t6_board", 8, -1, [item(MI + "processing_unit_board")], "Processing Unit Board", deps=["t6_pvc", "t6_cadmium"], xp=200,
      subtitle="PVC, platinum and cadmium in one board", desc=[
        "&eHow:&r Assembler: digital circuit board + 4 platinum plates + 2 cadmium batteries + 8 annealed copper cable + 1500 mB PVC.",
        "&eChemistry:&r platinum never corrodes, so it makes contacts that last forever.",
        "&eTip:&r platinum comes from MI's ore processing or the Platinum Line below (check JEI)."]),
    Q("t6_pu", 10, -2, [item(MI + "processing_unit"), item(MI + "highly_advanced_machine_hull")], "EV: Processing Units", deps=["t6_board", "t6_chips"], xp=400, size=1.5,
      items=[(MI + "processing_unit", 2)], subtitle="Extreme Voltage, built on purity", desc=[
        "&6A mind of silicon, insulated in salt and oil. It thinks the way you used to.&r",
        "&eWhat:&r processing units unlock EV machines, the NASA Workbench, Flux Networks and Alchemistry's chambers.",
        "&eHow:&r Assembler: processing unit board + 4 digital circuits + 2 RAM + ALU + MMU. The &eEV hull&r adds 2 cadmium batteries."]),
    # ---------------------------------------------------------------- nuclear
    Q("t6_yellowcake", 12, -5, [item(MEK + "yellow_cake_uranium", 4)], "Yellowcake", deps=["t6_pu"], xp=150,
      subtitle="The first step from ore to fuel", desc=[
        "&eWhat:&r yellowcake is concentrated uranium oxide powder, the raw material of nuclear fuel.",
        "&eChemistry:&r natural uranium is only 0.72% U-235, the isotope that splits. The rest is U-238.",
        "&eHow:&r Enrichment Chamber: 1 uranium ingot → 2 yellowcake. Then the Chemical Oxidizer turns it into uranium oxide gas.",
        "&eTip:&r a Geiger counter tells you when you're standing too close to anything radioactive."]),
    Q("t6_hf", 12, -7, [item(MEK + "fluorite_gem", 16)], "Hydrofluoric Acid", deps=["t6_pu"], xp=150,
      subtitle="The acid that eats glass", desc=[
        "&eChemistry:&r CaF₂ + H₂SO₄ → CaSO₄ + 2HF. Hydrogen fluoride dissolves glass and is one of the most dangerous acids there is.",
        "&eHow:&r Chemical Dissolution Chamber: fluorite + sulfuric acid → hydrofluoric acid gas.",
        "&eTip:&r fluorite ore sits deep. Mystical Agriculture and Occultism can't make it in this pack. Keep extra HF: the Seed of a New World needs 4 buckets (a Rotary Condensentrator in liquid mode turns the gas into fluid)."]),
    Q("t6_uf6", 14, -6, [item(MEK + "chemical_infuser"), item(MEK + "chemical_oxidizer")], "Uranium Hexafluoride", deps=["t6_yellowcake", "t6_hf"], xp=200,
      subtitle="Turn uranium into a gas", desc=[
        "&eWhat:&r UF₆ is the only uranium compound that becomes a gas at low temperature (it sublimes at 56 °C), so it can be spun.",
        "&eChemistry:&r real plants go UO₂ → UF₄ → UF₆ with HF and then fluorine. Mekanism combines the steps.",
        "&eHow:&r Chemical Infuser: uranium oxide + hydrofluoric acid → uranium hexafluoride."]),
    Q("t6_centrifuge", 16, -6, [item(MEK + "isotopic_centrifuge")], "Isotope Separation", deps=["t6_uf6"], xp=300,
      subtitle="Only mass tells U-235 and U-238 apart", desc=[
        "&eWhat:&r the two isotopes behave identically in every reaction, so chemistry can't separate them.",
        "&eChemistry:&r U-235 is about 1% lighter. Spin UF₆ fast enough and the heavier molecules drift outward.",
        "&eHow:&r Isotopic Centrifuge: uranium hexafluoride → fissile fuel."]),
    Q("t6_fission_parts", 18, -6, [item(GEN + "fission_fuel_assembly", 4), item(GEN + "control_rod_assembly"), item(GEN + "fission_reactor_port", 4)], "Reactor Parts", deps=["t6_centrifuge"], xp=250,
      subtitle="Fuel, control rods and ports", desc=[
        "&eWhat:&r fuel assemblies hold the fuel, control rods absorb neutrons, and ports move fuel, coolant and waste.",
        "&eChemistry:&r each split releases 2 to 3 neutrons. Absorb too few and the chain reaction runs away.",
        "&eHow:&r check JEI for each part. Plan for water or sodium coolant and somewhere for the steam to go."]),
    Q("t6_fission", 20, -6, [item(GEN + "fission_reactor_casing", 16)], "Fission", deps=["t6_fission_parts"], xp=400,
      subtitle="Split the atom", desc=[
        "&eWhat:&r split heavy nuclei and release enormous energy. Mind the temperature, and the waste.",
        "&eChemistry:&r U-235 + n → two lighter nuclei + 2-3 n + about 200 MeV, millions of times more than any chemical bond.",
        "&eHow:&r Just Enough Mekanism Multiblocks shows the layout in JEI. Pair it with a turbine (see Power).",
        "&eTip:&r wire a Logic Adapter to SCRAM the reactor if it overheats."]),
    Q("t6_plutonium", 22, -7, [item(MEK + "pellet_plutonium")], "Plutonium", deps=["t6_fission"], xp=250,
      subtitle="An element made by neutrons", desc=[
        "&eChemistry:&r U-238 captures a neutron and beta-decays twice into Pu-239, which is itself fissile.",
        "&eHow:&r Isotopic Centrifuge: 10 nuclear waste → 1 plutonium. Pressurized Reaction Chamber: plutonium + fluorite dust + water → pellet.",
        "&eTip:&r the pellet reaction also gives spent nuclear waste. Store it in a Radioactive Waste Barrel."]),
    Q("t6_polonium", 22, -5, [item(MEK + "solar_neutron_activator"), item(MEK + "pellet_polonium")], "Polonium", deps=["t6_fission"], xp=250,
      subtitle="The element Marie Curie named for Poland", desc=[
        "&eChemistry:&r polonium-210 is made by neutron capture; it is intensely radioactive and gives off heat on its own.",
        "&eHow:&r Solar Neutron Activator (needs open sky and daylight): 10 nuclear waste → 1 polonium. Pellets come from the Pressurized Reaction Chamber, as with plutonium.",
        "&eTip:&r polonium is the input for the SPS and for Energy Cores."]),
    Q("t6_waste", 24, -6, [item(MEK + "pellet_plutonium"), item(MEK + "pellet_polonium")], "Transmutation by Neutron", deps=["t6_plutonium", "t6_polonium"], xp=500, size=1.5,
      subtitle="Lead to gold was never the hard part", desc=[
        "&6The old alchemists wanted to change one element into another. You do it before breakfast.&r",
        "&eWhat:&r reprocessing nuclear waste gives &eplutonium&r and &epolonium&r, two elements that barely exist in nature.",
        "&eHow:&r keep both pellet lines running. Plutonium feeds the quantum tier; polonium feeds antimatter.",
        "&eTip:&r spent waste still goes in a Radioactive Waste Barrel. Never dump it."]),
    # ---------------------------------------------------------------- transmutation
    Q("t6_reactor_parts", 12, 0, [item("alchemistry:reactor_casing", 16), item("alchemistry:reactor_energy"), item("alchemistry:reactor_input"), item("alchemistry:reactor_output")],
      "Chamber Frame", deps=["t6_pu"], xp=200, subtitle="The shell around an element reactor", desc=[
        "&eWhat:&r Alchemistry's fission and fusion chambers share the same casing, energy, input and output blocks.",
        "&eHow:&r craft the frame blocks (check JEI) and build the chamber around its controller. The controllers themselves are crafted with a reactor casing.",
        "&eTip:&r build both chambers side by side so one can feed the other."]),
    Q("t6_chambers", 14, 0, [item("alchemistry:fission_chamber_controller"), item("alchemistry:fusion_chamber_controller")], "Element Transmutation", deps=["t6_reactor_parts"], xp=500, size=1.5,
      subtitle="Split or merge any element", desc=[
        "&eWhat:&r the fission chamber splits one element into two lighter ones; the fusion chamber merges two into a heavier one.",
        "&eChemistry:&r atomic numbers simply add or divide: fuse sodium (11) with chlorine (17) and you get nickel (28).",
        "&eHow:&r both controllers need a processing unit; fusion also needs a Nether Star.",
        "&eTip:&r with both, &eevery element&r is within reach."]),
    Q("t6_table", 16, 0, [item("chemlib:uranium", 16), item("chemlib:oganesson")], "The Complete Periodic Table", deps=["t6_chambers"], xp=1000, size=2.0, shape="gear",
      items=[("kubejs:energy_core_empty", 1)], subtitle="Element 118", desc=[
        "&6Oganesson. It barely exists in reality, but you made one.&r",
        "&eWhat:&r the heaviest element on the table, made by fusing lighter ones.",
        "&eChemistry:&r real oganesson has been made only a handful of times, and each atom lasted under a millisecond.",
        "&eHow:&r fuse your way up in the Fusion Chamber (check JEI for which pairs reach 118).",
        "&6Every block in this world can now be built from chemicals. You're close to what you once were.&r"]),
    Q("t6_flux", 12, 2, [item("fluxnetworks:flux_core")], "Wireless Power", deps=["t6_pu"], xp=200,
      optional=True, tokens=1, subtitle="Optional: energy without cables", desc=[
        "&eWhat:&r Flux Networks moves energy anywhere in a dimension, or across them.",
        "&eHow:&r the Flux Core needs a processing unit in this pack. Add plugs at sources and points at machines.",
        "&eTip:&r set a password on your network if you share a server."]),
    # ---------------------------------------------------------------- nitrogen chemistry and the platinum line
    Q("t6_haber", 0, 4, [item("chemlib:ammonia_bucket")], "Haber-Bosch", deps=["t4_reactor", "t5_hv"], xp=250,
      subtitle="Bread from air", desc=[
        "&6Feeding a world used to take a harvest god. Now it takes a reactor and some hydrogen.&r",
        "&eWhat:&r ammonia is the root of fertiliser, nitric acid and ammonium salts.",
        "&eChemistry:&r N₂ + 3H₂ → 2NH₃. Breaking nitrogen's triple bond is hard; this process feeds about half the world through fertiliser.",
        "&eHow:&r Chemical Reactor: 1 B nitrogen + 3 B hydrogen → 2 B ammonia. Fill a bucket from the output tank."]),
    Q("t6_ostwald", 2, 4, [item("chemlib:nitric_acid_bucket")], "Ostwald Process", deps=["t6_haber"], xp=250,
      subtitle="Burn ammonia, catch nitric acid", desc=[
        "&eChemistry:&r NH₃ + 2O₂ → HNO₃ + H₂O. Real plants burn ammonia over a platinum gauze, the very metal you're about to extract with it.",
        "&eHow:&r Chemical Reactor: 1 B ammonia + 2 B oxygen → 1 B nitric acid + 1 B water.",
        "&eTip:&r the water by-product can go back into your electrolysis line."]),
    Q("t6_sludge", 4, 4, [item("kubejs:pgm_sludge", 4)], "Anode Sludge", deps=["t6_ostwald"], xp=200,
      subtitle="Treasure in the electrolyzer's leftovers", desc=[
        "&eWhat:&r refining nickel and copper electrically leaves a sludge rich in platinum-group metals.",
        "&eChemistry:&r noble metals don't dissolve at the anode, so they fall to the bottom of the cell.",
        "&eHow:&r Electrolyzer: 4 nickel or copper dust → 4 dust back + PGM sludge (25% chance).",
        "&eTip:&r it costs you nothing but power. Leave it running."]),
    Q("t6_nh4cl", 4, 6, [item("chemlib:ammonium_chloride_dust", 4)], "Ammonium Chloride", deps=["t6_haber"], xp=150,
      subtitle="Two gases make a white powder", desc=[
        "&eChemistry:&r NH₃ + HCl → NH₄Cl. Open bottles of each near one another and a white smoke of this salt forms in the air.",
        "&eHow:&r Chemical Reactor: 1 B ammonia + 1 B hydrochloric acid → 1 ammonium chloride.",
        "&eTip:&r you need 2 per precipitation, so make plenty."]),
    Q("t6_aqua", 6, 4, [item("kubejs:chloroplatinic_acid", 2), item("kubejs:pgm_residue")], "Aqua Regia", deps=["t6_sludge"], xp=250,
      subtitle="Royal water dissolves the noble metals", desc=[
        "&eChemistry:&r 3 HCl : 1 HNO₃. Nitric acid oxidises the platinum and chloride grabs the ions, forming chloroplatinic acid, H₂PtCl₆.",
        "&eHow:&r Chemical Reactor: 4 PGM sludge + 3 B HCl + 1 B nitric acid → 2 chloroplatinic acid + 1 PGM residue.",
        "&eTip:&r iridium, osmium, rhodium and ruthenium don't dissolve. Keep the residue."]),
    Q("t6_precip", 8, 5, [item("kubejs:ammonium_hexachloroplatinate", 2)], "Precipitation", deps=["t6_aqua", "t6_nh4cl"], xp=200,
      subtitle="Pull platinum out of solution as a salt", desc=[
        "&eChemistry:&r ammonium chloride makes the platinum fall out as yellow ammonium hexachloroplatinate, (NH₄)₂PtCl₆.",
        "&eHow:&r Chemical Reactor: 1 chloroplatinic acid + 2 ammonium chloride → 1 ammonium hexachloroplatinate.",
        "&eTip:&r this step is why real platinum refining needs both the Haber-Bosch and Ostwald plants."]),
    Q("t6_pgm", 10, 5, [item(MI + "platinum_dust", 4)], "The Platinum Line", deps=["t6_precip"], xp=500, size=1.5,
      subtitle="Calcine the salt, keep the metal", desc=[
        "&6You remember metals that never tarnish. Now you know why: they refuse to react.&r",
        "&eChemistry:&r heating (calcining) drives off ammonia and HCl and leaves pure platinum metal.",
        "&eHow:&r Electric Blast Furnace: 2 ammonium hexachloroplatinate → 1 platinum dust.",
        "&eTip:&r processing unit boards need 4 platinum plates each. Automate this line."]),
    Q("t6_rare_pgm", 12, 5, [item(MI + "iridium_dust"), item("mekanism:dust_osmium"), item("chemlib:rhodium_dust"), item("chemlib:ruthenium_dust")], "The Rare Four", deps=["t6_pgm"], xp=250,
      optional=True, tokens=1, subtitle="Optional: iridium, osmium, rhodium, ruthenium", desc=[
        "&eWhat:&r the insoluble residue holds the rarest metals on Earth.",
        "&eChemistry:&r osmium is the densest element known, and iridium the most corrosion-resistant metal.",
        "&eHow:&r Centrifuge the PGM residue. Each output is a chance, so run plenty.",
        "&eTip:&r iridium is needed for monocrystalline silicon and, later, quantum circuit boards."]),
    # ---------------------------------------------------------------- optional side quests
    Q("t6_opt_hazmat", 18, -8, [item(MEK + "hazmat_mask"), item(MEK + "hazmat_gown"), item(MEK + "hazmat_pants"), item(MEK + "hazmat_boots"), item(MEK + "geiger_counter")],
      "Dress for the Job", deps=["t6_centrifuge"], xp=100, optional=True, tokens=1, subtitle="Optional: radiation safety", desc=[
        "&eHow:&r check JEI for each piece.",
        "&eWhat:&r a full hazmat suit blocks radiation; the Geiger counter shows how much is around you.",
        "&eTip:&r a leaking waste pipe can make an area dangerous for a long time. Check before you build."]),
    Q("t6_opt_reprocess", 24, -8, [item(MEK + "reprocessed_fissile_fragment", 4)], "Closing the Fuel Cycle", deps=["t6_plutonium"], xp=150,
      optional=True, tokens=1, subtitle="Optional: burn plutonium as fuel", desc=[
        "&eChemistry:&r plutonium-239 is fissile, so spent fuel can be recycled into new fuel, as some real reactors do.",
        "&eHow:&r Chemical Injection Chamber: plutonium pellet + hydrogen chloride → 4 fragments. Oxidize them into fissile fuel.",
        "&eTip:&r it means less waste and more fuel from every uranium ingot."]),
    Q("t6_opt_unstable", 16, 2, [item("chemlib:technetium"), item("chemlib:promethium"), item("chemlib:astatine"), item("chemlib:francium")],
      "The Unstable Ones", deps=["t6_chambers"], xp=300, optional=True, tokens=2, subtitle="Optional: elements with no stable form", desc=[
        "&eWhat:&r four elements that real chemists almost never get to hold.",
        "&eChemistry:&r technetium (43) and promethium (61) are the only light elements with no stable isotope. Astatine and francium are the rarest natural elements: grams exist in the whole crust.",
        "&eHow:&r fuse or split your way to each atomic number (check JEI)."]),
    Q("t6_opt_platinum", 10, 7, [item(MI + "platinum_ingot", 32)], "Platinum Reserve", deps=["t6_pgm"], xp=150,
      optional=True, tokens=1, subtitle="Optional: stockpile challenge", desc=[
        "&eHow:&r keep the Platinum Line running, then smelt the dust.",
        "&eWhat:&r half a stack of platinum ingots, all pulled out of sludge.",
        "&eTip:&r every processing unit board eats 4 platinum plates. You'll be glad of the reserve."]),
])
