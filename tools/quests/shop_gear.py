"""Quest chapter: shop_gear (shop group). See tools/quests/STYLE.md and docs/research/shop_brief.md.

The Gear stall of the Demigod's Market: repeatable buy-quests for tools, armour, weapons, backpacks and their
upgrades, storage blocks, QoL items and magic gear. Rule: you can only buy what you've already made yourself.
Every entry depends on the quest where the player first makes that item and stays invisible (locked_hidden)
until then. Pay by handing in tokens (consume=True); the quest resets after claiming (repeat=True).

Layout is manual (same pattern as shop_materials.py): one block per stall, each starting with a counter quest,
entries 10 per line. Blocks start on a 6-cell grid (y = 0, 6, 12, ...); a block with more than four lines
pushes the next block down to the next free multiple of 6.
Prices follow the brief's gear column: Steam 2-6 tokens per piece or set (more for diamond, Greater for
netherite), LV 6-12 tokens, MV 1-2 Greater, HV 3-4 Greater, EV 5+ Greater. Storage and QoL items use the
cheaper materials/world bands.
Never sold here: anything flight-related (jetpacks, Angel Ring, pylons, elytra and Soul Elytra, JDT flight and
elytra chestplates, Ars flight), random relic/artifact loot, boss drops and things the market chapter already sells.
"""
import math

from questlib import Q, Chapter, item, tick, SIDE  # noqa: F401

T = "kubejs:demigod_token"
G = "kubejs:greater_demigod_token"

PER_LINE = 10     # entries per line before wrapping
STEP_X = 1.5
STEP_Y = 1.5
BLOCK = 6         # stall blocks start on multiples of this
_rows = []        # [start y, entry count] per stall block


def _price(n, greater):
    if greater:
        return f"{n} Greater"
    return f"{n} tokens" if n > 1 else "1 token"


