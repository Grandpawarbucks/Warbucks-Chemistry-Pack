"""Quest chapter: ae2 (Applied Energistics 2 and its addons). See tools/quests/STYLE.md.

The s_ae_* / s_exae / s_mega / s_appmek / s_appflux / s_requester quests moved here from storage.py
(keys unchanged, so player progress is kept).
Layout: y=-2 power and infrastructure, y=0 core network, y=2 wireless, y=4 ExtendedAE, y=6 MEGA Cells,
y=9 chemicals and energy in cells, y=11 AdvancedAE, y=13 cards and packaged crafting.
Gate: AE2 opens at t5_ae2 (the Inscriber needs an MI Turbo hull, the Controller a digital circuit).
"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

CHAPTER = Chapter("ae2", "Applied Energistics", "ae2:controller",
        ["The archive of a god: every item as data, every recipe on demand."], SIDE, [
    # --- Power and infrastructure (y=-2) -------------------------------------------------------
    Q("ae_energy", 0, -2, [item("ae2:energy_acceptor"), item("ae2:energy_cell")], "Feeding the Network", deps=["s_ae_drive"], xp=75,
      subtitle="AE2 runs on its own energy, fed by FE", desc=[
        "&eWhat:&r the ME network turns FE into its own AE energy. The Energy Acceptor converts it; Energy Cells buffer it.",
        "&eHow:&r connect an Energy Acceptor to any FE source (an energy cube, a Powah cell, a Flux Point) and to your cables. Add an Energy Cell next to the controller (check JEI).",
        "&eTip:&r a big autocraft can drain the network fast. A Dense Energy Cell keeps it from browning out mid-job."]),
    Q("ae_growth", 1, -3.5, [item("ae2:growth_accelerator", 2)], "Growing Certus", deps=["s_ae_drive"], xp=60,
      optional=True, tokens=1, subtitle="Optional: crystal farms at full speed", desc=[
        "&eWhat:&r Growth Accelerators speed up certus quartz buds growing on budding certus blocks.",
        "&eChemistry:&r real quartz (SiO₂) crystals grow from silica-rich water over thousands of years. Certus is fictional, but the idea of a seed crystal pulling dissolved material out of solution is real.",
        "&eHow:&r iron, fluix glass cable, quartz glass and a fluix block (check JEI). Place them touching budding certus and power them.",
        "&eTip:&r flawless budding certus never decays. Find it in meteorites and never break it with a normal pickaxe."]),
    Q("ae_p2p", 2, -2, [item("ae2:me_p2p_tunnel", 2)], "P2P Tunnels", deps=["ae_channels"], xp=60,
      optional=True, tokens=1, subtitle="Optional: one cable, many channels", desc=[
        "&eWhat:&r a pair of P2P tunnels carries 32 channels (or items, fluids, FE and redstone) through a single dense cable.",
        "&eHow:&r place both tunnels, then copy the input's settings to the output with a Memory Card (check JEI).",
        "&eTip:&r right-click a P2P tunnel with a bucket, a redstone dust or an FE item to change what it carries."]),
    Q("ae_condenser", 4, -2, [item("ae2:condenser"), item("ae2:singularity")], "The Matter Condenser", deps=["ae_energy"], xp=150,
      subtitle="Crush a quarter-million items into a point", desc=[
        "&eWhat:&r the Matter Condenser destroys items. With a 64k component inside, it squeezes them into Matter Balls or a Singularity.",
        "&eHow:&r craft it (check JEI), put a storage component in it, set it to Singularity and feed it cobblestone from a pipe. It takes a lot of items.",
        "&eTip:&r singularities unlock MEGA Cells' accumulation processor and every AdvancedAE machine, so start a cobblestone generator early."]),
    Q("ae_quantum_ring", 6, -2, [item("ae2:quantum_ring", 8), item("ae2:quantum_link")], "Quantum Bridge", deps=["ae_condenser", "ae_p2p"], xp=150,
      optional=True, tokens=2, subtitle="Optional: link networks across dimensions", desc=[
        "&eWhat:&r two Quantum Network Bridges joined by entangled singularities act like one cable, even across dimensions.",
        "&eHow:&r build a 3x3 ring of 8 Quantum Rings around a Quantum Link Chamber at each end, then put one of a pair of entangled singularities in each chamber.",
        "&eTip:&r both ends must be chunk-loaded. Use FTB Chunks to force-load them."]),
    Q("ae_qes", 5, -3.5, [item("ae2:quantum_entangled_singularity", 2)], "Spooky Action", deps=["ae_condenser"], xp=100,
      secret=True, loot="secret", subtitle="Secret: two particles, one fate", desc=[
        "&6You remember being in two places at once. It felt exactly like this.&r",
        "&eWhat:&r you made a pair of Quantum Entangled Singularities by blowing up a singularity with ender pearl dust.",
        "&eChemistry:&r real entangled particles share one quantum state: measure one and you know the other, however far apart. Sadly it can't send messages faster than light; AE2 is kinder."]),

    # --- Core network (y=0) --------------------------------------------------------------------
    Q("s_ae_drive", 0, 0, [item("ae2:drive"), item("ae2:terminal")], "AE2 Storage", deps=["t5_ae2"], xp=150,
      subtitle="Drives, terminals and the god's archive", desc=[
        "&6You remember a mind that held every name of every thing. The archive is waking.&r",
        "&eWhat:&r ME Drives hold storage cells; terminals let you see and search everything.",
        "&eHow:&r connect the drive and a terminal to your ME Controller with cables (check JEI).",
        "&eTip:&r keep power stable: an Energy Cell buffers the network."]),
    Q("ae_channels", 2, 0, [item("ae2:fluix_smart_cable", 16), item("ae2:fluix_covered_dense_cable", 4)], "Cables and Channels", deps=["s_ae_drive"], xp=75,
      subtitle="Every device needs a channel", desc=[
        "&eWhat:&r each ME device uses one channel. Normal cables carry 8 channels, dense cables 32. The controller sends 32 out of each face.",
        "&eHow:&r craft fluix cables, then smart cables (they show channel use as lines) and dense cables (check JEI).",
        "&eTip:&r build a dense-cable backbone from the controller and branch normal cables off it. Smart cables show you where channels run out.",
        "{@pagebreak}",
        "&eDeep dive:&r if a device's light is off, it has no channel. Count devices on each normal cable (max 8). Drives, terminals, buses and interfaces all count. Plain cables, quartz fibre and energy cells don't.",
        "&eHow:&r the Network Tool (check JEI) shows the channel count of any cable when you right-click it."]),
    Q("s_ae_cell", 4, 0, [item("ae2:cell_component_1k", 2), item("ae2:item_storage_cell_1k")], "Storage Cells", deps=["s_ae_drive"], xp=75,
      subtitle="Bytes for your items", desc=[
        "&eWhat:&r cells are where the network actually stores things. Bigger components (4k, 16k, 64k, 256k) hold more.",
        "&eChemistry:&r certus and fluix are fictional, but the logic processors behind them echo real chips: doped silicon (Si).",
        "&eHow:&r craft components from processors and certus quartz, then put one in a cell housing (check JEI)."]),
    Q("ae_cell_tiers", 6, 0, [item("ae2:cell_component_16k"), item("ae2:cell_component_64k")], "Bigger Components", deps=["s_ae_cell"], xp=100,
      subtitle="16k and 64k: room for whole chemical stocks", desc=[
        "&eWhat:&r each tier combines three of the last with a calculation processor and quartz glass, holding four times as many bytes.",
        "&eHow:&r 4k from 1k, 16k from 4k, 64k from 16k (check JEI). Put them in housings, or into the Matter Condenser.",
        "&eTip:&r a cell holds up to 63 different item types whatever its size, so use small cells for many odd items and big cells for bulk ores and dusts."]),
    Q("s_ae_craft", 8, 0, [item("ae2:crafting_terminal")], "Autocrafting", deps=["s_ae_cell"], xp=150,
      subtitle="Whole chemical chains in one click", desc=[
        "&eWhat:&r pattern providers plus molecular assemblers turn whole chemical chains into one click.",
        "&eHow:&r a Crafting Terminal, some crafting storage, and patterns encoded in a Pattern Encoding Terminal (check JEI).",
        "&eTip:&r processing patterns can drive MI machines too: send the inputs, wait for the outputs. The Automation and Logic page walks through a full sulfuric acid line."]),

    # --- Wireless (y=2) ------------------------------------------------------------------------
    Q("s_ae_wireless", 0, 2, [item("ae2:wireless_crafting_terminal")], "Wireless Access", deps=["s_ae_drive"], xp=75,
      optional=True, tokens=1, subtitle="Optional: your network in your pocket", desc=[
        "&eWhat:&r reach your ME network from anywhere in range of a Wireless Access Point.",
        "&eHow:&r check JEI. Link the terminal by putting it in the access point, and charge it in the Charger.",
        "&eTip:&r put the access point near the middle of your base for the best coverage."]),
    Q("ae_wut", 2, 2, [item("ae2wtlib:wireless_universal_terminal")], "Universal Terminal", deps=["s_ae_wireless"], xp=100,
      optional=True, tokens=1, subtitle="Optional: one terminal to rule them all", desc=[
        "&eWhat:&r AE2 Wireless Terminals merges the crafting, pattern access and pattern encoding terminals into one Universal Terminal.",
        "&eHow:&r combine two wireless terminals in a crafting grid (check JEI); add more by crafting them in again.",
        "&eTip:&r a Magnet Card from the same mod pulls nearby drops straight into your network. A Quantum Bridge Card works across dimensions."]),
    Q("ae_infinity", 4, 2, [item("aeinfinitybooster:infinity_card")], "Infinite Range", deps=["s_ae_wireless", "t2_nether"], xp=150,
      optional=True, tokens=2, subtitle="Optional: no more range limit", desc=[
        "&eWhat:&r the Infinity Booster Card removes the Wireless Access Point's range limit within one dimension.",
        "&eHow:&r a Nether Star, wireless boosters, eyes of ender and netherite ingots (check JEI). The star means fighting the Wither first.",
        "&eTip:&r put it in the Wireless Access Point, not the terminal."]),
    Q("ae_dimension", 6, 2, [item("aeinfinitybooster:dimension_card")], "Across Worlds", deps=["ae_infinity"], xp=200,
      optional=True, tokens=2, subtitle="Optional: your archive in every dimension", desc=[
        "&eWhat:&r the Dimension Card lets a Wireless Access Point reach you in any dimension: the Nether, the Twilight Forest, the Moon.",
        "&eHow:&r four Infinity Cards, four Nether Stars and an eye of ender (check JEI).",
        "&eTip:&r the access point's chunk must stay loaded while you're away."]),
    Q("s_requester", 8, 2, [item("merequester:requester")], "ME Requester", deps=["s_ae_craft"], xp=75,
      optional=True, tokens=1, subtitle="Optional: keep stock topped up", desc=[
        "&eWhat:&r the ME Requester keeps a set amount of an item in stock by ordering crafts automatically.",
        "&eHow:&r check JEI. Set \"keep 64 HDPE\" and it never runs out.",
        "&eTip:&r it needs autocrafting patterns for whatever it keeps in stock."]),
    Q("ae_requester_term", 10, 2, [item("merequester:requester_terminal")], "Requester Terminal", deps=["s_requester"], xp=60,
      optional=True, tokens=1, subtitle="Optional: every stock rule on one screen", desc=[
        "&eWhat:&r the Requester Terminal lists every ME Requester on the network, so you can edit all your stock rules from one place.",
        "&eHow:&r an illuminated panel, a logic processor and a Requester, shapeless (check JEI).",
        "&eTip:&r keep a stock rule for each acid and solvent: H₂SO₄, HCl and HNO₃ are inputs to almost everything late game."]),

    # --- ExtendedAE (y=4) ----------------------------------------------------------------------
    Q("ae_entro", 0, 4, [item("extendedae:entro_seed"), item("extendedae:entro_crystal", 8)], "Entro Crystals", deps=["s_ae_craft"], xp=100,
      subtitle="ExtendedAE's own budding crystal", desc=[
        "&eWhat:&r entro crystals feed every ExtendedAE machine. They grow like certus, from Budding Entroized Fluix.",
        "&eHow:&r craft Entro Seeds (sand, ender dust, redstone, glowstone, sky dust), then right-click a placed Fluix Block with a seed to make it budding. Harvest the clusters.",
        "&eTip:&r Growth Accelerators work on budding entro too."]),
    Q("ae_crystal_assembler", 2, 4, [item("extendedae:machine_frame"), item("extendedae:crystal_assembler")], "Crystal Assembler", deps=["ae_entro"], xp=150,
      subtitle="A crafting machine for AE2 parts", desc=[
        "&eWhat:&r the Crystal Assembler makes ExtendedAE's blocks from several items (and sometimes a fluid) at once.",
        "&eHow:&r crush entro to dust in the Inscriber, drop it in water with a gold ingot and lapis for an entro ingot, then build a Machine Frame and the Assembler (check JEI).",
        "&eTip:&r it accepts pipes and patterns, so the network can drive it like any other machine."]),
    Q("s_exae", 4, 4, [item("extendedae:ex_pattern_provider"), item("extendedae:ex_drive")], "ExtendedAE", deps=["s_ae_craft", "ae_crystal_assembler"], xp=150,
      subtitle="Bigger providers and drives", desc=[
        "&eWhat:&r ExtendedAE adds larger versions of AE2 blocks: the Extended Pattern Provider holds many more patterns, the Extended Drive many more cells.",
        "&eHow:&r made in the Crystal Assembler from the normal blocks plus concurrent processors (check JEI).",
        "&eTip:&r one extended provider can feed a whole row of chemical reactors."]),
    Q("ae_wireless_connector", 6, 4, [item("extendedae:wireless_connect", 2)], "Wireless Connectors", deps=["s_exae"], xp=75,
      optional=True, tokens=1, subtitle="Optional: cables through thin air", desc=[
        "&eWhat:&r a pair of Wireless Connectors links two parts of your network without a cable between them.",
        "&eHow:&r made two at a time in the Crystal Assembler. Bind them with the Wireless Setup Kit (check JEI).",
        "&eTip:&r great for reaching a reactor room behind thick shielding."]),
    Q("ae_assembler_matrix", 8, 4, [item("extendedae:assembler_matrix_frame", 8), item("extendedae:assembler_matrix_crafter"), item("extendedae:assembler_matrix_pattern")], "Assembler Matrix", deps=["s_exae"], xp=200,
      optional=True, tokens=2, subtitle="Optional: one multiblock, thousands of crafts", desc=[
        "&eWhat:&r the Assembler Matrix is a multiblock that replaces walls of molecular assemblers: crafter blocks do the work, pattern blocks hold the patterns.",
        "&eHow:&r build a hollow box of frames and walls (or glass), with crafter, pattern and speed cores inside (check JEI for the rules).",
        "&eTip:&r it's for crafting-table recipes only. Processing patterns for MI machines still need pattern providers."]),

    # --- MEGA Cells (y=6) ----------------------------------------------------------------------
    Q("s_mega", 0, 6, [item("megacells:sky_steel_ingot", 4), item("megacells:item_storage_cell_1m")], "MEGA Cells", deps=["s_ae_cell"], xp=200,
      subtitle="Sky steel and million-byte cells", desc=[
        "&eWhat:&r MEGA Cells adds 1M to 256M cells, bulk cells and bigger crafting storage.",
        "&eChemistry:&r sky steel is made by dropping charged certus, iron and sky stone into lava: heat drives the alloying, like a tiny smelter.",
        "&eHow:&r throw the ingredients into a lava pool for sky steel, then build the 1M component (check JEI)."]),
    Q("ae_sky_alloys", 1, 7.5, [item("megacells:sky_bronze_ingot", 4), item("megacells:sky_osmium_ingot", 4)], "Sky Bronze and Sky Osmium", deps=["s_mega"], xp=75,
      optional=True, tokens=1, subtitle="Optional: more lava alloys", desc=[
        "&eWhat:&r the same lava trick with copper gives sky bronze, and with osmium gives sky osmium. Both go into MEGA's larger parts.",
        "&eChemistry:&r bronze is really copper plus tin (Cu + Sn); here the sky stone plays the tin. Osmium (Os) is the densest natural element, 22.6 g/cm³.",
        "&eHow:&r drop charged certus, the ingot and a sky stone block into lava together. Each throw makes two ingots."]),
    Q("ae_accumulation", 2, 6, [item("megacells:accumulation_processor", 4)], "Accumulation Processors", deps=["s_mega", "ae_condenser"], xp=150,
      subtitle="A press made from a singularity", desc=[
        "&eWhat:&r the accumulation processor is MEGA's fourth processor, needed for every 1M+ part.",
        "&eHow:&r inscribe a singularity between the calculation and engineering presses to make the Accumulation Press, then print sky steel with it (check JEI).",
        "&eTip:&r keep the press. The Inscriber can copy it with an iron block, like the other presses."]),
    Q("ae_mega_crafting", 4, 6, [item("megacells:1m_crafting_storage"), item("megacells:mega_crafting_unit", 4)], "MEGA Crafting CPU", deps=["ae_accumulation"], xp=150,
      subtitle="Room for the biggest crafting jobs", desc=[
        "&eWhat:&r MEGA crafting storage and units build a separate, much larger crafting CPU.",
        "&eHow:&r check JEI. MEGA blocks only join other MEGA blocks, so build it as its own multiblock.",
        "&eTip:&r the Seed of a New World chain is huge. One big CPU saves splitting the job by hand."]),
    Q("ae_mega_provider", 6, 6, [item("megacells:mega_pattern_provider")], "MEGA Pattern Provider", deps=["ae_mega_crafting"], xp=100,
      optional=True, tokens=1, subtitle="Optional: room for many more patterns", desc=[
        "&eWhat:&r a pattern provider with many more pattern slots than the normal one.",
        "&eHow:&r made as a cable part and turned into a block in the crafting grid (check JEI).",
        "&eTip:&r put one on each multi-input MI machine, like the Chemical Reactor or the Large Diesel Generator's fuel line."]),
    Q("ae_bulk", 8, 6, [item("megacells:bulk_item_cell"), item("megacells:compression_card")], "Bulk Cells", deps=["ae_mega_crafting"], xp=150,
      optional=True, tokens=2, subtitle="Optional: one item, practically no limit", desc=[
        "&eWhat:&r a Bulk Item Cell holds a single item type in near-unlimited amounts. The Compression Card stores nuggets, ingots and blocks as one pool.",
        "&eHow:&r the bulk component needs a 1M component and accumulation processors; the card is an advanced card plus a matter ball (check JEI).",
        "&eTip:&r perfect for cobblestone (condenser feed), salt dust or coal coke."]),

    # --- Chemicals and energy in cells (y=9) ---------------------------------------------------
    Q("s_appmek", 0, 9, [item("appmek:chemical_storage_cell_1k")], "Gas in the Network", deps=["s_ae_cell", "t4_mv"], xp=150,
      subtitle="Store Mekanism chemicals in AE2", desc=[
        "&eWhat:&r Applied Mekanistics lets AE2 store and move Mekanism chemicals: H₂, O₂, Cl₂, HCl, SO₂ and the rest.",
        "&eChemistry:&r a 1k cell holds a lot of gas because the network stores amounts, not tanks. Real gases need pressure vessels.",
        "&eHow:&r a chemical cell housing (osmium, quartz glass, redstone) + a 1k component. Import buses on chemical tanks fill it.",
        "&eTip:&r processing patterns can pull stored SO₂ and O₂ straight from the cell to feed your sulfuric acid line."]),
    Q("ae_appmek_big", 2, 9, [item("appmek:chemical_storage_cell_64k")], "A Tank Farm in a Cell", deps=["s_appmek", "ae_cell_tiers"], xp=100,
      optional=True, tokens=1, subtitle="Optional: 64k of chemicals", desc=[
        "&eWhat:&r a 64k chemical cell replaces a room full of chemical tanks.",
        "&eChemistry:&r one mole of any ideal gas fills about 22.4 L at 0 °C and 1 atm. Stored as data, it fills nothing at all.",
        "&eHow:&r chemical housing plus a 64k component, or upgrade a smaller cell in the crafting grid (check JEI)."]),
    Q("ae_radioactive", 4, 9, [item("megacells:radioactive_chemical_cell")], "Shielded Storage", deps=["ae_appmek_big", "s_mega", "t6_fission"], xp=150,
      optional=True, tokens=2, subtitle="Optional: a cell for hot chemicals", desc=[
        "&eWhat:&r normal chemical cells refuse radioactive chemicals. MEGA's Radioactive Chemical Cell holds one, like nuclear waste or plutonium.",
        "&eChemistry:&r spent fuel stays dangerous because unstable nuclei keep decaying, giving off α, β and γ radiation for years.",
        "&eHow:&r check JEI for the radioactive component and cell.",
        "&eTip:&r a cell never leaks, unlike a broken tank. It's the safest place to keep waste before you reprocess it."]),
    Q("s_appflux", 6, 9, [item("appflux:charged_redstone", 4), item("appflux:fe_1k_cell")], "Energy in a Cell", deps=["s_ae_cell"], xp=150,
      subtitle="Applied Flux stores FE in AE2", desc=[
        "&eWhat:&r Applied Flux stores FE in AE2 cells and moves it through the network with Flux Accessors.",
        "&eHow:&r redstone crystal (redstone block, fluix and glowstone dropped in water) → charge it in the AE2 Charger → FE cell core and housing (check JEI).",
        "&eTip:&r the housing needs insulating resin, which needs silicon: a little chemistry even here."]),
    Q("ae_flux_accessor", 8, 9, [item("appflux:flux_accessor"), item("appflux:induction_card")], "Flux Accessor", deps=["s_appflux"], xp=100,
      subtitle="Power machines from the network", desc=[
        "&eWhat:&r a Flux Accessor pushes FE from your FE cells into any machine it touches. An Induction Card lets an I/O bus or interface do the same.",
        "&eHow:&r an energy acceptor, energy processors (iron block charged into the Energy Press, then inscribed), copper and glowstone (check JEI).",
        "&eTip:&r one FE cell plus accessors can replace a tangle of power cables around a dense machine room."]),

    # --- AdvancedAE (y=11) ---------------------------------------------------------------------
    Q("ae_reaction", 0, 11, [item("advanced_ae:reaction_chamber"), item("advanced_ae:shattered_singularity", 2)], "Reaction Chamber", deps=["ae_condenser"], xp=150,
      subtitle="AdvancedAE's powered reactor", desc=[
        "&eWhat:&r AdvancedAE's Reaction Chamber combines items and a fluid with lots of energy. Its first job: shattering singularities.",
        "&eHow:&r a matter condenser, a vibration chamber, fluix dust, glowstone and a bucket (check JEI). Feed it a singularity, ender dust, sky dust and lava.",
        "&eTip:&r it uses a lot of power per craft. Put it on its own Energy Acceptor."]),
    Q("ae_quantum_alloy", 2, 11, [item("advanced_ae:quantum_alloy", 4)], "Quantum Alloy", deps=["ae_reaction"], xp=200,
      subtitle="Copper, singularities and quantum infusion", desc=[
        "&eWhat:&r quantum alloy is AdvancedAE's top material, for the quantum computer and gear.",
        "&eHow:&r press a shattered singularity into quantum-infused dust, react it with water into Quantum Infusion, then react that with copper ingots, singularities and shattered singularities (check JEI).",
        "&eChemistry:&r copper (Cu) is the base for a reason: after silver it's the best electrical conductor of any metal."]),
    Q("ae_adv_provider", 4, 11, [item("advanced_ae:adv_pattern_provider")], "Directional Providers", deps=["s_exae"], xp=100,
      subtitle="Send each ingredient to the right face", desc=[
        "&eWhat:&r the Advanced Pattern Provider lets a processing pattern send each input to a chosen side of the machine.",
        "&eHow:&r an Extended Pattern Provider, a logic processor, an ender pearl and redstone (check JEI). Encode patterns in the Advanced Pattern Encoder.",
        "&eTip:&r ideal for machines with separate input faces, like a Mekanism machine that takes gas on one side and items on another."]),
    Q("ae_quantum_computer", 6, 11, [item("advanced_ae:quantum_core"), item("advanced_ae:quantum_structure", 8), item("advanced_ae:quantum_multi_threader")], "Quantum Computer", deps=["ae_quantum_alloy", "ae_mega_crafting"], xp=300,
      optional=True, tokens=2, subtitle="Optional: the archive learns to think", desc=[
        "&6You remember thinking a thousand thoughts at once. The machine remembers how, too.&r",
        "&eWhat:&r the Quantum Computer is a multiblock crafting CPU: huge storage, many parallel jobs, and accelerators that multiply speed.",
        "&eHow:&r a Quantum Core inside a shell of Quantum Structure blocks, with multi-threaders, accelerators and storage blocks (check JEI for size limits).",
        "&eTip:&r build it next to your main pattern providers so every chemical line can run at once."]),

    # --- Cards and packaged crafting (y=13) ----------------------------------------------------
    Q("ae_io_card", 0, 13, [item("ae2importexportcard:import_card"), item("ae2importexportcard:export_card")], "Import and Export Cards", deps=["s_ae_wireless"], xp=100,
      optional=True, tokens=1, subtitle="Optional: your inventory, auto-sorted", desc=[
        "&eWhat:&r these cards go in a wireless terminal. The Import Card pushes chosen items from your inventory into the network; the Export Card keeps chosen items stocked in your inventory.",
        "&eHow:&r an import (or export) bus, redstone blocks, an advanced card and processors (check JEI).",
        "&eTip:&r set the Import Card to cobblestone, dirt and raw ores, and mining trips never fill your inventory."]),
    Q("ae_packaged_ex", 2, 13, [item("packagedexcrafting:basic_crafter")], "Packaged Extended Crafting", deps=["mf_packaged", "mf_crystaltine"], xp=150,
      optional=True, tokens=1, subtitle="Optional: autocraft on the big tables", desc=[
        "&eWhat:&r Packaged ExCrafting adds crafters that run Extended Crafting recipes from packages: one for each table size, plus combination and ender crafting.",
        "&eHow:&r an auto table of the right size, an ME package component, crystaltine components, black iron and a redstone catalyst (check JEI).",
        "&eTip:&r encode the recipe in the Packaged Auto encoder, just like normal packages."]),
    Q("ae_packaged_ult", 4, 13, [item("packagedexcrafting:ultimate_crafter")], "The Ultimate Crafter", deps=["ae_packaged_ex", "mf_ult_table"], xp=250,
      optional=True, tokens=2, subtitle="Optional: 9x9 recipes on demand", desc=[
        "&eWhat:&r the Ultimate Crafter runs 9x9 Ultimate Table recipes automatically from the network.",
        "&eHow:&r same recipe as the basic crafter, with an Ultimate Auto Table in the middle (check JEI).",
        "&eTip:&r the Seed of a New World is a 9x9 recipe. Feed it from the network and the capstone crafts itself once its ingredients exist."]),
], links=[("t5_ae2", -2, 0), ("t5_cells", -2, 2), ("lg_patterns", 10, 0), ("mf_packaged", -2, 13), ("t4_mv", -2, 9)])
