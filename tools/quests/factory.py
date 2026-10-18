"""Quest chapter: factory. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

CHAPTER = Chapter("factory", "Mob Data and Big Crafting", "hostilenetworks:sim_chamber",
        ["Monifactory-inspired machinery: simulate mobs, craft on giant tables, and fold whole factories into a block."], SIDE, [
    Q("mf_learner", 0, 0, [item("hostilenetworks:deep_learner"), item("hostilenetworks:blank_data_model")], "Deep Learning", deps=["gs_iron"], xp=40, desc=[
        "Hostile Neural Networks: put a data model for a mob in the Deep Learner, then fight that mob to train it.",
        "How: right-click a blank data model on a mob type (or craft a specific one), and keep the Deep Learner in your inventory while you fight."]),
    Q("mf_sim", 2, 0, [item("hostilenetworks:sim_chamber"), item("hostilenetworks:prediction_matrix", 4)], "Simulation", deps=["mf_learner", "t4_mv"], xp=150, desc=[
        "The Simulation Chamber runs a trained model on power and prediction matrices to produce mob drops without the mob.",
        "In this pack it needs an &eMV electronic circuit&r, so a trained model pays off once you reach aluminum chemistry."]),
    Q("mf_fab", 4, 0, [item("hostilenetworks:loot_fabricator")], "Loot Fabricator", deps=["mf_sim"], xp=150, desc=[
        "Turns simulated predictions into specific drops. Also needs an MV electronic circuit."]),
    Q("mf_basic_table", 0, 2, [item("extendedcrafting:black_iron_ingot", 8), item("extendedcrafting:basic_table")], "Extended Crafting", deps=["t1_steel"], xp=50, desc=[
        "Black iron is the frame of Extended Crafting. The Basic Table is a 3x3 table for its recipes.",
        "How: check JEI for black iron. The bigger tables come later."]),
    Q("mf_adv_table", 2, 2, [item("extendedcrafting:advanced_table")], "5x5: Advanced Table", deps=["mf_basic_table", "t4_mv"], xp=100, desc=[
        "Needs an MV electronic circuit."]),
    Q("mf_elite_table", 4, 2, [item("extendedcrafting:elite_table")], "7x7: Elite Table", deps=["mf_adv_table", "t5_hv"], xp=200, desc=[
        "Needs an HV digital circuit."]),
    Q("mf_ult_table", 6, 2, [item("extendedcrafting:ultimate_table")], "9x9: Ultimate Table", deps=["mf_elite_table", "t6_pu"], xp=400, desc=[
        "Needs an EV processing unit. The endgame's biggest crafts happen here."]),
    Q("mf_packaged", 6, 0, [item("packagedauto:packager"), item("packagedauto:unpackager")], "Packaged Automation", deps=["t5_ae2", "mf_adv_table"], xp=150, desc=[
        "Packaged Auto lets AE2 autocraft with Extended Crafting tables (through the PackagedExCrafting addon). Put a big recipe in a pattern and AE2 does the rest."]),
    Q("mf_compact", 0, 4, [item("compactmachines:personal_shrinking_device")], "Compact Machines", deps=["t3_hull"], xp=75, desc=[
        "Fold an entire factory into a single block. The Personal Shrinking Device lets you walk inside it."]),
    Q("mf_facade", 2, 4, [item("cable_facades:facade_wrench")], "Hide the Cables", deps=["t3_hull"], xp=25, desc=[
        "Cable Facades disguise cables and pipes as any block. Tidy factories, same throughput."]),
    Q("mf_cake", 4, 4, [item("telepastries:overworld_cake")], "Teleporting Cake", deps=["t2_nether"], xp=40, desc=[
        "TelePastries: eat a slice to travel to that cake's dimension. Refill it with the right ingredient."]),
])
