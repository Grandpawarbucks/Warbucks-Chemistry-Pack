"""Quest chapter: ae2 (Applied Energistics 2 and its small addons). See tools/quests/STYLE.md.

Mirror of ATM10's "Applied Energistics 2" chapter (user decision 2026-10-20: quest for quest where we have the mod;
the same items, counts, order, sections and sizes). Every quest with mirror="<id>" sits where that ATM10 quest
sits; all text is ours. All 74 ATM10 quests are mirrored. Quests ATM10 doesn't have (presses and silicon, housings,
cores, MEGA's own parts, Applied Mekanistics, Applied Flux, requesters, packaged crafting) stay as optional side
quests off the nearest quest.
ExtendedAE and AdvancedAE quests live on their own page, tools/quests/eae.py (keys unchanged).
Gate: AE2 opens in t5 (the Inscriber needs an MI Turbo hull, the Controller a digital circuit); the page's
first quest hangs off t5_hv. The AdvancedAE Flight Card is under review in this pack: no quest asks for it.
"""
from questlib import Q, Chapter, item, dim, tick, anytag, anyof, MAIN, SIDE  # noqa: F401

S_START, S_CRYS, S_POWER, S_NET = "First Steps", "Crystals and Processors", "Power", "The Network"
S_CELLS, S_MEGA, S_IO, S_AUTO = "Storage Cells", "MEGA Cells", "Interfaces and Buses", "Autocrafting"
S_COND, S_WIRE, S_SPACE, S_CHEM = "Matter Condenser", "Wireless", "Spatial Storage", "Chemicals and Flux"
OPT = dict(optional=True, tokens=1)

