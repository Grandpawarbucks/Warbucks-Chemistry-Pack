"""Quest chapter: magic. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

CHAPTER = Chapter("magic", "Divine Gifts", "ars_nouveau:novice_spell_book",
        ["Light magic, relics, and the enchanter's craft."], SIDE, [
    Q("m_book", 0, 0, [item("ars_nouveau:novice_spell_book")], deps=["t2_ars"], xp=50, desc=[
        "Write your first spells. Glyphs combine into effects."]),
    Q("m_jar", 2, 0, [item("ars_nouveau:source_jar"), item("ars_nouveau:imbuement_chamber")], deps=["m_book"], xp=75, desc=[
        "Source is magical energy. Store it in jars; the Imbuement Chamber uses it."]),
    Q("m_ritual", 4, 0, [item("ars_nouveau:ritual_flight")], "Ritual of Flight", deps=["m_jar"], xp=150, desc=[
        "Gives creative flight to players nearby, paid for with Source. Good for base flight."]),
    Q("m_apoth", 0, 2, [item("apotheosis:reforging_table")], "Apotheosis", deps=["gs_iron"], xp=50, desc=[
        "Gear with affixes and gems. Reforge, salvage and socket your way to divine equipment."]),
    Q("m_reliquary", 2, 2, [item("reliquary:mob_charm_fragment")], "Relics", deps=["m_apoth"], xp=50, desc=[
        "Reliquary, Relics and Artifacts add relics and artifacts to find and build. Some drop from mobs, others are hidden in structures."]),
])
