"""Quest chapter: storage. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

CHAPTER = Chapter("storage", "Storage and Logistics", "sophisticatedbackpacks:backpack",
        ["A god needs somewhere to keep things."], SIDE, [
    # --- Sophisticated Storage (y=0) -----------------------------------------------------------
    Q("s_barrel", 0, 0, [item("sophisticatedstorage:barrel")], "Sophisticated Barrel", deps=["gs_backpack"], xp=25,
      subtitle="Chests and barrels that grow with you", desc=[
        "&6You remember vaults that held the stars. A barrel is humbler, but it's a start.&r",
        "&eWhat:&r Sophisticated Storage chests and barrels take upgrades, just like your backpack. Sophisticated Storage Plus raises their limits.",
        "&eHow:&r craft a wooden barrel (check JEI). Tier upgrades improve it in place later.",
        "&eTip:&r barrels keep their contents when broken, so moving a full one is easy."]),
    Q("s_ss_tier", 2, 0, [item("sophisticatedstorage:basic_to_iron_tier_upgrade")], "Tier Upgrades", deps=["s_barrel"], xp=25,
      subtitle="More slots without emptying anything", desc=[
        "&eWhat:&r tier upgrades turn a placed chest or barrel into the next tier (copper, iron, gold, diamond, netherite) without moving items.",
        "&eHow:&r craft the upgrade (check JEI) and right-click it on the placed container.",
        "&eTip:&r you can skip tiers with the direct upgrades, like basic → iron."]),
    Q("s_ss_compacting", 4, 0, [item("sophisticatedstorage:compacting_upgrade")], "Compacting", deps=["s_ss_tier"], xp=40,
      subtitle="Nuggets to ingots to blocks, automatically", desc=[
        "&eWhat:&r the Compacting Upgrade squeezes 9 nuggets into an ingot and 9 ingots into a block as items arrive.",
        "&eChemistry:&r a block holds the same metal atoms as 9 ingots; only the packing changes, so no mass is lost either way.",
        "&eHow:&r craft it (check JEI) and put it in an upgrade slot. Add a filter so it only compacts what you choose."]),
    Q("s_ss_controller", 6, 0, [item("sophisticatedstorage:controller"), item("sophisticatedstorage:storage_link", 2)], "Storage Controller", deps=["s_ss_compacting"], xp=50,
      subtitle="Many containers, one inventory", desc=[
        "&eWhat:&r the Controller joins touching Sophisticated containers into one inventory; Storage Links extend its reach.",
        "&eHow:&r place it next to your chests and barrels. Pipes into the controller reach every connected container.",
        "&eTip:&r one pipe into the controller is a simple sorting system: items go where matching items already are."]),

    # --- Functional Storage (y=2) --------------------------------------------------------------
    Q("s_drawers", 0, 2, [item("functionalstorage:oak_1")], "Drawers", deps=["s_barrel"], xp=25,
      subtitle="Huge stacks of one item each", desc=[
        "&eWhat:&r Functional Storage drawers hold lots of a single item and show it on the front.",
        "&eHow:&r craft an oak drawer (1, 2 or 4 slots; check JEI). Right-click to insert, left-click to take.",
        "&eTip:&r upgrades (copper, gold, diamond, netherite) multiply drawer capacity."]),
    Q("s_fs_compacting", 2, 2, [item("functionalstorage:compacting_drawer")], "Compacting Drawer", deps=["s_drawers"], xp=40,
      subtitle="One drawer, three sizes of the same metal", desc=[
        "&eWhat:&r a compacting drawer stores nuggets, ingots and blocks of one metal as a single pool, and hands out whichever you ask for.",
        "&eHow:&r craft it (check JEI), then insert the item you want to track.",
        "&eTip:&r perfect for copper and tin near your bronze setup."]),
    Q("s_fs_controller", 4, 2, [item("functionalstorage:storage_controller")], "Drawer Controller", deps=["s_fs_compacting"], xp=50,
      subtitle="One face for every drawer", desc=[
        "&eWhat:&r the Storage Controller links nearby drawers into one inventory you (and pipes) can use.",
        "&eHow:&r place it among your drawers. Use the Linking Tool to add drawers further away.",
        "&eTip:&r a Controller Extension gives you a second access point."]),
    Q("s_toms", 0, 4, [item("toms_storage:storage_terminal"), item("toms_storage:inventory_connector")], "An Early Network", deps=["s_drawers"], xp=75,
      subtitle="Tom's Simple Storage: one searchable terminal", desc=[
        "&eWhat:&r Tom's Simple Storage connects your chests into one searchable terminal. It's your network until AE2.",
        "&eHow:&r place an Inventory Connector touching your chests (or link them with Inventory Cables), and a Storage Terminal on it.",
        "&eTip:&r point it at a drawer controller and every drawer shows up in the terminal."]),
    Q("s_toms_craft", 1, 5.5, [item("toms_storage:crafting_terminal")], "Crafting Terminal", deps=["s_toms"], xp=40,
      optional=True, tokens=1, subtitle="Optional: craft straight from storage", desc=[
        "&eWhat:&r a terminal with a crafting grid that pulls ingredients from the network. JEI's + button fills it for you.",
        "&eHow:&r upgrade a Storage Terminal (check JEI).",
        "&eTip:&r a Wireless Terminal (also in JEI) lets you use it from across the base."]),

    # --- Moving things (y=7) -------------------------------------------------------------------
    Q("s_furnace", 0, 7, [item("ironfurnaces:iron_furnace")], "Faster Furnaces", deps=["gs_iron"], xp=25,
      subtitle="Iron Furnaces smelt faster", desc=[
        "&eWhat:&r Iron Furnaces are faster furnaces in metal tiers. A generator augment turns one into a small FE source.",
        "&eChemistry:&r smelting iron ore is a reduction: carbon pulls the oxygen off, Fe₂O₃ + 3CO → 2Fe + 3CO₂.",
        "&eHow:&r ring a furnace with iron (check JEI). Upgrade kits move it up a tier without breaking it."]),
    Q("s_pipes", 2, 7, [item("pipez:item_pipe", 8)], "Pipez", deps=["gs_iron"], xp=25,
      subtitle="Simple item, fluid and energy pipes", desc=[
        "&eWhat:&r simple pipes for moving items, fluids and energy between non-MI machines.",
        "&eHow:&r place a line from source to target, then set the end touching the source to extract (the pipe tooltip explains how).",
        "&eTip:&r MI machines have their own pipes; Pipez is best for everything else."]),
    Q("s_laser", 4, 7, [item("laserio:laser_node", 2)], "LaserIO", deps=["s_pipes", "t3_hull"], xp=75,
      subtitle="Move things through the air", desc=[
        "&eWhat:&r Laser Nodes move items, fluids and energy between machines without cables.",
        "&eHow:&r place nodes on machines, link them with the Laser Wrench, and add cards to set what moves (check JEI).",
        "&eTip:&r one node can serve all six faces of a block, great for compact chemical setups."]),

    # --- Applied Energistics 2 (y=9.5) ---------------------------------------------------------
    Q("s_ae_drive", 0, 9.5, [item("ae2:drive"), item("ae2:terminal")], "AE2 Storage", deps=["t5_ae2"], xp=150,
      subtitle="Drives, terminals and the god's archive", desc=[
        "&6You remember a mind that held every name of every thing. The archive is waking.&r",
        "&eWhat:&r ME Drives hold storage cells; terminals let you see and search everything.",
        "&eHow:&r connect the drive and a terminal to your ME Controller with cables (check JEI).",
        "&eTip:&r keep power stable: an Energy Cell buffers the network."]),
    Q("s_ae_cell", 2, 9.5, [item("ae2:cell_component_1k", 2), item("ae2:item_storage_cell_1k")], "Storage Cells", deps=["s_ae_drive"], xp=75,
      subtitle="Bytes for your items", desc=[
        "&eWhat:&r cells are where the network actually stores things. Bigger components (4k, 16k, 64k, 256k) hold more.",
        "&eChemistry:&r certus and fluix are fictional, but the logic processors behind them echo real chips: doped silicon (Si).",
        "&eHow:&r craft components from processors and certus quartz, then put one in a cell housing (check JEI)."]),
    Q("s_ae_craft", 4, 9.5, [item("ae2:crafting_terminal")], "Autocrafting", deps=["s_ae_cell"], xp=150,
      subtitle="Whole chemical chains in one click", desc=[
        "&eWhat:&r pattern providers plus molecular assemblers turn whole chemical chains into one click.",
        "&eHow:&r a Crafting Terminal, some crafting storage, and patterns encoded in a Pattern Encoding Terminal (check JEI).",
        "&eTip:&r processing patterns can drive MI machines too: send the inputs, wait for the outputs."]),
    Q("s_exae", 6, 9.5, [item("extendedae:ex_pattern_provider"), item("extendedae:ex_drive")], "ExtendedAE", deps=["s_ae_craft"], xp=150,
      subtitle="Bigger providers and drives", desc=[
        "&eWhat:&r ExtendedAE adds larger versions of AE2 blocks: the Extended Pattern Provider holds many more patterns, the Extended Drive many more cells.",
        "&eHow:&r made in ExtendedAE's Crystal Assembler from the normal blocks (check JEI).",
        "&eTip:&r one extended provider can feed a whole row of chemical reactors."]),
    Q("s_mega", 2, 11.5, [item("megacells:sky_steel_ingot", 4), item("megacells:item_storage_cell_1m")], "MEGA Cells", deps=["s_ae_cell"], xp=200,
      subtitle="Sky steel and million-byte cells", desc=[
        "&eWhat:&r MEGA Cells adds 1M to 256M cells, bulk cells and bigger crafting storage.",
        "&eChemistry:&r sky steel is made by dropping charged certus, iron and sky stone into lava: heat drives the alloying, like a tiny smelter.",
        "&eHow:&r throw the ingredients into a lava pool for sky steel, then build the 1M component (check JEI)."]),
    Q("s_appmek", 4, 11.5, [item("appmek:chemical_storage_cell_1k")], "Gas in the Network", deps=["s_ae_cell", "t4_mv"], xp=150,
      subtitle="Store Mekanism chemicals in AE2", desc=[
        "&eWhat:&r Applied Mekanistics lets AE2 store and move Mekanism chemicals: H₂, O₂, Cl₂, HCl, SO₂ and the rest.",
        "&eChemistry:&r a 1k cell holds a lot of gas because the network stores amounts, not tanks. Real gases need pressure vessels.",
        "&eHow:&r a chemical cell housing (osmium, quartz glass, redstone) + a 1k component. Import buses on chemical tanks fill it.",
        "&eTip:&r processing patterns can pull stored SO₂ and O₂ straight from the cell to feed your sulfuric acid line."]),
    Q("s_appflux", 6, 11.5, [item("appflux:charged_redstone", 4), item("appflux:fe_1k_cell")], "Energy in a Cell", deps=["s_ae_cell"], xp=150,
      subtitle="Applied Flux stores FE in AE2", desc=[
        "&eWhat:&r Applied Flux stores FE in AE2 cells and moves it through the network with Flux Accessors.",
        "&eHow:&r redstone crystal (redstone block, fluix and glowstone dropped in water) → charge it in the AE2 Charger → FE cell core and housing (check JEI).",
        "&eTip:&r the housing needs insulating resin, which needs silicon: a little chemistry even here."]),
    Q("s_ae_wireless", 1, 8, [item("ae2:wireless_crafting_terminal")], "Wireless Access", deps=["s_ae_drive"], xp=75,
      optional=True, tokens=1, subtitle="Optional: your network in your pocket", desc=[
        "&eWhat:&r reach your ME network from anywhere in range of a Wireless Access Point.",
        "&eHow:&r check JEI. AE2 Wireless Terminals adds a universal terminal; the Infinity Booster Card removes the range limit.",
        "&eTip:&r put the access point near the middle of your base for the best coverage."]),
    Q("s_requester", 5, 8, [item("merequester:requester")], "ME Requester", deps=["s_ae_craft"], xp=75,
      optional=True, tokens=1, subtitle="Optional: keep stock topped up", desc=[
        "&eWhat:&r the ME Requester keeps a set amount of an item in stock by ordering crafts automatically.",
        "&eHow:&r check JEI. Set \"keep 64 HDPE\" and it never runs out.",
        "&eTip:&r it needs autocrafting patterns for whatever it keeps in stock."]),
])
