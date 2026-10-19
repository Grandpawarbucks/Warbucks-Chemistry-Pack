#!/usr/bin/env python3
"""Compare another pack's FTB quest book with ours: which items do they quest on that exist in our pack
but that our book never asks for? A checklist for chapter writers.

Uses task REQUIREMENTS only (item ids). Never copy another pack's quest files or text into this repo:
ATM10, for example, is All Rights Reserved. Read the list, then write our own quests (tools/quests/STYLE.md).

usage:
  python tools/quest_compare.py <their config/ftbquests/quests folder>              summary per chapter
  python tools/quest_compare.py <folder> --mod undergarden                           every missing item of one mod
  python tools/quest_compare.py <folder> --chapter twilight_forest                   every missing item of one chapter

Reads test/ids.tsv (what exists in our pack) and pack/config/ftbquests/quests (our generated book), so run
python tools/build_quests.py first if you changed quests.
"""
import argparse
import collections
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
ITEM = re.compile(r'item: (?:\{[^}]*?id: )?"([a-z0-9_]+:[a-z0-9_/]+)"')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("theirs", help="the other pack's config/ftbquests/quests folder")
    ap.add_argument("--mod", help="list every missing item of this namespace")
    ap.add_argument("--chapter", help="list every missing item of this chapter (file name without .snbt)")
    args = ap.parse_args()

    names = {}
    for line in (ROOT / "test/ids.tsv").read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        names[parts[0]] = names.get(parts[0]) or (parts[2] if len(parts) > 2 else "")  # unnamed registry rows keep the lang name
    ours = set()
    for f in (ROOT / "pack/config/ftbquests/quests/chapters").glob("*.snbt"):
        text = f.read_text(encoding="utf-8")
        ours |= set(re.findall(r'id: "([a-z0-9_]+:[a-z0-9_/]+)"', text))
        # anyof() tasks are FTB Filter System strings listing item(ns:id). anytag() tasks are not expanded,
        # so items our book only asks for through a tag still show up as missing.
        ours |= set(re.findall(r'(?<![_a-z])item\(([a-z0-9_]+:[a-z0-9_/]+)\)', text))

    chapters = {}
    for f in sorted((pathlib.Path(args.theirs) / "chapters").glob("*.snbt")):
        found = list(dict.fromkeys(ITEM.findall(f.read_text(encoding="utf-8", errors="replace"))))
        in_pack = [i for i in found if i in names]
        if in_pack:
            chapters[f.stem] = (len(found), in_pack, [i for i in in_pack if i not in ours])

    if args.mod or args.chapter:
        seen = {}
        for ch, (_, _, missing) in chapters.items():
            if args.chapter and ch != args.chapter:
                continue
            for i in missing:
                if not args.mod or i.startswith(args.mod + ":"):
                    seen.setdefault(i, ch)
        for i, ch in sorted(seen.items()):
            print(f"{i}\t{names[i]}\t(their chapter: {ch})")
        print(f"{len(seen)} items")
        return

    print(f"{'their chapter':32} {'items':>5} {'in our pack':>11} {'not in our book':>15}")
    for ch, (n, in_pack, missing) in sorted(chapters.items(), key=lambda kv: -len(kv[1][2])):
        eg = ", ".join(m.split(":")[1] for m in missing[:5])
        print(f"{ch:32} {n:5} {len(in_pack):11} {len(missing):15}   e.g. {eg}")
    total = {m for _, _, ms in chapters.values() for m in ms}
    by_mod = collections.Counter(m.split(":")[0] for m in total)
    print(f"\n{len(total)} distinct items they quest on, that exist in our pack, but our book never asks for.")
    print("By mod:", ", ".join(f"{k} {v}" for k, v in by_mod.most_common(25)))


if __name__ == "__main__":
    main()
