"""Quest chapter: logic. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

Mirror of ATM10's "Basic Logistics" chapter (user decision 2026-10-20: quest for quest where we have the mod; the
same items, order, clusters and sizes; the text is ours). ATM10's "Integrated Dynamics" chapter is its own
page now (integrated.py, split out 2026-10-20 with the keys unchanged).

ATM10 Basic Logistics quests skipped: the info checkmark (ATM10's own credits) and Transfer Labels (mod not in the
pack). Our own quests ATM10 doesn't have (ComputerCraft, AE2 autocrafting, Super Factory Manager, Logistics Networks) stay as
side quests; lg_ae_io/lg_cpu/lg_encode/lg_patterns stay required because the AE2 page builds on them.
"""
from questlib import Q, Chapter, item, dim, tick, kill, anyof, anytag, MAIN, SIDE  # noqa: F401

OPT = dict(optional=True, tokens=1)
S_HUB, S_PIPEZ, S_MEK, S_IDT, S_LASER = "The Toolbox", "Pipez", "Mekanism Transmitters", "Integrated Tunnels", "LaserIO"
S_CC, S_AE, S_SFM = "ComputerCraft", "AE2 Autocrafting", "Factory Managers"
MEK = "mekanism:"
TIERS = ("basic", "advanced", "elite", "ultimate")

