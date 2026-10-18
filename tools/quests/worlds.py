"""Quest chapter: worlds. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

CHAPTER = Chapter("worlds", "Other Worlds", "deeperdarker:heart_of_the_deep",
        ["Realms beyond the Overworld."], SIDE, [
    Q("w_otherside", 0, 0, [item("deeperdarker:heart_of_the_deep"), dim("deeperdarker:otherside")], "The Otherside", deps=["t2_nether"], xp=300, desc=[
        "Beyond the Ancient City lies the Otherside. Take a Heart of the Deep from the Warden."]),
    Q("w_end", 2, 0, [dim("minecraft:the_end")], "The End", deps=["t2_nether"], xp=200, desc=[
        "End Crystals from here power Just Dire Things' flight upgrade."]),
    Q("w_echo", 0, 2, [item("deeperdarker:reinforced_echo_shard", 4)], "Echoes of the Deep", deps=["w_otherside"], xp=200, desc=[
        "The Otherside's strongest material, for gear that rivals netherite."]),
    Q("w_undergarden", 2, 2, [item("undergarden:cloggrum_ingot", 8), item("undergarden:froststeel_ingot", 4), item("undergarden:utherium_crystal", 4)], "Undergarden Metals", deps=["t4_undergarden"], xp=200, desc=[
        "New ores beneath the world: cloggrum, froststeel and utherium. Run them through the Dissolver: what are they made of?"]),
    Q("w_naga", 4, 0, [item("twilightforest:naga_scale", 4)], "The Naga", deps=["t5_twilight"], xp=200, desc=[
        "The Twilight Forest's first boss, coiled in a courtyard. Its scales unlock the path forward."]),
    Q("w_lich", 6, 0, [item("twilightforest:lich_trophy")], "The Lich", deps=["w_naga"], xp=300, desc=[
        "A sorcerer atop a tower. Defeating it opens the deeper Twilight."]),
    Q("w_tf_metals", 6, 2, [item("twilightforest:ironwood_ingot", 4), item("twilightforest:knightmetal_ingot", 4), item("twilightforest:fiery_ingot", 2)], "Twilight Metals", deps=["w_lich"], xp=250, desc=[
        "Ironwood, knightmetal and fiery metal: alloys found nowhere else."]),
    Q("w_mars", 8, -1, [dim("ad_astra:mars"), item("ad_astra:tier_2_rocket")], "Mars", deps=["t7_rocket"], xp=500, desc=[
        "The red planet: iron oxide dust over everything. Desh is mined here."]),
    Q("w_venus", 10, -1, [dim("ad_astra:venus"), item("ad_astra:tier_3_rocket")], "Venus", deps=["w_mars"], xp=600, desc=[
        "Sulfuric acid clouds and crushing CO₂ pressure. Bring your best suit: the atmosphere is a chemistry lesson in itself."]),
    Q("w_space_metals", 12, -1, [item("ad_astra:desh_ingot", 8), item("ad_astra:ostrum_ingot", 4), item("ad_astra:calorite_ingot", 4)], "Alien Metals", deps=["w_venus"], xp=600, desc=[
        "Desh, ostrum and calorite. Each one builds the next rocket tier."]),
])
