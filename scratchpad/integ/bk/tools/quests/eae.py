"""Quest chapter: eae (ExtendedAE and AdvancedAE). See tools/quests/STYLE.md.

Mirror of ATM10's "Extended & Advanced AE" chapter (user decision 2026-10-20: quest for quest where we have the mod;
the same items, counts, order, sections and sizes). Every quest with mirror="<id>" sits where that ATM10 quest
sits; all text is ours. The ae_* quests moved here from ae2.py (keys unchanged, so player progress is kept); new
quests use the eae_ prefix.
Skipped ATM10 quests: the Flight Card and Flight Drift Card (flight in this pack comes from chemistry; the AdvancedAE
Flight Card is an open review item), and the Mystical Agriculture entro seeds / entro bee (not in this pack). ATM10's
KubeJS-only infinity cells are left out of the infinity-cell quest; ExtendedAE's own water and cobblestone cells stay.
Entry: the page opens from ae_fluix (Applied Energistics page).
"""
from questlib import Q, Chapter, item, dim, tick, anytag, anyof, MAIN, SIDE  # noqa: F401

S_ENTRO, S_EXT, S_MATRIX = "Entro", "ExtendedAE Machines", "Assembler Matrix"
S_ADV, S_QC, S_ARMOR = "AdvancedAE", "Quantum Computer", "Quantum Armour"
OPT = dict(optional=True, tokens=1)


def card(key, mirror, card_id, title, sub, what, deps=("ae_quantum_base_card",), tip=None):
    """One Quantum Armour card quest (all share the same shape: base card plus a few items)."""
    desc = ["&eWhat:&r " + what,
            "&eHow:&r a Quantum Upgrade Base plus a few items (check JEI). Install it in a quantum armour piece's GUI."]
    if tip:
        desc.append("&eTip:&r " + tip)
    return Q(key, 0, 0, [item(card_id)], title, section=S_ARMOR, deps=list(deps), xp=40, mirror=mirror, subtitle=sub, desc=desc)


