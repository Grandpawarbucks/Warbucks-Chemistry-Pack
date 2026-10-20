"""Quest chapter: ars. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

Mirrors ATM10's "ars_nouveau" chapter quest for quest (its quest list, order, clusters and requirements only; every
word here is ours): first steps and spell books, three glyph tiers (one quest per glyph), Source, the Apparatus,
magebloom, helpers, enchanter's gear and rituals. Our own essences, Wilden, Ars Elemental, mage armor and Ars
Additions quests stay as side sections. Recipes checked against ars_nouveau 5.13.3, ars_elemental 0.7.10.4 and
ars_additions 21.3.0. The only pack change to Ars is the Ritual of Flight tablet: it needs 2 chemlib:hydrogen
(pack/kubejs/server_scripts/phase4_flight.js), so ritual flight arrives with the Infusion Pylon (t2_pylon).
"""
from questlib import Q, Chapter, item, dim, tick, kill, anyof, anytag, SIDE  # noqa: F401

