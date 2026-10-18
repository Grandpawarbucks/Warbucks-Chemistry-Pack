"""Quest chapter: storage. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

CHAPTER = Chapter("storage", "Storage and Logistics", "sophisticatedbackpacks:backpack",
        ["A god needs somewhere to keep things."], SIDE, [
    Q("s_barrel", 0, 0, [item("sophisticatedstorage:barrel")], deps=["gs_backpack"], xp=25, desc=[
        "Upgradable chests and barrels. Sophisticated Storage Plus raises their limits."]),
    Q("s_drawers", 2, 0, [item("functionalstorage:oak_1")], deps=["s_barrel"], xp=25, desc=[
        "Functional Storage drawers hold lots of one item. Pair them with a storage controller."]),
    Q("s_toms", 4, 0, [item("toms_storage:storage_terminal"), item("toms_storage:inventory_connector")], "An Early Network", deps=["s_drawers"], xp=75, desc=[
        "Tom's Simple Storage connects your chests into one searchable terminal. It's your network until AE2.",
        "How: place an Inventory Connector touching your chests (or link them with Inventory Cables), and a Storage Terminal on it."]),
    Q("s_furnace", 0, 2, [item("ironfurnaces:iron_furnace")], "Faster Furnaces", deps=["gs_iron"], xp=25, desc=[
        "Iron Furnaces: faster furnaces, and some can generate power."]),
    Q("s_pipes", 2, 2, [item("pipez:item_pipe", 8)], "Pipez", deps=["gs_iron"], xp=25, desc=[
        "Simple item, fluid and energy pipes for moving things between non-MI machines."]),
    Q("s_laser", 4, 2, [item("laserio:laser_node", 2)], "LaserIO", deps=["s_pipes", "t3_hull"], xp=75, desc=[
        "Moves items, fluids and energy between nodes without cables."]),
    Q("s_ae_drive", 6, 0, [item("ae2:drive"), item("ae2:terminal")], "AE2 Storage", deps=["t5_ae2"], xp=150, desc=[
        "Drives hold storage cells, and terminals let you see everything. MEGA Cells adds much bigger cells later."]),
    Q("s_ae_craft", 8, 0, [item("ae2:crafting_terminal")], "Autocrafting", deps=["s_ae_drive"], xp=150, desc=[
        "Pattern providers plus molecular assemblers turn whole chemical chains into one click. ME Requester keeps stock topped up automatically."]),
])