CHAPTER = Chapter("logic", "Automation and Logic", "computercraft:computer_advanced",
        ["Make the factory run itself."], SIDE, mirror="basic_logistics", quests=[
    # ===== The Toolbox (ATM10 centre) =======================================================
    Q("lg_hub", 0, 0, [anyof(["pipez:wrench", "integrateddynamics:wrench", "laserio:laser_wrench", MEK + "configurator",
                              "powah:wrench", "modern_industrialization:wrench"])], "Moving Things Around", section=S_HUB,
      deps=["gs_iron"], xp=50, size=2.0, shape="gear", mirror="6CD7D99AA102A5C3", subtitle="Any wrench opens the logistics page", desc=[
        "&6You never carried your own buckets. You remember things flowing to where you wanted them.&r",
        "&eWhat:&r this page is every way the pack moves items, fluids, gases and power: Pipez, Mekanism transmitters, Integrated Dynamics, LaserIO, and a few extras.",
        "&eHow:&r any of the logistics wrenches counts: Pipez, Integrated Dynamics, LaserIO, the Mekanism Configurator, Powah or Modern Industrialization.",
        "&eTip:&r start with Pipez. It is cheap, it works early, and you can swap it for something cleverer later."]),

    # ===== Pipez ============================================================================
    Q("lg_pipez_tools", 0, 0, [item("pipez:wrench")], "Pipez", section=S_PIPEZ, deps=["gs_iron"], xp=40, size=1.5,
      mirror="2329AA0AFBEF1E13", subtitle="Simple pipes, one for each job", desc=[
        "&eWhat:&r Pipez has a pipe for each thing that moves, and the Pipe Wrench to cut and rejoin pipe sides.",
        "&eHow:&r check JEI for the wrench. Sneak-click where a pipe meets a machine to make that end extract.",
        "&eTip:&r Pipez only pulls from ends you set to extract, so connecting a pipe to a machine never drains it by accident."]),
    Q("lg_pipez_item", 0, 0, [item("pipez:item_pipe")], "Item Pipes", section=S_PIPEZ, deps=["lg_pipez_tools"], xp=25,
      mirror="36836AD948F96B9F", subtitle="Ore in one end, ingots out the other", desc=[
        "&eWhat:&r the item pipe moves stacks between inventories.",
        "&eHow:&r iron and redstone (check JEI). Set the machine end to extract with the wrench or by sneak-clicking.",
        "&eTip:&r one pipe line can feed a whole row of furnaces; items go to the nearest free one first."]),
    Q("lg_pipez_types", 0, 0, [item("pipez:fluid_pipe")], "Fluid Pipes", section=S_PIPEZ, deps=["lg_pipez_tools"], xp=25,
      mirror="33433A443B65D252", subtitle="Water, acids and fuels", desc=[
        "&eWhat:&r the fluid pipe moves liquids: water to boilers, acid to reactors, fuel to generators.",
        "&eChemistry:&r a pipe of sulfuric acid in real life is lined with PTFE or glass, because H₂SO₄ eats most metals. Pipez is kinder.",
        "&eHow:&r iron and redstone with a bucket (check JEI).",
        "&eTip:&r keep one fluid per pipe line, or the first fluid in blocks the rest."]),
    Q("lg_pipez_energy", 0, 0, [item("pipez:energy_pipe")], "Energy Pipes", section=S_PIPEZ, deps=["lg_pipez_tools"], xp=25,
      mirror="53EC96FA0E7C4ED4", subtitle="FE from generator to machine", desc=[
        "&eWhat:&r the energy pipe carries FE (Forge Energy), the power most mods share.",
        "&eHow:&r iron and redstone with a redstone block (check JEI). Extract from the generator side.",
        "&eTip:&r MI machines run on EU, not FE. Use MI cables for those."]),
    Q("lg_pipez_universal", 0, 0, [item("pipez:universal_pipe")], "Universal Pipe", section=S_PIPEZ,
      deps=["lg_pipez_item", "lg_pipez_types", "lg_pipez_energy"], xp=40, mirror="4FBAB3A0FBF8CE2F",
      subtitle="One pipe, all the jobs", desc=[
        "&eWhat:&r the Universal Pipe carries several kinds of thing at once in one line (its tooltip lists which).",
        "&eHow:&r item, fluid and energy pipes with iron and a redstone block (check JEI).",
        "&eTip:&r set each side's mode per type in its GUI, so one pipe can feed a machine items and power together."]),
    Q("lg_pipez_gas", 0, 0, [item("pipez:gas_pipe")], "Gas Pipes", section=S_PIPEZ, deps=["lg_pipez_tools"], xp=25,
      mirror="2F4458E9921DEB86", subtitle="Mekanism chemicals by pipe", desc=[
        "&eWhat:&r the gas pipe moves Mekanism chemicals: hydrogen, oxygen, chlorine, SO₂ and the rest.",
        "&eChemistry:&r keep H₂ and Cl₂ in separate lines: mixed and lit, they react explosively (H₂ + Cl₂ → 2HCl).",
        "&eHow:&r iron and redstone with infused alloy (check JEI)."]),
    Q("lg_pipez_dest", 0, 0, [item("pipez:filter_destination_tool")], "Filter Destination Tool", section=S_PIPEZ,
      deps=["lg_pipez_tools"], xp=20, mirror="2A976D41F79C34B1", subtitle="Aim a filter at one inventory", desc=[
        "&eWhat:&r this tool picks the one inventory a filter sends its items to.",
        "&eHow:&r right-click the target block with the tool, then click the filter entry in the pipe's GUI (check JEI for the recipe).",
        "&eTip:&r useful when two furnaces sit on one line but only one should get the coal."]),
    Q("lg_pipez_upgrade", 0, 0, [anyof([f"pipez:{t}_upgrade" for t in ("basic", "improved", "advanced", "ultimate")])], "Pipe Upgrades",
      section=S_PIPEZ, deps=["lg_pipez_tools"], xp=40, mirror="6A962535CD68713E", subtitle="Faster pipes with filters and modes", desc=[
        "&eWhat:&r upgrades raise a pipe end's speed and unlock filters, redstone modes and round-robin. Any tier counts.",
        "&eHow:&r each tier is the one before plus better materials (check JEI). Put it in the extracting end.",
        "&eTip:&r round-robin spreads ore evenly across a row of machines."]),

    # ===== Mekanism Transmitters =============================================================
    Q("lg_mek", 0, 0, [tick()], "Mekanism Transport", section=S_MEK, deps=['t3_infuser', 't3_mekcircuit'], optional=True, tokens=0, xp=0, mirror="34CFE1439262AA72", icon="mekanism:configurator", subtitle="Moved: see Configurator", desc=["&eMoved:&r this step is now \"Configurator\" on the Mekanism page. Click to dismiss."]),
    Q("lg_mek_pipe", 0, 0, [tick()], "Mechanical Pipes", section=S_MEK, deps=['lg_mek'], optional=True, tokens=0, xp=0, mirror="1834B5C1F8435D7A", icon="mekanism:basic_mechanical_pipe", subtitle="Moved: see Mechanical Pipes", desc=["&eMoved:&r this step is now \"Mechanical Pipes\" on the Mekanism page. Click to dismiss."]),
    Q("lg_mek_cable", 0, 0, [tick()], "Universal Cables", section=S_MEK, deps=['lg_mek'], optional=True, tokens=0, xp=0, mirror="493D04D954E4FBA0", icon="mekanism:basic_universal_cable", subtitle="Moved: see Universal Cable", desc=["&eMoved:&r this step is now \"Universal Cable\" on the Mekanism page. Click to dismiss."]),
    Q("lg_mek_transporter", 0, 0, [tick()], "Logistical Transporters", section=S_MEK, deps=['lg_mek'], optional=True, tokens=0, xp=0, mirror="30DE4F5BC3EDB555", icon="mekanism:basic_logistical_transporter", subtitle="Moved: see Logistical Transporters", desc=["&eMoved:&r this step is now \"Logistical Transporters\" on the Mekanism page. Click to dismiss."]),
    Q("lg_mek_conductor", 0, 0, [tick()], "Thermodynamic Conductors", section=S_MEK, deps=['lg_mek'], optional=True, tokens=0, xp=0, mirror="316B513FE568EF57", icon="mekanism:basic_thermodynamic_conductor", subtitle="Moved: see Thermodynamic Conductors", desc=["&eMoved:&r this step is now \"Thermodynamic Conductors\" on the Mekanism page. Click to dismiss."]),
    Q("lg_mek_tube", 0, 0, [tick()], "Pressurized Tubes", section=S_MEK, deps=['lg_mek'], optional=True, tokens=0, xp=0, mirror="4BC2D7FCDD792DBA", icon="mekanism:basic_pressurized_tube", subtitle="Moved: see Pressurized Tubes", desc=["&eMoved:&r this step is now \"Pressurized Tubes\" on the Mekanism page. Click to dismiss."]),

    # ===== Integrated Tunnels (ATM10 Basic Logistics) ========================================
    Q("lg_id_book", 0, 0, [item("integrateddynamics:wrench")], "Integrated Dynamics", section=S_IDT, deps=["lg_menril"], xp=40,
      size=1.5, mirror="6E05B62A40D5A891", subtitle="Logic networks built from resin", desc=[
        "&eWhat:&r Integrated Dynamics reads values from the world (tank levels, item counts), applies logic, and acts on them. Integrated Tunnels uses the same cables to move things. The Menril wrench rotates and removes ID blocks and parts.",
        "&eHow:&r Menril chunks and redstone (check JEI). The mod's own book, On the Dynamics of Integration, has worked examples.",
        "&eTip:&r the resin line that makes Menril chunks is on the Integrated Dynamics page."]),
    Q("lg_id_cable", 0, 0, [item("integrateddynamics:cable", 10)], "Logic Cables", section=S_IDT, deps=["lg_id_book"], xp=30,
      mirror="6112956E19017D2D", subtitle="The wiring for every part", desc=[
        "&eWhat:&r logic cables join readers, writers, importers and exporters into one network.",
        "&eHow:&r crystalized Menril chunks and redstone (check JEI). Parts go on the side of a cable.",
        "&eTip:&r use the wrench on a cable side to cut it, so two networks next to each other stay apart."]),
    Q("lg_id_variable", 0, 0, [item("integrateddynamics:variable")], "Variable Cards", section=S_IDT, deps=["lg_id_book"], xp=30,
      mirror="03C40D6A5D722543", subtitle="A card that holds a value or a rule", desc=[
        "&eWhat:&r a variable card stores one thing: a number, a yes/no, an item, or a rule built in the Logic Programmer.",
        "&eHow:&r Menril chunks around redstone (check JEI).",
        "&eTip:&r make a stack. Every reader value and every exporter rule wants its own card."]),
    Q("lg_idt_item", 0, 0, [item("integratedtunnels:part_importer_item"), item("integratedtunnels:part_interface_item")], "Items by Logic",
      section=S_IDT, deps=["lg_id_cable", "lg_id_variable"], xp=40, mirror="6F152402756DA35E", subtitle="Importer in, interface out", desc=[
        "&eWhat:&r an Item Importer pulls items into the network; an Item Interface lets the network's items be reached from a chest or machine.",
        "&eHow:&r put both on cables (check JEI for the parts). The importer takes a variable card that says what to move.",
        "&eTip:&r with no card, an importer moves everything. Add a card when you want it picky."]),
    Q("lg_idt_fluid", 0, 0, [item("integratedtunnels:part_importer_fluid"), item("integratedtunnels:part_interface_fluid")], "Fluids by Logic",
      section=S_IDT, deps=["lg_id_cable", "lg_id_variable"], xp=40, mirror="034F2CDF0830254B", subtitle="Tanks joined by cable", desc=[
        "&eWhat:&r the fluid versions of the importer and interface.",
        "&eChemistry:&r an exporter that only runs while a tank reader says 'below 50%' is a simple feedback loop, the same idea as a float valve in a cistern.",
        "&eHow:&r check JEI for both parts; place them on cables against tanks and machines."]),
    Q("lg_idt_energy", 0, 0, [item("integratedtunnels:part_importer_energy"), item("integratedtunnels:part_interface_energy")], "Energy by Logic",
      section=S_IDT, deps=["lg_id_cable", "lg_id_variable"], xp=40, mirror="76CECFB244F39F18", subtitle="Power along the same cables", desc=[
        "&eWhat:&r energy importers and interfaces move FE through logic cables.",
        "&eHow:&r check JEI. Pull from a generator or battery, push out at a machine.",
        "&eTip:&r a redstone variable can switch power to a whole wing of the base on and off."]),

    # ===== LaserIO ===========================================================================
    Q("lg_laser_kit", 0, 0, [item("laserio:logic_chip")], "LaserIO", section=S_LASER, deps=["t3_hull"], xp=50, size=1.5,
      mirror="5F1218CF8EFC607B", subtitle="Move things through the air", desc=[
        "&eWhat:&r LaserIO nodes sit on machines and pass items, fluids, chemicals, power and redstone along lasers. Logic chips go into every node and card.",
        "&eHow:&r raw logic chips are a quartz block, clay, gold nuggets and redstone (4 at a time); smelt them.",
        "&eTip:&r one node can serve all six sides of the block it touches."]),
    Q("lg_laser_wrench", 0, 0, [item("laserio:laser_wrench")], "Laser Wrench", section=S_LASER, deps=["lg_laser_kit"], xp=30, size=1.5,
      mirror="7BC8F50A89A3BE1A", subtitle="Click one node, then the other", desc=[
        "&eWhat:&r the Laser Wrench links nodes together.",
        "&eHow:&r iron and a logic chip (check JEI). Click the first node, then the second.",
        "&eTip:&r sneak-click a node with the wrench to unlink it."]),
    Q("lg_laser_node", 0, 0, [item("laserio:laser_node")], "Laser Nodes", section=S_LASER, deps=["lg_laser_kit"], xp=30,
      mirror="5C0F6B1C93A52113", subtitle="One per machine", desc=[
        "&eWhat:&r a node sits against a machine and holds the cards for each of its sides.",
        "&eHow:&r glass, iron, redstone and a logic chip (check JEI).",
        "&eTip:&r right-click a node to open its six side slots."]),
    Q("lg_laser_filter", 0, 0, [item("laserio:filter_basic")], "Basic Filter", section=S_LASER, deps=["lg_laser_kit"], xp=30,
      mirror="47A2BEFB11F4D581", subtitle="Only these items, please", desc=[
        "&eWhat:&r filters go inside cards. The basic filter matches the items you list.",
        "&eHow:&r put the filter in a card's filter slot and set it up.",
        "&eTip:&r flip it to deny mode to send everything except the listed items."]),
    Q("lg_laser", 0, 0, [item("laserio:card_item")], "Item Cards", section=S_LASER, deps=["lg_laser_kit"], xp=30,
      mirror="4C41FD926F31180B", subtitle="Configure what each node moves", desc=[
        "&eWhat:&r cards tell each node what to move and in which direction.",
        "&eHow:&r put a card in a node's side slot. Set it to Extract on the source and Insert on the destination.",
        "&eTip:&r right-click with a card in your hand to open its settings."]),
    Q("lg_laser_chem", 0, 0, [item("laserio:card_fluid")], "Fluid Cards", section=S_LASER, deps=["lg_laser_kit"], xp=30,
      mirror="1C70D739CE464E25", subtitle="Move acids without pipes", desc=[
        "&eWhat:&r fluid cards move liquids between nodes.",
        "&eHow:&r same as item cards: Extract on the tank, Insert on the machine.",
        "&eTip:&r one node can run several cards on one side."]),
    Q("lg_laser_energy", 0, 0, [item("laserio:card_energy")], "Energy Cards", section=S_LASER, deps=["lg_laser_kit"], xp=30,
      mirror="52F85CED20C8B1E9", subtitle="Power by laser", desc=[
        "&eWhat:&r energy cards move FE between nodes.",
        "&eHow:&r a logic chip with quartz, gold nuggets and a redstone block (check JEI).",
        "&eTip:&r a node on your battery and one on each machine replaces a whole cable run."]),
    Q("lg_laser_redstone", 0, 0, [item("laserio:card_redstone")], "Redstone Cards", section=S_LASER, deps=["lg_laser_kit"], xp=30,
      mirror="47768B1FFD57D56E", subtitle="Signals along the laser network", desc=[
        "&eWhat:&r redstone cards read a signal at one node and send it out at another.",
        "&eHow:&r a logic chip with redstone (check JEI). Set channels to pair senders and receivers.",
        "&eTip:&r switch a separator on only while the sulfur chest has stock."]),
    Q("lg_laser_chemcard", 0, 0, [item("laserio:card_chemical")], "Chemical Cards", section=S_LASER, deps=["lg_laser_kit"], xp=30,
      mirror="6718043D0F2D1830", subtitle="Mekanism gases by laser", desc=[
        "&eWhat:&r chemical cards move Mekanism chemicals: hydrogen, oxygen, SO₂, slurries.",
        "&eChemistry:&r a separator splits water 2H₂O → 2H₂ + O₂. Two chemical cards on one node carry both gases off to different machines.",
        "&eHow:&r check JEI for the recipe; set Extract and Insert like any card."]),
    Q("lg_laser_org", 0, 0, [item("laserio:card_holder")], "Card Holder", section=S_LASER, deps=["lg_laser_kit"], xp=20, **OPT,
      mirror="617695A9CA45D88F", subtitle="Optional: spare cards on your belt", desc=[
        "&eWhat:&r the Card Holder carries spare cards and filters and fills nodes from your inventory.",
        "&eHow:&r a logic chip in iron with a chest (check JEI).",
        "&eTip:&r keep one of each card type in it while you wire a new line."]),
    Q("lg_laser_cloner", 0, 0, [item("laserio:card_cloner")], "Card Cloner", section=S_LASER, deps=["lg_laser_kit"], xp=20, **OPT,
      mirror="308935C85364B04D", subtitle="Optional: copy one card's settings", desc=[
        "&eWhat:&r the Card Cloner copies one card's settings onto others.",
        "&eHow:&r a logic chip in iron with paper (check JEI). Sneak-click a card to copy, click another to paste.",
        "&eTip:&r clone one tuned acid card to every reactor in the line."]),
    Q("lg_laser_connector", 0, 0, [item("laserio:laser_connector")], "Laser Connector", section=S_LASER, deps=["lg_laser_node"], xp=20,
      **OPT, mirror="7EE27C3908008E20", subtitle="Optional: relay lasers round corners", desc=[
        "&eWhat:&r a connector relays lasers between nodes without holding cards.",
        "&eHow:&r glass, redstone, iron and a logic chip (check JEI).",
        "&eTip:&r nodes link up to a set range; connectors let you go round corners and through walls."]),
    Q("lg_laser_count", 0, 0, [item("laserio:filter_count")], "Count Filter", section=S_LASER, deps=["lg_laser_filter"], xp=30,
      mirror="06767BA0AFE8C1EE", subtitle="Keep exactly this many in stock", desc=[
        "&eWhat:&r the count filter tops a machine up to a set number and stops.",
        "&eHow:&r a basic filter with a comparator (check JEI).",
        "&eTip:&r 64 sulfur in the oxidizer and no more: the rest stays in storage for other lines."]),
    Q("lg_laser_tag", 0, 0, [item("laserio:filter_tag")], "Tag Filter", section=S_LASER, deps=["lg_laser_filter"], xp=30,
      mirror="3065EA195D0A36BA", subtitle="Every dust, every ingot", desc=[
        "&eWhat:&r the tag filter matches whole tags, like c:dusts or c:ores.",
        "&eHow:&r a basic filter with a name tag or paper (check JEI). Type the tag in its screen.",
        "&eTip:&r one tag filter on c:raw_materials sends every raw ore to your processing line."]),
    Q("lg_laser_mod", 0, 0, [item("laserio:filter_mod")], "Mod Filter", section=S_LASER, deps=["lg_laser_filter"], xp=30,
      mirror="2A6900E87DE8BAE0", subtitle="Everything from one mod", desc=[
        "&eWhat:&r the mod filter matches every item from the mod of the item you show it.",
        "&eHow:&r a basic filter plus a book (check JEI).",
        "&eTip:&r route all ChemLib items to the lab store with one card."]),
    Q("lg_overclock", 0, 0, [item("laserio:overclocker_card")], "Card Overclocker", section=S_LASER, deps=["lg_laser_kit"], xp=40, **OPT,
      mirror="046C417B2ADF3AA7", subtitle="Optional: bigger batches per card", desc=[
        "&eWhat:&r card overclockers raise how much one card moves per trip.",
        "&eHow:&r check JEI; it goes in a card's upgrade slot.",
        "&eTip:&r most lines don't need it. Add it when a machine starves."]),
    Q("lg_overclock_node", 0, 0, [item("laserio:overclocker_node")], "Node Overclocker", section=S_LASER, deps=["lg_laser_kit"], xp=40,
      **OPT, mirror="0BB562FB44B0AAA7", subtitle="Optional: faster nodes", desc=[
        "&eWhat:&r node overclockers make a node act more often.",
        "&eHow:&r check JEI; it goes in the node's upgrade slot.",
        "&eTip:&r pair a fast node with an overclocked card for the busiest machine in a line."]),

    # ===== ComputerCraft (ours; ATM10 has no page for it here) ===============================
    Q("lg_computer", 0, 0, [item("computercraft:computer_normal")], "A Computer", section=S_CC, subtitle="Optional: Lua, in a box",
      deps=["t3_hull"], xp=50, **OPT, desc=[
        "&6You never did your own chores. You remember having things that did them for you.&r",
        "&eWhat:&r CC: Tweaked computers run Lua programs: monitor tanks, balance chemical lines, build a base dashboard.",
        "&eHow:&r place it and right-click. Type &ehelp&r, or &eedit startup&r to write a program that runs on boot.",
        "&eTip:&r Mekanism machines can be read by computers directly. Put a computer next to one and try &eperipheral.getNames()&r."]),
    Q("lg_monitor", 0, 0, [item("computercraft:monitor_advanced", 4)], "Monitors", section=S_CC, subtitle="Optional: a screen for your numbers",
      deps=["lg_computer"], xp=50, **OPT, desc=[
        "&eWhat:&r monitors show program output on a wall. Placed together, they join into one big screen.",
        "&eHow:&r put monitors next to the computer and run &emonitor <side> <program>&r to send output to them.",
        "&eTip:&r advanced monitors show colour and accept clicks, so you can make touch buttons."]),
    Q("lg_modem", 0, 0, [item("computercraft:wired_modem", 2), item("computercraft:cable", 16)], "Wired Networks", section=S_CC,
      subtitle="Optional: reach machines across the room", deps=["lg_monitor"], xp=60, **OPT, desc=[
        "&eWhat:&r wired modems and networking cable connect a computer to machines that aren't touching it.",
        "&eHow:&r put a modem on the machine, run cable back to a modem on the computer, and right-click the machine's modem to attach it.",
        "&eTip:&r each attached peripheral gets a name. List them with &eperipheral.getNames()&r."]),
    Q("lg_wireless", 0, 0, [item("computercraft:wireless_modem_advanced"), item("computercraft:pocket_computer_advanced")], "Ender Modem",
      section=S_CC, subtitle="Optional: talk across dimensions", deps=["lg_modem"], xp=100, **OPT, desc=[
        "&eWhat:&r the Ender Modem sends messages with no range limit, even between dimensions. A pocket computer carries a terminal with you.",
        "&eHow:&r use &erednet&r on both ends: one computer broadcasts tank levels, your pocket computer reads them.",
        "&eTip:&r a remote alarm for your reactor is a very good idea."]),
    Q("lg_turtle", 0, 0, [item("computercraft:turtle_normal")], "Turtles", section=S_CC, subtitle="Optional: robots you program",
      deps=["lg_computer"], xp=75, **OPT, desc=[
        "&eWhat:&r turtles are programmable robots that mine, build and farm.",
        "&eHow:&r craft one with a tool (a pickaxe makes a mining turtle) and fuel it with coal.",
        "&eTip:&r try the built-in &eexcavate&r and &etunnel&r programs first."]),
    Q("lg_peripherals", 0, 0, [item("advancedperipherals:energy_detector"), item("advancedperipherals:me_bridge")], "Advanced Peripherals",
      section=S_CC, subtitle="Optional: read power flow and your ME network", deps=["lg_modem", "t5_ae2"], xp=150, **OPT, desc=[
        "&eWhat:&r extra peripherals: the Energy Detector measures power flow; the ME Bridge reads (and requests crafts from) your whole AE2 network.",
        "&eHow:&r place them on your wired network like any other peripheral.",
        "&eTip:&r an ME Bridge program can keep your stock of every intermediate topped up."]),
    Q("lg_dashboard", 0, 0, [item("advancedperipherals:fluid_detector"), item("computercraft:monitor_advanced", 8)], "Base Dashboard",
      section=S_CC, subtitle="Optional: every tank on one screen", deps=["lg_peripherals"], xp=150, **OPT, desc=[
        "&eWhat:&r a wall screen that shows your chemical stocks, power and flow rates at a glance.",
        "&eHow:&r the Fluid Detector measures flow through a pipe. Combine it with tank readings and the energy detector in one program.",
        "&eTip:&r colour lines red when a tank drops below 20%. You'll spot problems from across the room."]),
    Q("lg_printer", 0, 0, [item("computercraft:printer"), item("computercraft:disk_drive")], "Printers and Disks", section=S_CC,
      deps=["lg_computer"], xp=40, **OPT, subtitle="Optional: save programs, print lab notes", desc=[
        "&eWhat:&r a Disk Drive lets you save programs on floppy disks and carry them between computers. A Printer prints text onto paper.",
        "&eHow:&r check JEI. Put a disk in the drive and it appears as &edisk/&r in the computer's files.",
        "&eTip:&r print a list of your reactions and their inputs and bind the pages into a book: a real lab notebook."]),
    Q("lg_turtle_adv", 0, 0, [item("computercraft:turtle_advanced")], "Advanced Turtle", section=S_CC, deps=["lg_turtle"], xp=60, **OPT,
      subtitle="Optional: a golden robot with a colour screen", desc=[
        "&eWhat:&r advanced turtles have colour screens and can be clicked, which makes menus easy.",
        "&eHow:&r an advanced computer with gold instead of iron around it (check JEI). Give it a pickaxe to make a Mining Turtle.",
        "&eTip:&r run &eexcavate 16&r on a mining turtle and it digs a 16x16 hole down to bedrock, bringing everything back."]),
    Q("lg_ap_geo", 0, 0, [item("advancedperipherals:geo_scanner")], "Geo Scanner", section=S_CC, deps=["lg_peripherals"], xp=60, **OPT,
      subtitle="Optional: find ores with a program", desc=[
        "&eWhat:&r the Geo Scanner lists every block around it within a radius, including ores, for your computer to read.",
        "&eChemistry:&r real geologists find ore bodies by measuring gravity, magnetism and how rocks conduct electricity, rather than digging blind.",
        "&eHow:&r check JEI. Put it next to a computer (or in a pocket computer) and call &escan(8)&r.",
        "&eTip:&r write a program that counts ore blocks by type: it's a quick way to check a deposit before setting up a mine."]),
    Q("lg_ap_chat", 0, 0, [item("advancedperipherals:chat_box"), item("advancedperipherals:player_detector")], "Chat Box and Player Detector",
      section=S_CC, deps=["lg_peripherals"], xp=60, **OPT, subtitle="Optional: a base that talks back", desc=[
        "&eWhat:&r the Chat Box lets a computer send chat messages; the Player Detector tells it who is nearby.",
        "&eHow:&r check JEI. Place them next to a computer.",
        "&eTip:&r have the base warn everyone in chat when a tank of hydrogen is nearly full or an induction matrix is running low."]),
    Q("lg_ap_inventory", 0, 0, [item("advancedperipherals:inventory_manager"), item("advancedperipherals:memory_card")], "Inventory Manager",
      section=S_CC, deps=["lg_peripherals"], xp=60, **OPT, subtitle="Optional: programs that use your inventory", desc=[
        "&eWhat:&r the Inventory Manager lets a computer move items into and out of your own inventory, once you bind it with a Memory Card.",
        "&eHow:&r right-click the Memory Card to bind it to yourself, then put it in the manager (check JEI).",
        "&eTip:&r a button that refills your hotbar with torches and food from storage is a classic first program."]),

    # ===== AE2 Autocrafting (ours; the AE2 page builds on lg_cpu and lg_patterns) ============
    Q("lg_ae_io", 0, 0, [item("ae2:import_bus"), item("ae2:export_bus"), item("ae2:storage_bus")], "Buses", section=S_AE,
      subtitle="AE2 pulls, pushes and reads", deps=["t5_ae2"], xp=100, desc=[
        "&eWhat:&r an import bus pulls items out of a machine, an export bus pushes them in, and a storage bus lets ME see inside a chest or tank.",
        "&eHow:&r place them on cable facing the machine. Set filters in each bus's GUI.",
        "&eTip:&r Applied Mekanistics is in the pack, so buses and storage also handle Mekanism gases like hydrogen and SO₂."]),
    Q("lg_cpu", 0, 0, [item("ae2:crafting_unit", 2), item("ae2:1k_crafting_storage")], "Crafting CPU", section=S_AE,
      subtitle="The part of AE2 that plans", deps=["lg_ae_io"], xp=150, desc=[
        "&eWhat:&r a crafting CPU is a multiblock that works out and tracks autocrafting jobs.",
        "&eHow:&r build a solid box of crafting units with at least one crafting storage, and connect it to your network.",
        "&eTip:&r more storage lets it plan bigger jobs; co-processing units run more steps at once."]),
    Q("lg_encode", 0, 0, [item("ae2:pattern_encoding_terminal"), item("ae2:blank_pattern", 8)], "Encoding Patterns", section=S_AE,
      subtitle="Teach AE2 a recipe", deps=["lg_cpu"], xp=100, desc=[
        "&eWhat:&r a pattern is a recipe card: these inputs make that output.",
        "&eHow:&r in the Pattern Encoding Terminal, switch to Processing mode for machine recipes and fill in the inputs and outputs.",
        "&eTip:&r processing patterns work for any machine: MI, Mekanism or the Combiner."]),
    Q("lg_patterns", 0, 0, [item("ae2:pattern_provider"), item("ae2:molecular_assembler")], "Autocraft a Chemical Line", section=S_AE,
      subtitle="Pattern providers drive your machines", deps=["lg_encode"], xp=200, desc=[
        "&eWhat:&r pattern providers push ingredients into machines; molecular assemblers do crafting-table recipes.",
        "&eHow:&r put a provider against an MI or Mekanism machine, load a processing pattern, and send the output back into the network.",
        "&eTip:&r chain patterns (sulfur → SO₂ → SO₃ → H₂SO₄) and one request runs the whole line."]),
    Q("lg_level", 0, 0, [tick()], "Level Emitters", section=S_AE, deps=['lg_ae_io'], optional=True, tokens=0, xp=0, icon="ae2:level_emitter", subtitle="Moved: see Level Emitter", desc=["&eMoved:&r this step is now \"Level Emitter\" on the Applied Energistics page. Click to dismiss."]),
    Q("lg_acid_line", 0, 0, [item("modern_industrialization:sulfuric_acid_bucket", 16), tick()], "Fully Automated Sulfuric Acid", section=S_AE,
      subtitle="Optional: sulfur in, acid out, no hands", deps=["lg_patterns", "ae_level_emitter"], xp=1000, size=1.5, optional=True, tokens=2, desc=[
        "&6The factory hums without you. You remember this kind of quiet.&r",
        "&eWhat:&r a line that makes sulfuric acid on its own and stops when the tanks are full.",
        "&eChemistry:&r 2SO₂ + O₂ → 2SO₃ (industry uses a vanadium oxide catalyst), then SO₃ + H₂O → H₂SO₄.",
        "&eHow:&r Separator (O₂) → Oxidizer (S → SO₂) → Infuser (SO₃) → Rotary Condensentrator (water vapour) → Infuser (H₂SO₄). Feed sulfur with a bus or LaserIO and gate it with a level emitter.",
        "&eTip:&r when it runs a full day with no help, fill 16 buckets and click the checkmark."]),

    # ===== Factory Managers (ours) ===========================================================
    Q("lg_sfm", 0, 0, [item("sfm:manager"), item("sfm:cable", 8), item("sfm:disk")], "Super Factory Manager", section=S_SFM,
      subtitle="Optional: one block scripts the whole factory", deps=["t3_hull"], xp=100, **OPT, desc=[
        "&eWhat:&r one Manager block runs a short program that moves items, fluids and energy between everything on its cables.",
        "&eHow:&r put the disk in the Manager and write a program, e.g. &eEVERY 20 TICKS DO INPUT FROM a OUTPUT TO b END&r.",
        "&eTip:&r the in-game editor has examples. Start with one input and one output."]),
    Q("lg_sfm_label", 0, 0, [item("sfm:labelgun"), item("sfm:network_tool")], "Labels", section=S_SFM, subtitle="Optional: name every machine",
      deps=["lg_sfm"], xp=60, **OPT, desc=[
        "&eWhat:&r the Label Gun tags inventories with names (like &ea&r and &eb&r above) for your programs.",
        "&eHow:&r set a label in the gun, then right-click each machine. The Network Tool shows what's connected.",
        "&eTip:&r label by job ('sulfur_in', 'acid_out'), not by machine type."]),
    Q("lg_sfm_program", 0, 0, [tick()], "Your First SFM Program", section=S_SFM, deps=["lg_sfm"], xp=40, **OPT,
      subtitle="Optional: four lines that move items", desc=[
        "&eWhat:&r Super Factory Manager runs small text programs written on a disk. Labels name the blocks it talks to.",
        "&eHow:&r label a chest &ea&r and a furnace &eb&r with the Label Gun, then write this program on the disk and put it in the manager. Click the checkmark when items start moving.",
        "{@pagebreak}",
        "&eProgram:&r",
        "EVERY 20 TICKS DO",
        "    INPUT FROM a",
        "    OUTPUT TO b",
        "END",
        "&eTip:&r add a side, like &eOUTPUT TO b TOP SIDE&r, to choose which face of the block is used. The manager's built-in examples cover fluids and energy too."]),
    Q("lg_logistics", 0, 0, [item("logisticsnetworks:logistics_node", 2)], "Logistics Network", section=S_SFM,
      subtitle="Optional: nodes that route by rules", deps=["lg_sfm_label"], xp=75, **OPT, desc=[
        "&eWhat:&r Logistics Network nodes sit on machines and chests and move items, fluids and energy between every node in the same named network, with no cables.",
        "&eHow:&r obsidian, a redstone block, hoppers, an eye of ender and a redstone torch for a node (check JEI). Open a node to create or join a network, then set what it imports and exports.",
        "&eTip:&r the Wrench has a copy-paste mode: set up one node, then paste its settings onto the rest."]),
    Q("lg_logistics_filter", 0, 0, [item("logisticsnetworks:tag_filter"), item("logisticsnetworks:amount_filter")], "Logistics Filters",
      section=S_SFM, subtitle="Optional: move only what you mean to", deps=["lg_logistics"], xp=75, **OPT, desc=[
        "&eWhat:&r filters narrow what a node moves: by tag, by amount and more.",
        "&eHow:&r put a filter in a node's slot and set it up in its GUI (check JEI for all the filter types).",
        "&eTip:&r a tag filter for 'c:dusts' sends every dust to one chest."]),
    # Moved from storage.py (keys unchanged) when its Logistics Networks row was removed (2026-10-18).
    Q("sto_ln_upgrade", 0, 0, [item("logisticsnetworks:iron_upgrade"), item("logisticsnetworks:gold_upgrade")], "Node Upgrades", section=S_SFM,
      subtitle="Optional: bigger batches, shorter delays", deps=["lg_logistics"], xp=60, **OPT, desc=[
        "&eWhat:&r upgrades raise how much a node moves per batch and how often. Iron, gold, diamond and netherite tiers each do more.",
        "&eHow:&r the tier's metal, hoppers, chests and smooth stone (check JEI). Put them in the node's upgrade slots.",
        "&eTip:&r the upgrade's tooltip lists its exact items, fluid and energy per batch."]),
    Q("sto_ln_chem", 0, 0, [item("logisticsnetworks:mekanism_chemical_upgrade")], "Moving Chemicals", section=S_SFM,
      subtitle="Optional: nodes that carry Mekanism gases", deps=["sto_ln_upgrade", "t3_infuser"], xp=75, **OPT, desc=[
        "&eWhat:&r the Mekanism Chemical Upgrade lets nodes move Mekanism chemicals: H₂, O₂, Cl₂, SO₂ and the rest.",
        "&eChemistry:&r the contact process needs SO₂ and O₂ in the same place: 2SO₂ + O₂ → 2SO₃. Nodes can bring both to one Chemical Infuser.",
        "&eHow:&r basic chemical tanks, infused alloy, chests and an Iron Upgrade (check JEI).",
        "&eTip:&r one network for gases and another for items keeps the settings easy to read."]),
    Q("sto_ln_computer", 0, 0, [item("logisticsnetworks:computer")], "Network Manager", section=S_SFM,
      subtitle="Optional: see every node and its flow", deps=["lg_logistics"], xp=50, **OPT, desc=[
        "&eWhat:&r the Computer opens a Network Manager that lists your networks, their nodes and how much each channel moves.",
        "&eHow:&r iron, glass and a comparator (check JEI).",
        "&eTip:&r when a line stops, look here first: a channel with no flow shows where the jam is."]),
], links=[("gs_iron", 0, 0), ("t3_hull", 0, 0), ("t3_infuser", 0, 0), ("t5_ae2", 0, 0), ("lg_menril", 0, 0)])
