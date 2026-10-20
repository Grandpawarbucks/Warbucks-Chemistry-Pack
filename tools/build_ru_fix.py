#!/usr/bin/env python3
"""Work around a world-generation deadlock between Regions Unexplored 0.6.2 and Lithostitched 1.8.1.

Eight Regions Unexplored placed features filter with `not(lithostitched:in_structure, search_range 4)`. That predicate
calls level.getChunk() on chunks up to 4 away from inside a worldgen worker; when those chunks aren't generated yet the
worker waits on itself and chunk generation stops (found 2026-10-20: Chunky stuck at 50% with a worker parked in
InStructurePredicate.test). This writes the same placed features without that one filter into pack/kubejs/data, so they
still generate but no longer avoid structures. Re-run after updating Regions Unexplored, and delete the overrides once
a fixed version ships.
Run: python tools/build_ru_fix.py (reads the jar from test/server/mods)
"""
import json
import pathlib
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "pack/kubejs/data"


def strip(placement):
    keep = []
    for step in placement:
        pred = step.get("predicate", {}) if step.get("type") == "minecraft:block_predicate_filter" else {}
        inner = pred.get("predicate", {}) if pred.get("type") == "minecraft:not" else pred
        if inner.get("type") == "lithostitched:in_structure":
            continue
        keep.append(step)
    return keep


def main():
    jar = next((ROOT / "test/server/mods").glob("regions-unexplored-*.jar"))
    n = 0
    with zipfile.ZipFile(jar) as z:
        for name in z.namelist():
            if "/worldgen/placed_feature/" not in name or not name.endswith(".json"):
                continue
            text = z.read(name).decode("utf-8")
            if "lithostitched:in_structure" not in text:
                continue
            obj = json.loads(text)
            obj["placement"] = strip(obj["placement"])
            assert "in_structure" not in json.dumps(obj), name
            dest = OUT / name[len("data/"):]
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8", newline="\n")
            n += 1
            print("override", dest.relative_to(ROOT))
    print(f"{n} Regions Unexplored placed features written without lithostitched:in_structure ({jar.name})")


if __name__ == "__main__":
    main()
