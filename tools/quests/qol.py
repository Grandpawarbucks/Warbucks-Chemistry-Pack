"""Quest chapter: qol. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

CHAPTER = Chapter("qol", "Quality of Life", "akashictome:tome",
        ["Small things that make a big difference."], SIDE, [
    Q("q_tome", 0, 0, [item("akashictome:tome")], "One Book to Rule Them All", deps=["gs_table"], xp=20, desc=[
        "The Akashic Tome merges every mod's guidebook into one item.",
        "How: craft it, then right-click it with other guidebooks to add them."]),
    Q("q_compass", 2, 0, [item("naturescompass:naturescompass"), item("explorerscompass:explorerscompass")], "Find Anything", deps=["gs_iron"], xp=30, desc=[
        "Nature's Compass finds biomes; Explorer's Compass finds structures (Nether Fortresses, Ancient Cities, villages)."]),
    Q("q_torch", 4, 0, [item("torchmaster:megatorch")], "No More Mob Spawns", deps=["gs_iron"], xp=40, desc=[
        "The Mega Torch stops hostile mobs spawning in a huge radius. Great around your base."]),
    Q("q_grave", 6, 0, [tick()], "Graves", deps=["gs_iron"], xp=10, desc=[
        "If you die, Corail Tombstone keeps your items in a grave where you fell. Walk back and open it to recover everything."]),
    Q("q_bp_up", 0, 2, [item("sophisticatedbackpacks:pickup_upgrade"), item("sophisticatedbackpacks:magnet_upgrade")], "Backpack Upgrades", deps=["gs_backpack"], xp=40, desc=[
        "Pickup and magnet upgrades pull items straight into your backpack. There's also feeding, crafting, smelting and more (check JEI)."]),
    Q("q_waystone", 2, 2, [item("waystones:waystone")], "Waystones", deps=["gs_iron"], xp=40, desc=[
        "Place waystones at your important locations and teleport between them."]),
    Q("q_gadget", 4, 2, [item("buildinggadgets2:gadget_building")], "Building Gadgets", deps=["t3_hull"], xp=40, desc=[
        "Place and copy whole structures with FE-powered gadgets."]),
    Q("q_effortless", 6, 2, [item("effortlessbuilding:randomizer_tool")], "Effortless Building", deps=["gs_table"], xp=20, desc=[
        "Mirror, array and line building modes for big builds. The randomizer places a random mix of blocks."]),
    Q("q_backups", 8, 1, [tick()], "Backups", deps=["gs_iron"], xp=10, desc=[
        "Simple Backups saves your world automatically. On a server, backups live in the server's backups folder."]),
])
