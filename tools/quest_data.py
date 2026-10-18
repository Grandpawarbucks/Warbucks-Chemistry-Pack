"""Quest book content: the Demigod's Codex. Edit this file, then run python3 tools/build_quests.py.

Conventions:
- Each quest teaches one step and says HOW to do it ("How:" line), so a new player is never lost.
- Story beats are gold (&6), key terms yellow (&e). FTB Quests renders & colour codes.
- Main chapters follow the tiers in docs/PROGRESSION.md; side chapters hang off main quests.
"""
import importlib

from questlib import MAIN, SIDE  # noqa: F401

GROUPS = {MAIN: "The Demigod's Path", SIDE: "Divine Workshop"}
BOOK_TITLE = "Warbucks Chemistry: The Demigod's Codex"

# Chapter order (each chapter lives in tools/quests/<key>.py)
ORDER = ['welcome', 'start', 't0', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 'tools', 'factory', 'qol', 'periodic', 'power', 'logic', 'create', 'storage', 'magic', 'worlds', 'farming']
CHAPTERS = [importlib.import_module(f"quests.{k}").CHAPTER for k in ORDER]

# Demigod Tokens per quest, scaled by tier (milestone quests, size >= 1.5, pay double).
TOKENS = {"welcome": 1, "start": 1, "t0": 1, "t1": 2, "t2": 2, "t3": 3, "t4": 3, "t5": 4, "t6": 5, "t7": 8}
for _c in CHAPTERS:
    _c.tokens = TOKENS.get(_c.key, 1)
