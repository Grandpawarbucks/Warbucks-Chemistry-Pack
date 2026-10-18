"""Quest chapter: logic. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

CHAPTER = Chapter("logic", "Automation and Logic", "computercraft:computer_advanced",
        ["Make the factory run itself."], SIDE, [
    Q("lg_computer", 0, 0, [item("computercraft:computer_normal")], "A Computer", deps=["t3_hull"], xp=50, desc=[
        "CC: Tweaked computers run Lua programs. Monitor tanks, balance chemical lines, or build a base dashboard."]),
    Q("lg_turtle", 2, -1, [item("computercraft:turtle_normal")], "Turtles", deps=["lg_computer"], xp=75, desc=[
        "Programmable robots that mine, build and farm."]),
    Q("lg_peripherals", 2, 1, [item("advancedperipherals:energy_detector"), item("advancedperipherals:me_bridge")], "Advanced Peripherals", deps=["lg_computer", "t5_ae2"], xp=150, desc=[
        "Let computers read energy flow and your whole ME network."]),
    Q("lg_id", 0, 3, [item("integrateddynamics:cable", 8), item("integrateddynamics:logic_programmer"), item("integrateddynamics:variable", 4)], "Integrated Dynamics", deps=["t3_hull"], xp=100, desc=[
        "Logic networks without code: read a value (tank level, item count), apply logic, and act on it.",
        "Perfect for chemistry: stop the electrolyzer when the hydrogen tank is full."]),
    Q("lg_sfm", 2, 3, [item("sfm:manager"), item("sfm:cable", 8), item("sfm:disk")], "Super Factory Manager", deps=["lg_id"], xp=100, desc=[
        "Script exactly how items, fluids and energy move through a whole factory from one block."]),
    Q("lg_logistics", 4, 3, [item("logisticsnetworks:logistics_node", 2)], "Logistics Network", deps=["lg_sfm"], xp=75, desc=[
        "Nodes that route items between inventories by rules."]),
    Q("lg_laser", 4, 1, [item("laserio:card_item", 2)], "LaserIO Cards", deps=["s_laser"], xp=50, desc=[
        "Cards configure what each LaserIO node moves: items, fluids, energy, with filters."]),
    Q("lg_patterns", 6, 1, [item("ae2:pattern_provider"), item("ae2:molecular_assembler")], "Autocraft a Chemical Line", deps=["t5_ae2", "lg_peripherals"], xp=200, desc=[
        "Pattern providers can drive MI and Mekanism machines. Encode the steps of a chemical chain (say, sulfur to sulfuric acid) and AE2 runs it on request."]),
])
