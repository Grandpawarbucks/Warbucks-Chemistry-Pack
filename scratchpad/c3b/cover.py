import importlib, pathlib, sys, collections
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import layout
for key, stem in [("create", "create"), ("justdirethings", "justdirethings"), ("mekanism", "mekanism"), ("mekanism_power", "mekanism_reactors")]:
    ch = importlib.import_module(f"quests.{key}").CHAPTER
    atm = layout.load_mirror(stem)
    ids = [q.mirror for q in ch.quests if q.mirror]
    dup = [i for i, n in collections.Counter(ids).items() if n > 1]
    bad = [i for i in ids if i not in atm["quests"]]
    missing = [a for a in atm["order"] if a not in ids]
    opt = sum(1 for q in ch.quests if q.optional)
    print(f"{key}: {len(ch.quests)} quests ({opt} optional), mirrored {len(set(ids))}/{len(atm['order'])}, dup {dup}, bad {bad}")
    for a in missing:
        print("   unmatched ATM10:", a, atm["quests"][a]["item"])