CHAPTER = Chapter("ae2", "Applied Energistics", "ae2:controller",
        ["The archive of a god: every item as data, every recipe on demand."], SIDE, [
    # ===== First Steps ==========================================================================
    Q("ae_start", 0, 0, [anytag("c:chests")], "Before the Archive", section=S_START, deps=["t5_hv"], xp=25,
      size=1.5, shape="hexagon", mirror="2893F483C10293E6", subtitle="Any chest: the last storage that isn't data", desc=[
        "&6You remember a library with no shelves, where every book answered when you thought of it.&r",
        "&eWhat:&r Applied Energistics 2 turns items into data. A network of cables, drives and terminals holds everything you own and can craft on demand.",
        "&eHow:&r show any chest to begin. Soon a single terminal will replace rooms of them.",
        "&eTip:&r AE2 opens in the HV tier here: the Inscriber needs an MI Turbo hull and the Controller a digital circuit."]),
    Q("ae_tip_start", 0, 0, [tick()], "Note: Read the Guide", section=S_START, deps=["ae_start"], xp=10, icon="ae2:guide",
      **OPT, mirror="7C40F1963FC5BF65", subtitle="AE2 ships its own manual", desc=[
        "&eWhat:&r AE2's in-game guide explains every block, with pictures. Hold G over an AE2 item in JEI or your inventory to open its page.",
        "&eTip:&r the guide's 'Getting Started' pages cover channels better than any quest text could."]),
    Q("ae_tip_guide", 0, 0, [tick(), tick()], "Note: Channels and Power", section=S_START, deps=["ae_start"], xp=10, icon="ae2:fluix_glass_cable",
      **OPT, mirror="5034A9137E0F3D3D", subtitle="The two things that break a network", desc=[
        "&eWhat:&r almost every AE2 problem is one of two things: the network has no power, or a device has no channel.",
        "&eHow:&r a device whose light is off has no channel; a dark terminal means no power. Tick one box for each once you've read it.",
        "&eTip:&r the Network Tool (later in this chapter) shows both at a glance."]),
    Q("ae_wrench", 0, 0, [anytag("ae2:quartz_wrench")], "Quartz Wrench", section=S_START, deps=["ae_start"], xp=20,
      mirror="1B686954D34A0F23", subtitle="Turn and pick up AE2 blocks", desc=[
        "&eWhat:&r the wrench rotates AE2 blocks and sneak-click picks them up, parts included.",
        "&eHow:&r certus or nether quartz with iron (check JEI).",
        "&eTip:&r it also removes a single cable part without breaking the cable."]),
    Q("ae_charged", 0, 0, [item("ae2:charger"), item("ae2:inscriber")], "Charger and Inscriber", section=S_START, deps=["ae_start"], xp=60,
      mirror="68B0B3DAF1145191", subtitle="The two machines every AE2 part goes through", desc=[
        "&eWhat:&r the Charger puts energy into certus crystals; the Inscriber presses processors and grinds crystals into dust.",
        "&eChemistry:&r real quartz is piezoelectric: squeeze it and it makes a voltage, push a voltage into it and it flexes. AE2 imagines it can store the charge.",
        "&eHow:&r the Charger is iron and copper (check JEI). The Inscriber is gated here: it needs an MI Turbo hull.",
        "&eTip:&r a Crank on top of the Charger works too, slowly, if your power isn't up yet."]),
    Q("ae_dowsing", 0, 0, [item("ars_nouveau:dowsing_rod")], "Dowsing Rod", section=S_START, deps=["ae_charged"], xp=20,
      **OPT, mirror="332A3C7BA261DBFC", subtitle="Optional: a magical way to find things", desc=[
        "&eWhat:&r Ars Nouveau's Dowsing Rod highlights nearby blocks of interest. It's a second way into the meteor hunt.",
        "&eHow:&r check JEI (it needs source from Ars Nouveau).",
        "&eTip:&r the compass is faster for meteorites; the rod is handy for everything else."]),
    Q("ae_compass", 0, 0, [item("ae2:meteorite_compass")], "Meteorite Compass", section=S_START, deps=["ae_charged", "ae_dowsing"], xp=50,
      any_dep=True, mirror="51236544BFEF487B", subtitle="It points at fallen stars", desc=[
        "&eWhat:&r the compass needle swings towards the nearest meteorite, where certus and the Inscriber presses wait.",
        "&eHow:&r charged certus and iron (check JEI).",
        "&eTip:&r each meteorite holds one press in its mysterious cube. You need four."]),

    # ===== Crystals and Processors ==============================================================
    Q("ae_certus", 0, 0, [item("ae2:certus_quartz_crystal"), item("ae2:certus_quartz_dust")], "Certus Quartz", section=S_CRYS, deps=["ae_compass"], xp=60,
      mirror="79D2617E01481281", subtitle="The crystal every AE2 part starts from", desc=[
        "&6You remember crystals that sang when you touched them. These still hum, faintly.&r",
        "&eWhat:&r certus quartz goes into almost every AE2 recipe: processors, glass, cells and cards.",
        "&eChemistry:&r certus is fictional, but it behaves like real quartz (SiO₂), which is piezoelectric: squeeze it and it makes a small voltage.",
        "&eHow:&r mine certus from meteorite craters and budding certus. Grind crystals into dust in the Inscriber with no press.",
        "&eTip:&r charged certus plus certus dust dropped in water makes two new crystals. Grow it once you have a little."]),
    Q("ae_fluix", 0, 0, [item("ae2:fluix_dust"), item("ae2:fluix_crystal")], "Fluix", section=S_CRYS, deps=["ae_certus"], xp=60,
      mirror="4BF0BB763BFFACF0", subtitle="Certus, quartz and redstone, in water", desc=[
        "&eWhat:&r fluix crystals carry AE2's channels: every cable, core and most parts need fluix.",
        "&eChemistry:&r a reaction in solution: charged certus, nether quartz and redstone dropped together in water fuse into fluix. Real crystals also grow fastest from a seed in solution.",
        "&eHow:&r throw charged certus, nether quartz and redstone into a water block: you get two fluix crystals. Grind fluix in the Inscriber for dust.",
        "&eTip:&r four crystals make a fluix block, which is where ExtendedAE's entro grows (see its own page)."]),
    Q("ae_logic", 0, 0, [item("ae2:logic_processor"), item("ae2:calculation_processor"), item("ae2:engineering_processor")], "The Three Processors",
      section=S_CRYS, deps=["ae_compass"], xp=100, mirror="15564C11744D6AA0", subtitle="Logic, calculation and engineering", desc=[
        "&eWhat:&r AE2's three processors: logic (gold), calculation (certus) and engineering (diamond). You'll want hundreds of each.",
        "&eChemistry:&r gold barely reacts with air or water, so it never corrodes; real chips use it for contacts. Diamond spreads heat better than any metal.",
        "&eHow:&r press the material with its press, press MI silicon with the Silicon Press, then inscribe the print, redstone and printed silicon together.",
        "&eTip:&r one Inscriber per processor type, each fed by pipes, keeps all three in stock."]),
    Q("ae_channels", 0, 0, [anytag("ae2:glass_cable"), anytag("ae2:covered_cable"), anytag("ae2:covered_dense_cable")], "Cables",
      section=S_CRYS, deps=["ae_fluix"], xp=60, mirror="5C22E3103544B120", subtitle="Glass, covered and dense", desc=[
        "&eWhat:&r each ME device uses one channel. Glass and covered cables carry 8 channels, dense cables 32. Any colour counts.",
        "&eHow:&r fluix crystals and quartz make glass cable; wool covers it; four covered cables and redstone make a dense one (check JEI).",
        "&eTip:&r build a dense-cable backbone from the controller and branch normal cables off it.",
        "{@pagebreak}",
        "&eDeep dive:&r if a device's light is off, it has no channel. Count devices on each normal cable (max 8). Drives, terminals, buses and interfaces all count. Plain cables, quartz fibre and energy cells don't."]),
    Q("ae_smart_cables", 0, 0, [anytag("ae2:smart_cable"), anytag("ae2:smart_dense_cable")], "Smart Cables", section=S_CRYS, deps=["ae_channels"], xp=40,
      mirror="5233A447BAA4593C", subtitle="Cables that show their channels", desc=[
        "&eWhat:&r smart cables light up one stripe per channel in use, so you can see where a branch runs out.",
        "&eHow:&r a covered cable plus redstone and glowstone (check JEI); the dense version from dense cable.",
        "&eTip:&r use smart cable on the busy branches and plain cable everywhere else."]),
    Q("ae_tip_channels", 0, 0, [tick()], "Note: Count Your Channels", section=S_CRYS, deps=["ae_channels"], xp=10, icon="ae2:fluix_smart_cable",
      mirror="78311531069807DE", subtitle="Eight on a cable, thirty-two on a dense one", desc=[
        "&eWhat:&r a controller sends 32 channels out of each face. A normal cable carries 8 of them, a dense cable all 32.",
        "&eHow:&r plan one dense line per face, then branch. Click to continue.",
        "&eTip:&r a subnetwork behind an interface spends only one channel on the main network."]),
    Q("ae_name_press", 0, 0, [anytag("ae2:knife"), item("ae2:cable_anchor"), item("ae2:name_press")], "Knife, Anchor and Name Press", section=S_CRYS,
      deps=["ae_channels"], xp=40, mirror="6144202A97C6CD1C", subtitle="Small tools for tidy networks", desc=[
        "&eWhat:&r the cutting knife makes Cable Anchors (they keep two neighbouring cables from joining) and the Inscriber Name Press, which labels items.",
        "&eHow:&r a knife from certus or nether quartz and iron; cut any metal ingot for 4 anchors, or iron for the press (check JEI).",
        "&eTip:&r rename the press in an anvil, then press anything with it to give it that name. Every chemist labels their bottles."]),
    Q("ae_color_applicator", 0, 0, [item("ae2:color_applicator")], "Color Applicator", section=S_CRYS, deps=["ae_channels"], xp=40,
      mirror="03E6FA4DCB71162E", subtitle="Paint your cables", desc=[
        "&eWhat:&r the Color Applicator paints cables. Cables of different colours don't connect, so two networks can run side by side.",
        "&eChemistry:&r dyes work by absorbing some wavelengths of light and reflecting the rest; the colour you see is what's left over.",
        "&eHow:&r an energy cell, a 4k component and processors (check JEI). Load dye into it and charge it."]),
    # --- our own steps (ATM10 has none of these): optional
    Q("ae_sky_stone", 0, 0, [item("ae2:sky_stone_block", 16), item("ae2:smooth_sky_stone_block", 4)], "Sky Stone", section=S_CRYS, deps=["ae_compass"], xp=50,
      **OPT, subtitle="Optional: stone that fell from the sky", desc=[
        "&eWhat:&r sky stone is the rock of AE2 meteorites. The ME Controller in this pack needs smooth sky stone.",
        "&eChemistry:&r real stony meteorites are mostly silicate minerals like olivine and pyroxene; iron meteorites are an iron-nickel alloy.",
        "&eHow:&r mine the crater shell (iron pickaxe or better), then smelt sky stone into smooth sky stone.",
        "&eTip:&r the Inscriber grinds sky stone into sky dust, which ExtendedAE and AdvancedAE recipes ask for."]),
    Q("ae_presses", 0, 0, [item("ae2:logic_processor_press"), item("ae2:calculation_processor_press")], "All Four Presses", section=S_CRYS, deps=["ae_compass"], xp=100,
      **OPT, subtitle="Optional: logic and calculation join the set", desc=[
        "&eWhat:&r the Inscriber has four presses: silicon, logic, calculation and engineering. You need all four for the processors.",
        "&eHow:&r each meteorite's mysterious cube holds one press. Keep finding meteorites until you have the set.",
        "&eTip:&r never use your only copy in a long automation line. Make a spare in the Inscriber with an iron block first (check JEI)."]),
    Q("ae_silicon", 0, 0, [item("modern_industrialization:silicon_ingot", 8), item("ae2:printed_silicon", 4)], "Printed Silicon", section=S_CRYS, deps=["ae_presses"], xp=75,
      **OPT, subtitle="Optional: every processor sits on silicon", desc=[
        "&eWhat:&r printed silicon is the base layer of every AE2 processor.",
        "&eChemistry:&r industry makes silicon by heating quartz with carbon to about 2000 °C: SiO₂ + 2C → Si + 2CO. Chips need it purer than 99.9999999%.",
        "&eHow:&r press MI silicon ingots in the Inscriber with the Silicon Press. They come from the Electric Blast Furnace (quartz dust + coke dust).",
        "&eTip:&r in this pack certus and sand don't smelt into silicon: carbothermic reduction is the only way, as in the real world."]),
    Q("ae_calc", 0, 0, [item("ae2:printed_calculation_processor", 4), item("ae2:calculation_processor", 4)], "Calculation Prints", section=S_CRYS, deps=["ae_silicon"], xp=60,
      **OPT, subtitle="Optional: a quartz heartbeat for the network", desc=[
        "&eWhat:&r calculation processors go into crafting units, cards, bigger cell components and wireless parts.",
        "&eChemistry:&r a real quartz crystal vibrates at a precise frequency when a voltage drives it. Watches count 32,768 vibrations a second to keep time.",
        "&eHow:&r press a certus crystal with the Calculation Press, then combine it with redstone and printed silicon."]),
    Q("ae_housing", 0, 0, [item("ae2:item_cell_housing", 2), item("ae2:fluid_cell_housing", 2)], "Cell Housings", section=S_CRYS, deps=["ae_certus"], xp=50,
      **OPT, subtitle="Optional: the case every storage cell needs", desc=[
        "&eWhat:&r a storage cell is a housing plus a component. Item housings take iron; fluid housings take copper.",
        "&eHow:&r quartz glass, redstone and metal in a crafting table (check JEI).",
        "&eTip:&r sneak-use an empty cell in the air to split it back into housing and component, for upgrading to a bigger one."]),
    Q("ae_cores", 0, 0, [item("ae2:annihilation_core", 2), item("ae2:formation_core", 2)], "Annihilation and Formation", section=S_CRYS, deps=["ae_logic"], xp=60,
      **OPT, subtitle="Optional: the cores that move things in and out", desc=[
        "&eWhat:&r annihilation cores take things into the network; formation cores put things out. Interfaces, providers, planes and assemblers all need both.",
        "&eHow:&r nether quartz (annihilation) or certus (formation), plus fluix dust and a logic processor, two at a time.",
        "&eTip:&r make a stack of each. Autocrafting eats them fast."]),
    Q("ae_budding", 0, 0, [item("ae2:damaged_budding_quartz"), item("ae2:chipped_budding_quartz")], "Budding Certus by Hand", section=S_CRYS, deps=["ae_certus"], xp=60,
      **OPT, subtitle="Optional: grow your own crystal farm", desc=[
        "&eWhat:&r a certus quartz block dropped in water with charged certus becomes Damaged Budding Certus; repeat to climb to Chipped and better.",
        "&eHow:&r throw a certus block and a charged crystal into water together (JEI's transform tab).",
        "&eTip:&r lower-grade budding blocks decay as they grow. Keep charged certus to remake them."]),
    Q("ae_ender_dust", 0, 0, [item("ae2:ender_dust", 8)], "Ender Dust", section=S_CRYS, deps=["ae_charged"], xp=30,
      **OPT, subtitle="Optional: ground pearls", desc=[
        "&eWhat:&r ender pearls ground into dust in the Inscriber. Entangled singularities, entro seeds and wireless parts use it.",
        "&eHow:&r put an ender pearl in the Inscriber with no press.",
        "&eTip:&r an enderman model in a Simulation Chamber keeps the pearls coming."]),
    Q("ae_fluix_sword", 0, 0, [item("ae2:fluix_sword")], "Fluix Sword", section=S_CRYS, deps=["ae_fluix"], xp=30,
      **OPT, subtitle="Optional: a crystal blade", desc=[
        "&eWhat:&r a sword with a fluix crystal edge. Compare its stats with iron in JEI.",
        "&eHow:&r fluix crystals and a stick, like any sword (check JEI)."]),

    # ===== Power ================================================================================
    Q("ae_energy", 0, 0, [item("ae2:energy_acceptor")], "Energy Acceptor", section=S_POWER, deps=["ae_certus"], xp=60,
      mirror="00611844AFD5C31E", subtitle="AE2 runs on its own energy, fed by FE", desc=[
        "&eWhat:&r the ME network turns FE into its own AE energy. The Energy Acceptor does the converting.",
        "&eHow:&r connect it to any FE source (an energy cube, a Powah cell, a Flux Point) and to your cables (check JEI).",
        "&eTip:&r a controller face can't take power directly from FE; always go through an acceptor."]),
    Q("ae_dense_energy", 0, 0, [item("ae2:energy_cell"), item("ae2:dense_energy_cell")], "Energy Cells", section=S_POWER, deps=["ae_energy"], xp=60,
      mirror="037488EF1F3581CE", subtitle="A buffer for big jobs", desc=[
        "&eWhat:&r Energy Cells store AE; a Dense Energy Cell stores eight times more.",
        "&eHow:&r the dense cell is eight Energy Cells around a calculation processor (check JEI). Put them anywhere on the network.",
        "&eTip:&r when a network flickers during autocrafting, more buffer is usually the cure, not more power input."]),
    Q("ae_energy_card", 0, 0, [item("ae2:energy_card")], "Energy Card", section=S_POWER, deps=["ae_dense_energy"], xp=40,
      mirror="6D54B45CDA70FEAB", subtitle="More charge in your portable tools", desc=[
        "&eWhat:&r an Energy Card raises how much AE a portable terminal, cell or tool holds.",
        "&eChemistry:&r a battery's capacity depends on how much reactant it holds; adding cells in parallel adds capacity, as this card does.",
        "&eHow:&r an advanced card plus a dense energy cell (check JEI). Slot it into the item in a Cell Workbench."]),

    # ===== The Network ==========================================================================
    Q("s_ae_craft", 0, 0, [item("ae2:terminal"), item("ae2:crafting_terminal")], "Terminals", section=S_NET, deps=["ae_logic"], xp=75,
      mirror="22C4318523A43B49", subtitle="Your window into the archive", desc=[
        "&eWhat:&r the ME Terminal shows and searches everything the network stores. The Crafting Terminal adds a crafting grid that pulls from storage.",
        "&eHow:&r an illuminated panel plus processors; the crafting version adds a crafting table (check JEI).",
        "&eTip:&r JEI's + button fills the crafting terminal's grid straight from the network."]),
    Q("ae_controller", 0, 0, [item("ae2:controller")], "ME Controller", section=S_NET, deps=["s_ae_craft", "ae_channels"], xp=100,
      mirror="2F16B6A173525277", subtitle="The heart of the network", desc=[
        "&eWhat:&r the Controller hands out channels: 32 from each face. Without one, a network is limited to 8 devices.",
        "&eHow:&r in this pack it takes smooth sky stone, fluix, an engineering processor and an MI digital circuit (check JEI).",
        "&eTip:&r controller blocks can be joined into a bigger box, but never into a cross or a loop."]),
    Q("ae_tools", 0, 0, [item("ae2:network_tool")], "Network Tool", section=S_NET, deps=["s_ae_craft"], xp=40,
      mirror="6431A384DDFBF439", subtitle="Read channels and power at a glance", desc=[
        "&eWhat:&r right-click any cable or device with the Network Tool to see its channels, power use and status. It also holds spare upgrade cards.",
        "&eHow:&r a quartz wrench, a chest and a calculation processor (check JEI).",
        "&eTip:&r when something's dark, this is the first tool to reach for."]),
    Q("s_ae_drive", 0, 0, [item("ae2:chest"), item("ae2:drive")], "ME Chest and Drive", section=S_NET, deps=["ae_controller"], xp=150,
      size=1.5, shape="hexagon", mirror="4E8A05C3BFA80540", subtitle="Where the cells live", desc=[
        "&6You remember a mind that held every name of every thing. The archive is waking.&r",
        "&eWhat:&r the ME Chest is a one-cell drive with its own terminal. The ME Drive holds ten cells for the whole network.",
        "&eHow:&r both from iron, quartz glass, fluix cable and processors (check JEI). Connect the drive to the controller with cable.",
        "&eTip:&r keep power stable: an Energy Cell buffers the network."]),
    Q("ae_workbench", 0, 0, [item("ae2:cell_workbench")], "Cell Workbench", section=S_NET, deps=["s_ae_drive"], xp=50,
      mirror="2F556E7919582D2D", subtitle="Partition and upgrade cells", desc=[
        "&eWhat:&r the Cell Workbench sets which items a cell accepts (partitioning) and adds cards to cells.",
        "&eHow:&r wool, iron, a chest and a calculation processor (check JEI).",
        "&eTip:&r a cell partitioned to one dust keeps that stock in one place."]),
    Q("ae_io_port", 0, 0, [item("ae2:io_port")], "IO Port", section=S_NET, deps=["s_ae_drive"], xp=50,
      mirror="7B7D1F0CB326B28F", subtitle="Move whole cells at once", desc=[
        "&eWhat:&r the IO Port empties a cell into the network, or fills a cell from it.",
        "&eHow:&r glass, two drives, fluix cable, iron and a logic processor (check JEI).",
        "&eTip:&r upgrading 4k cells to 64k? Run the old cells through an IO Port first."]),
    Q("ae_flow_cards", 0, 0, [item("ae2:equal_distribution_card")], "Equal Distribution Card", section=S_NET, deps=["ae_workbench"], xp=40,
      mirror="3195A7AA874163CD", subtitle="Spread items over a cell's partitions", desc=[
        "&eWhat:&r with this card a partitioned cell keeps the same room for each of its items, so one item can't crowd out the others.",
        "&eHow:&r a basic card plus a few items (check JEI). Slot it in through the Cell Workbench."]),
    Q("ae_void_card", 0, 0, [item("ae2:void_card")], "Overflow Destruction Card", section=S_NET, deps=["ae_workbench"], xp=40,
      mirror="33ADE41526C39AFD", subtitle="Delete what a full cell can't hold", desc=[
        "&eWhat:&r a cell with this card destroys items of its partitioned types once it's full, instead of refusing them.",
        "&eChemistry:&r real matter can't vanish: mass is conserved in every chemical reaction. In Minecraft it can.",
        "&eHow:&r a basic card plus a few items (check JEI). Use it with a partition, or it will delete everything.",
        "&eTip:&r a void card on a cobblestone cell stops a generator from filling your whole network."]),

    # ===== Storage Cells ========================================================================
    Q("s_ae_cell", 0, 0, [item("ae2:cell_component_1k")], "1k Component", section=S_CELLS, deps=["s_ae_drive"], xp=60,
      mirror="2FB231069D2E4E77", subtitle="Bytes for your items", desc=[
        "&eWhat:&r components are the memory inside every storage cell. The 1k is the smallest.",
        "&eChemistry:&r certus and fluix are fictional, but the logic processors behind them echo real chips: doped silicon (Si).",
        "&eHow:&r certus, redstone and a logic processor (check JEI)."]),
    Q("ae_cell_4k", 0, 0, [item("ae2:cell_component_4k")], "4k Component", section=S_CELLS, deps=["s_ae_cell"], xp=50,
      mirror="3B42CCC19D23EC6D", subtitle="Four times the bytes", desc=[
        "&eWhat:&r the first step up: a 4k component holds four times as many bytes as a 1k.",
        "&eHow:&r three 1k components around quartz glass, with redstone and a calculation processor (check JEI)."]),
    Q("ae_cell_tiers", 0, 0, [item("ae2:cell_component_16k")], "16k Component", section=S_CELLS, deps=["ae_cell_4k"], xp=60,
      mirror="219932CB19258C16", subtitle="Room for whole chemical stocks", desc=[
        "&eWhat:&r each tier combines three of the last with a calculation processor and quartz glass.",
        "&eHow:&r 16k from three 4k (check JEI).",
        "&eTip:&r a cell holds up to 63 item types whatever its size, so use small cells for odd items and big cells for bulk."]),
    Q("ae_cell_64k", 0, 0, [item("ae2:cell_component_64k")], "64k Component", section=S_CELLS, deps=["ae_cell_tiers"], xp=75,
      mirror="523853C1C4E688BA", subtitle="Enough for a mine's worth of dust", desc=[
        "&eWhat:&r the 64k component, also what the Matter Condenser needs to make singularities.",
        "&eHow:&r three 16k components around quartz glass, with a calculation processor (check JEI)."]),
    Q("ae_cell_256k", 0, 0, [item("ae2:cell_component_256k")], "256k Component", section=S_CELLS, deps=["ae_cell_64k"], xp=100,
      mirror="5F56892CD904C40F", subtitle="The biggest cell in base AE2", desc=[
        "&eWhat:&r the top AE2 component: 256 kilobytes for a single cell.",
        "&eHow:&r three 64k components around quartz glass, with sky stone dust and a calculation processor (check JEI).",
        "&eTip:&r a cell spends bytes on every new item type, so put bulk stock here and rare items elsewhere."]),
    Q("ae_mega_ladder", 0, 0, [item("megacells:cell_component_1m")], "1M Component", section=S_CELLS, deps=["ae_cell_256k"], xp=150,
      size=1.5, shape="hexagon", mirror="460A8F17F3ED6CAF", subtitle="MEGA Cells: a million bytes", desc=[
        "&eWhat:&r MEGA Cells continues the ladder past 256k: 1M, 4M, 16M, 64M, 256M.",
        "&eHow:&r 256k components, sky steel and accumulation processors (check JEI; the MEGA Cells section has both).",
        "&eTip:&r MEGA components need MEGA cell housings; AE2's won't take them."]),
    Q("ae_mega_big", 0, 0, [item("megacells:cell_component_4m")], "4M Component", section=S_CELLS, deps=["ae_mega_ladder"], xp=100,
      mirror="25DBA00422301EDC", subtitle="Four million bytes", desc=[
        "&eWhat:&r the 4M component, four times the 1M.",
        "&eHow:&r 1M components, accumulation processors, ender dust and vibrant quartz glass (check JEI)."]),
    Q("ae_mega_16m", 0, 0, [item("megacells:cell_component_16m")], "16M Component", section=S_CELLS, deps=["ae_mega_big"], xp=125,
      mirror="0E809747193ED3A9", subtitle="Sixteen million", desc=[
        "&eWhat:&r the next MEGA step.",
        "&eHow:&r three 4M components with accumulation processors (check JEI)."]),
    Q("ae_mega_64m", 0, 0, [item("megacells:cell_component_64m")], "64M Component", section=S_CELLS, deps=["ae_mega_16m"], xp=150,
      mirror="3CE3D9245F8EC005", subtitle="Sixty-four million", desc=[
        "&eWhat:&r one step from the top.",
        "&eHow:&r three 16M components with accumulation processors (check JEI)."]),
    Q("ae_mega_top", 0, 0, [item("megacells:cell_component_256m")], "256M Component", section=S_CELLS, deps=["ae_mega_64m"], xp=250,
      mirror="51A57E142C686C8F", subtitle="The largest component there is", desc=[
        "&6Every name of every thing, and room to spare. You remember this kind of memory.&r",
        "&eWhat:&r the 256M MEGA component, the top of AE2 storage in this pack.",
        "&eHow:&r three 64M components with accumulation processors (check JEI)."]),
    Q("ae_item_cell", 0, 0, [item("ae2:item_storage_cell_1k")], "Item Storage Cell", section=S_CELLS, deps=["s_ae_cell"], xp=40,
      mirror="361CCBD353D6FF34", subtitle="A component in a housing", desc=[
        "&eWhat:&r the 1k item cell: the thing you actually put in a drive.",
        "&eHow:&r a 1k component in an item cell housing (check JEI).",
        "&eTip:&r sneak-use an empty cell in the air to split it back into housing and component."]),
    Q("ae_fluid_cell", 0, 0, [anyof(["ae2:fluid_storage_cell_1k", "ae2:fluid_storage_cell_4k", "ae2:fluid_storage_cell_16k",
                                     "ae2:fluid_storage_cell_64k", "ae2:fluid_storage_cell_256k"])], "Fluid Storage Cell", section=S_CELLS,
      deps=["ae_item_cell"], xp=40, mirror="5E24012A3D9B72A1", subtitle="Acids and solvents as data", desc=[
        "&eWhat:&r fluid cells store fluids the same way item cells store items. Any size counts.",
        "&eChemistry:&r H₂SO₄, HCl and HNO₃ each eat through different metals, so a real lab needs a different container for each. A fluid cell doesn't care.",
        "&eHow:&r a component in a fluid cell housing (check JEI)."]),
    Q("ae_portable_cell", 0, 0, [anyof(["ae2:portable_item_cell_1k", "ae2:portable_item_cell_4k", "ae2:portable_item_cell_16k", "ae2:portable_item_cell_64k",
                                        "ae2:portable_item_cell_256k", "ae2:portable_fluid_cell_1k", "ae2:portable_fluid_cell_4k", "ae2:portable_fluid_cell_16k",
                                        "ae2:portable_fluid_cell_64k", "ae2:portable_fluid_cell_256k"])], "Portable Cell", section=S_CELLS,
      deps=["ae_item_cell"], xp=40, mirror="77C9EE701F72586D", subtitle="A drive in your pocket", desc=[
        "&eWhat:&r a portable cell is a storage cell with its own terminal and battery. Any size, item or fluid.",
        "&eHow:&r a component, a chest, a terminal and an energy cell (check JEI). Charge it in the Charger.",
        "&eTip:&r a portable cell on a mining trip holds far more than a backpack."]),
    Q("ae_bulk", 0, 0, [item("megacells:bulk_item_cell")], "Bulk Item Cell", section=S_CELLS, deps=["ae_item_cell"], xp=100,
      mirror="0F03E75CF79BADD7", subtitle="One item, practically no limit", desc=[
        "&eWhat:&r a Bulk Item Cell holds a single item type in near-unlimited amounts.",
        "&eHow:&r the bulk component needs a 1M component and accumulation processors (check JEI). Partition it in a Cell Workbench.",
        "&eTip:&r perfect for cobblestone (condenser feed), salt dust or coal coke. A Compression Card stores nuggets, ingots and blocks as one pool."]),
    Q("ae_powered_tools", 0, 0, [item("ae2:charged_staff"), item("ae2:entropy_manipulator"), item("ae2:matter_cannon")], "AE2 Powered Tools", section=S_CELLS,
      deps=["s_ae_cell"], xp=60, mirror="5CD8D169181C7339", subtitle="Zap, heat and cool, shoot", desc=[
        "&eWhat:&r the Charged Staff zaps mobs; the Entropy Manipulator heats or cools blocks; the Matter Cannon fires matter balls or nuggets.",
        "&eChemistry:&r the manipulator follows real phase changes: removing heat freezes water, and lava cools into obsidian when it loses heat too fast to crystallise.",
        "&eHow:&r each uses an energy cell and processors; the cannon also takes a 4k component (check JEI). Charge them in the Charger."]),

    # ===== MEGA Cells (our own parts of MEGA; optional) =========================================
    Q("s_mega", 0, 0, [item("megacells:sky_steel_ingot", 4), item("megacells:item_storage_cell_1m")], "Sky Steel", section=S_MEGA, deps=["ae_cell_256k"], xp=150,
      **OPT, subtitle="Optional: the lava alloy behind MEGA's cells", desc=[
        "&eWhat:&r sky steel goes into every MEGA part. The 1M item cell is the first MEGA cell you can put in a drive.",
        "&eChemistry:&r sky steel is made by dropping charged certus, iron and sky stone into lava: heat drives the alloying, like a tiny smelter.",
        "&eHow:&r throw the ingredients into a lava pool for sky steel, then build the 1M cell (check JEI)."]),
    Q("ae_sky_alloys", 0, 0, [item("megacells:sky_bronze_ingot", 4), item("megacells:sky_osmium_ingot", 4)], "Sky Bronze and Sky Osmium", section=S_MEGA, deps=["s_mega"], xp=75,
      **OPT, subtitle="Optional: more lava alloys", desc=[
        "&eWhat:&r the same lava trick with copper gives sky bronze, and with osmium gives sky osmium. Both go into MEGA's larger parts.",
        "&eChemistry:&r real bronze is copper plus tin (Cu + Sn); here the sky stone plays the tin. Osmium (Os) is the densest natural element, 22.6 g/cm³.",
        "&eHow:&r drop charged certus, the ingot and a sky stone block into lava together."]),
    Q("ae_accumulation", 0, 0, [item("megacells:accumulation_processor", 4)], "Accumulation Processors", section=S_MEGA, deps=["s_mega", "ae_condenser"], xp=150,
      **OPT, subtitle="Optional: a press made from a singularity", desc=[
        "&eWhat:&r the accumulation processor is MEGA's fourth processor, needed for every 1M+ part.",
        "&eHow:&r inscribe a singularity between the calculation and engineering presses to make the Accumulation Press, then print sky steel with it (check JEI).",
        "&eTip:&r keep the press. The Inscriber can copy it with an iron block, like the other presses."]),
    Q("ae_mega_crafting", 0, 0, [item("megacells:1m_crafting_storage"), item("megacells:mega_crafting_unit", 4)], "MEGA Crafting CPU", section=S_MEGA, deps=["ae_accumulation"], xp=150,
      **OPT, subtitle="Optional: room for the biggest crafting jobs", desc=[
        "&eWhat:&r MEGA crafting storage and units build a separate, much larger crafting CPU.",
        "&eHow:&r check JEI. MEGA blocks only join other MEGA blocks, so build it as its own multiblock.",
        "&eTip:&r the Seed of a New World chain is huge. One big CPU saves splitting the job by hand."]),
    Q("ae_mega_provider", 0, 0, [item("megacells:mega_pattern_provider")], "MEGA Pattern Provider", section=S_MEGA, deps=["ae_mega_crafting"], xp=100,
      **OPT, subtitle="Optional: room for many more patterns", desc=[
        "&eWhat:&r a pattern provider with many more pattern slots than the normal one.",
        "&eHow:&r made as a cable part and turned into a block in the crafting grid (check JEI).",
        "&eTip:&r put one on each multi-input MI machine, like the Chemical Reactor."]),
    Q("ae_mega_energy", 0, 0, [item("megacells:mega_energy_cell"), item("megacells:greater_energy_card")], "MEGA Energy", section=S_MEGA, deps=["ae_accumulation"], xp=100,
      **OPT, subtitle="Optional: a huge AE buffer and a stronger card", desc=[
        "&eWhat:&r the MEGA Energy Cell is eight dense cells around an accumulation processor. The Greater Energy Card gives portable tools far more charge.",
        "&eHow:&r both in a crafting table (check JEI)."]),
    Q("ae_mega_portable", 0, 0, [item("megacells:portable_item_cell_256m")], "A Pocket Archive", section=S_MEGA, deps=["ae_mega_top"], xp=200,
      optional=True, tokens=2, subtitle="Optional: 256M in your inventory", desc=[
        "&eWhat:&r a portable cell with a 256M component: a whole storage network you carry, no drive needed.",
        "&eHow:&r a 256M component in a portable cell housing with an energy cell (check JEI). Charge it first.",
        "&eTip:&r perfect for a long trip to another planet."]),

    # ===== Interfaces and Buses =================================================================
    Q("ae_interface", 0, 0, [anytag("ae2:interface")], "ME Interface", section=S_IO, deps=["ae_channels"], xp=100,
      size=1.5, shape="hexagon", mirror="74FC0DDDB91DB172", subtitle="Stock a machine, or join two networks", desc=[
        "&eWhat:&r an interface keeps chosen items stocked in itself for pipes and machines to pull. A storage bus on an interface lets one network see into another. Block or cable-part version.",
        "&eHow:&r iron, glass, an annihilation core and a formation core (check JEI). Set the items to keep in its top row.",
        "&eTip:&r a subnetwork for one chemical line, joined to the main network through an interface, keeps channels free."]),
    Q("ae_import_bus", 0, 0, [item("ae2:import_bus")], "Import Bus", section=S_IO, deps=["ae_interface"], xp=40,
      mirror="5E7E35CCAF1C88EE", subtitle="Pull items into the network", desc=[
        "&eWhat:&r an Import Bus pulls items out of the inventory it faces and into storage.",
        "&eHow:&r an annihilation core, iron and a sticky piston (check JEI). Put it on a cable facing a machine's output.",
        "&eTip:&r add a filter and Acceleration Cards to pull only products, faster."]),
    Q("ae_export_bus", 0, 0, [item("ae2:export_bus")], "Export Bus", section=S_IO, deps=["ae_interface"], xp=40,
      mirror="083D458032F0325C", subtitle="Push items out to a machine", desc=[
        "&eWhat:&r an Export Bus pushes chosen items from storage into the inventory it faces.",
        "&eHow:&r a formation core, iron and a piston (check JEI). Set what it exports in its slots.",
        "&eTip:&r an export bus feeding coal coke to a boiler keeps it lit forever."]),
    Q("ae_planes", 0, 0, [item("ae2:annihilation_plane")], "Annihilation Plane", section=S_IO, deps=["ae_import_bus"], xp=50,
      mirror="140DE53DC0FCD9F4", subtitle="Break blocks into the network", desc=[
        "&eWhat:&r the Annihilation Plane breaks the block in front of it, or picks up items that land there, and stores them.",
        "&eHow:&r fluix crystals and an annihilation core (check JEI). It takes enchantments like a pickaxe.",
        "&eTip:&r an annihilation plane in front of a cobblestone generator feeds the Matter Condenser with no pipes."]),
    Q("ae_formation_plane", 0, 0, [item("ae2:formation_plane")], "Formation Plane", section=S_IO, deps=["ae_export_bus"], xp=50,
      mirror="525F25F4ADE45B50", subtitle="Place blocks or drop items out", desc=[
        "&eWhat:&r the Formation Plane places blocks (or drops items) from the network into the space in front of it.",
        "&eHow:&r fluix crystals and a formation core (check JEI). Filter it, or it places anything you store."]),
    Q("ae_p2p", 0, 0, [item("ae2:me_p2p_tunnel")], "P2P Tunnels", section=S_IO, deps=["ae_interface"], xp=60,
      mirror="1710B3D05215A71E", subtitle="One cable, many channels", desc=[
        "&eWhat:&r a pair of P2P tunnels carries 32 channels (or items, fluids, FE and redstone) through a single cable.",
        "&eHow:&r iron, an engineering processor and fluix (check JEI). Place both ends, then link them with a Memory Card.",
        "&eTip:&r right-click a P2P tunnel with a bucket, redstone dust or an FE item to change what it carries."]),
    Q("ae_storage_bus", 0, 0, [item("ae2:storage_bus")], "Storage Bus", section=S_IO, deps=["ae_interface"], xp=50,
      mirror="7EFBAF3E281D2EBE", subtitle="Treat any chest as network storage", desc=[
        "&eWhat:&r a Storage Bus on a chest, drawer controller or tank lets the network read and fill it as if it were a cell.",
        "&eHow:&r an interface, a piston and a sticky piston (check JEI).",
        "&eTip:&r a storage bus on your Functional Storage controller gives AE2 the whole drawer wall, without spending cell types."]),
    Q("ae_memory_card", 0, 0, [item("ae2:memory_card")], "Memory Card", section=S_IO, deps=["ae_p2p"], xp=40,
      mirror="55186B8602689B66", subtitle="Copy settings from part to part", desc=[
        "&eWhat:&r the Memory Card copies a part's settings and filters to another, and links P2P tunnels.",
        "&eHow:&r a calculation processor, iron, gold and redstone (check JEI). Sneak-use it on the source, then use it on the target."]),
    Q("ae_capacity_card", 0, 0, [item("ae2:capacity_card")], "Capacity Card", section=S_IO, deps=["ae_storage_bus"], xp=40,
      mirror="371A382CF1DDF2B2", subtitle="More filter slots", desc=[
        "&eWhat:&r a Capacity Card adds filter slots to buses and other parts.",
        "&eHow:&r a basic card plus certus (check JEI). Slot it into the part's upgrade slots."]),
    Q("ae_fuzzy_inverter", 0, 0, [item("ae2:fuzzy_card"), item("ae2:inverter_card")], "Fuzzy and Inverter Cards", section=S_IO, deps=["ae_capacity_card"], xp=50,
      mirror="6E15447FC3D678E0", subtitle="Looser matches, reversed filters", desc=[
        "&eWhat:&r Fuzzy matches items by damage or ignores their data; Inverter turns a whitelist into a blacklist.",
        "&eHow:&r an advanced card plus one extra item each (check JEI).",
        "&eTip:&r an inverted storage bus on a junk chest takes everything except what you list."]),
    Q("ae_quartz_glass", 0, 0, [item("ae2:quartz_fiber")], "Quartz Fiber", section=S_IO, deps=["ae_interface"], xp=30,
      mirror="2077D64428E9C067", subtitle="Share power, not channels", desc=[
        "&eWhat:&r Quartz Fiber passes power between two networks without joining them.",
        "&eChemistry:&r glass made from pure SiO₂ (fused silica) is what real optical fibre is made of: so clear that light travels kilometres inside it.",
        "&eHow:&r glass and quartz dust (check JEI)."]),
    Q("ae_p2p_types", 0, 0, [item("ae2:fe_p2p_tunnel", 2), item("ae2:fluid_p2p_tunnel", 2)], "Tunnels for Everything", section=S_IO, deps=["ae_p2p"], xp=50,
      **OPT, subtitle="Optional: P2P for power and fluids", desc=[
        "&eWhat:&r P2P tunnels can carry FE, fluids, items, light or redstone instead of channels.",
        "&eHow:&r right-click an ME P2P tunnel with what it should carry, like a bucket or an FE item (check JEI for the full list).",
        "&eTip:&r FE tunnels move power through one cable instead of a bundle of power lines."]),

    # ===== Autocrafting =========================================================================
    Q("ae_pattern_access", 0, 0, [anytag("ae2:pattern_provider"), item("ae2:pattern_access_terminal")], "Pattern Providers", section=S_AUTO,
      deps=["ae_channels"], xp=150, size=1.5, shape="hexagon", mirror="51DE3157DE3E57B8", subtitle="Where recipes meet machines", desc=[
        "&eWhat:&r a Pattern Provider holds crafting patterns and sends their inputs to the machine it faces. The Pattern Access Terminal shows every provider on one screen.",
        "&eHow:&r iron, a crafting table and cores for the provider; an illuminated panel, an engineering processor and a provider for the terminal (check JEI).",
        "&eTip:&r processing patterns can drive MI machines too: send the inputs, wait for the outputs. The Automation and Logic page walks through a full sulfuric acid line."]),
    Q("ae_encoding", 0, 0, [item("ae2:pattern_encoding_terminal"), item("ae2:blank_pattern")], "Encoding Patterns", section=S_AUTO, deps=["ae_pattern_access"], xp=60,
      mirror="2C04B3BA507D5673", subtitle="Write a recipe onto a pattern", desc=[
        "&eWhat:&r the Pattern Encoding Terminal writes crafting or processing recipes onto blank patterns.",
        "&eHow:&r a crafting terminal plus an engineering processor; blank patterns from quartz glass, glowstone and iron (check JEI).",
        "&eTip:&r JEI's + button fills the encoder with any recipe you look up."]),
    Q("ae_assembler", 0, 0, [item("ae2:molecular_assembler")], "Molecular Assembler", section=S_AUTO, deps=["ae_encoding"], xp=75,
      mirror="4597D3B3BDC2BED5", subtitle="A crafting table that runs itself", desc=[
        "&eWhat:&r a Molecular Assembler next to a pattern provider crafts crafting-table recipes for the network.",
        "&eHow:&r iron, quartz glass, cores and a crafting table (check JEI).",
        "&eTip:&r one provider can feed up to six assemblers, one on each face."]),
    Q("ae_cards", 0, 0, [item("ae2:speed_card")], "Acceleration Card", section=S_AUTO, deps=["ae_assembler"], xp=40,
      mirror="1F7DFA5AA65F2812", subtitle="Faster buses, Inscribers and assemblers", desc=[
        "&eWhat:&r Acceleration Cards speed up buses, Inscribers and Molecular Assemblers.",
        "&eHow:&r an advanced card plus fluix (check JEI). Up to five in an assembler."]),
    Q("ae_level_emitter", 0, 0, [item("ae2:level_emitter")], "Level Emitter", section=S_AUTO, deps=["ae_pattern_access"], xp=50,
      mirror="3DDB0DDA7571B2C1", subtitle="A redstone signal that counts", desc=[
        "&eWhat:&r the Level Emitter gives a redstone signal when the network holds more (or less) of an item than you set.",
        "&eHow:&r a redstone torch and a calculation processor (check JEI).",
        "&eTip:&r wire one to an MI Electrolyzer so it only runs while hydrogen stock is low."]),
    Q("ae_cable_tricks", 0, 0, [item("ae2:redstone_card"), item("ae2:toggle_bus")], "Redstone Card and Toggle Bus", section=S_AUTO, deps=["ae_level_emitter"], xp=40,
      mirror="1AAF0B31B47AF23D", subtitle="Switch parts and branches by signal", desc=[
        "&eWhat:&r a Redstone Card makes a bus work only with (or without) a signal. A Toggle Bus connects or cuts a cable branch by redstone.",
        "&eHow:&r a basic card plus a redstone torch; the toggle bus is fluix cable, redstone and a lever (check JEI).",
        "&eTip:&r put a toggle bus in front of a subnetwork you only want running sometimes."]),
    Q("ae_behaviour_cards", 0, 0, [item("ae2:crafting_card")], "Crafting Card", section=S_AUTO, deps=["ae_cable_tricks"], xp=40,
      mirror="5E6585F7627247E3", subtitle="A bus that orders what it lacks", desc=[
        "&eWhat:&r with a Crafting Card, an export bus or interface asks autocrafting for items the network doesn't have.",
        "&eHow:&r a basic card plus a crafting table (check JEI).",
        "&eTip:&r a Crafting Card and a Redstone Card together make items only when a machine asks for them."]),
    Q("ae_growth", 0, 0, [item("ae2:growth_accelerator")], "Growth Accelerator", section=S_AUTO, deps=["ae_pattern_access"], xp=50,
      mirror="5AA3E5DFECB4AC4D", subtitle="Crystal farms at full speed", desc=[
        "&eWhat:&r Growth Accelerators speed up certus buds growing on budding certus blocks.",
        "&eChemistry:&r real quartz crystals grow from silica-rich water over thousands of years. The idea of a seed crystal pulling material out of solution is real.",
        "&eHow:&r iron, fluix cable, quartz glass and a fluix block (check JEI). Place them touching budding certus and power them.",
        "&eTip:&r flawless budding certus never decays. Never break it with a normal pickaxe."]),
    Q("ae_crafting_storage", 0, 0, [anyof(["ae2:1k_crafting_storage", "ae2:4k_crafting_storage", "ae2:16k_crafting_storage",
                                           "ae2:64k_crafting_storage", "ae2:256k_crafting_storage"])], "Crafting Storage", section=S_AUTO,
      deps=["ae_pattern_access"], xp=60, mirror="30E853CE699E669B", subtitle="The memory of a crafting CPU", desc=[
        "&eWhat:&r crafting storage blocks make a crafting CPU: the bigger the storage, the bigger the job it can plan.",
        "&eHow:&r a crafting unit plus a cell component of the matching size (check JEI). Build a solid box of crafting blocks.",
        "&eTip:&r two CPUs beat one huge one: a long job then doesn't block a quick request."]),
    Q("ae_cpu_accel", 0, 0, [item("ae2:crafting_accelerator")], "Co-Processor", section=S_AUTO, deps=["ae_crafting_storage"], xp=60,
      mirror="69B7DE2283B4EE6C", subtitle="More steps at once", desc=[
        "&eWhat:&r each Crafting Co-Processing Unit lets a CPU run one more step at the same time.",
        "&eHow:&r a crafting unit plus an engineering processor (check JEI).",
        "&eTip:&r co-processors only help if the machines keep up. Ten acid patterns on one Chemical Reactor still run one at a time."]),
    Q("ae_crafting_monitor", 0, 0, [item("ae2:crafting_monitor")], "Crafting Monitor", section=S_AUTO, deps=["ae_cpu_accel"], xp=40,
      mirror="1348995F64A94396", subtitle="See what the CPU is making", desc=[
        "&eWhat:&r the Crafting Monitor shows the item a CPU is working on, right on its face.",
        "&eHow:&r a crafting unit plus a storage monitor (check JEI). Part of the CPU's box."]),
    Q("ae_cpu_big", 0, 0, [item("ae2:16k_crafting_storage", 2), item("ae2:64k_crafting_storage")], "A Bigger Plan", section=S_AUTO, deps=["ae_crafting_storage"], xp=100,
      **OPT, subtitle="Optional: crafting storage for long chains", desc=[
        "&eWhat:&r long chemical chains need far more crafting storage than 1k.",
        "&eHow:&r a crafting unit plus a 16k or 64k component (check JEI). Add them to the CPU's box."]),
    Q("s_requester", 0, 0, [item("merequester:requester")], "ME Requester", section=S_AUTO, deps=["ae_crafting_storage"], xp=75,
      **OPT, subtitle="Optional: keep stock topped up", desc=[
        "&eWhat:&r the ME Requester keeps a set amount of an item in stock by ordering crafts automatically.",
        "&eHow:&r check JEI. Set \"keep 64 HDPE\" and it never runs out.",
        "&eTip:&r it needs autocrafting patterns for whatever it keeps in stock."]),
    Q("ae_requester_term", 0, 0, [item("merequester:requester_terminal")], "Requester Terminal", section=S_AUTO, deps=["s_requester"], xp=60,
      **OPT, subtitle="Optional: every stock rule on one screen", desc=[
        "&eWhat:&r the Requester Terminal lists every ME Requester on the network.",
        "&eHow:&r an illuminated panel, a logic processor and a Requester, shapeless (check JEI).",
        "&eTip:&r keep a stock rule for each acid: H₂SO₄, HCl and HNO₃ feed almost everything late game."]),
    Q("ae_packaged_ex", 0, 0, [item("packagedexcrafting:basic_crafter")], "Packaged Extended Crafting", section=S_AUTO, deps=["mf_packaged", "mf_crystaltine"], xp=150,
      **OPT, subtitle="Optional: autocraft on the big tables", desc=[
        "&eWhat:&r Packaged ExCrafting adds crafters that run Extended Crafting recipes from packages.",
        "&eHow:&r an auto table of the right size, an ME package component, crystaltine components, black iron and a redstone catalyst (check JEI).",
        "&eTip:&r encode the recipe in the Packaged Auto encoder, just like normal packages."]),
    Q("ae_packaged_ult", 0, 0, [item("packagedexcrafting:ultimate_crafter")], "The Ultimate Crafter", section=S_AUTO, deps=["ae_packaged_ex", "mf_ult_table"], xp=250,
      optional=True, tokens=2, subtitle="Optional: 9x9 recipes on demand", desc=[
        "&eWhat:&r the Ultimate Crafter runs 9x9 Ultimate Table recipes automatically from the network.",
        "&eHow:&r same recipe as the basic crafter, with an Ultimate Auto Table in the middle (check JEI).",
        "&eTip:&r the Seed of a New World is a 9x9 recipe. Feed it from the network and the capstone crafts itself."]),

    # ===== Matter Condenser =====================================================================
    Q("ae_condenser", 0, 0, [item("ae2:condenser"), item("ae2:matter_ball")], "Matter Condenser", section=S_COND, deps=["s_ae_cell"], xp=100,
      mirror="5BB887411B8B38FA", subtitle="Crush items into matter", desc=[
        "&eWhat:&r the Matter Condenser destroys items. With a component inside, it squeezes them into Matter Balls (or, with a 64k, a Singularity).",
        "&eHow:&r craft it (check JEI), put a component in, set the mode and feed it cobblestone from a pipe.",
        "&eTip:&r matter balls are Matter Cannon ammo; singularities unlock MEGA's press and every AdvancedAE machine."]),
    Q("ae_tiny_tnt", 0, 0, [item("ae2:singularity"), item("ae2:ender_dust"), item("ae2:tiny_tnt")], "Singularity, Dust and a Small Bang", section=S_COND,
      deps=["ae_condenser"], xp=100, mirror="3E3DF8E967D95DB0", subtitle="The ingredients of entanglement", desc=[
        "&eWhat:&r a singularity from the condenser, ender dust from the Inscriber and Tiny TNT: together they make entangled singularities.",
        "&eChemistry:&r gunpowder is potassium nitrate, charcoal and sulfur: 2KNO₃ + S + 3C → K₂S + N₂ + 3CO₂. The gases expanding all at once are the bang.",
        "&eHow:&r drop a singularity and ender dust together, then set off Tiny TNT next to them: you get a pair of Quantum Entangled Singularities.",
        "&eTip:&r set it off away from anything you care about. It is still TNT."]),
    Q("ae_quantum_ring", 0, 0, [item("ae2:quantum_ring", 16), item("ae2:quantum_link", 2), item("ae2:quantum_entangled_singularity", 2)], "Quantum Bridge",
      section=S_COND, deps=["ae_tiny_tnt"], xp=200, mirror="0B218DD73FE8D985", subtitle="Link networks across dimensions", desc=[
        "&eWhat:&r two Quantum Network Bridges joined by entangled singularities act like one cable, even across dimensions.",
        "&eHow:&r build a 3x3 ring of 8 Quantum Rings around a Quantum Link Chamber at each end, then put one of a pair of entangled singularities in each chamber.",
        "&eTip:&r both ends must be chunk-loaded. Use FTB Chunks to force-load them."]),
    Q("ae_qes", 0, 0, [item("ae2:quantum_entangled_singularity", 2)], "Spooky Action", section=S_COND, deps=["ae_tiny_tnt"], xp=100,
      secret=True, loot="secret", subtitle="Secret: two particles, one fate", desc=[
        "&6You remember being in two places at once. It felt exactly like this.&r",
        "&eWhat:&r you made a pair of Quantum Entangled Singularities by blowing up a singularity with ender dust.",
        "&eChemistry:&r real entangled particles share one quantum state: measure one and you know the other, however far apart. Sadly it can't send messages faster than light; AE2 is kinder."]),
    Q("ae_matter_cannon", 0, 0, [item("ae2:matter_cannon"), item("ae2:matter_ball", 16)], "Loaded Cannon", section=S_COND, deps=["ae_condenser"], xp=60,
      **OPT, subtitle="Optional: the heavier the atom, the harder it hits", desc=[
        "&eWhat:&r the Matter Cannon fires matter balls or metal nuggets from a cell inside it.",
        "&eChemistry:&r AE2 rates each nugget by its element's real atomic mass: iron 55.8, osmium 190.2, uranium 238. Heavier atoms carry more momentum at the same speed.",
        "&eHow:&r a condenser on Matter Ball mode makes ammo; the cannon's tooltip shows how to load it.",
        "&eTip:&r osmium and uranium nuggets are the best ammo you'll have spare."]),

    # ===== Wireless =============================================================================
    Q("ae_wap", 0, 0, [item("ae2:wireless_access_point"), item("ae2:wireless_booster")], "Wireless Access Point", section=S_WIRE, deps=["ae_controller"], xp=75,
      mirror="2B31E6C1707D8195", subtitle="Where every wireless terminal connects", desc=[
        "&eWhat:&r the Wireless Access Point sends your network a short distance through the air. Boosters raise its range.",
        "&eHow:&r a wireless receiver over a calculation processor and fluix cable; boosters from fluix dust, certus, ender dust and iron (check JEI).",
        "&eTip:&r put the access point near the middle of your base for the best coverage."]),
    Q("s_ae_wireless", 0, 0, [item("ae2:wireless_terminal"), item("ae2:wireless_crafting_terminal")], "Wireless Terminals", section=S_WIRE, deps=["ae_wap"], xp=75,
      mirror="16299B9AE87257DC", subtitle="Your network in your pocket", desc=[
        "&eWhat:&r reach your ME network from anywhere in range of a Wireless Access Point. The crafting version has a grid too.",
        "&eHow:&r check JEI. Link the terminal by putting it in the access point, and charge it in the Charger."]),
    Q("ae_infinity", 0, 0, [item("aeinfinitybooster:infinity_card"), item("aeinfinitybooster:dimension_card")], "Infinite Range", section=S_WIRE, deps=["s_ae_wireless"], xp=200,
      tokens=2, mirror="234DC1702333EB18", subtitle="No range limit, in any dimension", desc=[
        "&eWhat:&r the Infinity Booster Card removes the access point's range limit in one dimension; the Dimension Card reaches every dimension.",
        "&eHow:&r both need Nether Stars, so the Wither comes first (check JEI). The dimension card takes four infinity cards.",
        "&eTip:&r put the card in the Wireless Access Point, not the terminal, and keep that chunk loaded."]),
    Q("ae_bridge_card", 0, 0, [item("ae2wtlib:quantum_bridge_card")], "Quantum Bridge Card", section=S_WIRE, deps=["ae_quantum_ring", "s_ae_wireless"], xp=100,
      mirror="4B76FE0348DB0E45", subtitle="Your terminal, through an entangled pair", desc=[
        "&eWhat:&r this AE2 Wireless Terminals card lets a terminal reach the network through quantum entanglement, from any distance or dimension.",
        "&eHow:&r quantum rings, a Quantum Link Chamber and an advanced card (check JEI). Its tooltip explains how to pair it.",
        "&eTip:&r the network's end must stay chunk-loaded."]),
    Q("ae_wut", 0, 0, [item("ae2wtlib:wireless_universal_terminal")], "Universal Terminal", section=S_WIRE, deps=["s_ae_wireless"], xp=100,
      **OPT, subtitle="Optional: one terminal to rule them all", desc=[
        "&eWhat:&r AE2 Wireless Terminals merges the crafting, pattern access and pattern encoding terminals into one Universal Terminal.",
        "&eHow:&r combine two wireless terminals in a crafting grid (check JEI); add more by crafting them in again.",
        "&eTip:&r a Magnet Card from the same mod pulls nearby drops straight into your network."]),
    Q("ae_dimension", 0, 0, [item("aeinfinitybooster:dimension_card", 2)], "A Spare Dimension Card", section=S_WIRE, deps=["ae_infinity"], xp=100,
      **OPT, subtitle="Optional: one for every base", desc=[
        "&eWhat:&r a second Dimension Card, for a second network or an outpost's access point.",
        "&eHow:&r four Infinity Cards, four Nether Stars and an eye of ender (check JEI)."]),
    Q("ae_io_card", 0, 0, [item("ae2importexportcard:import_card"), item("ae2importexportcard:export_card")], "Import and Export Cards", section=S_WIRE, deps=["s_ae_wireless"], xp=100,
      **OPT, subtitle="Optional: your inventory, auto-sorted", desc=[
        "&eWhat:&r these cards go in a wireless terminal. The Import Card pushes chosen items from your inventory into the network; the Export Card keeps chosen items stocked in your inventory.",
        "&eHow:&r an import (or export) bus, redstone blocks, an advanced card and processors (check JEI).",
        "&eTip:&r set the Import Card to cobblestone, dirt and raw ores, and mining trips never fill your inventory."]),

    # ===== Spatial Storage ======================================================================
    Q("ae_spatial", 0, 0, [item("ae2:spatial_io_port")], "Spatial IO Port", section=S_SPACE, deps=["ae_io_port"], xp=150,
      size=1.5, shape="hexagon", mirror="01F3F0C25BA72BDA", subtitle="Cut a room out of the world", desc=[
        "&eWhat:&r the Spatial IO Port stores everything inside a frame of Spatial Pylons in a spatial cell, and can put it back elsewhere.",
        "&eHow:&r glass, an IO Port and an engineering processor (check JEI and the AE2 guide).",
        "&eTip:&r the stored room becomes a real dimension you can visit. Ask before you move someone else's base."]),
    Q("ae_spatial_pylon", 0, 0, [item("ae2:spatial_pylon")], "Spatial Pylon", section=S_SPACE, deps=["ae_spatial"], xp=60,
      mirror="18DFB25DC48D8BF7", subtitle="The frame of the box", desc=[
        "&eWhat:&r pylons outline the space to be stored, along three edges of a box.",
        "&eHow:&r fluix and quartz glass (check JEI). Each pylon row also takes a channel."]),
    Q("ae_spatial_anchor", 0, 0, [item("ae2:spatial_anchor")], "Spatial Anchor", section=S_SPACE, deps=["ae_spatial_pylon"], xp=60,
      **OPT, mirror="2897FA291E5A38D8", subtitle="Optional: keep a network's chunks loaded", desc=[
        "&eWhat:&r the Spatial Anchor keeps every chunk its network touches loaded.",
        "&eHow:&r check JEI.",
        "&eTip:&r one anchor keeps both ends of a quantum bridge alive."]),
    Q("ae_spatial_cell", 0, 0, [anyof(["ae2:spatial_storage_cell_2", "ae2:spatial_storage_cell_16", "ae2:spatial_storage_cell_128"])], "Spatial Cell", section=S_SPACE,
      deps=["ae_spatial_pylon"], xp=60, mirror="6F3D0A248B5A9CA2", subtitle="A room in a cell", desc=[
        "&eWhat:&r spatial cells hold the stored space: 2, 16 or 128 blocks to a side.",
        "&eHow:&r a spatial component in a housing (check JEI)."]),

    # ===== Chemicals and Flux (our own addons; optional) ========================================
    Q("s_appmek", 0, 0, [item("appmek:chemical_storage_cell_1k")], "Gas in the Network", section=S_CHEM, deps=["ae_item_cell"], xp=150,
      **OPT, subtitle="Optional: store Mekanism chemicals in AE2", desc=[
        "&eWhat:&r Applied Mekanistics lets AE2 store and move Mekanism chemicals: H₂, O₂, Cl₂, HCl, SO₂ and the rest.",
        "&eChemistry:&r a 1k cell holds a lot of gas because the network stores amounts, not tanks. Real gases need pressure vessels.",
        "&eHow:&r a chemical cell housing (osmium, quartz glass, redstone) + a 1k component. Import buses on chemical tanks fill it.",
        "&eTip:&r processing patterns can pull stored SO₂ and O₂ straight from the cell to feed your sulfuric acid line."]),
    Q("ae_appmek_big", 0, 0, [item("appmek:chemical_storage_cell_64k")], "A Tank Farm in a Cell", section=S_CHEM, deps=["s_appmek"], xp=100,
      **OPT, subtitle="Optional: 64k of chemicals", desc=[
        "&eWhat:&r a 64k chemical cell replaces a room full of chemical tanks.",
        "&eChemistry:&r one mole of any ideal gas fills about 22.4 L at 0 °C and 1 atm. Stored as data, it fills nothing at all.",
        "&eHow:&r chemical housing plus a 64k component (check JEI)."]),
    Q("ae_radioactive", 0, 0, [item("megacells:radioactive_chemical_cell")], "Shielded Storage", section=S_CHEM, deps=["ae_appmek_big", "t6_fission"], xp=150,
      optional=True, tokens=2, subtitle="Optional: a cell for hot chemicals", desc=[
        "&eWhat:&r normal chemical cells refuse radioactive chemicals. MEGA's Radioactive Chemical Cell holds one, like nuclear waste or plutonium.",
        "&eChemistry:&r spent fuel stays dangerous because unstable nuclei keep decaying, giving off α, β and γ radiation for years.",
        "&eHow:&r check JEI for the radioactive component and cell."]),
    Q("s_appflux", 0, 0, [item("appflux:charged_redstone", 4), item("appflux:fe_1k_cell")], "Energy in a Cell", section=S_CHEM, deps=["ae_item_cell"], xp=150,
      **OPT, subtitle="Optional: Applied Flux stores FE in AE2", desc=[
        "&eWhat:&r Applied Flux stores FE in AE2 cells and moves it through the network with Flux Accessors.",
        "&eHow:&r redstone crystal (redstone block, fluix and glowstone dropped in water) → charge it in the Charger → FE cell core and housing (check JEI).",
        "&eTip:&r the housing needs insulating resin, which needs silicon: a little chemistry even here."]),
    Q("ae_flux_accessor", 0, 0, [item("appflux:flux_accessor"), item("appflux:induction_card")], "Flux Accessor", section=S_CHEM, deps=["s_appflux"], xp=100,
      **OPT, subtitle="Optional: power machines from the network", desc=[
        "&eWhat:&r a Flux Accessor pushes FE from your FE cells into any machine it touches. An Induction Card lets an I/O bus or interface do the same.",
        "&eHow:&r an energy acceptor, energy processors, copper and glowstone (check JEI).",
        "&eTip:&r one FE cell plus accessors can replace a tangle of power cables."]),
], links=[("t5_hv", 0, 0), ("t5_ae2", 0, 0), ("mf_packaged", 0, 0)], mirror="applied_energistics_2")
