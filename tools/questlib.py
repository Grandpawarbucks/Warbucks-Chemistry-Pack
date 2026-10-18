"""Helpers for the quest book: quest/chapter classes, task constructors, and id checking.

Every item and dimension id passed to item()/dim()/Chapter(icon=...) is checked against
test/ids.tsv (built by test/build_id_index.py). Unknown ids are collected in ERRORS and the
build refuses to write anything.
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
_IDS_FILE = ROOT / "test/ids.tsv"
if not _IDS_FILE.exists():
    raise SystemExit("test/ids.tsv missing: run test/smoke.sh, then python3 test/build_id_index.py")
IDS = {line.split("\t")[0] for line in _IDS_FILE.read_text().splitlines()}
ERRORS = []


def check(id_):
    if id_ not in IDS:
        ERRORS.append(id_)
    return id_


def item(id_, count=1):
    """Item task: have `count` of this item in your inventory (any components)."""
    return ("item", check(id_), count)


def dim(id_):
    """Dimension task: visit this dimension."""
    return ("dimension", check(id_))


def tick():
    """Checkmark task: the player clicks to complete (used for tips and story beats)."""
    return ("checkmark",)


class Q:
    """One quest. x/y are grid positions in the chapter; deps are other quest keys (any chapter)."""

    def __init__(self, key, x, y, tasks, title=None, desc=(), deps=(), xp=0, items=(),
                 subtitle=None, size=None, shape=None):
        self.key, self.x, self.y, self.tasks = key, x, y, tasks
        self.title, self.desc, self.deps, self.xp = title, list(desc), list(deps), xp
        self.items = [(check(i), n) for i, n in items]
        self.subtitle, self.size, self.shape = subtitle, size, shape


class Chapter:
    def __init__(self, key, title, icon, subtitle, group, quests):
        self.key, self.title, self.icon = key, title, check(icon)
        self.subtitle, self.group, self.quests = subtitle, group, quests