def counter(key, title, dep, sub, desc):
    """Stall header: a short optional checkmark that opens this block. Placed below the previous block."""
    if _rows:
        y0, n = _rows[-1]
        end = y0 + STEP_Y * max(0, (n - 1) // PER_LINE)
        y = BLOCK * math.ceil((end + 3) / BLOCK)
    else:
        y = 0
    _rows.append([y, 0])
    return Q(key, 0, y, [tick()], title, deps=[dep], tokens=0, xp=0, optional=True, size=1.5,
             subtitle=sub, desc=desc)


def buy(name, title, items, price, dep, dep_title, what, greater=False):
    """One shop entry: pay `price` (Greater) tokens, get `items` [(id, count), ...]. Placed on the current block."""
    row = _rows[-1]
    i = row[1]
    row[1] += 1
    x = STEP_X * (1 + i % PER_LINE)
    y = row[0] + STEP_Y * (i // PER_LINE)
    if isinstance(items, str):
        items = [(items, 1)]
    cost = item(G if greater else T, price)
    return Q(f"sg_buy_{name}", x, y, [cost], title, deps=[dep], items=items,
             tokens=0, xp=0, optional=True, repeat=True, consume=True, locked_hidden=True,
             subtitle=f"{_price(price, greater)} · unlocked by {dep_title}",
             desc=[f"&eWhat:&r {what}"])


def g(*a, **k):
    """Shorthand for an entry paid in Greater Demigod Tokens."""
    return buy(*a, greater=True, **k)


def kit(prefix, parts):
    """[(prefix + part, 1), ...] for tool and armour sets."""
    return [(prefix + p, 1) for p in parts]


ARMOR = ["helmet", "chestplate", "leggings", "boots"]
MC = "minecraft:"
MT = "mekanismtools:"
SB = "sophisticatedbackpacks:"
SS = "sophisticatedstorage:"
J = "justdirethings:"
UG = "undergarden:"

QUESTS = [
    Q("sg_intro", 0, -3, [tick()], "The Gear Stall", deps=["wel_tokens"], tokens=0, xp=10, optional=True,
      size=1.5, subtitle="Replace what you've already earned", desc=[
          "&6You remember an armoury that never ran empty. This one fills as you prove yourself.&r",
          "&eWhat:&r this stall sells tools, armour, weapons, backpacks, storage, comforts and magic gear.",
          "&eHow:&r an item appears here only after the quest where you first made it. Hand in the tokens and claim it; the entry resets so you can buy again.",
          "&eTip:&r tokens replace a lost pickaxe, never a tier. Flight gear is never sold: that is earned through chemistry.",
          "&eTip:&r big-ticket gear costs Greater Demigod Tokens (1 Greater = 9 tokens; craft them in a grid)."]),

    # --- Steam (T0-T2): tools, armour and weapons -------------------------------------------------------
    counter("sg_row_steam_tools", "Steam Stall: Tools and Armour", "gs_iron", "Iron, bronze, steel and diamond", [
        "&eWhat:&r the early armoury: vanilla and Mekanism tools and armour, the first MI and Create tools, and Just Dire Things gear.",
        "&eHow:&r entries show up one by one as you finish the quests that make them."]),
    buy("iron_tools", "Iron Tool Kit", kit(MC + "iron_", ["pickaxe", "axe", "shovel", "sword"]), 4,
        "gs_irontools", "Iron Tools", "an iron pickaxe, axe, shovel and sword."),
    buy("iron_armor", "Iron Armour Set", kit(MC + "iron_", ARMOR), 6, "gs_armor", "Iron Armour",
        "a full set of iron armour."),
    buy("shield", "Shield", MC + "shield", 2, "gs_shield", "Shield", "a fresh shield."),
    buy("bow", "Bow and Arrows", [(MC + "bow", 1), (MC + "arrow", 32)], 2, "gs_opt_bow", "Bow and Arrow",
        "a bow and 32 arrows."),
    buy("shears", "Shears", MC + "shears", 1, "gs_opt_shears", "Shearing Season", "a pair of shears."),
    buy("iron_paxel", "Iron Paxel", MT + "iron_paxel", 3, "gs_paxel", "The Paxel",
        "an iron paxel: pickaxe, axe and shovel in one."),
    buy("bronze_paxel", "Bronze Paxel", MT + "bronze_paxel", 3, "t0_opt_paxel", "Bronze Paxel", "a bronze paxel."),
    buy("bronze_armor", "Bronze Armour Set", kit(MT + "bronze_", ARMOR), 5, "hv_bronze_armor", "Bronze Armour",
        "a full set of bronze armour."),
    buy("lapis_armor", "Lapis Armour Set", kit(MT + "lapis_lazuli_", ARMOR), 4, "hv_lapis_armor", "Lapis Armour",
        "a full set of lapis armour."),
    buy("steel_paxel", "Steel Paxel", MT + "steel_paxel", 4, "t1_steel_paxel", "Steel Paxel", "a steel paxel."),
    buy("steel_armor", "Steel Armour Set", kit(MT + "steel_", ARMOR), 6, "hv_steel_armor", "Steel Armour",
        "a full set of steel armour."),
    buy("mi_wrench", "MI Wrench", "modern_industrialization:wrench", 2, "t0_opt_wrench", "The Wrench",
        "a Modern Industrialization wrench."),
    buy("steam_drill", "Steam Mining Drill", "modern_industrialization:steam_mining_drill", 6, "t0_opt_drill",
        "Steam Mining Drill", "a steam mining drill (bring your own water and fuel)."),
    buy("create_goggles", "Goggles and Wrench", [("create:goggles", 1), ("create:wrench", 1)], 3, "cr_goggles",
        "Goggles and Wrench", "Engineer's Goggles and a Create wrench."),
    buy("diamond_pick", "Diamond Pickaxe", MC + "diamond_pickaxe", 6, "hv_diamond_pick", "Diamond Pickaxe",
        "a diamond pickaxe."),
    buy("diamond_kit", "Diamond Sword and Shovel", [(MC + "diamond_sword", 1), (MC + "diamond_shovel", 1)], 6,
        "hv_diamond_kit", "Diamond Sword and Shovel", "a diamond sword and a diamond shovel."),
    buy("diamond_armor", "Diamond Armour Set", kit(MC + "diamond_", ARMOR), 18, "hv_diamond_armor",
        "Diamond Armour", "a full set of diamond armour (24 diamonds' worth)."),
    g("netherite_pick", "Netherite Pickaxe", MC + "netherite_pickaxe", 3, "hv_netherite_pick", "Netherite Pickaxe",
      "a netherite pickaxe."),
    g("netherite_sword", "Netherite Sword", MC + "netherite_sword", 3, "hv_netherite_sword", "Netherite Sword",
      "a netherite sword."),
    g("netherite_armor", "Netherite Armour Set", kit(MC + "netherite_", ARMOR), 10, "hv_netherite_armor",
      "Netherite Armour", "a full set of netherite armour (four ingots' worth of scrap)."),
    buy("trident", "Trident", MC + "trident", 9, "hn_trident", "The Trident", "a trident, no Drowned required."),
    buy("ferricore_tools", "Ferricore Tool Kit", kit(J + "ferricore_", ["pickaxe", "axe", "shovel"]), 6,
        "jdt_tools_t1", "Ferricore Tools", "a ferricore pickaxe, axe and shovel."),
    buy("ferricore_armor", "Ferricore Armour Set", kit(J + "ferricore_", ARMOR), 8, "jdt_armor", "Ferricore Armour",
        "a full set of ferricore armour."),
    buy("blazegold_tools", "Blazegold Tool Kit", kit(J + "blazegold_", ["pickaxe", "axe", "shovel", "sword"]), 12,
        "jdt_blazegold_kit", "The Blazegold Set", "a blazegold pickaxe, axe, shovel and sword."),
    buy("blazegold_armor", "Blazegold Armour Set", kit(J + "blazegold_", ARMOR), 12, "jdt_blazegold_armor",
        "Blazegold Armour", "a full set of blazegold armour."),
    buy("celestigem_tools", "Celestigem Pickaxe and Paxel", kit(J + "celestigem_", ["pickaxe", "paxel"]), 18,
        "jdt_tools_t3", "Celestigem and the Paxel", "a celestigem pickaxe and paxel."),
    buy("celestigem_armor", "Celestigem Helmet, Leggings and Boots",
        kit(J + "celestigem_", ["helmet", "leggings", "boots"]), 18, "jdt_celestigem_armor", "Celestigem Armour",
        "celestigem helmet, leggings and boots (the chestplate is never sold: it carries the elytra upgrade)."),

    # --- Steam (T0-T2): backpacks and storage -------------------------------------------------------------
    counter("sg_row_steam_storage", "Steam Stall: Backpacks and Storage", "gs_chest", "Bags, upgrades, chests and drawers", [
        "&eWhat:&r backpacks and their upgrades, chests, barrels and drawers.",
        "&eHow:&r entries show up one by one as you finish the quests that make them. Upgrade bases are in The Market."]),
    buy("backpack", "Backpack", SB + "backpack", 2, "gs_backpack", "A Backpack", "a leather backpack."),
    buy("copper_backpack", "Copper Backpack", SB + "copper_backpack", 3, "sto_bp_copper", "Copper Backpack",
        "a copper backpack."),
    buy("iron_backpack", "Iron Backpack", SB + "iron_backpack", 4, "q_bp_iron", "Iron Backpack", "an iron backpack."),
    buy("gold_backpack", "Gold Backpack", SB + "gold_backpack", 6, "sto_bp_gold", "Gold Backpack", "a gold backpack."),
    buy("diamond_backpack", "Diamond Backpack", SB + "diamond_backpack", 12, "sto_bp_diamond", "Diamond Backpack",
        "a diamond backpack."),
    g("netherite_backpack", "Netherite Backpack", SB + "netherite_backpack", 3, "q_bp_netherite", "Netherite Backpack",
      "a netherite backpack."),
    buy("bp_pickup", "Pickup and Magnet Upgrades", [(SB + "pickup_upgrade", 1), (SB + "magnet_upgrade", 1)], 5,
        "q_bp_up", "Backpack Upgrades", "a pickup upgrade and a magnet upgrade."),
    buy("bp_crafting", "Crafting Upgrade", SB + "crafting_upgrade", 3, "sto_bp_crafting", "Crafting Upgrade",
        "a backpack crafting upgrade."),
    buy("bp_feeding", "Feeding Upgrade", SB + "feeding_upgrade", 3, "q_bp_feeding", "Feeding Upgrade",
        "a backpack feeding upgrade."),
    buy("bp_stack1", "Stack Upgrade I", SB + "stack_upgrade_tier_1", 3, "ql_bp_stack", "Stack Upgrade",
        "a tier 1 backpack stack upgrade."),
    buy("bp_stack2", "Stack Upgrade II", SB + "stack_upgrade_tier_2", 6, "sto_bp_stack", "Bigger Stacks",
        "a tier 2 backpack stack upgrade."),
    buy("bp_tool_swapper", "Tool Swapper Upgrade", SB + "tool_swapper_upgrade", 3, "ql_bp_tools", "Tool Swapper",
        "a backpack tool swapper upgrade."),
    buy("bp_refill", "Refill Upgrade", SB + "refill_upgrade", 3, "ql_bp_refill", "Refill Upgrade",
        "a backpack refill upgrade."),
    buy("bp_smelting", "Smelting Upgrades", [(SB + "smelting_upgrade", 1), (SB + "auto_smelting_upgrade", 1)], 5,
        "sto_bp_smelting", "Smelting on the Go", "a smelting upgrade and an auto-smelting upgrade."),
    buy("bp_void", "Void Upgrade", SB + "void_upgrade", 2, "sto_bp_void", "Void Upgrade", "a backpack void upgrade."),
    buy("bp_deposit", "Deposit and Restock Upgrades", [(SB + "deposit_upgrade", 1), (SB + "restock_upgrade", 1)], 4,
        "sto_bp_deposit", "Deposit and Restock", "a deposit upgrade and a restock upgrade."),
    buy("bp_tank", "Tank Upgrade", SB + "tank_upgrade", 4, "sto_bp_tank", "Tank Upgrade", "a backpack tank upgrade."),
    buy("bp_pump", "Pump Upgrades", [(SB + "pump_upgrade", 1), (SB + "xp_pump_upgrade", 1)], 4, "sto_bp_pump", "Pumps",
        "a pump upgrade and an XP pump upgrade."),
    buy("bp_compacting", "Compacting and Filter Upgrades",
        [(SB + "compacting_upgrade", 1), (SB + "filter_upgrade", 1)], 4, "sto_bp_compacting", "Compacting and Filters",
        "a compacting upgrade and a filter upgrade."),
    buy("bp_advanced", "Advanced Pickup Set",
        [(SB + "advanced_pickup_upgrade", 1), (SB + "advanced_magnet_upgrade", 1), (SB + "advanced_filter_upgrade", 1)],
        10, "sto_bp_advanced", "Advanced Pickup", "advanced pickup, magnet and filter upgrades."),
    buy("bp_battery", "Battery Upgrade", SB + "battery_upgrade", 4, "sto_bp_battery", "Battery Upgrade",
        "a backpack battery upgrade."),
    buy("chests", "Chests", [(MC + "chest", 8)], 1, "gs_chest", "Somewhere to Put Things",
        "8 wooden chests."),
    buy("barrels", "Barrels", [(MC + "barrel", 8)], 1, "sto_vanilla", "Barrels and Trapped Chests", "8 barrels."),
    buy("ender_chest", "Ender Chest", MC + "ender_chest", 4, "sto_ender_chest", "Ender Chest", "an ender chest."),
    buy("soph_barrel", "Sophisticated Barrels", [(SS + "barrel", 2)], 2, "s_barrel", "Sophisticated Barrel",
        "2 sophisticated barrels."),
    buy("soph_chest", "Sophisticated Chests", [(SS + "chest", 2)], 2, "sto_ss_chest", "Sophisticated Chests",
        "2 sophisticated chests."),
    buy("ss_iron_tier", "Iron Tier Upgrades", [(SS + "basic_to_iron_tier_upgrade", 2)], 2, "s_ss_tier",
        "Tier Upgrades", "2 basic-to-iron tier upgrades for barrels and chests."),
    buy("ss_ladder", "Gold and Diamond Tier Upgrades",
        [(SS + "iron_to_gold_tier_upgrade", 1), (SS + "gold_to_diamond_tier_upgrade", 1)], 8, "sto_ss_ladder",
        "Gold and Diamond Tiers", "an iron-to-gold and a gold-to-diamond tier upgrade."),
    buy("ss_stack", "Storage Stack Upgrade", SS + "stack_upgrade_tier_1", 3, "s_ss_stack", "Stack Upgrades",
        "a tier 1 stack upgrade for barrels and chests."),
    buy("ss_compacting", "Storage Compacting Upgrade", SS + "compacting_upgrade", 3, "s_ss_compacting", "Compacting",
        "a compacting upgrade for barrels and chests."),
    buy("ss_shulker", "Sophisticated Shulker Box", SS + "shulker_box", 12, "sto_ss_shulker",
        "Sophisticated Shulker Box", "a sophisticated shulker box (shulker shells included)."),
    buy("drawers", "Oak Drawers", [("functionalstorage:oak_1", 4)], 2, "s_drawers", "Drawers", "4 oak drawers."),
    buy("compacting_drawer", "Compacting Drawer", "functionalstorage:compacting_drawer", 4, "s_fs_compacting",
        "Compacting Drawer", "a compacting drawer."),
    buy("drawer_tiers", "Copper and Gold Drawer Upgrades",
        [("functionalstorage:copper_upgrade", 1), ("functionalstorage:gold_upgrade", 1)], 4, "sto_fs_tiers",
        "Copper and Gold Upgrades", "a copper and a gold drawer upgrade."),
    buy("drawer_diamond", "Diamond Drawer Upgrade", "functionalstorage:diamond_upgrade", 6, "s_fs_upgrade",
        "Drawer Upgrades", "a diamond drawer upgrade."),

    # --- Steam (T0-T2): comforts and magic --------------------------------------------------------------
    counter("sg_row_steam_comfort", "Steam Stall: Comforts and Magic", "gs_iron", "Pocket tools, torches and trinkets", [
        "&eWhat:&r quality-of-life items, early spell books, charms and trinkets.",
        "&eHow:&r entries show up one by one as you finish the quests that make them."]),
    buy("tome", "Akashic Tome", "akashictome:tome", 1, "q_tome", "One Book to Rule Them All",
        "an Akashic Tome (add your guidebooks again)."),
    buy("compasses", "Nature's and Explorer's Compass",
        [("naturescompass:naturescompass", 1), ("explorerscompass:explorerscompass", 1)], 5, "q_compass",
        "Find Anything", "one of each compass."),
    buy("mega_torch", "Mega Torch", "torchmaster:megatorch", 4, "q_torch", "No More Mob Spawns", "a Mega Torch."),
    buy("dread_lamp", "Dread Lamp", "torchmaster:dreadlamp", 5, "q_dreadlamp", "Dread Lamp", "a Dread Lamp."),
    buy("feral_flare", "Feral Flare Lantern", "torchmaster:feral_flare_lantern", 3, "ql_feral", "Feral Flare Lantern",
        "a Feral Flare Lantern."),
    buy("pocket_table", "Pocket Crafting Table", "crafting_on_a_stick:crafting_table", 1, "q_stick",
        "Crafting on a Stick", "a crafting table on a stick."),
    buy("pocket_workshop", "Pocket Stonecutter and Smithing Table",
        [("crafting_on_a_stick:stonecutter", 1), ("crafting_on_a_stick:smithing_table", 1)], 2, "q_stick_more",
        "A Whole Workshop", "a pocket stonecutter and smithing table."),
    buy("pocket_anvil", "Pocket Anvil and Grindstone",
        [("crafting_on_a_stick:anvil", 1), ("crafting_on_a_stick:grindstone", 1)], 5, "ql_stick_anvil",
        "Pocket Anvil", "a pocket anvil and grindstone."),
    buy("tool_belt", "Tool Belt", "toolbelt:belt", 3, "ql_belt", "Tool Belt", "a tool belt."),
    buy("belt_pouch", "Belt Pouch", "toolbelt:pouch", 2, "ql_pouch", "Belt Pouches", "a pouch to widen your tool belt."),
    buy("waystone", "Waystone", "waystones:waystone", 6, "q_waystone", "Waystones", "a waystone."),
    buy("warp_scrolls", "Warp Scrolls", [("waystones:warp_scroll", 4)], 3, "q_warp_scroll", "Warp Scrolls",
        "4 warp scrolls."),
    buy("trowel", "Trowel", "utilitarian:trowel", 2, "ut_trowel", "The Trowel", "a trowel."),
    buy("angel_blocks", "Angel Blocks", [("utilitarian:angel_block", 4)], 2, "ut_angel", "Angel Block",
        "4 angel blocks."),
    buy("block_magnet", "Block Magnet", "utilitarian:magnet", 3, "ut_magnet", "Block Magnet", "a block magnet."),
    buy("hammock", "Hammock", "comforts:hammock_white", 2, "tc_hammock", "Hammock", "a white hammock."),
    buy("watering_can", "Watering Can", "mysticalagriculture:watering_can", 2, "ma_can", "Watering Can",
        "a watering can."),
    buy("novice_book", "Novice Spell Book", "ars_nouveau:novice_spell_book", 3, "m_book", "Novice Spell Book",
        "a novice spell book (spells are rewritten, glyphs stay learned)."),
    buy("apprentice_book", "Apprentice Spell Book", "ars_nouveau:apprentice_spell_book", 12, "m_apprentice",
        "Apprentice Spell Book", "an apprentice spell book."),
    buy("lesser_discount", "Ring of Lesser Discount", "ars_nouveau:ring_of_lesser_discount", 6, "ars_discount",
        "Ring of Discount", "a ring that lowers spell mana costs."),
    buy("greater_discount", "Ring of Greater Discount", "ars_nouveau:ring_of_greater_discount", 12,
        "ars_greater_discount", "Greater Discount", "a stronger mana discount ring."),
    buy("caster_bag", "Caster's Bag", "ars_elemental:caster_bag", 6, "ars_caster_bag", "Caster's Bag",
        "a bag for spell items."),
    buy("dominion_wand", "Dominion Wand", "ars_nouveau:dominion_wand", 2, "ars_dominion", "Dominion Wand",
        "a dominion wand for linking blocks and creatures."),
    buy("starbuncle", "Starbuncle Charm", "ars_nouveau:starbuncle_charm", 4, "m_starbuncle", "Starbuncle",
        "a Starbuncle charm: another little item courier."),
    buy("satchel", "Surprisingly Large Bag", "occultism:satchel", 6, "oc_satchel", "Surprisingly Large Bag",
        "an Occultism satchel."),
    buy("otherworld_goggles", "Otherworld Goggles", "occultism:otherworld_goggles", 6, "oc_goggles",
        "Otherworld Goggles", "a pair of Otherworld Goggles."),
    buy("infused_pick", "Infused Pickaxe", "occultism:infused_pickaxe", 8, "oc_infused_pick", "Infused Pickaxe",
        "an infused pickaxe for otherworld ores."),
    buy("iesnium_pick", "Iesnium Pickaxe", "occultism:iesnium_pickaxe", 12, "oc_iesnium_pick", "Iesnium Tools",
        "an iesnium pickaxe."),
    buy("fortune_coin", "Fortune Coin", "reliquary:fortune_coin", 6, "m_fortune", "Fortune Coin",
        "a Fortune Coin that pulls items to you."),
    buy("paranoia_lantern", "Lantern of Paranoia", "reliquary:lantern_of_paranoia", 6, "rl_lantern",
        "Lantern of Paranoia", "a lantern that places torches as you walk."),

    # --- LV (T3) ----------------------------------------------------------------------------------------------
    counter("sg_row_lv", "LV Stall", "t3_analog", "Mekanism gear and building gadgets", [
        "&eWhat:&r osmium and refined obsidian gear, Mekanism tools and the building gadgets.",
        "&eHow:&r entries show up one by one as you finish the quests that make them."]),
    buy("osmium_paxel", "Osmium Paxel", MT + "osmium_paxel", 6, "tc_osmium_paxel", "Osmium Paxel", "an osmium paxel."),
    buy("osmium_armor", "Osmium Armour Set", kit(MT + "osmium_", ARMOR), 10, "mk2_armor_osmium", "Osmium Armour",
        "a full set of osmium armour."),
    buy("obsidian_paxel", "Refined Obsidian Paxel", MT + "refined_obsidian_paxel", 10, "tc_obsidian_paxel",
        "The Ultimate Paxel", "a refined obsidian paxel."),
    buy("obsidian_armor", "Refined Obsidian Armour Set", kit(MT + "refined_obsidian_", ARMOR), 18,
        "mk2_armor_obsidian", "Refined Obsidian Armour", "a full set of refined obsidian armour."),
    buy("glowstone_armor", "Refined Glowstone Armour Set", kit(MT + "refined_glowstone_", ARMOR), 12,
        "mk2_armor_glowstone", "Refined Glowstone Armour", "a full set of refined glowstone armour."),
    buy("disassembler", "Atomic Disassembler", "mekanism:atomic_disassembler", 10, "tc_disassembler",
        "Atomic Disassembler", "an Atomic Disassembler (uncharged)."),
    buy("scuba", "Scuba Mask and Tank", [("mekanism:scuba_mask", 1), ("mekanism:scuba_tank", 1)], 8, "tc_scuba",
        "Bottled Oxygen", "a scuba mask and an empty scuba tank."),
    buy("free_runners", "Free Runners", "mekanism:free_runners", 8, "tc_free_runners", "Free Runners",
        "a pair of Free Runners (uncharged)."),
    buy("configurator", "Configurator", "mekanism:configurator", 6, "mk2_configurator", "Configurator",
        "a Mekanism Configurator."),
    buy("electric_bow", "Electric Bow", "mekanism:electric_bow", 8, "mk2_electric_bow", "Electric Bow",
        "an Electric Bow (uncharged)."),
    buy("energy_tablet", "Energy Tablet", "mekanism:energy_tablet", 6, "mk2_tablet", "Energy Tablet",
        "an energy tablet."),
    buy("portable_tp", "Portable Teleporter", "mekanism:portable_teleporter", 12, "mk2_portable_tp",
        "Portable Teleporter", "a Portable Teleporter (uncharged)."),
    buy("canteen", "Canteen", "mekanism:canteen", 3, "mk2_nutrition", "Nutritional Paste", "an empty canteen."),
    buy("personal_chest", "Personal Chest", "mekanism:personal_chest", 4, "mk2_security", "Mine, Not Yours",
        "a personal chest only you can open."),
    buy("cardboard", "Cardboard Boxes", [("mekanism:cardboard_box", 4)], 2, "mk2_cardboard", "Moving Day",
        "4 cardboard boxes for moving blocks."),
    buy("robit", "Robit", "mekanism:robit", 10, "mk2_robit", "Robit", "a Robit companion."),
    buy("mining_gadget", "Mining Gadget", "mininggadgets:mininggadget_simple", 10, "tc_mining_gadget",
        "Mining Gadget", "a simple Mining Gadget (uncharged)."),
    buy("building_gadget", "Building Gadget", "buildinggadgets2:gadget_building", 8, "q_gadget", "Building Gadgets",
        "a Building Gadget."),
    buy("exchanging_gadget", "Exchanging Gadget", "buildinggadgets2:gadget_exchanging", 8, "q_gadget_exchange",
        "Exchanging Gadget", "an Exchanging Gadget."),
    buy("destruction_gadget", "Destruction Gadget", "buildinggadgets2:gadget_destruction", 10, "bd_gadget_destroy",
        "Destruction Gadget", "a Destruction Gadget."),

    # --- MV (T4) ----------------------------------------------------------------------------------------------
    counter("sg_row_mv", "MV Stall", "t4_mv", "Undergarden metals and the flamethrower", [
        "&eWhat:&r Undergarden tools and armour and the Mekanism flamethrower.",
        "&eHow:&r prices are in Greater Demigod Tokens from here on."]),
    g("flamethrower", "Flamethrower", "mekanism:flamethrower", 2, "mk2_flamethrower", "Flamethrower",
      "an empty Mekanism flamethrower (fill it with hydrogen)."),
    g("cloggrum_tools", "Cloggrum Tool Kit", kit(UG + "cloggrum_", ["pickaxe", "axe", "shovel", "sword"]), 1,
      "ug_cloggrum_kit", "Cloggrum Kit", "a cloggrum pickaxe, axe, shovel and sword."),
    g("cloggrum_armor", "Cloggrum Armour Set", kit(UG + "cloggrum_", ARMOR), 1, "ug_cloggrum_armor",
      "Cloggrum Armour", "a full set of cloggrum armour."),
    g("froststeel_tools", "Froststeel Tool Kit", kit(UG + "froststeel_", ["pickaxe", "axe", "shovel", "sword"]), 2,
      "ug_froststeel_tools", "Froststeel Tools", "a froststeel pickaxe, axe, shovel and sword."),
    g("froststeel_armor", "Froststeel Armour Set", kit(UG + "froststeel_", ARMOR), 2, "ug_froststeel_armor",
      "Froststeel Armour", "a full set of froststeel armour."),
    g("utherium_tools", "Utherium Tool Kit", kit(UG + "utherium_", ["pickaxe", "axe", "shovel", "sword"]), 2,
      "ug_utherium_tools", "Utherium Tools", "a utherium pickaxe, axe, shovel and sword."),
    g("utherium_armor", "Utherium Armour Set", kit(UG + "utherium_", ARMOR), 2, "ug_utherium_armor",
      "Utherium Armour", "a full set of utherium armour."),
    g("forgotten_tools", "Forgotten Tool Kit", kit(UG + "forgotten_", ["pickaxe", "axe", "shovel", "sword"]), 2,
      "ug_forgotten_kit", "Forgotten Kit", "a forgotten pickaxe, axe, shovel and sword."),

    # --- HV (T5) ----------------------------------------------------------------------------------------------
    counter("sg_row_hv", "HV Stall", "t5_hv", "Diesel, fluix and late dire tools", [
        "&eWhat:&r the diesel drill, AE2 tools, Naga armour and eclipse alloy tools.",
        "&eHow:&r entries show up one by one as you finish the quests that make them."]),
    g("diesel_drill", "Diesel Mining Drill", "modern_industrialization:diesel_mining_drill", 4, "t5_opt_tools",
      "Diesel Toys", "an empty diesel mining drill."),
    g("fluix_sword", "Fluix Sword", "ae2:fluix_sword", 3, "ae_fluix_sword", "Fluix Sword", "a fluix sword."),
    g("ae_tools", "Memory Card and Network Tool", [("ae2:memory_card", 1), ("ae2:network_tool", 1)], 3, "ae_tools",
      "Memory Card and Network Tool", "an AE2 memory card and network tool."),
    g("naga_armor", "Naga Scale Armour", [("twilightforest:naga_chestplate", 1), ("twilightforest:naga_leggings", 1)],
      3, "tf_naga_armor", "Naga Scale Armour", "a Naga scale chestplate and leggings."),
    g("eclipse_tools", "Eclipse Alloy Tool Kit", kit(J + "eclipsealloy_", ["pickaxe", "axe", "shovel", "sword"]), 4,
      "jdt_eclipse_kit", "The Eclipse Alloy Set", "an eclipse alloy pickaxe, axe, shovel and sword."),

    # --- EV (T6-T7) -------------------------------------------------------------------------------------------
    counter("sg_row_ev", "EV Stall", "t6_pu", "The MekaSuit and space suits", [
        "&eWhat:&r the MekaSuit, the Meka-Tool and Ad Astra space suits. Modules are never sold.",
        "&eHow:&r entries show up one by one as you finish the quests that make them."]),
    g("mekasuit", "MekaSuit", [("mekanism:mekasuit_helmet", 1), ("mekanism:mekasuit_bodyarmor", 1),
                               ("mekanism:mekasuit_pants", 1), ("mekanism:mekasuit_boots", 1)], 20,
      "mk2_mekasuit_full", "The Full MekaSuit", "a full, empty MekaSuit: no modules, no charge."),
    g("meka_tool", "Meka-Tool", "mekanism:meka_tool", 8, "mk2_mekatool", "Meka-Tool",
      "an empty Meka-Tool: no modules, no charge."),
    g("space_suit", "Space Suit", kit("ad_astra:space_", ["helmet", "suit", "pants", "boots"]), 6, "t7_suit_full",
      "The Full Suit", "a full Ad Astra space suit (fill it with oxygen)."),
    g("netherite_space_suit", "Netherite Space Suit",
      kit("ad_astra:netherite_space_", ["helmet", "suit", "pants", "boots"]), 10, "t7_opt_hot_suit",
      "Heat-Proof Suit", "a full heat-proof netherite space suit."),
]

CHAPTER = Chapter("shop_gear", "Market: Tools, Armour and Gear", "minecraft:iron_pickaxe",
        ["Replace the tools, armour and comforts you've already earned."], SIDE, QUESTS,
        tokens=0, layout="manual")