CHAPTER = Chapter("eae", "Extended and Advanced AE", "extendedae:ex_pattern_provider",
        ["Bigger providers, faster crafters, and a computer that thinks in parallel."], SIDE, [
    # ===== Entro ================================================================================
    Q("eae_fluix", 0, 0, [item("ae2:fluix_crystal")], "Beyond the Basics", section=S_ENTRO, deps=["ae_fluix"], xp=50,
      size=2.0, shape="gear", mirror="3972EE0ECB215843", subtitle="Two addons that grow AE2 up", desc=[
        "&6You remember the archive was never big enough. It can grow.&r",
        "&eWhat:&r ExtendedAE adds bigger versions of AE2's blocks and a new crystal, entro. AdvancedAE adds a reaction chamber, quantum alloy and a multiblock crafting computer.",
        "&eHow:&r any fluix crystal opens this page. Both halves start from it.",
        "&eTip:&r the Assembler Matrix and the Quantum Computer are the two big builds here; everything else feeds them."]),
    Q("eae_tip", 0, 0, [tick()], "Note: Two Mods, One Page", section=S_ENTRO, deps=["eae_fluix"], xp=10, icon="extendedae:entro_crystal",
      **OPT, mirror="1A815711703E4A24", subtitle="Which half is which", desc=[
        "&eWhat:&r the top half of this page is ExtendedAE (entro, the Crystal Assembler, extended blocks). The bottom half is AdvancedAE (the Reaction Chamber and everything quantum).",
        "&eTip:&r ExtendedAE changes a few AdvancedAE recipes to use its own parts, so check JEI rather than an online wiki."]),
    Q("eae_fluix_block", 0, 0, [item("ae2:fluix_block")], "Fluix Block", section=S_ENTRO, deps=["eae_fluix"], xp=30,
      size=1.5, shape="hexagon", mirror="4818C8387C0DBBE7", subtitle="The soil entro grows in", desc=[
        "&eWhat:&r four fluix crystals make a fluix block. Planted with an entro seed, it becomes budding entro.",
        "&eHow:&r four fluix crystals in a square (check JEI)."]),
    Q("ae_entro", 0, 0, [item("extendedae:entro_seed"), item("extendedae:entro_crystal")], "Entro Crystals", section=S_ENTRO, deps=["eae_fluix_block"], xp=100,
      mirror="34FBD04361657724", subtitle="ExtendedAE's own budding crystal", desc=[
        "&eWhat:&r entro crystals feed every ExtendedAE machine. They grow like certus, from Budding Entroized Fluix.",
        "&eHow:&r craft Entro Seeds (sand, ender dust, redstone, glowstone, sky dust), then right-click a placed Fluix Block with a seed to make it budding. Harvest the clusters.",
        "&eTip:&r Growth Accelerators work on budding entro too."]),
    Q("eae_tip_cells", 0, 0, [tick()], "Note: Cells That Aren't Storage", section=S_ENTRO, deps=["eae_fluix_block"], xp=10, icon="extendedae:void_cell",
      mirror="1E535784A9D3DE89", subtitle="Some cells delete, some never run dry", desc=[
        "&eWhat:&r ExtendedAE has cells that don't store anything: one that destroys what it's sent, and ones that supply water or cobblestone without end.",
        "&eHow:&r both go in an ordinary ME Drive. Click to continue."]),
    Q("ae_void_cell", 0, 0, [item("extendedae:void_cell")], "ME Void Cell", section=S_ENTRO, deps=["eae_tip_cells"], xp=60,
      mirror="3621155A4138EBCA", subtitle="Trash, matter balls or singularities", desc=[
        "&eWhat:&r a cell that destroys what you send it. Its modes delete items, turn them into Matter Balls, or compress them into Singularities.",
        "&eChemistry:&r in the real world matter is never destroyed in a chemical reaction; it only rearranges. This cell ignores that law.",
        "&eHow:&r check JEI. Partition it to cobblestone in a Cell Workbench and put it in a drive.",
        "&eTip:&r on Singularity mode it replaces the Matter Condenser for AdvancedAE and MEGA's singularity needs."]),
    Q("eae_infinity_cell", 0, 0, [anyof(["extendedae:infinity_water_cell", "extendedae:infinity_cobblestone_cell"])], "Infinity Cell", section=S_ENTRO,
      deps=["eae_tip_cells"], xp=75, mirror="36FB694262102CFD", subtitle="Water or cobblestone, forever", desc=[
        "&eWhat:&r an infinity cell reports an endless stock of water or cobblestone to the network. Either one counts.",
        "&eChemistry:&r water (H₂O) is the most-used solvent in this pack: electrolysis, the Bayer process, acid dilution. Never running out of it is a quiet luxury.",
        "&eHow:&r check JEI. Put it in a drive; autocrafting pulls from it like any cell."]),

    # ===== ExtendedAE Machines ==================================================================
    Q("ae_crystal_assembler", 0, 0, [item("extendedae:crystal_assembler")], "Crystal Assembler", section=S_EXT, deps=["ae_entro"], xp=150,
      size=1.5, shape="hexagon", mirror="1B90B94D07BBDD09", subtitle="A crafting machine for AE2 parts", desc=[
        "&eWhat:&r the Crystal Assembler makes ExtendedAE's blocks from several items (and sometimes a fluid) at once.",
        "&eHow:&r crush entro to dust in the Inscriber, drop it in water with a gold ingot and lapis for an entro ingot, then build a Machine Frame and the Assembler (check JEI).",
        "&eTip:&r it accepts pipes and patterns, so the network can drive it like any other machine."]),
    Q("s_exae", 0, 0, [anyof(["extendedae:ex_import_bus_part", "extendedae:ex_export_bus_part", "extendedae:ex_charger", "extendedae:ex_inscriber",
                              "extendedae:ex_molecular_assembler", "extendedae:ex_drive", "extendedae:ex_io_port", "extendedae:ex_interface",
                              "extendedae:ex_pattern_provider"])], "Extended Blocks", section=S_EXT, deps=["ae_crystal_assembler"], xp=100,
      mirror="3FE739EA7E297DF3", subtitle="Any one bigger version of an AE2 block", desc=[
        "&eWhat:&r ExtendedAE's 'Ex' blocks are larger versions of AE2's: the Extended Pattern Provider holds many more patterns, the Extended Drive many more cells, and so on.",
        "&eHow:&r made in the Crystal Assembler from the normal block plus concurrent processors (check JEI). Any one of them counts.",
        "&eTip:&r one extended provider can feed a whole row of chemical reactors."]),
    Q("ae_ex_pat", 0, 0, [item("extendedae:ex_pattern_access_part")], "Extended Pattern Access", section=S_EXT, deps=["ae_crystal_assembler"], xp=60,
      mirror="534D827A628907F4", subtitle="Every pattern, searchable", desc=[
        "&eWhat:&r the Extended Pattern Access Terminal lists every pattern provider on the network with search and filters.",
        "&eHow:&r a Pattern Access Terminal upgraded in the Crystal Assembler (check JEI). A wireless version exists too.",
        "&eTip:&r name your pattern providers in an anvil (Sulfuric Acid, Polyethylene) and the terminal groups them by name."]),
    Q("ae_circuit_slicer", 0, 0, [item("extendedae:circuit_cutter")], "Circuit Slicer", section=S_EXT, deps=["ae_crystal_assembler"], xp=60,
      mirror="48357A7486125C52", subtitle="A storage block into nine prints", desc=[
        "&eWhat:&r the Circuit Slicer cuts a whole block (gold, diamond, silicon, certus) into nine printed circuits at once.",
        "&eHow:&r made in the Crystal Assembler (check JEI). Put the matching press in and feed it blocks.",
        "&eTip:&r a silicon block becomes nine printed silicon. That's an MI ingot line feeding AE2 nine at a time."]),
    Q("ae_canner", 0, 0, [item("extendedae:caner")], "ME Canner", section=S_EXT, deps=["ae_crystal_assembler"], xp=60,
      mirror="27FC0C092EE00532", subtitle="Fill and empty containers for autocrafting", desc=[
        "&eWhat:&r the ME Canner fills buckets, cells and other containers from the network, or empties them back in.",
        "&eChemistry:&r many recipes still ask for a bucket of acid. The canner means the network can hand over 1,000 mB of H₂SO₄ in a bucket without you.",
        "&eHow:&r made in the Crystal Assembler (check JEI). Set Fill or Empty mode in its GUI and give it patterns through a provider."]),
    Q("ae_wireless_connector", 0, 0, [item("extendedae:wireless_connect", 2), item("extendedae:wireless_tool")], "Wireless Connectors", section=S_EXT,
      deps=["ae_crystal_assembler"], xp=75, mirror="52CD31F48715B17C", subtitle="Cables through thin air", desc=[
        "&eWhat:&r a pair of Wireless Connectors links two parts of your network without a cable between them. The Setup Kit binds them.",
        "&eHow:&r connectors come two at a time from the Crystal Assembler; the kit too (check JEI). Use the kit on one end, then the other.",
        "&eTip:&r great for reaching a reactor room behind thick shielding."]),
    Q("ae_wireless_hub", 0, 0, [item("extendedae:wireless_hub")], "Wireless Hub", section=S_EXT, deps=["ae_wireless_connector"], xp=60,
      mirror="3916B48D7F294932", subtitle="Many wireless links, one block", desc=[
        "&eWhat:&r the ME Wireless Hub takes many wireless links at one point.",
        "&eHow:&r from the Crystal Assembler (check JEI). Bind each connector to it with the Setup Kit.",
        "&eTip:&r one hub in the middle of your base, linked out to every outpost room."]),
    Q("ae_entro_budding", 0, 0, [item("extendedae:crystal_fixer")], "Crystal Fixer", section=S_EXT, deps=["ae_crystal_assembler"], xp=60,
      mirror="3CF32F2314839B1D", subtitle="Keep budding crystals budding", desc=[
        "&eWhat:&r budding entro and certus decay as they grow clusters. The Crystal Fixer restores them with fresh material.",
        "&eHow:&r from the Crystal Assembler (check JEI). Put it next to a budding block and give it what its GUI asks for.",
        "&eTip:&r one fixer keeps both farms alive."]),
    Q("ae_active_plane", 0, 0, [item("extendedae:active_formation_plane")], "Active Formation Plane", section=S_EXT, deps=["ae_crystal_assembler"], xp=50,
      mirror="18499D33BA12A8A9", subtitle="Push items into whatever is in front", desc=[
        "&eWhat:&r ExtendedAE's plane inserts items straight into the inventory it faces instead of dropping them.",
        "&eHow:&r a formation plane upgraded with ExtendedAE parts (check JEI).",
        "&eTip:&r handy for filling machines that don't accept a storage bus."]),
    # --- our own ExtendedAE steps (ATM10 has none of these): optional
    Q("ae_concurrent", 0, 0, [item("extendedae:concurrent_processor", 4)], "Concurrent Processors", section=S_EXT, deps=["ae_crystal_assembler"], xp=100,
      **OPT, subtitle="Optional: ExtendedAE's own processor", desc=[
        "&eWhat:&r concurrent processors go into nearly every Extended block: drives, providers, interfaces, inscribers and chargers.",
        "&eHow:&r build the Concurrent Press in the Crystal Assembler, inscribe entro crystals with it, then assemble the prints with printed silicon and redstone (check JEI).",
        "&eTip:&r the Crystal Assembler can also make AE2's normal processors from their prints."]),
    Q("ae_ex_machines", 0, 0, [item("extendedae:ex_inscriber"), item("extendedae:ex_charger")], "Extended Inscriber and Charger", section=S_EXT, deps=["ae_concurrent"], xp=100,
      **OPT, subtitle="Optional: process several stacks at once", desc=[
        "&eWhat:&r the Extended Inscriber and Extended Charger work on several items in parallel, so processors and charged certus stop being a bottleneck.",
        "&eHow:&r a normal Inscriber or Charger plus capacity cards and a concurrent processor, in the Crystal Assembler (check JEI)."]),
    Q("ae_ex_interface", 0, 0, [item("extendedae:ex_interface"), item("extendedae:ex_io_port")], "Extended Interface and IO Port", section=S_EXT, deps=["s_exae"], xp=100,
      **OPT, subtitle="Optional: more slots, faster cell transfers", desc=[
        "&eWhat:&r the Extended Interface stocks many more item types than a normal one. The Extended IO Port empties and fills cells far faster.",
        "&eHow:&r both from the Crystal Assembler (check JEI).",
        "&eTip:&r an Extended Interface next to an MI machine can hold every input that machine needs."]),
    Q("ae_ex_buses", 0, 0, [item("extendedae:tag_storage_bus"), item("extendedae:threshold_level_emitter")], "Smarter Buses", section=S_EXT, deps=["s_exae"], xp=75,
      **OPT, subtitle="Optional: filter by tag, switch with a margin", desc=[
        "&eWhat:&r the Tag Storage Bus filters by item tag, so one bus can accept every dust or every ingot. The Threshold Level Emitter turns on at one amount and off at another.",
        "&eHow:&r a storage bus or level emitter plus processors (check JEI).",
        "&eTip:&r a threshold emitter on an MI Electrolyzer stops it flickering: on below 10,000 mB of hydrogen, off above 50,000 mB."]),

    # ===== Assembler Matrix =====================================================================
    Q("ae_assembler_matrix", 0, 0, [item("extendedae:assembler_matrix_frame", 43),
                                    anyof(["extendedae:assembler_matrix_wall", "extendedae:assembler_matrix_glass"], 125)], "Assembler Matrix Shell",
      section=S_MATRIX, deps=["s_exae"], xp=200, tokens=2, size=1.5, shape="hexagon", mirror="7900A4836CC55428", subtitle="The box around a thousand crafters", desc=[
        "&eWhat:&r the Assembler Matrix is a multiblock that replaces walls of molecular assemblers. This is its shell: frames on the edges, walls or glass on the faces.",
        "&eHow:&r both from the Crystal Assembler (check JEI). The counts here are enough for a full-size shell.",
        "&eTip:&r glass faces let you watch the crafters work; walls are cheaper."]),
    Q("ae_ex_matrix_more", 0, 0, [item("extendedae:assembler_matrix_pattern", 35), item("extendedae:assembler_matrix_crafter", 35),
                                  item("extendedae:assembler_matrix_speed", 5)], "Filling the Matrix", section=S_MATRIX, deps=["ae_assembler_matrix"], xp=300,
      tokens=2, mirror="034AB493E1EC2E63",
      subtitle="Patterns, crafters and speed cores", desc=[
        "&6Thirty-five hands working as one. You remember having more, but this is a start.&r",
        "&eWhat:&r pattern cores hold the patterns, crafter cores do the work in parallel, and speed cores make each job finish sooner.",
        "&eHow:&r all from the Crystal Assembler with concurrent processors and entro (check JEI). They go inside the shell.",
        "&eTip:&r it's for crafting-table recipes only. Processing patterns for MI machines still need pattern providers."]),

    # ===== AdvancedAE ===========================================================================
    Q("eae_logic", 0, 0, [item("ae2:logic_processor")], "Into AdvancedAE", section=S_ADV, deps=["eae_fluix"], xp=40,
      size=1.5, shape="hexagon", mirror="7725CB7D0AE55180", subtitle="It starts with a logic processor", desc=[
        "&eWhat:&r AdvancedAE's first machines and its pattern provider all need logic processors. Bring one to begin.",
        "&eHow:&r the Inscriber, as on the Applied Energistics page."]),
    Q("ae_reaction", 0, 0, [item("advanced_ae:reaction_chamber")], "Reaction Chamber", section=S_ADV, deps=["eae_logic"], xp=150,
      mirror="14FC9E4A3C80C0AE", subtitle="AdvancedAE's powered reactor", desc=[
        "&eWhat:&r AdvancedAE's Reaction Chamber combines items and a fluid with lots of energy. Its first job: shattering singularities.",
        "&eHow:&r a matter condenser, a vibration chamber, fluix dust, glowstone and a bucket (check JEI). Feed it a singularity, ender dust, sky dust and lava.",
        "&eTip:&r it uses a lot of power per craft. Put it on its own Energy Acceptor."]),
    Q("ae_adv_provider", 0, 0, [anytag("advanced_ae:adv_pattern_provider"), item("advanced_ae:adv_pattern_encoder")], "Directional Providers", section=S_ADV,
      deps=["eae_logic"], xp=100, mirror="56DE217FEAE3F036", subtitle="Send each ingredient to the right face", desc=[
        "&eWhat:&r the Advanced Pattern Provider lets a processing pattern send each input to a chosen side of the machine. The Advanced Pattern Encoder writes the sides onto the pattern.",
        "&eHow:&r an Extended Pattern Provider, a logic processor, an ender pearl and redstone for the provider (check JEI for both).",
        "&eTip:&r a Mekanism PRC takes items, a fluid and a gas on different sides: perfect for this."]),
    Q("ae_quantum_alloy", 0, 0, [item("advanced_ae:shattered_singularity"), item("advanced_ae:quantum_alloy"), item("advanced_ae:quantum_processor")], "Quantum Materials",
      section=S_ADV, deps=["ae_reaction"], xp=200, mirror="411A463E98C3B102", subtitle="Shattered singularity, quantum alloy, quantum processor", desc=[
        "&eWhat:&r the three materials behind everything quantum: a shattered singularity, quantum alloy, and the quantum processor printed on it.",
        "&eChemistry:&r copper is the alloy's base for a reason: after silver it's the best electrical conductor of any metal.",
        "&eHow:&r shatter a singularity in the Reaction Chamber; react quantum infusion with copper ingots and singularities for the alloy; press it with the Quantum Press (check JEI).",
        "&eTip:&r copy the Quantum Press before you use it in automation, like the other presses."]),
    # --- our own AdvancedAE extras (optional)
    Q("ae_adv_encoder", 0, 0, [item("advanced_ae:adv_pattern_encoder")], "Encoding Directions", section=S_ADV, deps=["ae_adv_provider"], xp=40,
      **OPT, subtitle="Optional: pick a face for each ingredient", desc=[
        "&eWhat:&r the encoder adds side information to a processing pattern.",
        "&eHow:&r put a pattern in, set each input's side, and take it out. Click JEI for the recipe.",
        "&eTip:&r keep one next to your Pattern Encoding Terminal."]),
    Q("ae_quantum_processor", 0, 0, [item("advanced_ae:quantum_processor", 4)], "A Stack of Quantum Processors", section=S_ADV, deps=["ae_quantum_alloy"], xp=100,
      **OPT, subtitle="Optional: you'll need more than one", desc=[
        "&eWhat:&r quantum processors go into the Quantum Computer's parts, quantum gear and AdvancedAE's best buses.",
        "&eHow:&r inscribe quantum alloy with the Quantum Press, then add redstone and printed silicon (check JEI)."]),

    # ===== Quantum Computer =====================================================================
    Q("eae_quantum_unit", 0, 0, [item("advanced_ae:quantum_unit"), item("advanced_ae:quantum_structure")], "Quantum Unit and Structure", section=S_QC,
      deps=["ae_quantum_alloy"], xp=100, mirror="03164C4C7813CE2B", subtitle="The bricks of the computer", desc=[
        "&eWhat:&r Quantum Structure blocks make the computer's shell; Quantum Crafting Units fill its inside.",
        "&eHow:&r both need quantum alloy and shattered singularities (check JEI)."]),
    Q("ae_quantum_bigger", 0, 0, [item("advanced_ae:quantum_storage_128", 2), item("advanced_ae:quantum_storage_256")], "Quantum Storage", section=S_QC,
      deps=["eae_quantum_unit"], xp=150, mirror="658DEAAD1E68E549", subtitle="How big a job it can plan", desc=[
        "&eWhat:&r quantum storage blocks set how big a crafting job the computer can hold in mind.",
        "&eHow:&r a quantum unit plus storage components (check JEI; ExtendedAE changes a few recipes).",
        "&eTip:&r storage first: a long chemical chain fails to plan long before it runs short of threads."]),
    Q("eae_quantum_accel", 0, 0, [item("advanced_ae:quantum_accelerator")], "Quantum Accelerator", section=S_QC, deps=["eae_quantum_unit"], xp=100,
      mirror="0D8B4DAB82ABEF9D", subtitle="More jobs in parallel", desc=[
        "&eWhat:&r each Quantum Accelerator lets the computer run more crafting steps at once.",
        "&eHow:&r a quantum unit, quantum processors and shattered singularities (check JEI)."]),
    Q("ae_quantum_computer", 0, 0, [item("advanced_ae:quantum_core")], "Quantum Core", section=S_QC, deps=["eae_quantum_accel", "ae_quantum_bigger"], xp=250,
      tokens=2, size=1.5, shape="hexagon", mirror="55DFC96B4CDBFA7D", subtitle="The archive learns to think", desc=[
        "&6You remember thinking a thousand thoughts at once. The machine remembers how, too.&r",
        "&eWhat:&r the Quantum Core is the heart of the Quantum Computer: a multiblock crafting CPU with huge storage and many parallel jobs.",
        "&eHow:&r the core goes inside a shell of Quantum Structure, with units, accelerators and storage around it (check JEI for size limits).",
        "&eTip:&r build it next to your main pattern providers so every chemical line can run at once."]),
    Q("eae_multi_threader", 0, 0, [item("advanced_ae:quantum_multi_threader")], "Multi-Threader", section=S_QC, deps=["ae_quantum_computer", "ae_crystal_assembler"], xp=150,
      mirror="1A20BBBAFBEDF911", subtitle="Multiply the accelerators", desc=[
        "&eWhat:&r the Multi-Threader multiplies what each accelerator in the computer adds.",
        "&eHow:&r quantum parts and ExtendedAE's components (check JEI). Only a few fit in one computer."]),
    Q("ae_quantum_max", 0, 0, [item("advanced_ae:data_entangler")], "Data Entangler", section=S_QC, deps=["ae_quantum_computer", "ae_crystal_assembler"], xp=200,
      optional=True, tokens=2, mirror="09F43EB79DDBD127", subtitle="Optional: multiply the computer's memory", desc=[
        "&eWhat:&r the Quantum Data Entangler multiplies the whole computer's storage. Only a few fit in one multiblock.",
        "&eHow:&r quantum storage, quantum units and shattered singularities (check JEI).",
        "&eTip:&r one entangler is usually enough for the Seed of a New World chain."]),
    Q("ae_quantum_crafter", 0, 0, [item("advanced_ae:quantum_crafter")], "Quantum Crafter", section=S_QC, deps=["eae_quantum_accel"], xp=150,
      mirror="12749A25600C7FF3", subtitle="An assembler that keeps stock", desc=[
        "&eWhat:&r the Quantum Crafter crafts patterns over and over with no CPU, keeping a set amount in stock.",
        "&eHow:&r quantum accelerators, a quantum unit, 64k components and shattered singularities (check JEI).",
        "&eTip:&r set it to keep plates and wires in stock; the CPU stays free for the long chains."]),
    Q("eae_quantum_max", 0, 0, [item("advanced_ae:quantum_structure", 200), item("advanced_ae:quantum_accelerator", 100), item("advanced_ae:quantum_core"),
                                item("advanced_ae:quantum_multi_threader")], "The Full Quantum Computer", section=S_QC, deps=["eae_multi_threader"], xp=1000,
      tokens=3, size=2.0, shape="gear", mirror="7E35ED5B30697722", subtitle="Challenge: the largest computer the mod allows", desc=[
        "&6Every reaction you ever learned, planned at once. You remember being this.&r",
        "&eWhat:&r the materials for a maximum-size Quantum Computer: a full shell, a hundred accelerators, the core and a multi-threader.",
        "&eHow:&r it's a lot of shattered singularities. Automate the Reaction Chamber and the Condenser (or a Void Cell on Singularity mode) first.",
        "&eTip:&r you don't need the full size to finish the pack. This is for the archive's own sake."]),

    # ===== Quantum Armour =======================================================================
    Q("ae_quantum_armor", 0, 0, [item("advanced_ae:quantum_helmet"), item("advanced_ae:quantum_chestplate"), item("advanced_ae:quantum_leggings"),
                                 item("advanced_ae:quantum_boots")], "Quantum Armour", section=S_ARMOR, deps=["ae_quantum_alloy"], xp=300,
      tokens=2, mirror="78215D704E6095B0", subtitle="Armour wired into the network", desc=[
        "&eWhat:&r quantum armour is netherite armour rebuilt around quantum processors, with slots for AdvancedAE's armour cards.",
        "&eHow:&r each piece needs its netherite piece, quantum alloy plates, quantum processors and a quantum storage component (check JEI).",
        "&eTip:&r flight in this pack comes from chemistry (pylons, jetpacks, the Angel Ring), not from AE2, so no quest asks for the Flight Card."]),
    Q("ae_quantum_base_card", 0, 0, [item("advanced_ae:quantum_upgrade_base")], "Quantum Upgrade Base", section=S_ARMOR, deps=["ae_quantum_armor"], xp=60,
      mirror="0B4CE3969067FA31", subtitle="The blank behind every armour card", desc=[
        "&eWhat:&r the blank card that every Quantum Armour card is built on.",
        "&eHow:&r a quantum alloy plate surrounded by quantum processors (check JEI)."]),
    card("ae_cards_move", "188C9E5D340C5A0A", "advanced_ae:walk_speed_card", "Walk Speed Card", "Faster on your feet",
         "you walk faster while wearing the armour.", tip="stack it with Sprint Speed for crossing big bases."),
    card("eae_card_sprint", "70395883E97AE897", "advanced_ae:sprint_speed_card", "Sprint Speed Card", "Faster when you run",
         "sprinting is faster again."),
    card("eae_card_step", "5E610C059737628B", "advanced_ae:step_assist_card", "Step Assist Card", "Walk up blocks",
         "you step up full blocks without jumping, like a horse."),
    card("eae_card_jump", "0A354B4707894A62", "advanced_ae:jump_height_card", "Jump Height Card", "Higher jumps",
         "you jump higher."),
    card("eae_card_lava", "130A300418962332", "advanced_ae:lava_immunity_card", "Lava Immunity Card", "Swim in the Nether's oceans",
         "lava doesn't burn you.", tip="it doesn't stop fall damage into a lava lake. Look before you leap."),
    card("eae_card_water", "580624D24AE2DB4B", "advanced_ae:water_breathing_card", "Water Breathing Card", "No more air bar",
         "you breathe underwater."),
    card("eae_card_feeding", "451A6EEF33395A29", "advanced_ae:auto_feeding_card", "Auto Feeding Card", "Eat from the network",
         "when you're hungry the armour feeds you from the ME network.", tip="stock a farm's output in the network."),
    card("eae_card_stock", "621A996C7802D057", "advanced_ae:auto_stock_card", "Auto Stock Card", "Your inventory refills itself",
         "keeps chosen items stocked in your inventory from the network.", tip="torches, scaffolding and food, forever."),
    card("ae_cards_utility", "2303BB17339B240D", "advanced_ae:magnet_card", "Magnet Card", "Pull in nearby drops",
         "nearby dropped items fly to you.", tip="pair it with Auto Stock and you rarely visit storage at all."),
    card("ae_cards_survive", "4AC3EA41234BC5F0", "advanced_ae:hp_buffer_card", "HP Buffer Card", "Extra health",
         "adds extra health while worn."),
    card("eae_card_evasion", "07E5B0BF7D8E055A", "advanced_ae:evasion_card", "Evasion Card", "A chance to dodge",
         "gives a chance to dodge an attack entirely.",
         deps=("eae_card_swim", "ae_cards_move", "eae_card_sprint", "eae_card_attack")),
    card("eae_card_regen", "7610A0BB77AC8037", "advanced_ae:regeneration_card", "Regeneration Card", "Heal over time",
         "you slowly regenerate health."),
    card("eae_card_strength", "3B3F1DE1AF6EBC1E", "advanced_ae:strength_card", "Strength Card", "Hit harder",
         "your attacks deal more damage."),
    card("eae_card_attack", "6559C57A1A476489", "advanced_ae:attack_speed_card", "Attack Speed Card", "Swing faster",
         "your weapon recovers faster between swings."),
    card("eae_card_luck", "763A19067AEEF6D5", "advanced_ae:luck_card", "Luck Card", "Better loot",
         "adds luck, which improves loot rolls and fishing."),
    card("eae_card_reach", "2E61219FC0BAB675", "advanced_ae:reach_card", "Reach Card", "Longer arms",
         "you can reach blocks and entities further away."),
    card("eae_card_swim", "0D3874835F1367EE", "advanced_ae:swim_speed_card", "Swim Speed Card", "Faster in water",
         "you swim faster."),
    card("eae_card_night", "188952FC58EB40BC", "advanced_ae:night_vision_card", "Night Vision Card", "See in the dark",
         "permanent night vision while worn."),
    card("eae_card_recharge", "38D0BBD5F699EF41", "advanced_ae:recharging_card", "ME Recharging Card", "Charge from the network",
         "the armour recharges itself from the ME network's energy."),
    card("eae_card_workbench", "3347CB6478F486C6", "advanced_ae:portable_workbench_card", "Portable Workbench Card", "A crafting grid on the go",
         "opens a crafting grid from the armour."),
    card("eae_card_pick", "468E8D7CF9B83FEE", "advanced_ae:pick_craft_card", "Pick Craft Card", "Order what you look at",
         "middle-clicking a block you don't have orders it from your autocrafting."),
], links=[("ae_fluix", 0, 0)], mirror="extended__advanced_ae")
