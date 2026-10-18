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
MAIN, SIDE = "main", "side"


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


def kill(entity, count=1):
    """Kill task: kill `count` of this entity type (e.g. kill("minecraft:zombie", 25))."""
    return ("kill", check(entity), count)


def structure(id_):
    """Structure task: stand inside this structure."""
    return ("structure", check(id_))


def biome(id_):
    """Biome task: visit this biome."""
    return ("biome", check(id_))


def anytag(tag, count=1):
    """Item task matching ANY item in a tag (FTB Filter System smart filter), e.g. anytag("minecraft:logs", 16)."""
    return ("filter", f"item_tag({tag})", count)


def anyof(ids, count=1):
    """Item task matching any one of several items (FTB Filter System smart filter)."""
    return ("filter", "or(" + "".join(f"item({check(i)})" for i in ids) + ")", count)


def tick():
    """Checkmark task: the player clicks to complete (used for tips and story beats)."""
    return ("checkmark",)


class Q:
    """One quest. x/y are grid positions in the chapter; deps are other quest keys (any chapter)."""

    def __init__(self, key, x, y, tasks, title=None, desc=(), deps=(), xp=0, items=(),
                 subtitle=None, size=None, shape=None, tokens=None, optional=False,
                 hidden=False, secret=False, any_dep=False, loot=None, choice=None):
        self.key, self.x, self.y, self.tasks = key, x, y, tasks
        self.optional = optional  # optional side quest: shown, but not needed to progress
        self.hidden = hidden      # hidden until its dependencies are visible
        self.secret = secret      # invisible until completed (secret quests); never required for completion
        if secret:
            self.optional = True
        self.any_dep = any_dep    # completes its lock when ANY one dependency is done (alternative routes)
        self.loot = loot          # reward table key: one random roll from that table
        self.choice = choice      # reward table key: player chooses one item from that table
        self.tokens = tokens  # None = chapter default (doubled for milestone quests, size >= 1.5)
        self.title, self.desc, self.deps, self.xp = title, list(desc), list(deps), xp
        self.items = [(check(i), n) for i, n in items]
        self.subtitle, self.size, self.shape = subtitle, size, shape


class Chapter:
    def __init__(self, key, title, icon, subtitle, group, quests, tokens=1, links=()):
        self.tokens = tokens  # Demigod Tokens per quest in this chapter (tier-scaled reward)
        self.links = list(links)  # quest links: (quest_key_in_another_chapter, x, y)
        self.key, self.title, self.icon = key, title, check(icon)
        self.subtitle, self.group, self.quests = subtitle, group, quests
