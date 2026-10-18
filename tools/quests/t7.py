"""Quest chapter: t7. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

CHAPTER = Chapter("t7", "VIII. Creation", "ad_astra:tier_1_rocket",
        ["Leave the cradle. Make matter from energy. Seed a new world."], MAIN, [
    Q("t7_nasa", 0, 0, [item("ad_astra:nasa_workbench")], "Leaving the Cradle", deps=["t6_pu"], xp=400, desc=[
        "The NASA Workbench needs an EV hull. Rockets burn MI diesel."]),
    Q("t7_suit", 2, -2, [item("ad_astra:space_helmet"), item("ad_astra:oxygen_loader")], "Breathe", deps=["t7_nasa"], xp=200, desc=[
        "Space has no air. Fill your space suit with oxygen from your electrolysis line."]),
    Q("t7_rocket", 2, 0, [item("ad_astra:tier_1_rocket"), dim("ad_astra:moon")], "One Small Step", deps=["t7_nasa"], xp=600, size=1.5, desc=[
        "Reach the Moon.",
        "How: build the rocket in the NASA Workbench, fuel it with diesel, and climb in."]),
    Q("t7_antimatter", 4, 0, [item("mekanism:sps_casing", 4), item("mekanism:pellet_antimatter")], "Antimatter", deps=["t7_rocket", "t6_waste"], xp=1000, size=1.75, shape="hexagon", desc=[
        "The Supercritical Phase Shifter turns polonium into &eantimatter&r: matter with every charge reversed.",
        "It's the most energy-dense substance there is."]),
    Q("t7_cores", 6, -2, [item("kubejs:energy_core"), item("kubejs:antimatter_core")], "Energy Cores", deps=["t7_antimatter"], xp=1000, size=1.5, desc=[
        "A stainless-steel shell with polonium and a processing unit becomes an &eEmpty Energy Core&r. Charge it in MI's Assembler (about 3 million EU).",
        "Add antimatter and a quantum circuit and it becomes an &eAntimatter Core&r: the most concentrated energy you can hold."]),
    Q("t7_seed", 8, -1, [item("kubejs:seed_of_a_new_world")], "Seed of a New World", deps=["t7_cores", "t6_table", "mf_ult_table"], xp=3000, size=2.0, shape="hexagon", desc=[
        "&6The endgame goal.&r A 9x9 recipe on the Ultimate Table that needs something from every tier:",
        "coke, synthesized water and hydrogen, sulfuric acid, polyethylene, stainless steel, processing units, oganesson, plutonium, polonium, Nether Stars, four Antimatter Cores, and a Dragon Egg at the centre.",
        "Check JEI for the exact layout."]),
    Q("t7_creation", 10, 0, [tick()], "A New World", deps=["t7_seed"], xp=2000, size=2.5, shape="gear", tokens=50, desc=[
        "&6You took the world apart, element by element, and learned to build it again.&r",
        "Fire, steel, acid, oil, silicon, the atom, antimatter. Every tier was a lesson in chemistry, and you mastered them all.",
        "The worlds out there are blank canvases now. Go make them yours."]),
])
