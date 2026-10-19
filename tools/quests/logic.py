"""Quest chapter: logic. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, kill, anyof, MAIN, SIDE  # noqa: F401

# Layout: y=0 ComputerCraft, y=-2 turtles + AE2 automation, y=2 Integrated Dynamics,
# y=4 SFM + Logistics Networks, y=6 LaserIO. Capstone at the right end of y=0.
CHAPTER = Chapter("logic", "Automation and Logic", "computercraft:computer_advanced",
        ["Make the factory run itself."], SIDE, [
    # --- ComputerCraft (y = 0) -----------------------------------------------------------------
    Q("lg_computer", 0, 0, [item("computercraft:computer_normal")], "A Computer", subtitle="Lua, in a box", deps=["t3_hull"], xp=50, desc=[
        "&6You never did your own chores. You remember having things that did them for you.&r",
        "&eWhat:&r CC: Tweaked computers run Lua programs: monitor tanks, balance chemical lines, build a base dashboard.",
        "&eHow:&r place it and right-click. Type &ehelp&r, or &eedit startup&r to write a program that runs on boot.",
        "&eTip:&r Mekanism machines can be read by computers directly. Put a computer next to one and try &eperipheral.getNames()&r."]),
    Q("lg_monitor", 2, 0, [item("computercraft:monitor_advanced", 4)], "Monitors", subtitle="A screen for your numbers", deps=["lg_computer"], xp=50, desc=[
        "&eWhat:&r monitors show program output on a wall. Placed together, they join into one big screen.",
        "&eHow:&r put monitors next to the computer and run &emonitor <side> <program>&r to send output to them.",
        "&eTip:&r advanced monitors show colour and accept clicks, so you can make touch buttons."]),
    Q("lg_modem", 4, 0, [item("computercraft:wired_modem", 2), item("computercraft:cable", 16)], "Wired Networks", subtitle="Reach machines across the room", deps=["lg_monitor"], xp=60, desc=[
        "&eWhat:&r wired modems and networking cable connect a computer to machines that aren't touching it.",
        "&eHow:&r put a modem on the machine, run cable back to a modem on the computer, and right-click the machine's modem to attach it.",
        "&eTip:&r each attached peripheral gets a name. List them with &eperipheral.getNames()&r."]),
    Q("lg_wireless", 4, -2, [item("computercraft:wireless_modem_advanced"), item("computercraft:pocket_computer_advanced")], "Ender Modem", subtitle="Talk across dimensions", deps=["lg_modem"], xp=100, optional=True, tokens=1, desc=[
        "&eWhat:&r the Ender Modem sends messages with no range limit, even between dimensions. A pocket computer carries a terminal with you.",
        "&eHow:&r use &erednet&r on both ends: one computer broadcasts tank levels, your pocket computer reads them.",
        "&eTip:&r a remote alarm for your reactor is a very good idea."]),
    Q("lg_turtle", 2, -2, [item("computercraft:turtle_normal")], "Turtles", subtitle="Robots you program", deps=["lg_computer"], xp=75, desc=[
        "&eWhat:&r turtles are programmable robots that mine, build and farm.",
        "&eHow:&r craft one with a tool (a pickaxe makes a mining turtle) and fuel it with coal.",
        "&eTip:&r try the built-in &eexcavate&r and &etunnel&r programs first."]),
    Q("lg_peripherals", 6, 0, [item("advancedperipherals:energy_detector"), item("advancedperipherals:me_bridge")], "Advanced Peripherals", subtitle="Read power flow and your ME network", deps=["lg_modem", "t5_ae2"], xp=150, desc=[
        "&eWhat:&r extra peripherals: the Energy Detector measures power flow; the ME Bridge reads (and requests crafts from) your whole AE2 network.",
        "&eHow:&r place them on your wired network like any other peripheral.",
        "&eTip:&r an ME Bridge program can keep your stock of every intermediate topped up."]),
    Q("lg_dashboard", 8, 0, [item("advancedperipherals:fluid_detector"), item("computercraft:monitor_advanced", 8)], "Base Dashboard", subtitle="Every tank on one screen", deps=["lg_peripherals"], xp=150, desc=[
        "&eWhat:&r a wall screen that shows your chemical stocks, power and flow rates at a glance.",
        "&eHow:&r the Fluid Detector measures flow through a pipe. Combine it with tank readings and the energy detector in one program.",
        "&eTip:&r colour lines red when a tank drops below 20%. You'll spot problems from across the room."]),

    # --- AE2 automation (y = -2) ---------------------------------------------------------------
    Q("lg_ae_io", 8, -2, [item("ae2:import_bus"), item("ae2:export_bus"), item("ae2:storage_bus")], "Buses", subtitle="AE2 pulls, pushes and reads", deps=["t5_ae2"], xp=100, desc=[
        "&eWhat:&r an import bus pulls items out of a machine, an export bus pushes them in, and a storage bus lets ME see inside a chest or tank.",
        "&eHow:&r place them on cable facing the machine. Set filters in each bus's GUI.",
        "&eTip:&r Applied Mekanistics is in the pack, so buses and storage also handle Mekanism gases like hydrogen and SO₂."]),
    Q("lg_cpu", 10, -2, [item("ae2:crafting_unit", 2), item("ae2:1k_crafting_storage")], "Crafting CPU", subtitle="The part of AE2 that plans", deps=["lg_ae_io"], xp=150, desc=[
        "&eWhat:&r a crafting CPU is a multiblock that works out and tracks autocrafting jobs.",
        "&eHow:&r build a solid box of crafting units with at least one crafting storage, and connect it to your network.",
        "&eTip:&r more storage lets it plan bigger jobs; co-processing units run more steps at once."]),
    Q("lg_encode", 12, -2, [item("ae2:pattern_encoding_terminal"), item("ae2:blank_pattern", 8)], "Encoding Patterns", subtitle="Teach AE2 a recipe", deps=["lg_cpu"], xp=100, desc=[
        "&eWhat:&r a pattern is a recipe card: these inputs make that output.",
        "&eHow:&r in the Pattern Encoding Terminal, switch to Processing mode for machine recipes and fill in the inputs and outputs.",
        "&eTip:&r processing patterns work for any machine: MI, Mekanism or the Combiner."]),
    Q("lg_patterns", 14, -1, [item("ae2:pattern_provider"), item("ae2:molecular_assembler")], "Autocraft a Chemical Line", subtitle="Pattern providers drive your machines", deps=["lg_encode"], xp=200, desc=[
        "&eWhat:&r pattern providers push ingredients into machines; molecular assemblers do crafting-table recipes.",
        "&eHow:&r put a provider against an MI or Mekanism machine, load a processing pattern, and send the output back into the network.",
        "&eTip:&r chain patterns (sulfur → SO₂ → SO₃ → H₂SO₄) and one request runs the whole line."]),
    Q("lg_level", 12, 0, [item("ae2:level_emitter")], "Level Emitters", subtitle="Stop at enough", deps=["lg_dashboard", "lg_ae_io"], xp=100, desc=[
        "&eWhat:&r a level emitter gives a redstone signal when the network holds more (or less) than a number you set.",
        "&eHow:&r set the item and the amount, then wire the signal to a machine's redstone control.",
        "&eTip:&r stop the Electrolytic Separator when hydrogen hits your target and you never waste power on a full tank."]),
    Q("lg_acid_line", 16, 0, [item("modern_industrialization:sulfuric_acid_bucket", 16), tick()], "Fully Automated Sulfuric Acid", subtitle="Sulfur in, acid out, no hands", deps=["lg_patterns", "lg_level"], xp=1000, size=2.0, shape="gear", desc=[
        "&6The factory hums without you. You remember this kind of quiet.&r",
        "&eWhat:&r a line that makes sulfuric acid on its own and stops when the tanks are full.",
        "&eChemistry:&r 2SO₂ + O₂ → 2SO₃ (industry uses a vanadium oxide catalyst), then SO₃ + H₂O → H₂SO₄.",
        "&eHow:&r Separator (O₂) → Oxidizer (S → SO₂) → Infuser (SO₃) → Rotary Condensentrator (water vapour) → Infuser (H₂SO₄). Feed sulfur with a bus or LaserIO and gate it with a level emitter.",
        "&eTip:&r when it runs a full day with no help, fill 16 buckets and click the checkmark."]),

    # --- Integrated Dynamics (y = 2) -----------------------------------------------------------
    Q("lg_menril", 0, 2, [item("integrateddynamics:crystalized_menril_chunk", 16)], "Menril Resin", subtitle="The tree that grows logic", deps=["t3_hull"], xp=60, desc=[
        "&eWhat:&r Integrated Dynamics builds everything from crystallised Menril, a resin from Menril trees.",
        "&eChemistry:&r drying resin is just evaporation: the liquid loses its solvent and hardens, like tree sap turning into amber.",
        "&eHow:&r squeeze Menril logs in a Squeezer for resin, then dry the resin in a Drying Basin.",
        "&eTip:&r Menril trees grow wild in the Overworld. Plant the saplings once you find one."]),
    Q("lg_id", 2, 2, [item("integrateddynamics:cable", 8), item("integrateddynamics:logic_programmer"), item("integrateddynamics:variable", 4)], "Integrated Dynamics", subtitle="Logic networks without code", deps=["lg_menril"], xp=100, desc=[
        "&eWhat:&r read a value (tank level, item count), apply logic, and act on it, all with blocks and cards.",
        "&eHow:&r a Reader part (e.g. Fluid Reader) on a tank exposes values. Write one onto a Variable Card in the Logic Programmer.",
        "&eTip:&r a Redstone Writer can then turn that value into a signal: perfect for stopping a separator when its tank is full."]),
    Q("lg_id_store", 4, 2, [item("integrateddynamics:variablestore"), item("integrateddynamics:labeller")], "Variable Store", subtitle="Keep and name your logic", deps=["lg_id"], xp=75, desc=[
        "&eWhat:&r the Variable Store holds variable cards so the whole network can use them; the Labeller names them.",
        "&eHow:&r put cards in the store and reference them from any writer or display panel on the network.",
        "&eTip:&r name cards after what they measure ('H2 tank %'). You'll thank yourself later."]),
    Q("lg_id_tip", 7, 3, [tick()], "Challenge: The Self-Stopping Separator", subtitle="Your first closed loop", deps=["lg_id_store"], xp=150, optional=True, tokens=1, desc=[
        "&eWhat:&r make a Mekanism Electrolytic Separator turn itself off when its hydrogen tank is 90% full, and back on below 50%.",
        "&eHow:&r a Reader on the tank → a comparison in the Logic Programmer → a Redstone Writer on the separator (set it to redstone control in its GUI).",
        "&eTip:&r the gap between 50% and 90% (hysteresis) stops it flickering on and off.",
        "Click the checkmark once it works."]),

    # --- SFM + Logistics Networks (y = 4) ------------------------------------------------------
    Q("lg_sfm", 2, 4, [item("sfm:manager"), item("sfm:cable", 8), item("sfm:disk")], "Super Factory Manager", subtitle="One block scripts the whole factory", deps=["lg_id"], xp=100, desc=[
        "&eWhat:&r one Manager block runs a short program that moves items, fluids and energy between everything on its cables.",
        "&eHow:&r put the disk in the Manager and write a program, e.g. &eEVERY 20 TICKS DO INPUT FROM a OUTPUT TO b END&r.",
        "&eTip:&r the in-game editor has examples. Start with one input and one output."]),
    Q("lg_sfm_label", 4, 4, [item("sfm:labelgun"), item("sfm:network_tool")], "Labels", subtitle="Name every machine", deps=["lg_sfm"], xp=60, desc=[
        "&eWhat:&r the Label Gun tags inventories with names (like &ea&r and &eb&r above) for your programs.",
        "&eHow:&r set a label in the gun, then right-click each machine. The Network Tool shows what's connected.",
        "&eTip:&r label by job ('sulfur_in', 'acid_out'), not by machine type."]),
    Q("lg_logistics", 6, 4, [item("logisticsnetworks:logistics_node", 2)], "Logistics Network", subtitle="Nodes that route by rules", deps=["lg_sfm_label"], xp=75, desc=[
        "&eWhat:&r Logistics Network nodes sit on machines and chests and move items, fluids and energy between every node in the same named network, with no cables.",
        "&eHow:&r obsidian, a redstone block, hoppers, an eye of ender and a redstone torch for a node (check JEI). Open a node to create or join a network, then set what it imports and exports.",
        "&eTip:&r the Wrench has a copy-paste mode: set up one node, then paste its settings onto the rest."]),
    Q("lg_logistics_filter", 8, 5, [item("logisticsnetworks:tag_filter"), item("logisticsnetworks:amount_filter")], "Logistics Filters", subtitle="Move only what you mean to", deps=["lg_logistics"], xp=75, optional=True, tokens=1, desc=[
        "&eWhat:&r filters narrow what a node moves: by tag, by amount and more.",
        "&eHow:&r put a filter in a node's slot and set it up in its GUI (check JEI for all the filter types).",
        "&eTip:&r a tag filter for 'c:dusts' sends every dust to one chest."]),
    # Moved from storage.py (keys unchanged) when its Logistics Networks row was removed (2026-10-18).
    Q("sto_ln_upgrade", 8, 3, [item("logisticsnetworks:iron_upgrade"), item("logisticsnetworks:gold_upgrade")], "Node Upgrades", subtitle="Bigger batches, shorter delays", deps=["lg_logistics"], xp=60, optional=True, tokens=1, desc=[
        "&eWhat:&r upgrades raise how much a node moves per batch and how often. Iron, gold, diamond and netherite tiers each do more.",
        "&eHow:&r the tier's metal, hoppers, chests and smooth stone (check JEI). Put them in the node's upgrade slots.",
        "&eTip:&r the upgrade's tooltip lists its exact items, fluid and energy per batch."]),
    Q("sto_ln_chem", 10, 3, [item("logisticsnetworks:mekanism_chemical_upgrade")], "Moving Chemicals", subtitle="Nodes that carry Mekanism gases", deps=["sto_ln_upgrade", "t3_infuser"], xp=75, optional=True, tokens=1, desc=[
        "&eWhat:&r the Mekanism Chemical Upgrade lets nodes move Mekanism chemicals: H₂, O₂, Cl₂, SO₂ and the rest.",
        "&eChemistry:&r the contact process needs SO₂ and O₂ in the same place: 2SO₂ + O₂ → 2SO₃. Nodes can bring both to one Chemical Infuser.",
        "&eHow:&r basic chemical tanks, infused alloy, chests and an Iron Upgrade (check JEI).",
        "&eTip:&r one network for gases and another for items keeps the settings easy to read."]),
    Q("sto_ln_computer", 10, 5, [item("logisticsnetworks:computer")], "Network Manager", subtitle="Optional: see every node and its flow", deps=["lg_logistics"], xp=50, optional=True, tokens=1, desc=[
        "&eWhat:&r the Computer opens a Network Manager that lists your networks, their nodes and how much each channel moves.",
        "&eHow:&r iron, glass and a comparator (check JEI).",
        "&eTip:&r when a line stops, look here first: a channel with no flow shows where the jam is."]),

    # --- LaserIO (y = 6) ---------------------------------------------------------------------
    Q("lg_laser", 0, 6, [item("laserio:card_item", 2)], "LaserIO Cards", subtitle="Configure what each node moves", deps=["s_laser"], xp=50, desc=[
        "&eWhat:&r cards tell each LaserIO node what to move and in which direction.",
        "&eHow:&r put a card in a node's side slot. Set it to Extract on the source and Insert on the destination.",
        "&eTip:&r right-click with a card in your hand to open its settings."]),
    Q("lg_laser_chem", 2, 6, [item("laserio:card_fluid", 2), item("laserio:card_chemical", 2)], "Fluids and Gases by Laser", subtitle="Move acids without pipes", deps=["lg_laser"], xp=75, desc=[
        "&eWhat:&r fluid cards move liquids; chemical cards move Mekanism gases, like hydrogen and SO₂.",
        "&eHow:&r same as item cards: Extract on the tank, Insert on the machine.",
        "&eTip:&r one node can run several cards on one side. Hydrogen and oxygen out of one separator, two cards."]),
    Q("lg_laser_filter", 4, 6, [item("laserio:filter_basic"), item("laserio:filter_tag"), item("laserio:filter_count")], "LaserIO Filters", subtitle="Basic, tag and count filters", deps=["lg_laser_chem"], xp=75, desc=[
        "&eWhat:&r filters go inside cards. Basic matches a list, Tag matches a tag, Count keeps a set number in stock.",
        "&eHow:&r put the filter in a card's filter slot and set it up.",
        "&eTip:&r a count filter on an insert card keeps exactly 64 sulfur in the oxidizer and no more."]),
    Q("lg_overclock", 6, 7, [item("laserio:overclocker_card", 2), item("laserio:overclocker_node", 2)], "Overclocking", subtitle="Faster lasers", deps=["lg_laser_filter"], xp=100, optional=True, tokens=1, desc=[
        "&eWhat:&r overclockers make LaserIO move more, faster.",
        "&eHow:&r overclocker cards go in a card's upgrade slot; overclocker nodes go in the node.",
        "&eTip:&r most lines don't need it. Add it when a machine starves."]),

    # --- More ComputerCraft (y=-2 / -3.5) ------------------------------------------------------
    Q("lg_printer", 0, -2, [item("computercraft:printer"), item("computercraft:disk_drive")], "Printers and Disks", deps=["lg_computer"], xp=40,
      optional=True, tokens=1, subtitle="Optional: save programs, print lab notes", desc=[
        "&eWhat:&r a Disk Drive lets you save programs on floppy disks and carry them between computers. A Printer prints text onto paper.",
        "&eHow:&r check JEI. Put a disk in the drive and it appears as &edisk/&r in the computer's files.",
        "&eTip:&r print a list of your reactions and their inputs and bind the pages into a book: a real lab notebook."]),
    Q("lg_turtle_adv", 2, -3.5, [item("computercraft:turtle_advanced")], "Advanced Turtle", deps=["lg_turtle"], xp=60,
      optional=True, tokens=1, subtitle="Optional: a golden robot with a colour screen", desc=[
        "&eWhat:&r advanced turtles have colour screens and can be clicked, which makes menus easy.",
        "&eHow:&r an advanced computer with gold instead of iron around it (check JEI). Give it a pickaxe to make a Mining Turtle.",
        "&eTip:&r run &eexcavate 16&r on a mining turtle and it digs a 16x16 hole down to bedrock, bringing everything back."]),

    # --- More Advanced Peripherals (y=-4) ------------------------------------------------------
    Q("lg_ap_geo", 6, -4, [item("advancedperipherals:geo_scanner")], "Geo Scanner", deps=["lg_peripherals"], xp=60,
      optional=True, tokens=1, subtitle="Optional: find ores with a program", desc=[
        "&eWhat:&r the Geo Scanner lists every block around it within a radius, including ores, for your computer to read.",
        "&eChemistry:&r real geologists find ore bodies by measuring gravity, magnetism and how rocks conduct electricity, rather than digging blind.",
        "&eHow:&r check JEI. Put it next to a computer (or in a pocket computer) and call &escan(8)&r.",
        "&eTip:&r write a program that counts ore blocks by type: it's a quick way to check a deposit before setting up a mine."]),
    Q("lg_ap_chat", 8, -4, [item("advancedperipherals:chat_box"), item("advancedperipherals:player_detector")], "Chat Box and Player Detector", deps=["lg_peripherals"], xp=60,
      optional=True, tokens=1, subtitle="Optional: a base that talks back", desc=[
        "&eWhat:&r the Chat Box lets a computer send chat messages; the Player Detector tells it who is nearby.",
        "&eHow:&r check JEI. Place them next to a computer.",
        "&eTip:&r have the base warn everyone in chat when a tank of hydrogen is nearly full or an induction matrix is running low."]),
    Q("lg_ap_inventory", 10, -4, [item("advancedperipherals:inventory_manager"), item("advancedperipherals:memory_card")], "Inventory Manager", deps=["lg_peripherals"], xp=60,
      optional=True, tokens=1, subtitle="Optional: programs that use your inventory", desc=[
        "&eWhat:&r the Inventory Manager lets a computer move items into and out of your own inventory, once you bind it with a Memory Card.",
        "&eHow:&r right-click the Memory Card to bind it to yourself, then put it in the manager (check JEI).",
        "&eTip:&r a button that refills your hotbar with torches and food from storage is a classic first program."]),

    # --- Integrated family (y=2, x>=8) ---------------------------------------------------------
    Q("lg_tunnels", 8, 2, [tick()], "Integrated Tunnels", deps=["lg_id_store"], xp=60,
      subtitle="Move items, fluids and energy with logic", desc=[
        "&eWhat:&r Integrated Tunnels adds importer, exporter and interface parts for Integrated Dynamics cables: items, fluids and energy move along the network, controlled by variables.",
        "&eHow:&r craft an Item Importer and an Item Exporter (check JEI), put them on cables at a chest and a machine, and give the exporter a variable card that says what to move. Click the checkmark when it works.",
        "&eTip:&r a fluid exporter with a boolean variable from a tank reader only fills the reactor when it's below half."]),
    Q("lg_terminals", 10, 2, [item("integratedterminals:terminal_storage_portable")], "Integrated Terminals", deps=["lg_tunnels"], xp=60,
      optional=True, tokens=1, subtitle="Optional: a storage terminal for ID networks", desc=[
        "&eWhat:&r Integrated Terminals adds a Storage Terminal part that shows everything connected to an Integrated Dynamics network, plus a portable version.",
        "&eHow:&r a Storage Terminal part between two crystalized menril chunks makes the portable terminal (check JEI).",
        "&eTip:&r the Crafting Job Terminal shows what Integrated Crafting is working on."]),
    Q("lg_crafting", 12, 2, [tick()], "Integrated Crafting", deps=["lg_tunnels"], xp=60,
      optional=True, tokens=1, subtitle="Optional: autocrafting without AE2", desc=[
        "&eWhat:&r Integrated Crafting adds a Crafting Interface: give it recipe variables and it crafts on demand through the ID network, much like AE2 patterns.",
        "&eHow:&r craft a Crafting Interface (check JEI), write recipes into variable cards with the Logic Programmer, and put them in the interface. Click the checkmark when one craft works.",
        "&eTip:&r it's a cheaper autocrafter than AE2 for small chains, like rubber sheets or redstone batteries."]),

    # --- SFM program (y=4) ---------------------------------------------------------------------
    Q("lg_sfm_program", 0, 4, [tick()], "Your First SFM Program", deps=["lg_sfm"], xp=40,
      optional=True, tokens=1, subtitle="Optional: four lines that move items", desc=[
        "&eWhat:&r Super Factory Manager runs small text programs written on a disk. Labels name the blocks it talks to.",
        "&eHow:&r label a chest &ea&r and a furnace &eb&r with the Label Gun, then write this program on the disk and put it in the manager. Click the checkmark when items start moving.",
        "{@pagebreak}",
        "&eProgram:&r",
        "EVERY 20 TICKS DO",
        "    INPUT FROM a",
        "    OUTPUT TO b",
        "END",
        "&eTip:&r add a side, like &eOUTPUT TO b TOP SIDE&r, to choose which face of the block is used. The manager's built-in examples cover fluids and energy too."]),
], links=[("t3_hull", -2, 0), ("t5_ae2", 6, -2), ("s_laser", -2, 6)])
