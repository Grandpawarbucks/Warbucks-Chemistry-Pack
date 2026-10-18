"""Quest chapter: tools. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

CHAPTER = Chapter("tools", "Tools and Comfort", "silentgear:pickaxe",
        ["Better tools from better materials, and a soft place to land."], SIDE, [
    Q("tc_grader", 0, 0, [item("silentgear:material_grader")], "Material Grader", deps=["gs_silent"], xp=40, desc=[
        "Grades Silent Gear materials for a stat bonus. Better grades make better parts."]),
    Q("tc_salvager", 2, 0, [item("silentgear:salvager")], "Salvager", deps=["tc_grader"], xp=40, desc=[
        "Breaks old Silent Gear tools back into parts, so upgrading doesn't waste materials."]),
    Q("tc_bronze_paxel", 0, 2, [item("mekanismtools:bronze_paxel")], deps=["gs_paxel", "t0_bronze"], xp=25),
    Q("tc_osmium_paxel", 2, 2, [item("mekanismtools:osmium_paxel")], deps=["tc_bronze_paxel", "t3_infuser"], xp=40),
    Q("tc_diamond_paxel", 4, 2, [item("mekanismtools:diamond_paxel")], deps=["tc_osmium_paxel"], xp=50),
    Q("tc_obsidian_paxel", 6, 2, [item("mekanismtools:refined_obsidian_paxel")], "The Ultimate Paxel", deps=["tc_diamond_paxel"], xp=100, desc=[
        "Refined obsidian is Mekanism's toughest material."]),
    Q("tc_jetpack", 8, 0, [item("ironjetpacks:basic_coil"), item("ironjetpacks:jetpack")], "Jetpacks", deps=["t3_analog"], xp=100, desc=[
        "Iron Jetpacks run on FE. Every jetpack tier needs a coil, and in this pack the coils need MI circuits:",
        "&eBasic&r = analog (LV), &eAdvanced&r = electronic (MV), &eElite&r = digital (HV), &eUltimate&r = processing unit (EV).",
        "How: craft a coil, then the cells, thrusters and jetpack for the material you want (check JEI). Better metals fly faster and longer."]),
    Q("tc_angel", 8, 2, [item("angelring:diamond_ring"), item("angelring:angel_ring")], "The Angel Ring", deps=["t5_hv", "w_end"], xp=500, size=1.5, shape="hexagon", desc=[
        "Portable creative flight from a ring.",
        "It needs an Elytra, ghast tears, diamond blocks and Nether Stars, plus an &eMI digital circuit&r (polyethylene chemistry, HV).",
        "How: craft the Diamond Ring first, then the Angel Ring. Wear it in a Curios ring slot."]),
    Q("tc_hammock", 0, 4, [item("comforts:hammock_white")], "Hammock", deps=["gs_sleep"], xp=15, desc=[
        "Skips the day the way a sleeping bag skips the night."]),
    Q("tc_waystone", 2, 4, [item("waystones:warp_stone")], "Waystones", deps=["gs_iron"], xp=40, desc=[
        "Waystones (found in villages, or crafted) let you teleport between places you've visited.",
        "A Warp Stone lets you warp to any waystone from anywhere."]),
])
