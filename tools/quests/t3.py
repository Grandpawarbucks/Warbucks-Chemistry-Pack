"""Quest chapter: t3. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

MI = "modern_industrialization:"

S_RUBBER, S_WIRE, S_PARTS, S_BATTERY = "Synthetic Rubber", "Wire and Cable", "Circuit Parts", "The Lead-Acid Battery"
S_HULL, S_MACHINES, S_EBF, S_MEK = "The LV Hull", "LV Machines", "The Electric Blast Furnace", "Mekanism"

CHAPTER = Chapter("t3", "IV. The Electric Age", "modern_industrialization:basic_machine_hull",
        ["Electricity is the tool that splits compounds apart. First you have to make it, and build the circuits that use it."], MAIN, [
    # --- synthetic rubber -----------------------------------------------------------------
    Q("t3_raw_oil", 0, 0, [item(MI + "raw_synthetic_oil_bucket")], "Oil from Coal", section=S_RUBBER, deps=["t1_steel"], xp=40,
      subtitle="Coke dust and water, in the mixer", desc=[
        "&6Lightning used to come when you called it. Now you'll have to build it a road, and the road starts in a coal pit.&r",
        "&eWhat:&r Raw synthetic oil is the first step to rubber, and rubber is what keeps electricity in its wires.",
        "&eChemistry:&r Hot carbon and steam react into syngas, C + H₂O → CO + H₂, and the Fischer-Tropsch process builds that up into longer hydrocarbon chains. Coal-to-oil really was done this way.",
        "&eHow:&r In the Steam Mixer, 1 coke dust and 100 mB of water make 200 mB of raw synthetic oil. Fill a bucket from the mixer's output.",
        "&eTip:&r Grind coke in the Steam Macerator for the dust. One coke dust is a fifth of a bucket of oil."]),
    Q("t3_synth_oil", 0, 0, [item(MI + "synthetic_oil_bucket")], "Synthetic Oil", section=S_RUBBER, deps=["t3_raw_oil"], xp=40,
      subtitle="Refined in the Steam Blast Furnace", desc=[
        "&eWhat:&r Raw oil is a messy mixture. Heat refines it into synthetic oil, the input for rubber.",
        "&eChemistry:&r Heating a crude hydrocarbon mix breaks up the unstable pieces and drives off the light ones, leaving a cleaner, more uniform oil.",
        "&eHow:&r Pipe raw synthetic oil into a fluid input hatch on your Steam Blast Furnace: 100 mB in, 100 mB out. It needs a fluid output hatch too.",
        "&eTip:&r A tank between mixer and furnace keeps both busy."]),
    Q("t3_paper", 0, 0, [item("minecraft:paper", 16)], "Paper", subtitle="The backing for rubber and resistors", section=S_RUBBER, deps=["t1_steel"], xp=15, desc=[
        "&eWhat:&r Rubber sheets are cast on paper, and resistors are wrapped in it.",
        "&eChemistry:&r Paper is a mat of cellulose fibres held together by hydrogen bonds between the chains. Wet it and the water breaks those bonds, which is why wet paper tears.",
        "&eHow:&r 3 sugar cane make 3 paper.",
        "&eTip:&r A sugar cane farm next to water keeps this coming. Every rubber sheet batch eats one paper."]),
    Q("t3_rubber", 0, -2, [item(MI + "rubber_sheet", 8)], "Rubber", section=S_RUBBER, deps=["t3_synth_oil", "t3_paper"], xp=40, size=1.5,
      subtitle="Insulation, so current goes where you want", desc=[
        "&6A wire is only useful if the current stays inside it. You used to just tell lightning where to go.&r",
        "&eWhat:&r rubber sheets insulate cables and form circuit boards. Here rubber is &esynthetic&r, made from coal, not tree sap.",
        "&eChemistry:&r rubber is a polymer: long, tangled hydrocarbon chains. Cross-linked with sulfur (&evulcanisation&r), the chains become a tough, flexible insulator.",
        "&eHow:&r Mixer: 100 mB synthetic oil + 1 paper → 2 rubber sheets. Or vulcanise 1000 mB of oil with sulfur dust into synthetic rubber fluid first: then 1 paper and 100 mB give 12 sheets.",
        "&eTip:&r the sulfur route gives six times more sheets per oil, but it needs a steel or electric mixer (4 EU/t)."]),

    # --- wire and cable -------------------------------------------------------------------
    Q("t3_casing", 4, 2, [item(MI + "steel_machine_casing", 4)], "Casings for the LV Line", section=S_WIRE, deps=["t1_steel_casing"], xp=30,
      subtitle="A stack of steel frames", desc=[
        "&eWhat:&r the Steel Wiremill takes one casing and every LV machine hull takes another. Build a few ahead.",
        "&eHow:&r 8 steel plates around a steel gear, the same shape as the bronze one.",
        "&eTip:&r the Assembler later makes them for you. Until then, keep the blast furnace running."]),
    Q("t3_wiremill", 0, 0, [item(MI + "steel_wiremill")], "Steel Wiremill", section=S_WIRE, deps=["t3_casing", "t1_bronze_rotor"], xp=40,
      subtitle="Pulls plates into wire", desc=[
        "&eWhat:&r Copper wire can't be crafted by hand. The Wiremill draws plates into wire, and wire into fine wire.",
        "&eChemistry:&r Metals are &eductile&r: their atoms slide past each other without the bonds breaking, so a plate can be pulled through a die into a thin wire.",
        "&eHow:&r A steel machine casing, 4 bronze gears, 2 bronze rotors and 2 fluid pipes. It runs on steam like your other machines.",
        "&eTip:&r 1 copper plate makes 2 wire. Keep it fed from your Steam Compressor."]),
    Q("t3_tin_wire", 0, 0, [item(MI + "tin_wire", 8)], "Tin Wire", subtitle="The core of LV cable", section=S_WIRE, deps=["t3_wiremill"], xp=20, desc=[
        "&eWhat:&r Tin cable, the wire that carries LV power, has tin wire at its core. The Polarizer needs bare tin wire too.",
        "&eChemistry:&r tin conducts about a seventh as well as copper. That's plenty for low voltage, and tin was cheap and resisted corrosion.",
        "&eHow:&r Press tin ingots into plates, then draw each plate into 2 tin wire in the Wiremill."]),
    Q("t3_wire", 0, 0, [item(MI + "copper_wire", 8), item(MI + "tin_cable", 8)], "Wires and Cables", section=S_WIRE, deps=["t3_tin_wire", "t3_rubber"], xp=40,
      subtitle="Copper conducts; rubber makes it a cable", desc=[
        "&eWhat:&r copper wire goes into every component. Tin cable carries LV power between machines.",
        "&eChemistry:&r copper's single outer electron moves freely between atoms, which is why it conducts so well.",
        "&eHow:&r the Wiremill pulls copper plates into wire. 3 tin wire between 6 rubber sheets make 3 tin cable.",
        "&eTip:&r tin cable is rated for LV (32 EU/t). Higher tiers need better cable."]),
    Q("t3_fine_wire", 0, 0, [item(MI + "copper_fine_wire", 8)], "Fine Copper Wire", section=S_WIRE, deps=["t3_wire"], xp=25,
      subtitle="Wire, drawn again", desc=[
        "&eWhat:&r Thinner wire for small components. Resistors need it first.",
        "&eChemistry:&r A thinner wire has more resistance: current has less metal to flow through. Useful when you want to limit current, not carry it.",
        "&eHow:&r Put copper wire back into the Wiremill: 1 wire makes 4 fine wire."]),

    # --- circuit parts --------------------------------------------------------------------
    Q("t3_board", 2, -3, [item(MI + "analog_circuit_board", 2)], "Analog Circuit Board", section=S_PARTS, deps=["t3_rubber"], xp=40,
      subtitle="Rubber, copper, rubber", desc=[
        "&eWhat:&r the base every analog circuit is soldered onto.",
        "&eHow:&r rubber sheet, copper plate, rubber sheet stacked in a column.",
        "&eTip:&r once you have an Assembler, it makes these automatically."]),
    Q("t3_coal_dust", 0, 0, [item(MI + "coal_dust", 4)], "Coal Dust", subtitle="Carbon for a resistor", section=S_PARTS, deps=["t3_fine_wire"], xp=15, desc=[
        "&eWhat:&r the resistive filling of a carbon resistor.",
        "&eHow:&r the Steam Macerator grinds 1 coal into 1 coal dust. Coal, not charcoal: the recipe wants coal dust specifically.",
        "&eTip:&r one coal dust makes three resistors by hand, twelve in the Assembler."]),
    Q("t3_components", 2, 0, [item(MI + "resistor", 3)], "Resistor", section=S_PARTS, deps=["t3_fine_wire", "t3_coal_dust", "t3_paper"], xp=30,
      subtitle="Limits the current through a circuit", desc=[
        "&eWhat:&r resistors limit current so the rest of the circuit doesn't burn out.",
        "&eChemistry:&r carbon conducts, but poorly. A pinch of coal dust between fine copper wires makes a carbon resistor.",
        "&eHow:&r 2 paper, 2 copper fine wire and 1 coal dust. One craft gives three."]),
    Q("t3_gold_plate", 0, 0, [item(MI + "gold_plate", 4)], "Gold Plates", subtitle="The plates of a capacitor", section=S_PARTS, deps=["t3_wire"], xp=20, desc=[
        "&eWhat:&r every capacitor holds two gold plates.",
        "&eChemistry:&r gold doesn't oxidise, so its surface stays clean and conductive forever. Real electronics plate their contacts with a thin layer of it.",
        "&eHow:&r the Steam Compressor presses 1 gold ingot into 1 plate.",
        "&eTip:&r the Nether's gold ore and piglin trades are an easy source."]),
    Q("t3_capacitor", 2, -1, [item(MI + "capacitor", 2)], "Capacitor", section=S_PARTS, deps=["t3_gold_plate", "t3_wire"], xp=30,
      subtitle="Stores charge between two plates", desc=[
        "&eWhat:&r capacitors store a small charge and smooth out the current.",
        "&eChemistry:&r two conductors (gold plates) separated by an insulator (rubber): charge builds up on each side.",
        "&eHow:&r 2 gold plates, 2 copper wire and a rubber sheet."]),
    Q("t3_inductor", 2, 1, [item(MI + "inductor", 2)], "Inductor", section=S_PARTS, deps=["t3_wire"], xp=30,
      subtitle="A coil that resists change", desc=[
        "&eWhat:&r inductors resist sudden changes in current. The Polarizer also needs them.",
        "&eChemistry:&r current through a coil makes a magnetic field; changing the current fights that field.",
        "&eHow:&r 8 copper wire wound around a steel rod."]),
    Q("t3_analog", 4, -1, [item(MI + "analog_circuit", 2)], "Analog Circuit", section=S_PARTS, deps=["t3_board", "t3_capacitor", "t3_components", "t3_inductor"], xp=75,
      subtitle="Your first circuit", desc=[
        "&eWhat:&r the LV circuit. Mekanism's Basic Control Circuit also needs one, so MI and Mekanism advance together.",
        "&eHow:&r 2 resistors, 1 inductor, 2 capacitors, the board, and 3 copper wire (see JEI for the layout).",
        "&eTip:&r make four or five now. The hull, turbine and each machine all eat them."]),
    Q("t3_spectrometer", 2, 5, [item("warbuckscore:spectrometer")], "The Spectrometer", section=S_PARTS, deps=["t3_analog"], xp=60, optional=True, tokens=1,
      subtitle="Every element sings its own colour", desc=[
        "&6Once you could see the colours inside things, the light every element gives off. This is a fair copy.&r",
        "&eWhat:&r a hand-held scanner (Warbucks Core, made for this pack). Right-click to read the ore signal in the loaded chunks around you.",
        "&eChemistry:&r heated atoms give off light only at certain wavelengths, an emission spectrum unique to each element. That's how helium was found in the Sun before anyone found it on Earth.",
        "&eHow:&r amethyst prism, steel plates, copper wire and an analog circuit (check JEI). It lists each element with its strength, direction, distance and depth.",
        "&eTip:&r a \"strong\" signal is usually a rich deposit. Walk towards it and scan again."]),
    Q("t3_redstone_module", 0, 0, [item(MI + "redstone_control_module")], "Redstone Control Module", subtitle="An on-off switch for machines",
      section=S_PARTS, deps=["t3_analog"], optional=True, tokens=1, xp=25, desc=[
        "&eWhat:&r slot it into an electric machine or multiblock and a redstone signal decides when it runs.",
        "&eHow:&r redstone, a redstone torch, a capacitor, 2 resistors, 2 inductors and an analog circuit board (check JEI). Configure it in your hand first.",
        "&eTip:&r wire it to a comparator on a tank and a machine stops before its output overflows."]),

    # --- the lead-acid battery ------------------------------------------------------------
    Q("t3_lead", 0, 0, [item(MI + "lead_ingot", 8)], "Lead", subtitle="The heavy half of battery alloy", section=S_BATTERY, deps=["t1_steel"], xp=25, desc=[
        "&eWhat:&r lead is most of the battery alloy in every redstone battery.",
        "&eChemistry:&r most lead comes from galena, lead sulfide (PbS). Roasting drives the sulfur off as SO₂ and carbon reduces the oxide that's left: PbO + C → Pb + CO.",
        "&eHow:&r MI lead ore is common, and rich deposits sit around Y -24 to 16. Smelt the raw lead."]),
    Q("t3_lead_deposit", 0, 5, [item(MI + "raw_lead", 64)], "A Rich Lead Deposit", section=S_BATTERY, deps=["t3_lead"], xp=60, optional=True, tokens=1,
      subtitle="Find a chunk full of lead", desc=[
        "&eWhat:&r rich ore deposits hold hundreds of ores in one chunk, at a metal-specific depth. Lead's sits around Y -24 to 16.",
        "&eHow:&r strip-mine at that depth and check ore with Jade. FTB Ultimine clears a vein in one go.",
        "&eTip:&r galena (lead sulfide, PbS) is the world's main lead ore, and it often carries silver."]),
    Q("t3_antimony", 0, 0, [item(MI + "antimony_ingot", 4)], "Antimony", subtitle="The hardener", section=S_BATTERY, deps=["t1_steel"], xp=25, desc=[
        "&eWhat:&r a brittle, silvery metalloid. A little of it makes soft lead stiff enough to hold its shape in a battery.",
        "&eChemistry:&r antimony's main ore is stibnite, Sb₂S₃. Ancient Egyptians ground it into kohl, the black eyeliner.",
        "&eHow:&r MI antimony ore sits around Y -24 to 16 in rich deposits. Smelt the raw antimony."]),
    Q("t3_battery_dust", 0, 0, [item(MI + "battery_alloy_dust", 4)], "Battery Alloy Dust", subtitle="1 lead + 1 antimony", section=S_BATTERY,
      deps=["t3_lead", "t3_antimony"], xp=20, desc=[
        "&eWhat:&r the mixed powder of lead and antimony.",
        "&eHow:&r grind the ingots in the macerator, then mix 1 lead dust and 1 antimony dust into 2 battery alloy dust in the Steam Mixer."]),
    Q("t3_alloy", 0, 3, [item(MI + "battery_alloy_ingot", 4)], "Battery Alloy", section=S_BATTERY, deps=["t3_battery_dust"], xp=40,
      subtitle="Lead and antimony, as in a car battery", desc=[
        "&eWhat:&r battery alloy makes the casing and grids of redstone batteries.",
        "&eChemistry:&r lead hardened with antimony is the grid metal of real lead-acid batteries. Pure lead is too soft.",
        "&eHow:&r smelt battery alloy dust in any furnace."]),
    Q("t3_battery_plates", 0, 0, [item(MI + "battery_alloy_plate", 2), item(MI + "battery_alloy_curved_plate", 8)], "Battery Plates",
      subtitle="One flat, four curved per battery", section=S_BATTERY, deps=["t3_alloy"], xp=25, desc=[
        "&eWhat:&r each redstone battery is a flat battery alloy plate on top of four curved ones.",
        "&eChemistry:&r in a real lead-acid cell the plates are grids, so the acid can reach as much lead surface as possible. More surface, more current.",
        "&eHow:&r the Steam Compressor presses ingots into plates and plates into curved plates, 1:1."]),
    Q("t3_sulfur", 0, 0, [item("chemlib:sulfur", 8)], "Sulfur from Gunpowder", subtitle="Element 16, the brimstone", section=S_BATTERY, deps=["t1_dissolver"], xp=25, desc=[
        "&eWhat:&r the S in H₂SO₄. Battery acid needs it, and the Dissolver can pull it out of gunpowder.",
        "&eChemistry:&r gunpowder is saltpetre (KNO₃), sulfur and charcoal. One gunpowder dissolves into 2 potassium nitrate, 8 sulfur and 2 graphite.",
        "&eHow:&r creepers drop gunpowder. Blaze powder dissolves into 8 sulfur too."]),
    Q("t3_acid", 2, 5, [item("chemlib:sulfuric_acid", 2)], "Battery Acid", section=S_BATTERY, deps=["t1_combiner", "t3_sulfur"], xp=50,
      subtitle="2 H + S + 4 O → H₂SO₄, in the Combiner", desc=[
        "&eWhat:&r the redstone battery is a real &elead-acid battery&r, and its electrolyte is sulfuric acid. The Combiner from Chapter II makes it from elements.",
        "&eChemistry:&r H₂SO₄ is the most-produced chemical in the world. In a car battery it reacts with the lead plates (Pb + PbO₂ + 2H₂SO₄ → 2PbSO₄ + 2H₂O) and releases electrons; charging runs the reaction backwards.",
        "&eHow:&r pick sulfuric acid in the Combiner and supply 2 hydrogen, 1 sulfur and 4 oxygen. Water or cellulose give the hydrogen and oxygen.",
        "&eTip:&r every LV hull needs two batteries, so keep a stack of acid ready."]),
    Q("t3_battery", 2, 3, [item(MI + "redstone_battery", 2)], "Redstone Battery", section=S_BATTERY, deps=["t3_battery_plates", "t3_wire", "t3_acid"], xp=40,
      subtitle="Lead, antimony and acid: the LV hull needs two", desc=[
        "&eWhat:&r a rechargeable lead-acid battery. Every LV hull holds two.",
        "&eChemistry:&r lead-antimony grids, sulfuric acid electrolyte: the same chemistry as the battery under a car's bonnet.",
        "&eHow:&r 1 battery alloy plate, 4 curved plates, 2 tin cable, 1 redstone and 1 &esulfuric acid&r from the Combiner.",
        "&eTip:&r the LV Storage Unit is built from six of these, so make spares."]),
    Q("t3_storage", 14, -5, [tick()], "LV Storage Unit", section=S_BATTERY, deps=['t3_turbine'], optional=True, tokens=0, xp=0, icon="modern_industrialization:lv_storage_unit", subtitle="Moved: see EU Storage", desc=["&eMoved:&r this step is now \"EU Storage\" on the Power page. Click to dismiss."]),

    # --- the LV hull ----------------------------------------------------------------------
    Q("t3_hull", 6, 1, [item(MI + "basic_machine_hull")], "LV Machine Hull", section=S_HULL, deps=["t3_analog", "t3_battery", "t3_casing"], xp=150, size=1.5,
      items=[(MI + "analog_circuit", 4), (MI + "electric_macerator", 1)], subtitle="The heart of every LV machine", desc=[
        "&6Your hands remember wiring this. Your mind is still catching up.&r",
        "&eWhat:&r &eLV&r (Low Voltage) is the first electric tier. Every LV machine is built on this hull.",
        "&eHow:&r steel machine casing + analog circuit + 2 redstone batteries + 3 tin cable."]),
    Q("t3_magrod", 6, -3, [item(MI + "steel_rod_magnetic", 2)], "Magnetic Steel Rod", section=S_HULL, deps=["t1_steel_parts"], xp=30,
      subtitle="A steel rod surrounded by redstone", desc=[
        "&eWhat:&r the core of an electric motor.",
        "&eChemistry:&r iron-based alloys hold magnetism because their electron spins line up in domains.",
        "&eHow:&r a steel rod ringed by 6 redstone. Later the Polarizer magnetises rods with electricity."]),
    Q("t3_motor", 8, -3, [item(MI + "motor", 2)], "Electric Motor", section=S_HULL, deps=["t3_magrod", "t3_wire"], xp=50,
      subtitle="Electricity in, rotation out", desc=[
        "&eWhat:&r motors drive turbines, pistons, conveyors and robot arms. Nearly every LV machine needs one.",
        "&eChemistry:&r current in a coil next to a magnet creates a force; that's the motor effect. Run it backwards and it's a generator.",
        "&eHow:&r a magnetic steel rod, 2 steel rods, 4 copper wire and 2 tin cable."]),
    Q("t3_tin_parts", 0, 0, [item(MI + "tin_blade", 8), item(MI + "tin_ring", 2), item(MI + "tin_bolt", 8)], "Tin Blades, Rings and Bolts",
      subtitle="Rotor parts in tin", section=S_HULL, deps=["t3_tin_wire"], xp=25, desc=[
        "&eWhat:&r electric machines push fluids with tin rotors, not copper ones.",
        "&eHow:&r the same parts as before: 2 tin curved plates on a tin rod make 4 blades; the Forge Hammer and Cutting Machine make rods, bolts and rings.",
        "&eTip:&r the turbine and the mixer need 2 rotors each and a pump 3. Every rotor is 4 blades."]),
    Q("t3_tin_rotor", 0, 0, [item(MI + "tin_rotor", 4)], "Tin Rotors", subtitle="Blades for the turbine", section=S_HULL, deps=["t3_tin_parts"], xp=30, desc=[
        "&eWhat:&r the spinning heart of the steam turbine, and the stirrer of the electric mixer.",
        "&eHow:&r 4 tin blades, a tin ring and 4 tin bolts."]),
    Q("t3_turbine", 8, -1, [item(MI + "lv_steam_turbine")], "Steam to Electricity", section=S_HULL, deps=["t3_hull", "t3_motor", "t3_tin_rotor"], xp=100,
      subtitle="Your boilers become a power plant", desc=[
        "&eWhat:&r a turbine turns your boiler's steam into &eEU&r, MI's electricity: 1 mB of steam is 1 EU, up to 32 EU/t.",
        "&eHow:&r an LV hull, an analog circuit, 2 tin rotors, 2 motors, 2 fluid pipes and tin cable. Pipe steam in and run tin cable from its output side to your machines.",
        "&eTip:&r one turbine at full speed eats the steam of two steel boilers. If machines stall, add boilers before adding turbines."]),
    Q("t3_energy_hatch", 0, 0, [item(MI + "lv_energy_input_hatch")], "LV Energy Input Hatch", subtitle="Power into a multiblock", section=S_HULL,
      deps=["t3_hull"], xp=30, desc=[
        "&eWhat:&r electric multiblocks take power through energy hatches. The Electric Blast Furnace needs at least one.",
        "&eHow:&r a tin cable on top of an LV machine hull.",
        "&eTip:&r an LV hatch only connects to LV cables. Two hatches double the power a multiblock can draw."]),
    Q("t3_configcard", 6, -5, [item(MI + "config_card")], "Pipe Config Card", section=S_HULL, deps=["t3_hull"], xp=20, optional=True, tokens=1,
      subtitle="Copy one pipe's settings to another", desc=[
        "&eWhat:&r saves an item or fluid pipe connection's settings and pastes them onto other connections.",
        "&eHow:&r sneak + use on a configured pipe connection to save; use on another connection to apply. Sneak + use on air clears it.",
        "&eTip:&r it can also camouflage pipes as any block. The card's tooltip explains how."]),
    Q("t3_pump", 0, 0, [item(MI + "pump", 2)], "Pump", subtitle="A motor that moves fluid", section=S_HULL, deps=["t3_motor", "t3_tin_rotor"],
      optional=True, tokens=1, xp=30, desc=[
        "&eWhat:&r MI's pump component: the Electric Water Pump and the Diesel Generator are built around it.",
        "&eHow:&r 3 fluid pipes, a motor, 3 tin rotors and 2 tin bolts (check JEI)."]),
    Q("t3_waterpump", 16, -5, [item(MI + "electric_water_pump")], "Electric Water Pump", section=S_HULL, deps=["t3_turbine", "t3_pump"], xp=30, optional=True, tokens=1,
      subtitle="Endless water for boilers", desc=[
        "&eWhat:&r pumps water from nothing but power, for boilers and (soon) electrolysis.",
        "&eHow:&r an LV hull with 2 pumps, a tin rotor, fluid pipes, tin cable and an analog circuit.",
        "&eTip:&r next chapter, water becomes hydrogen and oxygen. You'll want lots of it."]),
    Q("t3_diesel", 0, 0, [item(MI + "lv_diesel_generator")], "Burning Creosote", subtitle="An LV generator that burns fluid fuel", section=S_HULL,
      deps=["t3_pump", "t1_creosote"], optional=True, tokens=1, xp=40, desc=[
        "&eWhat:&r the Diesel Generator burns liquid fuels into EU. Right now that means creosote from the Coke Oven, a waste product turned into power.",
        "&eChemistry:&r creosote is a mix of aromatic hydrocarbons and phenols. Burning them releases the energy in their C-H and C-C bonds as heat, just like coal, but it flows through a pipe.",
        "&eHow:&r an LV hull, 2 pumps, 2 tin gears, an analog circuit and 3 tin cable. Check JEI for every fuel it accepts.",
        "&eTip:&r later fuels from the distillation tower burn far longer per bucket."]),

    # --- LV machines ----------------------------------------------------------------------
    Q("t3_piston", 10, -4, [item(MI + "piston", 2)], "Piston", section=S_MACHINES, deps=["t3_motor"], xp=30,
      subtitle="A motor that pushes", desc=[
        "&eWhat:&r MI's piston component, used in the macerator, compressor and robot arm.",
        "&eHow:&r 3 steel plates, 2 steel rods, a steel gear, 2 tin cable and a motor.",
        "&eTip:&r the Electric Macerator needs 2 pistons and the Electric Compressor 4, so make plenty."]),
    Q("t3_conveyor", 10, -2, [item(MI + "conveyor", 2)], "Conveyor", section=S_MACHINES, deps=["t3_motor", "t3_rubber"], optional=True, tokens=1, xp=30,
      subtitle="A rubber belt on two motors", desc=[
        "&eWhat:&r conveyors move items inside machines. The Assembler, Packer and Cutting Machine need them.",
        "&eHow:&r 6 rubber sheets, 2 motors and a tin cable.",
        "&eTip:&r motors are the bottleneck here. Keep a few spare."]),
    Q("t3_robotarm", 12, -3, [item(MI + "robot_arm", 2)], "Robot Arm", section=S_MACHINES, deps=["t3_piston"], optional=True, tokens=1, xp=40,
      subtitle="Motors, a piston and a circuit", desc=[
        "&eWhat:&r robot arms move parts inside the Assembler and Packer.",
        "&eHow:&r two motors, a piston, steel rods, tin cable and an analog circuit.",
        "&eTip:&r the Assembler takes four and the Packer two."]),
    Q("t3_ecompressor", 10, 0, [item(MI + "electric_compressor")], "Electric Compressor", section=S_MACHINES, deps=["t3_turbine", "t3_piston"], optional=True, tokens=1, xp=40,
      subtitle="Plates, faster and without steam", desc=[
        "&eWhat:&r plates, curved plates and rings for every part you'll build next.",
        "&eHow:&r LV hull, four pistons, two analog circuits and two tin cable.",
        "&eTip:&r it doubles as a second plate source while the steam compressor keeps running."]),
    Q("t3_ewiremill", 10, 1, [item(MI + "electric_wiremill")], "Electric Wiremill", section=S_MACHINES, deps=["t3_turbine"], optional=True, tokens=1, xp=40,
      subtitle="Wire, faster", desc=[
        "&eWhat:&r copper wire and fine wire in bulk. Circuits and coils use a lot of it.",
        "&eHow:&r LV hull, 4 motors, 2 analog circuits and 2 tin cable.",
        "&eTip:&r feed it from your compressor's plate output."]),
    Q("t3_polarizer", 10, 2, [item(MI + "polarizer")], "Polarizer", section=S_MACHINES, deps=["t3_turbine", "t3_inductor"], xp=40,
      subtitle="Magnetises rods and wires", desc=[
        "&eWhat:&r magnetic steel rods for motors, and &emagnetic cupronickel wire&r for heating coils.",
        "&eChemistry:&r a strong field lines up the magnetic domains in the metal, and they stay lined up.",
        "&eHow:&r LV hull, 2 inductors, 4 tin wire and 2 tin cable."]),
    Q("t3_mixer", 10, 3, [item(MI + "electric_mixer")], "Electric Mixer", section=S_MACHINES, deps=["t3_turbine", "t3_tin_rotor"], xp=40,
      subtitle="Alloy dusts and chemical mixes", desc=[
        "&eWhat:&r mixing dusts into alloys (bronze, invar, cupronickel, battery alloy) and fluids into mixtures, faster than steam and up to 32 EU/t.",
        "&eHow:&r LV hull, a motor, 2 tin rotors, 2 glass, a fluid pipe and 2 analog circuits.",
        "&eTip:&r recipes that need more than 4 EU/t, like vulcanised synthetic rubber, run here and not in the steam mixer."]),
    Q("t3_emacerator", 12, -5, [item(MI + "electric_macerator")], "Electric Macerator", section=S_MACHINES, deps=["t3_piston", "t3_turbine", "t1_rotary_blade"], xp=40,
      subtitle="Grinding, now electric", desc=[
        "&eWhat:&r ore to crushed dust, ingots back to dust. Still capped at 2x per ore until acids.",
        "&eHow:&r an LV hull, an &einvar rotary blade&r, 2 pistons, 2 motors, 2 analog circuits and tin cable.",
        "&eTip:&r the hull quest reward included one. Build a second for throughput."]),
    Q("t3_cutting", 12, -1, [item(MI + "electric_cutting_machine")], "Cutting Machine", section=S_MACHINES, deps=["t3_conveyor", "t3_turbine", "t1_rotary_blade"],
      optional=True, tokens=1, xp=40, subtitle="Rods, bolts and planks", desc=[
        "&eWhat:&r cutting ingots into rods and bolts, and logs into more planks.",
        "&eHow:&r an LV hull, an invar rotary blade, 2 motors, a conveyor, 2 glass and 2 analog circuits. Its cuts use a little lubricant, the creosote + redstone mix from Chapter II.",
        "&eTip:&r logs give six planks here instead of four."]),
    Q("t3_assembler", 14, -3, [item(MI + "assembler")], "Assembler", section=S_MACHINES, deps=["t3_robotarm", "t3_conveyor"], optional=True, tokens=1, xp=60,
      subtitle="Where MI automation really starts", desc=[
        "&eWhat:&r circuits and machine parts, automatically, from a stocked input.",
        "&eHow:&r LV hull, four robot arms, two conveyors and two analog circuits.",
        "&eTip:&r automate hulls, circuits, motors, pistons, robot arms and conveyors first. With slot locking, one Assembler can hold up to three recipes."]),
    Q("t3_packer", 14, -1, [item(MI + "electric_packer")], "Packer", section=S_MACHINES, deps=["t3_robotarm", "t3_conveyor"], optional=True, tokens=1, xp=40,
      subtitle="Blocks, double ingots and more", desc=[
        "&eWhat:&r compacting ingots into blocks and double ingots, and assembling a few parts. You'll want bauxite blocks next chapter.",
        "&eHow:&r 2 robot arms, 2 conveyors, 3 analog circuits and 2 tin cable on an LV hull.",
        "&eTip:&r unpacking is a separate machine, the Unpacker. Build one if you store metal as blocks."]),
    Q("t3_configurable_chest", 0, 0, [item(MI + "configurable_chest")], "Configurable Chest", subtitle="27 slots that sort and eject", section=S_MACHINES,
      deps=["t3_analog", "t3_motor"], optional=True, tokens=1, xp=30, desc=[
        "&eWhat:&r a chest with lockable slots and auto-eject: a buffer between machines that keeps exactly what you tell it to.",
        "&eHow:&r a steel machine casing, 2 motors, 2 hoppers and 4 analog circuits make 4 chests.",
        "&eTip:&r lock its slots to the parts of a recipe and it becomes a tidy input buffer for an Assembler."]),
    Q("t3_steel_drill", 0, 0, [item(MI + "steel_drill", 4)], "Steel Drills", subtitle="Longer-lasting quarry drills", section=S_MACHINES,
      deps=["t1_opt_quarry", "t3_motor", "t3_analog"], optional=True, tokens=1, xp=40, desc=[
        "&eWhat:&r the steel tier of quarry drill. The Steam Quarry digs a different ore table with them (check JEI).",
        "&eHow:&r a steel drill head, 2 iron gears, 2 item pipes, 2 motors, a tin cable and an analog circuit make 4 drills."]),

    # --- the electric blast furnace -------------------------------------------------------
    Q("t3_cupronickel_dust", 0, 0, [item(MI + "cupronickel_dust", 8)], "Cupronickel Dust", subtitle="1 copper + 1 nickel", section=S_EBF,
      deps=["t1_nickel"], xp=25, desc=[
        "&eWhat:&r the mixed powder for MI's first heating wire.",
        "&eHow:&r in a mixer, 1 copper dust and 1 nickel dust make 2 cupronickel dust. The Steam Mixer can do it.",
        "&eTip:&r the furnace's coils alone take 64 cupronickel ingots. Find a nickel deposit (Y -32 to 8) before you start."]),
    Q("t3_cupronickel_ingot", 0, 0, [item(MI + "cupronickel_ingot", 4), item(MI + "cupronickel_plate", 8)], "Cupronickel Ingots and Plates",
      subtitle="Smelt, then press", section=S_EBF, deps=["t3_cupronickel_dust"], xp=25, desc=[
        "&eWhat:&r cupronickel is drawn into wire from plates, just like copper.",
        "&eChemistry:&r copper and nickel dissolve into each other in any ratio: a true &esolid solution&r, one crystal lattice with both atoms mixed at random.",
        "&eHow:&r smelt the dust into ingots, then press ingots into plates in a compressor."]),
    Q("t3_cupronickel_wire", 0, 0, [item(MI + "cupronickel_wire", 16)], "Cupronickel Wire", subtitle="Two wires per plate", section=S_EBF,
      deps=["t3_cupronickel_ingot", "t3_wiremill"], xp=25, desc=[
        "&eWhat:&r bare cupronickel wire, the start of both coils and heating elements.",
        "&eHow:&r the Wiremill draws 1 cupronickel plate into 2 wire."]),
    Q("t3_cupronickel", 12, 2, [item(MI + "cupronickel_wire_magnetic", 8)], "Magnetic Cupronickel Wire", section=S_EBF, deps=["t3_cupronickel_wire", "t3_polarizer"], xp=50,
      size=1.5, subtitle="Copper-nickel wire for heating coils", desc=[
        "&6A wire that turns current into heat on command. Fire, tamed one more time.&r",
        "&eWhat:&r the heating wire for the Electric Furnace (4) and the Electric Blast Furnace controller (7).",
        "&eChemistry:&r cupronickel (copper + nickel) resists current more than copper and survives heat. Coins and ship pipes use it too.",
        "&eHow:&r magnetise cupronickel wire in the Polarizer, 1:1."]),
    Q("t3_efurnace", 14, 1, [item(MI + "electric_furnace")], "Electric Furnace", section=S_EBF, deps=["t3_cupronickel"], optional=True, tokens=1, xp=40,
      subtitle="Smelting with heat from a wire coil", desc=[
        "&eWhat:&r fast, fuel-free smelting.",
        "&eChemistry:&r current through a resistive wire turns into heat (Joule heating), the same idea as a toaster.",
        "&eHow:&r LV hull wrapped in 4 magnetic cupronickel wire, with 2 analog circuits and tin cable."]),
    Q("t3_cupronickel_cable", 0, 0, [item(MI + "cupronickel_cable", 24)], "Cupronickel Cable", subtitle="Insulated heating wire", section=S_EBF,
      deps=["t3_cupronickel_wire", "t3_rubber"], xp=30, desc=[
        "&eWhat:&r coils are wound from insulated cupronickel cable. Cupronickel cable is also MV-rated if you ever need it for power.",
        "&eHow:&r 3 cupronickel wire between 6 rubber sheets make 3 cable. The Assembler does it with synthetic rubber fluid and no sheets.",
        "&eTip:&r 16 coils need 128 cable. This is where an Assembler and a rubber line pay off."]),
    Q("t3_coils", 0, 0, [item(MI + "cupronickel_coil", 16)], "Cupronickel Coils", subtitle="Two hollow rings of them", section=S_EBF,
      deps=["t3_cupronickel_cable"], xp=50, desc=[
        "&eWhat:&r the heating jacket of the Electric Blast Furnace: two hollow 3x3 rings of 8 coils each.",
        "&eChemistry:&r a coil packs a long wire into a small space, so a lot of resistive heating happens in one block. Kilns and toasters use the same trick.",
        "&eHow:&r 8 cupronickel cable in a ring make 1 coil.",
        "&eTip:&r cupronickel coils run EBF recipes up to 32 EU/t, which covers aluminium and silicon."]),
    Q("t3_invar_plates", 0, 0, [item(MI + "invar_plate", 32)], "A Stack of Invar Plates", subtitle="For the furnace's heatproof shell", section=S_EBF,
      deps=["t1_invar"], xp=25, desc=[
        "&eWhat:&r heatproof casings are 8 invar plates around an invar gear each. The furnace needs a dozen or more.",
        "&eHow:&r mix iron and nickel dust 2:1 into invar dust, smelt, and press the ingots into plates.",
        "&eTip:&r that's well over a hundred plates in all. Run the mixer, a furnace and the compressor in a line."]),
    Q("t3_heatproof", 0, 0, [item(MI + "heatproof_machine_casing", 12)], "Heatproof Machine Casings", subtitle="A floor and a roof that won't warp",
      section=S_EBF, deps=["t3_invar_plates", "t1_invar_parts"], xp=40, desc=[
        "&eWhat:&r the Electric Blast Furnace's bottom and top layers are heatproof casings, with the controller and hatches set into them.",
        "&eChemistry:&r a furnace wall that expands as it heats cracks at the joints. Invar barely expands, so a casing made of it holds its shape at any temperature the coils reach.",
        "&eHow:&r 8 invar plates around an invar gear. You need up to 14: 18 blocks in the two layers, minus the controller and each hatch."]),
    Q("t3_ebf", 14, 3, [item(MI + "electric_blast_furnace")], "Electric Blast Furnace", section=S_EBF,
      deps=["t3_cupronickel", "t3_coils", "t3_heatproof", "t3_energy_hatch"], xp=200, size=2.0, shape="gear",
      subtitle="The furnace that makes aluminum", desc=[
        "&6Fire you can measure in volts. You used to do this without the volts.&r",
        "&eWhat:&r MI's big furnace multiblock. With cupronickel coils it reaches the heat for &ealuminum&r and &esilicon&r.",
        "&eHow:&r the controller is an LV hull, 7 magnetic cupronickel wire and a blast furnace. Build a layer of heatproof casings (controller in it), two hollow rings of cupronickel coils, and another heatproof layer. Hatches go in the top or bottom layer: an LV energy input hatch and item hatches.",
        "&eTip:&r hold a hatch or wrench near the controller to see the valid positions highlighted. JEI shows the whole shape in 3D."]),

    # --- Mekanism -------------------------------------------------------------------------
    Q("t3_osmium", 6, 6, [item("mekanism:raw_osmium", 8)], "Osmium", section=S_MEK, deps=["t3_hull"], xp=40,
      subtitle="Mekanism's blue-grey metal", desc=[
        "&eWhat:&r Mekanism builds almost everything from osmium: its infuser, casings and circuits.",
        "&eChemistry:&r real osmium is the densest natural element, 22.6 g/cm³. A litre of it weighs about as much as a big dog.",
        "&eHow:&r osmium ore is common in small veins underground. Mine it with an iron pickaxe or better."]),
    Q("t3_osmium_ingot", 0, 0, [item("mekanism:ingot_osmium", 8)], "Osmium Ingots", subtitle="Raw osmium, smelted", section=S_MEK, deps=["t3_osmium"], xp=20, desc=[
        "&eWhat:&r the Metallurgic Infuser, the Steel Casing and every Basic Control Circuit each take an osmium ingot.",
        "&eChemistry:&r osmium is named for its smell: the Greek &eosme&r. Powdered osmium slowly oxidises in air to OsO₄, a volatile and very toxic oxide with a sharp odour.",
        "&eHow:&r smelt raw osmium in any furnace."]),
    Q("t3_osmium_hoard", 6, 8, [item("mekanism:ingot_osmium", 32)], "Osmium Hoard", section=S_MEK, deps=["t3_osmium_ingot"], xp=60, optional=True, tokens=1,
      subtitle="Stockpile for the Mekanism build-out", desc=[
        "&eWhat:&r every Mekanism machine, casing and circuit costs osmium. A stockpile saves trips.",
        "&eHow:&r smelt or enrich raw osmium into ingots.",
        "&eTip:&r the Enrichment Chamber doubles osmium ore, so process it there once it's built."]),
    Q("t3_infuser", 8, 6, [item("mekanism:metallurgic_infuser")], "Mekanism: Metallurgic Infuser", section=S_MEK, deps=["t3_osmium_ingot"], xp=60,
      subtitle="Infuse metals with carbon, redstone and more", desc=[
        "&eWhat:&r Mekanism's entry machine. It infuses metals with other materials.",
        "&eHow:&r 4 iron ingots, 2 redstone, an osmium ingot and 2 furnaces.",
        "&eTip:&r it runs on FE. Your Chapter II generator works, or a Mekanism Heat Generator (Power chapter)."]),
    Q("t3_infused", 8, 8, [item("mekanism:alloy_infused", 4)], "Infused Alloy", section=S_MEK, deps=["t3_infuser"], xp=40,
      subtitle="Copper infused with redstone", desc=[
        "&eWhat:&r Mekanism's basic alloy. The Enrichment Chamber and many basic machines need it.",
        "&eChemistry:&r a real alloy mixes metals at the atomic level. Here redstone plays the part of the second element.",
        "&eHow:&r put redstone in the infuser's left slot (it becomes an infusion buffer), then feed copper ingots."]),
    Q("t3_mekcircuit", 10, 6, [item("mekanism:basic_control_circuit", 2), item("mekanism:steel_casing")], "Mekanism Circuits", section=S_MEK,
      deps=["t3_infuser", "t3_analog"], xp=75, subtitle="MI's analog circuit, in Mekanism form", desc=[
        "&eWhat:&r in this pack, a Basic Control Circuit is &eMI Analog Circuit + osmium ingot&r (shapeless). Each Mekanism circuit tier needs the matching MI circuit.",
        "&eHow:&r the Steel Casing (4 steel, 4 glass and an osmium ingot) is the frame for most Mekanism machines.",
        "&eTip:&r make several casings at once. Every Mekanism machine in the next chapter needs one."]),
    Q("t3_enrich", 12, 6, [item("mekanism:enrichment_chamber")], "Enrichment Chamber", section=S_MEK, deps=["t3_mekcircuit", "t3_infused"], xp=60,
      subtitle="Mekanism's 2x ore processing", desc=[
        "&eWhat:&r ore → 2 dust. It also turns dirty dust into clean dust in the higher-tier lines.",
        "&eHow:&r steel casing, 4 infused alloy, 2 iron and 2 basic control circuits.",
        "&eTip:&r 3x, 4x and 5x need gases and acids: that's the next chapter."]),
    Q("t3_crusher", 12, 8, [item("mekanism:crusher")], "Crusher", section=S_MEK, deps=["t3_mekcircuit"], xp=40,
      subtitle="Clumps into dirty dust", desc=[
        "&eWhat:&r crushes ingots to dust and, later, ore clumps into dirty dust in the 3x+ lines.",
        "&eHow:&r steel casing, 2 basic control circuits, 4 redstone and 2 lava buckets.",
        "&eTip:&r it also turns ingots back into dust, handy for alloy recipes."]),
])
