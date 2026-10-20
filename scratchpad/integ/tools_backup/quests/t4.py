"""Quest chapter: t4. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, anytag, MAIN, SIDE  # noqa: F401

MI = "modern_industrialization:"
MEK = "mekanism:"

CHAPTER = Chapter("t4", "V. Electrochemistry and Acids", "modern_industrialization:sulfuric_acid_bucket",
        ["Electricity splits compounds into elements. Acids dissolve what fire can't.",
         "Ore processing becomes chemistry."], MAIN, [
    # ===== Upper line: Mekanism gases and the contact process (LV) =====
    Q("t4_separator", 0, -2, [item(MEK + "electrolytic_separator")], "Mekanism Gases", deps=["t4_electrolytic_core"], section="Gas Chemistry", xp=100,
      subtitle="Split water into hydrogen and oxygen", desc=[
        "&6Once a word was enough to pull water apart. Now it takes a machine and a cable, and that will have to do.&r",
        "&eWhat:&r the Electrolytic Separator makes hydrogen and oxygen as gases you can pipe and store.",
        "&eChemistry:&r 2H₂O → 2H₂ + O₂. Current drives the reaction backwards from burning hydrogen.",
        "&eHow:&r feed it water and FE. Gases leave from the coloured sides (configure them with the Configurator)."]),
    Q("t4_tubes", 2, -1, [item(MEK + "basic_pressurized_tube", 16)], "Pressurized Tubes", deps=["t4_separator"], xp=30,
      subtitle="Pipes for gases", desc=[
        "&eWhat:&r gases need sealed tubes. Item pipes and fluid pipes won't carry them.",
        "&eHow:&r craft basic pressurized tubes (see JEI) and run them from the separator's outputs.",
        "&eTip:&r vent what you don't need yet. A full output tank stops the whole separator."]),
    Q("t4_sulfur", 2, -3, [item(MI + "sulfur_dust", 8)], "A Source of Sulfur", deps=["t3_emacerator"], section="The Contact Process", xp=40,
      subtitle="Yellow brimstone for the contact process", desc=[
        "&eWhat:&r sulfur is where sulfuric acid starts.",
        "&eChemistry:&r S is element 16. Volcanoes and fossil fuels are full of it; most industrial sulfur is stripped out of oil and gas.",
        "&eHow:&r macerate crushed lignite coal (about half the time you get sulfur dust), or centrifuge lava later. Press U on Sulfur Dust in JEI for all sources."]),
    Q("t4_oxidizer", 4, -2, [item(MEK + "chemical_oxidizer")], "Contact Process 1: SO₂", deps=["t4_tubes", "t4_sulfur", "t4_dynamic_tank"], xp=100,
      subtitle="Burn sulfur into sulfur dioxide", desc=[
        "&eWhat:&r the Chemical Oxidizer turns a solid into a gas. Sulfur dust becomes sulfur dioxide.",
        "&eChemistry:&r S + O₂ → SO₂. It's the sharp smell of a struck match.",
        "&eHow:&r one sulfur dust gives 100 mB of SO₂. Pipe it out with pressurized tubes."]),
    Q("t4_so3", 6, -2, [item(MEK + "chemical_infuser")], "Contact Process 2: SO₃", deps=["t4_oxidizer"], xp=100,
      subtitle="Sulfur dioxide + oxygen", desc=[
        "&eWhat:&r the Chemical Infuser combines two gases. SO₂ plus oxygen from your separator gives sulfur trioxide.",
        "&eChemistry:&r 2SO₂ + O₂ → 2SO₃. Real plants pass the gases over a vanadium oxide (V₂O₅) catalyst at about 450 °C: the 'contact' in the name.",
        "&eHow:&r SO₂ in one side, O₂ in the other."]),
    Q("t4_vapor", 6, -4, [item(MEK + "rotary_condensentrator")], "Water Vapor", deps=["t4_so3", "t4_energy_tablet", "t4_chem_tank"], xp=60,
      subtitle="Turn water into a gas Mekanism can use", desc=[
        "&eWhat:&r the Rotary Condensentrator converts fluids to gases and back. It turns water into water vapor.",
        "&eHow:&r set it to gas mode (the toggle in its GUI), pipe water in and pressurized tube out.",
        "&eTip:&r it also turns Mekanism gases into buckets, which is handy for storage and trading."]),
    Q("t4_mek_acid", 8, -2, [tick()], "Contact Process 3: H₂SO₄", deps=["t4_so3", "t4_vapor"], xp=150,
      subtitle="SO₃ + water vapor in a second infuser", desc=[
        "&eWhat:&r a second Chemical Infuser combines SO₃ with water vapor into sulfuric acid gas. Tick this when acid is flowing.",
        "&eChemistry:&r SO₃ + H₂O → H₂SO₄. Real plants dissolve SO₃ in existing acid first (oleum), because SO₃ and water alone make a corrosive mist.",
        "&eTip:&r store the acid in a chemical tank. The 5x ore line drinks it."]),

    # ===== Chlorine and HCl =====
    Q("t4_salt", 0, -6, [item(MI + "salt_dust", 16)], "Salt", deps=["t3_emacerator"], section="Chlor-Alkali", xp=40,
      subtitle="Sodium chloride, NaCl", desc=[
        "&eWhat:&r salt is the start of the chlor-alkali industry: chlorine, sodium and everything made from them.",
        "&eChemistry:&r NaCl is an ionic crystal: Na⁺ and Cl⁻ held together by charge. Split it and you get a soft, reactive metal and a toxic green gas.",
        "&eHow:&r MI salt ore is found underground and drops salt dust."]),
    Q("t4_brine", 2, -6, [tick()], "Brine", deps=["t4_salt", "t4_oxidizer"], xp=60,
      subtitle="Salt dissolved in water", desc=[
        "&eWhat:&r brine is salty water, and Mekanism splits it into chlorine. Tick this when you have brine.",
        "&eHow:&r put salt dust in a Chemical Oxidizer (15 mB brine per dust), or build a Thermal Evaporation Plant (see the side quest).",
        "&eTip:&r a second oxidizer just for salt saves you from swapping inputs."]),
    Q("t4_chlorine", 4, -6, [tick()], "Chlorine", deps=["t4_brine", "t4_separator"], xp=75,
      subtitle="Electrolyse brine into Cl₂ and sodium", desc=[
        "&eWhat:&r the Electrolytic Separator also takes brine. Out come chlorine and sodium. Tick this when chlorine is flowing.",
        "&eChemistry:&r real brine electrolysis gives Cl₂ at one electrode and H₂ + NaOH at the other. Mekanism simplifies it to sodium + chlorine.",
        "&eTip:&r use a second separator so your hydrogen and oxygen line keeps running."]),
    Q("t4_hcl", 6, -6, [tick()], "Hydrogen Chloride", deps=["t4_chlorine", "t4_so3"], xp=100,
      subtitle="H₂ + Cl₂ in a Chemical Infuser", desc=[
        "&eWhat:&r hydrogen chloride drives the 4x ore line. Tick this when HCl is flowing.",
        "&eChemistry:&r H₂ + Cl₂ → 2HCl. Dissolved in water it's hydrochloric acid, the same acid in your stomach.",
        "&eHow:&r hydrogen in one side of a Chemical Infuser, chlorine in the other."]),

    # ===== Mekanism ore line: 3x, 4x, 5x =====
    Q("t4_ore3", 10, -4, [item(MEK + "purification_chamber")], "3x Ore: Oxygen", deps=["t4_separator", "t3_enrich", "t4_adv_circuit"], xp=150,
      subtitle="Purification Chamber + oxygen", desc=[
        "&eWhat:&r before acids, every route caps at &e2x&r per ore. Purifying ore with oxygen gives &e3x&r. The chamber needs advanced control circuits, which are built on MI's electronic circuit.",
        "&eHow:&r ore + O₂ → 3 clumps. Crusher: clumps → dirty dust. Enrichment Chamber: dirty dust → dust.",
        "&eTip:&r Mekanism shows each step in JEI. Chain them with pipes and side configuration."]),
    Q("t4_ore4", 12, -4, [item(MEK + "chemical_injection_chamber")], "4x Ore: Hydrogen Chloride", deps=["t4_ore3", "t4_hcl", "t4_reinforced"], xp=200,
      subtitle="Chemical Injection Chamber + HCl", desc=[
        "&eWhat:&r injecting hydrogen chloride splits ore into shards: &e4x&r.",
        "&eHow:&r ore + HCl → 4 shards. Purification Chamber: shards → clumps, then on through your 3x line.",
        "&eTip:&r your 3x machines are now the back half of the 4x line. Nothing is wasted."]),
    Q("t4_dissolution", 14, -5, [item(MEK + "chemical_dissolution_chamber")], "Dissolving Ore", deps=["t4_ore4", "t4_mek_acid", "t4_refined_obsidian"], xp=150,
      subtitle="Ore + sulfuric acid → dirty slurry", desc=[
        "&eWhat:&r the Dissolution Chamber dissolves ore in sulfuric acid, giving a dirty slurry.",
        "&eChemistry:&r acid leaching: H₂SO₄ turns metal minerals into soluble sulfates, leaving the rock behind.",
        "&eHow:&r feed it ore and sulfuric acid gas. The slurry comes out as a chemical."]),
    Q("t4_washer", 14, -3, [item(MEK + "chemical_washer")], "Washing Slurry", deps=["t4_dissolution"], xp=100,
      subtitle="Dirty slurry + water → clean slurry", desc=[
        "&eWhat:&r the Chemical Washer rinses impurities out of the slurry.",
        "&eChemistry:&r washing removes the dissolved gangue (waste rock) so only the metal salt is left to crystallise.",
        "&eHow:&r slurry in, water in, clean slurry out. An MI electric water pump keeps the water coming."]),
    Q("t4_ore5", 16, -4, [item(MEK + "chemical_crystallizer")], "5x Ore: Dissolution", deps=["t4_washer", "t4_fluorite"], xp=300, size=1.5,
      subtitle="Crystallise the slurry: five from one", desc=[
        "&6Five from one. You used to call that a small miracle. Now you call it hydrometallurgy.&r",
        "&eWhat:&r the Chemical Crystallizer turns clean slurry into crystals: &e5x&r per ore.",
        "&eChemistry:&r this is &ehydrometallurgy&r, the way most of the world's copper is really refined.",
        "&eHow:&r crystals → Injection Chamber (shards) → Purification Chamber (clumps) → Crusher → Enrichment Chamber.",
        "&eTip:&r the Crystallizer itself needs fluorite gems: Mekanism's fluorite ore sits deep underground (check JEI for the recipe)."]),
    Q("t4_byproduct", 18, -4, [item(MI + "silver_dust", 4)], "Ore Byproducts", deps=["t4_ore5", "t4_centrifuge"], xp=200,
      optional=True, tokens=1, subtitle="Dirty dust through a centrifuge", desc=[
        "&eWhat:&r real ores are never pure. Send Mekanism's &edirty dust&r through MI's &eCentrifuge&r instead of the Enrichment Chamber for the same dust plus a chance at a bonus metal.",
        "&eChemistry:&r iron → nickel, copper → gold, gold → silver, &elead → silver&r (galena), tin → tungsten, osmium → iridium, uranium → lead (decay).",
        "&eHow:&r route dirty dust to your Centrifuge instead of the Enrichment Chamber. Silver from lead (or gold) dirty dust ticks this quest."]),

    # ===== Lower line: aluminum (Bayer + Hall-Héroult), silicon and the electronic circuit (LV → MV) =====
    Q("t4_bauxite", -8, 2, [item(MI + "bauxite_dust", 16)], "Bauxite", deps=["t3_ebf"], section="Aluminium: Bayer and Hall-Héroult", xp=40,
      subtitle="The ore aluminum hides in", desc=[
        "&6An emperor once served his finest guests on this metal. You knew even then it was never rare, only stubborn.&r",
        "&eWhat:&r bauxite is the only practical aluminum ore. MI bauxite ore drops bauxite dust.",
        "&eChemistry:&r bauxite is mostly aluminium hydroxides, Al(OH)₃ and AlO(OH), stained red by iron oxide.",
        "&eHow:&r rich bauxite deposits sit around Y -16 to 24. No furnace will free the metal: it goes through the Bayer process first."]),
    Q("t4_lye_bayer", -8, 0, [item(MI + "sodium_hydroxide_bucket")], "Lye for the Digester", deps=["t3_mixer", "t1_combiner"], xp=60,
      subtitle="Sodium hydroxide from the Combiner", desc=[
        "&eWhat:&r the Bayer process dissolves bauxite in hot lye, so you need sodium hydroxide solution first.",
        "&eChemistry:&r NaOH is a strong base: it fully splits into Na⁺ and OH⁻ in water, and OH⁻ is what pulls aluminium into solution.",
        "&eHow:&r combine Na + O + H in the Alchemistry Combiner (check JEI on Sodium Hydroxide), then Mixer: 1 crystal + 250 mB water → 250 mB lye.",
        "&eTip:&r the digester gives most of the lye back, so a few crystals go a long way. Later the Chemical Reactor makes it in bulk."]),
    Q("t4_bayer_digest", -6, 2, [item(MI + "sodium_aluminate_solution_bucket")], "Bayer Digestion", deps=["t4_bauxite", "t4_lye_bayer"], xp=80,
      subtitle="Dissolve the aluminium, leave the rust", desc=[
        "&eWhat:&r the first step of every aluminium refinery since 1888: hot lye dissolves the aluminium out of bauxite.",
        "&eChemistry:&r Al(OH)₃ + NaOH → NaAl(OH)₄ (sodium aluminate). Iron and titanium oxides don't dissolve; they settle out as 'red mud'.",
        "&eHow:&r Mixer: 4 bauxite dust + 1000 mB lye → 1000 mB sodium aluminate solution + 2 tiny iron dust + 1 tiny titanium dust.",
        "&eTip:&r pipe the solution straight into the next Mixer; a bucket is only needed for this quest."]),
    Q("t4_bayer_precip", -4, 2, [item("chemlib:aluminum_hydroxide_dust", 8)], "Precipitation", deps=["t4_bayer_digest"], xp=60,
      subtitle="Cool, dilute, and crystals fall out", desc=[
        "&eWhat:&r pure aluminium hydroxide, crystallised back out of the solution, with the lye recovered.",
        "&eChemistry:&r NaAl(OH)₄ → Al(OH)₃ + NaOH. Diluting the liquor makes the reaction run backwards; the impurities stayed behind in the red mud.",
        "&eHow:&r Mixer: 1000 mB sodium aluminate + 1000 mB water → 4 aluminium hydroxide dust + 900 mB lye.",
        "&eTip:&r loop the 900 mB of lye back into the digester. That loop is why the Bayer process is cheap."]),
    Q("t4_alumina", -2, 2, [item("chemlib:aluminum_oxide_dust", 4)], "Alumina", deps=["t4_bayer_precip"], xp=60,
      subtitle="Bake out the water", desc=[
        "&eWhat:&r alumina (aluminium oxide) is the white powder that actually goes into the smelter.",
        "&eChemistry:&r calcination: 2Al(OH)₃ → Al₂O₃ + 3H₂O at around 1000 °C. Alumina also makes sapphire and ruby, coloured by traces of iron, titanium or chromium.",
        "&eHow:&r Electric Blast Furnace: 2 aluminium hydroxide dust → 1 alumina dust."]),
    Q("t4_hallheroult", 0, 2, [item(MI + "hall_heroult_cell")], "The Hall-Héroult Cell", deps=["t4_alumina", "t4_steel_large"], xp=150, size=1.5, shape="hexagon",
      subtitle="Electrolyse molten alumina", desc=[
        "&eWhat:&r a multiblock smelter that splits alumina with electricity. It's built from steel and LV parts, because it's what makes your first aluminium.",
        "&eChemistry:&r alumina melts at 2072 °C, far too hot. Dissolved in molten cryolite it melts near 950 °C. Current then splits it: 2Al₂O₃ + 3C → 4Al + 3CO₂, burning the carbon anode away.",
        "&eHow:&r controller from steel large plates, analog circuits, cupronickel coils and an LV hull. Check JEI (press U on the controller) for the 3x3x3 shape: steel casings top and bottom, a ring of cupronickel coils with the controller in the middle layer.",
        "{@pagebreak}",
        "&eHistory:&r Charles Martin Hall (USA) and Paul Héroult (France) found the process independently in 1886, both in their early twenties. Within about ten years the price of aluminium fell by more than 90%.",
        "&eNote:&r every primary aluminium smelter on Earth still uses it, and the cells draw a few percent of the world's electricity."]),
    Q("t4_aluminum", 2, 2, [item(MI + "aluminum_ingot", 8)], "Aluminum", deps=["t4_hallheroult"], xp=100,
      subtitle="Alumina + carbon → aluminum, in the cell", desc=[
        "&6The metal comes away bright and light in your hand. Some part of you is pleased it still had to work for it.&r",
        "&eWhat:&r aluminum is the metal of the MV tier: boards, rotors, casings, the Chemical Reactor and the Electrolyzer.",
        "&eChemistry:&r aluminium is the most common metal in the crust but clings to oxygen, so only electricity can pull it free.",
        "&eHow:&r Hall-Héroult Cell (LV power): 1 alumina dust + coke dust (the anode, used half the time) + a pinch of fluorite flux → 1 aluminum ingot.",
        "&eTip:&r 4 bauxite dust becomes 2 ingots. The cell only takes refined alumina dust, and no furnace will smelt aluminium dust: the Bayer line is the way in."]),
    Q("t4_alchemical_alumina", -2, 0, [tick()], "Fun Fact: No Shortcut", deps=["t4_alumina"], xp=40, optional=True, tokens=1,
      subtitle="Why fire can't free aluminium", desc=[
        "&eWhat:&r for decades aluminium cost more than silver, because nobody could pull it off its oxygen cheaply. Tick this once you've read why.",
        "&eChemistry:&r 4Al + 3O₂ → 2Al₂O₃ releases so much energy that thermite (Al + iron oxide) burns white-hot. Carbon grabs oxygen far less strongly, so coke in a furnace can't take it back from alumina.",
        "&eHow:&r that's why this pack has no furnace route for aluminium: the Hall-Héroult cell feeds in electricity instead, and it only accepts refined alumina dust from your Bayer line.",
        "&eTip:&r Napoleon III reportedly served his most honoured guests on aluminium plates. Everyone else made do with gold."]),
    Q("t4_electrum", 0, 4, [item(MI + "electrum_ingot", 4)], "Electrum", deps=["t3_mixer"], section="MV Components", xp=60,
      subtitle="Gold and silver, the ancient alloy", desc=[
        "&eWhat:&r electrum cable and fine wire go into every MV component.",
        "&eChemistry:&r electrum is a natural gold-silver alloy. The first coins, in Lydia around 600 BC, were struck from it.",
        "&eHow:&r mix gold and silver dust, then smelt. Check JEI (press R on Silver Dust) for silver ore in this pack."]),
    Q("t4_silicon", 2, 6, [item(MI + "silicon_ingot", 4)], "Silicon", deps=["t3_ebf", "t4_quartz_dust"], xp=100,
      subtitle="Quartz + carbon in the EBF", desc=[
        "&eWhat:&r silicon is the semiconductor every transistor and diode is built on.",
        "&eChemistry:&r SiO₂ + 2C → Si + 2CO. Carbon pulls the oxygen off quartz at furnace heat: carbothermic reduction.",
        "&eHow:&r macerate quartz into dust, then EBF: quartz dust + coke dust → silicon dust. Smelt it into ingots.",
        "&eTip:&r this is the only source of silicon in the pack. AE2's certus smelting and Mekanism's sand crushing are removed, so AE2 runs on this silicon too."]),
    Q("t4_ecboard", 4, 2, [item(MI + "electronic_circuit_board")], "Electronic Circuit Board", deps=["t4_al_plate", "t4_electrum_cable"], section="The Electronic Circuit", xp=60,
      subtitle="Aluminum, electrum and a battery", desc=[
        "&eWhat:&r the base for MV circuits.",
        "&eHow:&r an analog circuit board with aluminum plates, electrum cable and a redstone battery (see JEI).",
        "&eTip:&r the Assembler can make these too, once you stock it."]),
    Q("t4_transistor", 4, 4, [item(MI + "transistor", 2), item(MI + "diode", 2)], "Transistors and Diodes", deps=["t4_silicon_plate", "t4_fine_wire"], xp=75,
      subtitle="Semiconductors, finally", desc=[
        "&eWhat:&r diodes let current flow one way; transistors are switches controlled by current.",
        "&eChemistry:&r a pure silicon crystal barely conducts. Tiny amounts of other elements ('doping') make it conduct in controllable ways.",
        "&eHow:&r silicon plates, steel plates and electrum fine wire (diodes add glass)."]),
    Q("t4_circuit", 6, 3, [item(MI + "electronic_circuit", 2)], "Electronic Circuit", deps=["t4_ecboard", "t4_transistor"], xp=150,
      subtitle="The MV circuit", desc=[
        "&eWhat:&r the MV circuit. The Electrolyzer, Chemical Reactor and Centrifuge all need it, even though they sit on an LV hull.",
        "&eHow:&r electronic circuit board, 4 analog circuits, 2 diodes and 2 transistors.",
        "&eTip:&r set an Assembler to make these. You'll need dozens."]),
    Q("t4_electrolyzer", 8, 2, [item(MI + "electrolyzer")], "Electrolysis", deps=["t4_circuit", "t4_pumps"], xp=150,
      subtitle="MI's electrolysis machine", desc=[
        "&eWhat:&r pass current through a compound and it splits. This is &eelectrochemistry&r.",
        "&eChemistry:&r water → H₂ + O₂ (3000 mB water → 2000 mB H₂ + 1000 mB O₂). Salt → sodium + chlorine.",
        "&eHow:&r magnetic cupronickel wire, aluminum rods, an LV hull, an electronic circuit and a large pump."]),
    Q("t4_reactor", 8, 4, [item(MI + "chemical_reactor")], "The Chemical Reactor", deps=["t4_circuit", "t4_pumps"], xp=100,
      subtitle="MI's general-purpose reaction vessel", desc=[
        "&eWhat:&r combines items and fluids into new compounds. You'll use it constantly from here to the end.",
        "&eHow:&r glass, a large pump, aluminum rotors, an LV hull, electronic circuits and electrum cable.",
        "&eTip:&r MI fluids go in through pipes. A Configurable Tank holds spare H₂ and O₂."]),
    Q("t4_sodium", 10, 2, [item(MI + "sodium_dust", 4)], "Sodium", deps=["t4_electrolyzer", "t4_salt"], xp=75,
      subtitle="Electrolyse salt: sodium + chlorine", desc=[
        "&eWhat:&r sodium goes into the HV tier's sodium battery. The chlorine is a bonus.",
        "&eChemistry:&r 2NaCl → 2Na + Cl₂. Real sodium is made this way from molten salt (the Downs cell). It reacts violently with water.",
        "&eHow:&r Electrolyzer: 2 salt dust → 1 sodium dust + 125 mB chlorine."]),
    Q("t4_acid", 10, 4, [item(MI + "sulfuric_acid_bucket")], "Sulfuric Acid", deps=["t4_reactor", "t4_sulfur"], xp=250, size=1.75, shape="hexagon", items=[(MI + "sulfuric_acid_bucket", 2)],
      subtitle="The most-produced chemical on Earth", desc=[
        "&6Acid opens what fire cannot. You learned that once, the hard way, and the lesson has come back intact.&r",
        "&eWhat:&r sulfuric acid, as an MI fluid you can bucket. The Undergarden portal and many MI recipes need it.",
        "&eChemistry:&r S + O₂ + H₂O → &eH₂SO₄&r, the whole contact process in one vessel. Industry makes more of it than any other chemical.",
        "&eHow:&r Chemical Reactor: 1 sulfur dust + 200 mB O₂ + 200 mB water → 500 mB sulfuric acid."]),
    Q("t4_sibattery", 6, 6, [item(MI + "silicon_battery", 2)], "Silicon Battery", deps=["t4_ba_plates", "t4_electrum_cable", "t4_silicon"], xp=60,
      subtitle="The MV hull needs two", desc=[
        "&eWhat:&r the MV battery. Every MV hull holds two.",
        "&eHow:&r battery alloy plates, electrum cable and silicon dust.",
        "&eTip:&r make four. The Advanced (MV) hull uses two, and you'll want a second hull soon."]),
    Q("t4_mv", 8, 6, [item(MI + "electronic_circuit"), item(MI + "advanced_machine_hull")], "MV: Aluminum", deps=["t4_circuit", "t4_sibattery", "t4_adv_casing", "t4_electrum_cable"], section="The MV Hull", xp=250, size=1.5, items=[(MI + "electronic_circuit", 4)],
      subtitle="Medium Voltage: the MV machine hull", desc=[
        "&6The circuits are getting smaller and the power larger. So are you.&r",
        "&eWhat:&r the &eMV hull&r is the base for every MV machine, and Powah, Hostile Neural Networks and Extended Crafting all want MV circuits.",
        "&eHow:&r advanced machine casing (an LV hull wrapped in aluminum plates) + electronic circuit + 2 silicon batteries + electrum cable."]),
    Q("t4_uranium", 10, 8, [item(MI + "uranium_dust", 4)], "Uranium", deps=["t3_emacerator"], section="Uranium and the Undergarden", xp=60,
      subtitle="Deep, heavy and faintly warm", desc=[
        "&eWhat:&r uranium is the fuel of Powah's reactors and, much later, fission.",
        "&eChemistry:&r U is element 92, the heaviest element found in quantity in nature. It slowly decays into lead.",
        "&eHow:&r rich uranium deposits sit deep, around Y -56 to -24. Macerate the ore into dust."]),
    Q("t4_uraninite", 10, 6, [item("powah:energizing_orb"), item("powah:uraninite", 4)], "Uranium Dioxide", deps=["t4_mv", "t4_reactor", "t4_uranium"], xp=150,
      subtitle="Oxidise uranium in the Chemical Reactor", desc=[
        "&eWhat:&r uraninite fuels Powah's reactors. Powah's Energizing Orb needs an MV circuit.",
        "&eChemistry:&r uraninite is UO₂, the main ore of uranium in nature. Here you make it: U + O₂ → UO₂.",
        "&eHow:&r Chemical Reactor: uranium dust + 500 mB oxygen → uraninite. Powah's own uraninite ore is turned off."]),
    Q("t4_undergarden", 12, 4, [item("undergarden:catalyst"), dim("undergarden:undergarden")], "The Undergarden", deps=["t4_acid", "t4_mek_acid"], any_dep=True, xp=300,
      subtitle="A realm beneath the world", desc=[
        "&6A world beneath the world, and the key to its door is a bottle of acid. You are trusted with more every day.&r",
        "&eWhat:&r a strange underground dimension. Its portal catalyst needs a bucket of sulfuric acid: MI's, Mekanism's or ChemLib's all work.",
        "&eHow:&r the quickest bucket is your Mekanism contact process: a Rotary Condensentrator in liquid mode turns the acid gas into fluid you can bucket. MI's Chemical Reactor acid works too. Then build a stone-brick portal frame and right-click it with the catalyst.",
        "&eTip:&r bring torches and food. It is dark down there."]),

    # ===== Optional side quests =====
    Q("t4_thermal", 0, -8, [item(MEK + "thermal_evaporation_controller"), item(MEK + "thermal_evaporation_valve"), item(MEK + "thermal_evaporation_block", 16)], "Thermal Evaporation", deps=["t4_separator"], xp=150, optional=True, tokens=2,
      subtitle="Sun and heat turn water into brine", desc=[
        "&eWhat:&r a tall multiblock that boils water down into brine, and brine down into lithium.",
        "&eChemistry:&r evaporation concentrates dissolved salts. Salt flats and lithium ponds in Chile work the same way.",
        "&eHow:&r see Just Enough Mekanism Multiblocks in JEI for the layout. Taller towers run faster; heat speeds it up."]),
    Q("t4_tanks", 4, -8, [item(MEK + "basic_chemical_tank", 3)], "Bottled Gases", deps=["t4_chem_tank"], xp=60, optional=True, tokens=1,
      subtitle="Keep a tank of H₂, O₂ and Cl₂", desc=[
        "&eWhat:&r chemical tanks store gases and keep them when broken, so you can carry them around.",
        "&eHow:&r fill one tank each with hydrogen, oxygen and chlorine.",
        "&eTip:&r a tank of hydrogen also fuels the Gas-Burning Generator (Power chapter)."]),
    Q("t4_oleum", 8, -8, [tick()], "Fun Fact: Oleum", deps=["t4_mek_acid"], xp=40, optional=True, tokens=1,
      subtitle="How industry really makes H₂SO₄", desc=[
        "&eWhat:&r SO₃ hitting water directly forms a fine acid mist that's hard to capture.",
        "&eChemistry:&r plants absorb SO₃ into concentrated H₂SO₄ to make oleum (H₂S₂O₇), then dilute: H₂S₂O₇ + H₂O → 2H₂SO₄.",
        "&eTip:&r you've now run, in miniature, a process that makes over 250 million tonnes a year."]),
    Q("t4_all5x", 18, -6, [tick()], "Five for Everything", deps=["t4_ore5"], xp=200, optional=True, tokens=2,
      subtitle="Run iron, copper, gold, tin and osmium at 5x", desc=[
        "&eWhat:&r a challenge: put at least five different ores through the full 5x line.",
        "&eHow:&r one Dissolution Chamber handles every metal, but each slurry needs its own washer and crystallizer pass. Tick this when five ores are done.",
        "&eTip:&r Mekanism factories (upgraded machines) run several ores at once."]),
    Q("t4_bauxite_deposit", -8, 4, [item(MI + "bauxite_dust", 128)], "A Red Mountain", deps=["t4_bauxite"], xp=80, optional=True, tokens=1,
      subtitle="Mine a rich bauxite deposit", desc=[
        "&eWhat:&r rich deposits hold hundreds of ores in one chunk. Find bauxite's and the MV tier stops feeling slow.",
        "&eHow:&r strip-mine around Y -16 to 24 and look for red ore with Jade. FTB Ultimine helps a lot.",
        "&eTip:&r Fortune works on bauxite ore, since it drops dust."]),
    Q("t4_titanium", -6, 4, [item(MI + "titanium_tiny_dust", 9)], "A Hint of Titanium", deps=["t4_bayer_digest"], xp=60, optional=True, tokens=1,
      subtitle="Red mud hides titanium", desc=[
        "&eWhat:&r Bayer digestion leaves a little titanium behind with the iron. Save it for much later.",
        "&eChemistry:&r bauxite carries titanium dioxide (TiO₂) as an impurity. It doesn't dissolve in lye, so it ends up in the 'red mud'.",
        "&eHow:&r every Bayer digestion (4 bauxite dust) gives 1 tiny titanium dust. Nine of them pack into a full dust."]),
    Q("t4_mi_hcl", 8, 9, [item(MI + "hydrochloric_acid_bucket")], "Hydrochloric Acid, MI Style", deps=["t4_mi_h2o", "t4_mi_chlorine"], xp=60, tokens=1,
      subtitle="H₂ + Cl₂ in the Chemical Reactor", desc=[
        "&eWhat:&r MI makes hydrochloric acid as a fluid, the MI twin of Mekanism's HCl gas. Chromium leaching and PVC both need it later.",
        "&eChemistry:&r H₂ + Cl₂ → 2HCl. 1000 mB of each gas gives 2000 mB of acid.",
        "&eHow:&r chlorine from salt electrolysis, hydrogen from water electrolysis, both into the Chemical Reactor."]),
    Q("t4_naoh", 12, 9, [item(MI + "sodium_hydroxide_bucket")], "Lye", deps=["t4_reactor", "t4_sodium", "t4_mi_h2o"], xp=60, optional=True, tokens=1,
      subtitle="Sodium hydroxide, the strong base", desc=[
        "&eWhat:&r sodium hydroxide (NaOH, lye) is the strong base to sulfuric acid's strong acid. Soap is made with it.",
        "&eChemistry:&r acid + base → salt + water. H₂SO₄ + 2NaOH → Na₂SO₄ + 2H₂O.",
        "&eHow:&r Chemical Reactor: sodium dust + 1000 mB oxygen + 1000 mB hydrogen → 2000 mB sodium hydroxide.",
        "&eTip:&r this is the bulk lye supply for the Bayer digester, so you can stop feeding it Combiner crystals."]),

    # ===== ATM10-aligned additions (2026-10-19): MV components, doping, upgrades =====
    Q("t4_pumps", 0, 0, [item(MI + "pump", 3), item(MI + "large_pump")], "Pumps, Large and Small", deps=["t4_large_motor", "t4_al_rotor"], xp=100,
      subtitle="The heart of every MV fluid machine", desc=[
        "&eWhat:&r the Electrolyzer and the Chemical Reactor each need a Large Pump, and a Large Pump is three small pumps driven by a Large Motor.",
        "&eHow:&r Large Pump: 2 electronic circuits, 3 aluminum rotors, a Large Motor and 3 pumps (Assembler or crafting table; check JEI).",
        "&eTip:&r pumps are the part you'll run short of. Keep an Assembler stocked with motors and rotors."]),
    Q("t4_doped", 0, 0, [item(MI + "silicon_n_doped_plate"), item(MI + "silicon_p_doped_plate")], "Doping Silicon", deps=["t4_transistor", "t4_reactor"], xp=60,
      optional=True, tokens=1, subtitle="Optional: n-type and p-type silicon", desc=[
        "&eWhat:&r silicon plates with a trace of another element, used in cheaper recipes for transistors and diodes.",
        "&eChemistry:&r silicon has four outer electrons. Antimony has five, so it adds a spare electron (n-type); aluminium has three, so it leaves a 'hole' (p-type). Where n meets p, current flows one way only: a diode.",
        "&eHow:&r Chemical Reactor: 1 silicon plate + 1 tiny antimony dust → n-doped plate; 1 silicon plate + 1 tiny aluminum dust → p-doped plate. JEI shows the doped transistor and diode recipes."]),
    Q("t4_upgrade", 0, 0, [item(MI + "basic_upgrade", 4), item(MI + "overdrive_module")], "Machine Upgrades", deps=["t4_ecboard"], xp=60,
      optional=True, tokens=1, subtitle="Optional: let a machine draw more power", desc=[
        "&eWhat:&r Upgrades go in a machine's upgrade slot and raise how much EU/t it may draw, so it overclocks harder. The Overdrive Module keeps a machine's efficiency up while it waits for input.",
        "&eHow:&r Assembler: 2 conveyors, 4 motors, 2 robot arms and an analog circuit board → 4 basic upgrades. Overdrive Module: 2 diodes, 2 transistors, 4 electrum fine wire and an electronic circuit board.",
        "&eTip:&r hover over an upgrade for its exact bonus. Some late recipes ask for more EU/t than a plain machine allows; upgrades are the answer."]),
    Q("t4_lv_machines", 0, 0, [item("extended_industrialization:electric_alloy_smelter"), item(MI + "electric_unpacker")], "Electric Helpers", deps=["t4_separator"], xp=60,
      optional=True, tokens=1, subtitle="Optional: alloy smelter and unpacker, now electric", desc=[
        "&eWhat:&r the electric versions of two steam-age helpers: the Electric Alloy Smelter (Extended Industrialization) pours alloys from nuggets, the Electric Unpacker breaks blocks and double ingots back down.",
        "&eHow:&r both sit on an LV machine hull with analog circuits. The Alloy Smelter adds a tin rotor and magnetic cupronickel wire, the Unpacker motors and conveyors (check JEI).",
        "&eTip:&r they run on the same LV cable as everything else, so your steam boilers can finally rest."]),

    # ===== ATM10-style detail pass (2026-10-19): every machine, part and intermediate on the real chain =====
    # --- Mekanism gas parts
    Q("t4_electrolytic_core", 0, 0, [item(MEK + "electrolytic_core")], "The Electrolytic Core", deps=["t3_mekcircuit", "t3_infused"], xp=60,
      subtitle="Electrodes for the separator", desc=[
        "&6You remember a time when you split water by asking it to. The memory comes back as a wiring diagram.&r",
        "&eWhat:&r the core of Mekanism's Electrolytic Separator: the part that actually carries current through the water.",
        "&eChemistry:&r an electrolysis cell needs electrodes that conduct and don't dissolve. Real alkaline cells use nickel; Mekanism uses osmium, iron and gold.",
        "&eHow:&r infused alloy, osmium dust, iron dust and gold dust on a crafting table (check JEI for the pattern)."]),
    Q("t4_chem_tank", 0, 0, [item(MEK + "basic_chemical_tank", 2)], "A Tank for Gas", deps=["t4_separator"], xp=40,
      subtitle="Sealed storage for H₂, O₂ and everything after", desc=[
        "&eWhat:&r a basic chemical tank stores one gas. Most Mekanism chemistry machines have one built in.",
        "&eHow:&r basic alloy and osmium ingots (check JEI). The Oxidizer, Infuser, Condensentrator, Washer and Dissolution Chamber all take one.",
        "&eTip:&r a broken tank keeps its contents, so you can carry a tank of oxygen across the base."]),
    Q("t4_energy_tablet", 0, 0, [item(MEK + "energy_tablet")], "Energy Tablet", deps=["t3_infused"], xp=40,
      subtitle="A small battery for Mekanism parts", desc=[
        "&eWhat:&r a portable energy store. The Rotary Condensentrator and the laser are built around one.",
        "&eHow:&r gold ingots, infused alloy and redstone dust (check JEI).",
        "&eTip:&r it also charges Mekanism tools from your inventory."]),
    Q("t4_dynamic_tank", 0, 0, [item(MEK + "dynamic_tank", 4)], "Dynamic Tanks", deps=["t4_chem_tank"], xp=40,
      subtitle="Steel and a bucket", desc=[
        "&eWhat:&r dynamic tank blocks. One goes into the Chemical Oxidizer; a ring of them makes Mekanism's big multiblock fluid tank.",
        "&eHow:&r 4 steel ingots around a bucket → 4 dynamic tanks.",
        "&eTip:&r a small dynamic tank multiblock is a cheap place to keep thousands of buckets of water or brine."]),
    Q("t4_acid_bucket_mek", 0, 0, [item(MEK + "sulfuric_acid_bucket")], "Acid by the Bucket", deps=["t4_mek_acid", "t4_vapor"], xp=80,
      subtitle="Condense the acid gas into a liquid", desc=[
        "&eWhat:&r a bucket of Mekanism sulfuric acid. It opens the Undergarden and counts for the Seed's eight acid buckets.",
        "&eChemistry:&r pure H₂SO₄ boils near 337 °C, so at room temperature it is an oily liquid. Mekanism keeps it as a gas only for piping.",
        "&eHow:&r switch a Rotary Condensentrator to liquid mode, pipe the acid gas in and take the fluid out in a bucket."]),
    # --- Mekanism ore line parts
    Q("t4_adv_circuit", 0, 0, [item(MEK + "advanced_control_circuit", 2)], "Advanced Control Circuits", deps=["t4_circuit", "t3_infused"], xp=80,
      section="Ore Processing: 3x to 5x", subtitle="Mekanism's MV circuit, built on MI's", desc=[
        "&eWhat:&r every Mekanism chamber past the Enrichment Chamber needs advanced control circuits.",
        "&eHow:&r 1 MI electronic circuit, 2 infused alloy and 1 basic control circuit. Mekanism's own infuser shortcut is removed in this pack.",
        "&eTip:&r make six: the Purification, Injection, Dissolution, Washer and Crystallizer recipes all want two."]),
    Q("t4_clumps", 0, 0, [anytag("mekanism:clumps", 6)], "Clumps", deps=["t4_ore3"], xp=40,
      subtitle="Ore, purified with oxygen", desc=[
        "&eWhat:&r any 6 Mekanism clumps: the first product of the 3x line.",
        "&eChemistry:&r oxygen burns off sulfur and other volatile impurities (roasting), leaving a cleaner metal oxide behind.",
        "&eHow:&r Purification Chamber: 1 ore + a little oxygen → 3 clumps (2 from raw ore)."]),
    Q("t4_dirty", 0, 0, [anytag("mekanism:dirty_dusts", 6)], "Dirty Dust", deps=["t4_clumps", "t3_crusher"], xp=40,
      subtitle="Crush the clumps", desc=[
        "&eWhat:&r any 6 dirty dusts. One more Enrichment Chamber pass turns each into clean dust.",
        "&eHow:&r Crusher: 1 clump → 1 dirty dust. Enrichment Chamber: dirty dust → dust.",
        "&eTip:&r dirty dust is also what MI's Centrifuge wants for ore byproducts (silver from lead, nickel from iron)."]),
    Q("t4_reinforced", 0, 0, [item(MEK + "enriched_diamond", 2), item(MEK + "alloy_reinforced", 4)], "Reinforced Alloy", deps=["t4_ore3"], xp=80,
      subtitle="Infused alloy, hardened with diamond", desc=[
        "&eWhat:&r the second Mekanism alloy. The Injection Chamber, the laser and elite circuits all need it.",
        "&eHow:&r Enrichment Chamber: diamond → enriched diamond. Metallurgic Infuser: infused alloy + diamond infusion → reinforced alloy.",
        "&eTip:&r one enriched diamond is a lot of infusion. Don't waste whole diamonds on it."]),
    Q("t4_shards", 0, 0, [anytag("mekanism:shards", 8)], "Shards", deps=["t4_ore4"], xp=40,
      subtitle="Ore, cracked open with HCl", desc=[
        "&eWhat:&r any 8 Mekanism shards, the first product of the 4x line.",
        "&eChemistry:&r hydrochloric acid attacks the minerals around the metal (carbonates, oxides) and breaks the ore into fragments. Real hydrometallurgy leaches with HCl the same way.",
        "&eHow:&r Chemical Injection Chamber: 1 ore + HCl → 4 shards. Shards go into the Purification Chamber as if they were ore."]),
    Q("t4_refined_obsidian", 0, 0, [item(MEK + "ingot_refined_obsidian", 12)], "Refined Obsidian", deps=["t4_reinforced"], xp=100,
      subtitle="Volcanic glass, infused and pressed", desc=[
        "&eWhat:&r the casing metal of the 5x line: the Washer, Dissolution Chamber and Crystallizer each take 4 ingots.",
        "&eChemistry:&r obsidian is volcanic glass, mostly SiO₂, cooled too fast to crystallise. That's why it shatters into razor edges.",
        "&eHow:&r Crusher: obsidian → 4 obsidian dust. Metallurgic Infuser with diamond → refined obsidian dust. Osmium Compressor with osmium → ingot (check JEI)."]),
    Q("t4_fluorite", 0, 0, [item(MEK + "fluorite_gem", 4)], "Fluorite", deps=["t4_dissolution"], xp=60,
      subtitle="The mineral that gave us 'fluorescence'", desc=[
        "&eWhat:&r fluorite gems. The Chemical Crystallizer needs two, and later fluorite becomes hydrofluoric acid.",
        "&eChemistry:&r fluorite is calcium fluoride, CaF₂. Some samples glow under ultraviolet light, which is where the word fluorescence comes from.",
        "&eHow:&r Mekanism fluorite ore sits deep underground. It drops dust; the Enrichment Chamber turns dust into gems. No farm or spirit can make it in this pack."]),
    Q("t4_crystals", 0, 0, [anytag("mekanism:crystals", 8)], "Crystals", deps=["t4_ore5"], xp=60,
      subtitle="Clean slurry, crystallised", desc=[
        "&eWhat:&r any 8 Mekanism crystals, the first product of the 5x line.",
        "&eChemistry:&r crystallisation pulls a pure salt out of solution and leaves the impurities dissolved. It's one of the oldest purification tricks in chemistry.",
        "&eHow:&r Chemical Crystallizer: 200 mB clean slurry → 1 crystal. Then Injection Chamber → shards → Purification Chamber → and on down the line."]),
    # --- aluminium and the MV parts
    Q("t4_steel_large", 0, 0, [item(MI + "steel_large_plate", 4)], "Steel Large Plates", deps=["t1_steel_plate"], xp=40,
      subtitle="Four plates, one heavy sheet", desc=[
        "&eWhat:&r the Hall-Héroult Cell and, later, the Oil Drilling Rig are both framed in steel large plates.",
        "&eHow:&r 4 steel plates in a square on a crafting table, or the Packer."]),
    Q("t4_al_plate", 0, 0, [item(MI + "aluminum_plate", 16)], "Aluminum Plates", deps=["t4_aluminum"], xp=50,
      section="MV Components", subtitle="The sheet metal of the MV tier", desc=[
        "&eWhat:&r MV parts are wrapped in aluminum: 3 per electronic circuit board, 8 per advanced machine casing.",
        "&eChemistry:&r a fresh aluminium surface grows an oxide skin a few nanometres thick within seconds. It's why aluminium doesn't rust away, even though it reacts with oxygen far more eagerly than iron.",
        "&eHow:&r Compressor: 1 aluminum ingot → 1 plate."]),
    Q("t4_al_rod", 0, 0, [item(MI + "aluminum_rod", 6)], "Aluminum Rods", deps=["t4_aluminum"], xp=40,
      subtitle="Axles for motors and rotors", desc=[
        "&eWhat:&r the Electrolyzer and the Large Motor each take two; rotors and rings need more.",
        "&eHow:&r Cutting Machine with a little lubricant: 1 ingot → 2 rods."]),
    Q("t4_al_curved", 0, 0, [item(MI + "aluminum_curved_plate", 4)], "Curved Aluminum", deps=["t4_al_plate"], xp=30,
      subtitle="Bent plate for blades and drill heads", desc=[
        "&eWhat:&r curved plates become rotor blades now and drill heads in the next chapter.",
        "&eHow:&r Compressor: 1 aluminum plate → 1 curved plate (or Extended Industrialization's Bending Machine)."]),
    Q("t4_al_rotor", 0, 0, [item(MI + "aluminum_rotor", 3)], "Aluminum Rotors", deps=["t4_al_curved", "t4_al_rod"], xp=80,
      subtitle="Blades on a ring", desc=[
        "&eWhat:&r every Large Pump spins three aluminum rotors, and the Chemical Reactor stirs with two more.",
        "&eHow:&r blades: 2 curved plates + 1 rod → 4 blades. Ring: Compressor, 1 rod → 1 ring. Rotor: 4 blades, 4 bolts and a ring on a crafting table.",
        "&eTip:&r the Assembler also makes rotors, but its recipe uses soldering alloy, which comes much later. Craft these by hand."]),
    Q("t4_electrum_wire", 0, 0, [item(MI + "electrum_plate", 2), item(MI + "electrum_wire", 8)], "Electrum Wire", deps=["t4_electrum"], xp=40,
      subtitle="Draw gold and silver into wire", desc=[
        "&eWhat:&r electrum wire is the conductor of the MV tier.",
        "&eChemistry:&r silver is the best electrical conductor of all metals, and gold never tarnishes. Their alloy keeps a little of both virtues.",
        "&eHow:&r Compressor: ingot → plate. Wiremill: 1 plate → 2 wire."]),
    Q("t4_electrum_cable", 0, 0, [item(MI + "electrum_cable", 12)], "Electrum Cable", deps=["t4_electrum_wire", "t3_rubber"], xp=50,
      subtitle="MV cable, wrapped in rubber", desc=[
        "&eWhat:&r the MV cable. Circuit boards take 4, hulls 3, batteries 2, and it carries MV power between machines.",
        "&eChemistry:&r rubber is a polymer with no free electrons, so it can't carry current. A thin sleeve of it keeps the current inside the wire.",
        "&eHow:&r 3 electrum wire between 6 rubber sheets → 3 cables (crafting table or Packer)."]),
    Q("t4_fine_wire", 0, 0, [item(MI + "electrum_fine_wire", 8)], "Electrum Fine Wire", deps=["t4_electrum_wire"], xp=30,
      subtitle="Hair-thin leads for semiconductors", desc=[
        "&eWhat:&r the leads inside transistors (1 each) and diodes (3 each).",
        "&eHow:&r Wiremill: 1 electrum wire → 4 fine wire."]),
    Q("t4_quartz_dust", 0, 0, [item(MI + "quartz_dust", 8)], "Quartz Dust", deps=["t2_quartz", "t3_emacerator"], xp=30,
      subtitle="Silicon dioxide, ground fine", desc=[
        "&eWhat:&r the raw material for silicon.",
        "&eChemistry:&r quartz is SiO₂: every silicon atom bonded to four oxygens in a rigid network. That's why it's so hard and melts at about 1700 °C.",
        "&eHow:&r Macerator: 1 Nether quartz → 1 quartz dust. Centrifuging redstone also gives a little."]),
    Q("t4_silicon_plate", 0, 0, [item(MI + "silicon_plate", 6)], "Silicon Plates", deps=["t4_silicon"], xp=40,
      subtitle="Wafers for the first transistors", desc=[
        "&eWhat:&r transistors take 3 silicon plates, diodes 1.",
        "&eHow:&r Compressor: 1 silicon ingot → 1 plate."]),
    Q("t4_ba_plates", 0, 0, [item(MI + "battery_alloy_plate", 2), item(MI + "battery_alloy_curved_plate", 8)], "Battery Plates", deps=["t3_alloy"], xp=40,
      subtitle="The casing of every MI battery", desc=[
        "&eWhat:&r each battery from here to the quantum tier is 1 battery alloy plate and 4 curved plates around its chemistry.",
        "&eChemistry:&r battery alloy is lead and antimony, the same grid metal used in car batteries since the 1880s. Antimony makes soft lead stiff enough to hold its shape.",
        "&eHow:&r Compressor: ingot → plate; Compressor again: plate → curved plate."]),
    Q("t4_large_motor", 0, 0, [item(MI + "large_motor")], "Large Motor", deps=["t4_circuit", "t4_al_rod"], xp=80,
      section="Pumps and Machines", subtitle="Six motors on one shaft", desc=[
        "&eWhat:&r the drive of the Large Pump, the Centrifuge and the Electric Quarry.",
        "&eHow:&r an electronic circuit, 2 aluminum rods and 6 motors (crafting table or Assembler).",
        "&eTip:&r the Centrifuge alone eats four. Keep an Assembler on motors."]),
    Q("t4_centrifuge", 0, 0, [item(MI + "centrifuge")], "The Centrifuge", deps=["t4_pumps"], xp=120,
      subtitle="Separate by weight", desc=[
        "&eWhat:&r MI's Centrifuge spins mixtures apart. Ore byproducts, ruby and chromium, liquid air and monazite all go through it later.",
        "&eChemistry:&r spinning multiplies gravity thousands of times, so heavier particles and molecules move outward faster than light ones.",
        "&eHow:&r 4 large motors, a large pump, an electronic circuit, 2 electrum cable and an LV hull."]),
    Q("t4_adv_casing", 0, 0, [item(MI + "advanced_machine_casing")], "Advanced Machine Casing", deps=["t4_al_plate", "t3_hull"], xp=60,
      subtitle="An LV hull, clad in aluminum", desc=[
        "&eWhat:&r the shell of the MV hull.",
        "&eHow:&r 8 aluminum plates around a basic (LV) machine hull."]),
    # --- MI fluids
    Q("t4_mi_h2o", 0, 0, [item(MI + "hydrogen_bucket"), item(MI + "oxygen_bucket")], "Hydrogen and Oxygen, MI Style", deps=["t4_electrolyzer"], xp=60,
      subtitle="Water electrolysis as MI fluids", desc=[
        "&eWhat:&r MI's own hydrogen and oxygen. The Chemical Reactor takes them by pipe, not Mekanism's gases.",
        "&eChemistry:&r 2H₂O → 2H₂ + O₂: two volumes of hydrogen for every one of oxygen, as the recipe shows.",
        "&eHow:&r Electrolyzer: 3000 mB water → 2000 mB hydrogen + 1000 mB oxygen. Fill a bucket of each from the output."]),
    Q("t4_mi_chlorine", 0, 0, [item(MI + "chlorine_bucket")], "Chlorine, MI Style", deps=["t4_sodium"], xp=60,
      subtitle="The green gas from salt", desc=[
        "&eWhat:&r MI chlorine, the other half of salt electrolysis. It makes hydrochloric acid and, much later, PVC.",
        "&eChemistry:&r Cl₂ is a yellow-green gas, heavier than air. Its name comes from the Greek for pale green.",
        "&eHow:&r Electrolyzer: 2 salt dust → 1 sodium dust + 125 mB chlorine. Eight runs fill a bucket."]),
    Q("t4_mv_power", 0, 0, [item(MI + "lv_mv_transformer"), item(MI + "mv_storage_unit")], "An MV Grid", deps=["t4_mv"], xp=60,
      optional=True, tokens=1, subtitle="Optional: step up the voltage", desc=[
        "&eWhat:&r a transformer joins your LV and MV cables; the MV storage unit buffers a lot more energy than the LV one.",
        "&eHow:&r transformer: an LV hull, 4 tin cable and 1 electrum cable. Storage unit: an MV hull, 6 silicon batteries and 2 battery alloy plates.",
        "&eTip:&r multiblocks draw from energy hatches, so a big buffer next to them keeps recipes from stalling."]),
])
