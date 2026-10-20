"""Quest chapter: storage. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

Layout: y=-4.5..0 Sophisticated Storage, y=2..3.5 Functional Storage, y=4..5.5 Tom's Simple Storage,
y=7 moving things (Pipez, LaserIO, Entangled, SS in Motion), y=9/10.5 Sophisticated Backpacks (after the
QoL page's q_bp_iron / q_bp_up), y=12.5..15.5 Iron Furnaces (s_furnace moved here).
The Logistics Networks row was removed in the 2026-10-18 build round: logic.py teaches it (lg_logistics).
"""
from questlib import Q, Chapter, item, dim, tick, anytag, anyof, MAIN, SIDE  # noqa: F401

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
      optional=True, tokens=1, subtitle="Optional: nuggets to ingots to blocks, automatically", desc=[
        "&eWhat:&r the Compacting Upgrade squeezes 9 nuggets into an ingot and 9 ingots into a block as items arrive.",
        "&eChemistry:&r a block holds the same metal atoms as 9 ingots; only the packing changes, so no mass is lost either way.",
        "&eHow:&r craft it (check JEI) and put it in an upgrade slot. Add a filter so it only compacts what you choose."]),
    Q("s_ss_controller", 6, 0, [item("sophisticatedstorage:controller"), item("sophisticatedstorage:storage_link", 2)], "Storage Controller", deps=["s_ss_compacting"], xp=50,
      optional=True, tokens=1, subtitle="Optional: many containers, one inventory", desc=[
        "&eWhat:&r the Controller joins touching Sophisticated containers into one inventory; Storage Links extend its reach.",
        "&eHow:&r place it next to your chests and barrels. Pipes into the controller reach every connected container.",
        "&eTip:&r one pipe into the controller is a simple sorting system: items go where matching items already are."]),

    # --- Functional Storage (y=2) --------------------------------------------------------------
    Q("s_drawers", 0, 2, [anytag("functionalstorage:drawer")], "Drawers", deps=["s_barrel"], xp=25,
      subtitle="Huge stacks of one item each", desc=[
        "&eWhat:&r Functional Storage drawers hold lots of a single item and show it on the front.",
        "&eHow:&r craft a drawer of any wood (1, 2 or 4 slots; check JEI). Right-click to insert, left-click to take.",
        "&eTip:&r upgrades (copper, gold, diamond, netherite) multiply drawer capacity."]),
    Q("s_fs_compacting", 2, 2, [item("functionalstorage:compacting_drawer")], "Compacting Drawer", deps=["s_drawers"], xp=40,
      optional=True, tokens=1, subtitle="Optional: one drawer, three sizes of the same metal", desc=[
        "&eWhat:&r a compacting drawer stores nuggets, ingots and blocks of one metal as a single pool, and hands out whichever you ask for.",
        "&eHow:&r craft it (check JEI), then insert the item you want to track.",
        "&eTip:&r perfect for copper and tin near your bronze setup."]),
    Q("s_fs_controller", 4, 2, [item("functionalstorage:storage_controller")], "Drawer Controller", deps=["s_fs_compacting"], xp=50,
      optional=True, tokens=1, subtitle="Optional: one face for every drawer", desc=[
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
    Q("s_furnace", 0, 14, [item("ironfurnaces:iron_furnace")], "Faster Furnaces", deps=["gs_iron"], xp=25,
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
      optional=True, tokens=1, subtitle="Optional: one inventory, two places", desc=[
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
      optional=True, tokens=1, subtitle="Optional: copper, gold, diamond, netherite", desc=[
        "&eWhat:&r storage upgrades multiply a drawer's capacity. Each tier (copper, gold, diamond, netherite) holds more.",
        "&eHow:&r craft the upgrades in order (check JEI) and right-click the drawer to open its upgrade slots.",
        "&eTip:&r the Iron Downgrade does the reverse, limiting a drawer to a single stack per slot."]),
    Q("s_fs_puller", 8, 2, [item("functionalstorage:puller_upgrade"), item("functionalstorage:pusher_upgrade")], "Pullers and Pushers", deps=["s_fs_upgrade"], xp=40,
      optional=True, tokens=1, subtitle="Optional: drawers that move items themselves", desc=[
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
      optional=True, tokens=1, subtitle="Optional: reach chests across the room", desc=[
        "&eWhat:&r inventory cables carry the Inventory Connector's reach to chests that aren't touching it.",
        "&eHow:&r run cables from the connector and put a Cable Connector on each chest or drawer (check JEI).",
        "&eTip:&r framed cables can wear any block's texture, so they hide in walls."]),
    Q("s_toms_wireless", 4, 4, [item("toms_storage:adv_wireless_terminal")], "Wireless Terminal", deps=["s_toms_craft"], xp=40,
      optional=True, tokens=1, subtitle="Optional: your early network, anywhere", desc=[
        "&eWhat:&r the Advanced Wireless Terminal opens your Tom's network from a long way off.",
        "&eHow:&r check JEI, then right-click it on a Storage Terminal to bind it.",
        "&eTip:&r it's the cheapest remote storage access until AE2."]),

    # --- Even more Sophisticated Storage (y=-4.5 .. 0) -----------------------------------------
    Q("sto_ss_chest", 0, -3, [item("sophisticatedstorage:chest")], "Sophisticated Chests", deps=["s_barrel"], xp=25,
      optional=True, tokens=1, subtitle="Optional: the same upgrades, in chest form", desc=[
        "&eWhat:&r Sophisticated chests take the same tier upgrades and upgrade cards as the barrels.",
        "&eHow:&r craft a wooden chest version (check JEI). Tier upgrades work on it in place.",
        "&eTip:&r the Decoration Table re-skins chests and barrels with any wood or block, so your storage room can match your base."]),
    Q("sto_ss_shulker", 2, -3, [item("sophisticatedstorage:shulker_box")], "Sophisticated Shulker Box", deps=["sto_ss_chest", "w_end"], xp=60,
      optional=True, tokens=1, subtitle="Optional: upgradeable storage you can carry", desc=[
        "&eWhat:&r a shulker box that takes tier upgrades and upgrade cards, and keeps everything inside when you pick it up.",
        "&eHow:&r a chest, two shulker shells and a lever (check JEI). Shulkers live in End cities.",
        "&eTip:&r a shulker box with a compacting upgrade is a portable ore bank for long mining trips."]),
    Q("sto_ss_netherite", 3, -4.5, [anyof(["sophisticatedstorage:netherite_barrel", "sophisticatedstorage:netherite_chest"])], "Netherite Storage", deps=["s_ss_stack", "t2_debris"], xp=75,
      optional=True, tokens=1, subtitle="Optional: the top tier", desc=[
        "&eWhat:&r the netherite tier has the most slots and upgrade slots of any Sophisticated container.",
        "&eHow:&r a diamond-to-netherite tier upgrade on a placed diamond chest or barrel (check JEI).",
        "&eTip:&r upgrade the containers you use most first; a netherite barrel full of stack upgrades holds a staggering amount."]),
    Q("sto_ss_limited", 1, -1.5, [item("sophisticatedstorage:limited_barrel_1"), item("sophisticatedstorage:limited_barrel_4")], "Limited Barrels", deps=["s_barrel"], xp=30,
      optional=True, tokens=1, subtitle="Optional: drawer-style barrels with a few huge slots", desc=[
        "&eWhat:&r limited barrels have one to four big slots and show their items on the front, like drawers, but take Sophisticated upgrades.",
        "&eHow:&r check JEI for each size. They use the same tier upgrades as normal barrels.",
        "&eTip:&r a four-slot limited barrel per metal (ore, dust, ingot, block) makes a tidy wall."]),
    Q("sto_ss_hopper", 5, -1.5, [item("sophisticatedstorage:hopper_upgrade")], "Hopper Upgrade", deps=["s_ss_tier"], xp=30,
      optional=True, tokens=1, subtitle="Optional: containers that pull and push themselves", desc=[
        "&eWhat:&r the Hopper Upgrade pulls items from one side and pushes them out another, with filters.",
        "&eHow:&r an upgrade base, a hopper, iron and redstone (check JEI). Set directions and filters in the container's upgrade tab.",
        "&eTip:&r a barrel with a hopper upgrade under a machine's output collects everything without pipes."]),
    Q("sto_ss_compression", 7, -1.5, [item("sophisticatedstorage:compression_upgrade")], "Compression Upgrade", deps=["s_ss_compacting"], xp=40,
      optional=True, tokens=1, subtitle="Optional: nuggets, ingots and blocks as one stock", desc=[
        "&eWhat:&r the Compression Upgrade links a few slots so nuggets, ingots and blocks of one material count as a single stock.",
        "&eHow:&r an upgrade base, pistons, iron and redstone (check JEI). Choose which slots it uses in the upgrade tab.",
        "&eTip:&r take out exactly the form you need: blocks for storage, ingots for crafting, nuggets for small recipes."]),
    Q("sto_ss_io", 8, 0, [item("sophisticatedstorage:storage_input"), item("sophisticatedstorage:storage_output")], "Storage Input and Output", deps=["s_ss_controller"], xp=40,
      optional=True, tokens=1, subtitle="Optional: separate doors into your storage", desc=[
        "&eWhat:&r Storage Input only accepts items into the controller's containers; Storage Output only lets them out. Pipes and hoppers use them like any inventory.",
        "&eHow:&r a wooden storage block, gold, planks and a repeater (check JEI). Place them touching the controller's group.",
        "&eTip:&r put an Input at the end of your ore line and an Output by your crafting area, so the two never mix."]),
    Q("sto_ss_tool", 10, 0, [item("sophisticatedstorage:storage_tool")], "Storage Tool", deps=["sto_ss_io"], xp=25,
      optional=True, tokens=1, subtitle="Optional: link and lock from a distance", desc=[
        "&eWhat:&r the Storage Tool links containers to a controller without touching it and toggles settings like locks and displays.",
        "&eHow:&r an ender pearl, iron, sticks and a redstone torch (check JEI). Its tooltip lists each mode.",
        "&eTip:&r locked slots keep their item type even when empty, so a sorting system never fills them with junk."]),

    # --- Sophisticated Backpacks (y=9 / 10.5), after the QoL page's backpack quests ------------
    Q("sto_bp_gold", 0, 9, [item("sophisticatedbackpacks:gold_backpack")], "Gold Backpack", deps=["q_bp_iron"], xp=40,
      subtitle="More rows, more upgrade slots", desc=[
        "&eWhat:&r the gold backpack adds inventory rows and upgrade slots over the iron one.",
        "&eHow:&r surround an iron backpack with eight gold ingots. Everything inside stays put.",
        "&eTip:&r this pack's upgrade base is also sold in the Demigod Token shop (search \"Demigod Token\" in JEI)."]),
    Q("sto_bp_diamond", 2, 9, [item("sophisticatedbackpacks:diamond_backpack")], "Diamond Backpack", deps=["sto_bp_gold"], xp=60,
      optional=True, tokens=1, subtitle="Optional: room for a whole lab's worth of reagents", desc=[
        "&eWhat:&r the diamond backpack is the tier before netherite: even more rows and upgrade slots.",
        "&eHow:&r surround a gold backpack with eight diamonds. Netherite comes after it (see Netherite Backpack on the QoL page).",
        "&eTip:&r spend the extra slots on stack upgrades first; they multiply every slot at once."]),
    Q("sto_bp_everlasting", 4, 9, [item("sophisticatedbackpacks:everlasting_upgrade")], "Everlasting", deps=["sto_bp_diamond", "hn_wither", "w_end"], xp=150,
      optional=True, tokens=2, subtitle="Optional: a backpack that can't be lost", desc=[
        "&eWhat:&r with the Everlasting Upgrade, a dropped backpack can't burn, explode or despawn.",
        "&eHow:&r an upgrade base, nether stars and end crystals (check JEI). That means beating the Wither and visiting the End.",
        "&eTip:&r worth it before reactor work or deep Nether trips, where a lost pack hurts most."]),
    Q("sto_bp_crafting", 0, 10.5, [item("sophisticatedbackpacks:crafting_upgrade")], "Crafting Upgrade", deps=["q_bp_up"], xp=30,
      subtitle="A crafting grid in your backpack", desc=[
        "&eWhat:&r adds a 3x3 crafting grid to the backpack screen that can use the backpack's own items.",
        "&eHow:&r an upgrade base, a crafting table, iron and a chest (check JEI).",
        "&eTip:&r JEI's + button fills the backpack grid straight from the backpack."]),
    Q("sto_bp_smelting", 2, 10.5, [item("sophisticatedbackpacks:smelting_upgrade"), item("sophisticatedbackpacks:auto_smelting_upgrade")], "Smelting on the Go", deps=["sto_bp_crafting"], xp=40,
      optional=True, tokens=1, subtitle="Optional: a furnace in your backpack", desc=[
        "&eWhat:&r the Smelting Upgrade is a furnace in the backpack screen. The Auto-Smelting Upgrade smelts matching items inside the backpack by itself, using fuel from the backpack.",
        "&eChemistry:&r smelting iron ore is a reduction: carbon monoxide strips the oxygen off the ore, Fe₂O₃ + 3CO → 2Fe + 3CO₂.",
        "&eHow:&r an upgrade base and a furnace for the first; the auto version adds a hopper, gold, redstone and a diamond (check JEI).",
        "&eTip:&r filter auto-smelting to raw ores only, or it will smelt your logs into charcoal too."]),
    Q("sto_bp_void", 4, 10.5, [item("sophisticatedbackpacks:void_upgrade")], "Void Upgrade", deps=["sto_bp_smelting"], xp=30,
      optional=True, tokens=1, subtitle="Optional: delete the junk as you pick it up", desc=[
        "&eWhat:&r the Void Upgrade destroys chosen items as they enter the backpack: cobblestone, dirt, gravel, rotten flesh.",
        "&eChemistry:&r real matter can't vanish (mass is conserved in every chemical reaction). In Minecraft, it can.",
        "&eHow:&r an upgrade base, ender pearls, obsidian and redstone (check JEI). Set the filter carefully.",
        "&eTip:&r keep a stack of cobblestone out of the filter. You'll want it for building and for the Matter Condenser later."]),
    Q("sto_bp_deposit", 6, 10.5, [item("sophisticatedbackpacks:deposit_upgrade"), item("sophisticatedbackpacks:restock_upgrade")], "Deposit and Restock", deps=["sto_bp_void"], xp=40,
      optional=True, tokens=1, subtitle="Optional: empty into chests, refill from them", desc=[
        "&eWhat:&r with a Deposit Upgrade, using the backpack on a chest puts matching items into it. A Restock Upgrade does the reverse, topping up the backpack from the chest.",
        "&eHow:&r an upgrade base, a chest, iron, redstone and a piston (sticky for restock). Check JEI.",
        "&eTip:&r deposit ores into your processing chest, restock torches and food from your supply chest, all in two clicks."]),
    Q("sto_bp_tank", 8, 10.5, [item("sophisticatedbackpacks:tank_upgrade")], "Tank Upgrade", deps=["sto_bp_deposit"], xp=40,
      optional=True, tokens=1, subtitle="Optional: carry fluids in your backpack", desc=[
        "&eWhat:&r the Tank Upgrade stores fluid inside the backpack. Fill and empty it with buckets or tanks from its upgrade tab.",
        "&eChemistry:&r a real acid needs the right container: HF eats glass, so it's kept in PTFE; concentrated H₂SO₄ can sit in steel. A backpack tank isn't fussy.",
        "&eHow:&r an upgrade base surrounded by glass (check JEI).",
        "&eTip:&r a tank of water means you're never stuck in a lava cave without a way to cool it into obsidian."]),

    # --- Iron Furnaces (y=12.5 .. 15.5) --------------------------------------------------------
    Q("sto_if_augment", 1, 12.5, [item("ironfurnaces:augment_speed"), item("ironfurnaces:augment_fuel")], "Speed and Fuel Augments", deps=["s_furnace"], xp=30,
      optional=True, tokens=1, subtitle="Optional: faster cooking, or longer-lasting fuel", desc=[
        "&eWhat:&r augments go in an Iron Furnace's augment slot. Speed cooks faster but burns more fuel; Fuel Efficiency does the opposite.",
        "&eHow:&r stone, redstone and paper around sugar (speed) or coal (fuel). Check JEI.",
        "&eTip:&r speed for ores you need now, fuel efficiency for slow bulk jobs like glass or charcoal."]),
    Q("sto_if_generator", 3, 12.5, [item("ironfurnaces:augment_generator")], "Furnace Generator", deps=["sto_if_augment"], xp=40,
      optional=True, tokens=1, subtitle="Optional: burn fuel for FE instead of smelting", desc=[
        "&eWhat:&r the Generator Augment turns an Iron Furnace into a small FE generator that burns furnace fuel.",
        "&eChemistry:&r burning carbon releases about 394 kJ per mole: C + O₂ → CO₂. Every generator, from a furnace to a power plant, turns that heat into work.",
        "&eHow:&r stone, redstone and paper around a repeater (check JEI). Put it in the augment slot and pull FE from the furnace.",
        "&eTip:&r a few generator furnaces on charcoal can run the Alchemistry Dissolver before MI's electric age."]),
    Q("sto_if_factory", 5, 12.5, [item("ironfurnaces:augment_factory"), item("ironfurnaces:augment_blasting")], "Factory and Blasting", deps=["sto_if_generator"], xp=40,
      optional=True, tokens=1, subtitle="Optional: many slots, or blast-furnace mode", desc=[
        "&eWhat:&r the Factory Augment gives a furnace several input slots that smelt side by side. The Blasting Augment makes it work like a blast furnace (the Smoking Augment like a smoker).",
        "&eHow:&r stone, redstone and paper around a piston (factory) or a blast furnace (blasting). Check JEI.",
        "&eTip:&r a factory furnace runs on FE, so put it next to your generator furnaces."]),
    Q("sto_if_gold", 2, 14, [item("ironfurnaces:gold_furnace")], "Gold Furnace", deps=["s_furnace"], xp=30,
      optional=True, tokens=1, subtitle="Optional: the next tier up", desc=[
        "&eWhat:&r each furnace tier cooks faster than the last: iron, gold, diamond, emerald, obsidian, netherite.",
        "&eChemistry:&r gold melts at 1064 °C, lower than iron (1538 °C). It's here for its glitter, not its heat resistance.",
        "&eHow:&r gold ingots and a gold block around an Iron Furnace (check JEI)."]),
    Q("sto_if_diamond", 4, 14, [item("ironfurnaces:diamond_furnace")], "Diamond Furnace", deps=["sto_if_gold"], xp=40,
      optional=True, tokens=1, subtitle="Optional: carbon, in its hardest form", desc=[
        "&eWhat:&r the diamond furnace is a big step up in speed.",
        "&eChemistry:&r diamond is pure carbon, and it burns: heated in air to about 900 °C it turns into CO₂, like coal does.",
        "&eHow:&r diamonds and glass around a Gold Furnace (check JEI)."]),
    Q("sto_if_emerald", 6, 14, [item("ironfurnaces:emerald_furnace")], "Emerald Furnace", deps=["sto_if_diamond"], xp=40,
      optional=True, tokens=1, subtitle="Optional: faster still", desc=[
        "&eWhat:&r the emerald furnace is faster than diamond, and the base for the obsidian tier.",
        "&eChemistry:&r emerald is the mineral beryl, Be₃Al₂Si₆O₁₈, coloured green by a trace of chromium.",
        "&eHow:&r emeralds around a Diamond Furnace (check JEI). Villager trading is the easy source of emeralds."]),
    Q("sto_if_obsidian", 8, 14, [item("ironfurnaces:obsidian_furnace")], "Obsidian Furnace", deps=["sto_if_emerald", "t2_blaze"], xp=60,
      optional=True, tokens=1, subtitle="Optional: volcanic glass and blaze rods", desc=[
        "&eWhat:&r the obsidian furnace needs Nether blaze rods and is faster again.",
        "&eChemistry:&r obsidian is volcanic glass: lava, mostly SiO₂, cooled so fast that no crystals could form.",
        "&eHow:&r obsidian and blaze rods around an Emerald Furnace (check JEI)."]),
    Q("sto_if_netherite", 10, 14, [item("ironfurnaces:netherite_furnace")], "Netherite Furnace", deps=["sto_if_obsidian", "t2_debris"], xp=100,
      optional=True, tokens=1, subtitle="Optional: the fastest furnace you'll build", desc=[
        "&6You remember fire that answered to you. This one comes close.&r",
        "&eWhat:&r the netherite furnace is the top of the normal Iron Furnaces line.",
        "&eHow:&r netherite ingots, magma cream and a soul fire block around an Obsidian Furnace (check JEI).",
        "&eTip:&r use upgrade kits on a placed furnace so you keep its augment and settings."]),
    Q("sto_if_silver", 1, 15.5, [item("ironfurnaces:silver_furnace")], "Silver Furnace", deps=["s_furnace", "t4_byproduct"], xp=40,
      optional=True, tokens=1, subtitle="Optional: a side branch for MI's silver", desc=[
        "&eWhat:&r the silver furnace is a side tier between iron and gold, made with silver ingots.",
        "&eChemistry:&r silver (Ag) is the best conductor of heat and electricity of any element, better even than copper.",
        "&eHow:&r silver ingots and glass around an Iron Furnace (check JEI). Silver dust comes from ore byproducts in the MI Centrifuge."]),
    Q("sto_if_kits", 3, 15.5, [item("ironfurnaces:upgrade_gold"), item("ironfurnaces:upgrade_diamond")], "Upgrade Kits", deps=["sto_if_gold"], xp=30,
      optional=True, tokens=1, subtitle="Optional: upgrade a furnace without breaking it", desc=[
        "&eWhat:&r upgrade kits turn a placed furnace into the next tier and keep its contents, augment and settings.",
        "&eHow:&r each kit is the next tier's materials around a block (check JEI). Right-click the placed furnace with it.",
        "&eTip:&r kits are cheaper than crafting a new furnace when you have a whole row to upgrade."]),

    # ===== ATM10-aligned round (2026-10-19): the rest of each storage mod, grouped by job =====
    # --- vanilla containers and rails -----------------------------------------------------------
    Q("sto_vanilla", 0, 0, [item("minecraft:barrel", 2), item("minecraft:trapped_chest")], "Barrels and Trapped Chests", deps=["gs_chest"], xp=10,
      optional=True, tokens=1, subtitle="Optional: the plain vanilla containers", desc=[
        "&eWhat:&r a barrel holds as much as a chest and opens even with a block on top. A trapped chest gives a redstone signal while someone has it open.",
        "&eHow:&r barrel: planks and slabs. Trapped chest: a chest and a tripwire hook (check JEI).",
        "&eTip:&r a trapped chest next to a door makes a cheap 'is anyone in my lab?' alarm."]),
    Q("sto_ender_chest", 0, 0, [item("minecraft:ender_chest")], "Ender Chest", deps=["sto_vanilla", "t2_obsidian"], xp=30,
      optional=True, tokens=1, subtitle="Optional: one private inventory, everywhere", desc=[
        "&eWhat:&r every Ender Chest you open shows the same 27 slots, and only you can see yours.",
        "&eHow:&r 8 obsidian around an eye of ender.",
        "&eTip:&r keep spare tools and a water bucket in it; any Ender Chest becomes an emergency kit."]),
    Q("sto_hopper", 0, 0, [item("minecraft:hopper", 2)], "Hoppers", deps=["sto_vanilla", "gs_iron"], xp=15,
      optional=True, tokens=1, subtitle="Optional: the first item mover", desc=[
        "&eWhat:&r a hopper pulls items from the container above it and pushes them into the one it points at.",
        "&eHow:&r 5 iron ingots around a chest (Utilitarian also has a log recipe; check JEI).",
        "&eTip:&r a redstone signal locks a hopper, which makes simple item gates."]),
    Q("sto_rails", 0, 0, [item("minecraft:rail", 32), item("minecraft:minecart"), item("minecraft:chest_minecart"), item("minecraft:hopper_minecart")],
      "On Rails", deps=["sto_hopper"], xp=40, optional=True, tokens=1, subtitle="Optional: haul ore by cart", desc=[
        "&eWhat:&r minecarts move players and items along rails. A chest minecart carries cargo; a hopper minecart loads and unloads it.",
        "&eChemistry:&r steel rails on steel wheels have very low rolling resistance, which is why one locomotive can pull thousands of tonnes.",
        "&eHow:&r rails from iron and sticks; carts from 5 iron; combine a cart with a chest or a hopper (check JEI). Add powered rails to keep them moving.",
        "&eTip:&r a hopper under the track at your base empties every chest cart that rolls over it."]),

    # --- Functional Storage, the rest -----------------------------------------------------------
    Q("sto_fs_simple", 0, 0, [item("functionalstorage:simple_compacting_drawer")], "Simple Compacting Drawer", deps=["s_fs_compacting"], xp=25,
      optional=True, tokens=1, subtitle="Optional: two forms instead of three", desc=[
        "&eWhat:&r the simple version handles two forms of one item (ingot and block, say) instead of three.",
        "&eHow:&r check JEI. Insert the item you want it to track.",
        "&eTip:&r good for things with no nugget form, like coal and coal blocks."]),
    Q("sto_fs_tools", 0, 0, [item("functionalstorage:configuration_tool"), item("functionalstorage:linking_tool")], "Drawer Tools", deps=["s_fs_controller"], xp=30,
      optional=True, tokens=1, subtitle="Optional: lock, link and tidy your drawers", desc=[
        "&eWhat:&r the Configuration Tool locks drawers to their item and changes how the front displays. The Linking Tool adds far-away drawers to a controller.",
        "&eHow:&r check JEI for both. Sneak-use cycles the tool's mode; the mode shows on the item.",
        "&eTip:&r lock every drawer in a sorting wall, so an empty drawer still only accepts its own item."]),
    Q("sto_fs_access", 0, 0, [item("functionalstorage:controller_extension")], "Controller Access Point", deps=["sto_fs_tools"], xp=25,
      optional=True, tokens=1, subtitle="Optional: a second door into your drawer wall", desc=[
        "&eWhat:&r an access point works like the controller itself: pipes and players can use the whole drawer network through it.",
        "&eHow:&r check JEI, then link it with the Linking Tool.",
        "&eTip:&r one access point by the smelters, one by the crafting bench."]),
    Q("sto_fs_tiers", 0, 0, [item("functionalstorage:copper_upgrade"), item("functionalstorage:gold_upgrade")], "Copper and Gold Upgrades", deps=["s_fs_upgrade"], xp=25,
      optional=True, tokens=1, subtitle="Optional: the cheap capacity steps", desc=[
        "&eWhat:&r the first two capacity upgrades, before diamond. Each one multiplies how much a drawer holds.",
        "&eChemistry:&r copper (8.96 g/cm³) and gold (19.3 g/cm³) are both soft and malleable, which is why they were the first metals people worked.",
        "&eHow:&r copper: copper ingots and blocks, chests and a drawer. Gold builds on copper (check JEI)."]),
    Q("sto_fs_netherite", 0, 0, [item("functionalstorage:netherite_upgrade")], "Netherite Drawer Upgrade", deps=["sto_fs_tiers", "t2_debris"], xp=60,
      optional=True, tokens=1, subtitle="Optional: the biggest drawer there is", desc=[
        "&eWhat:&r the top drawer upgrade. One drawer holds an absurd amount of a single item.",
        "&eHow:&r smithing table: netherite upgrade template + diamond upgrade + netherite ingot.",
        "&eTip:&r save it for cobblestone, raw ore or dust, the things you have tens of thousands of."]),
    Q("sto_fs_void", 0, 0, [item("functionalstorage:void_upgrade"), item("functionalstorage:iron_downgrade")], "Void and Downgrade", deps=["s_fs_upgrade"], xp=25,
      optional=True, tokens=1, subtitle="Optional: delete the overflow, or hold less", desc=[
        "&eWhat:&r the Void Upgrade destroys whatever doesn't fit, so a full drawer never backs up a pipe. The Iron Downgrade limits a drawer to one stack per slot.",
        "&eHow:&r both are drawer upgrades (check JEI).",
        "&eTip:&r a void-upgraded cobblestone drawer at the end of a quarry line keeps everything flowing."]),

    # --- Sophisticated Storage tiers ------------------------------------------------------------
    Q("sto_ss_base", 0, 0, [item("sophisticatedstorage:upgrade_base", 2)], "Upgrade Base", deps=["s_barrel"], xp=15,
      optional=True, tokens=1, subtitle="Optional: the blank every upgrade starts from", desc=[
        "&eWhat:&r every Sophisticated Storage upgrade card starts from an upgrade base.",
        "&eHow:&r planks and iron ingots in a checker pattern. The backpack mod has its own base; JEI shows both.",
        "&eTip:&r make a few at a time; you'll want stack, hopper and compacting upgrades soon."]),
    Q("sto_ss_copper", 0, 0, [item("sophisticatedstorage:basic_to_copper_tier_upgrade")], "Copper Tier", deps=["s_ss_tier"], xp=20,
      optional=True, tokens=1, subtitle="Optional: the first small step up", desc=[
        "&eWhat:&r the copper tier sits between wood and iron: a few more slots for a little copper.",
        "&eChemistry:&r copper tarnishes green: over years it forms a patina of basic copper carbonate, Cu₂CO₃(OH)₂, which then protects the metal underneath.",
        "&eHow:&r right-click the placed container with the tier upgrade (check JEI)."]),
    Q("sto_ss_ladder", 0, 0, [item("sophisticatedstorage:iron_to_gold_tier_upgrade"), item("sophisticatedstorage:gold_to_diamond_tier_upgrade")], "Gold and Diamond Tiers", deps=["s_ss_tier"], xp=40,
      optional=True, tokens=1, subtitle="Optional: climb the ladder one tier at a time", desc=[
        "&eWhat:&r tier upgrades for an iron container to gold, then gold to diamond. More slots and more upgrade slots each time.",
        "&eHow:&r check JEI, then right-click the placed chest or barrel. Nothing inside moves.",
        "&eTip:&r upgrade the barrel your ore line feeds first; it fills fastest."]),
    Q("sto_ss_netherite_kit", 0, 0, [item("sophisticatedstorage:diamond_to_netherite_tier_upgrade")], "The Netherite Tier Kit", deps=["sto_ss_ladder", "t2_debris"], xp=60,
      optional=True, tokens=1, subtitle="Optional: the last tier upgrade", desc=[
        "&eWhat:&r turns a placed diamond chest or barrel into netherite: the most slots any Sophisticated container gets.",
        "&eHow:&r a lever and a netherite ingot, shapeless.",
        "&eTip:&r upgrade in place and every item and upgrade card inside stays where it was."]),

    # --- Sophisticated Backpacks, the rest ------------------------------------------------------
    Q("sto_bp_copper", 0, 0, [item("sophisticatedbackpacks:copper_backpack")], "Copper Backpack", deps=["gs_backpack"], xp=20,
      optional=True, tokens=1, subtitle="Optional: one small step before iron", desc=[
        "&eWhat:&r the copper backpack sits between leather and iron: a few more slots and an extra upgrade slot.",
        "&eHow:&r surround your backpack with copper ingots (check JEI). Everything inside stays put.",
        "&eTip:&r copper is plentiful early, so this is the cheapest upgrade in the line."]),
    Q("sto_bp_stack", 0, 0, [item("sophisticatedbackpacks:stack_upgrade_tier_2"), anyof(["sophisticatedbackpacks:stack_upgrade_tier_3", "sophisticatedbackpacks:stack_upgrade_tier_4"])],
      "Bigger Stacks", deps=["ql_bp_stack"], xp=40, optional=True, tokens=1, subtitle="Optional: stack upgrades II and up", desc=[
        "&eWhat:&r each stack tier multiplies how many items fit in every backpack slot. Tier 2 and either tier 3 or 4.",
        "&eHow:&r each tier is built from the one before with better materials (check JEI).",
        "&eTip:&r a backpack full of stacked dust is the cheapest way to move a day's mining to your machines."]),
    Q("sto_bp_compacting", 0, 0, [item("sophisticatedbackpacks:compacting_upgrade"), item("sophisticatedbackpacks:filter_upgrade")], "Compacting and Filters", deps=["q_bp_up"], xp=30,
      optional=True, tokens=1, subtitle="Optional: nuggets to ingots, and only what you want", desc=[
        "&eWhat:&r the Compacting Upgrade squeezes 9 of something into its block as you pick it up. The Filter Upgrade decides what pipes and hoppers may put in or take out.",
        "&eHow:&r an upgrade base with pistons, iron and redstone (compacting), or with string and redstone (filter). Check JEI.",
        "&eTip:&r compact redstone, lapis and coal while mining; whole blocks take a ninth of the space."]),
    Q("sto_bp_advanced", 0, 0, [item("sophisticatedbackpacks:advanced_pickup_upgrade"), item("sophisticatedbackpacks:advanced_magnet_upgrade"), item("sophisticatedbackpacks:advanced_filter_upgrade")],
      "Advanced Pickup", deps=["sto_bp_compacting", "sto_bp_gold"], xp=60, optional=True, tokens=1, subtitle="Optional: more filter slots, tag and mod filters", desc=[
        "&eWhat:&r the advanced versions of pickup, magnet and filter: more filter slots, plus filters by tag, mod or durability.",
        "&eHow:&r each one is its basic upgrade with gold, diamonds and redstone (check JEI).",
        "&eTip:&r a tag filter for 'c:raw_materials' picks up every raw ore in the pack with one entry."]),
    Q("sto_bp_advanced_more", 0, 0, [anyof(["sophisticatedbackpacks:advanced_feeding_upgrade", "sophisticatedbackpacks:advanced_refill_upgrade",
                                             "sophisticatedbackpacks:advanced_restock_upgrade", "sophisticatedbackpacks:advanced_deposit_upgrade",
                                             "sophisticatedbackpacks:advanced_void_upgrade", "sophisticatedbackpacks:advanced_tool_swapper_upgrade",
                                             "sophisticatedbackpacks:advanced_compacting_upgrade", "sophisticatedbackpacks:advanced_pump_upgrade"], 2)],
      "Advanced Everything", deps=["sto_bp_advanced"], xp=60, optional=True, tokens=1, subtitle="Optional: any two more advanced upgrades", desc=[
        "&eWhat:&r almost every upgrade has an advanced form with more slots and finer filters: feeding, refill, restock, deposit, void, tool swapper, compacting, pump. Any two.",
        "&eHow:&r the basic upgrade plus gold, diamonds and redstone (check JEI for each).",
        "&eTip:&r advanced feeding can be set to eat only when it won't waste food, so meals last longer."]),
    Q("sto_bp_cookers", 0, 0, [anyof(["sophisticatedbackpacks:smoking_upgrade", "sophisticatedbackpacks:blasting_upgrade"]),
                               anyof(["sophisticatedbackpacks:auto_smoking_upgrade", "sophisticatedbackpacks:auto_blasting_upgrade"])],
      "Smoker and Blast Furnace", deps=["sto_bp_smelting"], xp=40, optional=True, tokens=1, subtitle="Optional: specialist cooking in your pack", desc=[
        "&eWhat:&r smoking upgrades cook food twice as fast; blasting upgrades smelt ores twice as fast. The auto versions work by themselves.",
        "&eChemistry:&r a blast furnace forces air through the fuel, so it burns hotter. Real ones blow hot air into the bottom of a coke-and-ore stack: C + O₂ → CO₂, then CO₂ + C → 2CO, and the CO reduces the ore.",
        "&eHow:&r an upgrade base with a smoker or a blast furnace, iron and redstone; the auto ones add hoppers, gold and diamonds (check JEI).",
        "&eTip:&r one of each, not both furnace upgrades: they share the backpack's fuel."]),
    Q("sto_bp_pump", 0, 0, [item("sophisticatedbackpacks:pump_upgrade"), item("sophisticatedbackpacks:xp_pump_upgrade")], "Pumps", deps=["sto_bp_tank"], xp=40,
      optional=True, tokens=1, subtitle="Optional: fluids and experience on tap", desc=[
        "&eWhat:&r the Pump Upgrade fills and empties the backpack's tank from the world or from tanks. The XP Pump stores your experience and gives it back.",
        "&eHow:&r pump: an upgrade base with buckets, glass, a piston and a sticky piston. XP pump: an advanced pump upgrade with ender eyes, bottles o' enchanting and redstone (check JEI).",
        "&eTip:&r bank your levels in the XP pump before a risky fight; a grave keeps items, not levels."]),
    Q("sto_bp_battery", 0, 0, [item("sophisticatedbackpacks:battery_upgrade")], "Battery Upgrade", deps=["sto_bp_crafting", "t1_power"], xp=40,
      optional=True, tokens=1, subtitle="Optional: FE in your backpack", desc=[
        "&eWhat:&r stores Forge Energy in the backpack, which other upgrades and charging tools can use.",
        "&eChemistry:&r a battery stores energy as chemistry: two electrodes with different appetites for electrons, kept apart by an electrolyte.",
        "&eHow:&r an upgrade base with gold ingots and redstone blocks (check JEI).",
        "&eTip:&r charge it at home, then top up your jetpack or Mining Gadget in the field."]),
    Q("sto_bp_stonecutter", 0, 0, [item("sophisticatedbackpacks:stonecutter_upgrade")], "Stonecutter Upgrade", deps=["sto_bp_crafting"], xp=25,
      optional=True, tokens=1, subtitle="Optional: cut stone without a block", desc=[
        "&eWhat:&r the Stonecutter Upgrade adds a stonecutter to the backpack screen.",
        "&eHow:&r an upgrade base with a stonecutter, iron and redstone (check JEI).",
        "&eTip:&r perfect for Create Deco, Rechiseled and laboratory blocks on a building trip."]),
    Q("sto_bp_inception", 0, 0, [item("sophisticatedbackpacks:inception_upgrade")], "Inception", deps=["sto_bp_diamond", "hn_wither"], xp=100,
      optional=True, tokens=2, subtitle="Optional: backpacks within backpacks", desc=[
        "&eWhat:&r with the Inception Upgrade, backpacks stored inside your backpack keep using their own upgrades, and you can open them from the outer one.",
        "&eHow:&r an upgrade base with ender eyes, diamonds and a Nether Star (check JEI).",
        "&eTip:&r a small 'mining' backpack inside your main one keeps its magnet and void settings separate."]),
    Q("sto_bp_jukebox", 0, 0, [item("sophisticatedbackpacks:jukebox_upgrade")], "Mixtape", deps=["sto_bp_crafting"], xp=20,
      secret=True, loot="secret", subtitle="Secret: music while you mine", desc=[
        "&6You remember a time when the spheres sang to you. A jukebox in a backpack will have to do.&r",
        "&eWhat:&r the Jukebox Upgrade plays music discs from inside your backpack, wherever you walk.",
        "&eTip:&r it plays to everyone nearby. Choose your disc with care."]),

    # --- Iron Furnaces, the rest ----------------------------------------------------------------
    Q("sto_if_copper", 0, 0, [item("ironfurnaces:copper_furnace")], "Copper Furnace", deps=["gs_furnace"], xp=15,
      optional=True, tokens=1, subtitle="Optional: the first metal furnace", desc=[
        "&eWhat:&r the copper furnace is a small step faster than vanilla, and the cheapest Iron Furnace.",
        "&eChemistry:&r copper conducts heat about five times better than iron, which is why good saucepans have copper bottoms.",
        "&eHow:&r 8 copper ingots around a furnace."]),
    Q("sto_if_crystal", 0, 0, [item("ironfurnaces:crystal_furnace")], "Crystal Furnace", deps=["sto_if_diamond"], xp=40,
      optional=True, tokens=1, subtitle="Optional: a furnace you can see into", desc=[
        "&eWhat:&r a side tier from diamond: as fast as a diamond furnace, built of clear glass.",
        "&eChemistry:&r glass lets visible light through because its electrons need more energy than visible light carries to jump up, so the photons pass straight through.",
        "&eHow:&r clear glass and an eye of ender around a diamond furnace (check JEI)."]),
    Q("sto_if_more_kits", 0, 0, [anyof(["ironfurnaces:upgrade_copper", "ironfurnaces:upgrade_iron", "ironfurnaces:upgrade_iron2", "ironfurnaces:upgrade_gold2",
                                       "ironfurnaces:upgrade_silver", "ironfurnaces:upgrade_silver2", "ironfurnaces:upgrade_emerald", "ironfurnaces:upgrade_crystal",
                                       "ironfurnaces:upgrade_obsidian", "ironfurnaces:upgrade_obsidian2", "ironfurnaces:upgrade_netherite"], 2)],
      "Every Kit", deps=["sto_if_kits"], xp=30, optional=True, tokens=1, subtitle="Optional: any two more upgrade kits", desc=[
        "&eWhat:&r there's a kit for every step: vanilla to copper or iron, copper to iron, iron to gold or silver, diamond to emerald or crystal, up to netherite. Any two.",
        "&eHow:&r each is the next tier's material around a stone tool material or gem (check JEI).",
        "&eTip:&r kits keep the furnace's augment, so upgrade a generator furnace without losing its setup."]),
    Q("sto_if_smoking", 0, 0, [item("ironfurnaces:augment_smoking")], "Smoking Augment", deps=["sto_if_factory"], xp=20,
      optional=True, tokens=1, subtitle="Optional: a furnace that cooks food fast", desc=[
        "&eWhat:&r turns an Iron Furnace into a smoker: food only, at double speed.",
        "&eChemistry:&r smoking preserves meat: phenols and other compounds in wood smoke kill microbes and slow the fats going rancid.",
        "&eHow:&r stone, redstone and paper around a smoker."]),
    Q("sto_if_wireless", 0, 0, [item("ironfurnaces:heater"), item("ironfurnaces:item_heater")], "Wireless Heat", deps=["sto_if_factory"], xp=40,
      optional=True, tokens=1, subtitle="Optional: run furnaces on FE without cables", desc=[
        "&eWhat:&r the Wireless Heat Transmitter takes FE; a Wireless Heat Receiver bound to it goes into a furnace's fuel slot and heats it with that energy. Iron tier and up.",
        "&eHow:&r the transmitter is stone, a comparator, a redstone block and a furnace; the receiver is stone, redstone and a comparator. Bind the receiver to the transmitter (check its tooltip).",
        "&eTip:&r one transmitter on your power line, receivers in a whole row of furnaces: no coal ever again."]),
    Q("sto_if_copy", 0, 0, [item("ironfurnaces:item_copy")], "Settings Linker", deps=["s_furnace"], xp=15,
      optional=True, tokens=1, subtitle="Optional: copy one furnace's setup to another", desc=[
        "&eWhat:&r the Furnace Settings Linker copies a furnace's side and redstone settings onto other furnaces.",
        "&eHow:&r paper around a furnace (check JEI). Use it on the configured furnace, then on the others.",
        "&eTip:&r set up one furnace's input and output sides, then copy it down the whole row."]),
    Q("sto_if_rainbow", 0, 0, [item("ironfurnaces:rainbow_plating", 8), item("ironfurnaces:rainbow_core"), item("ironfurnaces:million_furnace")],
      "The Rainbow Furnace", deps=["sto_if_netherite", "sto_if_crystal", "sto_if_silver", "sto_if_copper"], xp=200,
      optional=True, tokens=2, subtitle="Optional: every furnace, melted into one", desc=[
        "&6Every colour of fire at once. You remember when a flame would do whatever you asked.&r",
        "&eWhat:&r the Rainbow Furnace is the top of Iron Furnaces, built from one of every other furnace.",
        "&eChemistry:&r flame colours are real chemistry: copper burns green, sodium yellow, strontium red, potassium lilac. Each element's electrons emit their own wavelengths (that's how fireworks get their colours).",
        "&eHow:&r rainbow plating is iron, gold, diamond, emerald, obsidian, crystal, copper and silver furnaces, shapeless (makes 8). The core is a netherite furnace in rainbow glass. 8 plating around the core makes the furnace."]),
], links=[("gs_backpack", -2, 0), ("t3_hull", -2, 7), ("t5_ae2", -2, 4), ("q_bp_iron", -2, 9), ("q_bp_up", -2, 10.5),
          ("gs_iron", -2, 14), ("lg_logistics", -2, 17)])
