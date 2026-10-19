"""Quest chapter: t5. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

MI = "modern_industrialization:"

CHAPTER = Chapter("t5", "VI. Petrochemistry", "modern_industrialization:polyethylene_bucket",
        ["Crude oil is a mixture. Separate it by boiling point, then build polymers from the pieces."], MAIN, [
    # ---------------------------------------------------------------- main line: crude -> polymers
    Q("t5_oil", 0, 0, [item(MI + "oil_drilling_rig"), item(MI + "crude_oil_bucket")], "Black Gold", deps=["t4_mv"], xp=200,
      subtitle="Millions of years of sunlight, stored underground", desc=[
        "&6Before there were people, you watched forests grow, fall and sink, and the ages press them into oil. Time to take some of that sunlight back.&r",
        "&eWhat:&r crude oil is a soup of hydrocarbons, from tiny gas molecules to long waxy chains.",
        "&eChemistry:&r hydrocarbons are just carbon and hydrogen (CₙH₂ₙ₊₂ and friends). Chain length decides whether one is a gas, a fuel or a tar.",
        "&eHow:&r put the Oil Drilling Rig in an MI Quarry over an oil-rich area (check JEI). It slowly wears out aluminum drills.",
        "&eTip:&r pipe the crude straight into a tank. You'll need a lot of it."]),
    Q("t5_distill", 2, 0, [item(MI + "distillation_tower")], "Fractional Distillation", deps=["t5_oil", "t5_pipe_casing"], xp=300, size=1.5,
      subtitle="The refinery of the pack", desc=[
        "&eWhat:&r the Distillation Tower is a multiblock that splits one fluid into several fractions at once.",
        "&eChemistry:&r heat the crude and each fraction boils off at its own temperature. Light molecules rise to the top, heavy ones stay low.",
        "&eHow:&r the 3D layout is in JEI and the MI guidebook. Each extra layer adds one more output.",
        "&eTip:&r every other mod gets its fuel and plastic from here, so build it with room to grow."]),
    Q("t5_fractions", 4, 0, [item(MI + "sulfuric_light_fuel_bucket"), item(MI + "sulfuric_heavy_fuel_bucket"), item(MI + "sulfuric_naphtha_bucket")],
      "Sour Fractions", deps=["t5_distill"], xp=150, subtitle="Three cuts of crude, all still full of sulfur", desc=[
        "&eWhat:&r 1000 mB of crude gives 500 light fuel, 200 heavy fuel and 300 naphtha, but all three are 'sour'.",
        "&eChemistry:&r natural oil carries sulfur compounds. Burn them and you get SO₂, the gas behind acid rain.",
        "&eHow:&r run crude through the Distillation Tower and catch each output in its own tank or bucket."]),
    Q("t5_hydrotreat", 6, 0, [item(MI + "light_fuel_bucket"), item(MI + "heavy_fuel_bucket"), item(MI + "naphtha_bucket")],
      "Sweetening the Oil", deps=["t5_fractions"], xp=200, subtitle="Hydrogen pulls the sulfur out", desc=[
        "&eWhat:&r hydrotreating removes the sulfur and gives clean light fuel, heavy fuel and naphtha.",
        "&eChemistry:&r hydrogen reacts with sulfur compounds to form H₂S. Real refineries turn that into sulfur and then acid; MI hands you sulfuric acid directly.",
        "&eHow:&r Chemical Reactor: 12 B of a sour fraction + 2 B hydrogen → 12 B clean fraction + 2 B H₂SO₄.",
        "&eTip:&r feed the acid back into your ore line. Nothing is wasted."]),
    Q("t5_diesel", 6, -2, [item(MI + "diesel_bucket"), item(MI + "lv_diesel_generator")], "Diesel Power", deps=["t5_hydrotreat"], xp=150,
      subtitle="Blend two fuels into one", desc=[
        "&eWhat:&r diesel runs MI generators, tools and, later, your rockets (Ad Astra burns MI diesel).",
        "&eChemistry:&r diesel is a blend of C₁₀ to C₂₀ hydrocarbons: mostly light fuel, with heavy fuel for energy density.",
        "&eHow:&r Mixer: 5 B light fuel + 1 B heavy fuel → 6 B diesel.",
        "&eTip:&r a Large Diesel Generator is far more efficient than a row of small ones."]),
    Q("t5_crack", 8, 0, [item(MI + "steam_cracked_naphtha_bucket")], "Steam Cracking", deps=["t5_hydrotreat"], xp=200,
      subtitle="Break big molecules into useful small ones", desc=[
        "&eWhat:&r naphtha is too big to make plastic from. Cracking breaks it into the small building blocks chemists actually want.",
        "&eChemistry:&r at high temperature with steam, long chains snap apart into short, reactive molecules with double bonds (alkenes).",
        "&eHow:&r Chemical Reactor: 1000 mB naphtha + 100 mB steam → 1000 mB steam-cracked naphtha."]),
    Q("t5_ethylene", 10, 0, [item(MI + "ethylene_bucket")], "Ethylene", deps=["t5_crack"], xp=150,
      subtitle="C₂H₄, the most important molecule in plastics", desc=[
        "&eWhat:&r distilling cracked naphtha gives eight products: methane, acetylene, &eethylene&r, propene, butadiene, benzene, toluene and ethylbenzene.",
        "&eChemistry:&r ethylene's C=C double bond can open up and link to its neighbours. That is how plastics are born.",
        "&eHow:&r send steam-cracked naphtha through the Distillation Tower (more layers give more outputs; all eight need the full tower).",
        "&eTip:&r store every fraction. Each one has a use later in this chapter."]),
    Q("t5_pe", 12, 0, [item(MI + "polyethylene_bucket")], "Polymerisation", deps=["t5_ethylene"], xp=250,
      subtitle="Thousands of ethylenes, one long chain", desc=[
        "&eWhat:&r polyethylene, (C₂H₄)ₙ, is the plastic in bags and bottles, and the laminate on HV circuit boards.",
        "&eChemistry:&r a metal catalyst opens each double bond so the molecules join head to tail. Real plants use chromium (Phillips) or titanium catalysts.",
        "&eHow:&r Chemical Reactor: 500 mB ethylene + 4 tiny lead or chromium dust → 300 mB polyethylene."]),
    Q("t5_hdpe", 12, -2, [item("mekanism:hdpe_pellet", 8)], "HDPE", deps=["t5_pe"], xp=150,
      subtitle="Mekanism's plastic, from your ethylene", desc=[
        "&eWhat:&r high-density polyethylene pellets become Mekanism's plastic sheets, rods and later the MekaSuit.",
        "&eChemistry:&r HDPE has straight chains that pack tightly, so it's stiffer than ordinary polyethylene.",
        "&eHow:&r Pressurized Reaction Chamber with ethylene, water and substrate (check JEI)."]),
    # ---------------------------------------------------------------- stainless steel
    Q("t5_chromium", 8, -4, [item(MI + "chromium_dust", 4), item(MI + "manganese_dust", 4)], "Chromium and Manganese", deps=["t4_mv"], xp=150,
      subtitle="The metals that keep steel from rusting", desc=[
        "&eWhat:&r stainless steel needs chromium, nickel and manganese on top of iron.",
        "&eChemistry:&r chromium is leached with acid: crushed chromium + HCl → chromium chloride solution, then electrolysis splits out the metal plus H₂ and Cl₂.",
        "&eHow:&r Chemical Reactor (chromium crushed dust + 9 B HCl), then Electrolyzer. Check JEI for manganese."]),
    Q("t5_ss_dust", 10, -4, [item(MI + "stainless_steel_dust", 9)], "Stainless Steel Dust", deps=["t5_chromium"], xp=100,
      subtitle="Six parts iron, one each of Cr, Ni and Mn", desc=[
        "&eWhat:&r the mixed powder that becomes stainless steel.",
        "&eChemistry:&r at 10.5% chromium or more, the surface forms an invisible Cr₂O₃ film that stops rust spreading.",
        "&eHow:&r Mixer: 6 iron dust + 1 chromium + 1 nickel + 1 manganese → 9 stainless steel dust."]),
    Q("t5_freezer", 12, -4, [item(MI + "vacuum_freezer"), item(MI + "stainless_steel_hot_ingot")], "Hot Ingots", deps=["t5_ss_dust"], xp=200,
      subtitle="Too hot to handle, until you freeze it", desc=[
        "&eWhat:&r the Electric Blast Furnace melts the dust into a &ehot ingot&r that must be cooled before use.",
        "&eHow:&r EBF turns 1 stainless steel dust into 1 hot ingot. Build the Vacuum Freezer multiblock (layout in JEI) to cool it.",
        "&eTip:&r later, the Heat Exchanger cools hot ingots too and gives argon and helium back."]),
    Q("t5_ebf", 14, -4, [item(MI + "stainless_steel_ingot", 8)], "Stainless Steel", deps=["t5_freezer", "t3_ebf"], xp=200,
      subtitle="The metal that survives acid", desc=[
        "&eWhat:&r stainless steel resists corrosion, so it can hold acids and hot fluids.",
        "&eChemistry:&r if the surface is scratched, chromium re-forms the oxide film at once. The steel heals itself.",
        "&eHow:&r cool hot ingots in the Vacuum Freezer. HV circuit boards need 4 stainless plates each.",
        "&eTip:&r automate the whole line: mixer → EBF → freezer → compressor."]),
    # ---------------------------------------------------------------- HV
    Q("t5_dcb", 14, 0, [item(MI + "digital_circuit_board")], "Digital Circuit Board", deps=["t5_pe", "t5_ebf"], xp=200,
      subtitle="Plastic, steel and silicon in one board", desc=[
        "&eWhat:&r the base of every HV circuit.",
        "&eChemistry:&r polyethylene is an excellent insulator, so it separates the copper layers of the board.",
        "&eHow:&r Assembler: electronic circuit board + 4 stainless steel plates + silicon battery + 6 aluminum cable + 750 mB polyethylene."]),
    Q("t5_sodium", 16, -2, [item(MI + "sodium_battery", 2)], "Sodium Battery", deps=["t4_sodium"], xp=150,
      subtitle="Table salt becomes a battery", desc=[
        "&eWhat:&r the HV hull needs two sodium batteries.",
        "&eChemistry:&r sodium metal gives up its one outer electron very easily (it fizzes in water), which is what makes it a good battery material.",
        "&eHow:&r sodium dust from the Electrolyzer (2 salt dust → 1 sodium dust + chlorine), as in Electrochemistry. Then craft the battery (check JEI).",
        "&eTip:&r keep the chlorine. It's needed for HCl and, next chapter, PVC."]),
    Q("t5_hv", 16, 0, [item(MI + "digital_circuit"), item(MI + "turbo_machine_hull")], "HV: Digital Circuits", deps=["t5_dcb", "t5_sodium", "t5_gates"], xp=300, size=1.5,
      items=[(MI + "digital_circuit", 2)], subtitle="High Voltage, built on plastic", desc=[
        "&6Logic gates, clicking into place. You used to think this fast.&r",
        "&eWhat:&r digital circuits unlock HV machines, AE2, the Angel Ring and elite jetpack coils.",
        "&eHow:&r Assembler: digital circuit board + 4 electronic circuits + AND, OR and NOT gates. The &eTurbo hull&r adds 2 sodium batteries and aluminum cable.",
        "&eTip:&r set up a dedicated assembler for circuits. You'll make hundreds."]),
    # ---------------------------------------------------------------- AE2
    Q("t5_meteor", 18, 2, [item("ae2:meteorite_compass"), item("ae2:engineering_processor_press"), item("ae2:silicon_press")], "Fallen Stars", deps=["t5_hv"], xp=200,
      subtitle="Meteorites hide the presses AE2 needs", desc=[
        "&eWhat:&r AE2's inscriber presses are only found in the core of meteorites.",
        "&eHow:&r craft a Meteorite Compass, follow it, and dig to the centre of the sky stone crater. Each meteorite's mysterious cube holds one press.",
        "&eTip:&r once you have one press, the Inscriber can copy it with an iron block."]),
    Q("t5_fluix", 18, -2, [item("ae2:charger"), item("ae2:fluix_crystal", 8)], "Fluix", deps=["t5_hv"], xp=150,
      subtitle="Charged quartz for the network", desc=[
        "&eWhat:&r fluix crystals carry the ME network's signal. The ME Controller needs them.",
        "&eHow:&r charge certus quartz in the Charger, then drop charged certus, redstone and Nether quartz in water together (check JEI).",
        "&eTip:&r budding certus quartz grows new crystals, so certus is renewable once you find some."]),
    Q("t5_inscriber", 18, 0, [item("ae2:inscriber"), item("ae2:engineering_processor", 2)], "The Inscriber", deps=["t5_hv", "t5_meteor"], xp=200,
      subtitle="Printing circuits onto silicon", desc=[
        "&eWhat:&r every AE2 processor is printed in the Inscriber. In this pack it's built on a Turbo hull.",
        "&eChemistry:&r engineering processors print a circuit onto silicon, the same element your HV boards depend on.",
        "&eHow:&r press a diamond into a printed engineering circuit, silicon into printed silicon, then combine them with redstone.",
        "&eTip:&r the silicon is your MI silicon from the EBF. AE2's certus-to-silicon smelting is removed in this pack."]),
    Q("t5_ae2", 20, 0, [item("ae2:controller")], "The God's Archive", deps=["t5_inscriber", "t5_fluix"], xp=400, size=1.75, shape="hexagon",
      items=[("ae2:drive", 1)], subtitle="Your memory, rebuilt as a network", desc=[
        "&6Everything you own, known at once and found in an instant. Your memory used to work like this; now it lives in a network you built.&r",
        "&eWhat:&r Applied Energistics 2 stores items as data and crafts on demand.",
        "&eHow:&r the ME Controller needs a digital circuit, an engineering processor, fluix and smooth sky stone.",
        "&eTip:&r Tom's Simple Storage was your early network. AE2 takes over from here (see the Applied Energistics page in Engineering)."]),
    Q("t5_cells", 22, 0, [item("ae2:item_storage_cell_1k", 2), item("ae2:fluid_storage_cell_1k")], "First Storage Cells", deps=["t5_ae2"], xp=150,
      optional=True, tokens=1, subtitle="Optional: where the archive keeps its memories", desc=[
        "&eWhat:&r storage cells go into an ME Drive. Fluid cells hold your acids and fuels as data too.",
        "&eHow:&r a 1k cell component needs a logic processor (gold + logic press). Check JEI for the housing.",
        "&eTip:&r a few fluid cells beat a wall of tanks for small stocks of rare chemicals."]),
    Q("t5_twilight", 16, 3, [dim("twilightforest:twilight_forest")], "The Twilight Forest", deps=["t5_hv"], xp=300,
      subtitle="A realm of permanent dusk", desc=[
        "&6A forest held forever at dusk. Even a god can get lost here, which is half the fun.&r",
        "&eWhat:&r a dimension of bosses, strange woods and unique metals (see the Twilight Forest page in Exploration).",
        "&eHow:&r dig a 2x2 pool of water ringed with flowers, stand in it, and throw in a diamond.",
        "&eTip:&r set a waystone near the portal before you explore."]),
    # ---------------------------------------------------------------- synthetic rubber
    Q("t5_aromatics", 8, 2, [item(MI + "benzene_bucket"), item(MI + "toluene_bucket")], "Benzene Rings", deps=["t5_crack"], xp=150,
      optional=True, tokens=1, subtitle="Optional: the hexagon at the heart of organic chemistry", desc=[
        "&eWhat:&r benzene (C₆H₆) and toluene (C₇H₈) come out of the cracked-naphtha distillation.",
        "&eChemistry:&r benzene is a flat ring of six carbons whose electrons are shared around the whole ring. That makes it unusually stable.",
        "&eHow:&r collect them from the Distillation Tower's benzene and toluene outputs.",
        "&eTip:&r benzene also makes dyes and, via caprolactam, nylon."]),
    Q("t5_styrene", 10, 2, [item(MI + "ethylbenzene_bucket"), item(MI + "styrene_bucket")], "Styrene", deps=["t5_aromatics"], xp=150,
      optional=True, tokens=1, subtitle="Optional: add ethylene, then strip off hydrogen", desc=[
        "&eChemistry:&r benzene + ethylene → ethylbenzene (acid catalyst). Steam over iron then pulls off H₂ to give styrene, C₈H₈, exactly as in real plants.",
        "&eHow:&r Chemical Reactor: benzene + ethylene + a little HCl → ethylbenzene. Then ethylbenzene + steam + iron dust → styrene + hydrogen.",
        "&eTip:&r the hydrogen by-product can go straight back into hydrotreating."]),
    Q("t5_sbr", 12, 2, [item(MI + "styrene_butadiene_rubber_bucket")], "Synthetic Rubber", deps=["t5_styrene", "t5_opt_butadiene"], xp=200,
      optional=True, tokens=1, subtitle="Optional: car-tyre rubber, made from oil", desc=[
        "&eWhat:&r styrene-butadiene rubber (SBR) is the rubber in most tyres. Here it makes rubber sheets by the stack.",
        "&eChemistry:&r styrene and butadiene polymerise together into one chain (a copolymer): stiff styrene parts, springy butadiene parts.",
        "&eHow:&r Chemical Reactor: styrene + butadiene → styrene-butadiene, then polymerise with tiny lead or chromium dust. The Vacuum Freezer turns 200 mB into 64 rubber sheets.",
        "&eTip:&r far more rubber per batch than your old coke-oil rubber line, and it feeds the better cable recipes."]),
    # ---------------------------------------------------------------- optional side quests
    Q("t5_opt_tools", 6, -4, [item(MI + "diesel_mining_drill"), item(MI + "diesel_jetpack")], "Diesel Toys", deps=["t5_diesel"], xp=100,
      optional=True, tokens=1, subtitle="Optional: fuel-powered tools", desc=[
        "&eWhat:&r MI's diesel drill and jetpack run on the fuel you just learned to blend.",
        "&eHow:&r check JEI for both recipes, then fill them from a tank.",
        "&eTip:&r the jetpack is loud and thirsty, but it flies. Real flight comes later."]),
    Q("t5_opt_biodiesel", 4, -2, [item(MI + "biodiesel_bucket")], "Fuel from Plants", deps=["t5_diesel"], xp=100,
      optional=True, tokens=1, subtitle="Optional: diesel without drilling", desc=[
        "&eChemistry:&r transesterification: plant oil + ethanol, with NaOH as catalyst, swaps the oil's glycerol backbone for ethyl groups. The result burns like diesel.",
        "&eHow:&r Chemical Reactor: plant oil + ethanol + sodium hydroxide → raw biodiesel, then wash it with steam (check JEI for plant oil).",
        "&eTip:&r Ad Astra rockets accept biodiesel too."]),
    Q("t5_opt_glue", 6, 2, [item(MI + "acrylic_acid_bucket"), item(MI + "acrylic_glue_bucket")], "Acrylic Glue", deps=["t5_crack"], xp=100,
      optional=True, tokens=1, subtitle="Optional: slime from propene", desc=[
        "&eChemistry:&r propene + oxygen → acrylic acid + water. Polymerised, it becomes a sticky acrylic: the same family as superabsorbent polymers.",
        "&eHow:&r Chemical Reactor for the acid, then polymerise with tiny lead or chromium dust.",
        "&eTip:&r the Chemical Reactor can turn acrylic glue into slime balls. No more slime farms."]),
    Q("t5_opt_nylon", 8, 4, [item(MI + "caprolactam_bucket"), item(MI + "nylon_bucket")], "Nylon", deps=["t5_aromatics"], xp=100,
      optional=True, tokens=1, subtitle="Optional: string from benzene", desc=[
        "&eChemistry:&r benzene + hydrogen over nickel leads to caprolactam, a ring that opens up and polymerises into nylon-6.",
        "&eHow:&r Chemical Reactor: benzene + hydrogen + tiny nickel dust → caprolactam, then polymerise it.",
        "&eTip:&r 20 mB of nylon makes one string in the Chemical Reactor."]),
    Q("t5_opt_rubber", 12, 4, [item(MI + "rubber_sheet", 256)], "A Mountain of Rubber", deps=["t5_sbr"], xp=150,
      optional=True, tokens=1, subtitle="Optional: stockpile challenge", desc=[
        "&eHow:&r keep the SBR line and Vacuum Freezer running until you have 256 sheets.",
        "&eWhat:&r four full stacks of rubber sheets, made the modern way.",
        "&eTip:&r one bucket of SBR is five freezer runs, so a single bucket gets you there."]),

    # ---------------------------------------------------------------- ATM10-aligned additions (2026-10-19)
    Q("t5_pipe_casing", 0, 0, [item(MI + "steel_machine_casing_pipe", 4)], "Pipe Casings", deps=["t5_oil"], xp=60,
      subtitle="The tower's hollow core", desc=[
        "&eWhat:&r steel pipe machine casings form the inside of the Distillation Tower, where the vapours rise.",
        "&eHow:&r a steel machine casing wrapped in 6 steel curved plates gives 2 pipe casings (crafting table or Assembler).",
        "&eTip:&r a taller tower needs more of them. Check the layout in JEI before you craft."]),
    Q("t5_gates", 0, 0, [item(MI + "op_amp", 2), item(MI + "and_gate"), item(MI + "or_gate"), item(MI + "not_gate")], "Logic Gates", deps=["t5_dcb"], xp=150,
      subtitle="AND, OR, NOT: the grammar of thought", desc=[
        "&eWhat:&r every digital circuit needs one AND, one OR and one NOT gate, and every gate starts with an operational amplifier.",
        "&eChemistry:&r a transistor is a switch with no moving parts. Wire a few together and they answer yes-or-no questions; wire millions and you have a computer.",
        "&eHow:&r Assembler. Op amp: 4 resistors, 4 transistors, 1 diode. AND: 2 resistors, 1 op amp, 4 aluminum wire. OR: 2 op amps, 2 aluminum wire, 1 diode. NOT: 1 resistor, 1 op amp, 1 aluminum wire.",
        "&eTip:&r set one Assembler per gate type. Digital circuits eat them by the dozen."]),
    Q("t5_opt_distillery", 0, 0, [item(MI + "distillery")], "The Distillery", deps=["t5_oil"], xp=75,
      optional=True, tokens=1, subtitle="Optional: one fraction at a time", desc=[
        "&eWhat:&r a single-block still that pulls just one fraction out of a fluid. Cheaper than the tower, slower and wasteful.",
        "&eChemistry:&r a pot still works by boiling point too, but with only one stage it can't separate everything at once.",
        "&eHow:&r LV machine hull, 2 large pumps, 2 electronic circuits, glass, a fluid pipe and electrum cable.",
        "&eTip:&r good for a side fluid you only need a little of, like one fraction of cracked naphtha."]),
    Q("t5_opt_crushed", 0, 0, [item(MI + "chromium_crushed_dust", 2), item(MI + "manganese_crushed_dust", 2)], "Chromium and Manganese Ores", deps=["t5_chromium"], xp=75,
      optional=True, tokens=1, subtitle="Optional: where the crushed dust comes from", desc=[
        "&eWhat:&r the raw material for the chromium and manganese leaching lines.",
        "&eChemistry:&r ruby is aluminium oxide coloured red by chromium, so it hides chromium. Iron ores usually carry a little manganese.",
        "&eHow:&r Centrifuge: 6 ruby dust → 1 chromium crushed dust + 2 aluminum dust (ruby dust comes from centrifuging redstone). Centrifuge: 6 raw iron → 8 iron dust + 1 manganese crushed dust."]),
    Q("t5_opt_casings", 0, 0, [item(MI + "heatproof_machine_casing", 4), item(MI + "frostproof_machine_casing", 4)], "Hot and Cold Casings", deps=["t5_freezer"], xp=60,
      optional=True, tokens=1, subtitle="Optional: invar for heat, aluminum for cold", desc=[
        "&eWhat:&r heatproof casings wall in your Blast Furnace; frostproof casings wall in the Vacuum Freezer. The Heat Exchanger needs both.",
        "&eChemistry:&r invar (iron with 36% nickel) barely expands when heated. Aluminium stays tough in the cold, where steel turns brittle.",
        "&eHow:&r 8 invar plates + an invar gear, or 8 aluminum plates + an aluminum gear (Assembler or crafting table)."]),
    Q("t5_opt_up_adv", 0, 0, [item(MI + "advanced_upgrade", 4)], "Advanced Upgrades", deps=["t5_pe"], xp=75,
      optional=True, tokens=1, subtitle="Optional: four basic upgrades, made better", desc=[
        "&eWhat:&r a bigger EU/t boost per slot than basic upgrades.",
        "&eHow:&r Assembler: 4 basic upgrades, 2 large motors, a large pump, an electronic circuit board and 1000 mB polyethylene → 4 advanced upgrades."]),
    Q("t5_opt_cracked_light", 0, 0, [item(MI + "steam_cracked_light_fuel_bucket")], "Cracking Light Fuel", deps=["t5_crack"], xp=60,
      optional=True, tokens=1, subtitle="Optional: crack the fuel, not just the naphtha", desc=[
        "&eWhat:&r light fuel can be steam-cracked too, and the cracked fuel distils into another mix of small molecules.",
        "&eChemistry:&r cracking breaks long chains into short ones. Refineries crack whatever fraction the market wants less of into what it wants more of.",
        "&eHow:&r steam + light fuel in the cracker (check JEI), then send it through the Distillation Tower."]),
    Q("t5_opt_butadiene", 0, 0, [item(MI + "butadiene_bucket"), item(MI + "styrene_butadiene_bucket")], "Butadiene", deps=["t5_styrene"], xp=75,
      optional=True, tokens=1, subtitle="Optional: the springy half of synthetic rubber", desc=[
        "&eWhat:&r butadiene (C₄H₆) is the second monomer of SBR rubber.",
        "&eChemistry:&r two double bonds make it springy once polymerised. Before oil, Soviet plants made it from ethanol (the Lebedev process); MI can too.",
        "&eHow:&r Chemical Reactor: 750 mB ethanol + a tiny aluminum dust, or distil it out of cracked naphtha or cracked fuels (check JEI). Then styrene + butadiene → styrene-butadiene."]),
    Q("t5_opt_shale", 0, 0, [item(MI + "sulfuric_crude_oil_bucket")], "Shale Oil", deps=["t5_hydrotreat", "t5_ebf"], xp=100,
      optional=True, tokens=1, subtitle="Optional: sour crude and a breath of helium", desc=[
        "&eWhat:&r the Oil Drilling Rig, fed stainless steel drills instead of aluminum ones, brings up shale oil. Distilled, it gives sour (sulfuric) crude, sulfuric naphtha and a little helium.",
        "&eChemistry:&r sour crude is full of sulfur compounds. Hydrotreating strips them out with hydrogen, the same way your fuels are cleaned: 12 B sour crude + 2 B H₂ → 12 B crude oil + 2 B sulfuric acid.",
        "&eTip:&r real helium is mined from natural gas wells, where it collects from uranium decay. Keep this helium; you'll want it later."]),
    Q("t5_opt_array", 0, 0, [item("extended_industrialization:processing_array"), item(MI + "clean_stainless_steel_machine_casing", 2)], "Processing Array", deps=["t5_hv"], xp=100,
      optional=True, tokens=1, subtitle="Optional: many machines, one controller", desc=[
        "&eWhat:&r an Extended Industrialization multiblock that holds a stack of identical machines and runs them as one.",
        "&eHow:&r an Assembler, 4 robot arms, 2 digital circuits and 2 clean stainless steel casings (8 stainless plates + a stainless gear each). Check JEI for the layout and what it accepts.",
        "&eTip:&r one array of 16 macerators beats 16 macerators on cables."]),
])
