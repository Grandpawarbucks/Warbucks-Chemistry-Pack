"""Quest chapter: integrated. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

Mirror of ATM10's "Integrated Dynamics" chapter (user decision 2026-10-20: quest for quest where we have the mod; the
same items, order, clusters and sizes; the text is ours). Split out of logic.py on 2026-10-20 (keys unchanged), so
each quest now carries its ATM10 id. The Integrated Dynamics wrench, logic cables, variable cards and the Integrated
Tunnels interfaces stay on the logistics page (logic.py), where ATM10's Basic Logistics asks for them.

ATM10 Integrated Dynamics quests skipped: the credits checkmark, the Productive Bees menril bee (no Productive Bees),
and five that repeat a Basic Logistics item (wrench, cable, variable card, the interfaces).
"""
from questlib import Q, Chapter, item, dim, tick, kill, anyof, anytag, MAIN, SIDE  # noqa: F401

OPT = dict(optional=True, tokens=1)
S_MENRIL, S_IDL = "Menril and Resin", "Logic Networks"

CHAPTER = Chapter("integrated", "Integrated Dynamics", "integrateddynamics:logic_programmer",
        ["Logic networks grown from resin."], SIDE, mirror="integrated_dynamics", quests=[
    # ===== Menril and Resin (ATM10 Integrated Dynamics, left side) ===========================
    Q("lg_menril_wood", 0, 0, [item("integrateddynamics:menril_log")], "Menril Trees", section=S_MENRIL, mirror="499CF9F39CED8899", deps=["t3_hull"], xp=40,
      size=1.5, subtitle="Blue-grey wood full of resin", desc=[
        "&6Thought made solid, growing on a tree. You remember building minds out of stranger things.&r",
        "&eWhat:&r Menril trees are where Integrated Dynamics starts: logs for resin, and berries from the leaves.",
        "&eChemistry:&r real tree resins are mixtures of terpenes, small hydrocarbons that plants build from isoprene units (C₅H₈). Amber is resin that hardened over millions of years.",
        "&eHow:&r find a Menril tree in the Overworld (Jade names it) and plant its saplings near your base."]),
    Q("lg_menril_berries", 0, 0, [item("integrateddynamics:menril_berries")], "Menril Berries", section=S_MENRIL, mirror="6C9191DA4B1039D6", deps=["lg_menril_wood"],
      xp=20, subtitle="A snack with side effects", desc=[
        "&eWhat:&r berries drop from Menril leaves.",
        "&eHow:&r break or wait for Menril leaves to decay.",
        "&eTip:&r read the berries' tooltip before you eat a stack."]),
    Q("lg_menril_seeds", 0, 0, [item("mysticalagriculture:menril_seeds")], "Menril Seeds", section=S_MENRIL, mirror="232A06C9FF0EE7B2", deps=["lg_menril_berries"],
      xp=60, **OPT, subtitle="Optional: grow Menril as a crop", desc=[
        "&eWhat:&r Mystical Agriculture can grow Menril essence, which crafts into Menril logs, so you never chase trees again.",
        "&eHow:&r check JEI for the seed; its tier sets which Mystical Agriculture essence and circuit it needs.",
        "&eTip:&r the Mystical Agriculture page covers seed tiers."]),
    Q("lg_squeezer", 0, 0, [item("integrateddynamics:squeezer")], "Squeezer", section=S_MENRIL, mirror="68498ADEF9765F81", deps=["lg_menril_wood"], xp=40,
      subtitle="Press the resin out", desc=[
        "&eWhat:&r the Squeezer presses Menril logs into liquid resin.",
        "&eHow:&r an iron block, iron, planks and sticks (check JEI). Put a Menril log in and jump on it a few times.",
        "&eTip:&r it presses other things too. Ores give 2 raw ores in this pack, like every early processor."]),
    Q("lg_drying_basin", 0, 0, [item("integrateddynamics:drying_basin")], "Drying Basin", section=S_MENRIL, mirror="62B4A37CFDECA679", deps=["lg_squeezer"], xp=40,
      subtitle="Leave the resin to set", desc=[
        "&eWhat:&r the Drying Basin dries Menril resin into crystalized Menril chunks.",
        "&eChemistry:&r drying is evaporation: the solvent leaves and the dissolved solids stay, just as salt is left when brine dries.",
        "&eHow:&r logs, iron and black dye (check JEI). Place the Squeezer on top of the basin and the resin flows straight in."]),
    Q("lg_menril", 0, 0, [item("integrateddynamics:crystalized_menril_chunk", 10)], "Crystalized Menril", section=S_MENRIL, mirror="72F57D77C3FB366D",
      deps=["lg_drying_basin"], xp=60, subtitle="The building block of logic", desc=[
        "&eWhat:&r crystalized Menril chunks make every cable, card and part of Integrated Dynamics.",
        "&eHow:&r dry resin in the basin, a bucket at a time.",
        "&eTip:&r nine chunks make a block, and some recipes want the block."]),
    Q("lg_id_power", 0, 0, [item("integrateddynamics:energy_battery")], "Energy Battery", section=S_MENRIL, mirror="6D75CF34957ECCD9", deps=["lg_menril"], xp=40,
      subtitle="Power for a logic network", desc=[
        "&eWhat:&r the Energy Battery stores FE and can feed a network through its cables.",
        "&eHow:&r crystalized Menril chunks and blocks around a redstone block (check JEI).",
        "&eTip:&r any FE source works; link a cable to your main grid instead if you have one."]),
    Q("lg_id_coalgen", 0, 0, [item("integrateddynamics:coal_generator")], "ID Generator", section=S_MENRIL, mirror="4D62C62B523C69EC", deps=["lg_id_power"], xp=30,
      **OPT, subtitle="Optional: burn fuel for the network", desc=[
        "&eWhat:&r Integrated Dynamics' own Generator burns furnace fuel for FE.",
        "&eChemistry:&r burning charcoal is C + O₂ → CO₂, about 33 kJ of heat for every gram of carbon.",
        "&eHow:&r an Energy Battery plus a furnace (check JEI)."]),
    Q("lg_id_mech", 0, 0, [item("integrateddynamics:mechanical_squeezer")], "Mechanical Squeezer", section=S_MENRIL, mirror="44DA091B53473723",
      deps=["lg_id_power", "lg_squeezer"], xp=50, **OPT, subtitle="Optional: no more jumping", desc=[
        "&eWhat:&r the powered Squeezer: faster and pipe-friendly.",
        "&eHow:&r the Squeezer with Energy Batteries, a diamond and obsidian (check JEI). Feed it FE.",
        "&eTip:&r ore output is capped at 2 raw ores in this pack, the same as the hand-powered one."]),
    Q("lg_id_mech_basin", 0, 0, [item("integrateddynamics:mechanical_drying_basin")], "Mechanical Drying Basin", section=S_MENRIL, mirror="7413BB136EF9D6C5",
      deps=["lg_id_power", "lg_drying_basin"], xp=50, **OPT, subtitle="Optional: drying on power", desc=[
        "&eWhat:&r the powered Drying Basin: it dries resin much faster.",
        "&eHow:&r the Drying Basin with Energy Batteries and more (check JEI).",
        "&eTip:&r press U on it in JEI to see what else it dries."]),

    # ===== Logic Networks (ATM10 Integrated Dynamics, right side) ============================
    Q("lg_id_transformers", 0, 0, [item("integrateddynamics:variable_transformer_input")], "Input Transformer", section=S_IDL, mirror="3BC94B0B922C0708",
      deps=["lg_id_variable"], xp=30, subtitle="The part inside every importer", desc=[
        "&eWhat:&r input variable transformers are the crafting parts of readers and importers.",
        "&eHow:&r variable cards, Menril chunks and a sticky piston (check JEI). Craft extra before a big build.",
        "&eTip:&r one transformer per part, so a dozen goes quickly."]),
    Q("lg_id_transformer_out", 0, 0, [item("integrateddynamics:variable_transformer_output")], "Output Transformer", section=S_IDL, mirror="6D9FA4DF842C1010",
      deps=["lg_id_variable"], xp=30, subtitle="The part inside every exporter", desc=[
        "&eWhat:&r output variable transformers are the crafting parts of writers and exporters.",
        "&eHow:&r like the input one, mirrored (check JEI).",
        "&eTip:&r keep both kinds in a chest next to your crafting table."]),
    Q("lg_id_importers", 0, 0, [anyof([f"integratedtunnels:part_importer_{k}" for k in
                                       ("energy", "world_energy", "item", "world_item", "fluid", "world_fluid", "world_block")])],
      "Importers", section=S_IDL, mirror="73EA326304C01C3B", deps=["lg_id_transformers"], xp=40, subtitle="Pull things into the network", desc=[
        "&eWhat:&r importers pull items, fluids or energy into the network. World importers take straight from the world: they break blocks, pick up items, or drain fluid.",
        "&eHow:&r an input transformer and a few extras per part (check JEI). Any importer counts.",
        "&eTip:&r a world block importer with a filter is a tidy quarry face."]),
    Q("lg_id_exporters", 0, 0, [anyof([f"integratedtunnels:part_exporter_{k}" for k in
                                       ("energy", "world_energy", "item", "world_item", "fluid", "world_fluid", "world_block")])],
      "Exporters", section=S_IDL, mirror="33F4A7613764A016", deps=["lg_id_transformer_out"], xp=40, subtitle="Push things out where you want them", desc=[
        "&eWhat:&r exporters push items, fluids or energy out of the network. World exporters place blocks, drop items or pour fluid.",
        "&eHow:&r an output transformer and a few extras per part (check JEI). Any exporter counts.",
        "&eTip:&r a world block exporter is an automatic block placer for a cobble or basalt generator."]),
    Q("lg_tunnels", 0, 0, [tick()], "Integrated Tunnels", section=S_IDL, mirror="65FA86357BC60573", deps=["lg_id_importers", "lg_id_exporters", "lg_idt_item"],
      xp=60, size=1.5, subtitle="Move items, fluids and energy with logic", desc=[
        "&eWhat:&r importers, exporters and interfaces together move anything along the logic cables, controlled by variables.",
        "&eHow:&r put an Item Importer on a chest and an Item Exporter on a machine, and give the exporter a variable card that says what to move. Click the checkmark when it works.",
        "&eTip:&r a fluid exporter with a yes/no variable from a tank reader only fills the reactor when it's below half."]),
    Q("lg_id", 0, 0, [item("integrateddynamics:logic_programmer")], "Logic Programmer", section=S_IDL, mirror="4D4152032F0410D2", deps=["lg_tunnels"], xp=60,
      subtitle="Write rules onto cards", desc=[
        "&eWhat:&r the Logic Programmer writes values and rules onto variable cards: 'tank above 90%', 'more than 64 sulfur', and so on.",
        "&eHow:&r Menril chunks and a few extras (check JEI). Pick an operator on the left, fill in its inputs, and write it onto a blank card.",
        "&eTip:&r a Redstone Writer turns a yes/no card into a signal: perfect for stopping a separator when its tank is full."]),
    Q("lg_id_portable", 0, 0, [item("integrateddynamics:portable_logic_programmer")], "Portable Programmer", section=S_IDL, mirror="1568CBFA09827137", deps=["lg_id"],
      xp=40, subtitle="The programmer in your pocket", desc=[
        "&eWhat:&r the same Logic Programmer, as an item.",
        "&eHow:&r a Logic Programmer and Menril chunks (check JEI).",
        "&eTip:&r carry it while wiring up a factory, so you can fix a card on the spot."]),
    Q("lg_id_tip", 0, 0, [tick()], "Challenge: The Self-Stopping Separator", section=S_IDL, mirror="1B5C86AE05678420", deps=["lg_tunnels"], xp=150, **OPT,
      subtitle="Your first closed loop", desc=[
        "&eWhat:&r make a Mekanism Electrolytic Separator turn itself off when its hydrogen tank is 90% full, and back on below 50%.",
        "&eHow:&r a Reader on the tank → a comparison in the Logic Programmer → a Redstone Writer on the separator (set it to redstone control in its GUI).",
        "&eTip:&r the gap between 50% and 90% (hysteresis) stops it flickering on and off.",
        "Click the checkmark once it works."]),
    Q("lg_id_aspects", 0, 0, [tick()], "Note: Readers and Aspects", section=S_IDL, mirror="437F4945AFBE0825", deps=["lg_tunnels"], xp=30,
      icon="integrateddynamics:variable", subtitle="What a reader can tell you", desc=[
        "&eWhat:&r every Reader part (inventory, fluid, energy, redstone, world and more) offers a list of aspects: single values it can read, like 'fill ratio' or 'item count'.",
        "&eHow:&r right-click a placed reader to see its aspects, and drag one onto a blank card to save it. Display Panels show a card's value live.",
        "&eTip:&r a Display Panel on every main tank is a cheap base dashboard. Click the checkmark when you've read one value."]),
    Q("lg_crafting", 0, 0, [item("integratedcrafting:part_interface_crafting")], "Integrated Crafting", section=S_IDL, mirror="65D89991A45BC042", deps=["lg_id"],
      xp=60, subtitle="Autocrafting without AE2", desc=[
        "&eWhat:&r the Crafting Interface crafts on demand through the ID network, much like AE2 patterns.",
        "&eHow:&r write recipes onto variable cards with the Logic Programmer and put them in the interface on a machine (check JEI for the part).",
        "&eTip:&r it's a cheaper autocrafter than AE2 for small chains, like rubber sheets or redstone batteries."]),
    Q("lg_id_store", 0, 0, [item("integrateddynamics:variablestore")], "Variable Store", section=S_IDL, mirror="60D9F04E91171D16", deps=["lg_id"], xp=50, size=1.5,
      subtitle="Keep your logic in one place", desc=[
        "&eWhat:&r the Variable Store holds variable cards so the whole network can use them.",
        "&eHow:&r check JEI. Put cards in the store and reference them from any writer or display panel on the network.",
        "&eTip:&r name cards with the Labeller after what they measure ('H2 tank %'). You'll thank yourself later."]),
    Q("lg_terminals", 0, 0, [item("integratedterminals:part_terminal_crafting_job")], "Crafting Job Terminal", section=S_IDL, mirror="56BF647EA84FFF7E",
      deps=["lg_crafting"], xp=50, subtitle="Watch the network craft", desc=[
        "&eWhat:&r Integrated Terminals' Crafting Job Terminal shows what Integrated Crafting is working on and what it's waiting for.",
        "&eHow:&r check JEI; it's a part, so it goes on a cable.",
        "&eTip:&r the Storage Terminal part (and its portable version) shows everything on the network, like an ME terminal."]),
], links=[("t3_hull", 0, 0), ("lg_id_variable", 0, 0), ("lg_idt_item", 0, 0)])
