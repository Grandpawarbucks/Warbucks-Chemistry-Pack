"""Scratch: run build_quests --check with extra chapter keys added to LAYOUT (for new, not-yet-listed files).
Usage: check.py group=key[,key] ... (QUEST_ONLY env as usual)."""
import sys, pathlib, types, runpy
ROOT = pathlib.Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))
extra = [a for a in sys.argv[1:] if "=" in a]
src = (TOOLS / "quest_data.py").read_text(encoding="utf-8")
inject = "".join(f"\nLAYOUT[{g!r}] = LAYOUT[{g!r}] + {ks.split(',')!r}" for g, ks in (a.split("=", 1) for a in extra))
marker = "# Sidebar titles"
src = src.replace(marker, inject + "\n" + marker, 1)
mod = types.ModuleType("quest_data"); mod.__file__ = str(TOOLS / "quest_data.py")
sys.modules["quest_data"] = mod
exec(compile(src, str(TOOLS / "quest_data.py"), "exec"), mod.__dict__)
sys.argv = [str(TOOLS / "build_quests.py"), "--check"]
runpy.run_path(str(TOOLS / "build_quests.py"), run_name="__main__")
