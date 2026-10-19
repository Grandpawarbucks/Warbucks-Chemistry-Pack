"""Quest book content: the Demigod's Codex. Edit this file, then run python3 tools/build_quests.py.

Conventions:
- Each quest teaches one step and says HOW to do it ("How:" line), so a new player is never lost.
- Story beats are gold (&6), key terms yellow (&e). FTB Quests renders & colour codes.
- Main chapters follow the tiers in docs/PROGRESSION.md; side chapters hang off main quests.
"""
import importlib
import os
import pathlib

from questlib import MAIN, SIDE  # noqa: F401
from quests._tables import REWARD_TABLES  # noqa: F401  (loot / choice reward tables)

BOOK_TITLE = "Warbucks Chemistry: The Demigod's Codex"

# Chapter groups (the left-hand tabs in the book), in display order. Each chapter's group is set
# here by key, so splitting or moving a chapter never touches quest keys (player progress is safe).
GROUPS = {
    "main": "The Demigod's Path",
    "chem": "Chemistry Lab",
    "eng": "Engineering",
    "magic": "Magic and Relics",
    "world": "Exploration",
    "life": "Farming and Food",
    "extra": "Collections",
}
LAYOUT = {
    "main": ["welcome", "start", "t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7", "seed", "creation"],
    "chem": ["periodic", "lab_notes", "mekanism"],
    "eng": ["power", "powah", "factory", "logic", "create", "tools", "justdirethings", "storage", "ae2", "building"],
    "magic": ["ars", "apotheosis", "relics", "occultism", "projecte", "magic"],
    "world": ["worlds", "undergarden", "twilight", "deeperdarker", "space", "explore", "hunting"],
    "life": ["farming", "mystical"],
    "extra": ["qol", "utilitarian", "market", "completionist"],
}
# Chapter files that don't exist yet are skipped, so new chapters can be added one at a time.
_QDIR = pathlib.Path(__file__).resolve().parent / "quests"
ORDER = [k for g in LAYOUT.values() for k in g if (_QDIR / f"{k}.py").exists()]
# Writers can validate just their own chapters (plus the main tiers) while others are mid-edit:
#   QUEST_ONLY=ars,apotheosis python3 tools/build_quests.py --check
ONLY = [k for k in os.environ.get("QUEST_ONLY", "").split(",") if k]
if ONLY:
    ORDER = [k for k in ORDER if k in ONLY or k in ("welcome", "start", *(f"t{i}" for i in range(8)))]
CHAPTERS = [importlib.import_module(f"quests.{k}").CHAPTER for k in ORDER]
for _c in CHAPTERS:
    _c.group = next(g for g, ks in LAYOUT.items() if _c.key in ks)

# Demigod Tokens per quest, scaled by tier (milestone quests, size >= 1.5, pay double).
TOKENS = {"welcome": 1, "start": 1, "t0": 1, "t1": 2, "t2": 2, "t3": 3, "t4": 3, "t5": 4, "t6": 5, "t7": 8,
          "seed": 10, "creation": 10, "completionist": 3}
for _c in CHAPTERS:
    _c.tokens = TOKENS.get(_c.key, 1)

# Tier milestones (size >= 1.5 in t0..t7) also roll that tier's loot table, unless set by hand.
for _c in CHAPTERS:
    if _c.key in REWARD_TABLES:
        for _q in _c.quests:
            if (_q.size or 1) >= 1.5 and not _q.loot and not _q.optional:
                _q.loot = _c.key
