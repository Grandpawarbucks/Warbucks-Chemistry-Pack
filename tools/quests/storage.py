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
    Q("s_entangled", 6, 7, [tick()], "Entangled", deps=["gs_iron", "s_barrel"], xp=40,
      subtitle="One inventory, two places", desc=[
        "&eWhat:&r an Entangled Block is a window into another inventory: bind it to a chest or machine, and anything put in the Entangled Block goes into the bound block, even across dimensions.",
        "&eHow:&r ender pearls, obsidian and a wooden chest (check JEI). Right-click the target with the Entangled Binder (pearls, obsidian and a diamond), then right-click the Entangled Block. Click the checkmark when one is working.",
        "&eTip:&r put one next to a remote ore processor and pipe the output straight home. Both chunks must be loaded."]),
    Q("s_ss_minecart", 8, 7, [item("sophisticatedstorageinmotion:storage_minecart")], "Storage in Motion", deps=["s_ss_tier"], xp=40,
      optional=True, tokens=1, subtitle="Optional: Sophisticated chests on rails and water", desc=[
        "&eWhat:&r Sophisticated Storage in Motion puts upgradeable chests and barrels on minecarts, boats and rafts, upgrades and all.",
        "&eHow:&r combine a minecart with a Sophisticated chest or barrel (check JEI). Boats and rafts work the same way.",
        "&eTip:&r a hopper upgrade on a storage minecart makes a simple ore train between your mine and base."]),

    # --- More Sophisticated Storage (y=-1.5) ---------------------------------------------------
    Q("s_ss_stack", 3, -1.5, [item("sophisticatedstorage:stack_upgrade_tier_1")], "Stack Upgrades", deps=["s_ss_tier"], xp=40,
      optional=True, tokens=1, subtitle="Optional: more items in every slot", desc=[
        "&eWhat:&r stack upgrades multiply how many items fit in each slot of a chest or barrel. Higher tiers multiply more.",
        "&eHow:&r an upgrade base and storage blocks (check JEI). Insert it in an upgrade slot.",
        "&eTip:&r a barrel with a few stack upgrades holds a whole mine's worth of cobblestone or raw ore."]),

    # --- More Functional Storage (y=2) ---------------------------------------------------------
    Q("s_fs_upgrade", 6, 2, [item("functionalstorage:diamond_upgrade")], "Drawer Upgrades", deps=["s_fs_controller"], xp=40,
      subtitle="Copper, gold, diamond, netherite", desc=[
        "&eWhat:&r storage upgrades multiply a drawer's capacity. Each tier (copper, gold, diamond, netherite) holds more.",
        "&eHow:&r craft the upgrades in order (check JEI) and right-click the drawer to open its upgrade slots.",
        "&eTip:&r the Iron Downgrade does the reverse, limiting a drawer to a single stack per slot."]),
    Q("s_fs_puller", 8, 2, [item("functionalstorage:puller_upgrade"), item("functionalstorage:pusher_upgrade")], "Pullers and Pushers", deps=["s_fs_upgrade"], xp=40,
      subtitle="Drawers that move items themselves", desc=[
        "&eWhat:&r utility upgrades: the Puller pulls items from the block it faces, the Pusher pushes items into it. No pipes needed.",
        "&eHow:&r check JEI. Put one in a drawer's utility slot and set its direction in the drawer's menu.",
        "&eTip:&r a drawer with a Puller behind a macerator collects all the dust without a single pipe."]),
    Q("s_fs_fluid", 10, 2, [item("functionalstorage:fluid_1")], "Fluid Drawers", deps=["s_fs_upgrade"], xp=40,
      optional=True, tokens=1, subtitle="Optional: drawers for liquids", desc=[
        "&eWhat:&r fluid drawers store a fluid instead of items, and show it on the front.",
        "&eChemistry:&r handy for small stocks of acids: one drawer of H₂SO₄, one of HCl, one of HNO₃. A real lab keeps acids in separate, labelled containers too.",
        "&eHow:&r check JEI. Pipes and MI fluid pipes can fill and drain them; the storage upgrades work on them too."]),
    Q("s_fs_ender", 7, 3.5, [item("functionalstorage:ender_drawer")], "Ender Drawer", deps=["s_fs_upgrade"], xp=40,
      optional=True, tokens=1, subtitle="Optional: one drawer, many places", desc=[
        "&eWhat:&r every Ender Drawer with the same frequency shares one inventory, wherever it is.",
        "&eHow:&r check JEI. Link drawers with the Linking Tool to give them the same frequency.",
        "&eTip:&r put one at your mine and one at your smelters to send ore home."]),

    # --- More Tom's Simple Storage (y=4) -------------------------------------------------------
    Q("s_toms_cable", 2, 4, [item("toms_storage:inventory_cable", 16), item("toms_storage:inventory_cable_connector")], "Inventory Cables", deps=["s_toms"], xp=30,
      subtitle="Reach chests across the room", desc=[
        "&eWhat:&r inventory cables carry the Inventory Connector's reach to chests that aren't touching it.",
        "&eHow:&r run cables from the connector and put a Cable Connector on each chest or drawer (check JEI).",
        "&eTip:&r framed cables can wear any block's texture, so they hide in walls."]),
    Q("s_toms_wireless", 4, 4, [item("toms_storage:adv_wireless_terminal")], "Wireless Terminal", deps=["s_toms_craft"], xp=40,
      optional=True, tokens=1, subtitle="Optional: your early network, anywhere", desc=[
        "&eWhat:&r the Advanced Wireless Terminal opens your Tom's network from a long way off.",
        "&eHow:&r check JEI, then right-click it on a Storage Terminal to bind it.",
        "&eTip:&r it's the cheapest remote storage access until AE2."]),
], links=[("gs_backpack", -2, 0), ("t3_hull", -2, 7), ("t5_ae2", -2, 4)])
