"""Quest chapter: storage. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

Mirror of ATM10's "Basic Storage" chapter (user decision 2026-10-20: quest for quest where we have the mod; the
same items, order, sections and sizes). Every quest with mirror="<id>" sits where that ATM10 quest sits; the
text is ours. ATM10 quests we skip: Dimensional Storage (no dimstorage), Trash Cans (no trashcans), Chipped
workbench upgrades (no chipped). Quests ATM10 doesn't have (Tom's Simple Storage, Pipez/LaserIO/Entangled, Storage
in Motion, Iron Furnaces, the Sophisticated tier-upgrade kits) stay as optional side quests off the nearest quest.

INTEGRATOR: eight ATM10 storage quests are covered by quests that live in qol.py (keys must not change, so move
them here or leave them; ids are hashed from the key alone). Their mirror ids, for whoever owns that file:
  q_bp_up (pickup + magnet)  -> 0E0CAA31480EC0A1 (pickup)  [ATM10 also has magnet 110D27EA86CDA62B]
  q_bp_iron                  -> 2F9B0C642A6BE30C
  q_bp_netherite             -> 46D756F4DC6CC894
  q_bp_feeding               -> 5FA9BC0D8476D322
  ql_bp_stack (tier 1)       -> 7E9E03274A88347D
  ql_bp_tools (tool swapper) -> 615B9062FE8CCD36
  ql_bp_refill               -> 33882172DA8021F6
"""
from questlib import Q, Chapter, item, dim, tick, anytag, anyof, MAIN, SIDE  # noqa: F401

S_HUB, S_VAN, S_FS, S_SS, S_BP = "Storage Basics", "Vanilla Containers", "Functional Storage", "Sophisticated Storage", "Sophisticated Backpacks"
S_TOMS, S_MOVE, S_IF = "Tom's Simple Storage", "Moving Things", "Iron Furnaces"
OPT = dict(optional=True, tokens=1)

