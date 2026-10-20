"""Quest chapter: t3. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

MI = "modern_industrialization:"

CHAPTER = Chapter("t3", "IV. The Electric Age", "modern_industrialization:basic_machine_hull",
        ["Electricity is the tool that splits compounds apart. First you have to make it, and build the circuits that use it."], MAIN, [
    # --- Raw materials ---
    Q("t3_raw_oil", 0, 0, [item(MI + "raw_synthetic_oil_bucket")], "Oil from Coal", deps=["t1_steel"], xp=40,
      subtitle="Coke dust and water, in the mixer", desc=[
        "&6Lightning used to come when you called it. Now you'll have to build it a road, and the road starts in a coal pit.&r",
        "&eWhat:&r Raw synthetic oil is the first step to rubber, and rubber is what keeps electricity in its wires.",
        "&eChemistry:&r Hot carbon and steam react into syngas, C + H₂O → CO + H₂, and the Fischer-Tropsch process builds that up into longer hydrocarbon chains. Coal-to-oil really was done this way.",
        "&eHow:&r In the Steam Mixer, 1 coke dust and 100 mB of water make 200 mB of raw synthetic oil. Fill a bucket from the mixer's output.",
        "&eTip:&r Grind coke in the Steam Macerator for the dust. One coke dust is a fifth of a bucket of oil."]),
    Q("t3_synth_oil", 0, 0, [item(MI + "synthetic_oil_bucket")], "Synthetic Oil", deps=["t3_raw_oil"], xp=40,
      subtitle="Refined in the Steam Blast Furnace", desc=[
        "&eWhat:&r Raw oil is a messy mixture. Heat refines it into synthetic oil, the input for rubber.",
        "&eChemistry:&r Heating a crude hydrocarbon mix breaks up the unstable pieces and drives off the light ones, leaving a cleaner, more uniform oil.",
        "&eHow:&r Pipe raw synthetic oil into a fluid input hatch on your Steam Blast Furnace: 100 mB in, 100 mB out. It needs a fluid output hatch too.",
        "&eTip:&r A tank between mixer and furnace keeps both busy."]),
    Q("t3_rubber", 0, -2, [item(MI + "rubber_sheet", 8)], "Rubber", deps=["t3_synth_oil"], xp=40,
      subtitle="Insulation, so current goes where you want", desc=[
        "&eWhat:&r rubber sheets insulate cables and form circuit boards. Here rubber is &esynthetic&r, made from coal, not tree sap.",
        "&eChemistry:&r rubber is a polymer: long, tangled hydrocarbon chains. Cross-linked with sulfur (&evulcanisation&r), the chains become a tough, flexible insulator.",
        "&eHow:&r Mixer: synthetic oil + paper → 2 rubber sheets, or + sulfur dust → synthetic rubber fluid (12 sheets per paper). Check JEI.",
        "&eTip:&r the sulfur route gives six times more sheets per oil, but its mixer needs more power (check JEI for sulfur dust sources)."]),
    Q("t3_wiremill", 0, 0, [item(MI + "steel_wiremill")], "Steel Wiremill", deps=["t3_casing"], xp=40,
      subtitle="Pulls plates into wire", desc=[
        "&eWhat:&r Copper wire can't be crafted by hand. The Wiremill draws plates into wire, and wire into fine wire.",
        "&eChemistry:&r Metals are &eductile&r: their atoms slide past each other without the bonds breaking, so a plate can be pulled through a die into a thin wire.",
        "&eHow:&r A steel machine casing with bronze gears, bronze rotors and fluid pipes (check JEI). It runs on steam like your other machines.",
        "&eTip:&r 1 copper plate makes 2 wire. Keep it fed from your Steam Compressor."]),
    Q("t3_wire", 0, 0, [item(MI + "copper_wire", 8), item(MI + "tin_cable", 8)], "Wires and Cables", deps=["t3_wiremill"], xp=40,
      subtitle="Copper conducts; rubber makes it a cable", desc=[
        "&eWhat:&r copper wire goes into every component. Tin cable carries LV power between machines.",
        "&eChemistry:&r copper's single outer electron moves freely between atoms, which is why it conducts so well.",
        "&eHow:&r the Steel Wiremill pulls plates into wire. Cables combine wire with rubber sheets.",
        "&eTip:&r tin cable is rated for LV (32 EU/t). Higher tiers need better cable."]),
    Q("t3_alloy", 0, 3, [item(MI + "battery_alloy_ingot", 4)], "Battery Alloy", deps=["t1_steel"], xp=40,
      subtitle="Lead and antimony, as in a car battery", desc=[
        "&eWhat:&r battery alloy makes the casing and grids of redstone batteries.",
        "&eChemistry:&r lead hardened with antimony is the grid metal of real lead-acid batteries. Pure lead is too soft.",
        "&eHow:&r mix lead and antimony dust (check JEI), then smelt. Lead deposits sit around Y -24 to 16."]),

    # --- Components for the analog circuit ---
    Q("t3_board", 2, -3, [item(MI + "analog_circuit_board", 2)], "Analog Circuit Board", deps=["t3_rubber"], xp=40,
      subtitle="Rubber, copper, rubber", desc=[
        "&eWhat:&r the base every analog circuit is soldered onto.",
        "&eHow:&r rubber sheet, copper plate, rubber sheet stacked in a column.",
        "&eTip:&r once you have an Assembler, it makes these automatically."]),
    Q("t3_capacitor", 2, -1, [item(MI + "capacitor", 2)], "Capacitor", deps=["t3_rubber", "t3_wire"], xp=30,
      subtitle="Stores charge between two plates", desc=[
        "&eWhat:&r capacitors store a small charge and smooth out the current.",
        "&eChemistry:&r two conductors (gold plates) separated by an insulator (rubber): charge builds up on each side.",
        "&eHow:&r gold plates, copper wire and a rubber sheet (see JEI)."]),
    Q("t3_fine_wire", 0, 0, [item(MI + "copper_fine_wire", 8)], "Fine Copper Wire", deps=["t3_wire"], xp=25,
      subtitle="Wire, drawn again", desc=[
        "&eWhat:&r Thinner wire for small components. Resistors need it first.",
        "&eChemistry:&r A thinner wire has more resistance: current has less metal to flow through. Useful when you want to limit current, not carry it.",
        "&eHow:&r Put copper wire back into the Wiremill: 1 wire makes 4 fine wire."]),
    Q("t3_components", 2, 0, [item(MI + "resistor", 3)], "Resistor", deps=["t3_fine_wire"], xp=30,
      subtitle="Limits the current through a circuit", desc=[
        "&eWhat:&r resistors limit current so the rest of the circuit doesn't burn out.",
        "&eChemistry:&r carbon conducts, but poorly. A pinch of coal dust between fine copper wires makes a carbon resistor.",
        "&eHow:&r paper, copper fine wire and coal dust. One craft gives three."]),
    Q("t3_inductor", 2, 1, [item(MI + "inductor", 2)], "Inductor", deps=["t3_wire"], xp=30,
      subtitle="A coil that resists change", desc=[
        "&eWhat:&r inductors resist sudden changes in current. The Polarizer also needs them.",
        "&eChemistry:&r current through a coil makes a magnetic field; changing the current fights that field.",
        "&eHow:&r copper wire wound around a steel rod."]),
    Q("t3_acid", 2, 5, [item("chemlib:sulfuric_acid", 2)], "Battery Acid", deps=["t1_combiner"], xp=50,
      subtitle="2 H + S + 4 O → H₂SO₄, in the Combiner", desc=[
        "&eWhat:&r the redstone battery is a real &elead-acid battery&r, and its electrolyte is sulfuric acid. The Combiner from Chapter II makes it from elements.",
        "&eChemistry:&r H₂SO₄ is the most-produced chemical in the world. In a car battery it reacts with the lead plates (Pb + PbO₂ + 2H₂SO₄ → 2PbSO₄ + 2H₂O) and releases electrons; charging runs the reaction backwards.",
        "&eHow:&r pick sulfuric acid in the Combiner and supply 2 hydrogen, 1 sulfur and 4 oxygen. Dissolve gunpowder for sulfur (1 gunpowder → 8 S) and water or cellulose for hydrogen and oxygen.",
        "&eTip:&r every LV hull needs two batteries, so keep a stack of acid ready."]),
    Q("t3_battery", 2, 3, [item(MI + "redstone_battery", 2)], "Redstone Battery", deps=["t3_alloy", "t3_wire", "t3_acid"], xp=40,
      subtitle="Lead, antimony and acid: the LV hull needs two", desc=[
        "&eWhat:&r a rechargeable lead-acid battery. Every LV hull holds two.",
        "&eChemistry:&r lead-antimony grids, sulfuric acid electrolyte: the same chemistry as the battery under a car's bonnet.",
        "&eHow:&r battery alloy plate and curved plates, tin cable, redstone and &esulfuric acid&r from the Combiner (check JEI for the exact recipe).",
        "&eTip:&r the LV Storage Unit is built from six of these, so make spares."]),
    Q("t3_analog", 4, -1, [item(MI + "analog_circuit", 2)], "Analog Circuit", deps=["t3_board", "t3_capacitor", "t3_components", "t3_inductor"], xp=75,
      subtitle="Your first circuit", desc=[
        "&eWhat:&r the LV circuit. Mekanism's Basic Control Circuit also needs one, so MI and Mekanism advance together.",
        "&eHow:&r 2 resistors, 1 inductor, 2 capacitors, the board, and 3 copper wire (see JEI for the layout).",
        "&eTip:&r make four or five now. The hull, turbine and each machine all eat them."]),
    Q("t3_casing", 4, 2, [item(MI + "steel_machine_casing")], "Steel Machine Casing", deps=["t1_steel_gear"], xp=30,
      subtitle="The frame inside every LV machine", desc=[
        "&eWhat:&r a steel frame. The LV hull is built around it.",
        "&eHow:&r 8 steel plates around a steel gear, the same shape as the bronze one.",
        "&eTip:&r the LV hull uses one casing each, and every LV machine needs a hull. Make a few."]),
    Q("t3_hull", 6, 1, [item(MI + "basic_machine_hull")], "LV Machine Hull", deps=["t3_analog", "t3_battery", "t3_casing"], xp=150, size=1.5, items=[(MI + "analog_circuit", 4), (MI + "electric_macerator", 1)],
      subtitle="The heart of every LV machine", desc=[
        "&6Your hands remember wiring this. Your mind is still catching up.&r",
        "&eWhat:&r &eLV&r (Low Voltage) is the first electric tier. Every LV machine is built on this hull.",
        "&eHow:&r steel machine casing + analog circuit + 2 redstone batteries + 3 tin cable."]),

    # --- Motors and power ---
    Q("t3_magrod", 6, -3, [item(MI + "steel_rod_magnetic", 2)], "Magnetic Steel Rod", deps=["t1_steel"], xp=30,
      subtitle="A steel rod surrounded by redstone", desc=[
        "&eWhat:&r the core of an electric motor.",
        "&eChemistry:&r iron-based alloys hold magnetism because their electron spins line up in domains.",
        "&eHow:&r a steel rod ringed by redstone. Later the Polarizer magnetises rods with electricity."]),
    Q("t3_motor", 8, -3, [item(MI + "motor", 2)], "Electric Motor", deps=["t3_magrod", "t3_wire"], xp=50,
      subtitle="Electricity in, rotation out", desc=[
        "&eWhat:&r motors drive turbines, pistons, conveyors and robot arms. Nearly every LV machine needs one.",
        "&eChemistry:&r current in a coil next to a magnet creates a force; that's the motor effect. Run it backwards and it's a generator.",
        "&eHow:&r magnetic steel rod, steel rods, copper wire and tin cable (see JEI)."]),
    Q("t3_turbine", 8, -1, [item(MI + "lv_steam_turbine")], "Steam to Electricity", deps=["t3_hull", "t3_motor"], xp=100,
      subtitle="Your boilers become a power plant", desc=[
        "&eWhat:&r a turbine turns your boiler's steam into &eEU&r, MI's electricity.",
        "&eHow:&r pipe steam in, and run tin cable from the turbine to your machines.",
        "&eTip:&r watch the turbine's steam input. If machines stall, add boilers before adding turbines."]),

    # --- LV machines, one per quest ---
    Q("t3_piston", 10, -4, [item(MI + "piston", 2)], "Piston", deps=["t3_motor"], xp=30,
      subtitle="A motor that pushes", desc=[
        "&eWhat:&r MI's piston component, used in the macerator, compressor and robot arm.",
        "&eHow:&r steel plates, steel rods, steel gear, tin cable and a motor.",
        "&eTip:&r the Electric Macerator and Electric Compressor each need pistons, so make four."]),
    Q("t3_conveyor", 10, -2, [item(MI + "conveyor", 2)], "Conveyor", deps=["t3_motor", "t3_rubber"], optional=True, tokens=1, xp=30,
      subtitle="A rubber belt on two motors", desc=[
        "&eWhat:&r conveyors move items inside machines. The Assembler, Packer and Cutting Machine need them.",
        "&eHow:&r rubber sheets, two motors and tin cable.",
        "&eTip:&r motors are the bottleneck here. Keep a few spare."]),
    Q("t3_ecompressor", 10, 0, [item(MI + "electric_compressor")], "Electric Compressor", deps=["t3_turbine", "t3_piston"], optional=True, tokens=1, xp=40,
      subtitle="Plates, faster and without steam", desc=[
        "&eWhat:&r plates, curved plates and rings for every part you'll build next.",
        "&eHow:&r LV hull, two pistons, analog circuits and tin cable.",
        "&eTip:&r it doubles as a second plate source while the steam compressor keeps running."]),
    Q("t3_ewiremill", 10, 1, [item(MI + "electric_wiremill")], "Electric Wiremill", deps=["t3_turbine"], optional=True, tokens=1, xp=40,
      subtitle="Wire, faster", desc=[
        "&eWhat:&r copper wire and fine wire in bulk. Circuits use a lot of it.",
        "&eHow:&r LV hull, motors and analog circuits (see JEI).",
        "&eTip:&r feed it from your compressor's plate output."]),
    Q("t3_polarizer", 10, 2, [item(MI + "polarizer")], "Polarizer", deps=["t3_turbine", "t3_inductor"], xp=40,
      subtitle="Magnetises rods and wires", desc=[
        "&eWhat:&r magnetic steel rods for motors, and &emagnetic cupronickel wire&r for heating coils.",
        "&eChemistry:&r a strong field lines up the magnetic domains in the metal, and they stay lined up.",
        "&eHow:&r LV hull, inductors, tin wire and tin cable."]),
    Q("t3_mixer", 10, 3, [item(MI + "electric_mixer")], "Electric Mixer", deps=["t3_turbine"], xp=40,
      subtitle="Alloy dusts and chemical mixes", desc=[
        "&eWhat:&r mixing dusts into alloys (bronze, invar, cupronickel, battery alloy) and fluids into mixtures.",
        "&eHow:&r LV hull, motor, tin rotor, glass, a fluid pipe and analog circuits.",
        "&eTip:&r you'll need it for cupronickel (copper + nickel) and invar (iron + nickel) right away."]),
    Q("t3_emacerator", 12, -5, [item(MI + "electric_macerator")], "Electric Macerator", deps=["t3_piston", "t3_turbine"], xp=40,
      subtitle="Grinding, now electric", desc=[
        "&eWhat:&r ore to crushed dust, ingots back to dust. Still capped at 2x per ore until acids.",
        "&eHow:&r needs an &einvar rotary blade&r (invar gear + diamond dust). Invar is iron + nickel; mix the dusts.",
        "&eTip:&r the hull quest reward included one. Build a second for throughput."]),
    Q("t3_efurnace", 14, 1, [item(MI + "electric_furnace")], "Electric Furnace", deps=["t3_cupronickel"], optional=True, tokens=1, xp=40,
      subtitle="Smelting with heat from a wire coil", desc=[
        "&eWhat:&r fast, fuel-free smelting.",
        "&eChemistry:&r current through a resistive wire turns into heat (Joule heating), the same idea as a toaster.",
        "&eHow:&r LV hull wrapped in magnetic cupronickel wire, with analog circuits."]),
    Q("t3_robotarm", 12, -3, [item(MI + "robot_arm", 2)], "Robot Arm", deps=["t3_piston"], optional=True, tokens=1, xp=40,
      subtitle="Motors, a piston and a circuit", desc=[
        "&eWhat:&r robot arms move parts inside the Assembler and Packer.",
        "&eHow:&r two motors, a piston, steel rods, tin cable and an analog circuit.",
        "&eTip:&r the Assembler takes two and the Packer two more."]),
    Q("t3_cutting", 12, -1, [item(MI + "electric_cutting_machine")], "Cutting Machine", deps=["t3_conveyor", "t3_turbine"], optional=True, tokens=1, xp=40,
      subtitle="Rods, bolts and planks", desc=[
        "&eWhat:&r cutting ingots into rods and bolts, and logs into more planks.",
        "&eHow:&r it uses an invar rotary blade, motors and a conveyor. Its cuts use a little lubricant, the creosote + redstone mix from Chapter II.",
        "&eTip:&r logs give six planks here instead of four."]),
    Q("t3_cupronickel", 12, 2, [item(MI + "cupronickel_wire_magnetic", 8)], "Magnetic Cupronickel Wire", deps=["t3_polarizer", "t3_mixer"], xp=50,
      subtitle="Copper-nickel wire for heating coils", desc=[
        "&eWhat:&r the heating wire for the Electric Furnace and Electric Blast Furnace.",
        "&eChemistry:&r cupronickel (copper + nickel) resists current more than copper and survives heat. Coins and ship pipes use it too.",
        "&eHow:&r mix copper and nickel dust, smelt, draw into wire, then magnetise it in the Polarizer."]),
    Q("t3_assembler", 14, -3, [item(MI + "assembler")], "Assembler", deps=["t3_robotarm", "t3_conveyor"], optional=True, tokens=1, xp=60,
      subtitle="Where MI automation really starts", desc=[
        "&eWhat:&r circuits and machine parts, automatically, from a stocked input.",
        "&eHow:&r LV hull, two robot arms, two conveyors and two analog circuits.",
        "&eTip:&r MI shows every assembler recipe in JEI. Feed it sheets, wire and plates and leave it running."]),
    Q("t3_packer", 14, -1, [item(MI + "electric_packer")], "Packer", deps=["t3_robotarm", "t3_conveyor"], optional=True, tokens=1, xp=40,
      subtitle="Blocks, double ingots and more", desc=[
        "&eWhat:&r compacting ingots into blocks and double ingots, and assembling a few parts. You'll want bauxite blocks next chapter.",
        "&eHow:&r robot arms, conveyors, analog circuits and tin cable on an LV hull.",
        "&eTip:&r unpacking is a separate machine, the Unpacker. Build one if you store metal as blocks."]),
    Q("t3_ebf", 14, 3, [item(MI + "electric_blast_furnace"), item(MI + "cupronickel_coil", 8)], "Electric Blast Furnace", deps=["t3_cupronickel"], xp=200, size=1.5, shape="gear",
      subtitle="The furnace that makes aluminum", desc=[
        "&6Fire you can measure in volts. You used to do this without the volts.&r",
        "&eWhat:&r MI's big furnace multiblock. With cupronickel coils it reaches the heat for &ealuminum&r and &esilicon&r.",
        "&eHow:&r the controller is an LV hull wrapped in magnetic cupronickel wire. Check the structure in JEI or the MI guidebook, then add an LV energy input hatch and item hatches.",
        "&eTip:&r hold a hatch or wrench near the controller to see the valid positions highlighted."]),

    # --- Mekanism ---
    Q("t3_osmium", 6, 6, [item("mekanism:raw_osmium", 8)], "Osmium", deps=["t3_hull"], xp=40,
      subtitle="Mekanism's blue-grey metal", desc=[
        "&eWhat:&r Mekanism builds almost everything from osmium: its infuser, casings and circuits.",
        "&eChemistry:&r real osmium is the densest natural element, 22.6 g/cm³. A litre of it weighs about as much as a big dog.",
        "&eHow:&r osmium ore is common in small veins underground. Smelt the raw osmium into ingots."]),
    Q("t3_infuser", 8, 6, [item("mekanism:metallurgic_infuser")], "Mekanism: Metallurgic Infuser", deps=["t3_osmium"], xp=60,
      subtitle="Infuse metals with carbon, redstone and more", desc=[
        "&eWhat:&r Mekanism's entry machine. It infuses metals with other materials.",
        "&eHow:&r iron ingots, redstone, an osmium ingot and two furnaces.",
        "&eTip:&r it runs on FE. Your Chapter II generator works, or a Mekanism Heat Generator (Power chapter)."]),
    Q("t3_infused", 8, 8, [item("mekanism:alloy_infused", 4)], "Infused Alloy", deps=["t3_infuser"], xp=40,
      subtitle="Copper infused with redstone", desc=[
        "&eWhat:&r Mekanism's basic alloy. The Enrichment Chamber and many basic machines need it.",
        "&eChemistry:&r a real alloy mixes metals at the atomic level. Here redstone plays the part of the second element.",
        "&eHow:&r put redstone in the infuser's left slot (it becomes an infusion buffer), then feed copper ingots."]),
    Q("t3_mekcircuit", 10, 6, [item("mekanism:basic_control_circuit", 2), item("mekanism:steel_casing")], "Mekanism Circuits", deps=["t3_infuser", "t3_analog"], xp=75,
      subtitle="MI's analog circuit, in Mekanism form", desc=[
        "&eWhat:&r in this pack, a Basic Control Circuit is &eMI Analog Circuit + osmium&r. Each Mekanism circuit tier needs the matching MI circuit.",
        "&eHow:&r the Steel Casing (steel, glass and osmium) is the frame for most Mekanism machines.",
        "&eTip:&r make several casings at once. Every Mekanism machine in the next chapter needs one."]),
    Q("t3_enrich", 12, 6, [item("mekanism:enrichment_chamber")], "Enrichment Chamber", deps=["t3_mekcircuit", "t3_infused"], xp=60,
      subtitle="Mekanism's 2x ore processing", desc=[
        "&eWhat:&r ore → 2 dust. It also turns dirty dust into clean dust in the higher-tier lines.",
        "&eHow:&r steel casing, infused alloy, iron and a basic control circuit.",
        "&eTip:&r 3x, 4x and 5x need gases and acids: that's the next chapter."]),
    Q("t3_crusher", 12, 8, [item("mekanism:crusher")], "Crusher", deps=["t3_mekcircuit"], xp=40,
      subtitle="Clumps into dirty dust", desc=[
        "&eWhat:&r crushes ingots to dust and, later, ore clumps into dirty dust in the 3x+ lines.",
        "&eHow:&r steel casing, basic control circuits, redstone and lava buckets.",
        "&eTip:&r it also turns ingots back into dust, handy for alloy recipes."]),

    # --- Optional side quests ---
    Q("t3_configcard", 6, -5, [item(MI + "config_card")], "Pipe Config Card", deps=["t3_hull"], xp=20, optional=True, tokens=1,
      subtitle="Copy one pipe's settings to another", desc=[
        "&eWhat:&r saves an item or fluid pipe connection's settings and pastes them onto other connections.",
        "&eHow:&r sneak + use on a configured pipe connection to save; use on another connection to apply. Sneak + use on air clears it.",
        "&eTip:&r it can also camouflage pipes as any block. The card's tooltip explains how."]),
    Q("t3_storage", 14, -5, [item(MI + "lv_storage_unit")], "LV Storage Unit", deps=["t3_turbine", "t3_battery"], xp=40, optional=True, tokens=1,
      subtitle="A buffer for your power grid", desc=[
        "&eWhat:&r stores EU, so machines keep running when the turbine can't keep up for a moment.",
        "&eHow:&r six redstone batteries, battery alloy plates and an LV hull.",
        "&eTip:&r put it between turbine and machines so short dips don't stop anything."]),
    Q("t3_waterpump", 16, -5, [item(MI + "electric_water_pump")], "Electric Water Pump", deps=["t3_turbine"], xp=30, optional=True, tokens=1,
      subtitle="Endless water for boilers", desc=[
        "&eWhat:&r pumps water from nothing but power, for boilers and (soon) electrolysis.",
        "&eHow:&r an LV hull with a pump, tin rotor, pipes and an analog circuit.",
        "&eTip:&r next chapter, water becomes hydrogen and oxygen. You'll want lots of it."]),
    Q("t3_spectrometer", 2, 5, [item("warbuckscore:spectrometer")], "The Spectrometer", deps=["t3_analog"], xp=60, optional=True, tokens=1,
      subtitle="Every element sings its own colour", desc=[
        "&6Once you could see the colours inside things, the light every element gives off. This is a fair copy.&r",
        "&eWhat:&r a hand-held scanner (Warbucks Core, made for this pack). Right-click to read the ore signal in the loaded chunks around you.",
        "&eChemistry:&r heated atoms give off light only at certain wavelengths, an emission spectrum unique to each element. That's how helium was found in the Sun before anyone found it on Earth.",
        "&eHow:&r amethyst prism, steel plates, copper wire and an analog circuit (check JEI). It lists each element with its strength, direction, distance and depth.",
        "&eTip:&r a \"strong\" signal is usually a rich deposit. Walk towards it and scan again."]),
    Q("t3_lead_deposit", 0, 5, [item(MI + "raw_lead", 64)], "A Rich Lead Deposit", deps=["t1_steel"], xp=60, optional=True, tokens=1,
      subtitle="Find a chunk full of lead", desc=[
        "&eWhat:&r rich ore deposits hold hundreds of ores in one chunk, at a metal-specific depth. Lead's sits around Y -24 to 16.",
        "&eHow:&r strip-mine at that depth and check ore with Jade. FTB Ultimine clears a vein in one go.",
        "&eTip:&r galena (lead sulfide, PbS) is the world's main lead ore, and it often carries silver."]),
    Q("t3_osmium_hoard", 6, 8, [item("mekanism:ingot_osmium", 32)], "Osmium Hoard", deps=["t3_osmium"], xp=60, optional=True, tokens=1,
      subtitle="Stockpile for the Mekanism build-out", desc=[
        "&eWhat:&r every Mekanism machine, casing and circuit costs osmium. A stockpile saves trips.",
        "&eHow:&r smelt or enrich raw osmium into ingots.",
        "&eTip:&r the Enrichment Chamber doubles osmium ore, so process it there once it's built."]),
])
