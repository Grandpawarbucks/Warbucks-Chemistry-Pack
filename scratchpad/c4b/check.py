"""--check wrapper that also builds chapter files not yet in LAYOUT (artifacts, silentgear, apothic_enchanting).
Usage: QUEST_ONLY=a,b python scratchpad/c4b/check.py   (adds the new keys to LAYOUT in memory only)."""
import importlib.util, pathlib, runpy, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))
src = (TOOLS / "quest_data.py").read_text(encoding="utf-8")
src = src.replace('"gear": ["tools", "harvest", "apotheosis", "relics", "qol"]',
                  '"gear": ["tools", "harvest", "apotheosis", "relics", "artifacts", "silentgear", "qol"]')
src = src.replace('"magic": ["ars", "occultism", "neovitae", "projecte"]',
                  '"magic": ["ars", "occultism", "neovitae", "apothic_enchanting", "projecte"]')
src = src.replace('"apotheosis": "apotheosis_gear",', '"apotheosis": "apotheosis_gear", "artifacts": "artifacts", "silentgear": "silent_gear", "apothic_enchanting": "apothic_enchanting",')
spec = importlib.util.spec_from_loader("quest_data", loader=None, origin=str(TOOLS / "quest_data.py"))
mod = importlib.util.module_from_spec(spec)
mod.__file__ = str(TOOLS / "quest_data.py")
sys.modules["quest_data"] = mod
exec(compile(src, str(TOOLS / "quest_data.py"), "exec"), mod.__dict__)
sys.argv = [str(TOOLS / "build_quests.py"), "--check"]
runpy.run_path(str(TOOLS / "build_quests.py"), run_name="__main__")
