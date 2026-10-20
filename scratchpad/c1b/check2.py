"""Run build_quests.py --check with "eae" added to LAYOUT["storage"] in memory (quest_data.py itself is untouched)."""
import os, sys, types, pathlib, runpy
_ARGS = sys.argv[1:]

TOOLS = pathlib.Path(__file__).resolve().parents[2] / "tools"
sys.path.insert(0, str(TOOLS))
os.chdir(TOOLS.parent)
path = TOOLS / "quest_data.py"
src = path.read_text(encoding="utf-8")
old = '"storage": ["storage", "ae2"],'
assert old in src, "LAYOUT line changed"
src = src.replace(old, '"storage": ["storage", "ae2", "eae"],', 1)
mod = types.ModuleType("quest_data")
mod.__file__ = str(path)
sys.modules["quest_data"] = mod
exec(compile(src, str(path), "exec"), mod.__dict__)
sys.argv = [str(TOOLS / "build_quests.py")] + (_ARGS or ["--check"])
runpy.run_path(str(TOOLS / "build_quests.py"), run_name="__main__")
