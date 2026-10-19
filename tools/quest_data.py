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
from layout import normalize_milestones
from quests._tables import REWARD_TABLES  # noqa: F401  (loot / choice reward tables)

BOOK_TITLE = "Warbucks Chemistry: The Demigod's Codex"

# Chapter groups (the left-hand tabs in the book), in display order. Each chapter's group is set
# here by key, so splitting or moving a chapter never touches quest keys (player progress is safe).
# "top" is the ungrouped area above the first tab (title None): FTB Quests shows chapters whose group is ""
# there, as ATM10 does with Welcome and its market pages. A group's id comes from its key, so keys never change;
# titles can. Groups with no chapter (e.g. while a QUEST_ONLY check runs) are not written.
GROUPS = {
    "top": None,
    "main": "The Demigod's Path",
    "basics": "Basics",
    "chem": "Chemistry Lab",
    "eng": "Industry and Automation",
    "magic": "Magic and Relics",
    "world": "Exploration",
    "life": "Resources",
}
LAYOUT = {
    "top": ["welcome", "market", "lab_notes", "completionist"],
    "main": ["start", "t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7", "seed", "creation"],
    # Beginner "comfort" pages (ATM10's Basic Tools/Storage/Power idea). utilitarian is merged into qol.
    "basics": ["tools", "harvest", "storage", "power", "powah", "farming", "qol", "building"],
    "chem": ["periodic", "mekanism", "mekanism_power"],
    "eng": ["factory", "logic", "create", "justdirethings", "ae2"],
    "magic": ["ars", "occultism", "apotheosis", "relics", "projecte"],
    "world": ["worlds", "explore", "undergarden", "twilight", "deeperdarker", "space", "hunting"],
    "life": ["mystical"],
}
# Chapter files that don't exist yet are skipped, so new chapters can be added one at a time.
_QDIR = pathlib.Path(__file__).resolve().parent / "quests"
ORDER = [k for g in LAYOUT.values() for k in g if (_QDIR / f"{k}.py").exists()]
# A chapter file that isn't in LAYOUT is not built: say so (its quests would silently vanish otherwise).
UNLISTED = sorted(f.stem for f in _QDIR.glob("*.py") if not f.stem.startswith("_") and f.stem not in ORDER)
# Writers can validate just their own chapters (plus the main tiers) while others are mid-edit:
#   QUEST_ONLY=ars,apotheosis python3 tools/build_quests.py --check
ONLY = [k for k in os.environ.get("QUEST_ONLY", "").split(",") if k]
if ONLY:
    ORDER = [k for k in ORDER if k in ONLY or k in ("welcome", "start", *(f"t{i}" for i in range(8)))]
CHAPTERS = [importlib.import_module(f"quests.{k}").CHAPTER for k in ORDER]
for _c in CHAPTERS:
    _c.group = next(g for g, ks in LAYOUT.items() if _c.key in ks)
    normalize_milestones(_c)  # capstone = 2.0 gear, section milestone = 1.5 hexagon (tools/layout.py)

# Demigod Tokens per quest, scaled by tier (milestone quests, size >= 1.5, pay double).
TOKENS = {"welcome": 1, "start": 1, "t0": 1, "t1": 2, "t2": 2, "t3": 3, "t4": 3, "t5": 4, "t6": 5, "t7": 8,
          "seed": 10, "creation": 10, "completionist": 3, "harvest": 1}
for _c in CHAPTERS:
    _c.tokens = TOKENS.get(_c.key, 1)

# Tier milestones (size >= 1.5 in t0..t7) also roll that tier's loot table, unless set by hand.
for _c in CHAPTERS:
    if _c.key in REWARD_TABLES:
        for _q in _c.quests:
            if (_q.size or 1) >= 1.5 and not _q.loot and not _q.optional:
                _q.loot = _c.key
