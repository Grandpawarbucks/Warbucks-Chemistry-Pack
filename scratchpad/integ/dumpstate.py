import sys, json, io, contextlib, pathlib
tools = pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tools))
import os; os.chdir(tools.parent if (tools.parent / "test/ids.tsv").exists() else pathlib.Path(__file__).resolve().parents[2])
with contextlib.redirect_stdout(io.StringIO()):
    import questlib
    questlib.IDS  # noqa
    import quest_data as qd
out = {q.key: {"opt": bool(q.optional), "ch": c.key, "tick": q.tasks == [("checkmark",)], "deps": q.deps} for c in qd.CHAPTERS for q in c.quests}
json.dump(out, open(sys.argv[2], "w"))
print(len(out), len(qd.CHAPTERS))