CHAPTER = Chapter("storage", "Storage and Logistics", "sophisticatedbackpacks:backpack",
        ["A god needs somewhere to keep things."], SIDE, [
    # ===== Storage Basics: the hub (ATM10 centre) ==============================================
    Q("sto_hub", 0, 0, [anytag("c:chests")], "Somewhere for Everything", section=S_HUB, deps=["gs_chest"], xp=20,
      size=2.0, shape="gear", mirror="5A94A2664BFDD7B9", subtitle="Any chest opens the storage chapter", desc=[
        "&6You remember vaults that held the stars. Today it's a box of planks, and that's fine.&r",
        "&eWhat:&r this page is every way the pack stores things: vanilla containers, Functional Storage drawers, Sophisticated chests and backpacks, and a few extras of our own.",
        "&eHow:&r any chest counts: vanilla, Sophisticated, archwood, whatever you have.",
        "&eTip:&r the god's archive (AE2) has its own page. Build a drawer wall first; it'll feed the archive later."]),
    Q("sto_tip_nbt", 0, 0, [tick()], "Note: Items With Data", section=S_HUB, deps=["sto_hub"], xp=10, icon="minecraft:enchanted_book",
      mirror="7EF57BBEAA4B6B08", subtitle="Why your enchanted books clog a digital system", desc=[
        "&eWhat:&r some items carry data: enchanted books, damaged tools, filled backpacks, named things. Digital storage (AE2) spends a whole item type on each variant, so a thousand odd books eat a cell's 63 types fast.",
        "&eHow:&r keep data-heavy items in plain chests, drawers or a Sophisticated chest. Put only bulk, identical items (ores, dusts, ingots) in cells.",
        "&eTip:&r a storage bus on a chest full of books gives AE2 a window into it without wasting cell types."]),
    Q("sto_tip_sorting", 0, 0, [tick()], "Note: Sort As You Go", section=S_HUB, deps=["sto_hub"], xp=10, icon="minecraft:hopper",
      **OPT, mirror="209DC1E9AD4C5A84", subtitle="A tidy base is a fast base", desc=[
        "&eWhat:&r a chest named 'stuff' is where ingredients go to be forgotten. Pick a home for each kind of thing early: one wall for ores and metals, one for chemicals, one for building blocks.",
        "&eHow:&r drawers for bulk items, chests for odds and ends, a backpack with a void filter for junk.",
        "&eTip:&r every mod on this page can feed a controller, and a controller is what AE2 will read later."]),

    # ===== Vanilla Containers (ATM10 below the hub) ===========================================
    Q("sto_vanilla_hub", 0, 0, [anyof(["minecraft:chest", "ars_nouveau:archwood_chest"])], "Vanilla Storage", section=S_VAN, deps=["sto_hub"], xp=15,
      size=1.5, shape="hexagon", mirror="134608BB2B04D96E", subtitle="The containers Minecraft already gives you", desc=[
        "&eWhat:&r chests, barrels, trapped chests, ender chests, chest boats and minecarts. Simple, cheap, and still useful late game.",
        "&eHow:&r a chest from 8 planks, or an archwood chest from Ars Nouveau's archwood.",
        "&eTip:&r two chests side by side make a double chest; a barrel opens even with a block on top."]),
    Q("sto_vanilla", 0, 0, [item("minecraft:trapped_chest")], "Trapped Chest", section=S_VAN, deps=["sto_vanilla_hub"], xp=10,
      mirror="7F990FBC1A691020", subtitle="A chest that tells on whoever opens it", desc=[
        "&eWhat:&r a trapped chest gives a redstone signal while someone has it open.",
        "&eHow:&r a chest and a tripwire hook (check JEI).",
        "&eTip:&r a trapped chest next to a door makes a cheap 'is anyone in my lab?' alarm."]),
    Q("sto_barrel", 0, 0, [item("minecraft:barrel")], "Barrel", section=S_VAN, deps=["sto_vanilla_hub"], xp=10,
      mirror="1659A59303C15CC9", subtitle="A chest with no lid to block", desc=[
        "&eWhat:&r a barrel holds as much as a chest and opens with any block on top, so you can stack them in a wall.",
        "&eHow:&r planks and slabs (check JEI).",
        "&eTip:&r a wall of barrels with item frames is a fine early sorting room."]),
    Q("sto_ender_chest", 0, 0, [item("minecraft:ender_chest")], "Ender Chest", section=S_VAN, deps=["sto_vanilla_hub", "t2_obsidian"], xp=30,
      mirror="25AFD10D008DF30B", subtitle="One private inventory, everywhere", desc=[
        "&eWhat:&r every Ender Chest you open shows the same 27 slots, and only you can see yours.",
        "&eHow:&r 8 obsidian around an eye of ender.",
        "&eTip:&r keep spare tools and a water bucket in it; any Ender Chest becomes an emergency kit."]),
    Q("sto_rails", 0, 0, [item("minecraft:chest_minecart")], "Chest Minecart", section=S_VAN, deps=["sto_vanilla_hub"], xp=15,
      mirror="33AADC1B97E9F7A9", subtitle="Haul a chest by rail", desc=[
        "&eWhat:&r a chest on wheels: a minecart that carries 27 stacks along rails. A hopper under the track at home empties it as it rolls by.",
        "&eChemistry:&r steel wheels on steel rails have very low rolling resistance, which is why one locomotive can pull thousands of tonnes.",
        "&eHow:&r a minecart (5 iron) plus a chest (check JEI). Powered rails keep it moving.",
        "&eTip:&r a hopper minecart (also in JEI) loads itself from containers it passes under."]),
    Q("sto_chest_boat", 0, 0, [anytag("minecraft:chest_boats")], "Chest Boat", section=S_VAN, deps=["sto_vanilla_hub"], xp=15,
      mirror="544791880F315D5A", subtitle="Cargo by river", desc=[
        "&eWhat:&r a boat with a chest in it. Any wood works.",
        "&eHow:&r a boat plus a chest, shapeless (check JEI).",
        "&eTip:&r rivers run a long way in this pack's biomes; a chest boat is the cheapest long-distance freight before rails."]),
    Q("sto_hopper", 0, 0, [item("minecraft:hopper", 2)], "Hoppers", section=S_VAN, deps=["sto_vanilla_hub", "gs_iron"], xp=15,
      **OPT, subtitle="Optional: the first item mover", desc=[
        "&eWhat:&r a hopper pulls items from the container above it and pushes them into the one it points at.",
        "&eHow:&r 5 iron ingots around a chest (Utilitarian also has a log recipe; check JEI).",
        "&eTip:&r a redstone signal locks a hopper, which makes simple item gates."]),

    # ===== Functional Storage (ATM10 left) =====================================================
    Q("sto_fs_hub", 0, 0, [item("minecraft:chest")], "Functional Storage", section=S_FS, deps=["sto_hub"], xp=15, icon="functionalstorage:oak_1",
      size=1.5, shape="hexagon", mirror="0682DC1F2417DAEB", subtitle="Drawers: one item each, thousands deep", desc=[
        "&6You remember shelves that went on forever. Drawers are the closest thing to them.&r",
        "&eWhat:&r Functional Storage drawers hold a lot of a single item and show it on the front. They're the backbone of a bulk store: cobblestone, dusts, ingots, salts.",
        "&eHow:&r every drawer starts with a chest in the middle of its recipe, so bring one. The first drawer is the next quest.",
        "&eTip:&r a drawer wall behind a Storage Controller is one inventory for pipes, and later for AE2."]),
    Q("s_drawers", 0, 0, [anytag("functionalstorage:drawer")], "Your First Drawer", section=S_FS, deps=["sto_fs_hub"], xp=25,
      size=1.5, shape="hexagon", mirror="2746575C929B6C50", subtitle="Any drawer of any wood", desc=[
        "&eWhat:&r a drawer of any wood with 1, 2 or 4 slots. Right-click to insert, left-click to take one, sneak-left-click for a stack.",
        "&eHow:&r planks and a chest in the drawer shape (check JEI).",
        "&eTip:&r double-right-click with an item to pour in every matching stack from your inventory."]),
    Q("sto_fs_tools", 0, 0, [item("functionalstorage:linking_tool")], "Linking Tool", section=S_FS, deps=["s_drawers"], xp=30,
      size=1.5, shape="hexagon", mirror="072FBEB0F6F1BC48", subtitle="Join far-away drawers to a controller", desc=[
        "&eWhat:&r the Linking Tool adds drawers that aren't touching a Storage Controller to its network, and pairs Ender Drawers.",
        "&eHow:&r check JEI. Right-click the controller to start, then right-click each drawer. Holding the tool shows what's linked.",
        "&eTip:&r link a drawer at your mine entrance so ore pours straight into the wall at home."]),
    Q("s_fs_controller", 0, 0, [anyof(["functionalstorage:storage_controller", "functionalstorage:framed_storage_controller"])], "Drawer Controller",
      section=S_FS, deps=["sto_fs_tools"], xp=50, size=1.5, shape="hexagon", mirror="6FBAE89EE782DABA", subtitle="One face for every drawer", desc=[
        "&eWhat:&r the Storage Controller links nearby drawers into one inventory you (and pipes, hoppers and AE2 storage buses) can use.",
        "&eHow:&r place it among your drawers (check JEI). Drawers touching it or linked with the Linking Tool join the network.",
        "&eTip:&r one pipe into the controller is a sorting system: each item goes to the drawer that already holds it."]),
    Q("sto_fs_access", 0, 0, [item("functionalstorage:controller_extension")], "Controller Extension", section=S_FS, deps=["s_fs_controller"], xp=25,
      size=1.5, shape="hexagon", mirror="61A22707DBC83818", subtitle="A second door into your drawer wall", desc=[
        "&eWhat:&r an extension works like the controller itself: pipes and players reach the whole drawer network through it.",
        "&eHow:&r check JEI, then link it with the Linking Tool.",
        "&eTip:&r one by the smelters, one by the crafting bench."]),
    Q("sto_fs_simple", 0, 0, [item("functionalstorage:simple_compacting_drawer")], "Simple Compacting Drawer", section=S_FS, deps=["sto_fs_tools"], xp=25,
      mirror="4E4C8BCD45766F03", subtitle="Two forms of one thing", desc=[
        "&eWhat:&r stores two forms of one item (ingot and block, say) as a single pool and hands out whichever you ask for.",
        "&eHow:&r check JEI. Insert the item you want it to track.",
        "&eTip:&r good for things with no nugget form, like coal and coal blocks."]),
    Q("s_fs_compacting", 0, 0, [item("functionalstorage:compacting_drawer")], "Compacting Drawer", section=S_FS, deps=["sto_fs_tools"], xp=40,
      mirror="2B422B7E0CE3590D", subtitle="Nuggets, ingots and blocks as one stock", desc=[
        "&eWhat:&r a compacting drawer stores nuggets, ingots and blocks of one metal as a single pool.",
        "&eChemistry:&r a block holds the same metal atoms as 9 ingots; only the packing changes, so nothing is lost either way.",
        "&eHow:&r craft it (check JEI), then insert the item you want to track.",
        "&eTip:&r perfect for copper and tin next to your bronze setup."]),
    Q("sto_fs_framed", 0, 0, [anyof(["functionalstorage:framed_1", "functionalstorage:framed_2", "functionalstorage:framed_4",
                                      "functionalstorage:compacting_framed_drawer", "functionalstorage:framed_storage_controller",
                                      "functionalstorage:framed_controller_extension", "functionalstorage:framed_simple_compacting_drawer"])],
      "Framed Drawers", section=S_FS, deps=["sto_fs_tools"], xp=25, mirror="1310C1E14C259807", subtitle="Drawers in any block's clothes", desc=[
        "&eWhat:&r framed drawers and controllers take on the texture of blocks you give them, so a drawer wall can match your lab.",
        "&eHow:&r craft the framed version (check JEI), then sneak-right-click it with the blocks you want for its frame and face.",
        "&eTip:&r framed drawers work exactly like normal ones, upgrades included."]),
    Q("sto_fs_config", 0, 0, [item("functionalstorage:configuration_tool")], "Configuration Tool", section=S_FS, deps=["sto_fs_tools"], xp=25,
      mirror="508A8366219175FE", subtitle="Lock, hide and tidy", desc=[
        "&eWhat:&r the Configuration Tool locks drawers to their item, toggles the count and item display, and more.",
        "&eHow:&r check JEI. Sneak-use cycles its mode; the mode shows on the item.",
        "&eTip:&r lock every drawer in a sorting wall, so an empty drawer still only accepts its own item."]),
    Q("s_fs_fluid", 0, 0, [anyof(["functionalstorage:fluid_1", "functionalstorage:fluid_2", "functionalstorage:fluid_4"])], "Fluid Drawers",
      section=S_FS, deps=["sto_fs_tools"], xp=40, mirror="38F9E9A830D3EA0C", subtitle="Drawers for liquids", desc=[
        "&eWhat:&r fluid drawers store a fluid instead of items, and show it on the front.",
        "&eChemistry:&r handy for small stocks of acids: one drawer of H₂SO₄, one of HCl, one of HNO₃. A real lab keeps acids in separate, labelled containers too.",
        "&eHow:&r check JEI for the 1, 2 and 4 slot versions. Pipes and MI fluid pipes fill and drain them; storage upgrades work on them."]),
    Q("s_fs_ender", 0, 0, [item("functionalstorage:ender_drawer")], "Ender Drawer", section=S_FS, deps=["sto_fs_tools"], xp=40,
      mirror="1A4B1CA7EC15348E", subtitle="One drawer, many places", desc=[
        "&eWhat:&r every Ender Drawer with the same frequency shares one inventory, wherever it is.",
        "&eHow:&r check JEI. Pair drawers with the Linking Tool.",
        "&eTip:&r put one at your mine and one at your smelters to send ore home."]),
    Q("sto_fs_collector", 0, 0, [item("functionalstorage:collector_upgrade")], "Collector Upgrade", section=S_FS, deps=["s_drawers"], xp=25,
      mirror="11D4EEAC61C7E530", subtitle="A drawer that picks up drops", desc=[
        "&eWhat:&r a drawer with a Collector Upgrade pulls in matching items dropped nearby.",
        "&eHow:&r check JEI. Right-click the drawer to open its upgrade slots.",
        "&eTip:&r under a cobblestone generator or a mob farm's drop point it replaces a hopper line."]),
    Q("sto_fs_redstone", 0, 0, [item("functionalstorage:redstone_upgrade")], "Redstone Upgrade", section=S_FS, deps=["s_drawers"], xp=25,
      mirror="70902EF96F060672", subtitle="A signal that reads the drawer", desc=[
        "&eWhat:&r the Redstone Upgrade makes a drawer emit a signal based on how full it is (or full / empty, by mode).",
        "&eHow:&r check JEI. Put it in the drawer's utility slot and cycle its mode.",
        "&eTip:&r wire it to a machine so a cobblestone drawer that's full switches the generator off."]),
    Q("sto_fs_tiers", 0, 0, [item("functionalstorage:copper_upgrade")], "Copper Upgrade", section=S_FS, deps=["s_drawers"], xp=25,
      mirror="485D5664A17E16DF", subtitle="The first capacity step", desc=[
        "&eWhat:&r storage upgrades multiply how much a drawer holds. Copper is the first and cheapest.",
        "&eChemistry:&r copper (8.96 g/cm³) is soft and malleable, which is why it was the first metal people worked.",
        "&eHow:&r copper ingots and blocks, chests and a drawer (check JEI). Right-click the drawer to open its upgrade slots."]),
    Q("sto_fs_gold", 0, 0, [item("functionalstorage:gold_upgrade")], "Gold Upgrade", section=S_FS, deps=["sto_fs_tiers"], xp=30,
      mirror="3B570B3DB5F6D2CB", subtitle="More room again", desc=[
        "&eWhat:&r the gold upgrade multiplies a drawer's capacity more than copper.",
        "&eChemistry:&r gold is the most malleable metal there is: one gram beats into a square metre of leaf.",
        "&eHow:&r builds on the copper upgrade (check JEI)."]),
    Q("s_fs_upgrade", 0, 0, [item("functionalstorage:diamond_upgrade")], "Diamond Upgrade", section=S_FS, deps=["sto_fs_gold"], xp=40,
      mirror="1B72E95569B07E18", subtitle="A very deep drawer", desc=[
        "&eWhat:&r the diamond upgrade is the big step: one drawer holds a serious stockpile.",
        "&eHow:&r builds on the gold upgrade (check JEI).",
        "&eTip:&r the Iron Downgrade does the reverse, limiting a drawer to a single stack per slot."]),
    Q("sto_fs_netherite", 0, 0, [item("functionalstorage:netherite_upgrade")], "Netherite Upgrade", section=S_FS, deps=["s_fs_upgrade", "t2_nether"], xp=60,
      mirror="0E5AE195158CF344", subtitle="The biggest drawer there is", desc=[
        "&eWhat:&r the top drawer upgrade. One drawer holds an absurd amount of a single item.",
        "&eHow:&r smithing table: netherite upgrade template + diamond upgrade + netherite ingot.",
        "&eTip:&r save it for cobblestone, raw ore or dust, the things you have tens of thousands of."]),
    Q("sto_fs_downgrade", 0, 0, [item("functionalstorage:iron_downgrade")], "Iron Downgrade", section=S_FS, deps=["s_drawers"], xp=20,
      mirror="122FBF5110E4CFF2", subtitle="Hold less, on purpose", desc=[
        "&eWhat:&r the Iron Downgrade limits a drawer to one stack per slot.",
        "&eHow:&r check JEI.",
        "&eTip:&r useful for a drawer that feeds a machine: it keeps a small buffer instead of swallowing your whole stock."]),
    Q("sto_fs_void", 0, 0, [item("functionalstorage:void_upgrade")], "Void Upgrade", section=S_FS, deps=["s_drawers"], xp=25,
      mirror="1CACE201C6AA0913", subtitle="Delete the overflow", desc=[
        "&eWhat:&r a drawer with a Void Upgrade destroys whatever doesn't fit, so a full drawer never backs up a pipe.",
        "&eChemistry:&r real matter can't vanish (mass is conserved in every chemical reaction). In Minecraft, it can.",
        "&eHow:&r check JEI.",
        "&eTip:&r a void-upgraded cobblestone drawer at the end of a quarry line keeps everything flowing."]),
    Q("sto_fs_pusher", 0, 0, [item("functionalstorage:pusher_upgrade")], "Pusher Upgrade", section=S_FS, deps=["s_drawers"], xp=25,
      mirror="19DFAEB6D88F3580", subtitle="A drawer that feeds a machine", desc=[
        "&eWhat:&r the Pusher pushes the drawer's items into the block it faces. No pipes needed.",
        "&eHow:&r check JEI. Put it in the drawer's utility slot and set its direction in the drawer's menu.",
        "&eTip:&r a drawer of coal with a Pusher behind a row of furnaces keeps them fuelled."]),
    Q("s_fs_puller", 0, 0, [item("functionalstorage:puller_upgrade")], "Puller Upgrade", section=S_FS, deps=["s_drawers"], xp=25,
      mirror="7649D648A3688D4A", subtitle="A drawer that empties a machine", desc=[
        "&eWhat:&r the Puller pulls items from the block it faces into the drawer.",
        "&eHow:&r check JEI. Utility slot, set the direction in the drawer's menu.",
        "&eTip:&r a drawer with a Puller behind a macerator collects all the dust without a single pipe."]),

    # ===== Sophisticated Storage (ATM10 upper right) ===========================================
    Q("s_barrel", 0, 0, [anytag("sophisticatedstorage:base_tier_wooden_storage")], "Sophisticated Storage", section=S_SS, deps=["sto_hub"], xp=25,
      size=1.5, shape="hexagon", mirror="5E4BC0F59C90433A", subtitle="Chests and barrels that grow with you", desc=[
        "&6You remember vaults that answered to a word. These answer to upgrade cards, which is nearly as good.&r",
        "&eWhat:&r Sophisticated Storage chests, barrels, limited barrels and shulker boxes take upgrade cards (stack, compacting, hopper, filters) and tier upgrades, just like your backpack.",
        "&eHow:&r craft any wooden chest or barrel of the mod (check JEI).",
        "&eTip:&r barrels keep their contents when broken, so moving a full one is easy."]),
    Q("sto_ss_copper", 0, 0, [anyof(["sophisticatedstorage:copper_chest", "sophisticatedstorage:copper_barrel"])], "Copper Tier", section=S_SS, deps=["s_barrel"], xp=20,
      **OPT, mirror="0CD04A00529FE1C9", subtitle="Optional: the first small step up", desc=[
        "&eWhat:&r the copper tier sits between wood and iron: a few more slots for a little copper.",
        "&eChemistry:&r copper tarnishes green: over years it forms a patina of basic copper carbonate, Cu₂CO₃(OH)₂, which then protects the metal underneath.",
        "&eHow:&r a copper chest or barrel from JEI, or a basic-to-copper tier upgrade right-clicked on a placed wooden one."]),
    Q("s_ss_tier", 0, 0, [anyof(["sophisticatedstorage:iron_chest", "sophisticatedstorage:iron_barrel"])], "Iron Tier", section=S_SS, deps=["s_barrel"], xp=25,
      any_dep=True, mirror="58514FDE153FD971", subtitle="More slots without emptying anything", desc=[
        "&eWhat:&r the iron tier: more slots and more upgrade slots.",
        "&eHow:&r craft an iron chest or barrel, or use a tier upgrade (basic → iron skips copper) on the placed container: nothing inside moves.",
        "&eTip:&r the Decoration Table re-skins chests and barrels with any wood or block, so your storage room can match your base."]),
    Q("sto_ss_ladder", 0, 0, [anyof(["sophisticatedstorage:gold_chest", "sophisticatedstorage:gold_barrel"])], "Gold Tier", section=S_SS, deps=["s_ss_tier"], xp=40,
      mirror="3E33730DC2115D26", subtitle="Climb the ladder one tier at a time", desc=[
        "&eWhat:&r the gold tier, with more slots and upgrade slots again.",
        "&eHow:&r check JEI, or an iron-to-gold tier upgrade on the placed chest or barrel.",
        "&eTip:&r upgrade the barrel your ore line feeds first; it fills fastest."]),
    Q("sto_ss_diamond", 0, 0, [anyof(["sophisticatedstorage:diamond_chest", "sophisticatedstorage:diamond_barrel"])], "Diamond Tier", section=S_SS, deps=["sto_ss_ladder"], xp=50,
      mirror="4C0BDD483CCB40C4", subtitle="The tier before netherite", desc=[
        "&eWhat:&r the diamond tier. Enough upgrade slots for stack upgrades, a hopper and a filter at once.",
        "&eChemistry:&r diamond is pure carbon, the same element as the coal in your furnace, arranged in a lattice where every atom bonds to four others.",
        "&eHow:&r check JEI, or a gold-to-diamond tier upgrade on the placed container."]),
    Q("sto_ss_netherite", 0, 0, [anyof(["sophisticatedstorage:netherite_barrel", "sophisticatedstorage:netherite_chest"])], "Netherite Tier", section=S_SS, deps=["sto_ss_diamond", "t2_nether"], xp=75,
      mirror="77F241BEE9902751", subtitle="The top tier", desc=[
        "&eWhat:&r the netherite tier has the most slots and upgrade slots of any Sophisticated container.",
        "&eHow:&r check JEI, or a diamond-to-netherite tier upgrade on a placed diamond chest or barrel.",
        "&eTip:&r a netherite barrel full of stack upgrades holds a staggering amount."]),
    Q("sto_ss_base", 0, 0, [item("sophisticatedstorage:upgrade_base")], "Upgrade Base", section=S_SS, deps=["s_barrel"], xp=15,
      mirror="4007DFA7CC3A5FF2", subtitle="The blank every upgrade starts from", desc=[
        "&eWhat:&r every Sophisticated Storage upgrade card starts from an upgrade base.",
        "&eHow:&r planks and iron ingots in a checker pattern. The backpack mod has its own base; JEI shows both.",
        "&eTip:&r make a few at a time; you'll want stack, hopper and compacting upgrades soon."]),
    Q("s_ss_controller", 0, 0, [item("sophisticatedstorage:controller")], "Storage Controller", section=S_SS, deps=["s_barrel"], xp=50,
      size=1.5, shape="hexagon", mirror="1FE17B1C7C639F88", subtitle="Many containers, one inventory", desc=[
        "&eWhat:&r the Controller joins touching Sophisticated containers into one inventory. Right-click it with an item and it goes to the container that already holds that item.",
        "&eHow:&r place it next to your chests and barrels (check JEI). Pipes into the controller reach every connected container.",
        "&eTip:&r one pipe into the controller is a sorting system; a storage bus on it later gives AE2 the whole room."]),
    Q("sto_ss_tool", 0, 0, [item("sophisticatedstorage:storage_tool")], "Storage Tool", section=S_SS, deps=["s_ss_controller"], xp=25,
      mirror="78E51D22C16C4686", subtitle="Link and lock from a distance", desc=[
        "&eWhat:&r the Storage Tool links containers to a controller without touching it and toggles settings like locks and displays.",
        "&eHow:&r an ender pearl, iron, sticks and a redstone torch (check JEI). Its tooltip lists each mode.",
        "&eTip:&r locked slots keep their item type even when empty, so a sorting system never fills them with junk."]),
    Q("sto_ss_link", 0, 0, [item("sophisticatedstorage:storage_link")], "Storage Link", section=S_SS, deps=["s_ss_controller", "sto_ss_tool"], xp=30,
      mirror="0108F3EFDFD6DFD0", subtitle="Reach containers the controller can't touch", desc=[
        "&eWhat:&r a Storage Link joins containers that aren't touching the controller's group, within the controller's range.",
        "&eHow:&r check JEI. Place it against the far container (or group) and link it with the Storage Tool.",
        "&eTip:&r a link under the floor joins a second storage room without a wall of cables."]),
    # --- our own Sophisticated Storage extras (ATM10 has none of these): optional, off the nearest quest
    Q("sto_ss_chest", 0, 0, [item("sophisticatedstorage:chest")], "Sophisticated Chest", section=S_SS, deps=["s_barrel"], xp=15,
      **OPT, subtitle="Optional: the same upgrades, in chest form", desc=[
        "&eWhat:&r Sophisticated chests take the same tier upgrades and upgrade cards as the barrels, and show their contents in a double-chest layout.",
        "&eHow:&r a wooden chest version (check JEI).",
        "&eTip:&r chests connect to the controller the same way barrels do."]),
    Q("sto_ss_limited", 0, 0, [item("sophisticatedstorage:limited_barrel_1"), item("sophisticatedstorage:limited_barrel_4")], "Limited Barrels", section=S_SS, deps=["s_barrel"], xp=30,
      **OPT, subtitle="Optional: drawer-style barrels with a few huge slots", desc=[
        "&eWhat:&r limited barrels have one to four big slots and show their items on the front, like drawers, but take Sophisticated upgrades.",
        "&eHow:&r check JEI for each size. They use the same tier upgrades as normal barrels.",
        "&eTip:&r a four-slot limited barrel per metal (ore, dust, ingot, block) makes a tidy wall."]),
    Q("sto_ss_shulker", 0, 0, [item("sophisticatedstorage:shulker_box")], "Sophisticated Shulker Box", section=S_SS, deps=["sto_ss_chest", "w_end"], xp=60,
      **OPT, subtitle="Optional: upgradeable storage you can carry", desc=[
        "&eWhat:&r a shulker box that takes tier upgrades and upgrade cards, and keeps everything inside when you pick it up.",
        "&eHow:&r a chest, two shulker shells and a lever (check JEI). Shulkers live in End cities.",
        "&eTip:&r a shulker box with a compacting upgrade is a portable ore bank for long mining trips."]),
    Q("sto_ss_netherite_kit", 0, 0, [item("sophisticatedstorage:diamond_to_netherite_tier_upgrade")], "Tier Upgrade Kits", section=S_SS, deps=["sto_ss_netherite"], xp=40,
      **OPT, subtitle="Optional: upgrade in place instead of crafting anew", desc=[
        "&eWhat:&r tier upgrades turn a placed chest or barrel into the next tier without moving a thing. This one is the last step, diamond to netherite.",
        "&eHow:&r a lever and a netherite ingot, shapeless (check JEI for the other steps).",
        "&eTip:&r every item and upgrade card inside stays where it was."]),
    Q("s_ss_stack", 0, 0, [item("sophisticatedstorage:stack_upgrade_tier_1")], "Stack Upgrades", section=S_SS, deps=["sto_ss_base"], xp=40,
      **OPT, subtitle="Optional: more items in every slot", desc=[
        "&eWhat:&r stack upgrades multiply how many items fit in each slot of a chest or barrel. Higher tiers multiply more.",
        "&eHow:&r an upgrade base and storage blocks (check JEI). Insert it in an upgrade slot.",
        "&eTip:&r a barrel with a few stack upgrades holds a whole mine's worth of cobblestone or raw ore."]),
    Q("s_ss_compacting", 0, 0, [item("sophisticatedstorage:compacting_upgrade")], "Compacting Upgrade", section=S_SS, deps=["sto_ss_base"], xp=40,
      **OPT, subtitle="Optional: nuggets to ingots to blocks, automatically", desc=[
        "&eWhat:&r the Compacting Upgrade squeezes 9 nuggets into an ingot and 9 ingots into a block as items arrive.",
        "&eChemistry:&r a block holds the same metal atoms as 9 ingots; only the packing changes, so no mass is lost either way.",
        "&eHow:&r craft it (check JEI) and put it in an upgrade slot. Add a filter so it only compacts what you choose."]),
    Q("sto_ss_compression", 0, 0, [item("sophisticatedstorage:compression_upgrade")], "Compression Upgrade", section=S_SS, deps=["s_ss_compacting"], xp=40,
      **OPT, subtitle="Optional: nuggets, ingots and blocks as one stock", desc=[
        "&eWhat:&r the Compression Upgrade links a few slots so nuggets, ingots and blocks of one material count as a single stock.",
        "&eHow:&r an upgrade base, pistons, iron and redstone (check JEI). Choose which slots it uses in the upgrade tab.",
        "&eTip:&r take out exactly the form you need: blocks for storage, ingots for crafting, nuggets for small recipes."]),
    Q("sto_ss_hopper", 0, 0, [item("sophisticatedstorage:hopper_upgrade")], "Hopper Upgrade", section=S_SS, deps=["sto_ss_base"], xp=30,
      **OPT, subtitle="Optional: containers that pull and push themselves", desc=[
        "&eWhat:&r the Hopper Upgrade pulls items from one side and pushes them out another, with filters.",
        "&eHow:&r an upgrade base, a hopper, iron and redstone (check JEI). Set directions and filters in the container's upgrade tab.",
        "&eTip:&r a barrel with a hopper upgrade under a machine's output collects everything without pipes."]),
    Q("sto_ss_io", 0, 0, [item("sophisticatedstorage:storage_input"), item("sophisticatedstorage:storage_output")], "Storage Input and Output", section=S_SS, deps=["s_ss_controller"], xp=40,
      **OPT, subtitle="Optional: separate doors into your storage", desc=[
        "&eWhat:&r Storage Input only accepts items into the controller's containers; Storage Output only lets them out. Pipes and hoppers use them like any inventory.",
        "&eHow:&r a wooden storage block, gold, planks and a repeater (check JEI). Place them touching the controller's group.",
        "&eTip:&r put an Input at the end of your ore line and an Output by your crafting area, so the two never mix."]),
    Q("s_ss_minecart", 0, 0, [item("sophisticatedstorageinmotion:storage_minecart")], "Storage in Motion", section=S_SS, deps=["s_ss_tier"], xp=40,
      **OPT, subtitle="Optional: Sophisticated chests on rails and water", desc=[
        "&eWhat:&r Sophisticated Storage in Motion puts upgradeable chests and barrels on minecarts, boats and rafts, upgrades and all.",
        "&eHow:&r combine a minecart with a Sophisticated chest or barrel (check JEI). Boats and rafts work the same way.",
        "&eTip:&r a hopper upgrade on a storage minecart makes a simple ore train between your mine and base."]),

    # ===== Sophisticated Backpacks (ATM10 lower right) =========================================
    Q("gs_backpack", 0, 0, [item("sophisticatedbackpacks:backpack")], "A Backpack", section=S_BP, deps=["gs_leather", "gs_chest", "sto_hub"], xp=20,
      size=1.5, shape="hexagon", mirror="6A2B2C5E2ADCE366", subtitle="More pockets, upgradeable later", desc=[
        "&6You remember carrying whole worlds. For now, a leather bag will do.&r",
        "&eWhat:&r more inventory, and it can be upgraded later (pickup, magnet, feeding and more).",
        "&eHow:&r leather, string and a chest (check JEI for the shape). Wear it in the chest slot or keep it in your inventory.",
        "&eTip:&r take it on your first mining trip. The upgrade base is also sold in the Demigod Token shop."]),
    Q("sto_bp_copper", 0, 0, [item("sophisticatedbackpacks:copper_backpack")], "Copper Backpack", section=S_BP, deps=["gs_backpack"], xp=20,
      **OPT, mirror="0E057B7F76401421", subtitle="Optional: one small step before iron", desc=[
        "&eWhat:&r the copper backpack sits between leather and iron: a few more slots and an extra upgrade slot.",
        "&eHow:&r surround your backpack with copper ingots (check JEI). Everything inside stays put.",
        "&eTip:&r copper is plentiful early, so this is the cheapest upgrade in the line."]),
    # iron backpack: q_bp_iron (qol.py, mirror 2F9B0C642A6BE30C)
    Q("sto_bp_gold", 0, 0, [item("sophisticatedbackpacks:gold_backpack")], "Gold Backpack", section=S_BP, deps=["q_bp_iron"], xp=40,
      mirror="45268A619787288F", subtitle="More rows, more upgrade slots", desc=[
        "&eWhat:&r the gold backpack adds inventory rows and upgrade slots over the iron one.",
        "&eHow:&r surround an iron backpack with eight gold ingots. Everything inside stays put.",
        "&eTip:&r spend the new upgrade slot on a stack upgrade; it multiplies every slot at once."]),
    Q("sto_bp_diamond", 0, 0, [item("sophisticatedbackpacks:diamond_backpack")], "Diamond Backpack", section=S_BP, deps=["sto_bp_gold"], xp=60,
      mirror="67704F7341EDCC49", subtitle="Room for a whole lab's worth of reagents", desc=[
        "&eWhat:&r the diamond backpack is the tier before netherite: even more rows and upgrade slots.",
        "&eHow:&r surround a gold backpack with eight diamonds.",
        "&eTip:&r netherite comes after it (the Netherite Backpack quest, on the Quality of Life page)."]),
    # netherite backpack: q_bp_netherite (qol.py, mirror 46D756F4DC6CC894)
    Q("sto_bp_base", 0, 0, [item("sophisticatedbackpacks:upgrade_base")], "Backpack Upgrade Base", section=S_BP, deps=["gs_backpack"], xp=15,
      mirror="1FE052F643401232", subtitle="The blank behind every backpack upgrade", desc=[
        "&eWhat:&r every backpack upgrade starts from this base. The upgrades below each add one thing the pack does by itself.",
        "&eHow:&r leather, string and iron (check JEI). It's also in the Demigod Token shop.",
        "&eTip:&r upgrades go in the slots on the left of the backpack screen; sneak-right-click the slot to open an upgrade's settings."]),
    Q("sto_bp_tank", 0, 0, [item("sophisticatedbackpacks:tank_upgrade")], "Tank Upgrade", section=S_BP, deps=["sto_bp_base"], xp=40,
      **OPT, mirror="0D4C64DD58567758", subtitle="Optional: carry fluids in your backpack", desc=[
        "&eWhat:&r the Tank Upgrade stores fluid inside the backpack. Fill and empty it with buckets or tanks from its upgrade tab.",
        "&eChemistry:&r a real acid needs the right container: HF eats glass, so it's kept in PTFE; concentrated H₂SO₄ can sit in steel. A backpack tank isn't fussy.",
        "&eHow:&r an upgrade base surrounded by glass (check JEI).",
        "&eTip:&r a tank of water means you're never stuck in a lava cave without a way to cool it into obsidian."]),
    # pickup + magnet: q_bp_up (qol.py, mirror 0E0CAA31480EC0A1 / 110D27EA86CDA62B)
    Q("sto_bp_advanced", 0, 0, [item("sophisticatedbackpacks:advanced_pickup_upgrade")], "Advanced Pickup", section=S_BP, deps=["q_bp_up"], xp=40,
      **OPT, mirror="1985CFD1F0425E88", subtitle="Optional: more filter slots, tag and mod filters", desc=[
        "&eWhat:&r the advanced pickup upgrade has more filter slots and can filter by tag, mod or durability.",
        "&eHow:&r the basic pickup upgrade with gold, diamonds and redstone (check JEI).",
        "&eTip:&r a tag filter for 'c:raw_materials' picks up every raw ore in the pack with one entry."]),
    Q("sto_bp_adv_magnet", 0, 0, [item("sophisticatedbackpacks:advanced_magnet_upgrade")], "Advanced Magnet", section=S_BP, deps=["q_bp_up"], xp=40,
      **OPT, mirror="11D57C768032E3F7", subtitle="Optional: a wider pull and finer filters", desc=[
        "&eWhat:&r the advanced magnet pulls drops from further away, with the advanced filter slots.",
        "&eChemistry:&r a real magnet only pulls iron, nickel, cobalt and a few alloys. This one is less picky.",
        "&eHow:&r the basic magnet upgrade with gold, diamonds and redstone (check JEI)."]),
    Q("sto_bp_smelting", 0, 0, [item("sophisticatedbackpacks:smelting_upgrade")], "Smelting Upgrade", section=S_BP, deps=["sto_bp_base"], xp=30,
      **OPT, mirror="668C313FF46B6005", subtitle="Optional: a furnace in your backpack", desc=[
        "&eWhat:&r the Smelting Upgrade is a furnace in the backpack screen, burning fuel from the backpack.",
        "&eChemistry:&r smelting iron ore is a reduction: carbon monoxide strips the oxygen off the ore, Fe₂O₃ + 3CO → 2Fe + 3CO₂.",
        "&eHow:&r an upgrade base and a furnace (check JEI).",
        "&eTip:&r smelt your raw ore on the walk home."]),
    Q("sto_bp_auto_smelting", 0, 0, [item("sophisticatedbackpacks:auto_smelting_upgrade")], "Auto-Smelting Upgrade", section=S_BP, deps=["sto_bp_smelting"], xp=40,
      **OPT, mirror="3A1D07AED2A841E4", subtitle="Optional: it smelts by itself", desc=[
        "&eWhat:&r the Auto-Smelting Upgrade smelts matching items inside the backpack on its own, using fuel from the backpack.",
        "&eHow:&r the smelting upgrade with a hopper, gold, redstone and a diamond (check JEI).",
        "&eTip:&r filter it to raw ores only, or it will smelt your logs into charcoal too."]),
    Q("sto_bp_pump", 0, 0, [item("sophisticatedbackpacks:pump_upgrade")], "Pump Upgrade", section=S_BP, deps=["sto_bp_base"], xp=30,
      **OPT, mirror="6E9041744C592573", subtitle="Optional: fill the tank from the world", desc=[
        "&eWhat:&r the Pump Upgrade fills and empties the backpack's tank from blocks in the world or from tanks you click on.",
        "&eHow:&r an upgrade base with buckets, glass, a piston and a sticky piston (check JEI). It needs a Tank Upgrade to work with.",
        "&eTip:&r set it to 'fill' on a water source and the tank is never empty."]),
    Q("sto_bp_adv_pump", 0, 0, [item("sophisticatedbackpacks:advanced_pump_upgrade")], "Advanced Pump", section=S_BP, deps=["sto_bp_pump"], xp=40,
      **OPT, mirror="56B80A7EBFE21428", subtitle="Optional: faster, with filters", desc=[
        "&eWhat:&r the advanced pump moves fluid faster and filters which fluids it touches.",
        "&eHow:&r the pump upgrade with gold, diamonds and redstone (check JEI)."]),
    Q("sto_bp_xp_pump", 0, 0, [item("sophisticatedbackpacks:xp_pump_upgrade")], "Experience Pump", section=S_BP, deps=["sto_bp_adv_pump"], xp=40,
      **OPT, mirror="6E3D53D1C4569A89", subtitle="Optional: bank your levels", desc=[
        "&eWhat:&r the XP Pump stores your experience as fluid in the backpack's tank and gives it back on demand.",
        "&eHow:&r an advanced pump upgrade with ender eyes, bottles o' enchanting and redstone (check JEI).",
        "&eTip:&r bank your levels before a risky fight; a grave keeps items, not levels."]),
    Q("sto_bp_battery", 0, 0, [item("sophisticatedbackpacks:battery_upgrade")], "Battery Upgrade", section=S_BP, deps=["sto_bp_base", "t1_power"], xp=40,
      **OPT, mirror="4C2A60FC1F1E0328", subtitle="Optional: FE in your backpack", desc=[
        "&eWhat:&r stores Forge Energy in the backpack, which other upgrades and charging tools can use.",
        "&eChemistry:&r a battery stores energy as chemistry: two electrodes with different appetites for electrons, kept apart by an electrolyte.",
        "&eHow:&r an upgrade base with gold ingots and redstone blocks (check JEI).",
        "&eTip:&r charge it at home, then top up your jetpack or Mining Gadget in the field."]),
    Q("sto_bp_deposit", 0, 0, [item("sophisticatedbackpacks:deposit_upgrade")], "Deposit Upgrade", section=S_BP, deps=["sto_bp_base"], xp=30,
      **OPT, mirror="00DB5495C3A44999", subtitle="Optional: empty into a chest in one click", desc=[
        "&eWhat:&r with a Deposit Upgrade, sneak-right-clicking a container with the backpack puts matching items into it.",
        "&eHow:&r an upgrade base, a chest, iron, redstone and a piston (check JEI).",
        "&eTip:&r deposit ores into your processing chest in one click when you get home."]),
    Q("sto_bp_adv_deposit", 0, 0, [item("sophisticatedbackpacks:advanced_deposit_upgrade")], "Advanced Deposit", section=S_BP, deps=["sto_bp_deposit"], xp=40,
      **OPT, mirror="4C0EAB9F795686D0", subtitle="Optional: more filter slots", desc=[
        "&eWhat:&r the advanced version with more filter slots and tag filters.",
        "&eHow:&r the deposit upgrade with gold, diamonds and redstone (check JEI)."]),
    Q("sto_bp_cookers", 0, 0, [item("sophisticatedbackpacks:blasting_upgrade")], "Blasting Upgrade", section=S_BP, deps=["sto_bp_base"], xp=30,
      **OPT, mirror="1E499F94A2A193E1", subtitle="Optional: a blast furnace in your pack", desc=[
        "&eWhat:&r the Blasting Upgrade smelts ores and metal at double speed, like a blast furnace, from the backpack screen.",
        "&eChemistry:&r a blast furnace forces air through the fuel so it burns hotter: C + O₂ → CO₂, then CO₂ + C → 2CO, and the CO reduces the ore.",
        "&eHow:&r an upgrade base with a blast furnace, iron and redstone (check JEI).",
        "&eTip:&r one furnace-type upgrade is enough: they share the backpack's fuel."]),
    Q("sto_bp_auto_blasting", 0, 0, [item("sophisticatedbackpacks:auto_blasting_upgrade")], "Auto-Blasting Upgrade", section=S_BP, deps=["sto_bp_cookers"], xp=40,
      **OPT, mirror="26988E22BD019628", subtitle="Optional: ores smelt themselves", desc=[
        "&eWhat:&r the automatic version: it blasts matching items inside the backpack by itself.",
        "&eHow:&r the blasting upgrade with a hopper, gold, redstone and a diamond (check JEI)."]),
    Q("sto_bp_stonecutter", 0, 0, [item("sophisticatedbackpacks:stonecutter_upgrade")], "Stonecutter Upgrade", section=S_BP, deps=["sto_bp_base"], xp=25,
      **OPT, mirror="52672B7FFFD51D16", subtitle="Optional: cut stone without a block", desc=[
        "&eWhat:&r the Stonecutter Upgrade adds a stonecutter to the backpack screen.",
        "&eHow:&r an upgrade base with a stonecutter, iron and redstone (check JEI).",
        "&eTip:&r perfect for Create Deco, Rechiseled and laboratory blocks on a building trip."]),
    Q("sto_bp_filter", 0, 0, [item("sophisticatedbackpacks:filter_upgrade")], "Filter Upgrade", section=S_BP, deps=["sto_bp_base"], xp=25,
      **OPT, mirror="156FF8B7B724DC38", subtitle="Optional: only what you want gets in or out", desc=[
        "&eWhat:&r the Filter Upgrade decides what pipes and hoppers may put into or take out of the backpack.",
        "&eHow:&r an upgrade base with string and redstone (check JEI).",
        "&eTip:&r a backpack in a hopper line with a filter is a cheap sorter."]),
    Q("sto_bp_adv_filter", 0, 0, [item("sophisticatedbackpacks:advanced_filter_upgrade")], "Advanced Filter", section=S_BP, deps=["sto_bp_filter"], xp=40,
      **OPT, mirror="57CF8C6C867B9BDA", subtitle="Optional: filter by tag or mod", desc=[
        "&eWhat:&r more filter slots, plus filters by tag, mod or durability.",
        "&eHow:&r the filter upgrade with gold, diamonds and redstone (check JEI)."]),
    Q("sto_bp_smoking", 0, 0, [item("sophisticatedbackpacks:smoking_upgrade")], "Smoking Upgrade", section=S_BP, deps=["sto_bp_base"], xp=30,
      **OPT, mirror="26A9F402DAE15EA2", subtitle="Optional: cook food twice as fast", desc=[
        "&eWhat:&r the Smoking Upgrade is a smoker in the backpack screen: food only, at double speed.",
        "&eChemistry:&r smoking preserves meat: phenols and other compounds in wood smoke kill microbes and slow the fats going rancid.",
        "&eHow:&r an upgrade base with a smoker, iron and redstone (check JEI)."]),
    Q("sto_bp_auto_smoking", 0, 0, [item("sophisticatedbackpacks:auto_smoking_upgrade")], "Auto-Smoking Upgrade", section=S_BP, deps=["sto_bp_smoking"], xp=40,
      **OPT, mirror="36BCE35215B2B6E9", subtitle="Optional: dinner cooks itself", desc=[
        "&eWhat:&r the automatic version: raw food in the backpack is smoked by itself.",
        "&eHow:&r the smoking upgrade with a hopper, gold, redstone and a diamond (check JEI)."]),
    Q("sto_bp_jukebox", 0, 0, [item("sophisticatedbackpacks:jukebox_upgrade")], "Mixtape", section=S_BP, deps=["sto_bp_base"], xp=20,
      secret=True, loot="secret", mirror="53F861876B991C36", subtitle="Secret: music while you mine", desc=[
        "&6You remember a time when the spheres sang to you. A jukebox in a backpack will have to do.&r",
        "&eWhat:&r the Jukebox Upgrade plays music discs from inside your backpack, wherever you walk.",
        "&eTip:&r it plays to everyone nearby. Choose your disc with care."]),
    # tool swapper: ql_bp_tools (qol.py, mirror 615B9062FE8CCD36)
    Q("sto_bp_adv_tools", 0, 0, [item("sophisticatedbackpacks:advanced_tool_swapper_upgrade")], "Advanced Tool Swapper", section=S_BP, deps=["ql_bp_tools"], xp=40,
      **OPT, mirror="15CD4BFDC56E9510", subtitle="Optional: swap weapons too", desc=[
        "&eWhat:&r the advanced tool swapper also swaps to the right weapon for the mob in front of you, with more filter slots.",
        "&eHow:&r the tool swapper upgrade with gold, diamonds and redstone (check JEI)."]),
    # stack tier 1: ql_bp_stack (qol.py, mirror 7E9E03274A88347D)
    Q("sto_bp_stack", 0, 0, [item("sophisticatedbackpacks:stack_upgrade_tier_2")], "Stack Upgrade II", section=S_BP, deps=["ql_bp_stack"], xp=40,
      **OPT, mirror="785951190FFDAA21", subtitle="Optional: every slot holds more", desc=[
        "&eWhat:&r each stack tier multiplies how many items fit in every backpack slot. Tier 2 multiplies more than tier 1.",
        "&eHow:&r the tier 1 upgrade with better materials (check JEI).",
        "&eTip:&r a backpack full of stacked dust is the cheapest way to move a day's mining to your machines."]),
    Q("sto_bp_stack3", 0, 0, [item("sophisticatedbackpacks:stack_upgrade_tier_3")], "Stack Upgrade III", section=S_BP, deps=["sto_bp_stack"], xp=50,
      **OPT, mirror="0298A17C2AAC5765", subtitle="Optional: bigger again", desc=[
        "&eWhat:&r tier 3 of the stack upgrade.",
        "&eHow:&r the tier 2 upgrade with diamonds (check JEI)."]),
    Q("sto_bp_stack4", 0, 0, [item("sophisticatedbackpacks:stack_upgrade_tier_4")], "Stack Upgrade IV", section=S_BP, deps=["sto_bp_stack3", "t2_debris"], xp=75,
      **OPT, mirror="7AE3C8134F5ED726", subtitle="Optional: the top stack tier", desc=[
        "&eWhat:&r tier 4, the biggest stack multiplier a backpack takes.",
        "&eHow:&r the tier 3 upgrade with netherite (check JEI).",
        "&eTip:&r two of these in a netherite backpack and you can carry a quarry's output."]),
    Q("sto_bp_crafting", 0, 0, [item("sophisticatedbackpacks:crafting_upgrade")], "Crafting Upgrade", section=S_BP, deps=["sto_bp_base"], xp=30,
      **OPT, mirror="4A854CD5EC70733E", subtitle="Optional: a crafting grid in your backpack", desc=[
        "&eWhat:&r adds a 3x3 crafting grid to the backpack screen that can use the backpack's own items.",
        "&eHow:&r an upgrade base, a crafting table, iron and a chest (check JEI).",
        "&eTip:&r JEI's + button fills the backpack grid straight from the backpack."]),
    # feeding: q_bp_feeding (qol.py, mirror 5FA9BC0D8476D322)
    Q("sto_bp_adv_feeding", 0, 0, [item("sophisticatedbackpacks:advanced_feeding_upgrade")], "Advanced Feeding", section=S_BP, deps=["q_bp_feeding"], xp=40,
      **OPT, mirror="1A739D36D5E3B1AD", subtitle="Optional: eats only when it's worth it", desc=[
        "&eWhat:&r the advanced feeding upgrade has more food slots and can be set to eat only when no hunger would be wasted.",
        "&eHow:&r the feeding upgrade with gold, diamonds and redstone (check JEI)."]),
    Q("sto_bp_void", 0, 0, [item("sophisticatedbackpacks:void_upgrade")], "Void Upgrade", section=S_BP, deps=["sto_bp_base"], xp=30,
      **OPT, mirror="7EFBFF5D0DA018E7", subtitle="Optional: delete the junk as you pick it up", desc=[
        "&eWhat:&r the Void Upgrade destroys chosen items as they enter the backpack: cobblestone, dirt, gravel, rotten flesh.",
        "&eChemistry:&r real matter can't vanish (mass is conserved in every chemical reaction). In Minecraft, it can.",
        "&eHow:&r an upgrade base, ender pearls, obsidian and redstone (check JEI). Set the filter carefully.",
        "&eTip:&r keep a stack of cobblestone out of the filter. You'll want it for building and for the Matter Condenser later."]),
    Q("sto_bp_adv_void", 0, 0, [item("sophisticatedbackpacks:advanced_void_upgrade")], "Advanced Void", section=S_BP, deps=["sto_bp_void"], xp=40,
      **OPT, mirror="2FC15D3916DBF4E4", subtitle="Optional: void by tag, and only the overflow", desc=[
        "&eWhat:&r more filter slots, tag filters, and an 'overflow only' mode that keeps one stack and deletes the rest.",
        "&eHow:&r the void upgrade with gold, diamonds and redstone (check JEI)."]),
    Q("sto_bp_inception", 0, 0, [item("sophisticatedbackpacks:inception_upgrade")], "Inception", section=S_BP, deps=["sto_bp_base", "hn_wither"], xp=100,
      optional=True, tokens=2, mirror="7C07D6A33F7ADB02", subtitle="Optional: backpacks within backpacks", desc=[
        "&eWhat:&r with the Inception Upgrade, backpacks stored inside your backpack keep using their own upgrades, and you can open them from the outer one.",
        "&eHow:&r an upgrade base with ender eyes, diamonds and a Nether Star (check JEI).",
        "&eTip:&r a small 'mining' backpack inside your main one keeps its magnet and void settings separate."]),
    Q("sto_bp_compacting", 0, 0, [item("sophisticatedbackpacks:compacting_upgrade")], "Compacting Upgrade", section=S_BP, deps=["sto_bp_base"], xp=30,
      **OPT, mirror="1CD2C6AFD788C35E", subtitle="Optional: nuggets to ingots as you walk", desc=[
        "&eWhat:&r the Compacting Upgrade squeezes 9 of something into its block as you pick it up.",
        "&eHow:&r an upgrade base with pistons, iron and redstone (check JEI).",
        "&eTip:&r compact redstone, lapis and coal while mining; whole blocks take a ninth of the space."]),
    Q("sto_bp_adv_compacting", 0, 0, [item("sophisticatedbackpacks:advanced_compacting_upgrade")], "Advanced Compacting", section=S_BP, deps=["sto_bp_compacting"], xp=40,
      **OPT, mirror="5E4FE420B6D2C97F", subtitle="Optional: more slots, uncrafting too", desc=[
        "&eWhat:&r the advanced version compacts more item types at once and can uncraft blocks back into pieces.",
        "&eHow:&r the compacting upgrade with gold, diamonds and redstone (check JEI)."]),
    Q("sto_bp_restock", 0, 0, [item("sophisticatedbackpacks:restock_upgrade")], "Restock Upgrade", section=S_BP, deps=["sto_bp_base"], xp=30,
      **OPT, mirror="4B62AF0405F68041", subtitle="Optional: refill from a chest in one click", desc=[
        "&eWhat:&r a Restock Upgrade tops the backpack up from a container you sneak-right-click: torches, food, whatever it already holds.",
        "&eHow:&r an upgrade base, a chest, iron, redstone and a sticky piston (check JEI).",
        "&eTip:&r restock torches and food from your supply chest on the way out, every time."]),
    Q("sto_bp_adv_restock", 0, 0, [item("sophisticatedbackpacks:advanced_restock_upgrade")], "Advanced Restock", section=S_BP, deps=["sto_bp_restock"], xp=40,
      **OPT, mirror="019CA0E35F888222", subtitle="Optional: more filter slots", desc=[
        "&eWhat:&r the advanced version with more filter slots and tag filters.",
        "&eHow:&r the restock upgrade with gold, diamonds and redstone (check JEI)."]),
    Q("sto_bp_everlasting", 0, 0, [item("sophisticatedbackpacks:everlasting_upgrade")], "Everlasting", section=S_BP, deps=["sto_bp_base", "hn_wither", "w_end"], xp=150,
      optional=True, tokens=2, mirror="037415D5B965E214", subtitle="Optional: a backpack that can't be lost", desc=[
        "&eWhat:&r with the Everlasting Upgrade, a dropped backpack can't burn, explode or despawn.",
        "&eHow:&r an upgrade base, nether stars and end crystals (check JEI). That means beating the Wither and visiting the End.",
        "&eTip:&r worth it before reactor work or deep Nether trips, where a lost pack hurts most."]),
    # refill: ql_bp_refill (qol.py, mirror 33882172DA8021F6)
    Q("sto_bp_adv_refill", 0, 0, [item("sophisticatedbackpacks:advanced_refill_upgrade")], "Advanced Refill", section=S_BP, deps=["ql_bp_refill"], xp=40,
      **OPT, mirror="7C0F7A1B3AB9A1A1", subtitle="Optional: keep more hotbar slots topped up", desc=[
        "&eWhat:&r the advanced refill upgrade keeps more hotbar items topped up from the backpack, with a target slot for each.",
        "&eHow:&r the refill upgrade with gold, diamonds and redstone (check JEI)."]),
    # --- our own backpack extras (not in ATM10): optional, off the nearest quest
    Q("sto_bp_advanced_more", 0, 0, [anyof(["sophisticatedbackpacks:advanced_feeding_upgrade", "sophisticatedbackpacks:advanced_refill_upgrade",
                                             "sophisticatedbackpacks:advanced_restock_upgrade", "sophisticatedbackpacks:advanced_deposit_upgrade",
                                             "sophisticatedbackpacks:advanced_void_upgrade", "sophisticatedbackpacks:advanced_tool_swapper_upgrade",
                                             "sophisticatedbackpacks:advanced_compacting_upgrade", "sophisticatedbackpacks:advanced_pump_upgrade"], 4)],
      "Fully Advanced", section=S_BP, deps=["sto_bp_advanced"], xp=60, **OPT, subtitle="Optional: four advanced upgrades in one pack", desc=[
        "&eWhat:&r a collection: any four advanced upgrades (feeding, refill, restock, deposit, void, tool swapper, compacting, pump).",
        "&eHow:&r each is its basic upgrade plus gold, diamonds and redstone (check JEI).",
        "&eTip:&r a diamond backpack has the slots for all of them at once."]),

    # ===== Our own sections (not in ATM10's chapter): optional side quests ======================
    # --- Tom's Simple Storage
    Q("s_toms", 0, 0, [item("toms_storage:storage_terminal"), item("toms_storage:inventory_connector")], "An Early Network", section=S_TOMS, deps=["s_fs_controller"], xp=75,
      **OPT, subtitle="Optional: Tom's Simple Storage, one searchable terminal", desc=[
        "&eWhat:&r Tom's Simple Storage connects your chests into one searchable terminal. It's your network until AE2.",
        "&eHow:&r place an Inventory Connector touching your chests (or link them with Inventory Cables), and a Storage Terminal on it.",
        "&eTip:&r point it at a drawer controller and every drawer shows up in the terminal."]),
    Q("s_toms_craft", 0, 0, [item("toms_storage:crafting_terminal")], "Crafting Terminal", section=S_TOMS, deps=["s_toms"], xp=40,
      **OPT, subtitle="Optional: craft straight from storage", desc=[
        "&eWhat:&r a terminal with a crafting grid that pulls ingredients from the network. JEI's + button fills it for you.",
        "&eHow:&r upgrade a Storage Terminal (check JEI).",
        "&eTip:&r a Wireless Terminal (also in JEI) lets you use it from across the base."]),
    Q("s_toms_cable", 0, 0, [item("toms_storage:inventory_cable", 16), item("toms_storage:inventory_cable_connector")], "Inventory Cables", section=S_TOMS, deps=["s_toms"], xp=30,
      **OPT, subtitle="Optional: reach chests across the room", desc=[
        "&eWhat:&r inventory cables carry the Inventory Connector's reach to chests that aren't touching it.",
        "&eHow:&r run cables from the connector and put a Cable Connector on each chest or drawer (check JEI).",
        "&eTip:&r framed cables can wear any block's texture, so they hide in walls."]),
    Q("s_toms_wireless", 0, 0, [item("toms_storage:adv_wireless_terminal")], "Wireless Terminal", section=S_TOMS, deps=["s_toms_craft"], xp=40,
      **OPT, subtitle="Optional: your early network, anywhere", desc=[
        "&eWhat:&r the Advanced Wireless Terminal opens your Tom's network from a long way off.",
        "&eHow:&r check JEI, then right-click it on a Storage Terminal to bind it.",
        "&eTip:&r it's the cheapest remote storage access until AE2."]),
    # --- Moving things
    Q("s_pipes", 0, 0, [tick()], "Pipez", section=S_MOVE, deps=['sto_hopper'], optional=True, tokens=0, xp=0, icon="pipez:item_pipe", subtitle="Moved: see Item Pipes", desc=["&eMoved:&r this step is now \"Item Pipes\" on the Automation and Logic page. Click to dismiss."]),
    Q("s_laser", 0, 0, [tick()], "LaserIO", section=S_MOVE, deps=['s_pipes', 't3_hull'], optional=True, tokens=0, xp=0, icon="laserio:laser_node", subtitle="Moved: see Laser Nodes", desc=["&eMoved:&r this step is now \"Laser Nodes\" on the Automation and Logic page. Click to dismiss."]),
    Q("s_entangled", 0, 0, [tick()], "Entangled", section=S_MOVE, deps=["sto_ender_chest"], xp=40, icon="minecraft:ender_pearl",
      **OPT, subtitle="Optional: one inventory, two places", desc=[
        "&eWhat:&r an Entangled Block is a window into another inventory: bind it to a chest or machine, and anything put in the Entangled Block goes into the bound block, even across dimensions.",
        "&eHow:&r ender pearls, obsidian and a wooden chest (check JEI). Right-click the target with the Entangled Binder (pearls, obsidian and a diamond), then right-click the Entangled Block. Click the checkmark when one is working.",
        "&eTip:&r put one next to a remote ore processor and pipe the output straight home. Both chunks must be loaded."]),
    # --- Iron Furnaces
    Q("s_furnace", 0, 0, [tick()], "Faster Furnaces", section=S_IF, deps=['sto_hub', 'gs_iron'], optional=True, tokens=0, xp=0, icon="ironfurnaces:iron_furnace", subtitle="Moved: see Iron Furnace", desc=["&eMoved:&r this step is now \"Iron Furnace\" on the Generators page. Click to dismiss."]),
    Q("sto_if_copper", 0, 0, [tick()], "Copper Furnace", section=S_IF, deps=['s_furnace'], optional=True, tokens=0, xp=0, icon="ironfurnaces:copper_furnace", subtitle="Moved: see Copper Furnace", desc=["&eMoved:&r this step is now \"Copper Furnace\" on the Generators page. Click to dismiss."]),
    Q("sto_if_augment", 0, 0, [tick()], "Speed and Fuel Augments", section=S_IF, deps=['s_furnace'], optional=True, tokens=0, xp=0, icon="ironfurnaces:augment_speed", subtitle="Moved: see Speed Augment", desc=["&eMoved:&r this step is now \"Speed Augment\" on the Generators page. Click to dismiss."]),
    Q("sto_if_generator", 0, 0, [tick()], "Furnace Generator", section=S_IF, deps=['sto_if_augment'], optional=True, tokens=0, xp=0, icon="ironfurnaces:augment_generator", subtitle="Moved: see Generator Augment", desc=["&eMoved:&r this step is now \"Generator Augment\" on the Generators page. Click to dismiss."]),
    Q("sto_if_factory", 0, 0, [tick()], "Factory and Blasting", section=S_IF, deps=['sto_if_generator'], optional=True, tokens=0, xp=0, icon="ironfurnaces:augment_factory", subtitle="Moved: see Factory Augment", desc=["&eMoved:&r this step is now \"Factory Augment\" on the Generators page. Click to dismiss."]),
    Q("sto_if_smoking", 0, 0, [tick()], "Smoking Augment", section=S_IF, deps=['sto_if_factory'], optional=True, tokens=0, xp=0, icon="ironfurnaces:augment_smoking", subtitle="Moved: see Smoking Augment", desc=["&eMoved:&r this step is now \"Smoking Augment\" on the Generators page. Click to dismiss."]),
    Q("sto_if_wireless", 0, 0, [tick()], "Wireless Heat", section=S_IF, deps=['sto_if_factory'], optional=True, tokens=0, xp=0, icon="ironfurnaces:heater", subtitle="Moved: see Wireless Heating", desc=["&eMoved:&r this step is now \"Wireless Heating\" on the Generators page. Click to dismiss."]),
    Q("sto_if_copy", 0, 0, [tick()], "Settings Linker", section=S_IF, deps=['s_furnace'], optional=True, tokens=0, xp=0, icon="ironfurnaces:item_copy", subtitle="Moved: see Configuration Copier", desc=["&eMoved:&r this step is now \"Configuration Copier\" on the Generators page. Click to dismiss."]),
    Q("sto_if_gold", 0, 0, [tick()], "Gold Furnace", section=S_IF, deps=['s_furnace'], optional=True, tokens=0, xp=0, icon="ironfurnaces:gold_furnace", subtitle="Moved: see Gold Furnace", desc=["&eMoved:&r this step is now \"Gold Furnace\" on the Generators page. Click to dismiss."]),
    Q("sto_if_silver", 0, 0, [tick()], "Silver Furnace", section=S_IF, deps=['s_furnace', 't4_byproduct'], optional=True, tokens=0, xp=0, icon="ironfurnaces:silver_furnace", subtitle="Moved: see Silver Furnace", desc=["&eMoved:&r this step is now \"Silver Furnace\" on the Generators page. Click to dismiss."]),
    Q("sto_if_diamond", 0, 0, [tick()], "Diamond Furnace", section=S_IF, deps=['sto_if_gold'], optional=True, tokens=0, xp=0, icon="ironfurnaces:diamond_furnace", subtitle="Moved: see Diamond Furnace", desc=["&eMoved:&r this step is now \"Diamond Furnace\" on the Generators page. Click to dismiss."]),
    Q("sto_if_crystal", 0, 0, [tick()], "Crystal Furnace", section=S_IF, deps=['sto_if_diamond'], optional=True, tokens=0, xp=0, icon="ironfurnaces:crystal_furnace", subtitle="Moved: see Crystal Furnace", desc=["&eMoved:&r this step is now \"Crystal Furnace\" on the Generators page. Click to dismiss."]),
    Q("sto_if_emerald", 0, 0, [tick()], "Emerald Furnace", section=S_IF, deps=['sto_if_diamond'], optional=True, tokens=0, xp=0, icon="ironfurnaces:emerald_furnace", subtitle="Moved: see Emerald Furnace", desc=["&eMoved:&r this step is now \"Emerald Furnace\" on the Generators page. Click to dismiss."]),
    Q("sto_if_obsidian", 0, 0, [tick()], "Obsidian Furnace", section=S_IF, deps=['sto_if_emerald', 't2_blaze'], optional=True, tokens=0, xp=0, icon="ironfurnaces:obsidian_furnace", subtitle="Moved: see Obsidian Furnace", desc=["&eMoved:&r this step is now \"Obsidian Furnace\" on the Generators page. Click to dismiss."]),
    Q("sto_if_netherite", 0, 0, [tick()], "Netherite Furnace", section=S_IF, deps=['sto_if_obsidian', 't2_debris'], optional=True, tokens=0, xp=0, icon="ironfurnaces:netherite_furnace", subtitle="Moved: see Netherite Furnace", desc=["&eMoved:&r this step is now \"Netherite Furnace\" on the Generators page. Click to dismiss."]),
    Q("sto_if_rainbow", 0, 0, [tick()], "The Rainbow Furnace", section=S_IF, deps=['sto_if_netherite', 'sto_if_crystal', 'sto_if_silver', 'sto_if_copper'], optional=True, tokens=0, xp=0, icon="ironfurnaces:rainbow_plating", subtitle="Moved: see The Rainbow Generator", desc=["&eMoved:&r this step is now \"The Rainbow Generator\" on the Generators page. Click to dismiss."]),
], links=[("gs_chest", -2, 0), ("q_bp_iron", -2, 9), ("q_bp_up", -2, 10.5), ("t3_hull", -2, 7), ("gs_iron", -2, 14)],
   mirror="storage")
