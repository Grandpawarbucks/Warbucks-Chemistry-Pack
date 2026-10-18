"""Quest chapter: farming. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

CHAPTER = Chapter("farming", "Farming", "botanypots:terracotta_hopper_botany_pot",
        ["Grow what you need, within the rules of chemistry."], SIDE, [
    Q("f_pot", 0, 0, [item("botanypots:terracotta_hopper_botany_pot")], "Hopper Botany Pots", deps=["gs_food"], xp=25, desc=[
        "Hopper Botany Pots grow crops and push the harvest into the container below.",
        "How: place one on a chest, add soil (dirt) and a seed."]),
    Q("f_altar", 2, 0, [item("mysticalagriculture:infusion_altar"), item("mysticalagriculture:inferium_essence", 16)], "Mystical Agriculture", deps=["f_pot"], xp=50, desc=[
        "Resource crops. Seeds are made on the Infusion Altar.",
        "&eTier 3/4/5 seeds need MI LV/MV/HV circuits&r, and crops for chemistry milestones (uranium, osmium, fluorite, silicon, steel, aluminum and others) can't be grown.",
        "Farming is a convenience here, not a shortcut."]),
])
