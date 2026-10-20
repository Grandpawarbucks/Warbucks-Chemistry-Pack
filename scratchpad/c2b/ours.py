import sys, pathlib, importlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
for s in sys.argv[1:]:
    ch = importlib.import_module(f"quests.{s}").CHAPTER
    print(f"== {s}: {len(ch.quests)} quests, links={[l[0] for l in ch.links]}")
    for q in ch.quests:
        t = "; ".join((f"{x[1]} x{x[2]}" if x[0]=="item" else (f"F[{x[1][:90]}] x{x[2]}" if x[0]=="filter" else x[0])) for x in q.tasks)
        print(f"{q.key:24} {'OPT' if q.optional else '   '} sz={q.size} deps={q.deps} | {q.title} | {t}")
