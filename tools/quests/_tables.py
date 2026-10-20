"""Reward tables for the quest book (FTB Quests reward_tables/*.snbt).

Use them from a quest with Q(..., loot="t2") (one random roll) or Q(..., choice="pick_t5")
(the player picks one). Entries are (item_id, count, weight); a higher weight is more likely.
Supplies and comforts, never machines, circuits or tier skips. No currency here: quests pay Wardaddy Market coins
(tools/build_quests.py), and the old Demigod Token entries were removed on 2026-10-20 ("Coins replace tokens").
Every id is checked against test/ids.tsv.
"""
from questlib import check

MI = "modern_industrialization"


def table(title, entries, loot_size=1):
    return {"title": title, "loot_size": loot_size,
            "entries": [(check(i), n, w) for i, n, w in entries]}


REWARD_TABLES = {
    # --- one random roll per tier (loot="tN") -------------------------------------------------
    "t0": table("Stone Age Cache", [
        ("minecraft:bread", 16, 4), ("minecraft:torch", 32, 4), ("minecraft:cooked_beef", 8, 3),
        ("minecraft:coal", 16, 3), ("minecraft:iron_ingot", 8, 2), ("minecraft:experience_bottle", 4, 2)]),
    "t1": table("Steam Age Cache", [
        ("minecraft:iron_ingot", 16, 4), (f"{MI}:coke", 16, 3), (f"{MI}:bronze_ingot", 8, 3),
        (f"{MI}:fire_clay_dust", 16, 2), ("minecraft:experience_bottle", 8, 2),
        ("minecraft:raw_copper", 32, 2)]),
    "t2": table("LV Cache", [
        (f"{MI}:steel_ingot", 8, 4), (f"{MI}:rubber_sheet", 16, 3), (f"{MI}:copper_wire", 16, 3),
        ("mekanism:ingot_osmium", 8, 2), ("minecraft:redstone", 32, 2), ("minecraft:ender_pearl", 4, 1)]),
    "t3": table("MV Cache", [
        (f"{MI}:aluminum_ingot", 8, 4), (f"{MI}:steel_gear", 4, 3), ("minecraft:blaze_rod", 8, 2),
        ("minecraft:quartz", 32, 2), ("ae2:certus_quartz_crystal", 16, 2), ("minecraft:diamond", 2, 1)]),
    "t4": table("HV Cache", [
        (f"{MI}:stainless_steel_ingot", 8, 4), ("ae2:fluix_crystal", 16, 3), ("mekanism:alloy_infused", 8, 3),
        ("minecraft:diamond", 4, 2), ("minecraft:golden_apple", 2, 2), ("apotheosis:gem_dust", 16, 1)]),
    "t5": table("EV Cache", [
        (f"{MI}:titanium_ingot", 8, 4), ("mekanism:alloy_reinforced", 8, 3), (f"{MI}:platinum_ingot", 4, 2),
        ("minecraft:emerald", 16, 2), ("apotheosis:sigil_of_socketing", 2, 2), ("minecraft:netherite_scrap", 1, 1)]),
    "t6": table("Nuclear Cache", [
        (f"{MI}:tungsten_ingot", 8, 4), ("mekanism:alloy_atomic", 4, 3), (f"{MI}:iridium_ingot", 2, 2),
        ("minecraft:shulker_shell", 4, 2), ("minecraft:totem_of_undying", 1, 1), ("minecraft:netherite_scrap", 2, 1)]),
    "t7": table("Stellar Cache", [
        ("mekanism:pellet_polonium", 2, 3), ("mekanism:pellet_plutonium", 2, 3), (f"{MI}:iridium_ingot", 4, 3),
        ("minecraft:echo_shard", 4, 2), ("minecraft:enchanted_golden_apple", 1, 1)]),
    # --- boss / monster hunting rolls (loot="hunt" / "boss") ----------------------------------
    "hunt": table("Hunter's Bounty", [
        ("minecraft:experience_bottle", 8, 4), ("minecraft:ender_pearl", 4, 3), ("minecraft:gunpowder", 16, 3),
        ("minecraft:name_tag", 1, 2), ("minecraft:golden_apple", 1, 1)]),
    "boss": table("Trophy Hoard", [
        ("minecraft:diamond", 8, 3), ("minecraft:enchanted_golden_apple", 1, 2), ("minecraft:totem_of_undying", 1, 2),
        ("minecraft:netherite_scrap", 2, 2), ("apotheosis:sigil_of_enhancement", 1, 1)], loot_size=2),
    # --- choose-one rewards (choice="pick_...") ----------------------------------------------
    "pick_early": table("Pick a Comfort", [
        ("comforts:sleeping_bag_white", 1, 1), ("waystones:warp_stone", 1, 1),
        ("sophisticatedbackpacks:upgrade_base", 2, 1), ("minecraft:saddle", 1, 1)]),
    "pick_mid": table("Pick a Feedstock", [
        (f"{MI}:raw_tin", 32, 1), (f"{MI}:raw_lead", 32, 1), (f"{MI}:raw_nickel", 32, 1),
        (f"{MI}:bauxite_dust", 32, 1), (f"{MI}:salt_dust", 64, 1)]),
    "pick_late": table("Pick a Treasure", [
        ("minecraft:totem_of_undying", 1, 1), ("minecraft:shulker_shell", 4, 1), ("minecraft:heart_of_the_sea", 1, 1),
        ("minecraft:enchanted_golden_apple", 1, 1)]),
    "secret": table("Hidden Stash", [
        ("minecraft:diamond", 4, 2), ("minecraft:experience_bottle", 16, 2), ("minecraft:golden_apple", 2, 1)]),
}
