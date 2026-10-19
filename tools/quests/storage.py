"""Quest chapter: storage. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

Layout: y=-4.5..0 Sophisticated Storage, y=2..3.5 Functional Storage, y=4..5.5 Tom's Simple Storage,
y=7 moving things (Pipez, LaserIO, Entangled, SS in Motion), y=9/10.5 Sophisticated Backpacks (after the
QoL page's q_bp_iron / q_bp_up), y=12.5..15.5 Iron Furnaces (s_furnace moved here), y=17/18.5 Logistics Network.
"""
from questlib import Q, Chapter, item, dim, tick, anyof, MAIN, SIDE  # noqa: F401

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

    # --- Even more Sophisticated Storage (y=-4.5 .. 0) -----------------------------------------
    Q("sto_ss_chest", 0, -3, [item("sophisticatedstorage:chest")], "Sophisticated Chests", deps=["s_barrel"], xp=25,
      subtitle="The same upgrades, in chest form", desc=[
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
      subtitle="Drawer-style barrels with a few huge slots", desc=[
        "&eWhat:&r limited barrels have one to four big slots and show their items on the front, like drawers, but take Sophisticated upgrades.",
        "&eHow:&r check JEI for each size. They use the same tier upgrades as normal barrels.",
        "&eTip:&r a four-slot limited barrel per metal (ore, dust, ingot, block) makes a tidy wall."]),
    Q("sto_ss_hopper", 5, -1.5, [item("sophisticatedstorage:hopper_upgrade")], "Hopper Upgrade", deps=["s_ss_tier"], xp=30,
      subtitle="Containers that pull and push themselves", desc=[
        "&eWhat:&r the Hopper Upgrade pulls items from one side and pushes them out another, with filters.",
        "&eHow:&r an upgrade base, a hopper, iron and redstone (check JEI). Set directions and filters in the container's upgrade tab.",
        "&eTip:&r a barrel with a hopper upgrade under a machine's output collects everything without pipes."]),
    Q("sto_ss_compression", 7, -1.5, [item("sophisticatedstorage:compression_upgrade")], "Compression Upgrade", deps=["s_ss_compacting"], xp=40,
      subtitle="Nuggets, ingots and blocks as one stock", desc=[
        "&eWhat:&r the Compression Upgrade links a few slots so nuggets, ingots and blocks of one material count as a single stock.",
        "&eHow:&r an upgrade base, pistons, iron and redstone (check JEI). Choose which slots it uses in the upgrade tab.",
        "&eTip:&r take out exactly the form you need: blocks for storage, ingots for crafting, nuggets for small recipes."]),
    Q("sto_ss_io", 8, 0, [item("sophisticatedstorage:storage_input"), item("sophisticatedstorage:storage_output")], "Storage Input and Output", deps=["s_ss_controller"], xp=40,
      subtitle="Separate doors into your storage", desc=[
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
      subtitle="Room for a whole lab's worth of reagents", desc=[
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
      subtitle="A furnace in your backpack", desc=[
        "&eWhat:&r the Smelting Upgrade is a furnace in the backpack screen. The Auto-Smelting Upgrade smelts matching items inside the backpack by itself, using fuel from the backpack.",
        "&eChemistry:&r smelting iron ore is a reduction: carbon monoxide strips the oxygen off the ore, Fe₂O₃ + 3CO → 2Fe + 3CO₂.",
        "&eHow:&r an upgrade base and a furnace for the first; the auto version adds a hopper, gold, redstone and a diamond (check JEI).",
        "&eTip:&r filter auto-smelting to raw ores only, or it will smelt your logs into charcoal too."]),
    Q("sto_bp_void", 4, 10.5, [item("sophisticatedbackpacks:void_upgrade")], "Void Upgrade", deps=["sto_bp_smelting"], xp=30,
      subtitle="Delete the junk as you pick it up", desc=[
        "&eWhat:&r the Void Upgrade destroys chosen items as they enter the backpack: cobblestone, dirt, gravel, rotten flesh.",
        "&eChemistry:&r real matter can't vanish (mass is conserved in every chemical reaction). In Minecraft, it can.",
        "&eHow:&r an upgrade base, ender pearls, obsidian and redstone (check JEI). Set the filter carefully.",
        "&eTip:&r keep a stack of cobblestone out of the filter. You'll want it for building and for the Matter Condenser later."]),
    Q("sto_bp_deposit", 6, 10.5, [item("sophisticatedbackpacks:deposit_upgrade"), item("sophisticatedbackpacks:restock_upgrade")], "Deposit and Restock", deps=["sto_bp_void"], xp=40,
      subtitle="Empty into chests, refill from them", desc=[
        "&eWhat:&r with a Deposit Upgrade, using the backpack on a chest puts matching items into it. A Restock Upgrade does the reverse, topping up the backpack from the chest.",
        "&eHow:&r an upgrade base, a chest, iron, redstone and a piston (sticky for restock). Check JEI.",
        "&eTip:&r deposit ores into your processing chest, restock torches and food from your supply chest, all in two clicks."]),
    Q("sto_bp_tank", 8, 10.5, [item("sophisticatedbackpacks:tank_upgrade")], "Tank Upgrade", deps=["sto_bp_deposit"], xp=40,
      subtitle="Carry fluids in your backpack", desc=[
        "&eWhat:&r the Tank Upgrade stores fluid inside the backpack. Fill and empty it with buckets or tanks from its upgrade tab.",
        "&eChemistry:&r a real acid needs the right container: HF eats glass, so it's kept in PTFE; concentrated H₂SO₄ can sit in steel. A backpack tank isn't fussy.",
        "&eHow:&r an upgrade base surrounded by glass (check JEI).",
        "&eTip:&r a tank of water means you're never stuck in a lava cave without a way to cool it into obsidian."]),

    # --- Iron Furnaces (y=12.5 .. 15.5) --------------------------------------------------------
    Q("sto_if_augment", 1, 12.5, [item("ironfurnaces:augment_speed"), item("ironfurnaces:augment_fuel")], "Speed and Fuel Augments", deps=["s_furnace"], xp=30,
      subtitle="Faster cooking, or longer-lasting fuel", desc=[
        "&eWhat:&r augments go in an Iron Furnace's augment slot. Speed cooks faster but burns more fuel; Fuel Efficiency does the opposite.",
        "&eHow:&r stone, redstone and paper around sugar (speed) or coal (fuel). Check JEI.",
        "&eTip:&r speed for ores you need now, fuel efficiency for slow bulk jobs like glass or charcoal."]),
    Q("sto_if_generator", 3, 12.5, [item("ironfurnaces:augment_generator")], "Furnace Generator", deps=["sto_if_augment"], xp=40,
      subtitle="Burn fuel for FE instead of smelting", desc=[
        "&eWhat:&r the Generator Augment turns an Iron Furnace into a small FE generator that burns furnace fuel.",
        "&eChemistry:&r burning carbon releases about 394 kJ per mole: C + O₂ → CO₂. Every generator, from a furnace to a power plant, turns that heat into work.",
        "&eHow:&r stone, redstone and paper around a repeater (check JEI). Put it in the augment slot and pull FE from the furnace.",
        "&eTip:&r a few generator furnaces on charcoal can run the Alchemistry Dissolver before MI's electric age."]),
    Q("sto_if_factory", 5, 12.5, [item("ironfurnaces:augment_factory"), item("ironfurnaces:augment_blasting")], "Factory and Blasting", deps=["sto_if_generator"], xp=40,
      subtitle="Many slots, or blast-furnace mode", desc=[
        "&eWhat:&r the Factory Augment gives a furnace several input slots that smelt side by side. The Blasting Augment makes it work like a blast furnace (the Smoking Augment like a smoker).",
        "&eHow:&r stone, redstone and paper around a piston (factory) or a blast furnace (blasting). Check JEI.",
        "&eTip:&r a factory furnace runs on FE, so put it next to your generator furnaces."]),
    Q("sto_if_gold", 2, 14, [item("ironfurnaces:gold_furnace")], "Gold Furnace", deps=["s_furnace"], xp=30,
      subtitle="The next tier up", desc=[
        "&eWhat:&r each furnace tier cooks faster than the last: iron, gold, diamond, emerald, obsidian, netherite.",
        "&eChemistry:&r gold melts at 1064 °C, lower than iron (1538 °C). It's here for its glitter, not its heat resistance.",
        "&eHow:&r gold ingots and a gold block around an Iron Furnace (check JEI)."]),
    Q("sto_if_diamond", 4, 14, [item("ironfurnaces:diamond_furnace")], "Diamond Furnace", deps=["sto_if_gold"], xp=40,
      subtitle="Carbon, in its hardest form", desc=[
        "&eWhat:&r the diamond furnace is a big step up in speed.",
        "&eChemistry:&r diamond is pure carbon, and it burns: heated in air to about 900 °C it turns into CO₂, like coal does.",
        "&eHow:&r diamonds and glass around a Gold Furnace (check JEI)."]),
    Q("sto_if_emerald", 6, 14, [item("ironfurnaces:emerald_furnace")], "Emerald Furnace", deps=["sto_if_diamond"], xp=40,
      subtitle="Faster still", desc=[
        "&eWhat:&r the emerald furnace is faster than diamond, and the base for the obsidian tier.",
        "&eChemistry:&r emerald is the mineral beryl, Be₃Al₂Si₆O₁₈, coloured green by a trace of chromium.",
        "&eHow:&r emeralds around a Diamond Furnace (check JEI). Villager trading is the easy source of emeralds."]),
    Q("sto_if_obsidian", 8, 14, [item("ironfurnaces:obsidian_furnace")], "Obsidian Furnace", deps=["sto_if_emerald", "t2_blaze"], xp=60,
      subtitle="Volcanic glass and blaze rods", desc=[
        "&eWhat:&r the obsidian furnace needs Nether blaze rods and is faster again.",
        "&eChemistry:&r obsidian is volcanic glass: lava, mostly SiO₂, cooled so fast that no crystals could form.",
        "&eHow:&r obsidian and blaze rods around an Emerald Furnace (check JEI)."]),
    Q("sto_if_netherite", 10, 14, [item("ironfurnaces:netherite_furnace")], "Netherite Furnace", deps=["sto_if_obsidian", "t2_debris"], xp=100,
      subtitle="The fastest furnace you'll build", desc=[
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

    # --- Logistics Network (y=17 / 18.5) -------------------------------------------------------
    Q("sto_ln_node", 0, 17, [item("logisticsnetworks:logistics_node", 2), item("logisticsnetworks:wrench")], "Logistics Nodes", deps=["t2_blaze"], xp=60,
      subtitle="Wireless item, fluid and energy transport", desc=[
        "&eWhat:&r Logistics Network nodes sit on machines and chests and move items, fluids and energy between every node in the same named network, with no cables.",
        "&eHow:&r obsidian, a redstone block, hoppers, an eye of ender and a redstone torch for a node (check JEI). Open a node to create or join a network, then set what it imports and exports.",
        "&eTip:&r the Wrench has a copy-paste mode: set up one node, then paste its settings onto the rest."]),
    Q("sto_ln_upgrade", 2, 17, [item("logisticsnetworks:iron_upgrade"), item("logisticsnetworks:gold_upgrade")], "Node Upgrades", deps=["sto_ln_node"], xp=40,
      subtitle="Bigger batches, shorter delays", desc=[
        "&eWhat:&r upgrades raise how much a node moves per batch and how often. Iron, gold, diamond and netherite tiers each do more.",
        "&eHow:&r the tier's metal, hoppers, chests and smooth stone (check JEI). Put them in the node's upgrade slots.",
        "&eTip:&r the upgrade's tooltip lists its exact items, fluid and energy per batch."]),
    Q("sto_ln_chem", 4, 17, [item("logisticsnetworks:mekanism_chemical_upgrade")], "Moving Chemicals", deps=["sto_ln_upgrade", "t4_tanks"], xp=75,
      subtitle="Nodes that carry Mekanism gases", desc=[
        "&eWhat:&r the Mekanism Chemical Upgrade lets nodes move Mekanism chemicals: H₂, O₂, Cl₂, SO₂ and the rest.",
        "&eChemistry:&r the contact process needs SO₂ and O₂ in the same place: 2SO₂ + O₂ → 2SO₃. Nodes can bring both to one Chemical Infuser.",
        "&eHow:&r basic chemical tanks, infused alloy, chests and an Iron Upgrade (check JEI).",
        "&eTip:&r one network for gases and another for items keeps the settings easy to read."]),
    Q("sto_ln_computer", 2, 18.5, [item("logisticsnetworks:computer")], "Network Manager", deps=["sto_ln_node"], xp=30,
      optional=True, tokens=1, subtitle="Optional: see every node and its flow", desc=[
        "&eWhat:&r the Computer opens a Network Manager that lists your networks, their nodes and how much each channel moves.",
        "&eHow:&r iron, glass and a comparator (check JEI).",
        "&eTip:&r when a line stops, look here first: a channel with no flow shows where the jam is."]),
], links=[("gs_backpack", -2, 0), ("t3_hull", -2, 7), ("t5_ae2", -2, 4), ("q_bp_iron", -2, 9), ("q_bp_up", -2, 10.5),
          ("gs_iron", -2, 14), ("t2_blaze", -2, 17)])
