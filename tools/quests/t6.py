"""Quest chapter: t6. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, anyof, MAIN, SIDE  # noqa: F401

MI = "modern_industrialization:"
MEK = "mekanism:"
GEN = "mekanismgenerators:"

CHAPTER = Chapter("t6", "VII. Materials and Nuclear", "mekanism:pellet_polonium",
        ["Purity and precision: semiconductors, PVC, isotopes.",
         "Then transmutation: any element from any other."], MAIN, [
    # ---------------------------------------------------------------- silicon
    Q("t6_argon", 2, -4, [item(MI + "argon_bucket")], "Argon from Air", deps=["t6_liquid_air", "t4_centrifuge"], xp=150,
      subtitle="The lazy gas that protects hot silicon", desc=[
        "&6You once stirred the sky. Now you pour it, liquid, into a tank.&r",
        "&eWhat:&r argon is an inert blanket gas. Growing a silicon crystal in air would ruin it.",
        "&eChemistry:&r air is 78% N₂, 21% O₂ and about 0.9% argon. Cool it until it liquefies, then separate the parts.",
        "&eHow:&r the Vacuum Freezer (or Pressurizer) with an Air Intake makes liquid air. The Centrifuge splits it into oxygen, nitrogen and a little argon.",
        "&eTip:&r the Heat Exchanger gives far more argon while it cools hot ingots."]),
    Q("t6_silicon", 4, -4, [item(MI + "silicon_wafer", 8)], "Semiconductor Silicon", deps=["t6_mono"], xp=250,
      subtitle="One perfect crystal, sliced thin", desc=[
        "&eWhat:&r computer chips need silicon purer than 99.9999999%, grown as one single crystal.",
        "&eChemistry:&r a seed crystal is pulled slowly out of molten silicon (the Czochralski process). Every atom lines up with the one below it.",
        "&eHow:&r Cutting Machine: 1 monocrystalline silicon + 500 mB lubricant → 32 wafers.",
        "&eTip:&r one boule is 32 wafers: enough for a long run of RAM and MMUs."]),
    Q("t6_chips", 6, -4, [item(MI + "random_access_memory", 2), item(MI + "arithmetic_logic_unit"), item(MI + "memory_management_unit")], "Chips", deps=["t6_ram", "t6_alu", "t6_mmu"], section="Chips", xp=200,
      subtitle="Memory, logic and control on silicon", desc=[
        "&eWhat:&r a processing unit needs RAM, an ALU and an MMU.",
        "&eChemistry:&r a pinch of aluminum (p-type) or phosphorus (n-type) in silicon changes how it carries current. That's 'doping', the basis of every transistor.",
        "&eHow:&r one of each, made in the quests around this one. The processing unit takes 2 RAM, 1 ALU and 1 MMU."]),
    # ---------------------------------------------------------------- PVC
    Q("t6_acetylene", 2, -2, [item(MI + "acetylene_bucket")], "Acetylene", deps=["t5_methane", "t5_hv"], section="PVC", xp=150,
      subtitle="The welding gas, from methane", desc=[
        "&eWhat:&r acetylene (C₂H₂) has a triple bond, which makes it very reactive.",
        "&eChemistry:&r heat methane hard enough and pairs of molecules lose hydrogen and join: 2CH₄ → C₂H₂ + 3H₂.",
        "&eHow:&r Electric Blast Furnace: 200 mB methane → 200 mB acetylene. Cracked naphtha also gives a little."]),
    Q("t6_vinyl", 4, -2, [item(MI + "vinyl_chloride_bucket")], "Vinyl Chloride", deps=["t6_acetylene", "t4_mi_hcl"], xp=150,
      subtitle="Acetylene meets hydrochloric acid", desc=[
        "&eChemistry:&r C₂H₂ + HCl → C₂H₃Cl. HCl adds across the triple bond. This was the original industrial route to PVC.",
        "&eHow:&r Chemical Reactor: 1 B acetylene + 1 B hydrochloric acid → 1 B vinyl chloride.",
        "&eTip:&r your salt line's chlorine and hydrogen make the HCl."]),
    Q("t6_pvc", 6, -2, [item(MI + "polyvinyl_chloride_bucket")], "PVC", deps=["t6_vinyl", "t5_catalyst"], xp=250,
      subtitle="Petrochemistry meets chlor-alkali", desc=[
        "&eWhat:&r polyvinyl chloride, (C₂H₃Cl)ₙ, is tough, fire-resistant and insulates EV circuit boards.",
        "&eChemistry:&r just like polyethylene, but every other carbon carries a chlorine atom. That's why PVC doesn't burn easily.",
        "&eHow:&r Chemical Reactor: 500 mB vinyl chloride + 4 tiny lead or chromium dust → 300 mB PVC."]),
    # ---------------------------------------------------------------- EV
    Q("t6_cadmium", 4, 0, [item(MI + "cadmium_dust", 4), item(MI + "cadmium_battery", 2)], "Cadmium Battery", deps=["t6_monazite_dust", "t6_annealed_cable"], xp=200,
      subtitle="Nickel-cadmium cells for the EV hull", desc=[
        "&eWhat:&r the EV hull and processing unit board each need 2 cadmium batteries.",
        "&eChemistry:&r a NiCd cell runs Cd + 2NiO(OH) + 2H₂O → Cd(OH)₂ + 2Ni(OH)₂, and it can be recharged by running it backwards.",
        "&eHow:&r Centrifuge: 9 monazite dust → 3 cadmium dust (plus neodymium, yttrium and helium). Battery: 2 cadmium dust, a battery alloy plate, 4 curved plates and 2 annealed copper cable. In reality cadmium is mostly a by-product of zinc refining.",
        "&eTip:&r cadmium is toxic in real life. Here it just needs a lot of monazite."]),
    Q("t6_board", 8, -1, [item(MI + "processing_unit_board")], "Processing Unit Board", deps=["t6_pvc", "t6_cadmium", "t6_annealed_cable", "t6_pt_plate"], section="The Processing Unit", xp=200,
      subtitle="PVC, platinum and cadmium in one board", desc=[
        "&eHow:&r Assembler: digital circuit board + 4 platinum plates + 2 cadmium batteries + 8 annealed copper cable + 1500 mB PVC.",
        "&eChemistry:&r platinum never corrodes, so it makes contacts that last forever.",
        "&eTip:&r platinum comes from MI's ore processing or the Platinum Line below (check JEI)."]),
    Q("t6_pu", 10, -2, [item(MI + "processing_unit"), item(MI + "highly_advanced_machine_hull")], "EV: Processing Units", deps=["t6_board", "t6_chips", "t6_ha_casing"], xp=400, size=1.5,
      items=[(MI + "processing_unit", 2)], subtitle="Extreme Voltage, built on purity", desc=[
        "&6A mind of silicon, insulated in salt and oil. It thinks the way you used to.&r",
        "&eWhat:&r processing units unlock EV machines, the NASA Workbench, Flux Networks and Alchemistry's chambers.",
        "&eHow:&r Assembler: processing unit board + 4 digital circuits + 2 RAM + ALU + MMU. The &eEV hull&r is a highly advanced casing + a processing unit + 2 cadmium batteries + 3 annealed copper cable."]),
    # ---------------------------------------------------------------- nuclear
    Q("t6_yellowcake", 12, -5, [item(MEK + "yellow_cake_uranium", 4)], "Yellowcake", deps=["t6_pu", "t6_uranium_ingot"], section="Mekanism Fission", xp=150,
      subtitle="The first step from ore to fuel", desc=[
        "&eWhat:&r yellowcake is concentrated uranium oxide powder, the raw material of nuclear fuel.",
        "&eChemistry:&r natural uranium is only 0.72% U-235, the isotope that splits. The rest is U-238.",
        "&eHow:&r Enrichment Chamber: 1 uranium ingot → 2 yellowcake. Then the Chemical Oxidizer turns it into uranium oxide gas.",
        "&eTip:&r a Geiger counter tells you when you're standing too close to anything radioactive."]),
    Q("t6_hf", 12, -7, [item(MEK + "fluorite_gem", 16)], "Hydrofluoric Acid", deps=["t6_pu", "t4_fluorite"], xp=150,
      subtitle="The acid that eats glass", desc=[
        "&eChemistry:&r CaF₂ + H₂SO₄ → CaSO₄ + 2HF. Hydrogen fluoride dissolves glass and is one of the most dangerous acids there is.",
        "&eHow:&r Chemical Dissolution Chamber: fluorite + sulfuric acid → hydrofluoric acid gas.",
        "&eTip:&r fluorite ore sits deep. Mystical Agriculture and Occultism can't make it in this pack. Keep extra HF: the Seed of a New World needs 4 buckets (a Rotary Condensentrator in liquid mode turns the gas into fluid)."]),
    Q("t6_uf6", 14, -6, [item(MEK + "chemical_infuser"), item(MEK + "chemical_oxidizer")], "Uranium Hexafluoride", deps=["t6_yellowcake", "t6_hf"], xp=200,
      subtitle="Turn uranium into a gas", desc=[
        "&eWhat:&r UF₆ is the only uranium compound that becomes a gas at low temperature (it sublimes at 56 °C), so it can be spun.",
        "&eChemistry:&r real plants go UO₂ → UF₄ → UF₆ with HF and then fluorine. Mekanism combines the steps.",
        "&eHow:&r Chemical Infuser: uranium oxide + hydrofluoric acid → uranium hexafluoride."]),
    Q("t6_centrifuge", 16, -6, [item(MEK + "isotopic_centrifuge")], "Isotope Separation", deps=["t6_uf6", "t6_ult_circuit"], xp=300,
      subtitle="Only mass tells U-235 and U-238 apart", desc=[
        "&eWhat:&r the two isotopes behave identically in every reaction, so chemistry can't separate them.",
        "&eChemistry:&r U-235 is about 1% lighter. Spin UF₆ fast enough and the heavier molecules drift outward.",
        "&eHow:&r Isotopic Centrifuge (6 lead ingots, 2 ultimate control circuits, a chemical tank): uranium hexafluoride → fissile fuel."]),
    Q("t6_fission_parts", 18, -6, [item(GEN + "fission_fuel_assembly", 4), item(GEN + "control_rod_assembly"), item(GEN + "fission_reactor_port", 4)], "Reactor Parts", deps=["t6_centrifuge", "t6_elite"], xp=250,
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
    Q("t6_plutonium", 22, -7, [item(MEK + "pellet_plutonium")], "Plutonium", deps=["t6_fission", "t6_fluorite_dust"], xp=250,
      subtitle="An element made by neutrons", desc=[
        "&eChemistry:&r U-238 captures a neutron and beta-decays twice into Pu-239, which is itself fissile.",
        "&eHow:&r Isotopic Centrifuge: 10 nuclear waste → 1 plutonium. Pressurized Reaction Chamber: plutonium + fluorite dust + water → pellet.",
        "&eTip:&r the pellet reaction also gives spent nuclear waste. Store it in a Radioactive Waste Barrel."]),
    Q("t6_polonium", 22, -5, [item(MEK + "pellet_polonium")], "Polonium", deps=["t6_fission", "t6_sna", "t6_fluorite_dust"], xp=250,
      subtitle="The element Marie Curie named for Poland", desc=[
        "&eChemistry:&r polonium-210 is made by neutron capture; it is intensely radioactive and gives off heat on its own.",
        "&eHow:&r Solar Neutron Activator (open sky, daylight): 10 nuclear waste → 1 polonium. Pellets come from the Pressurized Reaction Chamber, as with plutonium.",
        "&eTip:&r polonium is the input for the SPS and for Energy Cores."]),
    Q("t6_waste", 24, -6, [item(MEK + "pellet_plutonium"), item(MEK + "pellet_polonium")], "Transmutation by Neutron", deps=["t6_plutonium", "t6_polonium"], xp=500, size=1.5,
      subtitle="Lead to gold was never the hard part", desc=[
        "&6The old alchemists wanted to change one element into another. You do it before breakfast.&r",
        "&eWhat:&r reprocessing nuclear waste gives &eplutonium&r and &epolonium&r, two elements that barely exist in nature.",
        "&eHow:&r keep both pellet lines running. Plutonium feeds the quantum tier; polonium feeds antimatter.",
        "&eTip:&r spent waste still goes in a Radioactive Waste Barrel. Never dump it."]),
    # ---------------------------------------------------------------- transmutation
    Q("t6_reactor_parts", 12, 0, [item("alchemistry:reactor_casing", 16), item("alchemistry:reactor_energy"), item("alchemistry:reactor_input"), item("alchemistry:reactor_output")],
      "Chamber Frame", deps=["t6_pu"], section="Transmutation", xp=200, subtitle="The shell around an element reactor", desc=[
        "&eWhat:&r Alchemistry's fission and fusion chambers share the same casing, energy, input and output blocks.",
        "&eHow:&r craft the frame blocks (check JEI) and build the chamber around its controller. The controllers themselves are crafted with a reactor casing.",
        "&eTip:&r build both chambers side by side so one can feed the other."]),
    Q("t6_chambers", 14, 0, [item("alchemistry:fission_chamber_controller"), item("alchemistry:fusion_chamber_controller")], "Element Transmutation", deps=["t6_reactor_parts", "t6_nether_star"], xp=500, size=1.5,
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
    Q("t6_haber", 0, 4, [item("chemlib:ammonia_bucket")], "Haber-Bosch", deps=["t6_nitrogen", "t4_mi_h2o"], section="Nitrogen and Platinum", xp=250,
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
        "&6Metals that never tarnish. You used to think it was pride; now you know they simply refuse to react.&r",
        "&eChemistry:&r heating (calcining) drives off ammonia and HCl and leaves pure platinum metal.",
        "&eHow:&r Electric Blast Furnace: 2 ammonium hexachloroplatinate → 1 platinum dust.",
        "&eTip:&r processing unit boards need 4 platinum plates each. Automate this line."]),
    Q("t6_rare_pgm", 12, 5, [item(MI + "iridium_dust"), item("mekanism:dust_osmium"), item("chemlib:rhodium_dust"), item("chemlib:ruthenium_dust")], "The Rare Four", deps=["t6_pgm"], xp=250,
      subtitle="Iridium, osmium, rhodium, ruthenium", desc=[
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

    # ---------------------------------------------------------------- ATM10-aligned additions (2026-10-19)
    # Hotter furnaces: Kanthal coils open the EBF recipes for annealed copper, titanium, uranium and superconductor.
    Q("t6_kanthal", 0, 0, [item(MI + "kanthal_dust", 3), item(MI + "kanthal_hot_ingot"), item(MI + "kanthal_ingot", 4)], "Kanthal", deps=["t5_hv"], section="Hotter Furnaces", xp=150,
      subtitle="Iron, chromium, aluminium: the heating-element alloy", desc=[
        "&eWhat:&r Kanthal is the wire inside toasters and kilns. Coiled around your Blast Furnace it reaches recipes cupronickel can't.",
        "&eChemistry:&r FeCrAl alloy. When hot, its aluminium forms a thin skin of alumina (Al₂O₃) that stops the wire burning away, even near 1400 °C.",
        "&eHow:&r Mixer: 1 stainless steel + 1 chromium + 1 aluminum dust → 3 Kanthal dust. EBF → hot ingot, then the Vacuum Freezer."]),
    Q("t6_kanthal_coil", 0, 0, [item(MI + "kanthal_coil", 16)], "A Hotter Furnace", deps=["t6_kanthal_cable"], xp=250, size=1.5, shape="hexagon",
      subtitle="Swap your cupronickel coils for Kanthal", desc=[
        "&eWhat:&r an Electric Blast Furnace built with Kanthal coils unlocks a new set of recipes. JEI lists them under 'EBF (Kanthal Tier)'.",
        "&eHow:&r each coil is 8 Kanthal cables (crafting table or Assembler). The EBF's two coil rings take 16.",
        "&eTip:&r keep your old cupronickel furnace running too: cheap recipes don't need the upgrade."]),
    Q("t6_annealed", 0, 0, [item(MI + "annealed_copper_ingot", 8)], "Annealed Copper", deps=["t6_kanthal_coil"], xp=150,
      subtitle="Copper, softened by fire", desc=[
        "&eWhat:&r annealed copper cable goes into cadmium batteries, the processing unit board and every stainless motor.",
        "&eChemistry:&r annealing heats a metal and lets it cool slowly, so its crystals regrow without strain. Soft, fully annealed copper conducts best of all and is the standard (100% IACS) that other conductors are measured against.",
        "&eHow:&r Kanthal-tier EBF: copper dust + 250 mB oxygen → annealed copper hot ingot, then the Vacuum Freezer."]),
    Q("t6_titanium", 0, 0, [item(MI + "titanium_hot_ingot"), item(MI + "titanium_ingot", 8)], "Titanium", deps=["t6_kanthal_coil"], xp=200,
      subtitle="Light as aluminium, strong as steel", desc=[
        "&eWhat:&r titanium builds the toughest MI machines: the Implosion Compressor, the Pressurizer and their casings.",
        "&eChemistry:&r titanium grabs oxygen and nitrogen when hot, so real plants reduce TiCl₄ with molten magnesium under argon (the Kroll process). Here the EBF does it in one step.",
        "&eHow:&r MI titanium ore needs an iron pick; macerate it to dust (bauxite digestion leaves tiny titanium too). Kanthal-tier EBF → hot ingot → Vacuum Freezer."]),
    Q("t6_nitrogen", 0, 0, [item(MI + "nitrogen_bucket"), item(MI + "oxygen_bucket")], "The Rest of the Air", deps=["t6_liquid_air", "t4_centrifuge"], xp=100,
      subtitle="Nitrogen and oxygen, by the bucket", desc=[
        "&eWhat:&r the liquid air you split for argon is mostly nitrogen and oxygen. Nitrogen goes into explosives; oxygen into almost everything.",
        "&eChemistry:&r nitrogen boils at −196 °C, oxygen at −183 °C and argon in between. Real air-separation plants distil liquid air exactly along those steps.",
        "&eHow:&r Centrifuge: 3000 mB liquid air → 2315 nitrogen + 650 oxygen + 35 argon."]),
    Q("t6_itnt", 0, 0, [item(MI + "industrial_tnt", 8)], "Industrial TNT", deps=["t6_nitrogen", "t5_aromatics"], xp=150,
      subtitle="Controlled violence for compression", desc=[
        "&eWhat:&r Industrial TNT drives the Implosion Compressor, the only way to press the hardest alloys.",
        "&eChemistry:&r real TNT is 2,4,6-trinitrotoluene: toluene with three nitro groups, made with nitric and sulfuric acid. It's stable enough to melt and cast, which is why it was used so widely.",
        "&eHow:&r Mixer: 4 sand + 3 flint + 250 mB toluene (from cracked naphtha) + 1000 mB nitrogen → 4 Industrial TNT."]),
    Q("t6_tungsten", 0, 0, [item(MI + "tungsten_tiny_dust", 9), item(MI + "tungsten_nugget", 9), item(MI + "tungsten_ingot")], "Tungsten", deps=["t6_kanthal"], section="The Implosion Compressor", xp=150,
      subtitle="The metal with the highest melting point", desc=[
        "&eWhat:&r tungsten goes into blastproof alloy and, much later, the ultradense metal ball.",
        "&eChemistry:&r tungsten melts at 3422 °C, so no furnace casts it. Real tungsten parts are pressed from powder and sintered: powder metallurgy.",
        "&eHow:&r tungsten ore (iron pick, deep) → dust → tiny dust. Compressor: 1 tiny dust → 1 nugget (slow). Once you have an Implosion Compressor: 9 tiny dust + a stainless nugget + Industrial TNT → 1 ingot."]),
    Q("t6_advmotor", 0, 0, [item(MI + "advanced_motor", 2), item(MI + "advanced_pump")], "Stainless Motors", deps=["t6_annealed_cable", "t6_mag_rod", "t6_ss_rotor", "t5_al_cable"], section="Stainless Motors", xp=150,
      subtitle="Motors and pumps for the EV age", desc=[
        "&eWhat:&r advanced motors and pumps run the Implosion Compressor, the heat exchangers and the best upgrades.",
        "&eHow:&r advanced motor: a magnetic stainless rod, 2 stainless rods, 2 aluminum cable, 4 annealed copper wire. Advanced pump: advanced motor, 2 stainless rotors, fluid pipes and stainless bolts.",
        "&eTip:&r advanced pumps also build the Distillation Tower, the EV refinery."]),
    Q("t6_blastproof", 0, 0, [item(MI + "mixed_ingot_blastproof", 2), item(MI + "blastproof_alloy_plate", 4)], "Blastproof Alloy", deps=["t6_titanium", "t6_tungsten"], xp=200,
      subtitle="Tungsten, titanium and stainless, pressed as one", desc=[
        "&eWhat:&r the armour of the Implosion Compressor and every nuclear fuel rod.",
        "&eChemistry:&r tungsten for heat, titanium for lightness, stainless for toughness: a composite does what no single metal can.",
        "&eHow:&r Packer: 1 tungsten + 1 titanium + 1 stainless steel ingot → mixed blastproof ingot. Compressor: 2 mixed ingots → 1 plate (slow). With an Implosion Compressor: 1 mixed ingot + TNT → 3 ingots.",
        "&eTip:&r the Compressor route is only for your first compressor's 16 plates. After that, use the bang."]),
    Q("t6_implosion", 0, 0, [item(MI + "implosion_compressor"), item(MI + "blastproof_casing", 4)], "The Implosion Compressor", deps=["t6_blastproof", "t6_advmotor", "t6_itnt", "t6_ti_plates"], xp=300, size=1.5, shape="hexagon",
      subtitle="Squeeze metal with a shockwave", desc=[
        "&eWhat:&r a multiblock that uses Industrial TNT to press tungsten, blastproof alloy, beryllium and nuclear alloy.",
        "&eChemistry:&r explosive compaction is real: a shockwave can squeeze powder past what any press reaches. Explosions even make tiny diamonds from graphite.",
        "&eHow:&r controller: 2 advanced motors, 2 titanium large plates, an HV hull and 4 blastproof large plates. Blastproof casings (8 plates each) form the walls; layout in JEI and the MI guidebook."]),
    Q("t6_beryllium", 0, 0, [item(MI + "beryllium_dust", 3), item(MI + "beryllium_plate", 2)], "Beryllium", deps=["t6_implosion"], xp=150,
      subtitle="Emeralds are beryllium in disguise", desc=[
        "&eWhat:&r beryllium is one third of nuclear alloy.",
        "&eChemistry:&r emerald is the mineral beryl, Be₃Al₂Si₆O₁₈. Beryllium is light, stiff and reflects neutrons back into a reactor core.",
        "&eHow:&r Electrolyzer: 23 emerald dust → 3 beryllium + 2 aluminum + 6 silicon dust + oxygen. Implosion Compressor: 9 tiny beryllium dust + a stainless nugget + TNT → 1 ingot. Compress it into plates."]),
    Q("t6_monazite", 0, 0, [item(MI + "neodymium_dust", 3), item(MI + "yttrium_dust", 3), item(MI + "helium_bucket")], "Rare Earths and Helium", deps=["t6_monazite_dust"], xp=150,
      subtitle="Everything else hiding in monazite", desc=[
        "&eWhat:&r the same centrifuge run that gives cadmium also gives neodymium, yttrium and sometimes helium. You'll need all three for superconductors and fuel rods.",
        "&eChemistry:&r monazite is a rare-earth phosphate, (Ce,La,Nd,Th)PO₄. Its thorium slowly decays and the alpha particles it fires become helium atoms trapped in the crystal.",
        "&eHow:&r Centrifuge: 9 monazite dust → 3 neodymium + 3 yttrium + 3 cadmium dust, plus 300 mB helium half the time.",
        "&eTip:&r helium also comes from centrifuging uranium, distilling shale oil, and cooling hot ingots in the Heat Exchanger."]),
    Q("t6_solder", 0, 0, [item(MI + "soldering_alloy_dust", 8)], "Soldering Alloy", deps=["t6_kanthal"], xp=75,
      subtitle="Tin and lead, the metal glue", desc=[
        "&eWhat:&r molten solder seals every MI fuel rod and control rod.",
        "&eChemistry:&r tin and lead together melt lower than either alone (a eutectic, about 183 °C), so solder flows into joints without melting the parts.",
        "&eHow:&r Mixer: 1 tin dust + 1 lead dust → 2 solder dust. The EBF melts 1 dust into 90 mB of liquid solder."]),
    Q("t6_nuclear_alloy", 0, 0, [item(MI + "mixed_plate_nuclear"), item(MI + "nuclear_alloy_plate", 6), item(MI + "nuclear_alloy_large_plate")], "Nuclear Alloy", deps=["t6_beryllium", "t6_cadmium"], xp=200,
      subtitle="Blastproof, beryllium and cadmium, fused", desc=[
        "&eWhat:&r the metal the MI Nuclear Reactor is built from.",
        "&eChemistry:&r a reactor wall must survive heat and handle neutrons: beryllium reflects them, cadmium absorbs them, blastproof alloy holds it all together.",
        "&eHow:&r Packer: blastproof plate + beryllium plate + cadmium plate → mixed nuclear plate. Implosion Compressor with TNT → 3 nuclear alloy plates. Four plates make a large plate."]),
    Q("t6_control_rod", 0, 0, [item(MI + "cadmium_control_rod", 2)], "Control Rods", deps=["t6_blastproof", "t6_solder", "t6_monazite", "t6_cd_rods"], xp=200,
      subtitle="The brakes of a reactor", desc=[
        "&eWhat:&r cadmium control rods soak up neutrons. The reactor controller needs two, and they tame a hot core.",
        "&eChemistry:&r cadmium-113 swallows slow neutrons more readily than almost any other nucleus, so a little cadmium stops a chain reaction from running away.",
        "&eHow:&r Assembler: 18 cadmium rods, 2 blastproof curved plates, a large motor, 2 robot arms, 500 mB solder and 100 mB helium."]),
    Q("t6_mi_casing", 0, 0, [item(MI + "nuclear_casing", 4), item(MI + "nuclear_item_hatch"), item(MI + "nuclear_fluid_hatch"), item(MI + "nuclear_alloy_machine_casing_pipe")],
      "Reactor Shell", deps=["t6_nuclear_alloy", "t6_pu"], section="The MI Nuclear Reactor", xp=200,
      subtitle="Casings and hatches in nuclear alloy", desc=[
        "&eWhat:&r the walls and the top grid of the reactor. Item hatches hold fuel and rods; fluid hatches hold water to boil into steam.",
        "&eHow:&r nuclear casing: 8 nuclear alloy plates around an HV hull. Hatches: 8 plates around an EV item or fluid input hatch. Check JEI for the pipe casing.",
        "&eTip:&r the reactor comes in several sizes. Start small; the MI guidebook shows them all."]),
    Q("t6_fuel_rod", 0, 0, [item(MI + "uranium_fuel_rod", 2), item(MI + "uranium_fuel_rod_double")], "Fuel Rods", deps=["t6_blastproof", "t6_solder", "t6_monazite", "t6_nuclear_alloy", "t6_uranium_rods"], xp=200,
      subtitle="Natural uranium, sealed in blastproof", desc=[
        "&eWhat:&r plain uranium fuel rods need no enrichment. They burn slowly, and that slowness breeds plutonium.",
        "&eChemistry:&r natural uranium is 99.3% U-238 and 0.7% fissile U-235. U-238 catches a neutron and decays twice: ²³⁸U → ²³⁹U → ²³⁹Np → ²³⁹Pu.",
        "&eHow:&r 18 uranium rods (see Uranium Rods). Assembler: 18 uranium rods, 2 blastproof curved plates, a large motor, 2 robot arms, 500 mB solder, 100 mB helium. Packer: 2 rods + a nuclear alloy plate → double rod."]),
    Q("t6_mi_reactor", 0, 0, [item(MI + "nuclear_reactor")], "The Nuclear Reactor", deps=["t6_mi_casing", "t6_control_rod"], xp=400, size=1.5, shape="hexagon",
      subtitle="MI's fission reactor, a puzzle of neutrons", desc=[
        "&eWhat:&r a big power source, and the only place in the pack that makes MI plutonium. Quantum circuits need it.",
        "&eHow:&r Assembler: 4 nuclear alloy large plates, an EV hull, 2 processing units, 2 cadmium control rods. Put water in fluid hatches and fuel in item hatches; JEI shows each part's heat and neutron numbers.",
        "&eTip:&r it can't explode or irradiate anything. Too much heat only destroys what's inside the hatches. Experiment freely.",
        "{@pagebreak}",
        "&eDeep dive: fast and slow neutrons&r",
        "Fission releases fast neutrons. Fuel catches slow ones far better, so reactors use a moderator (water, heavy water, graphite) to slow them down by collisions.",
        "MI models both kinds. Neutrons that escape the edge are lost; ones that hit a hatch can scatter, slow down, or be absorbed. Read the reactor's GUI as a map of where neutrons go."]),
    Q("t6_mi_plutonium", 0, 0, [item(MI + "uranium_fuel_rod_depleted"), item(MI + "plutonium_tiny_dust", 9), item(MI + "plutonium_dust", 2)], "Bred Plutonium", deps=["t6_mi_reactor", "t6_fuel_rod"], xp=400, size=1.5, shape="hexagon",
      subtitle="Spent fuel, recycled into a new element", desc=[
        "&6Uranium in, plutonium out. You are keeping a forge for elements now.&r",
        "&eWhat:&r MI plutonium dust, the heart of the plutonium battery and so of every quantum circuit.",
        "&eHow:&r burn uranium fuel rods until they're depleted. Centrifuge one depleted rod → 53 tiny U-238 dust + 27 tiny plutonium dust (3 full dusts) and sometimes a tiny U-235.",
        "&eTip:&r this is MI plutonium, not Mekanism's pellets. You need both: pellets for the Seed, dust for quantum circuits."]),
    Q("t6_hx_small", 0, 0, [item(MI + "small_heat_exchanger", 2)], "Small Heat Exchanger", deps=["t6_advmotor"], xp=150,
      subtitle="Move heat without mixing fluids", desc=[
        "&eWhat:&r a component for cooling cells (quantum circuits need them) and for the Heat Exchanger multiblock.",
        "&eChemistry:&r a heat exchanger lets a hot fluid warm a cold one through a thin wall. Every power station and refrigerator relies on one.",
        "&eHow:&r Assembler: 4 invar plates, a stainless large plate and 4 advanced pumps."]),
    # ---------------------------------------------------------------- optional: nuclear and EV side lines
    Q("t6_opt_casings", 0, 0, [item(MI + "solid_titanium_machine_casing", 4), item(MI + "stainless_steel_machine_casing_pipe", 2)], "Titanium Casings", deps=["t6_titanium"], xp=75,
      optional=True, tokens=1, subtitle="Optional: walls for the big machines", desc=[
        "&eWhat:&r solid titanium casings wall in the Pressurizer and the high-pressure boilers; stainless pipe casings carry fluids through the Heat Exchanger.",
        "&eHow:&r 8 titanium plates + a titanium gear per casing (Assembler). Check JEI (press U on a casing) for the multiblocks that use each."]),
    Q("t6_opt_hx", 0, 0, [item(MI + "heat_exchanger")], "The Heat Exchanger", deps=["t6_hx_small", "t6_opt_casings"], xp=150,
      optional=True, tokens=1, subtitle="Optional: cool hot ingots, catch argon and helium", desc=[
        "&eWhat:&r a multiblock that cools hot ingots with cryofluid (giving back argon and helium) and recycles high-pressure water and steam.",
        "&eHow:&r Assembler: 2 small heat exchangers, an HV hull, 2 stainless pipe casings, 2 frostproof and 2 heatproof casings. Layout in JEI.",
        "&eTip:&r each ingot cooled this way returns 13 mB argon and 5 mB helium. It adds up."]),
    Q("t6_opt_heavy", 0, 0, [item(MI + "deuterium_bucket"), item(MI + "heavy_water_bucket")], "Heavy Water", deps=["t6_mi_reactor"], xp=100,
      optional=True, tokens=1, subtitle="Optional: hydrogen with a neutron", desc=[
        "&eWhat:&r deuterium is hydrogen with one extra neutron; heavy water is D₂O. Both feed fusion, and heavy water is a reactor coolant.",
        "&eChemistry:&r about 1 hydrogen atom in 6400 is deuterium. Heavy water is 11% denser than normal water, and ice made from it sinks.",
        "&eHow:&r Centrifuge: 1000 mB hydrogen → 20 mB deuterium + 1 mB tritium, or 1000 mB water → 20 mB heavy water. Chemical Reactor: 2000 deuterium + 1000 oxygen → 3000 heavy water."]),
    Q("t6_opt_isotopes", 0, 0, [item(MI + "uranium_235_tiny_dust"), item(MI + "uranium_238_tiny_dust", 16)], "Uranium Isotopes", deps=["t6_mi_reactor"], xp=100,
      optional=True, tokens=1, subtitle="Optional: split U-235 from U-238", desc=[
        "&eWhat:&r MI's own isotope split, for enriched fuel.",
        "&eChemistry:&r U-235 and U-238 differ by three neutrons, about 1% in mass. Spinning them hard is still how most enrichment is done.",
        "&eHow:&r Centrifuge: 9 uranium dust → 1 tiny U-235 + 80 tiny U-238 (and sometimes helium). Very slow; depleted rods give more."]),
    Q("t6_opt_enriched", 0, 0, [item(MI + "le_uranium_dust"), item(MI + "he_uranium_dust")], "Enriched Uranium", deps=["t6_opt_isotopes"], xp=100,
      optional=True, tokens=1, subtitle="Optional: low and high enrichment", desc=[
        "&eWhat:&r enriched fuel burns hotter and makes more neutrons than natural uranium.",
        "&eHow:&r Mixer: 8 U-238 + 1 U-235 dust → 9 LE uranium dust; 6 U-238 + 3 U-235 → 9 HE uranium dust. Then rods and fuel rods as before.",
        "&eTip:&r more neutrons also means more heat. Add control rods before you add HE fuel."]),
    Q("t6_opt_mox", 0, 0, [item(MI + "le_mox_dust"), item(MI + "he_mox_dust")], "MOX Fuel", deps=["t6_opt_enriched", "t6_mi_plutonium"], xp=100,
      optional=True, tokens=1, subtitle="Optional: burn the plutonium you bred", desc=[
        "&eWhat:&r mixed-oxide fuel uses plutonium in place of U-235.",
        "&eChemistry:&r real MOX mixes PuO₂ into UO₂. France recycles spent fuel into MOX, getting more energy from the same mined uranium.",
        "&eHow:&r Mixer: 8 U-238 + 1 plutonium dust → 9 LE MOX; 6 U-238 + 3 plutonium → 9 HE MOX."]),
    Q("t6_opt_rods", 0, 0, [anyof([MI + "le_uranium_fuel_rod_double", MI + "he_uranium_fuel_rod_double", MI + "le_mox_fuel_rod_double", MI + "he_mox_fuel_rod_double"], 1)],
      "Better Fuel Rods", deps=["t6_opt_enriched"], xp=100,
      optional=True, tokens=1, subtitle="Optional: any enriched or MOX double rod", desc=[
        "&eWhat:&r any double fuel rod made from LE or HE uranium, or from LE or HE MOX.",
        "&eHow:&r the same Assembler recipe as plain fuel rods, with the enriched rods instead. Packer: 2 rods + a nuclear alloy plate → double."]),
    Q("t6_opt_spent", 0, 0, [anyof([MI + "le_uranium_fuel_rod_depleted", MI + "he_uranium_fuel_rod_depleted", MI + "le_mox_fuel_rod_depleted", MI + "he_mox_fuel_rod_depleted"], 1)],
      "Spent Fuel", deps=["t6_opt_rods"], xp=100,
      optional=True, tokens=1, subtitle="Optional: burn an enriched rod to the end", desc=[
        "&eWhat:&r a depleted enriched or MOX rod, ready for the Centrifuge.",
        "&eHow:&r centrifuging it returns U-238 and plutonium (and U-235 from uranium fuel). HE MOX gives the most plutonium back.",
        "&eTip:&r this closes the loop: uranium in, plutonium out, plutonium back in as MOX."]),
    Q("t6_opt_up_turbo", 0, 0, [item(MI + "turbo_upgrade", 4)], "Turbo Upgrades", deps=["t6_advmotor", "t6_pvc"], xp=100,
      optional=True, tokens=1, subtitle="Optional: the next machine upgrade", desc=[
        "&eHow:&r Assembler: 16 advanced motors, 2 advanced pumps, 4 advanced upgrades, a digital circuit board and 1000 mB PVC → 4 turbo upgrades.",
        "&eTip:&r one turbo upgrade in a multiblock lets the hungriest recipes run."]),
    Q("t6_opt_large_adv", 0, 0, [item(MI + "large_advanced_motor"), item(MI + "large_advanced_pump")], "Large Advanced Motors", deps=["t6_advmotor", "t6_titanium", "t6_pu"], xp=100,
      optional=True, tokens=1, subtitle="Optional: titanium-rotored giants", desc=[
        "&eHow:&r large advanced motor: a processing unit, 2 titanium rods, 6 advanced motors. Large advanced pump: 2 processing units, 3 titanium rotors, a large advanced motor and 3 advanced pumps.",
        "&eTip:&r they go into highly advanced upgrades and the biggest pumps and machines."]),
    Q("t6_opt_up_ha", 0, 0, [item(MI + "highly_advanced_upgrade", 4)], "Highly Advanced Upgrades", deps=["t6_opt_up_turbo", "t6_opt_large_adv"], xp=150,
      optional=True, tokens=2, subtitle="Optional: the last upgrade before quantum", desc=[
        "&eHow:&r Assembler: 8 large advanced motors, 4 large advanced pumps, 4 turbo upgrades, a processing unit board and 2500 mB PVC → 4.",
        "&eTip:&r the Quantum Upgrade, after the Seed, needs 32 of these."]),
    Q("t5_distill", 2, 0, [item(MI + "distillation_tower")], "Fractional Distillation", deps=["t6_advmotor", "t5_opt_distillery"], section="The Full Refinery", xp=300, size=1.5,
      subtitle="The refinery of the pack", desc=[
        "&eWhat:&r the Distillation Tower is a multiblock that splits one fluid into several fractions at once.",
        "&eChemistry:&r heat the crude and each fraction boils off at its own temperature. Light molecules rise to the top, heavy ones stay low.",
        "&eHow:&r controller: 4 advanced pumps, 2 Distilleries, 2 digital circuits and a Turbo hull. The layout is in JEI. Each extra layer adds one more output, up to eight.",
        "&eTip:&r one tower replaces a whole row of Distilleries: steam-cracked naphtha gives methane, acetylene, ethylene, propene, butadiene, benzene, toluene and ethylbenzene in one pass."]),
    # ===== ATM10-style detail pass (2026-10-19) =====
    # --- air separation
    Q("t6_ss_rotor", 0, 0, [item(MI + "stainless_steel_rotor", 3)], "Stainless Rotors", deps=["t5_ss_plate"], xp=80,
      subtitle="Blades that survive heat and acid", desc=[
        "&eWhat:&r the air intake spins one; every advanced pump spins three.",
        "&eHow:&r blades: 2 stainless curved plates + 1 stainless rod → 4 blades. Ring: Compressor, 1 rod → 1 ring. Rotor: 4 blades, 4 bolts and a ring on a crafting table.",
        "&eTip:&r the Assembler recipe needs soldering alloy; craft by hand until your solder line runs."]),
    Q("t6_air_intake", 0, 0, [item(MI + "air_intake")], "Air Intake", deps=["t6_ss_rotor"], xp=80,
      section="Air Separation", subtitle="A fan that feeds the freezer", desc=[
        "&eWhat:&r the Air Intake sits in the Vacuum Freezer or Pressurizer and lets it pull in air to liquefy. It isn't used up.",
        "&eHow:&r 4 stainless plates, 4 aluminum plates and a stainless rotor."]),
    Q("t6_liquid_air", 0, 0, [item(MI + "liquid_air_bucket")], "Liquid Air", deps=["t6_air_intake", "t5_freezer"], xp=80,
      subtitle="Air, cooled until it pours", desc=[
        "&eWhat:&r air cold enough to be a liquid: the raw material for nitrogen, oxygen and argon.",
        "&eChemistry:&r air liquefies below about −194 °C. Carl von Linde did it industrially in 1895 by compressing air, cooling it, and letting it expand again and again.",
        "&eHow:&r Vacuum Freezer with an Air Intake inside: 1000 mB liquid air per run."]),
    # --- chips
    Q("t6_mono", 0, 0, [item(MI + "monocrystalline_silicon")], "A Perfect Crystal", deps=["t6_argon", "t6_rare_pgm"], xp=150,
      subtitle="Grow one silicon crystal under argon", desc=[
        "&eWhat:&r a monocrystalline silicon boule, the start of every chip.",
        "&eChemistry:&r in the Czochralski process a seed crystal is drawn slowly out of molten silicon, and every atom lines up with the one below. Argon keeps oxygen and nitrogen out of the melt.",
        "&eHow:&r Electric Blast Furnace: 32 silicon dust + 1 tiny iridium dust + 1250 mB argon → 1 monocrystalline silicon.",
        "&eTip:&r the tiny iridium is from the Platinum Line's residue. Keep a few."]),
    Q("t6_ram", 0, 0, [item(MI + "random_access_memory", 2)], "RAM", deps=["t6_silicon", "t5_sbr"], xp=100,
      subtitle="Memory, grown on a wafer", desc=[
        "&eWhat:&r random access memory; each processing unit takes 2.",
        "&eChemistry:&r a DRAM cell is one transistor and one tiny capacitor. The capacitor's charge is the bit, and it leaks away, so the chip refreshes itself thousands of times a second.",
        "&eHow:&r Chemical Reactor: 1 silicon wafer + 1 antimony dust + 1 aluminum dust + 250 mB argon + 500 mB styrene-butadiene rubber → 2 RAM."]),
    Q("t6_diamond_plate", 0, 0, [item(MI + "diamond_plate", 2)], "Diamond Plates", deps=["t5_hv"], xp=40,
      subtitle="The hardest substrate there is", desc=[
        "&eWhat:&r each ALU is built on a diamond plate.",
        "&eChemistry:&r diamond conducts heat better than any metal while insulating electrically: ideal for a chip that runs hot.",
        "&eHow:&r Compressor: 1 diamond → 1 diamond plate (slow)."]),
    Q("t6_alu", 0, 0, [item(MI + "arithmetic_logic_unit")], "Arithmetic Logic Unit", deps=["t6_diamond_plate", "t5_gates"], xp=100,
      subtitle="Eight gates that do sums", desc=[
        "&eWhat:&r the part of a processor that adds, compares and decides. Qubits need two each later.",
        "&eChemistry:&r binary addition is just XOR and AND: a half adder is two gates. Chain them and you can add numbers of any size.",
        "&eHow:&r 1 diamond plate, 2 AND gates, 2 OR gates and 4 NOT gates."]),
    Q("t6_emerald_plate", 0, 0, [item(MI + "emerald_plate", 2)], "Emerald Plates", deps=["t5_hv"], xp=40,
      subtitle="Beryl, pressed flat", desc=[
        "&eWhat:&r the MMU sits on an emerald plate.",
        "&eHow:&r Compressor: 1 emerald → 1 emerald plate (slow)."]),
    Q("t6_pt_plate", 0, 0, [item(MI + "platinum_plate", 8)], "Platinum Plates", deps=["t6_pgm"], xp=60,
      subtitle="The noble metal, rolled", desc=[
        "&eWhat:&r every processing unit board takes 4 platinum plates; wire for the MMU comes from them too.",
        "&eHow:&r smelt platinum dust into ingots, then Compressor: 1 ingot → 1 plate."]),
    Q("t6_pt_wire", 0, 0, [item(MI + "platinum_fine_wire", 6)], "Platinum Fine Wire", deps=["t6_pt_plate"], xp=40,
      subtitle="Contacts that never corrode", desc=[
        "&eWhat:&r each MMU takes 6.",
        "&eHow:&r Wiremill: plate → 2 platinum wire; wire → 4 fine wire."]),
    Q("t6_mmu", 0, 0, [item(MI + "memory_management_unit")], "Memory Management Unit", deps=["t6_silicon", "t6_emerald_plate", "t6_pt_wire"], xp=100,
      subtitle="The chip that keeps track of memory", desc=[
        "&eWhat:&r the MMU translates the addresses a program asks for into real places in RAM.",
        "&eHow:&r 1 emerald plate, 2 silicon wafers and 6 platinum fine wire."]),
    # --- EV parts
    Q("t6_monazite_dust", 0, 0, [item(MI + "monazite_dust", 9)], "Monazite", deps=["t4_centrifuge"], xp=60,
      subtitle="A rare-earth phosphate", desc=[
        "&eWhat:&r monazite is the pack's source of cadmium, neodymium, yttrium and helium, all from one centrifuge run.",
        "&eChemistry:&r (Ce,La,Nd,Th)PO₄: a phosphate of rare earths with a little thorium, which makes it faintly radioactive.",
        "&eHow:&r mine MI monazite ore and macerate it. A stainless steel drill in a quarry also brings some up."]),
    Q("t6_annealed_cable", 0, 0, [item(MI + "annealed_copper_wire", 8), item(MI + "annealed_copper_cable", 8)], "Annealed Copper Cable", deps=["t6_annealed"], xp=60,
      subtitle="The EV cable", desc=[
        "&eWhat:&r annealed copper cable carries EV power and goes into cadmium batteries, the processing unit board and the EV hull. Advanced motors use the bare wire.",
        "&eHow:&r Compressor: ingot → plate. Wiremill: plate → 2 wire. 3 wire + rubber (sheets or liquid SBR) → 3 cable."]),
    Q("t6_cr_plate", 0, 0, [item(MI + "chromium_ingot", 4), item(MI + "chromium_plate", 4)], "Chromium Plates", deps=["t5_chromium", "t5_freezer"], xp=60,
      subtitle="Bright, hard and stubborn", desc=[
        "&eWhat:&r the highly advanced casing is half chromium plates.",
        "&eChemistry:&r chromium is the hardest pure metal and the reason chrome plating shines: its oxide film is clear and self-healing.",
        "&eHow:&r EBF: chromium dust → hot ingot. Vacuum Freezer → ingot. Compressor → plate."]),
    Q("t6_ti_plates", 0, 0, [item(MI + "titanium_plate", 8), item(MI + "titanium_large_plate", 2)], "Titanium Plates", deps=["t6_titanium"], xp=60,
      subtitle="Light armour for EV machines", desc=[
        "&eWhat:&r the highly advanced casing takes 4 titanium plates; the Implosion Compressor takes 2 large plates.",
        "&eHow:&r Compressor: ingot → plate. 4 plates → 1 large plate (crafting table or Packer)."]),
    Q("t6_ha_casing", 0, 0, [item(MI + "highly_advanced_machine_casing")], "Highly Advanced Casing", deps=["t6_ti_plates", "t6_cr_plate", "t5_hv"], xp=80,
      subtitle="A Turbo hull in titanium and chromium", desc=[
        "&eWhat:&r the shell of the EV hull.",
        "&eHow:&r 4 titanium plates and 4 chromium plates around a Turbo (HV) machine hull."]),
    Q("t6_ev_power", 0, 0, [item(MI + "hv_ev_transformer"), item(MI + "ev_storage_unit")], "An EV Grid", deps=["t6_pu"], xp=60,
      optional=True, tokens=1, subtitle="Optional: the next step up", desc=[
        "&eWhat:&r an HV-to-EV transformer and an EV storage unit.",
        "&eHow:&r transformer: a Turbo hull, 4 aluminum cable, 1 annealed copper cable. Storage: an EV hull, 6 cadmium batteries, 2 battery alloy plates."]),
    Q("t6_kanthal_cable", 0, 0, [item(MI + "kanthal_wire", 6), item(MI + "kanthal_cable", 16)], "Kanthal Cable", deps=["t6_kanthal"], xp=60,
      subtitle="Heating wire, insulated", desc=[
        "&eWhat:&r Kanthal coils are wound from Kanthal cable, 8 per coil.",
        "&eHow:&r Compressor: ingot → plate. Wiremill: plate → 2 wire. 3 wire + rubber → 3 cable.",
        "&eTip:&r a full furnace needs 16 coils, so 128 cables. Set the Wiremill and Packer running early."]),
    Q("t6_mag_rod", 0, 0, [item(MI + "stainless_steel_rod_magnetic", 2)], "Magnetic Stainless Rods", deps=["t6_monazite", "t5_ebf"], xp=60,
      subtitle="Neodymium makes the magnet", desc=[
        "&eWhat:&r the rotor core of every advanced motor.",
        "&eChemistry:&r neodymium-iron-boron magnets are the strongest permanent magnets made. Every wind turbine and electric car motor has them.",
        "&eHow:&r Polarizer: 1 stainless steel rod + 1 neodymium dust → 1 magnetic stainless rod."]),
    # --- Mekanism nuclear parts
    Q("t6_elite", 0, 0, [item(MEK + "elite_control_circuit", 4)], "Elite Control Circuits", deps=["t5_hv", "t4_reinforced"], xp=80,
      subtitle="Mekanism's HV circuit", desc=[
        "&eWhat:&r fission ports, control rods and the Solar Neutron Activator all need elite circuits.",
        "&eHow:&r 1 MI digital circuit, 2 reinforced alloy and 1 advanced control circuit."]),
    Q("t6_ult_circuit", 0, 0, [item(MEK + "alloy_atomic", 4), item(MEK + "ultimate_control_circuit", 2)], "Ultimate Control Circuits", deps=["t6_pu", "t6_elite"], xp=100,
      subtitle="Mekanism's EV circuit", desc=[
        "&eWhat:&r the Isotopic Centrifuge and the SPS run on ultimate circuits.",
        "&eHow:&r atomic alloy: Metallurgic Infuser, reinforced alloy + refined obsidian. Circuit: 1 MI processing unit, 2 atomic alloy and 1 elite circuit."]),
    Q("t6_uranium_ingot", 0, 0, [item(MI + "uranium_ingot", 4)], "Uranium Ingots", deps=["t4_uranium"], xp=60,
      subtitle="The fuel, as metal", desc=[
        "&eWhat:&r Mekanism's enrichment starts from ingots, and MI's fuel rods are cut from them.",
        "&eChemistry:&r uranium metal is dense (19 g/cm³, about as heavy as gold) and burns in air when finely divided.",
        "&eHow:&r smelt raw uranium in any furnace, or melt uranium dust in a Kanthal-tier Electric Blast Furnace."]),
    Q("t6_fluorite_dust", 0, 0, [item(MEK + "dust_fluorite", 8)], "Fluorite Dust", deps=["t4_fluorite"], xp=40,
      subtitle="The binder of every pellet", desc=[
        "&eWhat:&r each plutonium or polonium pellet takes 1 fluorite dust.",
        "&eHow:&r Crusher: 1 fluorite gem → 1 dust. Fluorite ore crushed in Occultism gives more."]),
    Q("t6_hf_bucket", 0, 0, [item(MEK + "hydrofluoric_acid_bucket")], "HF in a Bucket", deps=["t6_hf"], xp=60,
      subtitle="The Seed wants four of these", desc=[
        "&eWhat:&r hydrofluoric acid as a liquid. The Seed of a New World takes 4 buckets.",
        "&eChemistry:&r HF boils at 19.5 °C, so on a warm day it's barely a liquid. Real plants keep it cooled under pressure in steel, never glass.",
        "&eHow:&r Rotary Condensentrator in liquid mode, HF gas in, fluid out."]),
    Q("t6_sna", 0, 0, [item(MEK + "solar_neutron_activator")], "Solar Neutron Activator", deps=["t6_elite", "t5_hdpe"], xp=100,
      subtitle="Sunlight, focused on waste", desc=[
        "&eWhat:&r the machine that turns nuclear waste into polonium.",
        "&eHow:&r reinforced alloy, an HDPE sheet, 2 elite circuits, a steel casing and bronze ingots (check JEI). It needs a clear view of the sky and works only in daylight."]),
    Q("t6_waste_barrel", 0, 0, [item(MEK + "radioactive_waste_barrel", 2)], "Waste Barrels", deps=["t6_fission"], xp=40,
      subtitle="Somewhere safe for what's left", desc=[
        "&eWhat:&r radioactive waste barrels hold spent waste and let it decay slowly instead of leaking.",
        "&eChemistry:&r every radioactive isotope halves on its own schedule. Real spent fuel is kept cool for years before it is moved anywhere.",
        "&eHow:&r 4 steel and 4 lead ingots."]),
    Q("t6_logic_adapter", 0, 0, [tick()], "Reactor Logic", deps=['t6_fission'], optional=True, tokens=0, xp=0, icon="mekanismgenerators:fission_reactor_logic_adapter", subtitle="Moved: see Fission Logic Adapter", desc=["&eMoved:&r this step is now \"Fission Logic Adapter\" on the Mekanism: Power page. Click to dismiss."]),
    Q("t6_nether_star", 0, 0, [item("minecraft:nether_star")], "A Nether Star", deps=["t6_reactor_parts"], xp=150,
      subtitle="The Fusion Chamber's heart", desc=[
        "&eWhat:&r the Fusion Chamber controller needs a Nether Star.",
        "&eHow:&r defeat a Wither (soul sand T, three wither skeleton skulls). Fight it in a sealed room, deep underground.",
        "&eTip:&r save the skulls you find from now on: the Seed of a New World needs four more stars."]),
    # --- MI nuclear parts
    Q("t6_cd_rods", 0, 0, [item(MI + "cadmium_ingot", 2), item(MI + "cadmium_rod", 18)], "Cadmium Rods", deps=["t6_cadmium"], xp=60,
      subtitle="Neutron sponges, cut to length", desc=[
        "&eWhat:&r each cadmium control rod is 18 of these.",
        "&eHow:&r smelt cadmium dust into ingots. Cutting Machine with lubricant: 1 ingot → 2 rods."]),
    Q("t6_uranium_rods", 0, 0, [item(MI + "uranium_rod", 18)], "Uranium Rods", deps=["t6_uranium_ingot"], xp=60,
      subtitle="Fuel, cut to length", desc=[
        "&eWhat:&r each MI uranium fuel rod is 18 of these.",
        "&eHow:&r Cutting Machine with lubricant: 1 uranium ingot → 2 rods."]),
    Q("t5_large_diesel", 0, 0, [tick()], "Large Diesel Generator", deps=['t6_advmotor', 't5_diesel'], optional=True, tokens=0, xp=0, icon="modern_industrialization:large_diesel_generator", subtitle="Moved: see Large Diesel Generator", desc=["&eMoved:&r this step is now \"Large Diesel Generator\" on the Power page. Click to dismiss."]),
])
